"""
跨天 URL 去重：读取近期已写入简报的链接，避免 Tavily/RSS 连日返回同一批头条。
"""
from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import config

# 正文里 [text](url) 形式的链接
_MD_LINK_RE = re.compile(r"\]\((https?://[^)\s]+)\)")
_FILENAME_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_daily_news\.md$")


def normalize_url(url: str) -> str:
    """用于去重：主机小写、去 fragment、路径去尾斜杠、去掉常见追踪参数。"""
    s = (url or "").strip()
    if not s:
        return ""
    s = s.split("#", 1)[0].strip()
    try:
        p = urlparse(s)
        scheme = (p.scheme or "https").lower()
        netloc = p.netloc.lower()
        path = (p.path or "").rstrip("/") or "/"
        q = [
            (k, v)
            for k, v in parse_qsl(p.query, keep_blank_values=True)
            if not k.lower().startswith("utm_")
        ]
        query = urlencode(q) if q else ""
        rebuilt = urlunparse((scheme, netloc, path, "", query, ""))
        return rebuilt.rstrip("/").lower()
    except Exception:
        return s.lower().rstrip("/")


def _urls_from_markdown_dir(output_dir: Path, min_file_date: date) -> set[str]:
    out: set[str] = set()
    if not output_dir.is_dir():
        return out
    for md in output_dir.glob("*_daily_news.md"):
        m = _FILENAME_DATE_RE.match(md.name)
        if not m:
            continue
        try:
            d = date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if d < min_file_date:
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        for u in _MD_LINK_RE.findall(text):
            nu = normalize_url(u)
            if nu:
                out.add(nu)
    return out


def _urls_from_history_json(path: Path, min_entry_date: date) -> set[str]:
    out: set[str] = set()
    if not path.exists():
        return out
    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return out
    for entry in data.get("entries", []):
        ds = entry.get("date") or ""
        try:
            d = date.fromisoformat(str(ds)[:10])
        except ValueError:
            continue
        if d < min_entry_date:
            continue
        for u in entry.get("urls") or []:
            nu = normalize_url(str(u))
            if nu:
                out.add(nu)
    return out


def load_recent_briefing_urls() -> set[str]:
    """最近 BRIEFING_RECENT_URL_DAYS 个日历日内出现在简报中的 URL（规范化后）。"""
    days = max(1, int(getattr(config, "BRIEFING_RECENT_URL_DAYS", 7)))
    min_date = date.today() - timedelta(days=days)
    hist_path = getattr(config, "BRIEFING_URL_HISTORY_PATH", None) or (
        config.PROJECT_ROOT / ".briefing_url_history.json"
    )
    combined = _urls_from_history_json(Path(hist_path), min_date)
    combined |= _urls_from_markdown_dir(config.OUTPUT_PATH, min_date)
    return combined


def prioritize_unseen_urls(items: list[dict], recent_urls: set[str]) -> list[dict]:
    """只保留近期未在简报中出现过的条目；宁可条数变少也不回填旧闻。"""
    if not items:
        return []
    out: list[dict] = []
    for it in items:
        u = normalize_url((it.get("url") or "").strip())
        if u and u in recent_urls:
            continue
        out.append(it)
    return out


def record_briefing_urls(for_date: str, urls: list[str], max_entries: int = 21) -> None:
    """将本日选用的原文链接写入 JSON，滚动保留最近 max_entries 天。"""
    hist_path = Path(
        getattr(config, "BRIEFING_URL_HISTORY_PATH", None)
        or (config.PROJECT_ROOT / ".briefing_url_history.json")
    )
    hist_path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, Any] = {"entries": []}
    if hist_path.exists():
        try:
            data = json.loads(hist_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {"entries": []}
    entries: list[dict[str, Any]] = list(data.get("entries", []))
    entries = [e for e in entries if e.get("date") != for_date]
    norm = []
    seen: set[str] = set()
    for u in urls:
        n = normalize_url(u)
        if not n or n in seen:
            continue
        seen.add(n)
        norm.append(n)
    entries.append({"date": for_date[:10], "urls": norm})
    entries.sort(key=lambda e: str(e.get("date", "")))
    if len(entries) > max_entries:
        entries = entries[-max_entries:]
    data["entries"] = entries
    hist_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
