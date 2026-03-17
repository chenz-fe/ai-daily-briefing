# Daily Briefing（AI 新闻雷达）

基于 LangGraph + Tavily + LLM 的 AI 日报 Agent，自动生成每日简报 Markdown。详见 [00_项目计划.md](00_项目计划.md)，执行清单见 [01_执行计划表.md](01_执行计划表.md)。

## 环境

- Python 3.10+
- 依赖：`pip install -r requirements.txt`

## 配置

复制 `.env.example` 为 `.env`，并填写：

- **TAVILY_API_KEY**（必填）：[Tavily](https://app.tavily.com) 申请 API Key。
- **LLM**（阶段二，**强烈建议**）：用于 Filter 筛选与 Summary 生成「背景+要点」的完整简报。配置 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`，或沿用 `DEEPSEEK_API_KEY` / `DEEPSEEK_BASE_URL` / `DEEPSEEK_MODEL`（与 ai-agent-project 一致）。**未配置时只会输出「标题+链接」的简易列表，内容较单薄。**
- **RSS**（阶段三）：默认拉取 MIT Technology Review + The Verge 与 Tavily 合并去重。可选 `RSS_FEEDS`（逗号分隔 URL）覆盖。Tavily 失败时会自动回退到仅 RSS，Filter/Summary 带有限次重试。

## 阶段一：信源验收

仅用 Tavily 拉取并打印 AI 新闻（不跑 LangGraph）：

```bash
python fetch_news.py
```

验收：控制台输出至少 3 条最新 AI 新闻的**标题与链接**。

## 阶段二：一键生成简报

运行完整 Agent 生成当日简报：

```bash
python main.py
```

输出文件：`daily_news/YYYY-MM-DD_daily_news.md`。
