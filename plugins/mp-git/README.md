# mp-git

Marketplace Git 工作流技能家族 — 提供适配个人插件仓库的分支、提交、推送、PR、Review、同步和清理能力。

## Skills

| Skill | 命令 | 触发场景 |
|-------|------|---------|
| branch | `/mp-git:mp-git-branch` | 创建分支、Worktree 设置 |
| commit | `/mp-git:mp-git-commit` | 规范化提交 |
| push | `/mp-git:mp-git-push` | 推送代码、pre-push 检查 |
| pr | `/mp-git:mp-git-pr` | 创建 Pull Request |
| review-pr | `/mp-git:mp-git-review-pr` | PR 插件结构评审 |
| check-merge | `/mp-git:mp-git-check-merge` | 检查 PR 合并就绪 |
| delete | `/mp-git:mp-git-delete` | 删除分支、清理 Worktree |
| issue | `/mp-git:mp-git-issue` | 创建 GitHub Issue |
| sync | `/mp-git:mp-git-sync` | 同步基线分支 |

## 安装

```bash
# 推荐以 project scope 安装（仅在 marketplace 仓库中生效）
/plugin marketplace add ranzuozhou/my-marketplace
/plugin install mp-git@my-marketplace
```

## 前置条件

- Claude Code 最新版本
- `GITHUB_PERSONAL_ACCESS_TOKEN` 系统环境变量

## 许可证

MIT
