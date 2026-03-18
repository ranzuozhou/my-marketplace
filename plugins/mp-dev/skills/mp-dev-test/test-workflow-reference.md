# Test Workflow Reference

mp-dev:test 技能的测试工作流参考文件。定义 3 阶段测试流程、平台命令和验证清单。

---

## 三阶段测试概览

| 阶段 | 名称 | 用途 | 风险 |
|------|------|------|------|
| **Phase 1** | `--plugin-dir` 快速迭代 | 开发中的快速验证 | 低 |
| **Phase 2** | 本地源切换 | 模拟真实安装环境 | 中（需修改 Claude 配置） |
| **Phase 3** | 预发布 GitHub 更新 | 发布前最终验证 | 低 |

---

## Phase 1: --plugin-dir 快速迭代

**适用场景**：插件开发过程中，快速验证 SKILL.md 加载和基本功能。

**命令格式**：

| 平台 | 命令 |
|------|------|
| **Bash** | `claude --plugin-dir "D:/workspace/10-software-project/projects/my-marketplace/plugins/<plugin-name>"` |
| **PowerShell** | `claude --plugin-dir "D:\workspace\10-software-project\projects\my-marketplace\plugins\<plugin-name>"` |

**多插件同时加载**：

```bash
claude \
  --plugin-dir "D:/workspace/10-software-project/projects/my-marketplace/plugins/mj-nlm" \
  --plugin-dir "D:/workspace/10-software-project/projects/my-marketplace/plugins/mp-git" \
  --plugin-dir "D:/workspace/10-software-project/projects/my-marketplace/plugins/mp-dev"
```

**验证清单**：

- [ ] `/plugin` 列表中出现目标 plugin
- [ ] 各 skill 的 `/` 命令可触发
- [ ] 自然语言触发正常工作
- [ ] 支撑文件可被引用
- [ ] H-point 在正确条件下触发

**提示**：修改 SKILL.md 后需执行 `/reload-plugins` 重新加载，无需重启 Claude。

---

## Phase 2: 本地源切换

**适用场景**：需要验证通过 marketplace 安装后的完整体验，模拟真实安装环境。

### 切换步骤（5 步）

> **Hard Block**：执行前必须获得用户明确确认。此操作会修改 Claude Code 的 plugin 源配置。

**Step 1: 备份当前配置**

```bash
# Bash
cp ~/.claude/plugins/sources.json ~/.claude/plugins/sources.json.bak

# PowerShell
Copy-Item "$env:USERPROFILE\.claude\plugins\sources.json" "$env:USERPROFILE\.claude\plugins\sources.json.bak"
```

**Step 2: 查看当前源**

```
/plugin marketplace list
```

**Step 3: 切换到本地源**

```
/plugin marketplace add-local "D:/workspace/10-software-project/projects/my-marketplace"
```

**Step 4: 安装插件**

```
/plugin install <plugin-name>@my-marketplace
```

**Step 5: 验证安装**

```
/plugin
/<plugin-name>:<skill-name>
```

### 验证清单

- [ ] `/plugin` 列表中出现目标 plugin（来源标记为 my-marketplace）
- [ ] 所有 skill 均可通过 `/` 命令调用
- [ ] MCP 服务正常注册（如有 .mcp.json）
- [ ] 自然语言触发正常
- [ ] 交叉 skill 引用正常（如 validate 引用 shared）

### 恢复步骤（5 步）

> 测试完成后必须恢复配置，避免影响日常使用。

**Step 1: 卸载测试插件**

```
/plugin uninstall <plugin-name>@my-marketplace
```

**Step 2: 移除本地源**

```
/plugin marketplace remove my-marketplace
```

**Step 3: 恢复备份**

```bash
# Bash
cp ~/.claude/plugins/sources.json.bak ~/.claude/plugins/sources.json

# PowerShell
Copy-Item "$env:USERPROFILE\.claude\plugins\sources.json.bak" "$env:USERPROFILE\.claude\plugins\sources.json"
```

**Step 4: 重新加载**

```
/reload-plugins
```

**Step 5: 确认恢复**

```
/plugin marketplace list
/plugin
```

### 安全提醒

- 操作对象为 Claude Code 的 plugin 配置文件，非系统级文件
- 备份是必须步骤，不可跳过
- 测试完成后必须恢复，否则可能影响其他 marketplace 插件
- 本地源地址为 `ranzuozhou/my-marketplace` GitHub 仓库的本地 clone

---

## Phase 3: 预发布 GitHub 更新

**适用场景**：版本发布前，确认 GitHub 上的最新代码在远端 marketplace 安装后正常工作。

### 更新步骤

**Step 1: 推送最新代码**

```bash
git push origin develop
```

**Step 2: 更新 marketplace 注册**

```
/plugin marketplace update my-marketplace
```

**Step 3: 更新插件**

```
/plugin update <plugin-name>@my-marketplace
```

**Step 4: 验证关键 skill**

逐一验证每个 skill 的核心功能：

| 验证项 | 命令 | 预期结果 |
|--------|------|---------|
| Skill 列表 | `/plugin` | 所有 skill 出现 |
| 脚手架 | `/mp-dev:scaffold` | 正确响应 |
| 校验 | `/mp-dev:validate` | 输出校验报告 |
| 自然语言 | "校验插件结构" | 触发 validate |

---

## 平台命令速查

| 操作 | Bash | PowerShell |
|------|------|------------|
| 复制文件 | `cp src dst` | `Copy-Item src dst` |
| 路径分隔 | `/` | `\` |
| 环境变量 | `$HOME` | `$env:USERPROFILE` |
| 多行命令 | `\` 续行 | `` ` `` 续行 |
| 插件目录 | `~/.claude/plugins/` | `$env:USERPROFILE\.claude\plugins\` |
