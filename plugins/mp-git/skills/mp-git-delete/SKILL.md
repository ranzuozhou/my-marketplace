---
name: mp-git-delete
description: >-
  在 my-marketplace 个人插件市场仓库中删除分支并清理 Worktree。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
  触发词：删除分支、清理分支、PR合并后清理、分支已合并，
  branch cleanup, delete branch, worktree remove, post-merge cleanup.
  在每个关键节点都需用户确认的安全删除流程。
---

# MP Git Delete

## Overview

删除 my-marketplace 中的 Git 分支，支持 Bare Repo Worktree 模式下的安全清理流程。删除是不可逆操作，每个关键节点都需要用户确认。

## 快速开始

### Step 0 — 确认分支名

若用户未提供分支名：
> 「要删除哪个分支？可先运行 `git worktree list` 查看。」

### Step 0.5 — 同步远程状态

```bash
git fetch origin --prune
```

### Step 1 — 确认删除范围

> 请选择删除范围：
> 1. **仅本地**：移除 worktree + 删除本地分支
> 2. **仅远程**：删除 GitHub 上的远程分支
> 3. **本地及远程**：完整清理

## 命令序列

### 选项 1：仅本地删除

```bash
git worktree remove ../<type>/<desc>
git branch -d <type>/<desc>
```

### 选项 2：仅远程删除

```bash
git push origin --delete <type>/<desc>
```

### 选项 3：本地及远程

```bash
git worktree remove ../<type>/<desc>
git branch -d <type>/<desc>
git push origin --delete <type>/<desc>
```

> 每个 Step 失败不阻塞后续 Step，最终输出清理摘要。

## 人工介入场景

| # | 触发条件 | 技能行为 |
|---|---------|---------|
| **H1** | worktree 内有未提交修改 | ⚠️ 询问是否确认删除 |
| **H2** | `git branch -d` 报错（未合并提交） | ⚠️ 检查远程是否已合并，若已合并自动 `-D`，否则询问用户 |
| **H3** | 当前 shell 在被删 worktree 内 | 🚫 暂停，提示 `cd ../develop` |
| **H4** | 远程分支不存在 | ℹ️ 告知，询问是否继续本地清理 |

## 安全规则

1. **禁止删除受保护分支**：`main` 和 `develop` 不可删除
2. **执行位置要求**：必须在其他 worktree 目录内执行
3. **`-d` vs `-D`**：已合并用 `-d`；未合并需 H2 确认后才用 `-D`
