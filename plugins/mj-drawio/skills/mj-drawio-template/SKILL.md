---
name: mj-drawio-template
description: >-
  [mj-drawio] 使用 mj-system 预定义模板快速生成 .drawio 图表。内置 4 个模板:
  DDD 六层架构(ddd-six-layer)、ODS/DWD/DWS 数仓分层(dwh-ods-dwd-dws)、
  PL/pgSQL ETL 流程含 Advisory Lock(etl-flow)、PostgreSQL ER 图(er-diagram)。
  自带 mj-system 专用配色与图元规范。当用户提到 "用模板/架构模板/mj-system
  架构图/数仓图/ETL 流程图/ER 图/六层架构/DDD 架构" 时触发。不适用于纯自由
  创作(此时用 mj-drawio-create)、不适用于非 mj-system 领域图表、不适用于
  Linux/macOS/WSL 桌面环境(v0.1.0 仅 Windows)。
---

# mj-drawio:mj-drawio-template

## 核心职责

读取 `assets/templates/` 下的预置 `.drawio` 模板 → 按用户要填的内容(层名、表名、函数名、关系)做字符串替换 / 节点增删 → 写出新 `.drawio` → 调起 draw.io Desktop。

## 可用模板

| 模板 ID | 用途 | 文件 |
|---|---|---|
| `ddd-six-layer` | DDD 六层架构示意 | `assets/templates/ddd-six-layer.drawio` |
| `dwh-ods-dwd-dws` | 数仓三层(ODS / DWD / DWS)分层图 | `assets/templates/dwh-ods-dwd-dws.drawio` |
| `etl-flow` | PL/pgSQL ETL 流程(源表 → 函数 → 目标表 + Advisory Lock) | `assets/templates/etl-flow.drawio` |
| `er-diagram` | PostgreSQL ER 图(表 + 列 + 外键) | `assets/templates/er-diagram.drawio` |

## 工作流

### Step 1: 确认模板

若用户明说模板 ID(`ddd-six-layer` 等),直接用。否则根据用户描述推断:

- "架构图" / "DDD" / "六层" → `ddd-six-layer`
- "数仓" / "ODS" / "DWD" / "DWS" / "分层" → `dwh-ods-dwd-dws`
- "ETL" / "PL/pgSQL" / "Advisory Lock" / "函数流程" → `etl-flow`
- "ER 图" / "表关系" / "外键" → `er-diagram`

推断失败,用 AskUserQuestion 让用户选。

### Step 2: 读取模板作为基底

```powershell
$skillRoot = $PSScriptRoot
$template = Get-Content "$skillRoot\assets\templates\$templateId.drawio" -Raw
```

### Step 3: 收集用户填充内容

不同模板要填不同字段:

| 模板 | 需要收集 |
|---|---|
| `ddd-six-layer` | 每层里的模块名(可选,不填则用默认示意) |
| `dwh-ods-dwd-dws` | 每层的表名清单 |
| `etl-flow` | 源表、函数、目标表的 schema.name |
| `er-diagram` | 表名 + 主要列 + 外键关系 |

### Step 4: 替换 / 增删节点

**简单场景**: 模板里预留了 `{{PLACEHOLDER}}` 风格的占位符,直接字符串替换。

**复杂场景**: 解析 XML,按用户输入动态增加 `<mxCell>` 节点。参考 `../mj-drawio-create/references/xml-reference.md` 的节点规范。

### Step 5: 写文件 + 调起 draw.io

和 `mj-drawio-create` 的 Step 4/5 相同(复用流程):
- 输出目录: settings.output_dir 或 cwd
- 文件名: `<template-id>-<user-suffix>.drawio`
- 打开编辑: 调用插件级 `detect-drawio-cli.ps1`

## 配色规范

详见 `references/mj-palette.md`。核心表:

| 类别 | 配色 |
|---|---|
| DDD 六层 | Interface `#D4E1F5` / Application `#D5E8D4` / Domain `#FFE6CC` / Infrastructure `#F8CECC` / Shared `#E1D5E7` / Config `#DAE8FC` |
| 数仓三层 | ODS `#CCE5FF` / DWD `#D5E8D4` / DWS `#FFE6CC` |
| ETL 函数 | `#FFF2CC`(浅黄) |

## 扩展模板

新增模板步骤:
1. 用 draw.io Desktop 画好,另存为 `assets/templates/<new-id>.drawio`
2. 在本 SKILL.md 的"可用模板"表格追加一行
3. 在 Step 1 的"推断"映射表加关键词
4. 更新 `plugins/mj-drawio/CHANGELOG.md`

## 反例(不应触发本 skill)

| 场景 | 正确路由 |
|---|---|
| "画一个简单的 A→B→C 流程图" | 不触发 — 用 `mj-drawio-create` 自由创作 |
| "导出已有模板为 PNG" | 路由 `mj-drawio-export` |
| "在 PPT 里插入架构图" | 先本 skill 生成,再 export 为 PNG |

## 与其他 skill 的协作

- **mj-drawio-create**: 共用 XML 规范(`references/xml-reference.md` 在 create 目录)
- **mj-drawio-export**: 模板生成后,用户要图片时路由给它

## Reference Files

- `references/mj-palette.md` — mj-system 配色规范
- `assets/templates/*.drawio` — 4 个预置模板
- `../mj-drawio-create/references/xml-reference.md` — XML 生成规范(跨 skill 引用)
- `../../scripts/detect-drawio-cli.ps1` — 插件级 drawio.exe 探测
