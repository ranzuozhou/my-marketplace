> **[GUIDE] My Marketplace 项目概览**
> 面向新成员和贡献者，介绍插件市场的架构、组成和开发环境。

## 1. 项目定位

My Marketplace 是个人 **Claude Code 插件市场**，集中管理和分发个人开发的 Claude Code 插件。

- **仓库**：[ranzuozhou/my-marketplace](https://github.com/ranzuozhou/my-marketplace)
- **许可证**：MIT
- **当前版本**：见 `VERSION` 文件（权威源）

## 2. 架构概览

> **物理目录**：本项目使用 **bare repo worktree 模式**（参考 §6.2 克隆仓库）。下图为逻辑结构，物理上每个分支对应一个 worktree 目录（如 `my-marketplace/develop/`、`my-marketplace/feature/xxx/`）。

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # 市场元数据（整体版本 + 插件注册表）
├── VERSION                       # 市场整体版本号（单一权威源）
├── CHANGELOG.md                  # 市场级变更日志
├── plugins/                      # 3 个插件
│   ├── mj-nlm/                   # NotebookLM 知识库
│   ├── mp-git/                   # Git 工作流
│   └── mp-dev/                   # 插件开发工具链
├── scripts/                      # 基础设施脚本
│   ├── bump-version.ps1          # 版本升级
│   └── clone-bare.ps1            # Bare repo 克隆
├── .github/
│   ├── workflows/                # CI/CD
│   │   ├── ci.yml                # PR 结构校验
│   │   └── release.yml           # 自动发布
│   └── PULL_REQUEST_TEMPLATE/    # 6 种 PR 模板
└── docs/
    └── CONTRIBUTING.md           # 贡献指南
```

## 3. 插件目录

| Plugin | 描述 | Skills | Version | MCP 依赖 |
|--------|------|--------|---------|----------|
| **mj-nlm** | NotebookLM 知识库：认证、创建、管理、查询、Studio 制品 | 5（含 1 共享资源） | 1.0.0 | notebooklm-mcp |
| **mp-git** | Git 工作流：分支、提交、推送、PR、Review、合并检查、同步、清理 | 9 | 1.0.0 | github, serena |
| **mp-dev** | 插件开发：脚手架、SKILL 编写、校验、测试、CHANGELOG、发布 | 6 | 1.0.0 | 无 |

### 3.1 插件标准结构

每个插件遵循统一结构：

```
<plugin>/
├── .claude-plugin/
│   └── plugin.json       # 插件元数据（name, version, author, skills）
├── .mcp.json             # MCP 服务器定义（可选）
├── CLAUDE.md             # 插件概述（Claude Code 上下文注入）
├── README.md             # 用户安装和使用指南
├── CHANGELOG.md          # 插件级变更日志
└── skills/
    └── <skill-name>/
        ├── SKILL.md      # Skill 行为规范（frontmatter + workflow）
        └── *.md          # 参考文档（规则、模板、清单）
```

### 3.2 技能工作流链

- **mp-git**：`issue` → `branch` → `commit` → `push` → `pr` → `review-pr` → `check-merge` → `sync` → `delete`
- **mp-dev**：`scaffold` → `skill-author` → `validate` → `test` → `changelog` → `release`
- **mj-nlm**：`auth` → `build` → `manage` → `query` → `studio`

## 4. 版本管理体系

采用 **双层独立版本管理**：

| 层级 | 权威源 | 升级时机 |
|------|--------|----------|
| Marketplace 整体 | `VERSION` 文件 | 新增/删除插件、跨插件变更 |
| 各 Plugin 独立 | `plugins/<name>/.claude-plugin/plugin.json` | 插件内部变更 |

两者独立升级，互不影响。详见 [版本管理指南](<./[GUIDE]_Version_Management.md>)。

## 5. CI/CD 体系

### 5.1 CI — 结构校验（ci.yml）

触发条件：feature/bugfix/documentation/maintain/hotfix 分支 push + PR to develop/main

| 检查项 | 内容 |
|--------|------|
| plugin.json 校验 | name, description, version, author, license, skills 字段完整 |
| marketplace.json 完整性 | 每个插件条目有对应目录 |
| SKILL.md 前置元数据 | YAML frontmatter 含 name + description |
| 目录结构 | 每个插件含 .claude-plugin/plugin.json, CLAUDE.md, README.md, skills/ |
| 版本一致性 | VERSION ↔ marketplace.json；plugin.json ↔ marketplace.json |
| CHANGELOG 存在性 | 根级 + 各插件级 |

### 5.2 Release — 自动发布（release.yml）

触发条件：VERSION 文件变更推送到 main

流程：读取版本 → 检查 tag 幂等 → 创建 git tag → 从 CHANGELOG 提取发布说明 → 创建 GitHub Release

## 6. 开发环境搭建

### 6.1 安装插件（使用者）

```bash
# 注册 marketplace
/plugin marketplace add ranzuozhou/my-marketplace

# 安装所需 plugin
/plugin install mp-git@my-marketplace
```

### 6.2 克隆仓库（开发者）

> [!NOTE]
> 首次克隆需要使用独立引导脚本 `my-marketplace-clone-bare.ps1`，
> 该脚本位于项目目录外（如 `D:\workspace\...\projects\`）。
> 仓库内的 `scripts/clone-bare.ps1` 是同一脚本的归档副本。

```powershell
# 新成员入职（创建 develop worktree）
powershell -ExecutionPolicy Bypass -File .\my-marketplace-clone-bare.ps1 `
    -RepoUrl https://github.com/ranzuozhou/my-marketplace

# 获取特定分支（如需直接进入某开发分支）
powershell -ExecutionPolicy Bypass -File .\my-marketplace-clone-bare.ps1 `
    -RepoUrl https://github.com/ranzuozhou/my-marketplace `
    -Branches "feature/12-add-new-skill"

# 同时创建多个 worktree
powershell -ExecutionPolicy Bypass -File .\my-marketplace-clone-bare.ps1 `
    -RepoUrl https://github.com/ranzuozhou/my-marketplace `
    -Branches "develop,main"

# 增量添加新分支（项目已存在时自动跳过初始化）
powershell -ExecutionPolicy Bypass -File .\my-marketplace-clone-bare.ps1 `
    -RepoUrl https://github.com/ranzuozhou/my-marketplace `
    -Branches "hotfix/fix-ci-validation"
```

### 6.3 分支策略

| 分支类型 | 来源 | 目标 |
|----------|------|------|
| `main` | — | 生产就绪（受保护） |
| `develop` | — | 集成主线（受保护） |
| `feature/*` | develop | develop |
| `bugfix/*` | develop | develop |
| `documentation/*` | develop | develop |
| `maintain/*` | develop | develop |
| `hotfix/*` | main | main（合并后同步 develop） |

## 7. 相关文档

- [版本管理指南](<./[GUIDE]_Version_Management.md>) — 版本管理详细指南
- [发布操作手册](<./[RUNBOOK]_Release_Operations.md>) — 发布操作手册
- [CONTRIBUTING.md](./CONTRIBUTING.md) — 贡献指南
