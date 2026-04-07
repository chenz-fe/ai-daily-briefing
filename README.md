# Weekly Briefing（AI 新闻雷达）

基于 LangGraph + Tavily + LLM 的 **每周一次** AI 周报 Agent，自动生成信息密度较高的 Markdown 简报（含产品与工具、模型与场景、大事件、趋势与行动清单）。详见 `docs/01_project_plan.md`，执行清单见 `docs/02_execution_plan.md`，前端界面设计见 `docs/03_frontend_design.md`。

## 环境

- Python 3.10+
- 依赖：`pip install -r requirements.txt`

## 配置

复制 `.env.example` 为 `.env`，并填写：

- **TAVILY_API_KEY**（必填）：[Tavily](https://app.tavily.com) 申请 API Key。
- **LLM**（**强烈建议**）：用于 Filter 筛选与 Summary 生成完整周报。配置 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`，或沿用 `DEEPSEEK_API_KEY` / `DEEPSEEK_BASE_URL` / `DEEPSEEK_MODEL`（与 ai-agent-project 一致）。**未配置时只会输出「标题+链接」的简易列表，内容较单薄。**
- **RSS**：默认拉取 MIT Technology Review、The Verge、36氪、虎嗅、Hacker News 等与 Tavily 合并去重。可选 `RSS_FEEDS`（逗号分隔 URL）覆盖。Tavily 失败时会自动回退到仅 RSS，Filter/Summary 带有限次重试。
- **抓取量**（可选）：`TAVILY_MAX_RESULTS_PER_QUERY`（默认 10）、`TAVILY_QUERY_LIMIT`（默认 5 条查询）控制 Tavily 广度。
- **跨期去重**（可选）：最近 **14** 天内（默认，可用 `BRIEFING_RECENT_URL_DAYS` 调整）已在 `daily_news/*.md`（及历史 JSON）中出现过的链接会被**直接丢弃**，**不会用旧闻补条数**（稿可变短）。每次成功保存后会把本次选用 URL 写入 `.briefing_url_history.json`（已加入 `.gitignore`）。可用 `BRIEFING_URL_HISTORY_PATH` 调整路径。

## 阶段一：信源验收

仅用 Tavily 拉取并打印 AI 新闻（不跑 LangGraph）：

```bash
python fetch_news.py
```

验收：控制台输出至少 3 条最新 AI 新闻的**标题与链接**。

## 阶段二：一键生成周报

运行完整 Agent 生成本次运行当日的周报文件（文件名含日期，便于归档）：

```bash
python main.py
```

输出文件：`daily_news/YYYY-MM-DD_weekly_ai_briefing.md`。

## GitHub Actions

工作流：`.github/workflows/weekly-briefing.yml`，默认 **每周一 00:00 UTC**（约北京时间周一 08:00）执行；也可手动 `workflow_dispatch`。

## 前端

`web/` 目录下为 Vite 阅读页，展示 `daily_news/` 中的 Markdown（兼容历史 `*_daily_news.md` 与当前 `*_weekly_ai_briefing.md`）。
