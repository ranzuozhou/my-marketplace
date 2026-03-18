---
name: mp-git-push
description: >-
  在 my-marketplace 个人插件市场仓库中执行 pre-push 检查并推送代码到 GitHub。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
  触发词：推送代码、push code、git push、推到远端、推送失败、CHANGELOG、推送前检查，
  push to remote, push error, pre-push check, push to GitHub.
  执行 7 项 pre-push checklist 和单路 GitHub 推送。
---

# MP Git Push

## Overview

7-item pre-push checklist + 单路 GitHub 推送。

> **前置技能**：`mp-git-commit` 已在提交阶段验证 commit message 格式和 type/branch 纪律。本技能的 Step 1-2 作为二次确认。

## Pre-Push Checklist (run in order)

```bash
# 1. Commit message format check
git log --oneline develop..HEAD
# Verify each: <type>(<scope>): <summary>

# 2. Commit type matches branch type
# feature/* → feat/perf/refactor/test/docs only
# bugfix/*  → fix/test/docs only
# documentation/* → docs only
# maintain/* → infra/docs only
# hotfix/*  → fix only

# 3. CHANGELOG check
git diff develop -- CHANGELOG.md
# Empty output + has feat/fix commits = missing CHANGELOG update

# 4. Clean working directory
git status --short
# Must be empty

# 5. Validate branch name
git branch --show-current
# Must match: feature/<desc> | bugfix/<desc> | documentation/<desc> | maintain/<desc> | hotfix/<desc>

# 6. Sync base branch
git fetch origin && git merge origin/develop   # regular branches
git fetch origin && git merge origin/main      # hotfix/* branches only

# 7. Execute push + confirm
git push -u origin <branch>    # first push
git push                       # subsequent pushes
git log origin/<branch> --oneline -3
```

## CHANGELOG Update Rules

| Commit Type | CHANGELOG Section | Record? |
|-------------|------------------|---------|
| `feat` | `### Added` | **Must record** |
| `fix` | `### Fixed` | **Must record** |
| `perf` | `### Changed` | **Must record** |
| `refactor` | `### Changed` | Only if significant |
| `infra` | `### Added` or `### Changed` | Only if significant |
| `docs` | — | Skip |
| `test` | — | Skip |

## Worktree Validation

Push must happen from inside a worktree directory.

```bash
git worktree list
pwd
git branch --show-current
```

## Force Push (after amending)

```bash
# Only on personal dev branches, never on main or develop
git commit --amend -m "<corrected message>"
git push --force-with-lease
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `rejected - non-fast-forward` | Remote has commits you don't | Run step 6: fetch + merge |
| `fatal: no upstream branch` | First push without `-u` | `git push -u origin <branch>` |
| `remote: Permission denied` | No write access | `gh auth status`, check permissions |

## Handoff to mp-git-pr

```
推送完成 ✓
下一步：使用 mp-git-pr 创建 Pull Request。
  已验证项：commit 格式 ✓、type/branch 纪律 ✓、CHANGELOG ✓、工作目录清洁 ✓、base 同步 ✓
```

## Common Issues → push-faq.md

完整排障指南见 `push-faq.md`。
