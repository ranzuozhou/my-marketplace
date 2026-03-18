# Release Checklist Reference

mp-dev:release 技能的发布检查清单参考文件。定义 6 步发布工作流和 scope 行为。

---

## 6 步发布工作流

| 步骤 | 名称 | 说明 |
|------|------|------|
| **Step 1** | 版本确定 | 分析 commit 历史，推荐 semver 版本号 |
| **Step 2** | 版本写入 | 执行 bump-version.ps1 脚本 |
| **Step 3** | CHANGELOG 转换 | [Unreleased] → [x.y.z] - YYYY-MM-DD |
| **Step 4** | Release Commit | 创建版本发布 commit |
| **Step 5** | Release PR | 创建发布 Pull Request |
| **Step 6** | 发布后验证 | 验证版本一致性和 CI 通过 |

---

## Step 1: 版本确定

**分析 commit 历史**：

```bash
git log --oneline $(git merge-base HEAD develop)..HEAD
```

**Semver 推荐规则**：

| Commit 类型 | 版本影响 | 示例 |
|-------------|---------|------|
| `feat` (新功能) | MINOR | 1.0.0 → 1.1.0 |
| `fix` (修复) | PATCH | 1.0.0 → 1.0.1 |
| `BREAKING CHANGE` | MAJOR | 1.0.0 → 2.0.0 |
| `enhance` / `refactor` | PATCH | 1.0.0 → 1.0.1 |
| `docs` / `chore` | 不单独发版 | — |

**多 plugin 变更时**：每个受影响的 plugin 独立推荐版本号。

---

## Step 2: 版本写入

**脚本路径**：`scripts/bump-version.ps1`

**DryRun（预览）**：

```powershell
.\scripts\bump-version.ps1 -From "<current>" -To "<target>" -Scope "<scope>" -DryRun
```

**执行**：

> **Hard Block**：执行写入前必须获得用户明确确认。DryRun 输出会展示将修改的文件和行。

```powershell
.\scripts\bump-version.ps1 -From "<current>" -To "<target>" -Scope "<scope>"
```

**Scope 值**：

| Scope | 影响文件 |
|-------|---------|
| `marketplace`（默认） | `VERSION`, `.claude-plugin/marketplace.json` (metadata.version) |
| `mj-nlm` | `plugins/mj-nlm/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (plugins[mj-nlm].version) |
| `mp-git` | `plugins/mp-git/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (plugins[mp-git].version) |
| `mp-dev` | `plugins/mp-dev/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (plugins[mp-dev].version) |

---

## Step 3: CHANGELOG 转换

将对应层级 CHANGELOG 的 `[Unreleased]` 节内容转换为版本号节。

**仓库层**（scope=marketplace）：

编辑 `CHANGELOG.md`（根目录）

**插件层**（scope=mj-nlm/mp-git/mp-dev）：

编辑 `plugins/<scope>/CHANGELOG.md`

**转换格式**：

```markdown
## [Unreleased]
（保留为空）

## [<version>] - <YYYY-MM-DD>
（原 Unreleased 内容移到这里）
```

详见 `→ ../mp-dev-changelog/changelog-format.md`

---

## Step 4: Release Commit

**Commit 消息格式**：

```
release(<scope>): v<version>

- bump <scope> version to <version>
- convert CHANGELOG [Unreleased] to [<version>]
```

**示例**：

```
release(mp-dev): v1.1.0

- bump mp-dev version to 1.1.0
- convert CHANGELOG [Unreleased] to [1.1.0]
```

**暂存文件**：
- scope=marketplace: `VERSION`, `.claude-plugin/marketplace.json`, `CHANGELOG.md`
- scope=plugin: `plugins/<name>/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `plugins/<name>/CHANGELOG.md`

---

## Step 5: Release PR

**PR 创建**：

使用 GitHub MCP（如可用）或 `gh` CLI 创建 PR。

```bash
gh pr create \
  --title "release(<scope>): v<version>" \
  --body "$(cat <<'EOF'
## Summary
- Bump <scope> version from <old> to <new>
- Convert CHANGELOG [Unreleased] to [<version>]

## Checklist
- [ ] Version numbers consistent (V5 check)
- [ ] CHANGELOG properly formatted
- [ ] CI passes
EOF
)" \
  --base develop
```

**PR 模板选择**：使用 `.github/PULL_REQUEST_TEMPLATE/release.md`

---

## Step 6: 发布后验证

| 检查项 | 命令/方式 | 预期 |
|--------|----------|------|
| 版本一致性 | `mp-dev:validate --scope <plugin>` | V5 PASS |
| CI 通过 | GitHub Actions | 绿色 |
| CHANGELOG 格式 | 阅读 CHANGELOG.md | [version] 节存在 |
| marketplace.json | 检查 version 字段 | 匹配新版本 |

---

## 多 Plugin 发布

当一次发布涉及多个 plugin 时：

1. 逐个确定各 plugin 的版本号
2. 逐个执行 bump-version.ps1（每个 scope 单独运行）
3. 逐个转换 CHANGELOG
4. 合并为一个 release commit（或分开）
5. 创建一个 PR 包含所有变更

**示例**：

```powershell
# 先 DryRun 确认
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-dev" -DryRun
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.0.1" -Scope "mj-nlm" -DryRun

# 确认后执行
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-dev"
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.0.1" -Scope "mj-nlm"
```
