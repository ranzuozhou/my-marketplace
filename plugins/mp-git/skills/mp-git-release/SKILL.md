---
name: mp-git-release
description: >-
  在 my-marketplace 个人插件市场仓库中执行版本发布流程：分析变更范围、确定版本号、
  bump 版本、更新 CHANGELOG、提交发布、创建 Release PR (develop → main)。
  不适用于 mj-system、不适用于 mj-agentlab-marketplace。
  触发词：发版、发布、release、版本发布、bump version、创建release、
  publish, create release, version bump, 准备发布, 上线, 进行release。
  此技能在 develop 分支上积累了足够变更后触发，或用户明确要求发布时触发。
  即使用户只说"发布"两个字，也应触发此技能。
---

# MP Git Release

## Overview

my-marketplace 版本发布的 7 步交互式工作流。发布流程处于 mp-git 工作流链的末端：开发完成 → 提交推送 → **发布**。

发布在 develop 分支上执行，生成 Release PR (develop → main)。PR 合并后 CI 自动创建 git tag 和 GitHub Release。

```text
mp-git-commit → mp-git-push → [mp-git-release] → CI auto-release
```

## 前置条件

- 在 my-marketplace develop worktree 内执行
- develop 分支上有新的变更（相对于上一个 tag 或 main）
- `gh` CLI 已认证
- `scripts/bump-version.ps1` 可用

## Step 1: 分析变更范围

确定自上次发布以来哪些插件有变更，以及变更类型。

```bash
# 获取最新 tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")

# 查看变更文件
if [ "$LAST_TAG" = "none" ]; then
  git diff --name-only main..HEAD
else
  git diff --name-only $LAST_TAG..HEAD
fi

# 识别变更的插件
git diff --name-only $LAST_TAG..HEAD | grep '^plugins/' | cut -d/ -f2 | sort -u

# 查看变更 commit
git log --oneline $LAST_TAG..HEAD
```

**判断逻辑**：

| 变更范围 | 需要 bump 的版本 |
|---------|-----------------|
| 仅 `plugins/mp-git/` 下文件 | mp-git + marketplace |
| 仅 `scripts/`、`docs/`、根目录文件 | 仅 marketplace |
| 多个插件目录 | 各变更插件 + marketplace |
| 无变更（develop == main） | **H1**: 告知无需发布，停止 |

**版本号推荐规则**：

| Commit 类型 | 推荐 bump |
|------------|-----------|
| 包含 `feat` 或新增 SKILL.md | MINOR |
| 仅 `fix`/`infra`/`docs` | PATCH |
| 包含 BREAKING CHANGE 或删除 skill | MAJOR |

## Step 2: 确认版本号（AskUserQuestion）

读取当前版本：

```bash
cat VERSION                                          # marketplace 当前版本
cat plugins/<plugin>/.claude-plugin/plugin.json       # 插件当前版本
```

展示推荐版本，通过 AskUserQuestion 确认：

```
当前版本:
  marketplace: 1.2.0
  mp-git: 1.0.0

推荐新版本:
  marketplace: 1.2.1 (PATCH — 仅 bug fix)
  mp-git: 1.0.1 (PATCH — 仅 bug fix)

确认还是修改?
```

用户可选择：
1. 接受推荐版本
2. 手动指定版本号

## Step 3: Bump 版本

**执行顺序**：先 bump 各变更插件，最后 bump marketplace。

```powershell
# 1. DryRun 预览（所有 scope）
.\scripts\bump-version.ps1 -From "<current>" -To "<new>" -Scope "<plugin>" -DryRun
.\scripts\bump-version.ps1 -From "<current>" -To "<new>" -DryRun

# 2. 展示预览结果给用户 → H3 确认

# 3. 实际执行
.\scripts\bump-version.ps1 -From "<current>" -To "<new>" -Scope "<plugin>"
.\scripts\bump-version.ps1 -From "<current>" -To "<new>"
```

**H3 触发**：DryRun 输出后，展示所有将要修改的文件和行，等用户确认后再实际执行。

## Step 4: 更新 CHANGELOG

### 4.1 提取变更摘要

```bash
# 从 commit log 提取
git log --oneline $LAST_TAG..HEAD --format="- %s"
```

按 commit type 分类到 Added / Changed / Fixed / Removed 四个 section。

### 4.2 更新文件

**Root CHANGELOG.md**：

```markdown
## [Unreleased]

## [X.Y.Z] - 2026-MM-DD

### Fixed
- mp-git: <变更摘要>

## [上一版本] - ...
```

**Plugin CHANGELOG.md**（仅变更的插件）：

```markdown
## [Unreleased]

## [X.Y.Z] - 2026-MM-DD

### Fixed
- <变更摘要>

## [上一版本] - ...
```

### 4.3 确认

**H4 触发**：展示生成的 CHANGELOG 条目，用户可修改后继续。

## Step 5: 提交发布

```bash
# 暂存所有发布文件
git add VERSION .claude-plugin/marketplace.json README.md CHANGELOG.md
git add plugins/*/CHANGELOG.md plugins/*/.claude-plugin/plugin.json

# 提交
git commit -m "release(marketplace): bump version to X.Y.Z

- marketplace: A.B.C → X.Y.Z
- <plugin>: D.E.F → G.H.I
- <高层变更摘要>

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"

# 推送
git push origin develop
```

## Step 6: 创建 Release PR

```bash
# 读取 release.md 模板
cat .github/PULL_REQUEST_TEMPLATE/release.md
```

从 CHANGELOG 中提取 Highlights，填充模板字段，写入临时文件：

```bash
gh pr create \
  --base main \
  --head develop \
  --title "Release vX.Y.Z" \
  --body-file <tmp-file> \
  --reviewer <reviewer>
```

**H5 触发**：展示 PR title + body 预览，用户确认后提交。

**Release PR body 结构**：

```markdown
## Highlights
<!-- 从 CHANGELOG [X.Y.Z] 提取 -->

### Versions
| Plugin | Version |
|--------|---------|
| mj-nlm | x.y.z |
| mp-git | x.y.z |
| mp-dev | x.y.z |
| flora-ptm | x.y.z |

## 审核要点
- [ ] CHANGELOG.md 完整
- [ ] VERSION 与 marketplace.json 一致
- [ ] 各 plugin.json 版本与 marketplace.json 一致
- [ ] 无残留调试代码
```

## Step 7: 验证（可选）

输出提示：

```
Release PR 已创建 ✓
下一步：
  1. Review 并合并 PR
  2. CI 将自动创建 tag vX.Y.Z 和 GitHub Release
  3. 验证命令：
     gh pr view <number> --repo ranzuozhou/my-marketplace
     gh release view vX.Y.Z --repo ranzuozhou/my-marketplace
```

## 人工交互节点

| # | 触发条件 | 行为 |
|---|---------|------|
| **H1** | develop 与 main/last-tag 无差异 | 告知无需发布，停止 |
| **H2** | Step 2 版本号确认 | AskUserQuestion 展示推荐版本 |
| **H3** | Step 3 DryRun 预览后 | 展示 bump 结果，确认执行 |
| **H4** | Step 4 CHANGELOG 生成后 | 展示条目，允许编辑 |
| **H5** | Step 6 PR 提交前 | 展示 PR 预览，确认提交 |

> H1 为硬性阻断。H2-H5 用户可选择跳过（快速模式）。

## 版本规则 & 常见问题 → release-checklist.md

完整的发布前检查清单、版本号速查表、CHANGELOG 格式模板、POM 同步问题说明见 `release-checklist.md`。
