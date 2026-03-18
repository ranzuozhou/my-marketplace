---
name: mp-git-sync
description: >-
  在 my-marketplace 个人插件市场仓库中同步基线分支最新代码到当前工作分支。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
  触发词：同步分支、拉取最新、分支落后、合并最新代码、同步一下、落后了、分支过时了，
  sync branch, pull develop, merge develop, update branch, branch behind, branch outdated, catch up with develop,
  self-update, pull remote, remote ahead.
---

# MP Git Sync

## Overview

同步基线分支（develop 或 main）的最新代码到当前工作分支，或从 origin 拉取同名分支的远端提交。侧循环辅助操作，可在 branch→push 之间任意时刻多次调用。

**三模式**：
- **开发中同步模式**：工作分支拉取基线分支最新代码
- **Hotfix 回同步模式**：在 develop 上将 main（含 hotfix 修复）合并回 develop 并推送
- **自更新模式**：任何分支从 origin/<当前分支> 拉取远端最新提交

## 前置条件

- 在 my-marketplace worktree 目录内执行
- `main` 分支上禁止跨分支合并（自更新例外）

## Sync Workflow (6 steps)

### Step 0 — 环境检测

```bash
git branch --show-current
git worktree list
```

检测逻辑：
- 自更新信号 → 自更新模式
- 跨分支同步信号 → 基于分支类型选择基线
- 意图模糊 → H-code 询问

### Step 1 — 检查工作目录状态

```bash
git status --short
```

有未提交修改 → H1

### Step 2 — 获取远程最新状态

```bash
git fetch origin
```

### Step 3 — 展示分歧信息 + 确认

```bash
git rev-list --count HEAD..origin/<base>
git rev-list --count origin/<base>..HEAD
git log --oneline HEAD..origin/<base>
```

count = 0 → 已是最新

### Step 4 — 执行合并

```bash
# 开发中同步
git merge origin/develop   # feature/bugfix/documentation/maintain
git merge origin/main      # hotfix

# Hotfix 回同步
git merge origin/main      # 在 develop 上

# 自更新
git merge origin/<current-branch>
```

### Step 5 — 同步后验证

```bash
git status --short
git log --oneline -3
```

**Hotfix 回同步额外步骤**：
```bash
git push origin develop
```

## 人工介入场景

| # | 触发条件 | 技能行为 | 级别 |
|---|---------|---------|------|
| **H1** | 有未提交修改 | 三选一：commit / stash / 取消 | Soft |
| **H2** | merge 产生冲突 | Claude 提案→用户选择→执行 | Soft |
| **H3** | stash pop 产生冲突 | 告知需手动解决 | Soft |
| **H4** | 在 main 上跨分支合并 | 硬阻断 | Hard |
| **H4a** | 在 main + 意图模糊 | 自更新 or 取消 | Soft |
| **H4b** | 在 develop + 意图模糊 | 三选一：自更新 / hotfix 回同步 / 取消 | Soft |
| **H5** | 用户要求 rebase | 引导为 merge | Info |
| **H6** | 分支前缀无法匹配 | 询问基线分支 | Soft |

## 安全规则

1. 禁止在 main 上跨分支 merge（自更新例外）
2. merge 策略强制（rebase → merge）
3. 冲突解决中保护工作成果

## 示例

### 示例 1：常规同步

```bash
git branch --show-current    # → feature/add-mp-git-plugin
git fetch origin
git rev-list --count HEAD..origin/develop  # → 3
git merge origin/develop
# 同步完成 ✓
```

### 示例 2：Hotfix 回同步

```bash
# 在 develop worktree
git fetch origin
git merge origin/main
git push origin develop
# hotfix 修复已同步到 develop ✓
```
