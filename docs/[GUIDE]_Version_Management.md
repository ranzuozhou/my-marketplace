> **[GUIDE] 版本管理指南 — My Marketplace**
> 说明双层版本架构、版本升级工具、CHANGELOG 规范和 CI/CD 自动化机制。

## 1. 版本架构

### 1.1 双层独立版本

Marketplace 采用**双层独立版本管理**，marketplace 整体和各插件各自维护版本号，互不影响。

```
版本层级
├── Marketplace 整体 v1.0.0      ← VERSION 文件（权威源）
│   同步 → marketplace.json metadata.version
│
├── mj-nlm v1.0.0               ← plugins/mj-nlm/.claude-plugin/plugin.json（权威源）
│   同步 → marketplace.json plugins[name=mj-nlm].version
│
├── mp-git v1.0.0                ← plugins/mp-git/.claude-plugin/plugin.json
└── mp-dev v1.0.0                ← plugins/mp-dev/.claude-plugin/plugin.json
```

### 1.2 语义化版本

遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)：`MAJOR.MINOR.PATCH`

| 组件 | 何时递增 |
|------|----------|
| MAJOR | 不兼容的 API 变更（如删除插件、重命名 skill） |
| MINOR | 向后兼容的新功能（如新增 skill、新增插件） |
| PATCH | 向后兼容的问题修复（如修复 SKILL.md 内容错误） |

### 1.3 版本文件位置

| 版本 | 权威文件 | 同步目标 |
|------|----------|----------|
| Marketplace 整体 | `VERSION`（纯文本） | `.claude-plugin/marketplace.json` → `metadata.version` |
| mj-nlm | `plugins/mj-nlm/.claude-plugin/plugin.json` → `version` | `.claude-plugin/marketplace.json` → `plugins[name=mj-nlm].version` |
| mp-git | `plugins/mp-git/.claude-plugin/plugin.json` → `version` | 同上模式 |
| mp-dev | `plugins/mp-dev/.claude-plugin/plugin.json` → `version` | 同上模式 |

## 2. bump-version.ps1 脚本

### 2.1 参数

```powershell
param(
    [Parameter(Mandatory=$true)]  [string]$From,      # 当前版本
    [Parameter(Mandatory=$true)]  [string]$To,        # 目标版本
    [ValidateSet("marketplace","mj-nlm","mp-git","mp-dev")]
    [string]$Scope = "marketplace",                    # 升级范围
    [switch]$DryRun                                    # 预览模式
)
```

### 2.2 Scope 行为

| Scope | 更新文件 |
|-------|----------|
| `marketplace` | `VERSION`, `.claude-plugin/marketplace.json`(metadata.version) |
| `mj-nlm` | `plugins/mj-nlm/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`(plugins[name=mj-nlm].version) |
| `mp-git` | `plugins/mp-git/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`(plugins[name=mp-git].version) |
| `mp-dev` | `plugins/mp-dev/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`(plugins[name=mp-dev].version) |

### 2.3 使用示例

```powershell
# 预览 marketplace 版本升级
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -DryRun

# 执行 marketplace 版本升级
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0"

# 预览某个插件版本升级
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git" -DryRun

# 执行某个插件版本升级
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git"
```

### 2.4 输出格式

```
[DryRun] Preview mode - no files will be modified
Scope: marketplace
Version: 1.0.0 -> 1.1.0
------------------------------------------------------------

  [MATCH] VERSION (1 occurrences)
    L1: 1.0.0
      -> 1.1.0

  [MATCH] .claude-plugin/marketplace.json (1 occurrences, scoped: marketplace)
    L10: "version": "1.0.0"
      -> "version": "1.1.0"
```

## 3. CHANGELOG 规范

### 3.1 格式

遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，使用 4 种分类：

| 分类 | 用途 |
|------|------|
| **Added** | 新功能、新 Skill、新插件 |
| **Changed** | 现有功能的变更 |
| **Fixed** | Bug 修复 |
| **Removed** | 删除的功能 |

### 3.2 双层 CHANGELOG

| CHANGELOG | 记录范围 | 示例条目 |
|-----------|----------|----------|
| 根 `CHANGELOG.md` | Marketplace 级事件 | "新增 mp-dev 插件"、"CI 新增版本一致性校验" |
| `plugins/<name>/CHANGELOG.md` | 插件内部变更 | "新增 check-merge skill"、"修复 commit scope 推断" |

### 3.3 工作流

1. **开发阶段**：所有变更写入 `[Unreleased]` 区块
2. **发布阶段**：`[Unreleased]` 内容转为 `[X.Y.Z] - YYYY-MM-DD` 正式版本节
3. 发布后 `[Unreleased]` 清空，准备接收下一轮变更

```markdown
## [Unreleased]

### Added
- 新增 release skill（branch → tag → GitHub Release）

## [1.0.0] - 2026-03-18

### Added
- 初始发布：5 个 Skill
```

## 4. CI/CD 自动化

### 4.1 CI — 结构校验（ci.yml）

**触发条件**：
- push: `feature/*`, `bugfix/*`, `documentation/*`, `maintain/*`, `hotfix/*`
- pull_request: `develop`, `main`

**6 项校验**：

| # | 检查项 | 失败示例 |
|---|--------|----------|
| 1 | plugin.json 字段完整 | `ERROR: plugins/mp-git/.claude-plugin/plugin.json missing field: license` |
| 2 | marketplace.json 插件目录匹配 | `ERROR: marketplace.json references 'mp-foo' but directory not found` |
| 3 | SKILL.md frontmatter | `ERROR: SKILL.md missing frontmatter field: description` |
| 4 | 目录结构 | `ERROR: plugins/mp-git missing required file: CLAUDE.md` |
| 5 | 版本一致性 | `ERROR: VERSION (1.1.0) != marketplace.json (1.0.0)` |
| 6 | CHANGELOG 存在性 | `ERROR: plugins/mp-git/CHANGELOG.md not found` |

### 4.2 Release — 自动发布（release.yml）

**触发条件**：VERSION 文件变更推送到 main（`paths: ['VERSION']`）

**流程**：

```
读取 VERSION → 验证格式 → 检查 tag 是否已存在
  ├── 已存在 → 跳过（幂等）
  └── 不存在 → 创建 tag → 从 CHANGELOG 提取发布说明 → 创建 GitHub Release
```

**幂等性**：如果 tag 已存在（如重复推送），workflow 不会创建重复 Release。

## 5. 版本升级场景

### 场景 A：仅插件变更

例：给 mp-git 新增一个 skill

1. 在 `feature/xx-new-skill` 分支开发
2. 更新 `plugins/mp-git/CHANGELOG.md` 的 `[Unreleased]`
3. 发布时 bump mp-git: `-Scope "mp-git" -From "1.0.0" -To "1.1.0"`
4. **Marketplace 版本不变**

### 场景 B：市场级变更

例：新增一个插件

1. 更新根 `CHANGELOG.md` 的 `[Unreleased]`
2. 发布时 bump marketplace: `-From "1.0.0" -To "1.1.0"`
3. **各插件版本不变**（除非它们也有变更）

### 场景 C：混合变更

1. 先分别 bump 变更的插件
2. 再 bump marketplace 版本
3. 两层 CHANGELOG 各自更新

## 6. 版本规则

| 规则 | 说明 |
|------|------|
| Feature/bugfix 分支**不**修改版本号 | 版本升级只在发布时执行 |
| 版本升级在 develop worktree 中执行 | `cd` 到 develop worktree 后操作，合并到 main 时触发自动发布 |
| VERSION 文件是 marketplace 版本的唯一权威源 | bump 脚本自动同步 marketplace.json |
| plugin.json 是各插件版本的唯一权威源 | bump 脚本自动同步 marketplace.json |

## 7. 相关文档

- [项目概览](<./[GUIDE]_Marketplace_Project_Overview.md>) — 项目整体概览
- [发布操作手册](<./[RUNBOOK]_Release_Operations.md>) — 发布操作手册
- [CONTRIBUTING.md](./CONTRIBUTING.md) — 贡献指南
