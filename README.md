# My Marketplace

![Version](https://img.shields.io/badge/version-1.3.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![CI](https://github.com/ranzuozhou/my-marketplace/actions/workflows/ci.yml/badge.svg)](https://github.com/ranzuozhou/my-marketplace/actions/workflows/ci.yml)

个人 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 插件市场 — 集中管理和分发知识管理、Git 工作流、插件开发等领域的自动化技能。

4 个插件，23 个技能，覆盖从知识库操作到插件发布的完整开发工作流。

## 插件目录

| Plugin | 描述 | Skills | Version | 前置条件 |
|--------|------|--------|---------|----------|
| [**mj-nlm**](plugins/mj-nlm/README.md) | NotebookLM 知识库：认证、创建、管理、查询、Studio 制品 | 5 | 1.0.0 | NotebookLM MCP CLI + Google 认证 |
| [**mp-git**](plugins/mp-git/README.md) | Git 工作流：分支、提交、推送、PR、Review、同步、清理 | 10 | 1.1.0 | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| [**mp-dev**](plugins/mp-dev/README.md) | 插件开发：脚手架、SKILL 编写、校验、测试、CHANGELOG、发布 | 6 | 1.0.0 | — |
| [**flora-ptm**](plugins/flora-ptm/README.md) | 研究报告分析与多媒体转化：导入消化、综述分库、媒体制作 | 3 | 1.0.0 | NotebookLM MCP CLI + Google 认证 |

## 安装

> 前提：已安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)。

### 1. 注册 Marketplace

```
/plugin marketplace add ranzuozhou/my-marketplace
```

### 2. 安装插件

Claude Code 插件支持三种安装级别：

| 级别 | 命令 flag | 配置文件 | 共享 | 适用场景 |
|------|-----------|----------|------|----------|
| 用户级 | （默认） | `~/.claude/settings.json` | 否 | 个人常用插件，跨项目生效 |
| 项目级 | `--scope project` | `.claude/settings.json` | 是（提交到 git） | 团队共享，新成员自动获取 |
| 本地级 | `--scope local` | `.claude/settings.local.json` | 否（gitignore） | 仅本项目、仅本人，不影响团队 |

#### 用户级安装（默认，所有项目可用）

```
/plugin install mj-nlm@my-marketplace
/plugin install mp-git@my-marketplace
/plugin install mp-dev@my-marketplace
/plugin install flora-ptm@my-marketplace
```

#### 项目级安装（提交到 git，团队共享）

```
/plugin install mj-nlm@my-marketplace --scope project
/plugin install mp-git@my-marketplace --scope project
/plugin install mp-dev@my-marketplace --scope project
/plugin install flora-ptm@my-marketplace --scope project
```

#### 本地级安装（gitignore，仅本人本项目）

```
/plugin install mj-nlm@my-marketplace --scope local
/plugin install mp-git@my-marketplace --scope local
/plugin install mp-dev@my-marketplace --scope local
/plugin install flora-ptm@my-marketplace --scope local
```

### 3. 使用示例

安装后在 Claude Code 中直接调用技能：

```
/mj-nlm:mj-nlm-build          # 创建 NotebookLM 知识库
/mp-git:mp-git-branch          # 按规范创建新分支
/mp-git:mp-git-commit          # 暂存并提交代码
/mp-dev:mp-dev-scaffold        # 脚手架生成新插件
/flora-ptm:digest              # 批量导入分析研究报告
```

## 更新

```
/plugin update mj-nlm@my-marketplace
```

## 文档

- 完整文档索引：[docs/INDEX.md](docs/INDEX.md)
- 贡献指引与发布流程：[CONTRIBUTING.md](docs/CONTRIBUTING.md)
- 变更日志：[CHANGELOG.md](CHANGELOG.md)

## 贡献

欢迎贡献！本项目采用 **bare repo + worktree** 开发模型，详见 [CONTRIBUTING.md](docs/CONTRIBUTING.md)。

## 许可证

MIT
