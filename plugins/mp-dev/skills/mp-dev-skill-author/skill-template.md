# SKILL.md Template Reference

mp-dev:skill-author 技能的模板参考文件。定义 SKILL.md 的完整规范，包括 YAML frontmatter、节结构和质量要求。

---

## YAML Frontmatter 规范

```yaml
---
name: <skill-short-name>
description: >
  在 my-marketplace 个人插件市场仓库中，当用户提到 <中文触发词1>, <中文触发词2>,
  <中文触发词3>, <中文触发词4>, 或 <英文触发词1>, <英文触发词2>,
  <英文触发词3>, <英文触发词4> 时使用此技能。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
---
```

### Frontmatter 字段要求

| 字段 | 必填 | 要求 |
|------|------|------|
| `name` | 是 | 与技能目录名中 `<plugin>-` 后的部分一致 |
| `description` | 是 | 50-300 字符；包含项目标识；包含排除声明 |

### Description 质量要求

| 维度 | 要求 | 示例 |
|------|------|------|
| **项目标识** | 必须包含 "在 my-marketplace 个人插件市场仓库中" | — |
| **中文触发词** | >= 3 个 | 创建插件, 插件脚手架, 生成插件模板 |
| **英文触发词** | >= 3 个 | scaffold plugin, create plugin, plugin template |
| **字符长度** | 50-300 字符 | — |
| **排除声明** | 必须包含 | 不适用于 mj-system、不适用于 mj-agentlab-marketplace |
| **独立性** | 触发词不应与同 plugin 内其他 skill 重叠 | — |

---

## 节结构模板

### 1. Overview

```markdown
## Overview

<一句话概述技能职责和价值>

**互补 skill**：<列出相关的其他 skill>
```

### 2. Prerequisites

```markdown
## Prerequisites

- <前置条件 1>
- <前置条件 2>
```

### 3. Quick Start

```markdown
## Quick Start（交互模式）

| 已知信息 | 行动 |
|---------|------|
| "<场景 1>" | <行动描述> |
| "<场景 2>" | <行动描述> |
```

### 4. Workflow

```markdown
## Workflow

（DOT 图或文字描述工作流程）

### Phase N: <阶段名>

**<阶段目的>**

1. <步骤 1>
2. <步骤 2>
```

### 5. H-point 表格

```markdown
## H-point 表格

| ID | 类型 | 触发条件 | 行为 |
|----|------|---------|------|
| **H1** | Hard Block / Conditional / Warning / Choice | <条件> | <行为> |
```

**H-point 类型**：

| 类型 | 含义 | 行为 |
|------|------|------|
| Hard Block | 不可绕过的阻断 | 必须解决才能继续 |
| Conditional | 有条件的暂停 | 补充信息后继续 |
| Warning | 警告但可继续 | 告知风险，用户决定 |
| Choice | 分支选择 | 展示选项供选择 |

### 6. Handoff（可选）

```markdown
## Handoff

<完成后的摘要输出模板和推荐下一步>
```

### 7. Examples

```markdown
## Examples

### 示例 1：<场景名>

（用户输入 → 推断 → 执行 → 结果）
```

### 8. Reference Files

```markdown
## Reference Files

- **`→ <relative-path>`** — <用途描述>
```

---

## 模式参考路径

### 现有 mj-nlm 技能（已验证模式）

| 技能 | 特点 | 可参考的模式 |
|------|------|------------|
| `mj-nlm-auth` | 三级降级、troubleshooting 支撑文件 | 错误处理降级、外部支撑文件 |
| `mj-nlm-build` | 5 Phase 工作流、丰富 H-point | 多阶段工作流、H-point 覆盖 |
| `mj-nlm-manage` | 操作路由、破坏性确认 | CRUD 路由、confirm 模式 |
| `mj-nlm-query` | 多模式分支、异步轮询 | 模式选择、异步等待 |
| `mj-nlm-studio` | 子参数矩阵、Focus Prompt | 参数配置、模板拼接 |

### mp-git 技能（新开发参考）

| 技能 | 可参考的模式 |
|------|------------|
| `mp-git-branch` | 分支命名规范、工作流引导 |
| `mp-git-commit` | commit message 规范、变更分析 |
| `mp-git-pr` | PR 模板选择、自动化检查 |

---

## 写作规范

1. **祈使句**：SKILL.md 是写给 Claude 的指令，使用祈使句（"检查…"、"调用…"、"展示…"）
2. **中文为主**：正文使用中文，技术术语保留英文
3. **代码块**：工具调用使用代码块，注明参数
4. **层次清晰**：Phase → Step → 细节，逐级展开
5. **安全第一**：破坏性操作必须有 H-point 门控
