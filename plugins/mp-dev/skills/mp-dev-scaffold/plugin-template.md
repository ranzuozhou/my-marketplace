# Plugin Template Reference

mp-dev:scaffold 技能的模板参考文件。定义插件标准目录结构、默认值和各元文件骨架。

---

## 标准目录结构

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # 插件元数据（必须）
├── skills/
│   ├── <plugin-name>-<skill>/
│   │   ├── SKILL.md         # 技能定义文件（必须）
│   │   └── *.md             # 支撑参考文件（可选）
│   └── <plugin-name>-shared/
│       └── *.md             # 共享参考资源（可选）
├── CLAUDE.md                # Plugin 概述（必须）
├── README.md                # 用户指南（必须）
└── CHANGELOG.md             # 变更记录（必须）
```

---

## 默认值表

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `version` | `1.0.0` | 初始版本号 |
| `author.name` | `ranzuozhou` | 插件作者 |
| `license` | `MIT` | 开源协议 |
| `repository` | `https://github.com/ranzuozhou/my-marketplace` | 仓库地址 |
| `skills` | `./skills/` | 技能目录路径 |

---

## plugin.json Schema

```json
{
  "name": "<plugin-name>",
  "description": "<中文描述 — 50-150 字符>",
  "version": "1.0.0",
  "author": { "name": "ranzuozhou" },
  "repository": "https://github.com/ranzuozhou/my-marketplace",
  "license": "MIT",
  "keywords": ["<keyword1>", "<keyword2>", "..."],
  "skills": "./skills/"
}
```

**必填字段**（CI V1 检查）：`name`, `description`, `version`, `author`, `license`, `skills`

---

## CLAUDE.md 骨架模板

```markdown
# CLAUDE.md — <plugin-name> Plugin

## Plugin 概述

<plugin-name> 是 my-marketplace 个人插件市场仓库的 <功能描述> Plugin，提供 N 个 skill：

| Skill | 命令 | 职责 |
|-------|------|------|
| **<skill-1>** | `/<plugin-name>:<skill-1>` | <职责描述> |
| ... | ... | ... |

## MCP 依赖

<说明 MCP 依赖情况，无依赖则注明"本 plugin 无 MCP 依赖">

## Skill 调用约定

- <约定 1>
- <约定 2>

## 文件结构

（目录树）
```

---

## README.md 骨架模板

```markdown
# <plugin-name> — <英文标题> for Claude Code

<一句话中文描述>

## 功能

| 命令 | 说明 |
|------|------|
| `/<plugin-name>:<skill>` | <说明> |

## 前置条件

- **Claude Code** v2.1+
- <其他依赖>

## 安装方式

### 通过 Marketplace 安装（推荐）

/plugin marketplace add ranzuozhou/my-marketplace
/plugin install <plugin-name>@my-marketplace

### 本地开发安装

claude --plugin-dir "<my-marketplace-path>/plugins/<plugin-name>"

## 许可

MIT License
```

---

## CHANGELOG.md 骨架模板

```markdown
# Changelog

All notable changes to the <plugin-name> plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - <YYYY-MM-DD>

### Added
- 初始发布：N 个 Skill（<skill-list>）
```

---

## marketplace.json 条目模板

在根目录 `.claude-plugin/marketplace.json` 的 `plugins` 数组中添加：

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<中文描述>",
  "version": "1.0.0",
  "author": { "name": "ranzuozhou" },
  "category": "<productivity|development|...>",
  "keywords": ["<keyword1>", "<keyword2>"],
  "license": "MIT"
}
```

---

## 注意事项

- 插件名使用 `mp-` 前缀（marketplace plugin）或 `mj-` 前缀（MJ System plugin）
- 当前仓库已有插件：mj-nlm, mp-git, mp-dev
- 安装方式统一使用 `@my-marketplace` 标识
- my-marketplace 仓库路径：`D:/workspace/10-software-project/projects/my-marketplace`
