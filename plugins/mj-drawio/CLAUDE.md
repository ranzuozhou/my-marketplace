# mj-drawio

draw.io 图表生成与 mj-system 模板工具集(Windows 桌面环境专用)。

## Skills

| Skill 目录 | 触发命令 | 用途 |
|---|---|---|
| `mj-drawio-create` | `/mj-drawio:mj-drawio-create`、"画一张/生成架构图" | 自然语言 → `.drawio` 文件 |
| `mj-drawio-export` | `/mj-drawio:mj-drawio-export`、"导出 PNG/SVG/PDF" | `.drawio` → 图片(带 `--embed-diagram`) |
| `mj-drawio-template` | `/mj-drawio:mj-drawio-template`、"用模板画" | 使用 mj-system 预置模板 |

## 依赖

| 依赖 | 版本 | 用途 |
|---|---|---|
| draw.io Desktop | 最新 | XML 渲染 + CLI 导出(`winget install JGraph.Draw`) |
| Python | ≥ 3.8 | `validate-xml.py` 预校验 |
| PowerShell | 7+ | `detect-drawio-cli.ps1` 路径探测 |
| Windows | 10 / 11 | 桌面环境(WSL / macOS / Linux 暂不支持) |

## 插件目录结构

```
mj-drawio/
├── .claude-plugin/plugin.json      # 插件元数据
├── CLAUDE.md                       # 本文件
├── README.md                       # 用户指南
├── CHANGELOG.md                    # 变更日志
├── scripts/
│   └── detect-drawio-cli.ps1       # drawio.exe 路径探测(两 skill 共用)
├── skills/
│   ├── mj-drawio-create/
│   │   ├── SKILL.md
│   │   ├── references/xml-reference.md
│   │   └── scripts/validate-xml.py
│   ├── mj-drawio-export/
│   │   └── SKILL.md
│   └── mj-drawio-template/
│       ├── SKILL.md
│       ├── references/mj-palette.md
│       └── assets/templates/       # 4 个 .drawio 预置模板
└── evals/evals.json                # skill-creator 测试集
```

## 用户级配置(可选)

支持 `.claude/mj-drawio.local.md`(项目内,被仓库根 `.gitignore` 的 `.claude/*` 规则覆盖):
- `drawio_cli_path` — 自定义 drawio.exe 路径
- `default_format` / `default_scale` / `default_transparent` — 导出默认值
- `output_dir` — 默认输出目录
- `validate_xml` — 是否启用生成后 Python 预校验

模板见 README.md。

## 不适用场景

- mj-system 服务代码生成(此处只做图表)
- 在线协作编辑(drawio.com 网页端工作流)
- 非 Windows 桌面环境(v0.1.0 范围内)
- 批量自动生成图表(当前逐张)
