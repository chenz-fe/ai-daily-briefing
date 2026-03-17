# Daily Briefing — 执行计划表

> 基于 `docs/01_project_plan.md` 拆解的可执行任务清单，按阶段推进，完成一项勾选一项。

**图例**：`[ ]` 未开始　`[x]` 已完成

---

## 阶段一：信源接入 — Tavily 获取信息

| 状态 | 序号 | 任务 | 说明 | 产出/验收 |
|------|------|------|------|-----------|
| [x] | 1.1 | 创建项目骨架 | 建目录、config、依赖、环境示例 | `config.py`、`requirements.txt`、`.env.example`、`daily_news/.gitkeep` 就绪 |
| [x] | 1.2 | 接入 Tavily | 关键词 → Tavily API → 结果列表 | `fetch_news.py` 可返回多条条目（title + url + content） |
| [x] | 1.3 | 阶段一验收 | 运行脚本，确认信源可用 | 本地执行 `python fetch_news.py`，控制台打印 ≥3 条最新 AI 新闻标题与链接 |

**阶段一完成标志**：不依赖 LangGraph，单独跑一个脚本就能拿到 Tavily 的 AI 新闻列表。

---

## 阶段二：LangGraph 图与 Filter / Summary / Save

| 状态 | 序号 | 任务 | 说明 | 产出/验收 |
|------|------|------|------|-----------|
| [x] | 2.1 | State 与建图 | 定义 state，用 StateGraph 建线性四节点图 | `graph/state.py`、`graph/build.py`，图可 compile |
| [x] | 2.2 | Search 节点 | Tavily 封装为节点，写 state.raw_items | `graph/nodes/search.py`，输出 raw_items |
| [x] | 2.3 | Filter 节点 | LLM 过滤无关/广告，输出 filtered_items | `graph/nodes/filter.py`、`prompts/filter_prompt.txt` |
| [x] | 2.4 | Summary 节点 | 用 prompt 模板基于 filtered_items 生成简报 | `graph/nodes/summary.py`、`prompts/summary_prompt.txt`，输出含摘要+三章节 |
| [x] | 2.5 | Save 节点 | 解析摘要、frontmatter，写入文件 | `graph/nodes/save.py`，生成 `daily_news/YYYY-MM-DD_daily_news.md` |
| [x] | 2.6 | 主入口 | main.py 构建图并 invoke | `main.py`，单次运行生成当日简报 |
| [x] | 2.7 | 阶段二验收 | 端到端跑通，内容符合规范 | 运行 `python main.py`，得到一份日报：frontmatter + 摘要 + 三章节 |

**阶段二完成标志**：`python main.py`（或等价命令）即可生成当日 `YYYY-MM-DD_daily_news.md`，内容可读、结构正确。

---

## 阶段三：可选增强（阶段二验收通过后再做）

| 状态 | 序号 | 任务 | 说明 | 产出/验收 |
|------|------|------|------|-----------|
| [x] | 3.1 | RSS 补充 | Search 内增加 1～2 个 RSS，与 Tavily 合并去重 | 默认 MIT Tech Review + The Verge；可配置 RSS_FEEDS |
| [x] | 3.2 | 错误与重试 | Search/Filter/Summary 有限次重试；Tavily 失败可回退 RSS | Tavily 重试 3 次；Filter/Summary 各重试 3 次；Tavily 全败仍可出报 |
| [ ] | 3.3 | Save 接入 MCP | 通过 Filesystem MCP 写入 daily_news/ | 可选，与 Cursor 等 MCP 生态集成 |
| [ ] | 3.4 | 与前端/CI 集成 | 生成目录可被拷贝到前端 content；脚本或 Actions | 可选，按需做 |

**阶段三**：按需挑选，不阻塞主流程。

---

## 收尾与文档

| 状态 | 任务 | 说明 |
|------|------|------|
| [ ] | README 完善 | 运行方式、环境变量、验收标准与自测方法（对应 docs/01_project_plan.md §7） |
| [ ] | 可选：单测 / E2E | `tests/` 下对单节点或整图做简单测试 |

---

## 建议执行顺序（依赖关系）

```
1.1 → 1.2 → 1.3
  ↓
2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6 → 2.7
  ↓
（按需）3.1 / 3.2 / 3.3 / 3.4
  ↓
README 完善
```

- 阶段一与阶段二为顺序依赖；阶段三各项可并行或选做。
- 2.1 的 state 与建图可先做「空节点」占位，再逐个实现 2.2～2.5。

