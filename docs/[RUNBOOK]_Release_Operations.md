> **[RUNBOOK] 发布操作手册 — My Marketplace**
> 从功能开发到版本发布的完整操作流程，面向执行者。

## 1. 流程总览

```
Issue → Branch → Develop → Commit → Push → PR → CI → Review → Merge
                                                                 │
                                              ┌──────────────────┘
                                              ▼
                                    develop 分支积累变更
                                              │
                                              ▼
                                    Bump 版本 + 更新 CHANGELOG
                                              │
                                              ▼
                                    Release PR (develop → main)
                                              │
                                              ▼
                                    CI 通过 → 合并 → 自动发布
                                              │
                                              ▼
                                    GitHub Release + Git Tag
```

## 2. 开发阶段

### 2.1 创建 Issue

```bash
# 使用 gh CLI 创建
gh issue create
```

### 2.2 创建分支

> **注意**：本项目使用 **bare repo worktree 模式**，不使用 `git checkout` 切换分支。每个分支对应一个独立目录，通过 `cd` 导航。

```bash
# 从 develop worktree 创建 feature worktree
cd D:/workspace/10-software-project/projects/my-marketplace/develop
git pull origin develop
git worktree add ../feature/<issue-id>-<description> -b feature/<issue-id>-<description> develop

# 示例
git worktree add ../feature/12-add-release-skill -b feature/12-add-release-skill develop
cd ../feature/12-add-release-skill
```

分支类型对照：

| Issue 类型 | 分支前缀 | 来源 |
|-----------|----------|------|
| 功能/需求 | `feature/` | develop |
| Bug 报告 | `bugfix/` | develop |
| 文档变更 | `documentation/` | develop |
| 维护任务 | `maintain/` | develop |
| 紧急修复 | `hotfix/` | **main** |

### 2.3 开发与提交

```bash
# 提交格式
git commit -m "<type>(<scope>): <summary>"

# 示例
git commit -m "feat(mp-git): add release skill"
git commit -m "fix(mj-nlm): fix auth token refresh"
git commit -m "infra(ci): add version consistency check"
```

**Commit 类型**：feat, fix, perf, refactor, test, docs, infra
**Scope 值**：mj-nlm, mp-git, mp-dev, marketplace, ci, scripts, deps

### 2.4 更新 CHANGELOG

在提交功能变更后，更新对应的 CHANGELOG `[Unreleased]` 区块：

```bash
# 插件级变更 → 更新插件 CHANGELOG
vim plugins/mp-git/CHANGELOG.md

# 市场级变更 → 更新根 CHANGELOG
vim CHANGELOG.md
```

添加内容到 `[Unreleased]` 下的合适分类（Added/Changed/Fixed/Removed）。

### 2.5 推送与创建 PR

```bash
# 推送分支
git push -u origin feature/12-add-release-skill

# 创建 PR（使用对应模板）
gh pr create --base develop --head feature/12-add-release-skill \
  --title "feat(mp-git): add release skill" \
  --body-file <filled-template>
```

### 2.6 CI 通过 → 合并

```bash
# 检查 CI 状态
gh pr checks <pr-number>

# 合并后清理 worktree 和分支
cd D:/workspace/10-software-project/projects/my-marketplace/develop
git pull origin develop
git worktree remove ../feature/12-add-release-skill
git branch -d feature/12-add-release-skill
# 可选：远程分支通常在 PR 合并后由 GitHub 自动删除
git push origin --delete feature/12-add-release-skill
```

## 3. 发布阶段

### 3.1 确定版本号

| 变更类型 | 版本变化示例 |
|----------|-------------|
| 新增 Skill | mp-git 1.0.0 → 1.1.0 |
| 修复 Skill Bug | mj-nlm 1.0.0 → 1.0.1 |
| 新增 Plugin | marketplace 1.0.0 → 1.1.0 |
| 删除 Plugin / 破坏性变更 | marketplace 1.0.0 → 2.0.0 |

### 3.2 Bump 版本号

在 develop worktree 中执行：

```bash
cd D:/workspace/10-software-project/projects/my-marketplace/develop
git pull origin develop
```

**仅插件变更**：

```powershell
# 预览
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git" -DryRun

# 执行
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git"
```

**市场级变更**：

```powershell
# 预览
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -DryRun

# 执行
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0"
```

**混合变更**：先 bump 各插件，再 bump marketplace。

### 3.3 更新 CHANGELOG 正式版本节

将 `[Unreleased]` 内容转为正式版本节：

**Before**：
```markdown
## [Unreleased]

### Added
- 新增 release skill

## [1.0.0] - 2026-03-18
```

**After**：
```markdown
## [Unreleased]

## [1.1.0] - 2026-03-20

### Added
- 新增 release skill

## [1.0.0] - 2026-03-18
```

对所有涉及变更的 CHANGELOG 执行此操作（根级和/或插件级）。

### 3.4 提交发布变更

```bash
git add VERSION .claude-plugin/marketplace.json CHANGELOG.md
# 如有插件变更，也加上：
git add plugins/mp-git/.claude-plugin/plugin.json plugins/mp-git/CHANGELOG.md

git commit -m "infra(marketplace): release v1.1.0"
git push origin develop
```

### 3.5 创建 Release PR

```bash
gh pr create \
  --base main \
  --head develop \
  --title "Release v1.1.0" \
  --body-file <filled-release-template>
```

Release PR 模板审核要点：
- [ ] CHANGELOG.md 完整性（`[Unreleased]` 已转为正式版本节）
- [ ] VERSION 文件与 marketplace.json 版本一致
- [ ] 各 plugin.json 版本号与 marketplace.json plugins 数组一致
- [ ] 无残留调试代码
- [ ] 无未关闭的阻塞性 Issue

### 3.6 合并 → 自动发布

合并 Release PR 后，release.yml 自动执行：

1. 读取 `VERSION` 文件
2. 创建 git tag `vX.Y.Z`
3. 从 `CHANGELOG.md` 提取发布说明
4. 创建 GitHub Release

验证发布成功：

```bash
# 检查 tag
git fetch --tags
git tag -l "v1.1.0"

# 检查 GitHub Release
gh release view v1.1.0
```

## 4. Hotfix 流程

用于修复已发布版本的紧急问题。

### 4.1 创建 Hotfix 分支

```bash
# 从 main worktree 创建 hotfix worktree
cd D:/workspace/10-software-project/projects/my-marketplace/main
git pull origin main
git worktree add ../hotfix/<issue-id>-<description> -b hotfix/<issue-id>-<description> main
cd ../hotfix/<issue-id>-<description>
```

### 4.2 修复 + Bump Patch 版本

```bash
# 修复问题
git commit -m "fix(mp-git): fix push skill crash on empty repo"

# Bump patch 版本
.\scripts\bump-version.ps1 -From "1.1.0" -To "1.1.1"
# 或 bump 插件版本
.\scripts\bump-version.ps1 -From "1.1.0" -To "1.1.1" -Scope "mp-git"

# 更新 CHANGELOG
# 直接写入正式版本节（hotfix 不走 [Unreleased]）
```

### 4.3 创建 Hotfix PR → main

```bash
gh pr create \
  --base main \
  --head hotfix/<issue-id>-<description> \
  --title "fix(mp-git): fix push skill crash on empty repo" \
  --body-file <filled-hotfix-template>
```

### 4.4 合并后同步 develop

```bash
cd D:/workspace/10-software-project/projects/my-marketplace/develop
git pull origin develop
git merge main
git push origin develop

# 清理 hotfix worktree
git worktree remove ../hotfix/<issue-id>-<description>
git branch -d hotfix/<issue-id>-<description>
```

## 5. 回滚流程

如发布版本存在严重问题且无法快速 hotfix：

```bash
# 删除错误的 GitHub Release
gh release delete v1.1.0 --yes

# 删除错误的 tag
git tag -d v1.1.0
git push origin --delete v1.1.0

# 然后走 hotfix 流程发布修正版本
```

## 6. 检查清单

### 发布前检查

- [ ] 所有目标变更已合并到 develop
- [ ] CI 全部通过（Validate Structure: SUCCESS）
- [ ] CHANGELOG 已从 `[Unreleased]` 转为正式版本节
- [ ] VERSION 文件已更新
- [ ] marketplace.json 版本与 VERSION 一致
- [ ] 各 plugin.json 版本与 marketplace.json 一致
- [ ] 无未关闭的阻塞性 Issue

### 发布后验证

- [ ] GitHub Release 已自动创建
- [ ] Git tag 已生成（`git tag -l "vX.Y.Z"`）
- [ ] Release notes 内容正确
- [ ] `gh release view vX.Y.Z` 输出无异常

## 7. 相关文档

- [项目概览](<./[GUIDE]_Marketplace_Project_Overview.md>) — 项目整体概览
- [版本管理指南](<./[GUIDE]_Version_Management.md>) — 版本管理详细指南
- [CONTRIBUTING.md](./CONTRIBUTING.md) — 贡献指南
