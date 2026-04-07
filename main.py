#!/usr/bin/env python3
"""
Weekly Briefing 入口：加载 .env、构建图、执行一次，生成本周 AI 简报（Markdown）。
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from graph.build import build_graph


def main():
    graph = build_graph()
    initial: dict = {}
    result = graph.invoke(initial)
    
    # 增加调试输出
    print(f"DEBUG: raw_items count = {len(result.get('raw_items', []))}")
    print(f"DEBUG: filtered_items count = {len(result.get('filtered_items', []))}")
    print(f"DEBUG: report_markdown length = {len(result.get('report_markdown', ''))}")
    if result.get("error"):
        print(f"DEBUG: error = {result.get('error')}")

    path = result.get("report_path")
    if result.get("error"):
        print(f"警告: {result['error']}", file=sys.stderr)
    if path:
        print(f"已生成: {path}")
    else:
        print("未生成文件（report_markdown 可能为空或 Save 失败）", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
