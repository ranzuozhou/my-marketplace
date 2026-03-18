---
name: mp-git-issue
description: >-
  在 my-marketplace 个人插件市场仓库中创建 GitHub Issue，选择模板并填充字段。
  不适用于 mj-system、不适用于服务级开发、不适用于 mj-agentlab-marketplace。
  触发词：创建issue、新建issue、提issue、报bug、新任务，
  create issue, new issue, report bug, file issue, open issue.
  使用 gh CLI 和 .github/ISSUE_TEMPLATE 模板。
---

# MP Git Issue

## Overview

为 my-marketplace 创建 GitHub Issues，使用 5 种 Issue 模板。模板驱动：运行时读取 `.github/ISSUE_TEMPLATE/<type>.md`。

**Workflow position**: optional pre-step before mp-git-branch.

## Prerequisite Check

```bash
gh auth status
```

## Step 1: Identify Issue Type

### Step 1a: Urgency Check
Ask: "Is this a production emergency bug?"
- **Yes** → type = `hotfix`
- **No** → Step 1b

### Step 1b: Choose Regular Type

| Option | Type | Template |
|--------|------|----------|
| 1 | Feature | `feature.md` |
| 2 | Bugfix | `bugfix.md` |
| 3 | Documentation | `documentation.md` |
| 4 | Maintain | `maintain.md` |

## Step 2: Read Issue Template

```bash
cat .github/ISSUE_TEMPLATE/<type>.md
```

## Step 3: Guide Title Input

Show title prefix from template → AskUserQuestion for description → combine.

## Step 4: Guide Body Fields

| Type | Required Fields |
|------|----------------|
| Feature | what, why, acceptance criteria |
| Bugfix | symptom, reproduction, expected vs actual, environment |
| Documentation | change content, change reason, acceptance criteria |
| Maintain | change content, impact assessment, acceptance criteria |
| Hotfix | symptom, impact scope, reproduction, expected vs actual, environment |

Strip template footer (`> **...` blockquote) before submitting.

## Step 5: Preview & Confirm

Options: Submit / Edit / Cancel

## Step 6: Create Issue

```bash
gh issue create \
  --title "<title>" \
  --body-file <tmp-file> \
  --label "<label>"
```

## Step 7: Output & Handoff

```
Issue Created
- URL: https://github.com/ranzuozhou/my-marketplace/issues/<number>
Next Step: use mp-git-branch to create the corresponding branch
```

## Human Intervention Points

| # | Trigger | Behavior |
|---|---------|----------|
| H1 | `gh` not installed | Output install instructions, stop |
| H2 | User cancels | Clean up, stop |
| H3 | `gh issue create` fails | Display error |
| H4 | User selects Hotfix | Reminder: branch from main |

## Detailed Fields → issue-templates-reference.md
