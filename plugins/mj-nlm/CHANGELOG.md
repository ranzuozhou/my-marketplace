# Changelog

All notable changes to the mj-nlm plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.0.1] - 2026-05-06

### Changed

- **`project=agent` 扫描映射定稿**：依据 mj-agent develop 仓库实际目录树，把 v2.0 的占位符（`agents/` `tools/` `workflows/`，4 scope）替换为方案 B 的 6 scope 真实映射。mj-agent 是单 agent 单包项目（LangChain 1.x + LangGraph 1.1.8 + Python 3.13 + dual-track 文档框架），新 scope 集：
  - `code` → `src/mj_agent/` 整包 + `langgraph.json` + `pyproject.toml`
  - `tool` → `src/mj_agent/tools/{ToolName}/`（含 `tools/sql/{guardrail,execute,introspect}.py`）+ `tools/__init__.py` ALL_TOOLS 注册
  - `skill` → `src/mj_agent/skills/{SkillName}/SKILL.md`（Track B）+ 关联 EVAL / PROMPT
  - `prompt` → `src/mj_agent/prompts/system.md` + 其他 prompt 文件（Track B）
  - `docs` → `docs/{adr,rule,infrastructure,assessments}/`（Track A）按聚焦点取子集
  - `cross` → `CLAUDE.md` + `pyproject.toml` + `langgraph.json` + `plans/` + `.env.example`
- **删除 scope `agent` 与 `workflow`**（旧占位符，与 mj-agent 单 agent 实际不符）
- **新增 source 类别标签**：`Agent核心` / `Skill` / `Prompt` / `集成`；移除 v2.0 的 `工作流` 标签
- **同步更新文件**：`naming-reference.md#project=agent`（scope 表 + Scope→默认扫描范围映射 + tag 示例）、`build/SKILL.md`（Phase 1 scope 映射表 + 命名示例 + Note 2 项目上下文模板 + Examples 2/2b）、`CLAUDE.md`（命名示例）、`README.md`（roadmap 标记）

### Notes

- 这是对 v2.0「Known Issues #1（mj-agent 路径占位符）」的定稿修订，无新功能、无 MCP 接口变更
- v2.0 → v2.0.1 的迁移：现有 `MJ-agent-agent-*` 命名 notebook 仍可用（命名格式向后兼容），但建议新建 notebook 改用新 scope（`code` / `tool` / `skill` / `prompt` / `docs` / `cross`）

## [2.0.0] - 2026-05-06

### 升级主旨

从 v1 的「被动产出制品」重构为 v2 的「学习闭环」（依据方法论文档：先降低进入成本，再用提问 / 测验 / 复述 / 查证完成真正理解）。覆盖范围扩展到 MJ-AgentLab 组织（mj-system + mj-agent 双项目）。

### Added

- **新增 skill `mj-nlm-learn`**：学习闭环编排器（10 Phase + 5 Gate），一站式调度 build / studio / query 走完完整学习闭环
  - 命令形态：`/mj-nlm:learn <topic>` / `--resume <nbid>` / `--quiz-only <nbid>` / `--triple-view <topic>` / `--lite <topic>`
- **build skill 新增 Phase 6**：来源充足性预检（来源/制品长度配比矩阵），输出元 source `00d-预检-来源充足性报告`
- **build skill 新增 Phase 7**：领域定向报告（含 7 节：领域归属 / 原始困惑翻译 / 核心概念地图 / 术语翻译表 / 成功失败案例 / 学习路线 / 推荐制品组合），输出元 source `00c-定向-{topic}领域定向报告`，作为后续制品的"学习地图"锚
- **build skill 新增双项目支持**：`project=agent` 进入正式支持（含 4 个 scope: agent / tool / workflow / cross；mj-agent 路径以占位符默认值提供，待用户提供真实目录后修正）
- **build skill 新增 H7 / H8** H-points
- **studio skill 新增 view 子参数**：`foundation` / `structural` / `challenge` 三个学习视角（来自方法论 §8 同一内容三版）
- **studio skill 新增默认幻觉防护**：所有 studio_create 调用自动追加固定约束句（可通过 `disable_guardrails=True` 关闭；`risk-class:high` notebook 强制开）
- **studio skill 新增 H4** Hard Block（来源充足性预检阻断）
- **query skill 新增 Mode D**：Quiz 错题 root cause 归因 + 重学建议
- **query skill 新增 Mode E**：Source Check 来源核查（DIRECT / INFERRED / BACKGROUND / UNCERTAIN / CONTRADICTED 5 级标注）
- **query skill 新增 Mode F**：7 项理解度量化指标自检 → 仪表盘 Note `99-自检-理解度仪表盘-{YYYYMMDD}-{HHMM}`
- **query skill 新增 H3 / H4** H-points
- **shared 新增 `risk-control-templates.md`**：来源/制品配比矩阵 + 默认幻觉防护约束句 + 高风险类别白名单（医疗 / 法律 / 财务 / 合同 / 考试 / 安全） + Source Check 等级体系 + 配额成本
- **shared 新增 `learning-loop-templates.md`**：7 个 prompt 模板（§1 领域定向报告 / §2 三版 / §3 错题 root cause / §4 案例机制 / §5 来源核查 / §6 术语翻译 / §7 理解度自检）
- **shared 新增 `understanding-metrics.md`**：7 项指标定义 + 自评量表 + NLM 验证逻辑 + 仪表盘 Note 模板 + 三级评级（入门 / 熟悉 / 掌握）

### Changed

- **`focus-prompt-templates.md` 完全重写为 v2 学习导向**：9 种 artifact_type 的 Intent Layer 模板全部改为「学习闭环」导向；新增 view × artifact_type 组合模板（audio/video/slide_deck × foundation/structural/challenge）；引入三层拼接策略（Intent + Content + Guardrails）；Content Layer 升级为额外读取 00c 定向报告
- **`naming-reference.md` 扩展为双项目**：project=system / agent / multi / intel 各自独立 scope→扫描路径映射；新增 `定向` / `预检` / `自检` / `Agent` / `工具` / `工作流` 类别标签；新增 `00c` / `00d` / `99` 元 source 编号约定；新增 v2 tag `learn-loop` 与 `risk-class:{level}`
- **`material-classification.md` 扩展多源类型**：新增 url / youtube / drive / image / audio 多源分类与注意事项；新增"5 类来源"对应表；新增 v2 来源充足性预检触发逻辑
- **`artifact-type-reference.md` 扩展子参数说明**：新增 `view` / `disable_guardrails` / `focus_prompt_template` 三个横切子参数详解
- **build skill 重写 SKILL.md**：原 5 Phase 扩展到 7 Phase；workflow 图更新；description 增加学习地图 / 双项目相关触发词
- **studio skill 重写 SKILL.md**：Phase 2 拆分为 5 个 Step（含三层 Focus Prompt 拼接 + 来源充足性预检 + view 选择）；Phase 3 增加三版循环模式；description 增加三版 / 学习导向相关触发词
- **query skill 重写 SKILL.md**：从 3 种 Mode 扩展到 6 种；workflow 图更新；description 增加 Mode D/E/F 相关触发词
- **plugin.json**：version 1.0.0 → 2.0.0；description 重写突出学习闭环 + 双项目；keywords 扩展（learning-loop / domain-orientation / quiz-feedback / source-check / mj-system / mj-agent / mj-agentlab）
- **README.md**：完全重写，突出学习闭环、6 命令、v2 核心新概念、双项目、设计哲学、未来 roadmap
- **CLAUDE.md**：6 skill 表 + 双项目说明 + v2 元 source 编号约定 + v2 文件结构

### Breaking Changes（仅 workflow 与产物层，不动 MCP 接口）

- **build 输出从 2 个元 source 增至 4 个**（新增 `00c-定向-` `00d-预检-`）— 旧 notebook 不受影响，新 build 自动加
- **studio focus-prompt 默认模板替换**：旧模板保留为 `legacy_*` 前缀别名（v2.0 / v2.1 / v2.2 仍可用，v2.3 抛 deprecation warning，v2.4 移除）
- **studio_create 默认追加幻觉防护约束**：可通过 `disable_guardrails=True` 关闭，但 `risk-class:high` tag notebook 强制忽略此设置

### Migration（v1 → v2）

- 旧 notebook 命名格式 `MJ-{project}-{scope}-{topic}-{YYYYMMDD}` **不变**，无需迁移命名
- 现有 v1 notebook 无 `00c` / `00d` 元 source —— 可手动跑 `/mj-nlm:build --resume <nbid>` 仅触发 P6/P7 补齐
- 现有 v1 prompt 调用：focus_prompt 字符串不变即可继续工作（v2 默认追加约束句但不破坏内容）；如需明确切换到 v1 模板用 `focus_prompt_template="legacy_*"`
- mj-agent 路径占位符：使用 `project=agent` 前先确认 mj-agent 真实仓库目录树，更新 `naming-reference.md` 相应小节

### Known Issues / Roadmap

- mj-agent 路径目前为占位符（`agents/` `tools/` `workflows/`）—— 需用户提供真实目录树后定稿
- 三版生成会触发 ~9 次 studio_create（约 25-30 分钟），可用 `--lite` 跳过 video 节省时间
- 24h 复述指标依赖人工触发 `/mj-nlm:query --mode=recall`，v2.1 计划用 hooks 自动提醒
- v2.0 prompt 模板仅中文，v2.x 计划增 en

## [1.0.0] - 2026-03-18

### Added

- 初始发布：5 个 Skill（auth / build / manage / query / studio）
- NotebookLM MCP 集成
- 共享参考文件（artifact-type-reference / focus-prompt-templates / material-classification / naming-reference）
