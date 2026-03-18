---
name: mp-git-check-merge
description: >-
  在 my-marketplace 个人插件市场仓库中检查 PR 是否满足合并条件。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
  触发词：PR能合并吗、可以合并了吗、PR审核状态、代码准备好了吗、可以让人review了吗，
  check merge readiness, PR ready, can merge, PR status, review status.
---

# MP Git Check Merge

## 前置条件

- `gh` CLI 已安装并完成身份认证
- 在 my-marketplace worktree 目录内执行

## Overview

PR 创建后的合并就绪检查，5 项检查（4 项门控 + 1 项信息），输出表格 + 针对失败项的建议操作。

## 快速开始

### Step 1 — 识别 PR

```bash
git branch --show-current
gh pr list --head <branch> --state open --json number,title
```

| 结果 | 处理方式 |
|------|---------|
| 0 个 open PR | 询问用户提供 PR 号 |
| 1 个 open PR | 自动使用 |
| 多个 open PR | 列出让用户选择 |

### Step 2 — 获取 PR 全部数据

```bash
gh pr view <number> --json number,title,headRefName,mergeable,body,reviews,statusCheckRollup
```

### Step 3 — 运行 5 项检查

1. **合并冲突**: `mergeable` 字段
2. **CI 检查**: `statusCheckRollup` 字段
3. **Review 状态**: `reviews` 字段
4. **PR 描述完整性**: 分支类型对应必填字段
5. **Merge Commit 检测**: `gh api` 获取 commit 列表

### Step 4 — 输出结果

## 描述完整性检查

| 分支类型 | 必检字段 |
|----------|---------|
| `feature/*` | 变更摘要、影响范围、审核要点、自检清单 |
| `bugfix/*` | Bug描述、根因分析、修复方案、影响范围、自检清单 |
| `hotfix/*` | 事故描述、影响范围、根因分析、修复方案、**回滚预案**、自检清单 |
| `maintain/*` | 变更摘要、影响评估、审核要点、自检清单 |
| `documentation/*` | 文档变更内容、变更原因、自检清单 |
| `develop`（release）| Highlights、审核要点 checklist |

## 输出格式

```
## PR #<number>「<title>」Merge Readiness

| 检查项         | 状态       | 说明                                |
|----------------|------------|-------------------------------------|
| 无合并冲突     | ✅ Pass    | 可正常合并                          |
| CI 检查通过    | ❌ Fail    | N 项未通过                          |
| Review 已批准  | ⚠️ Pending | 0/1 Approve                        |
| PR 描述完整    | ✅ Pass    | 所有必填字段已填写                  |
| Merge Commit   | ℹ️ Info    | N 个 merge commit                   |

**总判断：Ready to Merge / Not Ready / Waiting for Review**
```

**总判断规则**：
- 全部 Pass/Skip/Info → **Ready to Merge ✅**
- 任意 Fail → **Not Ready to Merge ❌**
- 仅有 Pending → **Waiting for Review ⏳**

## Handoff

- Ready → 通知审核并合并，合并后使用 mp-git-delete 清理
- Not Ready → 按待处理列表修复 → push → 再次运行
- Waiting → 联系审核人

## 人工介入场景

| # | 触发条件 | 处理方式 |
|---|---------|---------|
| **H1a** | 无 open PR | 询问 PR 号 |
| **H1b** | 多个 open PR | 列出让用户选择 |
| **H2** | mergeable = UNKNOWN | 告知稍后重试 |
| **H3** | 无 CI 配置 | 标记 Skip |
| **H4** | API 调用失败 | Merge Commit 标记 Skip |
