"""
Save 节点：解析摘要行、生成 frontmatter、写入 daily_news/YYYY-MM-DD_daily_news.md。
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config


def _parse_summary_and_content(markdown: str) -> tuple[str, str]:
    """从简报正文中解析首行「摘要：xxx」，返回 (description, 正文去掉该行)。"""
    if not markdown or not markdown.strip():
        return "", markdown
    lines = markdown.strip().split("\n")
    description = ""
    rest: list[str] = []
    
    summary_pattern = re.compile(r"^[*#]*摘要[:：]\s*(.*)$")
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if i == 0:
            match = summary_pattern.match(stripped)
            if match:
                description = match.group(1).rstrip("*# ")
                continue
        rest.append(line)
    body = "\n".join(rest).strip()
    return description, body


def save_node(state: dict) -> dict:
    """将 report_markdown 写入文件，返回 report_path。"""
    report = state.get("report_markdown") or ""
    if state.get("error") or not report.strip():
        return {"report_path": None}

    try:
        config.OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        today = date.today()
        filename = f"{today.isoformat()}_daily_news.md"
        out_path = config.OUTPUT_PATH / filename

        description, body = _parse_summary_and_content(report)
        desc_escaped = (description or "").replace("\n", " ").replace('"', '\\"')[:200]
        title = f"今日 AI 简报 {today.isoformat()}"
        slug = f"daily-{today.isoformat()}"

        frontmatter = f"""---
title: "{title}"
date: "{today.isoformat()}"
description: "{desc_escaped}"
slug: "{slug}"
---

"""
        full_content = frontmatter + body

        out_path.write_text(full_content, encoding="utf-8")
        return {"report_path": str(out_path), "error": None}
    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        return {"report_path": None, "error": str(e)}
