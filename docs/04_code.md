作为你的 AI 编程导师，我来帮你梳理一下当前 `@ai/daily-briefing` 项目的核心代码逻辑，并对照学习计划帮你查漏补缺。

### 🧠 核心代码解读

你的项目完全遵循了 LangGraph 的标准设计模式（类似于前端的 Redux 状态流转），核心逻辑如下：

1. **全局状态 (State)**：
  - 在 `graph/state.py` 中，你定义了 `BriefingState`。这就像是 React 中的全局 Context 或 Redux Store，数据在这个管道中单向流动：`raw_items` -> `filtered_items` -> `report_markdown` -> `report_path`。
2. **Search 节点 (信息收集)**：
  - `graph/nodes/search.py` 负责“看世界”。你不仅用了 **Tavily API**，还加入了 **RSS 兜底**。
  - **亮点**：你实现了基于 `difflib.SequenceMatcher` 的标题相似度去重，以及错误重试机制。这在实际工程中非常实用。
3. **Filter 节点 (信息降噪)**：
  - `graph/nodes/filter.py` 负责“洗数据”。
  - **亮点**：你使用了 LangChain 的 `with_structured_output(FilterResult)`。这非常关键！它强制 LLM 输出结构化的 JSON（返回保留条目的索引），而不是随意发散的文本。这就像是给 API 响应加了 TypeScript 接口校验一样稳健。
4. **Summary 节点 (内容生成)**：
  - `graph/nodes/summary.py` 负责“写文章”。将过滤后的数据拼接成 Prompt，让 LLM 按照固定的三个章节输出 Markdown 格式的简报。
5. **Save 节点 (持久化)**：
  - `graph/nodes/save.py` 负责“存结果”。提取摘要并拼接标准的 Frontmatter（包含 title, date, slug 等），最后写入 `daily_news` 目录。
6. **图的组装 (Graph Build)**：
  - `graph/build.py` 将上述节点串联起来。你还巧妙地使用了 `add_conditional_edges`，如果 Filter 节点把所有新闻都过滤掉了，图就会直接走向 `END`，避免无意义的 LLM 调用。

---

