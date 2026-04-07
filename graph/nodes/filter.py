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


from pydantic import BaseModel, Field

class FilterResult(BaseModel):
    keep_indices: list[int] = Field(description="保留条目的下标列表")

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
    structured_llm = llm.with_structured_output(FilterResult)
    last_error = None
    for attempt in range(LLM_RETRY_MAX + 1):
        try:
            result = structured_llm.invoke([HumanMessage(content=prompt)])
            indices = [i for i in result.keep_indices if isinstance(i, int) and 0 <= i < len(raw)]
            filtered = [raw[i] for i in indices] if indices else raw[:15]
            return {"filtered_items": filtered, "error": None}
        except Exception as e:
            last_error = e
            if attempt < LLM_RETRY_MAX:
                time.sleep(LLM_RETRY_DELAY)
    return {"filtered_items": raw[:15], "error": str(last_error)}
