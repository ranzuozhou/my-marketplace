---
name: mp-git-pr
description: >-
  在 my-marketplace 个人插件市场仓库中创建 Pull Request，选择正确的 PR 模板并填充字段。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
  触发词：创建PR、新建PR、提PR、PR模板、版本号、发版、合并到main，
  create PR, pull request, PR template, version bump, release, merge to main.
  使用 gh CLI 的 --body-file 模式和分支类型对应模板。
---

# MP Git PR

## Overview

为 my-marketplace 仓库创建 Pull Request，使用分支类型对应的模板。非交互模式下使用 `--body-file`（不用 `--body`）。6 种模板，6 种分支类型，2 个目标分支。

## Template Selection Matrix

| Template | Branch | Target | Special |
|----------|--------|--------|---------|
| `feature.md` | `feature/*` | develop | — |
| `bugfix.md` | `bugfix/*` | develop | — |
| `documentation.md` | `documentation/*` | develop | — |
| `maintain.md` | `maintain/*` | develop | — |
| `hotfix.md` | `hotfix/*` | **main** | Rollback plan mandatory |
| `release.md` | develop | **main** | Version bump required |

Templates are in `.github/PULL_REQUEST_TEMPLATE/`.

## Command Format

```bash
# Step 1: 读取对应模板
# .github/PULL_REQUEST_TEMPLATE/<type>.md

# Step 2: 填写内容后写入临时文件

# Step 3: 创建 PR
# Standard branches (feature/bugfix/documentation/maintain)
gh pr create \
  --base develop \
  --head <branch-name> \
  --title "<PR title>" \
  --body-file <tmp-file> \
  --reviewer "<reviewer-username>"

# Hotfix — target is main
gh pr create \
  --base main \
  --head hotfix/<desc> \
  --title "fix(<scope>): <summary>" \
  --body-file <tmp-file> \
  --reviewer "<reviewer-username>"

# Release
gh pr create \
  --base main \
  --head develop \
  --title "Release vX.Y.Z" \
  --body-file <tmp-file> \
  --reviewer "<reviewer-username>"
```

> **PROHIBITED**: 不得用 `--body` 内联 PR 描述。

## Per-Template Summary

| Template | Required Fields |
|----------|----------------|
| `feature.md` | 变更摘要, 影响范围, 审核要点, 自检结果 |
| `bugfix.md` | Bug描述, 根因分析, 修复方案, 影响范围, 自检结果 |
| `documentation.md` | 文档变更内容, 变更原因, 自检结果 |
| `maintain.md` | 变更摘要, 影响评估, 审核要点, 自检结果 |
| `hotfix.md` | 事故描述, 影响范围, 根因分析, 修复方案, **回滚预案**, 自检结果 |
| `release.md` | Highlights, 审核要点 checklist |

## Release PR: Version Bump

Only at release time (develop → main). Not during feature development.

```powershell
# Preview
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -DryRun

# Execute (marketplace level)
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0"

# Execute (plugin level)
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git"
```

## Hotfix Special Rules

1. Target branch is `main`
2. **Rollback plan is mandatory**
3. Must sync fix back to develop after merge
4. After merge: tag patch version on main

## Handoff to mp-git-check-merge

```
PR 创建完成 ✓
下一步：等待 CI 运行完成后，使用 mp-git-check-merge 检查合并就绪状态。
```

## Detailed Fields → pr-templates-reference.md

完整字段指南见 `pr-templates-reference.md`。
