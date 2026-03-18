---
name: mp-git-review-pr
description: >-
  在 my-marketplace 个人插件市场仓库中评审 Pull Request 的插件结构合规性。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
  触发词：评审PR、审查PR、PR评审、review PR、帮我看看这个PR、检查PR、可以merge吗、这个PR能合吗，
  review pull request, architecture review, PR review, check PR structure, plugin structure review.
  执行固定检查（F1-F3）和动态插件结构检查（D1-D6）。
---

# MP Git Review PR

## Overview

PR 插件结构评审 skill。

**核心价值**：回答"这个 PR **应不应该**合"——检查插件结构合规、SKILL.md 完整性、版本一致性。

与 `mp-git-check-merge`（回答"**能不能**合"——冲突、CI、审批）互补。

## 前置条件

- `gh` CLI 已安装且已认证
- 当前在 worktree 目录中
- 远端仓库可访问

## 快速开始

| 输入 | 行为 |
|------|------|
| `评审 PR #5` | 完整 5 阶段评审 |
| `帮我看看 feature/xxx` | 通过分支名定位 PR，完整评审 |
| `PR #5 的变更概览` | 快速模式：只执行 Stage 1-2 |

---

## 工作流

### Stage 1: 定位 PR

```bash
gh pr view {input} --json number,title,state,baseRefName,headRefName,additions,deletions,changedFiles,commits
```

- **H1**: PR 状态非 OPEN → 终止
- **H2**: 分支类型无法识别 → 询问用户

### Stage 2: 描述变更

```bash
gh pr view {number} --json commits --jq '.commits[].messageHeadline'
gh pr diff {number} --stat 2>/dev/null || gh api repos/{owner}/{repo}/pulls/{number}/files --jq '.[].filename'
```

按类别统计：Plugin / Skill / Config / Docs / Scripts / CI / Other

### Stage 3: 架构评审

#### 3.1 固定检查（每次必做）

| 检查 | 方法 |
|------|------|
| **F1 分支同步** | `git log HEAD..origin/{base_branch} --oneline` |
| **F2 变更概览** | 复用 Stage 2 统计 |
| **F3 Commit 规范** | 所有 commit type 对照 Branch×Type 矩阵 |

#### 3.2 动态检查触发

| 变更范围 | 触发的检查 |
|----------|-----------|
| `plugins/` 下有新目录 | D1（插件目录结构） |
| `skills/**/SKILL.md` 有变更 | D2（SKILL.md frontmatter） |
| `**/plugin.json` 有变更 | D3（plugin.json 合规） |
| `.claude-plugin/marketplace.json` 有变更 | D4（marketplace.json 一致性） |
| `VERSION` 有变更 | D5（版本同步） |
| `**/CHANGELOG.md` 有变更 | D6（CHANGELOG 格式） |

#### 3.3 执行检查

读取 `review-checklist.md` 中对应检查项定义，逐项执行：

- **D1**: 验证 plugin.json + CLAUDE.md + README.md + CHANGELOG.md + skills/ 存在
- **D2**: 验证 SKILL.md 有 name + description frontmatter（跳过 *-shared）
- **D3**: 验证 plugin.json 6 字段完整 + 版本匹配 marketplace.json
- **D4**: 验证插件名 ↔ 目录名匹配
- **D5**: 验证 VERSION = marketplace.json metadata.version
- **D6**: 验证 CHANGELOG 格式（[Unreleased] 节存在）

#### 3.4 汇总

```
| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| F1 | 分支同步 | ℹ️ | 同步 |
| F2 | 变更概览 | ℹ️ | Plugin 5 | Skill 3 | Config 1 |
| F3 | Commit 规范 | ✅ | 2 feat — 均在 feature/* 允许范围 |
| D1 | 插件结构 | ✅ | 5/5 项存在 |
```

### Stage 4: 人工确认 → 发布 comment

选项：发布到 PR / 修改后发布 / 仅本地查看

```bash
gh pr comment {number} --body "{review_comment}"
```

### Stage 5: (可选) 合并

仅在用户明确要求时触发，双重确认后执行：

```bash
gh pr merge {number} --merge --delete-branch
```

---

## Handoff

```
评审完成 ✓
  建议下一步：
  - 深度校验 → /mp-dev:mp-dev-validate
  - 技术合并检查 → /mp-git:mp-git-check-merge
  - 直接合并 → 回复"合并"触发 Stage 5
```

## Reference Files

| 文件 | 说明 |
|------|------|
| `review-checklist.md` | 检查项定义（F1-F3、D1-D6） |
| `comment-template.md` | PR 评论输出模板 |
