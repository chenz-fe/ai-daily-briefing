"""
Summary 节点：基于 filtered_items 用 LLM 生成简报正文（摘要 + 三章节）。带有限次重试（3.2）。
"""
import sys
import time
from pathlib import Path

LLM_RETRY_MAX = 2
LLM_RETRY_DELAY = 1.0

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


def _strip_markdown_fence(text: str) -> str:
    """去掉首尾的 ```markdown 或 ``` 代码块包裹，返回纯正文。"""
    t = text.strip()
    for prefix in ("```markdown\n", "```md\n", "```\n"):
        if t.startswith(prefix):
            t = t[len(prefix):]
            break
    if t.endswith("\n```"):
        t = t[:-4]
    elif t.endswith("```"):
        t = t[:-3]
    return t.strip()


def _load_prompt() -> str:
    p = ROOT / "prompts" / "summary_prompt.txt"
    return p.read_text(encoding="utf-8") if p.exists() else "请根据以下条目生成本周简报 Markdown，首行为「摘要：xxx」，然后四个章节。\n\n{{items_content}}"


def _items_to_content(items: list[dict]) -> str:
    """把条目列表转成给 LLM 的文本。"""
    parts = []
    for i, item in enumerate(items, 1):
        title = item.get("title", "")
        url = item.get("url", "")
        content = item.get("content", "") or item.get("snippet", "")
        source = item.get("source", "tavily")
        # 多给 LLM 原文片段，便于写出背景+要点（advanced 搜索下片段更长，保留 1200 字内）
        snippet = (content or "")[:1600] if content else "(无)"
        parts.append(f"【{i}】{title}\n链接: {url}\n来源: {source}\n内容片段: {snippet}\n")
    return "\n".join(parts)


def summary_node(state: dict) -> dict:
    """根据 filtered_items 生成 report_markdown。"""
    items = state.get("filtered_items") or []
    if state.get("error"):
        return {"report_markdown": ""}
    if not items:
        return {
            "report_markdown": "摘要：本周暂无筛选后的 AI 条目。\n\n## 1. 本周值得关注的 AI 产品与工具\n\n（无）\n\n## 2. 各场景下的头部模型与玩家\n\n（无）\n\n## 3. 本周 AI 大事件与重要言论\n\n（无）\n\n## 4. 趋势线索与行动清单（本周可执行）\n\n（无）"
        }

    # 防溢出：周报可合并更多条目（按 token 由模型侧截断）
    items = items[:28]

    items_content = _items_to_content(items)
    prompt_template = _load_prompt()
    prompt = prompt_template.replace("{{items_content}}", items_content)

    try:
        if not config.LLM_API_KEY:
            # 无 LLM 时仅列条目，并提示配置 LLM 后可生成完整周报
            desc = "本周 AI 条目列表（简易版）。在 .env 中配置 LLM_API_KEY 或 DEEPSEEK_API_KEY 后重新运行，可生成带背景、对比与行动清单的完整周报。"
            lines = [f"摘要：{desc}", ""]
            lines.append("## 1. 本周值得关注的 AI 产品与工具")
            for it in items[:10]:
                title = (it.get("title") or "").strip() or "无标题"
                lines.append(f"- [{title}]({it.get('url', '')})（来源：{it.get('source', '')}）")
            lines.append("\n## 2. 各场景下的头部模型与玩家\n\n（见上方条目）")
            lines.append("\n## 3. 本周 AI 大事件与重要言论")
            for it in items[10:18]:
                title = (it.get("title") or "").strip() or "无标题"
                lines.append(f"- [{title}]({it.get('url', '')})（来源：{it.get('source', '')}）")
            lines.append("\n## 4. 趋势线索与行动清单（本周可执行）\n\n（请配置 LLM 后生成）")
            return {"report_markdown": "\n".join(lines), "error": None}

        llm = ChatOpenAI(
            model=config.LLM_MODEL,
            api_key=config.LLM_API_KEY,
            base_url=config.LLM_BASE_URL or None,
            temperature=0.3,
        )
        last_error = None
        for attempt in range(LLM_RETRY_MAX + 1):
            try:
                msg = llm.invoke([HumanMessage(content=prompt)])
                content = (getattr(msg, "content", "") or str(msg)).strip()
                content = _strip_markdown_fence(content)
                return {"report_markdown": content, "error": None}
            except Exception as e:
                last_error = e
                if attempt < LLM_RETRY_MAX:
                    time.sleep(LLM_RETRY_DELAY)
        return {"report_markdown": "", "error": str(last_error)}
    except Exception as e:
        return {"report_markdown": "", "error": str(e)}
