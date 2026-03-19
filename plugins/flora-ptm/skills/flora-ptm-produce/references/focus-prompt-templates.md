# Focus Prompt 模板

本文档定义 flora-ptm-produce Phase 2 设计 Focus Prompt 的两层拼接策略。

---

## 两层拼接架构

每个 Focus Prompt = **Intent Layer** + **Content Layer**

```
{Intent Layer}，{Content Layer}
```

- **Intent Layer**: 定义制品的角色、受众和任务
- **Content Layer**: 引导 NLM 利用 notebook 中的 meta-knowledge sources

---

## Intent Layer 模板

按 artifact_type 分类，每种类型有专属的 Intent 模板：

### audio

| audio_format | Intent 模板 |
|-------------|-------------|
| `brief` | `"面向{audience}的{topic}简要概述播客"` |
| `deep_dive` | `"面向{audience}的{topic}深度剖析播客"` |
| `critique` | `"面向{audience}的{topic}批判性分析播客"` |
| `debate` | `"关于{topic}的多角度辩论式播客"` |

### video

| video_format | Intent 模板 |
|-------------|-------------|
| `explainer` | `"面向{audience}的{topic}解说视频"` |
| `brief` | `"面向{audience}的{topic}简报视频"` |
| `cinematic` | `"关于{topic}的电影化叙事视频"` |

### slide_deck

| slide_format | Intent 模板 |
|-------------|-------------|
| `detailed_deck` | `"面向{audience}的{topic}详细技术演示"` |
| `presenter_slides` | `"面向{audience}的{topic}演讲辅助幻灯片"` |

### report

| report_format | Intent 模板 |
|-------------|-------------|
| `Briefing Doc` | `"面向{audience}的{topic}简报文档，提炼关键发现和行动建议"` |
| `Study Guide` | `"帮助{audience}系统学习{topic}的学习指南"` |
| `Blog Post` | `"面向广泛读者的{topic}科普博文"` |
| `Create Your Own` | `"{user_custom_prompt}"` |

### infographic

```
"面向{audience}的{topic}信息图，视觉化呈现核心数据和关系"
```

### mind_map

```
"面向{audience}的{topic}知识结构思维导图"
```

### flashcards

```
"帮助{audience}记忆{topic}核心概念的学习闪卡"
```

### quiz

```
"检测{audience}对{topic}核心知识掌握程度的测验"
```

### data_table

```
"从{topic}研究资料中提取{description}的结构化数据表"
```

---

## Content Layer 构建

Content Layer 是动态生成的，基于目标 notebook 的实际内容：

### 步骤 1: 提取关键主题词

从 `notebook_describe(notebook_id)` 的返回结果中，提取 3-5 个最具代表性的主题关键词。

### 步骤 2: 构建内容引导句

```
"重点覆盖{keyword_1}、{keyword_2}、{keyword_3}等核心主题"
```

### 步骤 3: 元知识引导句

引导 NLM 优先利用 notebook 中的 meta-knowledge sources（精简短文、综述、关系分析）：

```
"参考内容中的「综述」和「关系分析」理解材料间的逻辑关系和研究脉络，参考各篇「精简」短文快速获取每份报告的核心价值"
```

---

## 组合示例

### 示例 1: 快速消化 — audio(brief)

```
面向研究者的 LLM 安全对齐技术简要概述播客，重点覆盖 RLHF、宪法 AI、红队测试等核心主题，参考内容中的「综述」和「关系分析」理解材料间的逻辑关系和研究脉络，参考各篇「精简」短文快速获取每份报告的核心价值
```

### 示例 2: 深度学习 — report(Study Guide)

```
帮助研究者系统学习 LLM 安全对齐技术的学习指南，重点覆盖 RLHF 训练流程、宪法 AI 原则设计、红队测试方法论等核心主题，参考内容中的「综述」和「关系分析」理解材料间的逻辑关系和研究脉络，参考各篇「精简」短文快速获取每份报告的核心价值
```

### 示例 3: 视觉优先 — slide_deck

```
面向技术团队的 LLM 安全对齐技术详细技术演示，重点覆盖 RLHF、宪法 AI、红队测试的技术细节和对比分析，参考内容中的「综述」和「关系分析」理解材料间的逻辑关系和研究脉络，参考各篇「精简」短文快速获取每份报告的核心价值
```

### 示例 4: 自定义 — quiz

```
检测研究者对 LLM 安全对齐技术核心知识掌握程度的测验，重点覆盖 RLHF 关键步骤、宪法 AI 与 RLHF 的区别、红队测试攻击向量分类等核心主题，参考内容中的「综述」和「关系分析」理解材料间的逻辑关系和研究脉络，参考各篇「精简」短文快速获取每份报告的核心价值
```

---

## 变量说明

| 变量 | 来源 | 说明 |
|------|------|------|
| `{audience}` | 用户指定或默认 "研究者" | 目标受众描述 |
| `{topic}` | notebook tag 或用户指定 | 研究主题名称 |
| `{keyword_N}` | `notebook_describe()` 提取 | 3-5 个关键主题词 |
| `{description}` | 仅 data_table 使用 | 用户指定的数据描述 |
| `{user_custom_prompt}` | 仅 report(Create Your Own) | 用户完全自定义的 prompt |

---

## Prompt 审核要点

在 Phase 2 人工判断点展示 prompt 时，提示用户关注：

1. **受众是否准确**: "面向研究者" vs "面向管理层" 会显著影响输出风格
2. **主题词是否完整**: 是否遗漏了重要子主题
3. **侧重点是否正确**: 是否需要偏向趋势分析、方法论对比或实践应用
4. **语言风格**: 学术严谨 vs 通俗易懂

用户可以直接修改 prompt 文本的任何部分，或只调整关键参数。
