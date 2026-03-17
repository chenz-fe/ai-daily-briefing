"""
图状态定义。各节点接收完整 state，返回「部分更新」dict。
"""
from typing import TypedDict


class BriefingState(TypedDict, total=False):
    """Daily Briefing 图状态。total=False 表示字段可选，便于节点只返回有更新的键。"""
    raw_items: list[dict]       # Search 输出：title, url, content, source 等
    filtered_items: list[dict] # Filter 输出：保留的条目
    report_markdown: str        # Summary 输出：摘要行 + 三章节
    report_path: str | None     # Save 输出：最终文件路径
    error: str | None           # 任意节点出错时写入
