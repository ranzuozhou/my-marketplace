# My Marketplace

个人插件市场 — 集中管理和分发个人 Claude Code 插件。

## Project Structure

- `plugins/` — 3 个插件：mj-nlm, mp-git, mp-dev
- `scripts/` — 基础设施脚本（bump-version, clone-bare）
- `.claude-plugin/marketplace.json` — 市场元数据（版本 + 插件注册表）
- `VERSION` — 市场整体版本号（权威源）
- `docs/` — 项目文档（见 [INDEX.md](docs/INDEX.md)）

## Key Conventions

- **Bare repo worktree model**: 每个分支对应独立 worktree 目录，不使用 `git checkout`
- **Dual-layer versioning**: marketplace 整体版本（`VERSION`）和各插件版本（`plugin.json`）独立管理
- **Commit format**: `<type>(<scope>): <summary>` — types: feat, fix, perf, refactor, test, docs, infra
- **Branch types**: feature/, bugfix/, documentation/, maintain/, hotfix/

## Plugin Structure

每个插件遵循统一结构：

```
<plugin>/
├── .claude-plugin/plugin.json   # 插件元数据
├── .mcp.json                    # MCP 服务器定义（可选）
├── CLAUDE.md                    # 插件概述
├── README.md                    # 用户指南
├── CHANGELOG.md                 # 变更日志
└── skills/                      # 技能目录
```

## Documentation

完整文档索引：[docs/INDEX.md](docs/INDEX.md)
