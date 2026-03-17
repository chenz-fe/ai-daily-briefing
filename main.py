#!/usr/bin/env python3
"""
Daily Briefing 入口：加载 .env、构建图、执行一次，生成当日简报。
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
