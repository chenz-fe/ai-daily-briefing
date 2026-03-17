"""
Filter 节点：LLM 过滤 raw_items，保留与 AI 相关、非广告的条目。带有限次重试（3.2）。
"""
import json
import re
import sys
import time
from pathlib import Path

LLM_RETRY_MAX = 2   # 最多重试 2 次，共 3 次调用
LLM_RETRY_DELAY = 1.0

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


def _load_prompt() -> str:
    p = ROOT / "prompts" / "filter_prompt.txt"
    return p.read_text(encoding="utf-8") if p.exists() else "请保留与 AI 相关的条目，输出 JSON: {\"keep_indices\": [0,1,2]}"


def _parse_keep_indices(text: str, n: int) -> list[int]:
    """从 LLM 输出中解析 keep_indices，合法下标在 [0, n-1]。"""
    text = text.strip()
    # 去掉可能的 markdown 代码块
    if "```" in text:
        for part in re.split(r"```\w*\n?", text):
            if "keep_indices" in part or "[" in part:
                text = part
                break
    try:
        obj = json.loads(text)
        indices = obj.get("keep_indices", obj.get("keep_indices", []))
    except json.JSONDecodeError:
        # 尝试从行内提取 [0, 1, 2]
        m = re.search(r"\[[\s\d,]+\]", text)
        if m:
            try:
                indices = json.loads(m.group())
            except json.JSONDecodeError:
                indices = []
        else:
            indices = []
    if not isinstance(indices, list):
        indices = []
    return [i for i in indices if isinstance(i, int) and 0 <= i < n]


def filter_node(state: dict) -> dict:
    """根据 raw_items 调用 LLM 筛选，返回 filtered_items。"""
    raw = state.get("raw_items") or []
    if not raw:
        return {"filtered_items": [], "error": None}
    if state.get("error"):
        return {"filtered_items": []}

    items_text = "\n".join(
        f"[{i}] {item.get('title', '')} | {item.get('url', '')}"
        for i, item in enumerate(raw)
    )
    prompt_template = _load_prompt()
    prompt = prompt_template.replace("{{items_text}}", items_text)

    if not config.LLM_API_KEY:
        return {"filtered_items": raw, "error": None}
    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL or None,
        temperature=0.1,
    )
    last_error = None
    for attempt in range(LLM_RETRY_MAX + 1):
        try:
            msg = llm.invoke([HumanMessage(content=prompt)])
            content = getattr(msg, "content", "") or str(msg)
            indices = _parse_keep_indices(content, len(raw))
            filtered = [raw[i] for i in indices] if indices else raw[:5]
            return {"filtered_items": filtered, "error": None}
        except Exception as e:
            last_error = e
            if attempt < LLM_RETRY_MAX:
                time.sleep(LLM_RETRY_DELAY)
    return {"filtered_items": raw[:5], "error": str(last_error)}
