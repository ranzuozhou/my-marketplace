# CLAUDE.md — mj-nlm Plugin

## Plugin 概述

mj-nlm 是 MJ System 的 NotebookLM 技能家族 Plugin，提供 5 个 skill：

| Skill | 命令 | 职责 |
|-------|------|------|
| **auth** | `/mj-nlm:auth` | NLM 认证生命周期（登录、刷新、切换、排障） |
| **build** | `/mj-nlm:build` | 知识库创建（扫描→导入→打标签） |
| **manage** | `/mj-nlm:manage` | 知识库 CRUD + 分享 |
| **query** | `/mj-nlm:query` | 知识问答（单 notebook / 跨 notebook / Deep Research） |
| **studio** | `/mj-nlm:studio` | Studio 制品生成 + 下载（9 种类型） |

## MCP 依赖

本 plugin 通过 `.mcp.json` 自动注册 `notebooklm-mcp` MCP server。

**前置安装**（一次性）：
```bash
uv tool install notebooklm-mcp-cli --with socksio --force
nlm login
```

## Skill 调用约定

- 所有 skill 遵循 Phase 式工作流（Phase 0 认证检查 → 业务 Phase）
- 认证失败统一引导到 `/mj-nlm:auth`
- 破坏性操作（delete）需用户二次确认（`confirm=True`）
- 共享参考资源位于 `skills/mj-nlm-shared/` 目录

## 文件结构

```
skills/
├── mj-nlm-auth/       # 认证技能 + troubleshooting 手册
├── mj-nlm-build/      # 知识库创建技能
├── mj-nlm-manage/     # 生命周期管理技能
├── mj-nlm-query/      # 知识问答技能
├── mj-nlm-studio/     # Studio 制品技能
└── mj-nlm-shared/     # 共享参考资源（命名规范、材料分类、制品类型、Prompt 模板）
```
