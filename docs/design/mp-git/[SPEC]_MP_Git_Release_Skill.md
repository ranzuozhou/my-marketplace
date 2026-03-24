---
tags:
  - spec
  - mp-git
  - release
  - skill
aliases:
  - MP Git Release Skill Specification
  - mp-git-release 技能设计规范
date: 2026-03-24
updated: 2026-03-24
version: v1.0
status: 定稿
owner: DevOps
service: mp-git
---

# mp-git-release 技能设计规范

## 1 背景与目标

### 1.1 问题

my-marketplace 的版本发布涉及多文件、多层级的手动操作：

1. **双层版本同步**：marketplace 整体版本 + 各插件独立版本，需分别 bump 并保持 marketplace.json 同步
2. **CHANGELOG 分散**：根目录 + 每个变更插件各有一份 CHANGELOG，需逐个更新
3. **POM 问题**：`bump-version.ps1` 的 plugin scope 曾遗漏 README.md 插件版本表更新
4. **Release PR 组装**：需手动读取模板、填充 Highlights、选择审核要点

### 1.2 目标

创建 `mp-git-release` 技能，将发布流程自动化为 7 步交互式工作流。技能定位于 mp-git 工作流链的末端：

```
mp-git-commit → mp-git-push → mp-git-release
                                    │
                                    ├── bump version (scripts/bump-version.ps1)
                                    ├── update CHANGELOG
                                    ├── commit + push
                                    └── create Release PR (develop → main)
                                         └── CI auto: tag + GitHub Release
```

### 1.3 适用范围

- **适用**：`ranzuozhou/my-marketplace` 仓库
- **不适用**：mj-system、mj-agentlab-marketplace、其他仓库

## 2 版本架构

### 2.1 双层独立版本

```
Marketplace 整体 (VERSION 文件)
├── 同步 → .claude-plugin/marketplace.json → metadata.version
├── 同步 → README.md → version badge
│
Plugin 独立版本 (plugins/<name>/.claude-plugin/plugin.json)
├── 同步 → .claude-plugin/marketplace.json → plugins[name].version
└── 同步 → README.md → 插件目录表 Version 列
```

Marketplace 和插件版本**互不影响**：只有变更的插件 bump 版本，未变更的保持不变。

### 2.2 语义化版本规则

| 组件 | 何时递增 | 示例 |
|------|----------|------|
| MAJOR | 不兼容变更：删除插件、重命名 skill、breaking API | 1.0.0 → 2.0.0 |
| MINOR | 新增功能：新 skill、新插件、新 hook | 1.0.0 → 1.1.0 |
| PATCH | 问题修复：SKILL.md 内容修正、脚本 bug 修复 | 1.0.0 → 1.0.1 |

### 2.3 版本文件位置

| 版本 | 权威文件 | 同步目标 |
|------|----------|----------|
| Marketplace | `VERSION` | `marketplace.json` → `metadata.version`; `README.md` badge |
| 各 Plugin | `plugins/<name>/.claude-plugin/plugin.json` → `version` | `marketplace.json` → `plugins[name].version`; `README.md` 表格 |

## 3 bump-version.ps1 脚本

### 3.1 两种 Scope

**Marketplace Scope（默认）**：
```powershell
.\scripts\bump-version.ps1 -From "1.2.0" -To "1.3.0" [-DryRun]
```
更新：`VERSION` + `marketplace.json` metadata.version + `README.md` badge

**Plugin Scope**：
```powershell
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git" [-DryRun]
```
更新：`plugins/mp-git/.claude-plugin/plugin.json` + `marketplace.json` plugins[mp-git].version + `README.md` 表格

### 3.2 执行顺序

多插件变更时：**先 bump 各插件（顺序不限），再 bump marketplace**。

```powershell
# 示例：mp-git 和 mj-nlm 都有变更
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.0.1" -Scope "mp-git"
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.0.1" -Scope "mj-nlm"
.\scripts\bump-version.ps1 -From "1.2.0" -To "1.2.1"  # marketplace
```

### 3.3 DryRun 模式

`-DryRun` 预览所有变更但不写入文件。技能应先执行 DryRun 展示给用户确认，再实际执行。

## 4 CHANGELOG 管理

### 4.1 文件位置

| 文件 | 记录范围 |
|------|----------|
| `CHANGELOG.md`（根目录） | Marketplace 级事件（跨插件摘要、新增/删除插件） |
| `plugins/<name>/CHANGELOG.md` | 该插件的具体变更 |

### 4.2 格式规范

基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)：

```markdown
## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- 新增的功能

### Changed
- 修改的行为

### Fixed
- 修复的问题

### Removed
- 删除的功能
```

### 4.3 发布时操作

1. 将 `[Unreleased]` 下的内容移动到新的 `[X.Y.Z] - YYYY-MM-DD` 标题下
2. `[Unreleased]` 变为空（保留标题）
3. 如果 `[Unreleased]` 为空（变更已在 PR merge 时记录），从 git log 提取变更摘要填入

## 5 发布工作流（7 步）

### Step 1: 分析变更范围

```bash
# 获取最新 tag
LAST_TAG=$(git describe --tags --abbrev=0)

# 查看变更文件
git diff --name-only $LAST_TAG..HEAD

# 按插件分组
git diff --name-only $LAST_TAG..HEAD | grep '^plugins/' | cut -d/ -f2 | sort -u
```

输出：变更了哪些插件，以及变更类型（feat/fix/infra）。

### Step 2: 确认版本号

根据变更类型推荐版本号，通过 AskUserQuestion 确认：

- 展示当前版本（marketplace + 各变更插件）
- 展示推荐的新版本
- 用户确认或手动修改

### Step 3: Bump 版本

```powershell
# DryRun 预览
.\scripts\bump-version.ps1 -From "X.Y.Z" -To "A.B.C" -Scope "<plugin>" -DryRun

# 用户确认后执行
.\scripts\bump-version.ps1 -From "X.Y.Z" -To "A.B.C" -Scope "<plugin>"

# 最后 bump marketplace
.\scripts\bump-version.ps1 -From "X.Y.Z" -To "A.B.C"
```

### Step 4: 更新 CHANGELOG

1. 从 git log 提取变更摘要
2. 更新根目录 CHANGELOG.md
3. 更新各变更插件的 CHANGELOG.md
4. 展示给用户确认

### Step 5: 提交发布

```bash
git add VERSION .claude-plugin/marketplace.json README.md CHANGELOG.md
git add plugins/*/CHANGELOG.md plugins/*/.claude-plugin/plugin.json

git commit -m "release(marketplace): bump version to X.Y.Z

- marketplace: A.B.C → X.Y.Z
- <plugin>: D.E.F → G.H.I
- <变更摘要>

Co-Authored-By: Claude <...>"

git push origin develop
```

### Step 6: 创建 Release PR

```bash
# 读取 release.md 模板
cat .github/PULL_REQUEST_TEMPLATE/release.md

# 填充字段 → 写入临时文件
# gh pr create
gh pr create \
  --base main \
  --head develop \
  --title "Release vX.Y.Z" \
  --body-file <tmp-file> \
  --reviewer <reviewer>
```

### Step 7: 验证（可选）

合并 PR 后，CI (`release.yml`) 自动：
1. 从 VERSION 提取版本号
2. 创建 git tag `vX.Y.Z`
3. 从 CHANGELOG 提取 release notes
4. 创建 GitHub Release

技能输出验证命令供用户使用。

## 6 人工交互节点

| # | 时机 | 触发条件 | 行为 |
|---|------|----------|------|
| H1 | Step 1 | develop 与 main 无差异 | 告知无需发布，停止 |
| H2 | Step 2 | 版本号确认 | AskUserQuestion 展示推荐版本，允许修改 |
| H3 | Step 3 | DryRun 预览 | 展示 bump 结果，确认后执行 |
| H4 | Step 4 | CHANGELOG 内容 | 展示生成的条目，允许编辑 |
| H5 | Step 6 | PR 提交 | 展示 PR 预览，确认提交 |

## 7 技能文件结构

```
plugins/mp-git/skills/mp-git-release/
├── SKILL.md                    # 技能主文件（7 步工作流 + 交互节点）
└── release-checklist.md        # 参考文件（版本规则、CHANGELOG 模板、常见问题）
```

## 8 与现有技能的关系

| 技能 | 关系 |
|------|------|
| mp-git-commit | 前置：发布前的提交已完成 |
| mp-git-push | 前置：代码已推送到 develop |
| mp-git-pr | 互补：release 内部调用 PR 创建逻辑，但使用 release.md 模板和 main 目标 |
| mp-git-check-merge | 后续：PR 创建后检查合并就绪状态 |

## 9 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| bump-version.ps1 遗漏文件 | 低 | 中 | DryRun 预览 + 用户确认 |
| CHANGELOG 格式错误 | 低 | 低 | 技能内置模板 |
| Release PR 合并后 CI 失败 | 低 | 中 | Step 7 提供验证命令 |
| 版本号冲突（tag 已存在） | 低 | 高 | release.yml 内置去重检查 |
