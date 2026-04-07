#!/usr/bin/env python3
"""
阶段一：通过 Tavily 获取最新 AI 新闻并打印标题与链接（与周报主流程同风格查询）。
运行前请设置 .env 中的 TAVILY_API_KEY。
"""
import os
import sys
from datetime import date
from pathlib import Path

# 确保项目根在 path 中，并优先加载 .env
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

import config
from tavily import TavilyClient


def fetch_ai_news(max_items: int = 8) -> list[dict]:
    """调用 Tavily 搜索 AI 新闻，返回条目列表，每项含 title, url, content(snippet)。"""
    if not config.TAVILY_API_KEY:
        raise ValueError("请设置环境变量 TAVILY_API_KEY（可在 .env 中配置）")

    client = TavilyClient(api_key=config.TAVILY_API_KEY)
    y, w, _ = date.today().isocalendar()
    week_tag = f"{y}-W{w:02d}"
    query = f"{config.TAVILY_SEARCH_QUERIES[0]} news past week {week_tag} {date.today().isoformat()}"
    response = client.search(
        query=query,
        topic="news",
        max_results=max_items,
        search_depth="basic",
    )
    results = getattr(response, "results", None) or response.get("results", [])
    # 统一为 list[dict]，便于后续 Filter 节点复用
    items = []
    for r in results:
        if isinstance(r, dict):
            items.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", ""),
                "source": "tavily",
            })
        else:
            items.append({
                "title": getattr(r, "title", ""),
                "url": getattr(r, "url", ""),
                "content": getattr(r, "content", ""),
                "source": "tavily",
            })
    return items


def main():
    try:
        items = fetch_ai_news(max_items=8)
    except Exception as e:
        print(f"获取失败: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"共获取 {len(items)} 条（展示标题与链接）：\n")
    for i, item in enumerate(items, 1):
        title = (item.get("title") or "").strip() or "(无标题)"
        url = (item.get("url") or "").strip()
        print(f"{i}. {title}")
        print(f"   {url}\n")

    if len(items) < 3:
        print("提示：当前不足 3 条，可检查关键词或 Tavily 配额。", file=sys.stderr)


if __name__ == "__main__":
    main()
