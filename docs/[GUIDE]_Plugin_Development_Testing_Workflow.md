> **[GUIDE] Plugin 开发测试工作流指南**
> 覆盖从 marketplace feature 分支开发到发布的完整插件测试流程，解决缓存冲突问题。

## TL;DR

- **核心问题**：目标项目中项目级安装了 marketplace 插件（有缓存），在 marketplace 仓库修改代码后**不会自动生效**
- **解决方案**：`claude --plugin-dir` 覆盖缓存 + `/reload-plugins` 热重载
- **三阶段**：快速开发（`--plugin-dir`）→ 集成验证（本地 marketplace install）→ 发布前验证（GitHub develop install）

---

## 目录

1. [1 问题：为什么需要这个工作流](#1-问题为什么需要这个工作流)
2. [2 前置条件](#2-前置条件)
3. [3 三阶段工作流总览](#3-三阶段工作流总览)
4. [4 阶段 1：快速开发迭代](#4-阶段-1快速开发迭代)
5. [5 阶段 2：集成验证](#5-阶段-2集成验证)
6. [6 阶段 3：发布前验证](#6-阶段-3发布前验证)
7. [7 常见问题](#7-常见问题)
8. [8 快速参考卡片](#8-快速参考卡片)

---

## 1 问题：为什么需要这个工作流

### 1.1 缓存机制

当通过 `/plugin install` 安装插件时，Claude Code 将插件**拷贝**到缓存目录：

```
~/.claude/plugins/cache/my-marketplace/{plugin}/{version}/
```

这是一份**静态副本**，不会跟踪源仓库的变更。

### 1.2 加载链路

```
正常加载（缓存）：
  settings.json (enabledPlugins: "mp-git@my-marketplace")
    → installed_plugins.json (installPath: cache/.../mp-git/1.0.0/)
      → 缓存目录（静态拷贝）
        → Claude Code 加载技能 ← 始终是安装时的旧版本

--plugin-dir 覆盖：
  claude --plugin-dir ../../my-marketplace/feature/xxx/plugins/mp-git
    → 直接读取本地目录（实时、无缓存）（路径需包含 worktree 段）
      → 同名插件时覆盖缓存版本
        → Claude Code 加载技能 ← 最新代码
```

### 1.3 实际影响

| 操作 | 结果 |
|------|------|
| 在 marketplace 仓库修改 SKILL.md | 目标项目中**不生效**（缓存未变） |
| 在 marketplace 仓库新增技能 | 目标项目中**看不到**（缓存未变） |
| 修改 .mcp.json | 目标项目中 MCP server **不变**（缓存未变） |
| 执行 `/plugin update` | 从 GitHub **已发布版本**更新，不含未发布的 feature 分支代码 |

---

## 2 前置条件

### 2.1 目录结构

目标项目和 marketplace 仓库需在同级目录下，且**都使用 bare repo worktree 模式**：

```
D:\workspace\10-software-project\projects\
├── <target-project>/
│   ├── .bare/                          ← bare repo（隐藏）
│   ├── develop/                        ← 主工作 worktree
│   └── maintain/test-xxx/              ← 测试用 worktree（可选，用于隔离测试）
│
└── my-marketplace/
    ├── .bare/                          ← bare repo（隐藏）
    ├── main/                           ← main worktree（发布用）
    └── feature/add-skill-xxx/          ← feature worktree（开发用）
        └── plugins/
            ├── mj-nlm/
            ├── mp-git/
            └── mp-dev/
```

> **关键理解**：bare repo worktree 模式下，每个分支对应一个**独立的目录**。切换分支 = `cd` 到对应 worktree 目录，**不使用 `git checkout`**。

### 2.2 分支状态

- **marketplace 仓库**：已创建 feature worktree 并 `cd` 到该目录（如 `my-marketplace/feature/add-skill-xxx/`）
- **目标项目**：在 develop worktree 或任意需要测试的 worktree

> bare repo worktree 模式下不使用 `git checkout` 切换分支。导航到不同分支 = `cd` 到对应 worktree 目录。

### 2.3 验证目录可达

```bash
# 从目标项目 develop 验证相对路径（注意需包含 worktree 名称）
ls ../../my-marketplace/feature/add-skill-xxx/plugins/

# 通用格式：../../my-marketplace/<worktree>/plugins/
# 示例：
#   ../../my-marketplace/feature/add-new-skill/plugins/
#   ../../my-marketplace/main/plugins/
```

---

## 3 三阶段工作流总览

```
阶段 1                    阶段 2                      阶段 3
快速开发迭代               集成验证                     发布前验证
(--plugin-dir)            (本地 marketplace)           (GitHub develop)
     │                         │                           │
     │  修改 → 热重载           │  源切换 → install          │  合并 → update
     │  秒级生效               │  模拟真实安装               │  验证发布版本
     │                         │                           │
     ▼                         ▼                           ▼
  单技能验证行为            多插件协作 + 安装流程         最终确认 → 发布
```

| 维度 | 阶段 1 | 阶段 2 | 阶段 3 |
|------|--------|--------|--------|
| **适用场景** | 修改 SKILL.md、调试技能逻辑 | 验证安装流程、多插件协作 | 发布前最终确认 |
| **缓存影响** | 绕过缓存，直接加载本地 | 替换缓存为本地版本 | 从 GitHub 更新缓存 |
| **操作复杂度** | 低（1 条启动命令） | 中（需要源切换+恢复） | 低（标准 update 流程） |
| **迭代速度** | 秒级（`/reload-plugins`） | 分钟级（需重新 install） | 分钟级（需推送到 GitHub） |
| **使用频率** | 高（每次修改） | 低（开发完成后 1 次） | 低（发布前 1 次） |

---

## 4 阶段 1：快速开发迭代

> **核心机制**：`--plugin-dir` 绕过缓存，直接加载本地目录。同名插件时本地版本**覆盖**已安装版本。

### 4.1 适用场景

- 修改现有 SKILL.md 的触发描述、指令内容、流程逻辑
- 新增技能、命令、Agent
- 调整 plugin.json、.mcp.json
- 调整插件目录结构

### 4.2 单插件测试

```bash
# Step 1: 确认 marketplace feature worktree 已创建
# （bare repo worktree 模式不用 git checkout，直接 cd 到 worktree 目录）
cd D:/workspace/10-software-project/projects/my-marketplace/feature/add-skill-xxx
# 如尚未创建 worktree，从 main worktree 中执行：
# cd ../main && git worktree add ../feature/add-skill-xxx -b feature/add-skill-xxx main

# Step 2: 从目标项目 worktree 启动 Claude Code，指定待测插件（路径含 worktree 段）
cd D:/workspace/10-software-project/projects/<target-project>/develop
claude --plugin-dir ../../my-marketplace/feature/add-skill-xxx/plugins/mp-git
```

> **PowerShell 用户**：`--plugin-dir` 必须使用**绝对路径**并用双引号包裹：
> ```powershell
> claude --plugin-dir "D:\workspace\10-software-project\projects\my-marketplace\feature\add-skill-xxx\plugins\mp-git"
> ```

启动后，`mp-git` 插件加载的是本地 feature 分支的代码，而不是缓存中的旧版本。其他未指定的插件（如 mj-nlm、mp-dev）仍从缓存加载。

### 4.3 多插件同时测试

**Bash / Git Bash**：
```bash
# 同时测试 mp-git 和 mj-nlm（路径含 worktree 段）
claude \
  --plugin-dir ../../my-marketplace/feature/add-skill-xxx/plugins/mp-git \
  --plugin-dir ../../my-marketplace/feature/add-skill-xxx/plugins/mj-nlm
```

**PowerShell**（反引号 `` ` `` 续行，绝对路径）：
```powershell
claude `
  --plugin-dir "D:\workspace\10-software-project\projects\my-marketplace\feature\add-skill-xxx\plugins\mp-git" `
  --plugin-dir "D:\workspace\10-software-project\projects\my-marketplace\feature\add-skill-xxx\plugins\mj-nlm"
```

### 4.4 测试 → 修改 → 热重载循环

```
  ┌─────────────────────────────────────┐
  │                                     │
  ▼                                     │
手动触发技能         修改 SKILL.md      │
  │  (如 /mp-git:mp-git-commit)   │     │
  │                               │     │
  ▼                               ▼     │
验证行为 ──── 不符合预期 ──→ 在 marketplace │
  │                          仓库中修改代码 │
  │                               │     │
  符合预期                        ▼     │
  │                     /reload-plugins ─┘
  ▼
完成（提交到 feature 分支）
```

**热重载命令**：在 Claude Code 中执行 `/reload-plugins`，会重新加载所有 `--plugin-dir` 指定的插件，无需退出重启。

重载范围包括：
- Skills（SKILL.md）
- Commands
- Agents
- Hooks
- MCP servers
- LSP servers

### 4.5 注意事项

1. **优先级规则**：`--plugin-dir` 加载的插件 > 已安装的同名插件。不影响全局安装状态。
2. **Session 范围**：覆盖仅在当前 Claude Code session 生效。退出后恢复使用缓存版本。
3. **MCP server**：`--plugin-dir` 加载的插件中的 `.mcp.json` 也会被加载。确保 `.env` 中的环境变量（如 `GITHUB_PERSONAL_ACCESS_TOKEN`）在目标项目中可用。
4. **相对路径**：`--plugin-dir` 的路径相对于**启动目录**（即 `cd` 到的目录），不是项目根目录。
5. **Windows PowerShell 路径**：`--plugin-dir` 在 PowerShell 中不能使用相对路径（`../../`），必须使用**绝对路径**并用双引号包裹（如 `"D:\...\plugins\mp-git"`）。Bash/Git Bash 中相对路径正常工作。

---

## 5 阶段 2：集成验证

> **核心机制**：将本地 marketplace 目录注册为源，通过 `/plugin install` 安装到缓存，模拟真实安装流程。

### 5.1 何时需要阶段 2

- 验证 `plugin.json` 的 metadata 是否正确（name、version、skills 路径）
- 验证技能的自然语言触发（不显式调用，看 `description` 的触发准确率）
- 验证多插件协作场景（如 mp-git 技能链）
- 验证 marketplace.json 中的插件注册是否正确

### 5.2 完整源切换流程

> **重要**：本地 marketplace 和 GitHub marketplace 使用**相同的名称** `my-marketplace`。注册本地源会**覆盖** `known_marketplaces.json` 中的 GitHub 源条目。测试完毕后**必须恢复**。

#### Step 1: 记录当前状态（备份参考）

```bash
# 查看当前注册的 marketplace（在 Claude Code 中执行）
/plugin marketplace list

# 或直接查看配置文件
cat ~/.claude/plugins/known_marketplaces.json
```

记录当前 `my-marketplace` 的 source 信息：
```json
{
  "my-marketplace": {
    "source": {
      "source": "github",
      "repo": "ranzuozhou/my-marketplace"
    }
  }
}
```

#### Step 2: 卸载已安装的目标插件

```bash
/plugin uninstall mp-git@my-marketplace
# 如需测试多个插件，逐个卸载
/plugin uninstall mj-nlm@my-marketplace
```

#### Step 3: 移除 GitHub marketplace 源

```bash
/plugin marketplace remove my-marketplace
```

#### Step 4: 注册本地 marketplace 源

```bash
# 路径指向 marketplace 的某个 worktree（含 .claude-plugin/marketplace.json）
# bare repo 根目录没有工作文件，必须指向具体 worktree
/plugin marketplace add ../../my-marketplace/feature/add-skill-xxx
```

#### Step 5: 从本地源安装插件

```bash
/plugin install mp-git@my-marketplace
/plugin install mj-nlm@my-marketplace
```

#### Step 6: 测试

- 手动触发技能验证行为
- 测试自然语言触发准确率
- 验证 MCP server 启动

### 5.3 恢复 GitHub 源（必做！）

> **测试完毕后务必执行以下步骤**，否则后续 `/plugin update` 将尝试从本地路径更新，可能导致异常。

#### Step 1: 卸载本地安装的插件

```bash
/plugin uninstall mp-git@my-marketplace
/plugin uninstall mj-nlm@my-marketplace
# ... 其他已安装的插件
```

#### Step 2: 移除本地 marketplace 源

```bash
/plugin marketplace remove my-marketplace
```

#### Step 3: 重新注册 GitHub 源

```bash
/plugin marketplace add ranzuozhou/my-marketplace
```

#### Step 4: 重新安装插件

```bash
/plugin install mj-nlm@my-marketplace
/plugin install mp-git@my-marketplace
/plugin install mp-dev@my-marketplace
```

#### Step 5: 验证恢复状态

```bash
# 确认 marketplace 源指向 GitHub
/plugin marketplace list

# 确认插件已安装
/plugin list
```

### 5.4 验证要点清单

- [ ] 技能显式调用正常（`/mp-git:mp-git-commit`）
- [ ] 技能自然语言触发正常（「提交代码」自动匹配 mp-git-commit）
- [ ] MCP server 正常启动（无连接错误）
- [ ] 新增技能在 `/plugin list` 中可见
- [ ] plugin.json 中的 metadata 正确

---

## 6 阶段 3：发布前验证

> **核心机制**：marketplace feature 分支合并到 develop 后，从 GitHub 更新安装，验证最终发布版本。

### 6.1 前置条件

- marketplace feature 分支已合并到 develop 并推送到 GitHub
- marketplace 源指向 GitHub（阶段 2 后已恢复，或未执行阶段 2）

### 6.2 操作步骤

```bash
# Step 1: 更新 marketplace 到最新 develop 分支
/plugin marketplace update my-marketplace

# Step 2: 更新已安装插件
/plugin update mp-git@my-marketplace
# 或更新全部
/plugin update --all

# Step 3: 验证
# 手动触发关键技能，确认行为符合预期
```

### 6.3 发布流程

验证通过后，在 marketplace 仓库中执行发布：

```bash
# ── 准备阶段（在 develop worktree）──

# 1. 确定版本号（semver: patch/minor/major）
#    - 新增 Skill/Plugin → minor（1.0.0 → 1.1.0）
#    - Bug fix → patch（1.0.0 → 1.0.1）
#    - 破坏性变更 → major（1.0.0 → 2.0.0）

# 2. Bump 版本号（使用 bump-version.ps1）
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -DryRun  # 预览
.\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0"           # 执行
#    更新文件：VERSION、marketplace.json (metadata.version)
#    如有插件变更，也 bump 插件：-Scope "mp-git" -From "1.0.0" -To "1.1.0"
#    更新文件：plugin.json (version)、marketplace.json (plugins[].version)

# 3. 更新 CHANGELOG.md（根级 + 插件级）
#    将 [Unreleased] 内容转为 [x.y.z] - YYYY-MM-DD 正式版本节

# 4. 提交发布变更
git add VERSION .claude-plugin/marketplace.json CHANGELOG.md
git add plugins/mp-git/.claude-plugin/plugin.json plugins/mp-git/CHANGELOG.md  # 如有插件变更
git commit -m "infra(marketplace): release v1.1.0"
git push origin develop

# ── 合并阶段 ──

# 5. 创建 Release PR（develop → main）
gh pr create --base main --head develop --title "Release v1.1.0" --body-file <filled-template>

# 6. CI 通过 → Review → 合并
gh pr checks <pr-number>
# 合并后 release.yml 自动：创建 tag → 提取 CHANGELOG → 创建 GitHub Release

# ── 验证阶段 ──

# 7. 验证发布
git fetch --tags && git tag -l "v1.1.0"
gh release view v1.1.0

# ── 下游更新 ──

# 8. 在目标项目中更新插件到发布版本
/plugin marketplace update my-marketplace
/plugin update --all
```

> **详细操作**：完整的 bump 工具使用和 CHANGELOG 格式参考 [版本管理指南](<./[GUIDE]_Version_Management.md>)；Release PR 模板和检查清单参考 [发布操作手册](<./[RUNBOOK]_Release_Operations.md>)。

### 6.4 发布后清理

发布完成后，清理开发和测试过程中创建的 worktree 和临时分支：

```bash
# ── marketplace 仓库：清理 feature worktree ──
cd D:/workspace/10-software-project/projects/my-marketplace/main
git worktree remove ../feature/add-skill-xxx
git branch -d feature/add-skill-xxx
# 可选：删除远程分支（PR 合并后 GitHub 通常已自动删除）
git push origin --delete feature/add-skill-xxx
```

> **注意**：删除 worktree 前确保所有变更已提交并推送。`git worktree remove` 会检查是否有未提交的变更，如有则拒绝删除（需加 `--force` 强制删除）。

---

## 7 常见问题

### Q1: `--plugin-dir` 加载的插件和缓存版本同时存在？

不会。`--plugin-dir` 指定的同名插件**完全覆盖**缓存版本。Claude Code 在该 session 中只会加载本地版本。未指定的插件仍从缓存加载。

### Q2: 忘记恢复 GitHub 源会怎样？

`known_marketplaces.json` 中 `my-marketplace` 的 `installLocation` 会指向本地路径。后续 `/plugin update` 会尝试从本地路径拉取更新，而不是 GitHub：

- 如果本地路径仍可达 → 更新为本地版本（可能不是你期望的）
- 如果本地路径已失效 → 更新失败报错

**修复方法**：执行 §5.3 的恢复步骤。

### Q3: `/reload-plugins` 没生效？

- `/reload-plugins` 仅对 `--plugin-dir` 加载的插件有实时效果
- 对缓存安装的插件，需要重新 `/plugin install` 才能更新缓存
- 确认修改的文件已保存（特别注意 IDE 的自动保存设置）

### Q4: MCP server 在 `--plugin-dir` 模式下不启动？

检查：
1. 插件目录中的 `.mcp.json` 是否存在且格式正确
2. `.env` 中的环境变量（如 `GITHUB_PERSONAL_ACCESS_TOKEN`）是否在目标项目中可用
3. MCP server 的可执行文件路径是否正确（注意 `${CLAUDE_PLUGIN_ROOT}` 占位符）

### Q5: project scope 插件在新 worktree 中不可用？

`installed_plugins.json` 中 project scope 插件绑定了具体的 `projectPath`。新建 worktree 后需要在该 worktree 中重新安装：

```bash
cd <target-project>/feature/xxx
# 重新启动 Claude Code，插件应自动可用（因为 settings.json 中声明了 enabledPlugins）
# 如不可用，手动安装：
/plugin install mp-git@my-marketplace
```

### Q6: 如何知道当前加载的是缓存版本还是本地版本？

- 启动 Claude Code 时，终端输出会显示加载的插件来源
- 如果使用了 `--plugin-dir`，输出中会标注该插件来自本地目录
- 也可以通过 `/plugin list` 查看插件信息

---

## 8 快速参考卡片

### 三阶段命令速查

| 阶段 | 命令 | 说明 |
|------|------|------|
| **阶段 1** | `claude --plugin-dir ../../my-marketplace/<worktree>/plugins/{plugin}` | 启动时指定本地插件（Bash） |
| | PowerShell: `claude --plugin-dir "D:\...\my-marketplace\<worktree>\plugins\{plugin}"` | PowerShell 需绝对路径 |
| | `/reload-plugins` | 修改后热重载 |
| **阶段 2** | `/plugin uninstall {plugin}@my-marketplace` | 卸载缓存版本 |
| | `/plugin marketplace remove my-marketplace` | 移除 GitHub 源 |
| | `/plugin marketplace add ../../my-marketplace/<worktree>` | 注册本地源（指向 worktree） |
| | `/plugin install {plugin}@my-marketplace` | 从本地源安装 |
| **恢复** | `/plugin marketplace remove my-marketplace` | 移除本地源 |
| | `/plugin marketplace add ranzuozhou/my-marketplace` | 恢复 GitHub 源 |
| | `/plugin install {plugin}@my-marketplace` | 重新安装 |
| **阶段 3** | `/plugin marketplace update my-marketplace` | 从 GitHub 更新 marketplace |
| | `/plugin update --all` | 更新所有插件 |

### 源切换完整命令序列

**切换到本地源**（5 步）：
```bash
# 1. 卸载目标插件
/plugin uninstall mp-git@my-marketplace

# 2. 移除 GitHub 源
/plugin marketplace remove my-marketplace

# 3. 注册本地源（路径指向 worktree，不是 bare repo 根目录）
/plugin marketplace add ../../my-marketplace/feature/add-skill-xxx

# 4. 安装
/plugin install mp-git@my-marketplace

# 5. 测试
/mp-git:mp-git-commit
```

**恢复 GitHub 源**（5 步）：
```bash
# 1. 卸载本地插件
/plugin uninstall mp-git@my-marketplace

# 2. 移除本地源
/plugin marketplace remove my-marketplace

# 3. 注册 GitHub 源
/plugin marketplace add ranzuozhou/my-marketplace

# 4. 重新安装
/plugin install mp-git@my-marketplace

# 5. 验证
/plugin marketplace list
```

---

> **关联文档**：[项目概览](<./[GUIDE]_Marketplace_Project_Overview.md>)、[版本管理](<./[GUIDE]_Version_Management.md>)、[发布操作](<./[RUNBOOK]_Release_Operations.md>)
