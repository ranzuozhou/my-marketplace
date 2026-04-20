# Changelog

## [0.1.0] - 2026-04-20

### Added
- 初始版本,基于 [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp) skill-cli 方案本地化适配
- 3 个 skill:`mj-drawio-create` / `mj-drawio-export` / `mj-drawio-template`
- 插件级共享脚本 `scripts/detect-drawio-cli.ps1`(两 skill 共用 drawio.exe 路径探测)
- `validate-xml.py` 预校验脚本:XML well-formed + 根 cell(id=0/1) + edge `<mxGeometry>` 结构检查
- 4 个 mj-system 预置模板占位(`assets/templates/` 下):
  - `ddd-six-layer` — DDD 六层架构
  - `dwh-ods-dwd-dws` — 数仓三层
  - `etl-flow` — PL/pgSQL ETL 流程
  - `er-diagram` — PostgreSQL ER 图
- 本地化 `xml-reference.md` + `mj-palette.md`(mj-system 配色规范)
- `evals/evals.json` 含 3 个代表性 test prompt + 客观 assertions(供 skill-creator iteration)
- 插件根 `CLAUDE.md` / `README.md` / `CHANGELOG.md`(与 marketplace 其他插件对齐)
- 支持 `.claude/mj-drawio.local.md` 用户级配置(可选启用)

### 适用范围
- 仅支持 Windows 10/11 桌面环境(v0.1.0)
- WSL2 / macOS / Linux desktop 延后到 v0.2+

### 已知限制
- 4 个 `.drawio` 模板 v0.1.0 为最小占位 XML,结构合法但示例图元简略;v0.1.1 计划用 draw.io Desktop 手画真实内容替换
