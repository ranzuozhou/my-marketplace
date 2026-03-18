# CHANGELOG Format Reference

mp-dev:changelog 技能的 CHANGELOG 管理参考文件。定义双层管理规则、scope 映射和条目编写规范。

---

## 双层管理规则

my-marketplace 仓库采用双层 CHANGELOG 管理：

| 层级 | 文件路径 | 记录范围 |
|------|---------|---------|
| **仓库层** | `CHANGELOG.md`（根目录） | 仓库基础设施变更（CI、脚本、PR 模板、marketplace.json 结构、全局文档） |
| **插件层** | `plugins/<name>/CHANGELOG.md` | 插件自身的 skill、参考文件、plugin.json 变更 |

### 判断规则

- 变更影响单个 plugin 内部 → 写入插件层 CHANGELOG
- 变更影响仓库基础设施或跨 plugin → 写入仓库层 CHANGELOG
- 一次变更可能同时影响两个层（例如：新增 plugin 时，plugin 层记录"初始发布"，仓库层记录"新增 plugin 注册"）

---

## Scope → Layer 映射

| Scope（变更范围） | 目标 CHANGELOG 层 | 说明 |
|-------------------|-------------------|------|
| `marketplace` | 仓库层 | marketplace.json 结构变更 |
| `mp-git` | 插件层 (`plugins/mp-git/CHANGELOG.md`) | mp-git 插件变更 |
| `mp-dev` | 插件层 (`plugins/mp-dev/CHANGELOG.md`) | mp-dev 插件变更 |
| `mj-nlm` | 插件层 (`plugins/mj-nlm/CHANGELOG.md`) | mj-nlm 插件变更 |
| `scripts` | 仓库层 | bump-version.ps1、clone-bare.ps1 等 |
| `ci` | 仓库层 | .github/workflows/ 变更 |
| `docs` | 仓库层 | 根目录 README.md 等全局文档 |

---

## Commit Type → CHANGELOG Category 映射

| Commit Type | CHANGELOG Category | 说明 |
|-------------|-------------------|------|
| `feat` | **Added** | 新功能 |
| `enhance` | **Changed** | 对已有功能的增强 |
| `fix` | **Fixed** | Bug 修复 |
| `refactor` | **Changed** | 重构（不改变外部行为） |
| `docs` | **Changed** （或不记录） | 文档更新（重要的记录为 Changed） |
| `test` | （通常不记录） | 测试变更 |
| `chore` | （通常不记录） | 杂务（依赖更新等） |
| `BREAKING CHANGE` | **Changed** + 标注 | 破坏性变更，需特别标注 |
| 删除功能 | **Removed** | 移除已有功能 |
| 废弃预告 | **Deprecated** | 即将移除的功能 |
| 安全修复 | **Security** | 安全相关修复 |

---

## Keep a Changelog 格式模板

```markdown
# Changelog

All notable changes to <scope> will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- <新增条目>

### Changed
- <变更条目>

### Fixed
- <修复条目>

## [1.1.0] - 2026-04-01

### Added
- <条目>

### Fixed
- <条目>

## [1.0.0] - 2026-03-18

### Added
- 初始发布：<概述>
```

---

## 条目编写指南

### 格式要求

- 每条以 `- ` 开头（Markdown 无序列表）
- 使用中文描述
- 简洁明了，一行说清一件事
- 关联 skill 时用反引号标记：`` `mp-dev:validate` ``

### 好的条目示例

```markdown
### Added
- 新增 `mp-dev:validate` 技能，支持 V1-V7 共 7 条结构校验规则
- 新增 validate_plugin.py 脚本，自动化 V1-V6 检查
- 新增 `--scope` 参数支持，限定校验范围到单个 plugin

### Changed
- 优化 `mp-dev:scaffold` 的 marketplace.json 注册流程，自动检测已有条目
- 重构 CHANGELOG 双层判断逻辑，使用 scope 映射表替代硬编码

### Fixed
- 修复 `mp-dev:release` 在 DryRun 模式下仍写入版本号的问题
```

### 不好的条目示例

```markdown
- 修了一些 bug（太模糊）
- Updated code（无意义）
- 大量重构和优化（不具体）
```

---

## 发布时 CHANGELOG 转换

发布版本时，将 `[Unreleased]` 节转换为版本号节：

**转换前**：
```markdown
## [Unreleased]

### Added
- 新增 xxx

### Fixed
- 修复 xxx
```

**转换后**：
```markdown
## [Unreleased]

## [1.1.0] - 2026-04-01

### Added
- 新增 xxx

### Fixed
- 修复 xxx
```

**注意**：
- 保留空的 `[Unreleased]` 节（后续变更继续写入）
- 日期格式：`YYYY-MM-DD`
- 版本号遵循语义化版本
