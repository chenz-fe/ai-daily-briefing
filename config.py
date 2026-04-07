# Weekly Briefing 配置（目录名 daily-briefing 为历史保留）
# 从环境变量加载，便于本地与 CI 复用

import os
from pathlib import Path

# 使用 python-dotenv 时在 main 入口 load_dotenv()，此处仅读取 os.environ
def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default).strip()


def _env_int(key: str, default: int) -> int:
    v = _env(key)
    if not v:
        return default
    try:
        return int(v)
    except ValueError:
        return default


# --- Tavily（每周简报：多查询、多结果，覆盖产品与模型/基础设施/政策等）---
TAVILY_API_KEY = _env("TAVILY_API_KEY")
TAVILY_SEARCH_QUERIES = [
    "Top AI news breakthroughs and product launches",
    "AI Agents autonomous systems enterprise",
    "LLM foundation models API pricing benchmarks 2026",
    "AI regulation policy chips compute datacenter",
    "RAG multimodal AI developer tools open source",
]
# 每条查询返回条数上限（每周一次可拉高，避免内容单薄）
TAVILY_MAX_RESULTS_PER_QUERY = _env_int("TAVILY_MAX_RESULTS_PER_QUERY", 10)
# 实际执行前 N 条查询（全部跑满可能耗时与配额更高）
TAVILY_QUERY_LIMIT = _env_int("TAVILY_QUERY_LIMIT", 5)

# --- RSS（阶段三，与 Tavily 合并去重）---
# 可选：通过环境变量 RSS_FEEDS 覆盖（逗号分隔的 URL）
_RSS_ENV = _env("RSS_FEEDS")
RSS_FEEDS = [u.strip() for u in _RSS_ENV.split(",") if u.strip()] if _RSS_ENV else [
    "https://www.technologyreview.com/feed",
    "https://www.theverge.com/rss/index.xml",
    "https://36kr.com/feed",                    # 36氪
    "https://www.huxiu.com/rss/0.xml",         # 虎嗅
    "https://hnrss.org/frontpage",             # Hacker News (hnrss.org)
]

# --- 输出 ---
OUTPUT_DIR = _env("OUTPUT_DIR") or "daily_news"
# 项目根目录（config.py 所在目录的父目录 = daily-briefing）
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = PROJECT_ROOT / OUTPUT_DIR

# --- 跨天去重（最近 N 天内已在简报中出现的 URL 直接丢弃，不补旧闻）---
BRIEFING_RECENT_URL_DAYS = _env_int("BRIEFING_RECENT_URL_DAYS", 14)
# 历史文件（记录每次运行实际选用的条目 URL，供后续搜索去重）
BRIEFING_URL_HISTORY_PATH = Path(
    _env("BRIEFING_URL_HISTORY_PATH") or str(PROJECT_ROOT / ".briefing_url_history.json")
)

# --- LLM（阶段二 Filter / Summary 使用）---
# 支持 LLM_* 或 DEEPSEEK_*（与 ai-agent-project 一致）
LLM_API_KEY = _env("LLM_API_KEY") or _env("DEEPSEEK_API_KEY")
LLM_BASE_URL = _env("LLM_BASE_URL") or _env("DEEPSEEK_BASE_URL")
LLM_MODEL = _env("LLM_MODEL") or _env("DEEPSEEK_MODEL") or "deepseek-chat"
