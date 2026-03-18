# Commit Rules Reference

## Commit Type 定义

| Type | 含义 | 何时使用 |
|------|------|---------|
| `feat` | 新功能 | 新增用户可感知的功能或能力 |
| `fix` | Bug 修复 | 修复已有功能的缺陷 |
| `perf` | 性能优化 | 以提升性能为目的的变更（查询优化、缓存、并发） |
| `refactor` | 重构 | 不改变外部行为的代码重组（目的是"更清晰"） |
| `test` | 测试相关 | 新增或修改测试用例 |
| `docs` | 文档变更 | 仅修改文档文件（`docs/`、`README.md`、`CHANGELOG.md` 等） |
| `infra` | 基础设施 | CI/CD、依赖更新、脚本、配置等不影响业务源码的变更 |

> `merge` 用于合并提交：`merge: 合并 develop 最新内容，解决冲突` — 由合并操作产生，不手动选择。

**判断辅助**：目的是"更快"→ `perf`；目的是"更清晰"→ `refactor`；改的是工具链/配置 → `infra`

## Branch × Commit Type Allowed Matrix

| 分支类型 | `feat` | `fix` | `perf` | `refactor` | `test` | `docs` | `infra` |
|---------|--------|-------|--------|------------|--------|--------|---------|
| `feature/*` | ✓ | — | ✓ | ✓ | ✓ | ✓ | — |
| `bugfix/*` | — | ✓ | — | — | ✓ | ✓ | — |
| `documentation/*` | — | — | — | — | — | ✓ | — |
| `maintain/*` | — | — | — | — | — | ✓ | ✓ |
| `hotfix/*` | — | ✓ | — | — | — | — | — |

> 与 mp-git-push Step 2 和 branch-rules.md 完全一致。

## Branch Type vs Commit Type 命名区分

| 分支类型（全称/复合词） | Commit 类型（缩写/不同词） | 命名区分方式 |
|------------------------|--------------------------|------------|
| `feature` | `feat` | 全称 ≠ 缩写 |
| `bugfix` | `fix` | 复合词 ≠ 简称 |
| `documentation` | `docs` | 全称 ≠ 缩写 |
| `maintain` | `infra` | 完全不同的词 |
| `hotfix` | `fix` | 复合词 ≠ 简称 |

常见错误：用 `feature` 作 commit type，或 `feat` 作分支前缀。

## 文件排除模式

### 硬性阻断（绝不提交）

| 模式 | 原因 |
|------|------|
| `.env` | API 密钥、Token、凭据 |
| `*.pem`, `*.key`, `*.p12`, `*.pfx` | 私钥/证书 |
| 明文包含 `password=`, `secret=`, `token=` 的文件 | 嵌入式密钥 |

### 软性阻断（提交前询问）

| 模式 | 原因 |
|------|------|
| 文件 > 10 MB | 大二进制应用 Git LFS 或排除 |
| `*.csv`, `*.xlsx`, `*.xls` | 数据文件 |
| `*.zip`, `*.rar`, `*.7z` | 归档文件 |
| `*.sqlite`, `*.db` | 数据库文件 |

### 自动跳过（.gitignore 已覆盖）

- `__pycache__/`, `*.pyc`, `*.pyo`, `*.egg-info/`
- `.venv/`, `venv/`, `env/`
- `.idea/`, `.vscode/`, `*.swp`, `*.swo`
- `Thumbs.db`, `.DS_Store`, `desktop.ini`
- `.claude/settings.local.json`, `.serena/`

## Scope 映射表

### 插件级 Scope

| Scope | 匹配路径 | 说明 |
|-------|---------|------|
| `marketplace` | `.claude-plugin/`、`VERSION`、根级文件 | 市场级变更 |
| `mp-git` | `plugins/mp-git/**` | mp-git 插件变更 |
| `mp-dev` | `plugins/mp-dev/**` | mp-dev 插件变更 |
| `mj-nlm` | `plugins/mj-nlm/**` | mj-nlm 插件变更 |
| `scripts` | `scripts/**` | 基础设施脚本 |
| `ci` | `.github/**` | CI/CD 配置 |
| `docs` | `docs/**` | 文档 |

### 根级文件归属规则

| 文件 | 归属 Scope | 说明 |
|------|-----------|------|
| `.gitignore` | `marketplace` | 仓库级配置 |
| `CLAUDE.md`（根目录） | `marketplace` | 仓库级说明 |
| `README.md`（根目录） | `marketplace` | 仓库级文档 |
| `VERSION` | `marketplace` | 已在映射表中 |
| `.claude-plugin/*` | `marketplace` | 已在映射表中 |

### 多 Scope 处理

| 情况 | Scope 选择 |
|------|-----------|
| 所有文件在同一插件 | 使用插件名（如 `mp-git`） |
| 跨插件但同一类型 | 使用层 scope（如 `scripts`） |
| 基础设施 + 相关文档 | 使用基础设施 scope |
| 真正混合，无主导 | 省略 scope：`feat: <summary>` |

### 跨 Scope 拆分规则（Soft ask）

- 跨插件变更**建议**拆分提交（如同时修改 mp-git 和 mj-nlm 应拆为两个 commit）
- 拆分为建议性质，不强制阻断提交流程
- 提示信息示例：`"检测到跨 scope 变更（mp-git + mj-nlm），建议拆分为独立提交。是否继续合并提交？"`

### 多 Scope 冲突规则

- 当单次提交涉及多个 scope 且用户选择不拆分时，以变更主体（行数最多的 scope）为主 scope
- 次要 scope 在 commit body 中以 `Also-affects: <scope>` 标注

## 拆分决策指南

### 判断流程

```
                    暂存的变更
                         |
                 单一逻辑目的？
                    /         \
                  是            否
                   |              |
              整体提交     涉及几个领域？
                              /        \
                           2 个       3+ 个
                             |              |
                    拆分为 2 个       制定拆分方案
                    (询问用户)      (展示方案，询问用户)
```

### 领域边界定义

变更跨越领域边界的情况：
1. **不同插件**（如 mp-git 代码 + mj-nlm 代码）
2. **不同关注点**（如插件代码 + CI workflow）
3. **不同 commit 类型**（如新功能 + 重构旧代码）
4. **配置 + 插件**（如 marketplace.json + plugin.json）

### 推荐提交顺序

| 顺序 | 内容 | 原因 |
|------|------|------|
| 1 | 基础设施（CI、scripts、config） | 其他代码可能依赖基础设施变更 |
| 2 | 核心插件代码（feat/fix/refactor） | 主要交付物 |
| 3 | 技能定义和参考文件（SKILL.md） | 描述已完成的功能 |
| 4 | 文档 | 记录已完成的内容 |

### 不拆分的情况

- 插件代码 + 其对应的 SKILL.md（同一逻辑单元）
- plugin.json 变更伴随 marketplace.json 更新（配套操作）
- 单个文档伴随代码变更（次要）
- <5 个文件，<100 行差异，单一 scope

## 常见 Commit Message 错误

| 错误类型 | 错误 | 正确 |
|---------|------|------|
| 大写 type | `Feat(mp-git): ...` | `feat(mp-git): ...` |
| 句号结尾 | `feat(mp-git): 新增功能.` | `feat(mp-git): 新增功能` |
| 缺少空格 | `feat(mp-git):新增功能` | `feat(mp-git): 新增功能` |
| 分支类型作 commit type | `feature(mp-git): ...` | `feat(mp-git): ...` |
| 模糊摘要 | `fix(mp-dev): fix bug` | `fix(mp-dev): 修复校验脚本跳过 -shared 目录的逻辑` |
| 过去时态 | `feat(mp-git): added sync` | `feat(mp-git): add sync` |
| 超过 72 字符 | `feat(mp-git): add marketplace-specific commit scope table with cross-scope split rules and conflict resolution` | `feat(mp-git): add marketplace-specific commit scope table` |
| 使用 mj-system scope | `feat(aec): ...` | `feat(mp-git): ...`（marketplace 使用插件名作 scope） |
