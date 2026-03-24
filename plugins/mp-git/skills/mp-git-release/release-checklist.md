# Release Checklist & Reference

## 发布前检查清单

| # | 检查项 | 命令 | 通过条件 |
|---|--------|------|----------|
| 1 | develop 有新变更 | `git log $(git describe --tags --abbrev=0)..HEAD --oneline` | 输出非空 |
| 2 | 工作目录干净 | `git status --short` | 输出为空 |
| 3 | 与 origin 同步 | `git fetch origin && git diff develop origin/develop` | 无差异 |
| 4 | CHANGELOG [Unreleased] 已清空 | 检查 CHANGELOG.md | [Unreleased] 下无内容（已移到版本号下） |
| 5 | VERSION 与 marketplace.json 一致 | 比较两个文件的版本号 | 一致 |
| 6 | 各 plugin.json 与 marketplace.json 一致 | 逐个比较 | 一致 |
| 7 | README 版本表正确 | 检查 README.md 插件目录表 | 版本号与 plugin.json 匹配 |

## 版本号速查表

### Marketplace 版本

| 场景 | Bump | 示例 |
|------|------|------|
| 新增插件 | MINOR | 1.2.0 → 1.3.0 |
| 新增 skill | MINOR | 1.2.0 → 1.3.0 |
| 修复 skill 内容 | PATCH | 1.2.0 → 1.2.1 |
| 修复脚本 bug | PATCH | 1.2.0 → 1.2.1 |
| 删除/重命名 skill | MAJOR | 1.2.0 → 2.0.0 |
| 仅文档变更 | PATCH | 1.2.0 → 1.2.1 |

### Plugin 版本

独立于 marketplace 版本。规则相同但作用域限于该插件。

**只 bump 变更了的插件**。未变更的插件版本保持不变。

## bump-version.ps1 用法

```powershell
# 预览（不修改文件）
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -DryRun
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git" -DryRun

# 执行
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git"
.\scripts\bump-version.ps1 -From "1.2.0" -To "1.3.0"

# 支持的 Scope 值
# marketplace (default), mj-nlm, mp-git, mp-dev, flora-ptm
```

**执行顺序**：先 plugin scope，后 marketplace scope。

**修改的文件**：

| Scope | 文件 |
|-------|------|
| marketplace | `VERSION`, `.claude-plugin/marketplace.json` (metadata), `README.md` (badge) |
| plugin | `plugins/<name>/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (plugins[]), `README.md` (表格) |

## CHANGELOG 格式模板

### 新版本条目

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- <新增功能描述>

### Changed
- <行为变更描述>

### Fixed
- <修复描述>
```

### Commit type → CHANGELOG section 映射

| Commit Type | CHANGELOG Section |
|-------------|-------------------|
| `feat` | Added |
| `fix` | Fixed |
| `perf` / `refactor` | Changed |
| `infra` | Changed（仅重要变更） |
| `docs` / `test` | 通常不记录 |

## Release Commit Message 格式

```
release(marketplace): bump version to X.Y.Z

- marketplace: A.B.C → X.Y.Z
- <plugin>: D.E.F → G.H.I
- <一行变更摘要>

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

## Release PR Body 模板

```markdown
## Highlights
<!-- 从 CHANGELOG [X.Y.Z] 段落提取核心变更 -->

### Versions
| Plugin | Version |
|--------|---------|
| mj-nlm | x.y.z |
| mp-git | x.y.z |
| mp-dev | x.y.z |
| flora-ptm | x.y.z |

## 审核要点
- [ ] CHANGELOG.md 完整（[Unreleased] 已转为正式版本节）
- [ ] VERSION 与 marketplace.json 一致
- [ ] 各 plugin.json 版本与 marketplace.json 一致
- [ ] 无残留调试代码
- [ ] 无未关闭的阻塞性 Issue
```

## 常见问题

### POM 同步问题

**问题**：bump plugin 版本后 README.md 插件目录表未更新。
**原因**：`bump-version.ps1` 的 plugin scope 需包含 `README.md` 作为目标文件。
**检查**：bump 后检查 `README.md` 中插件版本表是否匹配 `plugin.json`。

### CI 发布失败

**问题**：PR 合并后 `release.yml` 未创建 tag。
**原因**：VERSION 文件格式不正确或 tag 已存在。
**检查**：
```bash
cat VERSION                    # 必须是纯数字 X.Y.Z
git tag -l "v$(cat VERSION)"   # 不应有输出（tag 不存在）
```

### CHANGELOG 提取失败

**问题**：GitHub Release body 为空。
**原因**：CHANGELOG.md 中版本号格式不匹配 `## [X.Y.Z]`。
**检查**：确保 CHANGELOG 使用 `## [X.Y.Z] - YYYY-MM-DD` 格式。
