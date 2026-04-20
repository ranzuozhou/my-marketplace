---
name: mj-drawio-create
description: >-
  [mj-drawio] 在 Windows 桌面环境中,把自然语言描述转换为合法的 .drawio 文件
  (mxGraphModel XML),写入本地磁盘,并用 draw.io Desktop 打开。当用户需要绘制
  架构图、流程图、ER 图、序列图、类图、组件图、甘特图、思维导图,或提到
  "画一张/生成/创建/做一个" + "架构图/流程图/drawio 格式" 时触发。支持基于
  XML / Mermaid / CSV 的输入,输出文件带可编辑 XML,可在 draw.io Desktop
  重新打开编辑。即使用户没明说 drawio,只要目标是本地桌面可编辑的图表文件,
  也应使用本 skill。不适用于 mj-system 服务代码、不适用于在线 drawio.com 网页
  工作流、不适用于 Linux/macOS/WSL 桌面环境(v0.1.0 仅 Windows)。
---

# mj-drawio:mj-drawio-create

## 核心职责

把自然语言描述 → `mxGraphModel` XML → 本地 `.drawio` 文件,调起 draw.io Desktop 打开。

## 执行协议

### Step 1: 解析意图

从用户输入里识别:

| 维度 | 取值举例 |
|---|---|
| 图表类型 | flowchart / architecture / er / sequence / state / class / gantt / mindmap |
| 画布方向 | 横版 / 竖版 / 方形 |
| 是否用 mj-system 模板 | 是 → 路由到 `mj-drawio-template`;否 → 继续本 skill |
| 目标文件名 | 从用户描述推导 kebab-case,如 `ddd-six-layer-architecture.drawio` |
| 输出目录 | 优先 `.claude/mj-drawio.local.md` 的 `output_dir`,否则 cwd |

### Step 2: 生成 XML(硬性规则)

1. **根结构**: 必须是 `<mxGraphModel>` → `<root>` → 含 `id="0"` 和 `id="1"` 两个根 cell
2. **每条 edge**: 必须含 `<mxGeometry relative="1" as="geometry" />`
3. **XML 注释**: 不能包含 `--`
4. **标签里的特殊字符**: `&` → `&amp;`,`<` → `&lt;`,`>` → `&gt;`

**详细规范和样式字典见 `references/xml-reference.md`**(需要时再加载,不要一上来就全读)。

### Step 3: XML 预校验(强烈建议,除非 settings 禁用)

生成后用 Python 脚本预检,失败则重新生成:

```powershell
python "$PSScriptRoot\scripts\validate-xml.py" "$filepath"
```

预期输出: `OK: N cells, M edges, 全部 geometry 完整`

若报 `FAIL:...`,回到 Step 2 修正。

**跳过条件**: 当 `.claude/mj-drawio.local.md` 含 `validate_xml: false` 时可跳过。

### Step 4: 写文件

- **位置**: 优先 settings 里的 `output_dir`,否则当前工作目录
- **命名**: 基于用户描述生成 kebab-case,无中文无空格
- **已存在时**: 追加序号 `-v2` / `-v3` 避免覆盖

### Step 5: 调起 draw.io Desktop

先定位 CLI(复用插件级探测脚本),再打开文件:

```powershell
# 插件根 scripts/ 两 skill 共用
$drawioRoot = Split-Path (Split-Path (Split-Path $PSScriptRoot))
$drawio = & "$drawioRoot\scripts\detect-drawio-cli.ps1"
Start-Process $drawio -ArgumentList "`"$filepath`""
```

**优先级**: 若 `.claude/mj-drawio.local.md` 含 `drawio_cli_path`,用该路径;否则调探测脚本。

## 输出反馈给用户

- 文件的**绝对路径**
- 节点数、边数
- 使用的样式风格(flowchart / DDD / etc.)
- 后续建议(用 `mj-drawio-export` 导图、用 `mj-drawio-template` 套用其他模板)

## 反例(不应触发本 skill)

| 场景 | 正确路由 |
|---|---|
| "用 Mermaid 画个流程图贴在 README 里" | 不触发 — 直接在聊天里返回 Mermaid 代码 |
| "导出已有的 .drawio 为 PNG" | 路由到 `mj-drawio-export` |
| "用 DDD 六层模板画一张" | 路由到 `mj-drawio-template` |
| "生成 PostgreSQL 建表 SQL" | 不触发 — 这是数据库 SQL 不是图表 |
| "在 macOS 上画图" | 不触发 — v0.1.0 仅支持 Windows,告知用户 |

## 与其他 skill 的协作

- **mj-drawio-template**: 若用户明说模板名(`ddd-six-layer` / `etl-flow` 等),优先路由给它,它会复用本 skill 的写文件 + 调起逻辑
- **mj-drawio-export**: 创建完成后若用户要图片,路由给它,无需用户复述 drawio 路径

## Reference Files

- `references/xml-reference.md` — drawio XML 完整规范(mxGraphModel / mxCell / style string / mj-system 扩展)
- `scripts/validate-xml.py` — XML 结构预校验
- `../../scripts/detect-drawio-cli.ps1` — 插件级 drawio.exe 探测(两 skill 共用)
