# CLAUDE.md — mp-git Plugin

## Plugin 概述

mp-git 是 my-marketplace 个人插件市场的 Git 工作流技能家族 Plugin，提供 9 个 skill：

| Skill | 命令 | 职责 |
|-------|------|------|
| **branch** | `/mp-git:mp-git-branch` | 创建分支、命名规范、Worktree 设置 |
| **commit** | `/mp-git:mp-git-commit` | 规范化提交（scope 推断、message 格式） |
| **push** | `/mp-git:mp-git-push` | 推送代码（7 项 pre-push 检查） |
| **pr** | `/mp-git:mp-git-pr` | 创建 Pull Request（模板选择、版本号） |
| **review-pr** | `/mp-git:mp-git-review-pr` | PR 评审（插件结构检查） |
| **check-merge** | `/mp-git:mp-git-check-merge` | 检查 PR 合并就绪状态 |
| **delete** | `/mp-git:mp-git-delete` | 删除分支、清理 Worktree |
| **issue** | `/mp-git:mp-git-issue` | 创建 GitHub Issue（模板选择、字段填充） |
| **sync** | `/mp-git:mp-git-sync` | 同步分支（develop/main 合入当前分支） |

## MCP 依赖

本 plugin 通过 `.mcp.json` 自动注册 2 个 MCP server：

- **github**: GitHub API 访问（需 `GITHUB_PERSONAL_ACCESS_TOKEN` 系统环境变量）
- **serena**: 代码分析工具（使用 `--project-from-cwd`，无需额外配置）

## Skill 调用约定

- 完整工作流链：`issue` → `branch` → `commit` → `push` → `pr` → `review-pr` → `check-merge` → `delete`
- 破坏性操作（force push、branch delete）需用户二次确认
- `commit` skill 根据变更文件路径自动推断 scope（插件级 scope）
- 单路 GitHub 推送（无 Gitee）

## 文件结构

```
skills/
├── mp-git-branch/        # 分支技能 + branch-rules.md
├── mp-git-commit/        # 提交技能 + commit-rules.md
├── mp-git-push/          # 推送技能 + push-faq.md
├── mp-git-pr/            # PR 技能 + pr-templates-reference.md
├── mp-git-review-pr/     # PR 评审技能 + review-checklist.md + comment-template.md
├── mp-git-check-merge/   # 合并检查技能
├── mp-git-delete/        # 删除技能
├── mp-git-issue/         # Issue 技能 + issue-templates-reference.md
└── mp-git-sync/          # 同步技能
```
