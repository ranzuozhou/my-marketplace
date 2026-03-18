# PR Templates Reference

## Template Location

All templates: `.github/PULL_REQUEST_TEMPLATE/<template>.md`

## Branch → Template → Target 映射表

| 分支类型 | PR 模板 | 目标分支 |
|---------|---------|---------|
| `feature/*` | `feature.md` | `develop` |
| `bugfix/*` | `bugfix.md` | `develop` |
| `documentation/*` | `documentation.md` | `develop` |
| `maintain/*` | `maintain.md` | `develop` |
| `hotfix/*` | `hotfix.md` | `main` |
| `develop→main` | `release.md` | `main` |

> **Version bump 触发规则**：版本号变更仅在 Release PR（`develop→main`）时触发。feature/bugfix 等分支的 PR 不执行 version bump。

---

## feature.md — Field Guide

**When**: `feature/*` → develop. New features, new plugins, refactors.

| Field | Guidance | Example |
|-------|----------|---------|
| 变更摘要 | One paragraph: what changed and why | "新增 mp-git 插件，提供适配 marketplace 的 Git 工作流技能" |
| 影响范围 | List affected plugins, modules, file counts | "mp-git 插件（20 新文件）、marketplace.json（1 修改）" |
| 审核要点 | Tell reviewer what to focus on | "重点检查 scope 映射表和 review checklist 的完整性" |
| 自检结果 | Tick all checklist items | incl. "CHANGELOG.md [Unreleased] 区块已更新" |

**Commit types allowed**: `feat`, `perf`, `refactor`, `test`, `docs`

**Complete example**:
```markdown
## 变更摘要
新增 mp-git 插件，为 marketplace 仓库提供完全适配的 Git 工作流。
包含 9 个 skill（branch/commit/push/pr/review-pr/check-merge/delete/issue/sync），
scope 映射表和 review checklist 已针对插件级结构重写。

## 影响范围
- mp-git 插件：20 新文件
- marketplace.json：新增 mp-git 条目

## 审核要点
重点检查 commit-rules.md 的 scope 映射表和 review-checklist.md 的 D1-D6 检查项

## 自检结果
- [x] mp-dev-validate 校验通过
- [x] 无硬编码
- [x] 无残留调试代码
- [x] Commit message 符合规范
- [x] CHANGELOG.md [Unreleased] 区块已更新
```

---

## bugfix.md — Field Guide

**When**: `bugfix/*` → develop. Bugs found during development (not production).

| Field | Guidance |
|-------|----------|
| Bug 描述 | One sentence: what the user sees (external symptom) |
| 根因分析 | Root cause (not symptom) — helps reviewer assess if fix is correct |
| 修复方案 | What was changed and how |
| 影响范围 | Affected plugins/modules |
| 自检结果 | incl. "CHANGELOG.md [Unreleased] 区块已更新" |

**Commit types allowed**: `fix`, `test`, `docs`

---

## documentation.md — Field Guide

**When**: `documentation/*` → develop. Pure doc changes, no code.

> If docs change alongside code, use the code's branch type (feature/maintain) instead.

| Field | Guidance |
|-------|----------|
| 文档变更内容 | List changed files with a brief description of each |
| 变更原因 | Why this update is needed (gap, outdated content, standard change) |
| 自检结果 | File naming correct, INDEX.md updated |

**Commit types allowed**: `docs` only

**Lightest template** — no plugin validation required.

---

## maintain.md — Field Guide

**When**: `maintain/*` → develop. CI/CD, dependencies, tool scripts, config.

| Field | Guidance |
|-------|----------|
| 变更摘要 | What infrastructure was changed and why |
| 影响评估 | Which pipelines or tools are affected |
| 审核要点 | CI compatibility, script correctness, no sensitive info exposed |
| 自检结果 | Config syntax validated, no sensitive info exposed |

**Commit types allowed**: `infra`, `docs`

---

## hotfix.md — Field Guide

**When**: `hotfix/*` → **main**. Production emergency bug.

> Different from bugfix: hotfix targets main, not develop. Rollback plan is mandatory.

| Field | Guidance |
|-------|----------|
| 事故描述 | What users see in production (external symptom) |
| 影响范围 | Affected users, features, or plugins |
| 根因分析 | Root cause |
| 修复方案 | What was changed |
| **回滚预案** | **MANDATORY**: how to revert if this fix breaks something else |
| 自检结果 | Confirm: only `fix` commits; confirm: plan to sync back to develop after merge |

**Rollback plan example**:
```markdown
## 回滚预案
如修复引入新问题，执行以下步骤：
1. `git revert <merge-commit-sha>` 回滚合并
2. `git push origin main`
3. release.yml 会自动处理 tag/Release（如已触发）
```

**After hotfix PR merges**:
1. Tag a patch version on main: `git tag -a v1.1.1 -m "Hotfix: ..."` + push
2. Merge main → develop to sync the fix

---

## release.md — Field Guide

**When**: develop → **main**. Version release.

| Field | Guidance |
|-------|----------|
| Release 标题 | Format: `Release vX.Y.Z — <theme>` e.g. "Release v1.2.0 — mp-git 插件" |
| Highlights | Core changes extracted from `CHANGELOG.md [Unreleased]` |
| 审核要点 | Checklist: CHANGELOG complete, version numbers consistent, no debug code |
| Details | Link to `CHANGELOG.md` for full release notes |

**Version bump before Release PR**:
```powershell
# Dry run first
.\scripts\bump-version.ps1 -From "1.1.0" -To "1.2.0" -DryRun

# Execute
.\scripts\bump-version.ps1 -From "1.1.0" -To "1.2.0"

# Also bump plugins if changed:
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git" -DryRun
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git"
```

**Command** (non-interactive, e.g. Claude Code):
```bash
gh pr create \
  --base main \
  --head develop \
  --title "Release v1.2.0" \
  --body-file <tmp-file> \
  --reviewer "<reviewer-username>"
```

---

## Quick `gh` Command Reference

> **Note**: `--template` only works in interactive mode. In non-interactive mode (Claude Code, CI), read the template, fill fields, write to temp file, and use `--body-file`.

| Branch | Template | Command (non-interactive) |
|--------|----------|--------------------------|
| `feature/12-add-mp-git` | `feature.md` | `gh pr create --base develop --title "..." --body-file <tmp> --reviewer "<user>"` |
| `bugfix/25-fix-validate` | `bugfix.md` | `gh pr create --base develop --title "..." --body-file <tmp> --reviewer "<user>"` |
| `documentation/15-update-docs` | `documentation.md` | `gh pr create --base develop --title "..." --body-file <tmp> --reviewer "<user>"` |
| `maintain/8-update-ci` | `maintain.md` | `gh pr create --base develop --title "..." --body-file <tmp> --reviewer "<user>"` |
| `hotfix/20-push-crash` | `hotfix.md` | `gh pr create --base main --title "..." --body-file <tmp> --reviewer "<user>"` |
| Release | `release.md` | `gh pr create --base main --head develop --title "Release vX.Y.Z" --body-file <tmp> --reviewer "<user>"` |

## GitHub Web Alternative

To use a template via browser URL:
```
https://github.com/ranzuozhou/my-marketplace/compare/develop...<branch>?template=feature.md
```

Replace `feature.md` with the appropriate template name.
