---
name: mp-git-branch
description: >-
  在 my-marketplace 个人插件市场仓库中创建符合规范的 Git 分支和 Worktree。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
  触发词：创建分支、新建分支、开新分支、开始开发、哪种分支类型，
  create branch, new branch, branch naming, worktree add, start feature, start bugfix, start hotfix, which branch type.
---

# MP Git Branch

## Overview

为 my-marketplace 仓库创建和管理 Git 分支。5 种临时分支类型，2 个受保护永久分支（`main`、`develop`）。

## 前置条件

- 在 my-marketplace worktree 目录内执行（bare repo 根目录无 working tree）
- 当前分支为正确的基础分支（develop 或 main）

## 快速开始（交互模式）

### 信息充足性判断

| 已知信息 | 行动 |
|---------|------|
| 任务性质不明确 | 问：「这次任务是新功能、bug 修复、纯文档、基础设施维护，还是生产紧急修复？」 |
| 类型明确，但无英文描述词 | 问：「请用 2-5 个英文单词描述此任务（e.g. `add-mp-git-plugin`、`fix-validate-script`）」 |
| 类型 + 描述词均有，缺 issue-id | 直接生成（issue-id 可选）。若需先创建 Issue，可使用 mp-git-issue |
| 信息完整 | 直接生成命令 |

### 输出格式

信息收集完毕后，输出单行创建命令：

```bash
# feature / bugfix / documentation / maintain（从 develop/ 内执行）
cd develop && git worktree add ../<type>/<desc> -b <type>/<desc> develop

# hotfix（若 main/ 不存在则先创建）
git worktree add main main && cd main && git worktree add ../hotfix/<desc> -b hotfix/<desc> main
```

## Branch Type Decision

| Question | → Branch Type |
|----------|--------------|
| New feature, new plugin, new skill, or refactor? | `feature/` |
| Bug found on develop? | `bugfix/` |
| Only docs changed, no code? | `documentation/` |
| Docs changed alongside code? | Follow the code type |
| CI/scripts/deps/config? | `maintain/` |
| Production emergency bug? | `hotfix/` |

## Naming Format

```
<type>/<issue-id>-<description>   # with GitHub Issue
<type>/<description>              # without Issue
```

Valid types: `feature`, `bugfix`, `documentation`, `maintain`, `hotfix`

Rules: lowercase, hyphens only, no spaces or uppercase.

## Commands by Branch Type

### feature / bugfix / documentation / maintain

```bash
# Step 1: Create branch + worktree
cd develop && git worktree add ../feature/<desc> -b feature/<desc> develop

# Step 2: Work in the new worktree
cd ../feature/<desc>

# Step 3: Push (first push needs -u)
git push -u origin feature/<desc>

# After PR merge — cleanup:
cd ..
git worktree remove feature/<desc>
git -C develop branch -d feature/<desc>
```

### hotfix

```bash
# Step 1: Create main worktree if needed
git worktree add main main

# Step 2: Create hotfix branch
cd main && git worktree add ../hotfix/<desc> -b hotfix/<desc> main

# Step 3: Fix and commit (only fix commits)
cd ../hotfix/<desc>
git add <files> && git commit -m "fix(<scope>): <summary>"

# Step 4: Push and create PR targeting main
git push -u origin hotfix/<desc>

# Step 5: After merge — tag patch version
cd ../main && git pull origin main
git tag -a v1.0.1 -m "Hotfix: <summary>"
git push origin v1.0.1

# Step 6: Sync to develop (use mp-git-sync)
# Step 7: Cleanup (use mp-git-delete)
```

## 人工介入场景

| # | 触发条件 | 技能行为 |
|---|---------|---------|
| **H1** | 分支类型无法判断 | 展示 5 种类型说明，询问用户选择 |
| **H2** | 描述词缺失 | 要求提供 2-5 个英文单词 |
| **H3** | 当前不在 worktree 目录 | 提示切换到 develop worktree |

## Quick Reference → branch-rules.md

完整 commit-type × branch-type 允许矩阵、命名示例、生命周期图见 `branch-rules.md`。
