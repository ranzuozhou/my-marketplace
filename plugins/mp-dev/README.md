# mp-dev — Plugin Development Toolkit for Claude Code

my-marketplace 个人插件市场仓库的插件开发生命周期工具包，覆盖从脚手架到发布的完整开发链路。

## 功能

| 命令 | 说明 |
|------|------|
| `/mp-dev:scaffold` | 创建插件脚手架（目录结构、plugin.json、CLAUDE.md、README.md、CHANGELOG.md、marketplace.json 注册） |
| `/mp-dev:skill-author` | 编写 SKILL.md（模板引导、frontmatter 规范、参考文件生成） |
| `/mp-dev:validate` | 结构校验（V1-V7 规则，镜像 CI 检查，支持 --scope 参数） |
| `/mp-dev:test` | 3 阶段测试工作流（plugin-dir 快速迭代 → 本地源切换 → 预发布验证） |
| `/mp-dev:changelog` | CHANGELOG 管理（双层管理、变更检测、条目生成、发布转换） |
| `/mp-dev:release` | 发布准备（semver 推荐 → bump-version → CHANGELOG 转换 → release PR） |

## 前置条件

- **Claude Code** v2.1+
- **Python 3.10+**（用于 validate 脚本）
- **Git**（用于 changelog 变更检测和 release 工作流）
- **PowerShell**（用于 bump-version.ps1 脚本）

## 安装方式

### 通过 Marketplace 安装（推荐）

```
/plugin marketplace add ranzuozhou/my-marketplace
/plugin install mp-dev@my-marketplace
```

### 本地开发安装

```bash
claude --plugin-dir "D:\workspace\10-software-project\projects\my-marketplace\plugins\mp-dev"
```

## 验证安装

```
/plugin                    # 确认 mp-dev 出现在列表
/mp-dev:scaffold           # 测试 skill 加载
/mp-dev:validate           # 运行结构校验
```

## 自然语言触发

除了斜杠命令，也支持自然语言触发：

- "创建一个新插件" → `/mp-dev:scaffold`
- "帮我写 SKILL.md" → `/mp-dev:skill-author`
- "校验插件结构" → `/mp-dev:validate`
- "测试插件" → `/mp-dev:test`
- "更新 CHANGELOG" → `/mp-dev:changelog`
- "准备发布" → `/mp-dev:release`

## 工作流链路

推荐开发流程：

```
scaffold → skill-author → validate → test → changelog → release
```

1. `/mp-dev:scaffold` 创建插件骨架
2. `/mp-dev:skill-author` 编写各 skill 的 SKILL.md
3. `/mp-dev:validate` 校验结构是否符合规范
4. `/mp-dev:test` 三阶段测试验证
5. `/mp-dev:changelog` 生成变更记录
6. `/mp-dev:release` 准备发布

## 推荐搭配

建议同时安装 `mp-git` 插件，获得完整的 Git 工作流支持：

```
/plugin install mp-git@my-marketplace
```

## 许可

MIT License
