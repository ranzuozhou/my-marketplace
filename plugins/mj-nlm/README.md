# mj-nlm — NotebookLM Plugin for Claude Code

MJ System NotebookLM 技能家族，提供 NLM 知识库的认证、创建、管理、查询和 Studio 制品生成能力。

## 功能

| 命令 | 说明 |
|------|------|
| `/mj-nlm:auth` | NLM 认证（登录、刷新、切换账号、故障排查） |
| `/mj-nlm:build` | 创建知识库（扫描项目→导入 source→打标签） |
| `/mj-nlm:manage` | 管理知识库（Notebook/Source/Tag CRUD + 分享） |
| `/mj-nlm:query` | 知识问答（单 notebook / 跨 notebook / Deep Research） |
| `/mj-nlm:studio` | Studio 制品生成（音频/视频/幻灯片等 9 种类型） |

## 前置条件

- **Claude Code** v2.1+
- **NotebookLM MCP CLI**：
  ```bash
  uv tool install notebooklm-mcp-cli --with socksio --force
  ```
- **Google 认证**：
  ```bash
  nlm login
  ```

## 安装方式

### 通过 Marketplace 安装（推荐）

```
/plugin marketplace add ranzuozhou/mj-marketplace
/plugin install mj-nlm@mj-marketplace
```

### 本地开发安装

```bash
claude --plugin-dir "D:\workspace\10-software-project\projects\mj-marketplace\plugins\mj-nlm"
```

## 验证安装

```
/plugin                    # 确认 mj-nlm 出现在列表
/mj-nlm:build             # 测试 skill 加载
/mcp                       # 确认 notebooklm-mcp 可用
```

## 自然语言触发

除了斜杠命令，也支持自然语言触发：

- "帮我建一个 NLM 知识库" → `/mj-nlm:build`
- "NLM 认证过期了" → `/mj-nlm:auth`
- "查看 NLM 知识库列表" → `/mj-nlm:manage`
- "问一下 DQV 的验证策略" → `/mj-nlm:query`
- "生成音频播客" → `/mj-nlm:studio`

## 许可

MIT License
