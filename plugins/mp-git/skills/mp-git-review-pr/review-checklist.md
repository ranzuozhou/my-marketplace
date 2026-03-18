# PR Review Checklist

> 本文件定义 mp-git-review-pr skill 的检查项内容。触发条件和执行顺序见 SKILL.md。

---

## 固定检查

### F1 — 分支同步状态（ℹ️ 信息展示）

- **检查**: base branch 落后提交数
- **方法**: `git log HEAD..origin/{base_branch} --oneline`
- **输出**: "同步" 或 "落后 N 个提交"

### F2 — 变更概览（ℹ️ 信息展示）

- **检查**: 变更文件统计与分类
- **方法**: `git diff {base}...HEAD --stat` + `git log {base}...HEAD --oneline`
- **分类**: 按文件分类规则将文件归类为 Plugin / Skill / Config / Docs / Scripts / CI / Other
- **输出**: 分类统计表 + commit 列表

**文件分类规则**:

| 分类 | 匹配路径 | 说明 |
|------|---------|------|
| Plugin | `plugin.json` / `.mcp.json` / `CLAUDE.md` / `README.md`（插件级） | 插件元数据和文档 |
| Skill | `skills/**/SKILL.md` + reference files（非 CLAUDE.md/README.md） | 技能定义和参考文件 |
| Config | `.claude-plugin/` / `VERSION` / `marketplace.json` | 市场配置文件 |
| Docs | `docs/**` | 项目文档 |
| Scripts | `scripts/**` | 基础设施脚本 |
| CI | `.github/**` | CI/CD 工作流和模板 |
| Other | 不匹配以上任何规则的文件 | 需人工判断的文件 |

### F3 — Commit 规范（合规检查）

- **检查**: commit type 是否匹配分支类型
- **为什么**: commit type 不匹配分支类型意味着变更内容超出了分支职责范围
- **通过标准**: 所有 commit 的 type 都在分支允许范围内

**Branch×Type 速查**:

| 分支类型 | 允许的 commit type |
|----------|-------------------|
| feature/* | feat, perf, refactor, test, docs |
| bugfix/* | fix, test, docs |
| hotfix/* | fix |
| documentation/* | docs |
| maintain/* | infra, docs |
| release (develop→main) | 所有 type |

---

## 动态检查

> 动态检查基于 PR 中实际变更的文件触发。仅当触发条件满足时才执行对应检查。

### D1 — 插件目录结构（Important）

- **触发条件**: `plugins/` 下有新目录出现
- **检查**: 新插件目录结构是否完整
- **检查内容**:
  1. `.claude-plugin/plugin.json` 存在
  2. `CLAUDE.md` 存在
  3. `README.md` 存在
  4. `CHANGELOG.md` 存在
  5. `skills/` 目录存在
- **通过标准**: 以上 5 项全部存在

### D2 — SKILL.md 完整性（Important）

- **触发条件**: `skills/**/SKILL.md` 有变更或新增
- **检查**: SKILL.md frontmatter 完整性
- **检查内容**:
  1. YAML frontmatter 存在（`---` 包裹）
  2. `name` 字段存在且非空
  3. `description` 字段存在且非空
  4. description 包含中文触发词（≥3 个）
  5. description 包含英文触发词（≥3 个）
- **通过标准**: 1-3 必须通过，4-5 为 WARN 级别
- **跳过条件**: `*-shared/` 目录下的文件不检查 frontmatter

### D3 — plugin.json 合规（Important）

- **触发条件**: `**/plugin.json` 有变更
- **检查**: plugin.json schema 合规 + 版本号一致性
- **检查内容**:
  1. 必填字段存在：name, description, version, author, license, skills
  2. `name` 与目录名匹配
  3. `version` 与 marketplace.json 中对应条目一致
  4. `skills` 数组中的路径指向实际存在的 SKILL.md
- **通过标准**: 1-4 全部通过

### D4 — marketplace.json 一致性（Important）

- **触发条件**: `.claude-plugin/marketplace.json` 有变更
- **检查**: 插件注册一致性
- **检查内容**:
  1. 每个 `plugins[]` 条目的 `name` 对应 `plugins/` 下的实际目录
  2. `source` 字段格式正确（`plugins/<name>`）
  3. `metadata.version` 与 `VERSION` 文件一致
- **通过标准**: 1-3 全部通过

### D5 — VERSION 文件同步（Important）

- **触发条件**: `VERSION` 文件有变更
- **检查**: VERSION 与 marketplace.json 的 metadata.version 同步
- **检查内容**:
  1. `VERSION` 内容为合法 semver 格式
  2. `VERSION` 值与 `.claude-plugin/marketplace.json` 的 `metadata.version` 一致
- **通过标准**: 1-2 全部通过

### D6 — CHANGELOG 格式（Suggestion）

- **触发条件**: `**/CHANGELOG.md` 有变更
- **检查**: CHANGELOG 格式正确性
- **检查内容**:
  1. 遵循 Keep a Changelog 格式
  2. `[Unreleased]` 节存在
  3. 版本节格式：`## [X.Y.Z] - YYYY-MM-DD`
  4. 分类使用标准名称：Added / Changed / Fixed / Removed
- **通过标准**: 1-4 全部通过（Suggestion 级别，不阻塞合并）

---

## 触发条件汇总表

| 检查 | 触发文件模式 | 严重级别 |
|------|------------|---------|
| F1 | 始终执行 | ℹ️ Info |
| F2 | 始终执行 | ℹ️ Info |
| F3 | 始终执行 | ❌ Critical |
| D1 | `plugins/` 下新目录 | ❌ Important |
| D2 | `skills/**/SKILL.md` | ⚠️ Important |
| D3 | `**/plugin.json` | ❌ Important |
| D4 | `.claude-plugin/marketplace.json` | ❌ Important |
| D5 | `VERSION` | ❌ Important |
| D6 | `**/CHANGELOG.md` | ⚠️ Suggestion |

---

## docs/ 变更处理

检测到 `docs/` 变更时，输出提示：

> 文档变更已识别。如需深度文档质量检查，建议使用专门的文档审查工具。
