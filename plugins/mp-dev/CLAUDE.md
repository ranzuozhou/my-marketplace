# CLAUDE.md — mp-dev Plugin

## Plugin 概述

mp-dev 是 my-marketplace 个人插件市场仓库的插件开发生命周期 Plugin，提供 6 个 skill + 1 个共享资源目录：

| Skill | 命令 | 职责 |
|-------|------|------|
| **scaffold** | `/mp-dev:mp-dev-scaffold` | 插件脚手架（目录结构 + plugin.json + 元文件 + marketplace.json 注册） |
| **skill-author** | `/mp-dev:mp-dev-skill-author` | SKILL.md 编写辅助（模板、frontmatter 规范、参考文件生成） |
| **validate** | `/mp-dev:mp-dev-validate` | 结构校验（V1-V7 规则，镜像 CI 检查） |
| **test** | `/mp-dev:mp-dev-test` | 测试工作流（3 阶段：plugin-dir 快速迭代 → 本地源切换 → 预发布验证） |
| **changelog** | `/mp-dev:mp-dev-changelog` | CHANGELOG 管理（双层管理、自动检测变更、条目生成） |
| **release** | `/mp-dev:mp-dev-release` | 发布准备（版本号推荐 → bump-version → CHANGELOG 转换 → PR 创建） |

**共享资源**：`skills/mp-dev-shared/` — 交互模式模板（信息收集、范围确认、破坏性确认、结果展示）

## MCP 依赖

本 plugin 无 MCP 依赖。所有功能基于文件操作、Git 命令和 Python 脚本实现。

## Skill 调用约定

- 工作流推荐链路：scaffold → skill-author → validate → test → changelog → release
- 所有 skill 共享 `mp-dev-shared/question-patterns.md` 中的交互模式
- 破坏性操作（文件覆盖、版本写入、源切换）需用户二次确认（Hard Block）
- `--scope` 参数支持限定操作范围到单个 plugin

## 推荐搭配

建议与 `mp-git` 插件一起安装，获得完整的 Git 工作流支持（分支管理、PR 模板、commit 规范）。

## 文件结构

```
skills/
├── mp-dev-scaffold/       # 插件脚手架技能 + plugin-template.md
├── mp-dev-skill-author/   # SKILL.md 编写技能 + skill-template.md
├── mp-dev-validate/       # 结构校验技能 + validation-rules.md + scripts/validate_plugin.py
├── mp-dev-test/           # 测试工作流技能 + test-workflow-reference.md
├── mp-dev-changelog/      # CHANGELOG 管理技能 + changelog-format.md
├── mp-dev-release/        # 发布准备技能 + release-checklist.md
└── mp-dev-shared/         # 共享交互模式模板（question-patterns.md）
```
