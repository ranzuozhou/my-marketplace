---
name: mp-git-commit
description: >-
  在 my-marketplace 个人插件市场仓库中暂存文件并创建符合规范的 Git 提交。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
  触发词：提交代码、暂存文件、commit message、提交格式、拆分提交、准备提交、提交规范，
  git add, git commit, stage files, commit message, split commits, prepare commit.
  执行 type(scope) summary 格式校验和 branch-type 纪律检查。
---

# MP Git Commit

## Overview

暂存文件并创建符合项目规范的 Git 提交。6 步 Pre-Commit 工作流覆盖文件筛选、暂存策略、commit message 格式校验、type/branch 纪律、拆分指导。衔接 `mp-git-branch`（创建分支）与 `mp-git-push`（推送）之间的缺口。

## 前置条件

- 在 my-marketplace worktree 目录内执行
- 当前分支为临时分支（feature/bugfix/documentation/maintain/hotfix），不在 `main` 或 `develop` 上直接提交

## 快速开始（交互模式）

### 信息充足性判断

| 已知信息 | 行动 |
|---------|------|
| 用户说「提交」但未说明提交什么 | 运行 `git status --short`，展示修改列表，询问：「以下是当前修改，全部提交还是选择部分文件？」 |
| 有修改文件，但不确定变更性质 | 询问：「这次修改是新功能、bug 修复、重构、文档更新、还是基础设施维护？」 |
| 变更性质明确，但用户未提供 scope | 从修改的文件路径推断 scope（见 Step 3），不追问 |
| 变更性质 + 文件均明确 | 直接生成 commit 命令 |

---

## Pre-Commit Workflow (6 steps)

### Step 1 — Verify Working Location

```bash
git branch --show-current
# 必须返回分支名。若为 main 或 develop → STOP (H5)

git worktree list
```

### Step 2 — Review Changes & File Selection

```bash
git status --short
git diff
git diff --cached
```

**文件排除规则**：

| 模式 | 原因 | 发现后行为 |
|------|------|----------|
| `.env` | 含密钥/凭据 | **H1**: 硬性阻断，不暂存 |
| `*.pem`, `*.key`, `*.p12` | 私钥/证书 | **H1**: 硬性阻断 |
| 文件 > 10 MB | 大文件不宜纳入 Git | **H2**: 询问用户 |
| `__pycache__/`, `*.pyc`, `.venv/` | 运行时文件 | 静默跳过 |
| `.claude/settings.local.json` | 个人配置 | 静默跳过 |

**暂存策略**：

```bash
# 推荐：按文件名逐个暂存
git add plugins/mp-git/skills/mp-git-commit/SKILL.md

# 可接受：按目录暂存
git add plugins/mp-git/skills/mp-git-commit/

# 避免：git add -A 或 git add .
```

### Step 3 — Compose Commit Message

**格式**：`<type>(<scope>): <summary>`

**Scope 推导**：

| 修改路径模式 | Scope |
|-------------|-------|
| `.claude-plugin/`、`VERSION`、根级文件 | `marketplace` |
| `plugins/mp-git/**` | `mp-git` |
| `plugins/mp-dev/**` | `mp-dev` |
| `plugins/mj-nlm/**` | `mj-nlm` |
| `scripts/**` | `scripts` |
| `.github/**` | `ci` |
| `docs/**` | `docs` |
| 多领域无主导 | 省略 scope |

**根级文件归属**：`.gitignore`、根 `CLAUDE.md`、根 `README.md`、`VERSION`、`.claude-plugin/*` → `marketplace`

### Step 4 — Enforce Type/Branch Discipline

| 分支类型 | 允许的 Commit 类型 |
|---------|-------------------|
| `feature/*` | `feat`, `perf`, `refactor`, `test`, `docs` |
| `bugfix/*` | `fix`, `test`, `docs` |
| `documentation/*` | `docs` |
| `maintain/*` | `infra`, `docs` |
| `hotfix/*` | `fix` |

**若不匹配** → 触发 H3。

### Step 5 — Evaluate Split Necessity

**拆分信号**：

| 信号 | 示例 | 动作 |
|------|------|------|
| 暂存文件跨 2+ 不相关插件 | mp-git + mj-nlm | 按插件拆分 |
| 代码 + 文档涉及不同主题 | 插件代码 + CI 配置 | 分开提交 |
| 混合 feat + refactor | 新 skill + 重构旧代码 | 按类型拆分 |
| 差异 >300 行跨 5+ 文件 | 大型重构 | 按逻辑单元拆分 |

**不应拆分**：插件代码 + 其 SKILL.md；plugin.json + marketplace.json 配套更新；<5 文件 <100 行单一 scope。

**跨 Scope 拆分规则（Soft ask）**：跨插件变更**建议**拆分，不强制阻断。

### Step 6 — Execute Commit

```bash
git diff --cached --stat
git branch --show-current
git commit -m "<type>(<scope>): <summary>"
git log --oneline -1
git status --short
```

---

## 人工介入场景（STOP & ASK）

| # | 触发条件 | 技能行为 |
|---|---------|---------|
| **H1** | `.env`、凭据文件、私钥文件在暂存区 | 硬性阻断：展示文件名，警告含敏感信息，执行 `git reset HEAD <file>` |
| **H2** | 大文件（>10 MB）在暂存区 | 展示文件名和大小，询问是否确认提交 |
| **H3** | Commit type 与 branch type 不匹配 | 展示允许列表，提供：(1) 修改 type (2) 确认例外并继续 |
| **H4** | 暂存区为空但用户要求提交 | 告知暂存区为空，展示 `git status --short` |
| **H5** | 当前分支为 `main` 或 `develop` | 硬性阻断：拒绝提交，告知切换到工作分支 |
| **H6** | Commit message 不符合格式规范 | 展示格式要求，提供修正建议 |
| **H7** | 检测到可拆分的大变更 | 建议拆分方案，询问是否拆分 |

> **H1** 和 **H5** 是硬性阻断。其他场景允许用户覆盖。

---

## Handoff to mp-git-push

```
提交完成
下一步：使用 mp-git-push 执行 pre-push 检查。
  已验证项：commit message 格式、type/branch 纪律
  待检查项：CHANGELOG 更新、工作目录清洁、base branch 同步、推送
```

## 示例

### 示例 1：常规 feature 提交

```bash
# 当前在 feature/add-mp-git-plugin worktree
git branch --show-current  # → feature/add-mp-git-plugin ✓
git status --short
# M  plugins/mp-git/skills/mp-git-commit/SKILL.md
# M  plugins/mp-git/skills/mp-git-commit/commit-rules.md

# type=feat, branch=feature/* → 允许 ✓, scope=mp-git
git add plugins/mp-git/skills/mp-git-commit/
git commit -m "feat(mp-git): add commit skill with marketplace scope table"
```

### 示例 2：跨 scope 拆分

```bash
# 当前在 feature/add-dev-tools
git status --short
# M  plugins/mp-git/CLAUDE.md
# M  plugins/mp-dev/CLAUDE.md
# M  .claude-plugin/marketplace.json

# 检测到跨 scope（mp-git + mp-dev + marketplace），建议拆分
git add plugins/mp-git/CLAUDE.md
git commit -m "docs(mp-git): update plugin overview"

git add plugins/mp-dev/CLAUDE.md
git commit -m "docs(mp-dev): update plugin overview"

git add .claude-plugin/marketplace.json
git commit -m "infra(marketplace): register mp-git and mp-dev plugins"
```

## Commit Rules Reference → commit-rules.md

完整 type 定义、scope 推导表、文件排除模式、拆分决策流程图见 `commit-rules.md`。
