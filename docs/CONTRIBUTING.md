# 贡献指南 — My Marketplace

本文档面向人类贡献者，说明分支策略、提交规范、版本管理和发布流程。
Claude Code agent 行为规范请参考各 Plugin 的 SKILL.md（如 mp-git 的 commit-rules.md、branch-rules.md）。

## 分支策略

采用 Git Flow 模型。

### 永久分支

| 分支 | 用途 | 保护 |
|------|------|------|
| `main` | 生产就绪 | PR-only |
| `develop` | 集成主线 | PR-only |

### 临时分支

| 类型 | 来源 | 用途 |
|------|------|------|
| `feature/*` | develop | 新功能、新 Skill |
| `bugfix/*` | develop | Bug 修复 |
| `documentation/*` | develop | 纯文档变更 |
| `maintain/*` | develop | CI/CD、脚本、依赖维护 |
| `hotfix/*` | main | 紧急修复（PR 目标也是 main，合并后需同步 develop） |

### 命名规范

```
<type>/<issue-id>-<description>    # 有 Issue 时
<type>/<description>               # 无 Issue 时
```

示例：
- `feature/12-add-release-skill`
- `bugfix/25-commit-scope-error`
- `maintain/add-ci-workflow`

## 提交规范

### 格式

```
<type>(<scope>): <summary>
```

### 类型

| Type | 用途 |
|------|------|
| `feat` | 新功能、新 Skill |
| `fix` | Bug 修复 |
| `perf` | 性能优化 |
| `refactor` | 重构 |
| `test` | 测试 |
| `docs` | 文档 |
| `infra` | CI/CD、脚本、基础设施 |

### Scope

| Scope | 范围 |
|-------|------|
| `mj-nlm` | mj-nlm Plugin |
| `mp-git` | mp-git Plugin |
| `mp-dev` | mp-dev Plugin |
| `marketplace` | Marketplace 整体（README、marketplace.json、release） |
| `ci` | CI/CD workflows |
| `scripts` | 脚本（bump-version 等） |
| `deps` | 依赖管理 |

### 规则

- summary 小写开头，不加句号，≤72 字符
- 示例：`feat(mp-git): add worktree cleanup to delete skill`
- 示例：`infra(ci): add SKILL.md frontmatter validation`

## 版本管理

### 语义化版本

遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)：`MAJOR.MINOR.PATCH`

### 双层版本

| 层级 | 权威源 | 说明 |
|------|--------|------|
| Marketplace 整体 | `VERSION` 文件 | 新增/删除 Plugin、跨 Plugin 变更 |
| 各 Plugin 独立 | `plugins/<name>/.claude-plugin/plugin.json` | Plugin 内部变更 |

两者独立升级，互不影响。

### 版本升级

```powershell
# 升级 marketplace 版本
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -DryRun
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0"

# 升级某个 plugin 版本
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git"
```

### 规则

- Feature/bugfix 分支**不**修改版本号
- 版本升级在 develop 分支上执行，合并到 main 时触发自动发布

## CHANGELOG 规范

格式：[Keep a Changelog](https://keepachangelog.com/zh-CN/)

- 根 `CHANGELOG.md`：Marketplace 级事件
- 各 Plugin `CHANGELOG.md`：Plugin 内部变更
- 所有变更先写入 `[Unreleased]`，发布时转为正式版本节
- 分类：Added / Changed / Fixed / Removed

## 发布流程

1. 在 develop 分支上 bump 版本号（marketplace 和/或各 plugin）
2. 更新 CHANGELOG.md：`[Unreleased]` → `[X.Y.Z] - YYYY-MM-DD`
3. Commit: `infra(marketplace): release v1.1.0`
4. 创建 PR：develop → main（使用 release PR 模板）
5. 合并后自动触发：创建 git tag → GitHub Release

## 回滚流程

如发布版本存在问题，按以下步骤回滚：

1. 从 main 创建 hotfix 分支修复问题
2. 修复后 bump 为 patch 版本（如 1.1.0 → 1.1.1）
3. 走正常的 hotfix PR 流程
4. 如需删除错误的 GitHub Release：`gh release delete vX.Y.Z --yes`
5. 如需删除错误的 tag：`git tag -d vX.Y.Z && git push origin --delete vX.Y.Z`

## Bare Repo + Worktree

本项目使用 bare repo + worktree 模式管理多分支：

```bash
# 首次克隆（使用专用脚本）
powershell -ExecutionPolicy Bypass -File .\my-marketplace-clone-bare.ps1 \
  -RepoUrl https://github.com/ranzuozhou/my-marketplace

# 添加新分支 worktree
powershell -ExecutionPolicy Bypass -File .\my-marketplace-clone-bare.ps1 \
  -RepoUrl https://github.com/ranzuozhou/my-marketplace \
  -Branches "feature/12-add-new-skill"
```

结构：
```
my-marketplace/
├── .bare/       # bare repo（共享对象库）
├── .git         # 指针文件 (gitdir: ./.bare)
├── develop/     # develop worktree
├── feature/     # feature 分支 worktree
└── main/        # main worktree
```

## 推送

```bash
git push origin HEAD
```
