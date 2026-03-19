# CLAUDE.md — flora-ptm Plugin

## Plugin 概述

flora-ptm（Flora Paper-to-Media）是研究报告批量分析与多媒体转化插件，提供 3 个 skill：

| Skill | 命令 | 职责 |
|-------|------|------|
| **digest** | `/flora-ptm:digest` | 导入报告 → 逐篇深挖 → Deep Research 富化 |
| **synthesize** | `/flora-ptm:synthesize` | 跨报告关系分析 → 综述 → 智能分库 |
| **produce** | `/flora-ptm:produce` | 学习路径推荐 → Focus Prompt 设计 → 媒体制作 |

## 工作流: digest → synthesize → produce

典型使用流程按顺序执行三个技能，每个技能产出下一个技能的输入：
1. **digest** — 将原始报告导入 Staging notebook，逐篇分析并用 Deep Research 补充
2. **synthesize** — 发现 Staging notebook，生成跨文献综述，按主题分库到 Target notebooks
3. **produce** — 发现 Target notebooks，设计 Focus Prompt，生成多媒体学习材料

## 状态传递

技能间通过 NLM tag 系统自动发现相关 notebook，展示候选列表让用户确认选择。
- Staging notebook tag: `flora`, `staging`, `{topic}`
- Target notebook tag: `flora`, `target`, `{topic}`, `{subtopic}`

## MCP 依赖

本 plugin 通过 `.mcp.json` 自动注册 `notebooklm-mcp` MCP server（共享 mj-nlm 的 MCP 服务器）。

**前置安装**（一次性）：
```bash
uv tool install notebooklm-mcp-cli --with socksio --force
nlm login
```

认证问题使用 `/mj-nlm:auth` 解决。

## Skill 调用约定

- 所有 skill 遵循 Phase 式工作流（Phase 0 认证检查 → 业务 Phase）
- 认证失败统一引导到 `/mj-nlm:auth`
- 每个关键步骤设有人工判断点（👤），用户确认后才继续
- 共享参考资源位于 `skills/flora-ptm-shared/` 目录
- 典型规模: 5-15 篇报告，最多 3 个 notebook

## Settings

用户可在 `.claude/flora-ptm.local.md` 中自定义偏好（见 README）。

## 文件结构

```
skills/
├── flora-ptm-digest/      # 导入→深挖→富化 + 工作流详情
├── flora-ptm-synthesize/   # 综述→分库 + 分库逻辑详情
├── flora-ptm-produce/      # 提示词→媒体 + 学习路径 + Prompt 模板
└── flora-ptm-shared/       # 共享参考资源（命名规范、分析 Prompt、Prompt 模板）
```
