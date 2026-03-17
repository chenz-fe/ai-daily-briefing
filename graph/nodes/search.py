"""
Search 节点：Tavily 多关键词搜索 + 可选 RSS，合并去重；带重试，Tavily 失败时回退到仅 RSS。
"""
import time
import sys
from pathlib import Path
from urllib.parse import urlparse
import difflib
from typing import Optional
import os

# 项目根
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
from tavily import TavilyClient

try:
    import feedparser
except ImportError:
    feedparser = None


# 重试配置（3.2）
TAVILY_MAX_RETRIES = 3
TAVILY_RETRY_DELAY = 2.0
LLM_RETRY_MAX = 2
LLM_RETRY_DELAY = 1.0


def _fetch_rss() -> list[dict]:
    """拉取 config.RSS_FEEDS 中的 RSS，返回与 raw_items 同结构的 list。"""
    if not getattr(config, "RSS_FEEDS", None) or not feedparser:
        return []
    items = []
    for feed_url in config.RSS_FEEDS[:5]:  # 最多 5 个源
        try:
            parsed = feedparser.parse(feed_url)
            label = parsed.feed.get("title", urlparse(feed_url).netloc or "rss")[:30]
            for e in getattr(parsed, "entries", [])[:15]:  # 每源最多 15 条
                link = (e.get("link") or "").strip()
                if not link:
                    continue
                title = (e.get("title") or "").strip()
                content = (e.get("summary") or e.get("description") or "")
                if content and hasattr(content, "replace"):
                    try:
                        import re
                        content = re.sub(r"<[^>]+>", " ", content)[:1200]
                    except Exception:
                        content = content[:1200] if isinstance(content, str) else ""
                else:
                    content = ""
                items.append({
                    "title": title or "(无标题)",
                    "url": link,
                    "content": content,
                    "source": label,
                })
        except Exception:
            continue
    return items


def _fetch_tavily() -> list[dict]:
    """调用 Tavily 多查询，合并去重，返回 raw_items。"""
    if not config.TAVILY_API_KEY:
        return []
    client = TavilyClient(api_key=config.TAVILY_API_KEY)
    seen_urls: set[str] = set()
    all_items: list[dict] = []
    max_per_query = 5
    for query in config.TAVILY_SEARCH_QUERIES[:3]:
        response = client.search(
            query=query,
            topic="news",
            max_results=max_per_query,
            search_depth="advanced",
        )
        results = getattr(response, "results", None) or getattr(response, "results", [])
        if not results and isinstance(response, dict):
            results = response.get("results", [])
        for r in results:
            url = (r.get("url") if isinstance(r, dict) else getattr(r, "url", "")) or ""
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            all_items.append({
                "title": r.get("title", "") if isinstance(r, dict) else getattr(r, "title", ""),
                "url": url,
                "content": r.get("content", "") if isinstance(r, dict) else getattr(r, "content", ""),
                "source": "tavily",
            })
    return all_items


def search_node(state: dict) -> dict:
    """Tavily（带重试）+ RSS，合并按 url 去重；Tavily 全失败时仅返回 RSS。"""
    seen: set[str] = set()
    seen_titles: list[str] = []
    combined: list[dict] = []
    tavily_error: Optional[str] = None

    def add_if_not_duplicate(item: dict):
        u = (item.get("url") or "").strip()
        t = (item.get("title") or "").strip()
        
        if u and u in seen:
            return
            
        if t:
            t_lower = t.lower()
            for st in seen_titles:
                # 使用标题相似度去重，如果大于 0.8 则认为是同一条新闻
                if difflib.SequenceMatcher(None, t_lower, st).ratio() > 0.8:
                    return
            seen_titles.append(t_lower)
            
        if u:
            seen.add(u)
        combined.append(item)

    # 1) Tavily：有限次重试
    for attempt in range(TAVILY_MAX_RETRIES):
        try:
            if not config.TAVILY_API_KEY:
                tavily_error = "未配置 TAVILY_API_KEY"
                break
            items = _fetch_tavily()
            for it in items:
                add_if_not_duplicate(it)
            tavily_error = None
            break
        except Exception as e:
            tavily_error = str(e)
            print(f"DEBUG: Tavily fetch attempt {attempt + 1} failed: {e}", file=sys.stderr)
            if attempt < TAVILY_MAX_RETRIES - 1:
                time.sleep(TAVILY_RETRY_DELAY)

    # 2) RSS：与 Tavily 合并去重；Tavily 失败时 RSS 作唯一信源
    # 增加临时代理绕过（如果是因为代理导致无法访问RSS）
    old_proxy = os.environ.get("HTTP_PROXY")
    old_proxys = os.environ.get("HTTPS_PROXY")
    os.environ["HTTP_PROXY"] = ""
    os.environ["HTTPS_PROXY"] = ""
    
    rss_items = _fetch_rss()
    print(f"DEBUG: Fetched {len(rss_items)} items from RSS", file=sys.stderr)
    
    if old_proxy is not None:
        os.environ["HTTP_PROXY"] = old_proxy
    if old_proxys is not None:
        os.environ["HTTPS_PROXY"] = old_proxys
        
    for it in rss_items:
        add_if_not_duplicate(it)

    # 有任意信源即成功；仅当全部失败才返回 error
    if not combined and tavily_error:
        return {"raw_items": [], "error": tavily_error}
    return {"raw_items": combined, "error": None}
