# Push FAQ & Troubleshooting

## Pre-Push Checklist

推送前执行以下 7 项检查：

| # | 检查项 | 通过标准 | 失败处理 |
|---|--------|---------|---------|
| 1 | Commit message 格式 | `type(scope): summary` 格式正确 | 修正后重新提交 |
| 2 | Type/branch discipline | commit type 在分支允许范围内 | 参考 branch-rules.md 矩阵 |
| 3 | CHANGELOG 更新 | `feat`/`fix` commit 对应 CHANGELOG 已更新 | 补充 CHANGELOG 条目 |
| 4 | 工作目录干净 | `git status --porcelain` 无输出 | 暂存或 stash 未提交文件 |
| 5 | 分支名合规 | 匹配 `feature/`、`bugfix/`、`documentation/`、`maintain/`、`hotfix/` | 重命名分支 |
| 6 | 基础分支同步 | 当前分支不落后 base branch | `git fetch && git merge origin/develop` |
| 7 | 推送执行 + 远程确认 | `git push -u origin <branch>` 成功 | 排查推送错误 |

---

## Q1: Found a missing file after pushing — what to do?

Add it as a new commit and push again:

```bash
git add <missing file>
git commit -m "<type>(<scope>): 补充遗漏的文件"
git push
```

Prevention: always run `git status --short` before pushing.

## Q2: Commit message has a typo after pushing — what to do?

Only if you're the sole user of this branch:

```bash
git commit --amend -m "<type>(<scope>): corrected summary"
git push --force-with-lease   # safer than --force
```

> **Warning**: `--force-with-lease` is only safe on personal dev branches. NEVER use on `main` or `develop`.

## Q3: "no upstream branch" error on first push

Use `-u` to set upstream tracking:

```bash
git push -u origin <branch>
```

## Q4: Pushed to the wrong worktree directory

1. `git worktree list` — find which directory has which branch
2. Navigate to the correct directory: `cd ../<correct-dir>`
3. Push from the correct directory

Prevention: always run `git branch --show-current` before pushing.

## Q5: Setting up pre-push hook (optional automation)

Install a hook that warns when uncommitted files are found before pushing.

Create `.git/hooks/pre-push` with:

```bash
#!/bin/bash
# .git/hooks/pre-push — pre-push check for uncommitted files

UNCOMMITTED=$(git status --porcelain)

if [ -n "$UNCOMMITTED" ]; then
    echo ""
    echo "======================================"
    echo "  Warning: 发现未提交的修改"
    echo "======================================"
    echo ""
    git status --short
    echo ""
    echo "请确认这些文件是否应纳入提交。"
    echo "继续推送？(y/N)"
    read -r answer < /dev/tty
    if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
        echo "推送已取消。"
        exit 1
    fi
fi
```

Make it executable:

```bash
chmod +x .git/hooks/pre-push
```

**Windows notes**:
- Git for Windows uses MSYS2 — bash syntax works
- Hook path: `<repo-root>/.git/hooks/pre-push` (all worktrees share the main repo's hooks)
- Hook doesn't run with `git push --no-verify`

## Q6: Merge conflict during base sync

```bash
# Sync produces conflicts:
git fetch origin && git merge origin/develop
# CONFLICT (content): Merge conflict in <file>

# Resolve:
git status                  # see conflict files
# Edit files to resolve conflicts (look for <<<, ===, >>> markers)
git add .                   # mark resolved
git commit -m "merge: 合并 develop 最新内容，解决冲突"

# Too complex to resolve? Abort and get help:
git merge --abort
```
