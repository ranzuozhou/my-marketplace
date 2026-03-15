# Focus Prompt Templates — Studio 制品生成引导模板

## 两层拼接策略

Focus Prompt 由两层组合而成，确保制品既符合格式要求又贴合内容：

1. **Intent Layer** — 基于 artifact_type 选择模板，定义制品的格式和受众
2. **Content Layer** — 从 `notebook_describe()` 提取关键主题词，补充具体内容方向

### 组合公式

```
Focus Prompt = Intent Layer（模板填充） + Content Layer（主题词补充）
```

**语言设置**：使用 `language="zh"`（BCP-47 代码），NLM AI 支持跨语言理解。

---

## Intent Layer 模板

### audio（音频播客）

```
面向{audience}的{topic}技术播客，以通俗易懂的对话形式介绍核心概念和设计决策
```

**适用场景**：新人培训、知识分享、通勤学习
**搭配子参数**：`audio_format="brief"` 概述 / `"deep_dive"` 深入 / `"critique"` 评析 / `"debate"` 辩论

### video（视频概述）

```
面向{audience}的{topic}可视化讲解视频，直观展示架构和流程
```

**适用场景**：技术演示、可视化教学
**搭配子参数**：`video_format="explainer"` 讲解 / `"brief"` 简要 / `"cinematic"` 电影风格

### infographic（信息图）

```
面向{audience}的{topic}信息图，可视化展示核心架构、数据流和关键指标
```

**适用场景**：架构可视化、流程展示、数据对比
**搭配子参数**：`infographic_style="professional"` 专业 / `"sketch_note"` 手绘 / `"bento_grid"` 卡片式

### slide_deck（幻灯片）

```
面向{audience}的{topic}技术演示，结构清晰、重点突出，适合{minutes}分钟的技术分享
```

**适用场景**：技术分享会、团队培训、架构评审
**搭配子参数**：`slide_format="detailed_deck"` 详细 / `"presenter_slides"` 演讲者版

### report — Briefing Doc（简报文档）

```
面向{audience}的{topic}技术简报，提炼关键信息和决策要点，适合快速了解全貌
```

**适用场景**：管理层汇报、跨团队沟通
**使用**：`report_format="Briefing Doc"`

### report — Study Guide（学习指南）

```
帮助{audience}系统学习{topic}的指南，包含知识点梳理、学习路径和自测问题
```

**适用场景**：新人入职培训、技能提升
**使用**：`report_format="Study Guide"`

### report — Blog Post（博客文章）

```
面向{audience}的{topic}技术博客，以叙事方式介绍背景、实现和经验总结
```

**适用场景**：技术分享、知识沉淀
**使用**：`report_format="Blog Post"`

### report — Create Your Own（自定义）

```
{自定义格式描述}
```

**适用场景**：标准格式不满足需求时
**使用**：`report_format="Create Your Own"`, `custom_prompt="{格式描述}"`

### flashcards（闪卡）

```
{topic}的关键概念和要点闪卡，帮助{audience}快速记忆核心知识
```

**适用场景**：培训后复习、知识记忆强化

### quiz（测验）

```
{topic}的知识测验，覆盖{audience}应掌握的核心概念和实践要点
```

**适用场景**：培训考核、自我评估
**搭配子参数**：`question_count=10` 题目数 + `difficulty="medium"` 难度

### data_table（数据表）

```
从{topic}中提取{数据描述}的结构化数据表
```

**适用场景**：数据提取、对比分析
**注意**：`description` 参数必填，需明确描述要提取的数据

### mind_map（思维导图）

```
{topic}的知识图谱，可视化展示核心概念、模块关系和依赖链路
```

**适用场景**：架构可视化、知识梳理

---

## Content Layer 提取方法

1. 调用 `notebook_describe(notebook_id)` 获取 AI 摘要
2. 从摘要中提取 3-5 个关键主题词
3. 将主题词补充到 Intent Layer 模板中
4. 追加元知识引导句（见下方「元知识引导句」）

**提取示例**：

摘要：`"本 notebook 包含 DQV 数据质量验证服务的设计规范、三阶段处理管道（解压→验证→分发）、验证策略和数据库 ETL 模式"`

提取主题词：`三阶段管道`、`验证策略`、`ETL 模式`

#### 元知识引导句（当 Notebook 包含导航 Source 时）

在 Content Layer 末尾追加固定引导句，指导 NLM 利用元知识理解材料结构：

**引导句模板**：
> 参考「内容导航大纲」理解材料间的逻辑关系和推荐阅读顺序，参考「项目上下文」理解知识库的定位和背景

**组合示例**（含元知识引导）：
```
"面向新人开发者的 DQV 三阶段验证管道技术播客，
 重点覆盖解压、验证、分发三个核心阶段，
 参考内容导航大纲理解材料间的逻辑关系和推荐阅读顺序，
 参考项目上下文理解知识库的定位和背景"
```

---

## 组合示例

### 示例 1：DQV 音频播客（audio + deep_dive）

```
artifact_type: audio
audio_format: deep_dive
focus_prompt: "面向后端开发者的 DQV 数据质量验证管道技术播客，重点覆盖解压、验证、分发三个核心阶段及验证策略设计"
```

### 示例 2：全链路幻灯片（slide_deck）

```
artifact_type: slide_deck
slide_format: detailed_deck
focus_prompt: "面向团队的数据收集全链路技术演示，适合 20 分钟的技术分享，覆盖 AEC 邮件收集、DQV 质量验证、QVL 数据加载的端到端流程"
```

### 示例 3：数据库学习指南（report + Study Guide）

```
artifact_type: report
report_format: Study Guide
focus_prompt: "帮助新人 DBA 系统学习 MJ System 数据仓库架构的指南，包含双域设计（ops/biz）、四层模型（ODS→DWD→DWS→ADS）、ETL 模式和命名规范"
```

---

## 受众（audience）常用值

| audience | 适用场景 |
|----------|---------|
| 新人开发者 | 入职培训、基础学习 |
| 后端开发者 | 技术细节、代码级分析 |
| 团队 | 技术分享、Sprint 回顾 |
| 管理层 | 进度汇报、架构决策 |
| DBA | 数据库设计、ETL 优化 |
| DevOps | CI/CD、Docker、部署 |

---

## MJ System 推荐制品组合

| 场景 | 推荐制品 | 原因 |
|------|---------|------|
| **新人入职** | audio(brief) + report(Study Guide) + flashcards | 音频快速了解 → 指南系统学习 → 闪卡强化记忆 |
| **技术分享** | slide_deck + infographic | 幻灯片演示 + 信息图做辅助 |
| **架构评审** | report(Briefing Doc) + mind_map | 简报抓重点 + 思维导图看全局 |
| **深度学习** | audio(deep_dive) + report(Study Guide) + quiz | 深度音频 + 系统指南 + 测验自测 |
| **知识沉淀** | mind_map + report(Blog Post) + data_table | 思维导图结构化 + 博客叙事 + 数据表提取关键信息 |
