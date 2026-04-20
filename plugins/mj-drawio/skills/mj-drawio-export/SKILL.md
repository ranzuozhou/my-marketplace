---
name: mj-drawio-export
description: >-
  [mj-drawio] 在 Windows 桌面环境中,把 .drawio 文件导出为 PNG / SVG / PDF,
  全部带 --embed-diagram 保持 XML 可编辑。当用户提到 "导出/转成/生成图片/
  另存为/转 PNG/转 PDF/截图保存/插入 PPT/贴到 Word/发到微信" 等涉及
  drawio 文件到图片格式转换时触发。导出产物可被 draw.io Desktop 重新打开
  继续编辑。不适用于 Linux/macOS/WSL 桌面环境(v0.1.0 仅 Windows)、不适用于
  非 .drawio 源文件、不适用于在线 drawio.com 的导出操作。
---

# mj-drawio:mj-drawio-export

## 核心职责

把本地 `.drawio` 文件 → 指定格式图片文件(PNG / SVG / PDF),保留可编辑 XML。

## 参数解析

| 参数 | 说明 | 默认值 | 覆盖来源 |
|---|---|---|---|
| `format` | `png` / `svg` / `pdf` | `png` | settings.default_format |
| `source` | `.drawio` 源文件路径 | 必填(用户提供或从上一次 create 推导) | — |
| `scale` | PNG 缩放倍数 | `2` | settings.default_scale |
| `transparent` | PNG 背景透明 | `true` | settings.default_transparent |
| `embed` | 嵌入可编辑 XML | `true`(**固定,不建议禁用**) | — |
| `output_dir` | 输出目录 | 源文件所在目录 | settings.output_dir |
| `page` | 多页时指定页码(0-based) | `all`(所有页) | — |

**settings 读取**: 从 `.claude/mj-drawio.local.md` 的 YAML frontmatter 读取 `default_format` / `default_scale` / `default_transparent` / `output_dir` / `drawio_cli_path`。文件不存在则用上述默认。

## CLI 调用

先定位 drawio.exe(复用插件级脚本),再调导出:

```powershell
$drawioRoot = Split-Path (Split-Path $PSScriptRoot)
$drawio = & "$drawioRoot\scripts\detect-drawio-cli.ps1"

$output = "$($source -replace '\.drawio$','.drawio').$format"

& $drawio `
    --export `
    --format $format `
    --scale $scale `
    --transparent `
    --embed-diagram `
    --output "$output" `
    "$source"
```

**注**: SVG / PDF 不需要 `--scale` 和 `--transparent`,按 format 分支省略即可。

## 后置处理

1. **校验产物**: 检查输出文件存在且大小 > 1KB(过小往往是 XML 错误导致的空白)
2. **Embed 验证**(仅 PNG): 用 exiftool 或 PIL 检查 PNG 的 metadata 含 `diagram`/`mxGraphModel`,证实嵌入生效
3. **清理中间文件**(可选): 若用户说"清理原文件",删除 `.drawio`(因导出文件已嵌 XML 可回编辑)
4. **返回绝对路径**供用户贴到 PPT / Word / 微信等

## 常见失败

| 错误 | 原因 | 解决 |
|---|---|---|
| `Failed to parse XML` | .drawio 含 `--` 或未转义特殊字符 | 回到 `mj-drawio-create`,跑 validate-xml.py 定位 |
| `Command not found` | drawio.exe 路径异常 | 重跑 `detect-drawio-cli.ps1`,或在 settings 里显式给 `drawio_cli_path` |
| PNG 空白 | edge 缺 `<mxGeometry>` | 重新生成源文件 |
| PDF 字体乱码 | 系统缺中文字体 | 换 SVG 替代,或在 drawio CLI 指定 `--fontmap` |
| 输出文件 < 1KB | XML 渲染失败 | 检查源文件在 draw.io Desktop 里能否正常打开 |

## 反例(不应触发本 skill)

| 场景 | 正确路由 |
|---|---|
| "把 PDF 转成 PNG" | 不触发 — 这不是 drawio 文件 |
| "从头画张流程图并导出" | 先 `mj-drawio-create`,再本 skill |
| "截图当前屏幕" | 不触发 — 用系统截图工具 |
| "上传到网盘" | 不触发 — 超出 skill 范围 |

## 与其他 skill 的协作

- **mj-drawio-create**: 若用户只说"画一张 X 并导成 PNG",先调 create,再本 skill
- **mj-drawio-template**: 同上,template 会先生成 `.drawio`,再路由到本 skill

## Reference Files

- `../../scripts/detect-drawio-cli.ps1` — 插件级 drawio.exe 探测(两 skill 共用)
