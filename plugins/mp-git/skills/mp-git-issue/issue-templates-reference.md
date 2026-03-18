# Issue Templates Reference

## Template Location

All templates: `.github/ISSUE_TEMPLATE/<template>.md`

## feature.md — Field Guide

**When**: New feature, new plugin, new skill, refactor.

| Field | Required | Guidance | Example |
|-------|----------|----------|---------|
| **what** | Yes | One sentence: what to implement | "Add mp-git plugin with 9 marketplace-adapted skills" |
| **why** | Yes | Background or reason, keep it concise | "mj-git is designed for mj-system, marketplace needs its own Git workflow" |
| **acceptance criteria** | Yes | Checklist of completion conditions | "- [ ] 9 skills created\n- [ ] mp-dev-validate passes" |
| **notes** | No | Related plugins, known risks, dependency issues | "Depends on #11. Affects marketplace.json" |

**Title prefix**: `[Feature] `
**Label**: `feature`

**Guidance prompts**:
- what: "Please describe in one sentence what needs to be implemented."
- why: "What is the background or reason for this feature?"
- acceptance criteria: "List the completion criteria (each as a checkbox item)."
- notes: "Any related plugins, known risks, or dependency issues? (optional, press Enter to skip)"

**Complete example**:
```markdown
**what**
Add mp-git plugin with 9 marketplace-adapted Git workflow skills.

**why**
mj-git is designed for mj-system (service-level scopes, Gitee dual-push). Marketplace needs plugin-level scopes and single GitHub push.

**acceptance criteria**
- [ ] 9 skills created (branch/commit/push/pr/review-pr/check-merge/delete/issue/sync)
- [ ] commit-rules.md has 10 marketplace scopes
- [ ] review-checklist.md has D1-D6 plugin structure checks
- [ ] mp-dev-validate passes for mp-git

**notes**
Depends on marketplace.json registration. mp-git and mp-dev should be developed together.
```

---

## bugfix.md — Field Guide

**When**: Bug found during development or testing (not production — use hotfix for production).

| Field | Required | Guidance | Example |
|-------|----------|----------|---------|
| **symptom** | Yes | One sentence: what the user sees | "mp-dev-validate reports false FAIL on plugin.json with valid schema" |
| **reproduction** | Yes | Numbered steps to reproduce | "1. Run /mp-dev:mp-dev-validate\n2. Observe V1 FAIL for mp-git" |
| **expected vs actual** | Yes | Two lines: expected behavior, actual behavior | "Expected: V1 PASS\nActual: V1 FAIL — missing 'license' field" |
| **environment** | Yes | Testing environment + version | "marketplace v1.2.0, Claude Code latest" |

**Title prefix**: `[Bugfix] `
**Label**: `bugfix`

**Guidance prompts**:
- symptom: "Describe the problem in one sentence."
- reproduction: "List the steps to reproduce this bug (numbered list)."
- expected vs actual: "What did you expect to happen, and what actually happened?"
- environment: "Which marketplace version and testing method (--plugin-dir / installed)?"

**Complete example**:
```markdown
**symptom**
mp-dev-validate reports false FAIL on plugin.json V1 check for mp-git.

**reproduction**
1. Run `/mp-dev:mp-dev-validate --scope mp-git`
2. Observe V1 result shows FAIL
3. Manually inspect plugin.json — all 6 fields present

**expected vs actual**
- Expected: V1 PASS — plugin.json has all required fields
- Actual: V1 FAIL — script reports 'license' field missing (but it exists)

**environment**: marketplace v1.2.0, tested via `--plugin-dir`
```

---

## documentation.md — Field Guide

**When**: Pure documentation changes, no code. If docs change alongside code, use the code's branch type instead.

| Field | Required | Guidance | Example |
|-------|----------|----------|---------|
| **change content** | Yes | What docs are being changed and how | "Add contributing guide for plugin development" |
| **change reason** | Yes | Why this update is needed | "New contributors need onboarding documentation" |
| **acceptance criteria** | Yes | Checklist of completion conditions | "- [ ] Guide covers plugin structure\n- [ ] INDEX.md updated" |

**Title prefix**: `[Documentation] `
**Label**: `documentation`

**Complete example**:
```markdown
**change content**
Add contributing guide covering plugin development workflow, testing steps, and PR conventions.

**change reason**
New contributors have no onboarding documentation for marketplace plugin development.

**acceptance criteria**
- [ ] Guide covers plugin structure conventions
- [ ] Testing workflow (3 phases) explained
- [ ] INDEX.md updated with new guide entry
```

---

## maintain.md — Field Guide

**When**: CI/CD, dependencies, tool scripts, config changes. No business logic.

| Field | Required | Guidance | Example |
|-------|----------|----------|---------|
| **change content** | Yes | What infrastructure is being changed | "Add mp-git and mp-dev to bump-version.ps1 -Scope ValidateSet" |
| **impact assessment** | Yes | Scope of impact | "Scope: bump-version.ps1 script. No downtime." |
| **acceptance criteria** | Yes | Checklist of completion conditions | "- [ ] -Scope accepts mp-git/mp-dev\n- [ ] DryRun output correct" |

**Title prefix**: `[Maintain] `
**Label**: `maintain`

**Complete example**:
```markdown
**change content**
Add mp-git and mp-dev to bump-version.ps1 -Scope ValidateSet parameter.

**impact assessment**
- Scope: bump-version.ps1 script only
- No downtime, no CI changes

**acceptance criteria**
- [ ] `-Scope "mp-git"` accepted without error
- [ ] DryRun output shows correct target files
- [ ] Existing scopes (marketplace/mj-doc/mj-git/mj-n8n/mj-ops) still work
```

---

## hotfix.md — Field Guide

**When**: Production emergency bug. Branch from `main`, PR targets `main`.

> **Key difference from bugfix**: hotfix is for production issues. It creates a branch from `main` (not `develop`), and the PR target is also `main`. After merge, the fix must be synced back to `develop`.

| Field | Required | Guidance | Example |
|-------|----------|----------|---------|
| **symptom** | Yes | One sentence: production problem | "mp-git-push skill crashes when pushing to empty remote" |
| **impact scope** | Yes | Affected users/features/plugins | "All marketplace users using mp-git-push on new repos" |
| **reproduction** | Yes | Numbered steps to reproduce | "1. Create new repo\n2. Run /mp-git:mp-git-push\n3. Script errors" |
| **expected vs actual** | Yes | Expected behavior vs actual behavior | "Expected: Push succeeds\nActual: Error: remote has no branch" |
| **environment** | Yes | Production environment + version | "marketplace v1.2.0" |

**Title prefix**: `[Hotfix] `
**Label**: `hotfix`

**Complete example**:
```markdown
**symptom**
mp-git-push skill crashes when pushing to a newly created empty remote repository.

**impact scope**
All marketplace users using mp-git-push on repos with no existing remote branch.

**reproduction**
1. Create a new GitHub repository (empty, no initial commit)
2. Run `/mp-git:mp-git-push`
3. Skill errors with "remote has no branch 'develop'"

**expected vs actual**
- Expected: Push succeeds, upstream tracking set
- Actual: Error: "remote has no branch 'develop'" — skill assumes remote branch exists

**environment**: marketplace v1.2.0
```

---

## Quick `gh` Command Reference

| Type | Command |
|------|---------|
| Feature | `gh issue create --title "[Feature] ..." --body-file <tmp> --label feature` |
| Bugfix | `gh issue create --title "[Bugfix] ..." --body-file <tmp> --label bugfix` |
| Documentation | `gh issue create --title "[Documentation] ..." --body-file <tmp> --label documentation` |
| Maintain | `gh issue create --title "[Maintain] ..." --body-file <tmp> --label maintain` |
| Hotfix | `gh issue create --title "[Hotfix] ..." --body-file <tmp> --label hotfix` |
