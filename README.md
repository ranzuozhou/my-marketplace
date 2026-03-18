# My Marketplace

个人插件市场，为 Claude Code 提供数据处理、知识管理等专业插件。

## 安装 Marketplace

在 Claude Code 中执行：

```
/plugin marketplace add ranzuozhou/my-marketplace
```

## 可用插件

| 插件 | 版本 | 说明 |
|------|------|------|
| **[mj-nlm](plugins/mj-nlm/)** | 1.0.0 | NotebookLM 知识库完整操作：认证、创建、管理、查询、Studio 制品生成 |

## 安装插件

```
/plugin install mj-nlm@my-marketplace
```

安装后可用命令：

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

## 许可

MIT License
