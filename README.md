# My Marketplace

个人插件市场，为 Claude Code 提供知识管理、Git 工作流、插件开发等专业插件。

## 安装 Marketplace

在 Claude Code 中执行：

```
/plugin marketplace add ranzuozhou/my-marketplace
```

## 可用插件

| 插件 | 版本 | 说明 |
|------|------|------|
| **[mj-nlm](plugins/mj-nlm/)** | 1.0.0 | NotebookLM 知识库完整操作：认证、创建、管理、查询、Studio 制品生成 |
| **[mp-git](plugins/mp-git/)** | 1.0.0 | Marketplace Git 工作流：分支、提交、推送、PR、Review、同步、清理（9 skills） |
| **[mp-dev](plugins/mp-dev/)** | 1.0.0 | 插件开发生命周期：脚手架、SKILL.md 编写、校验、测试、CHANGELOG、发布（6 skills） |

## 安装插件

```bash
# 知识管理
/plugin install mj-nlm@my-marketplace

# Git 工作流（推荐 project scope 安装）
/plugin install mp-git@my-marketplace

# 插件开发工具链（推荐与 mp-git 一起安装）
/plugin install mp-dev@my-marketplace
```

## 前置条件

- **Claude Code** 最新版本
- **mj-nlm** 需要：NotebookLM MCP CLI (`uv tool install notebooklm-mcp-cli --with socksio --force`) + Google 认证 (`nlm login`)
- **mp-git** 需要：`GITHUB_PERSONAL_ACCESS_TOKEN` 系统环境变量

## 文档

完整文档索引：[docs/INDEX.md](docs/INDEX.md)

## 许可

MIT License
