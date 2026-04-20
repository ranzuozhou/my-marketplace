# mj-drawio

draw.io 图表生成工具集,适配 mj-system 领域语义。Windows 桌面专用。

## 前置要求

| 项 | 检查命令 | 期望 |
|---|---|---|
| Claude Code | `claude --version` | ≥ 1.0.33 |
| 运行环境 | — | Windows PowerShell 7(非 WSL) |
| draw.io Desktop | `Get-Command drawio -ErrorAction SilentlyContinue` | 已装(默认 `C:\Program Files\draw.io\`) |
| Python 3 | `python --version` | ≥ 3.8(validate-xml.py 依赖) |

draw.io Desktop 没装:

```powershell
winget install JGraph.Draw
```

## 安装

```
/plugin install mj-drawio@my-marketplace
```

## Skills

| Skill | 用途 |
|---|---|
| `mj-drawio-create` | 从自然语言生成 `.drawio`,Python 预校验 + 调起 draw.io Desktop |
| `mj-drawio-export` | `.drawio` → PNG / SVG / PDF(带 `--embed-diagram`,可回编辑) |
| `mj-drawio-template` | mj-system 预置模板:DDD 六层 / 数仓分层 / ETL 流程 / ER 图 |

## 快速开始

### 1. 从自然语言生成

```
画一张 mj-system 的 ETL 流程图,包含 QCM 贡献度计算和 Advisory Lock
```

### 2. 用模板快速起步

```
/mj-drawio:mj-drawio-template ddd-six-layer
```

### 3. 导出贴 PPT

```
/mj-drawio:mj-drawio-export png ./architecture.drawio
```

## 用户级配置(可选)

在**项目根目录**创建 `.claude/mj-drawio.local.md` 覆盖默认行为:

```markdown
---
enabled: true
drawio_cli_path: "C:\\Program Files\\draw.io\\draw.io.exe"
default_format: png
default_scale: 2
default_transparent: true
output_dir: "./"
validate_xml: true
---

# mj-drawio 项目级配置
```

**注**:
- 仓库根 `.gitignore` 已通过 `.claude/*` 规则覆盖 `.claude/*.local.md`,你的项目若未覆盖,建议自行添加
- 修改后需**重启 Claude Code**(settings 在 session 启动时加载)

## mj-system 专用模板

| 模板 ID | 用途 | 关键图元 |
|---|---|---|
| `ddd-six-layer` | DDD 六层架构示意 | Interface / Application / Domain / Infrastructure / Shared / Config(6 色) |
| `dwh-ods-dwd-dws` | 数仓三层分层图 | ODS(浅蓝) / DWD(浅绿) / DWS(浅橙) |
| `etl-flow` | PL/pgSQL ETL 流程 | 源表 → 函数节点 → 目标表 + Advisory Lock 标记 |
| `er-diagram` | PostgreSQL ER 图 | 表 + 列 + 外键关系 |

## 适用范围

- **v0.1.0 仅支持 Windows 10/11**(原生 PowerShell 环境)
- WSL2 / macOS / Linux 桌面暂不支持 — 有需求请提 Issue

## 致谢

- 核心协议与 XML 规范基于 [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp) skill-cli 方案本地化
