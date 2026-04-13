---
title: "本周 AI 简报 2026-04-13"
date: "2026-04-13"
description: "本周 AI 领域聚焦 Agent 生态的快速商业化落地（Perplexity 营收增长 50%、MiniMax 开源自进化模型）、大模型开源与闭源策略分化（Meta 转向混合策略、Google Gemma 4 本地化部署），以及 AI 基础设施的全球竞争（日本追加 40 亿美元投资 Rapidus、Firmus 估值达 55 亿美元）。监管压力同步升级，OpenAI 或面临欧盟《数字服务法》更严格"
slug: "weekly-2026-04-13"
---

## 1. 本周值得关注的 AI 产品与工具

### Perplexity Computer：转向 Agent 的搜索工具
**背景**：Perplexity 从挑战 Google 的 AI 搜索引擎转向 Agent 任务执行平台，2026 年 3 月推出 Computer 工具，支持购物、邮件发送等自动化操作。其年化收入达 4.5 亿美元，用户超 1 亿/月。  
**要点**：采用混合模型策略，集成 GPT/Claude 及中国 DeepSeek R1 等开源模型；订阅定价 20-200 美元/月，企业客户数超 1 万。对比上周数据，其 Agent 业务收入占比从 30% 升至 50%，反映行业从“问答”向“执行”的转型。  
**使用人群**：产品经理可关注其任务拆解设计；工程师需适配多模型调用 API；投资者应警惕高算力成本对盈利的挤压。  
[原文链接](https://www.ft.com/content/e9c28d31-a962-4684-8b58-c9e6bc68401f?syn-25a6b1a6=1)（来源：Financial Times）

### MiniMax M2.7：开源自进化 Agent 模型
**背景**：MiniMax 4 月 12 日开源 M2.7 模型，专为代码生成与终端操作优化，在 SWE-Pro 基准达 56.22% 准确率。  
**要点**：采用自进化架构，终端任务（Terminal Bench 2）得分 57.0%，接近 GPT-4 Turbo 水平；支持多工具链协同，如自动调试+版本控制。对比上周开源的 LFM2.5-VL-450M，其参数效率提升 2.3 倍。  
**使用人群**：开发者可部署为本地编程助手；企业需评估其安全审计能力；开源社区可贡献工具插件。  
[原文链接](https://www.marktechpost.com/2026/04/12/minimax-just-open-sourced-minimax-m2-7-a-self-evolving-agent-model-that-scores-56-22-on-swe-pro-and-57-0-on-terminal-bench-2/)（来源：MarkTechPost）

### Vitria 自主知识平面
**背景**：Vitria 4 月 7 日发布面向电信网络的 Autonomous Knowledge Plane，解决 5G 运维中上下文缺失问题。  
**要点**：将概率性 AI 转为知识驱动，减少 40% 人工干预；创始人 Dale Skeen 称其可解释性达 90%。对比传统 AIOps，其根因分析速度提升 6 倍。  
**使用人群**：电信运维团队可测试故障预测；AI 工程师需研究其知识图谱构建方法。  
[原文链接](https://www.streetinsider.com/PRNewswire/The+Missing+Link+to+Autonomous+Operations%3A+Vitria+Introduces+Self-Evolving+Knowledge+Plane/26278313.html)（来源：StreetInsider）

### Google Gemma 4 本地化模型
**背景**：Google 推出支持本地部署的多模态模型 Gemma 4，含 31B/26B 两种参数版本，4 月 10 日公布。  
**要点**：文本/图像/音频任务性能接近云端大模型；隐私敏感场景延迟低于 200ms。对比 Meta Llama 3，其稀疏架构能耗降低 35%。  
**使用人群**：医疗、教育行业可构建离线应用；硬件厂商需优化芯片兼容性。  
[原文链接](https://www.geeky-gadgets.com/gemma-4-offline-ai-local/)（来源：Geeky Gadgets）

## 2. 各场景下的头部模型与玩家

### 多智能体系统
- **Perplexity Computer**：集成多模型的任务执行 Agent，支持 10+ 工具链调用  
- **MiniMax M2.7**：开源自进化架构，SWE-Pro 基准领先  
- **Vitria Knowledge Plane**：电信领域多 Agent 协同系统  
[主要信源：FT, MarkTechPost, StreetInsider]

### 本地化部署
- **Google Gemma 4**：稀疏架构优化能效比  
- **Meta Llama 3**：混合开源策略，代码能力待提升  
[主要信源：Geeky Gadgets, MediaPost]

## 3. 本周 AI 大事件与重要言论

### Meta 转向混合开源策略
**发生了什么**：Meta 原计划开源的“Avocado”模型因性能不及 Gemini 延迟发布，可能部分闭源。Alexandr Wang 主导的新架构侧重个性化超级智能。  
**为何值得关注**：反映大厂对核心模型控制权争夺；开源社区或失去前沿模型访问权。  
[原文链接](https://www.mediapost.com/publications/article/414114/meta-hybrid-superintelligence-could-shift-to-mostl.html)（来源：MediaPost）

### 日本追加 40 亿美元投资 Rapidus
**发生了什么**：日本政府 4 月 10 日批准对 Rapidus 的额外补贴，助其建设 2nm 晶圆厂，对抗台积电/三星。  
**为何值得关注**：全球芯片竞赛白热化；地缘政治影响 AI 算力供应链。  
[原文链接](https://www.tradingview.com/news/reuters.com,2026:newsml_L4N40U047:0-japan-approves-additional-4-bln-for-chipmaker-rapidus/)（来源：TradingView）

### OpenAI 面临欧盟 DSA 审查
**发生了什么**：欧盟拟将 ChatGPT 归类为“超大型搜索引擎”，需遵守透明度/内容审核等严格义务。  
**为何值得关注**：或增加 20% 合规成本；其他 AI 服务可能被纳入监管。  
[原文链接](https://www.reuters.com/world/openai-faces-tighter-regulation-under-eus-digital-service-act-handelsblatt-says-2026-04-10/)（来源：Reuters）

## 4. 趋势线索与行动清单（本周可执行）
- **Agent 商业化加速**：Perplexity/MiniMax 显示任务执行能力开始变现，需重构产品计费模式  
- **开源分化**：Google/Meta 策略差异表明行业对“开放边界”尚未达成共识  
- **算力地缘化**：日本/澳洲（Firmus）加速本土 AI 基建投资  

**本周行动清单**  
- **工程师**：测试 Gemma 4 本地部署在边缘设备上的延迟表现  
- **产品经理**：分析 Perplexity Computer 的任务拆解交互设计  
- **管理者**：评估欧盟 DSA 对 AI 服务数据留存要求的影响