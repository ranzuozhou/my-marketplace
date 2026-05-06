# Focus Prompt Templates v2 — 学习导向 Studio 制品引导模板

> v2 版本说明：v2 重写为「学习闭环」导向（参考方法论 §4「不要让 NotebookLM 总结内容，要让它生成理解路径」）。v1 是「技术分享 / 培训」导向，保留为 `legacy_*` 别名，v2.3 移除。

## 三层拼接策略

Focus Prompt 由三层组合而成：

1. **Intent Layer** — 基于 artifact_type + view（学习视角）选模板
2. **Content Layer** — 从 `notebook_describe()` + `00c-定向-` 领域定向报告提取主题词
3. **Guardrails Layer** — 自动追加幻觉防护约束（详见 `→ ./risk-control-templates.md#2`）

```
Focus Prompt = Intent Layer + Content Layer + Guardrails Layer
```

**语言**：`language="zh"`（中文输出，BCP-47）。

**v2 与 v1 的关键差异**：
- Intent Layer 不再写"面向开发者的技术播客"，而是写"零基础学习者从陌生到理解的进入材料"
- 强制引用 `00c-定向-{topic}` 领域定向报告作为锚
- Guardrails Layer 默认追加（除非 `disable_guardrails=True`）

---

## Intent Layer 模板（按 artifact_type × view 组合）

### audio（音频播客）

#### audio + view=foundation（零基础版）

```
面向{audience}的{topic}零基础版音频。

主持人 A 与 B 用对话方式：
- A 假设听众没有任何背景，用日常生活类比开场
- B 不断追问"普通人会怎么误解这个？"
- 每引入一个术语，先用日常语言解释再说专业定义
- 长度控制在 brief，先降低进入门槛

结尾给"听完后我现在能回答的 3 个最简单问题"。

【参考】参考 00c 领域定向报告中的"原始困惑翻译"和"术语翻译表"。
```

#### audio + view=structural（结构版）

```
面向{audience}的{topic}结构版音频，5 分钟一节小结。

主持人 A 解释概念，主持人 B 不断追问：
- 这个概念和相邻概念的区别是什么？
- 什么时候不适用？适用边界在哪？
- 新手最容易误解什么？

每个核心概念配：定义 → 最小例子 → 反例 → 常见误解。

结尾给"听完后必须能回答的 5 个问题"。

【参考】参考 00c 领域定向报告中的"核心概念地图"和"成功失败案例"。
```

#### audio + view=challenge（挑战版）

```
面向{audience}的{topic}挑战版音频。

主持人 A 抛出 3 个"看似适用但不适用"的边界情形，B 分析为什么不适用。

至少包含：
- 3 个反例（含分析 why）
- 2 个迁移应用题（把原则用到相邻领域）
- 5 道"如果错答说明哪个概念没掌握"的诊断题

不要凑长度，密度高于时长。

【参考】参考 00c 领域定向报告中的"成功失败案例的机制"。
```

#### audio（默认，向后兼容）

```
面向{audience}的{topic}多形态学习音频，作为陌生主题的「第一遍进入」。

要求：
1. 用一个现实困惑开场，假设听众没有背景
2. 解释这个领域能解决什么、不能解决什么
3. 用 3 个成功案例 + 3 个失败案例对比说明
4. 建立概念地图（核心 / 相邻 / 前置 / 误解）
5. 每个抽象概念配最小例子和反例
6. 5 分钟一节小结
7. 结尾给"听完后我应该能回答的 5 个问题"

语气：耐心的老师。避免营销式夸张、过度简化、无来源依据的结论。
```

---

### video（视频概述）

#### video（默认）

```
面向{audience}的{topic}视频概述，作为第一遍进入主题的可视化讲解。

按以下结构：
1. 现实困惑开场（为什么需要理解这个？）
2. 领域能做什么 / 不能做什么
3. 3 个成功案例（何时有用）
4. 3 个失败案例（何时会误导）
5. 概念地图（核心 / 相邻 / 前置 / 误解）
6. 最小例子 + 反例
7. 看完应能回答的 5 个问题

风格：耐心讲解，避免堆砌术语。
【参考】参考 00c 领域定向报告。
```

#### video + view=foundation/structural/challenge

同 audio 三版的精神，针对 video 改写：foundation 多类比、structural 重概念地图、challenge 重反例与迁移题。

---

### slide_deck（幻灯片）

#### slide_deck（默认）

```
面向{audience}的{topic}可复习讲义（不是营销汇报）。

每页只讲一个核心点，多用图解 / 流程图 / 对比表，避免长段文字。

结构：
1. 标题：本主题在解决什么问题？
2. 新手原始困惑（不用术语描述）
3. 领域地图（属于什么大领域、与哪些相邻领域容易混）
4. 核心概念 1：定义 / 用途 / 最小例子 / 反例 / 常见误解
5. 核心概念 2：同上
6. 核心概念 3：同上
7. 成功案例：为什么成功 / 依赖什么条件
8. 失败案例：为什么失败 / 误用了什么概念
9. 判断清单：遇到新问题时如何判断本知识是否适用
10. 自测题（5 道）：定义 / 例子 / 反例 / 迁移

【参考】参考 00c 领域定向报告中的"学习路线"和"核心概念地图"。
```

#### slide_deck + view=foundation/structural/challenge

参考 audio 三版精神。

---

### infographic（信息图）

```
{topic}的可视化信息图，单页可读完。

要素：
- 中心放领域核心问题
- 周围放 5-7 个核心概念（含一句话定义）
- 标出 2-3 个常见误解（红色警示）
- 角落放 1 个成功案例 + 1 个失败案例的关键差异
- 底部放一行"判断本知识是否适用"的判断清单

【参考】参考 00c 领域定向报告。
```

---

### report（报告文档）

#### report — Briefing Doc（简报）

```
面向{audience}的{topic}简报文档，提炼关键信息和决策要点。

要求：
1. 一段大图描述（不超过 200 字）
2. 5 个关键判断（每条引用具体 source）
3. 3 个成功 / 3 个失败案例的机制对比表
4. 风险与不确定项清单
5. 推荐下一步行动

【参考】参考 00c 领域定向报告。
```

#### report — Study Guide（学习指南）

```
帮助{audience}系统学习{topic}的指南。

按以下结构：
1. 学习路线（从零基础到能理解，列每段需读哪些 source）
2. 核心概念地图（含前置 / 高级标注）
3. 术语翻译表（20 个，含日常语言/专业定义/最小例子/反例/常见误解）
4. 成功 / 失败案例机制分析
5. 自测问题（10 道，按定义 / 例子 / 反例 / 迁移分类）
6. 判断清单（遇到新问题时的适用性判断）

【参考】参考 00c 领域定向报告 + 00a 内容导航大纲。
```

#### report — Blog Post（博客）

```
{topic}的技术博客（叙事风格）。

按以下结构：
1. 用一个具体故事开场（来自来源中的案例）
2. 引出领域问题
3. 解释关键概念，逐层深入
4. 经验与教训（含失败案例）
5. 给读者的可迁移原则

【参考】参考 00c 领域定向报告。
```

#### report — Glossary（术语词典，新增）

调用方式：`report_format="Create Your Own"`, `custom_prompt=<§6 术语翻译模板>`，详见 `→ ./learning-loop-templates.md#§6`。

#### report — Mechanism Analysis（机制分析，新增）

调用方式：`report_format="Create Your Own"`, `custom_prompt=<§4 成功失败案例机制分析>`，详见 `→ ./learning-loop-templates.md#§4`。

---

### flashcards（闪卡）

```
{topic}的核心概念与要点闪卡。

每张卡：
- 正面：1 个术语 / 1 个概念问题 / 1 个反例情形
- 背面：日常语言 + 专业定义 + 最小例子 + 反例

至少包含：
- 10 张定义类
- 5 张反例类
- 5 张迁移类（"如果场景变成 X，本概念是否适用？"）

【参考】参考 00c 领域定向报告。
```

---

### quiz（测验）

```
{topic}的知识测验，覆盖{audience}应掌握的核心概念。

题型分布（{question_count} 题）：
- 30% 定义题（直接考概念）
- 30% 例子 / 反例题（区分适用与不适用）
- 20% 案例分析题（成功 / 失败机制）
- 20% 迁移应用题（用原则解决新问题）

不要只考记忆，要考"能不能判断适用边界"。

每题附简要解析（来源 + 推理）。

【参考】参考 00c 领域定向报告。
```

---

### data_table（数据表）

```
从{topic}中提取「{description}」的结构化数据表。

要求：
- 严格按用户描述的字段提取
- 来源中找不到对应数据时填 "N/A"，不要编造
- 每行附 source 引用

【参考】参考 00c 领域定向报告。
```

---

### mind_map（思维导图）

```
{topic}的概念地图。

要求：
- 中心节点 = 领域核心问题
- 第 1 层 = 核心概念（5-7 个）
- 第 2 层 = 每个核心的子概念 + 关键属性
- 第 3 层 = 最小例子 / 反例 / 适用边界
- 用不同颜色或符号标记：⭐ 前置 / ⚠️ 易误解 / 🚫 反例

【参考】参考 00c 领域定向报告中的"核心概念地图"。
```

---

## Content Layer 提取方法（v2 增强）

v1 仅从 `notebook_describe()` 摘要提取。v2 升级为：

1. 调用 `notebook_describe(notebook_id)` 获取 AI 摘要
2. **额外读取 `00c-定向-{topic}领域定向报告` source 的"核心概念地图"段**
3. 提取 5-8 个关键概念词（v1 只提 3-5 个）
4. 将概念词补充到 Intent Layer 模板的 `{topic}` 与新增的"重点覆盖"字段

**v2 提取示例**：

源摘要：`"本 notebook 包含 DQV 数据质量验证服务的设计规范、三阶段处理管道、验证策略、ETL 模式"`

定向报告核心概念：`三阶段管道 / 验证策略 / 错误降级 / 数据契约 / ETL 加载`

提取主题词（v2）：`三阶段管道、验证策略、错误降级、数据契约`（4 个）

最终 Content Layer：`重点覆盖三阶段管道、验证策略、错误降级与数据契约的设计与实现`

---

## Guardrails Layer（默认追加）

详见 `→ ./risk-control-templates.md#2 默认幻觉防护约束句`。

可通过 `disable_guardrails=True` 关闭（仅推荐用于内部技术分享场景）。

---

## 完整组合示例

### 示例 1：DQV 零基础版音频（v2）

```
artifact_type: audio
audio_format: brief
view: foundation
focus_prompt:
  Intent Layer (audio + view=foundation):
    "面向新人开发者的 DQV 数据质量验证零基础版音频..."（如上）
  Content Layer:
    "重点覆盖三阶段管道、验证策略、错误降级与数据契约的设计与实现"
  Guardrails Layer:
    "【约束】所有关键判断必须引用来源；来源中没有的内容标注「推断」..."
```

### 示例 2：陌生主题学习指南（v2）

```
artifact_type: report
report_format: Study Guide
focus_prompt:
  Intent Layer (Study Guide):
    "帮助零基础学习者系统学习 PMP 备考的指南..."（如上）
  Content Layer:
    "重点覆盖五大过程组、十大知识领域、敏捷与混合方法、考试思维"
  Guardrails Layer: 默认约束
```

---

## 受众（audience）常用值（v2 扩展）

| audience | 适用场景 |
|---|---|
| 零基础学习者 | 完全陌生的主题（v2 默认） |
| 新人开发者 | 入职培训、基础学习 |
| 后端开发者 / DBA / DevOps | 技术细节场景 |
| 团队 / 管理层 | 技术分享、评审 |
| 跨领域学习者 | 把本领域知识迁移到相邻领域 |

---

## v2 推荐制品组合（学习闭环导向）

| 场景 | 推荐顺序 | 备注 |
|---|---|---|
| **陌生主题首次学习** | 领域定向报告 → mind_map → audio(brief, foundation) → slide_deck → audio(deep_dive, structural) → quiz → flashcards | 方法论 §11 推荐流程 |
| **MJ 内部新人入职** | mind_map → slide_deck → audio(brief) → quiz → 错题 root cause | 沿用 v1 但加 quiz 闭环 |
| **架构评审** | report(Briefing Doc) → mind_map → audio(deep_dive) | guardrails 必开 |
| **三版深度学习** | view=foundation → view=structural → view=challenge（同 artifact_type） | 高级模式，配额×3 |
| **决策支持** | report(Briefing Doc) + Source Check（强制） | 高风险类别强制 |

---

## v1 → v2 兼容性（迁移期）

| v1 模板名 | v2 替代 | 弃用版本 |
|---|---|---|
| `legacy_audio_tech_podcast` | `audio` 默认 | v2.3 |
| `legacy_slide_tech_demo` | `slide_deck` 默认 | v2.3 |
| `legacy_report_briefing` | `report(Briefing Doc)` 默认 | v2.3 |

调用方法：`focus_prompt_template="legacy_audio_tech_podcast"`（v2.0 / v2.1 / v2.2 仍可用，v2.3 抛 deprecation warning，v2.4 移除）。
