# Changelog

All notable changes to the mj-nlm plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.3.0] - 2026-05-08

### 升级主旨

完成 v2.2 forward-announce 的 deprecation removal：移除 `/mj-nlm:learn` skill（v2.0 引入 / v2.2 deprecated）；新增 `mj-nlm-shared/preflight-checklist.md` + `mj-nlm-shared/quota-estimation.md` 两份共享规范，把 v2.0/v2.1 学习闭环卡 Phase 7 的根因（认证 / scope 故障晚发现）+ 用户对耗时无预期 两个 UX 痛点前移到 Phase 0。**轻量 BREAKING（已经过 v2.2 ~2 周公告期）**。

### Removed

- **`mj-nlm-learn/` skill**（连同 SKILL.md 整个目录）— v2.0 引入的单一编排器；v2.2 起 deprecated；v2.3 完整移除。所有调用应改用 `/mj-nlm:learn-make` + `/mj-nlm:learn-test` 串联（v2.2 已上线）。

### Added

- **共享文档 `mj-nlm-shared/preflight-checklist.md`**：NLM 启动冒烟三级 checklist —— L1 Auth Token（refresh_auth status） / L2 NLM Service Health（server_info + notebook_list） / L3 Notebook scope（notebook_describe + 可选 notebook_query），含 5min 缓存策略 + 集成点 + H-point 模板供各 skill Phase 0 嵌入
- **共享文档 `mj-nlm-shared/quota-estimation.md`**：单调用耗时基线（一次性 / per-source / per-artifact 三类） + 双 wrapper（learn-make / learn-test）配额预告 + build / studio / query 单步耗时 + NotebookLM 公开+经验配额上限（含 source 上限 / studio rate / query rate / 文件大小限）+ 总耗时报告模板（用于 Phase 0 输出）
- **build / learn-make / learn-test SKILL.md Reference 段** 加新两 shared 文档引用

### Changed

- **mj-nlm-shared/risk-control-templates.md §6** 抽出 → quota-estimation.md（risk-control 保留单行 stub 指向新文件，扩展为双 wrapper 口径）
- **build skill description 反向触发约束** 由「`/mj-nlm:learn`」改为「`/mj-nlm:learn-make`」+「`/mj-nlm:learn-test`」拆两条
- **studio / query SKILL.md** 内所有 `/mj-nlm:learn` 引用改为 wrapper 双命令（含 query Mode F 的 LEARN_ORCHESTRATED 边界说明改为 learn-test wrapper Phase 2c）
- **shared/artifact-metadata-template.md** "何时由谁写"表 + **shared/naming-reference.md** `learn-loop` tag 表 同步改为 wrapper 命令
- **plugin.json**：2.2.0 → 2.3.0；description 删除「learn[deprecated]」标识，改为「底层 5 skill」+ v2.3 preflight/quota 注释；keywords +`preflight` / `quota-estimation`
- **CLAUDE.md / README.md**：v2.3 升级要点段；8 skill → 7 skill 表（删 learn）；shared 8 份 → 10 份（preflight + quota）；roadmap v2.3 标 ✅；v2.4-v2.6 重排
- **README.md** 中「学习闭环编排器 `/mj-nlm:learn`（v2.2 deprecated）」整段删除；新增「v2.3 核心新概念」段；"单步使用 advanced" 表删 `/mj-nlm:learn` 行

### Migration（v2.2 → v2.3）

无破坏性影响——v2.2 已 forward-announce，所有正常用户在 v2.2 阶段已迁移到 wrapper。

| v2.2 状态 | v2.3 行为 |
|---|---|
| 用户调 `/mj-nlm:learn` | skill 已不存在 → Claude Code 报 unknown skill；改用 `/mj-nlm:learn-make` + `/mj-nlm:learn-test` |
| 调 `/mj-nlm:learn --resume <nb_id>` | 改用 `/mj-nlm:learn-make --resume <nb_id>`（共享 `learn-phase:G{N}-passed` tag） |
| Claude 引擎自动选 `/mj-nlm:learn` | 已删除，引擎自动改选 wrapper（learn-make 与 learn-test 的 description 已涵盖原 learn 触发关键词） |

### Known Issues / Roadmap

- v2.4 候选：将 preflight-checklist L1+L2 实际编进各 skill Phase 0 实施代码（v2.3 仅文档化 H-point 模板）；NLM artifact-level URL 暴露调研（v2.1 回退方案 B → 若 NLM 暴露则升级）
- v2.5 候选：Hooks 自动检测过期 24h 复述提醒
- v2.6 候选：移除 v1 `legacy_*` prompt 别名

## [2.2.0] - 2026-05-08

### 升级主旨

把 v2.0 引入的单一编排器 `/mj-nlm:learn` 拆为两个语义对偶的 high-level wrapper：`/mj-nlm:learn-make`（生成学习资料）+ `/mj-nlm:learn-test`（生成考察资料）。用户对外只需记 2 个命令，底层 6 skill 仍可独立调用。**非破坏性 UX 优化**。

### Added

- **新增 skill `mj-nlm-learn-make`**（wrapper 1，学习侧编排器）：
  - 4 Phase：Notebook Locate → Build (条件) → Artifact Mix Selection (AskUserQuestion 多选 7 类) → Studio Iteration (循环 record mode)
  - 启动标志：`<topic>` / `--resume <nb_id>` / `--triple-view` / `--with-download` / `--download-only`
  - 复用底层 `build` (Phase 1) + `studio` (Phase 3)，纯 dispatch 不重写
  - H1-H4 涵盖 build 失败 / 多选为空 / 单类失败 / 来源不足
- **新增 skill `mj-nlm-learn-test`**（wrapper 2，考察侧编排器）：
  - 3 Phase（含 4 子分支 2a/2b/2c/2d）：Notebook Locate → Assessment Mix Selection (默认锁 quiz+flashcards，D/F/E 需勾) → Quiz/Flashcards 生成 → 错题归因/自检/来源核查
  - 启动标志：`<nb_id>` / `--full` / `--rootcause` / `--selfcheck` / `--sourcecheck`
  - 复用底层 `studio` (Phase 2a) + `query` Mode D/F/E (Phase 2b/2c/2d)
  - H0/H1/H2a/H2b/H2d 涵盖无 notebook / 取消默认锁 / studio 失败 / 错题空 / 高风险强制核查
- **新增自然语言触发词**：「生成学习资料 / 一键学习材料」 → learn-make；「生成考察资料 / 出题 / 错题归因 / 自检 / 来源核查」 → learn-test

### Changed

- **mj-nlm-learn SKILL.md frontmatter** description 前缀加 `[DEPRECATED v2.2 — use /mj-nlm:learn-make + /mj-nlm:learn-test 串联替代]`
- **mj-nlm-learn SKILL.md body** 顶加 v2.2 迁移段（含 v2.1 → v2.2 的 Phase 对照表）；保留全部 10 Phase 原文供 v2.3 删除前回滚
- **CLAUDE.md**：v2.2 升级要点段；6 skill 表 → 8 skill 表（拆分为 high-level wrapper + 底层 skill 两段）；文件结构 + skill 调用约定
- **README.md**：v2.2 顶引；6 命令 → 8 命令表（同样拆两段）；新增「v2.2 核心新概念」段（高层入口 / 完整闭环示例 / 与 v2.1 关系）；快速上手段重写为「两 wrapper 串联」；自然语言触发段加 learn-make / learn-test 触发词；roadmap 标 v2.2 完成、v2.3-v2.5 重排
- **plugin.json**：version 2.1.0 → 2.2.0；description 加 v2.2 高层入口说明；keywords 新增 `learn-orchestration` / `high-level-wrapper` / `learn-make` / `learn-test`

### Deprecated

- **`/mj-nlm:learn`** — v2.0 引入的单一编排器；v2.2 起标 deprecated，由 `/mj-nlm:learn-make` + `/mj-nlm:learn-test` 串联替代；保留至 v2.3 删除（约 2-3 周观察期），现有 v2.0/v2.1 用户不受影响

### Migration（v2.1 → v2.2）

| v2.1 `/mj-nlm:learn` 阶段 | v2.2 替代 |
|---|---|
| Phase 0-1（来源准备 + build） | `/mj-nlm:learn-make <topic>` 内置 Phase 1 (build 条件触发) |
| Gate 1（00c 审定） | 下沉到 build skill Phase 7 H-point；如需强审定可单独 `/mj-nlm:build` |
| Phase 2-5（mind_map / video / slide / audio） | `/mj-nlm:learn-make` Phase 2 多选 + Phase 3 循环 |
| Phase 6（quiz + flashcards） | `/mj-nlm:learn-test <nb_id>` Phase 2a（默认锁定） |
| Phase 7（Mode D 错题归因） | `/mj-nlm:learn-test --rootcause <nb_id>` 或 Phase 1 勾选 |
| Phase 8（Mode F 自检） | `/mj-nlm:learn-test --selfcheck <nb_id>` 或 Phase 1 勾选 |
| Phase 9（Mode E 来源核查） | `/mj-nlm:learn-test --sourcecheck <nb_id>` 或 Phase 1 勾选 |
| `--triple-view` | `/mj-nlm:learn-make --triple-view <topic>` |
| `--with-download` / `--download-only` | 同名标志，wrapper 1/2 均支持透传 |
| `--resume <nb_id>` | `/mj-nlm:learn-make --resume <nb_id>`（兼容旧 `learn-phase:G{N}-passed` tag） |
| `--lite` / `--quiz-only` | wrapper 1 不选 video / wrapper 2 默认即等价 |

完整 v2.2 替代流程：`/mj-nlm:learn-make <topic>` → notebook + 学习资料 → `/mj-nlm:learn-test <nb_id>` → 考察资料 + 自检

### Known Issues / Roadmap

- v2.3 计划删除 deprecated 的 `/mj-nlm:learn`（约 2-3 周观察期后）
- v2.2 wrapper description 与底层 studio/build/query description 关键词存在重叠 → agent 分发时按 wrapper 强标识词「编排 / orchestrate / 一键 / wrapper」+ 反向「Do not use for: 单步...」三段消歧；如发现 agent 分发摇摆，会在 v2.2.x patch 强化 description
- 旧 v2.0/v2.1 `/mj-nlm:learn --resume <nb_id>` 流程可由 `/mj-nlm:learn-make --resume` 无缝接管（共享 `learn-phase:G{N}-passed` tag）

## [2.1.0] - 2026-05-08

### 升级主旨

studio Phase 4 默认输出形态从「download 二进制到本地」改为「record 元信息 markdown」，对齐 mj-system / mj-agent learning 子系统的强约束（markdown 进 git，binary 永不入 git，NotebookLM 产物全部在线托管）。download 路径降级为显式 opt-in。

### Added

- **新增共享模板 `mj-nlm-shared/artifact-metadata-template.md`**：record markdown 范式（frontmatter schema + ≤ 50 行 body + 命名与存放约定 + 与 learning 子系统对齐说明 + record vs download 对比）
- **studio skill Phase 4 三模式**：`--mode record`（默认）/ `--mode download`（opt-in）/ `--mode both`（学习+归档）
- **studio skill 新增 H5 / H6**：H5（mode 不明确时根据语境关键词询问）/ H6（record 模式但未指定输出路径时提议默认路径）
- **learn skill 新增标志**：`--with-download`（默认 record 之外同时下载，等同子调度 `mode=both`）/ `--download-only`（跳过 record 仅下载，等同 `mode=download`，v2.0 兼容）
- **studio / learn description 关键词扩展**：`metadata only` / `record_artifact_metadata` / `online reference` / `no download` / `online only` / `全在线模式` / `不下载`

### Changed

- **studio skill SKILL.md Phase 4 重写**：原"Download & Rename"改为"Output Capture"，含 Step 4.0 重命名（通用） + Step 4a/4b/4c 三模式分支；workflow dot 图新增 P4_R / P4_D / P4_B 三节点
- **studio skill Quick Start 表新增三行 v2.1 触发**：「只要 metadata」/「既要 metadata 也要本地」/「必须本地有二进制」
- **studio skill Examples 新增**：示例 1b（三版 both）/ 示例 6（v2.1 record 单制品）/ 示例 7（v2.1 download 显式离线）
- **learn skill Phase 2-6 调度参数加 mode 字段**：默认 record，从 learn 启动参数透传
- **learn skill Gate 2/3/4 文案**：审定对象由「本地文件」改为「NotebookLM 在线制品」（artifact 完成 ≠ 必须本地化）
- **learn skill Phase 6 quiz/flashcards 输出说明**：默认 record markdown 含 NotebookLM URL 用于在线答题；`--with-download` 时本地存 JSON 便于做题工具加载
- **learn skill Handoff 输出**：按 mode 分形态展示 record / both / download 输出物
- **learn skill 示例**：示例 1 改为 v2.1 默认 record；新增示例 1b（--with-download）
- **`mj-nlm-shared/artifact-type-reference.md`**：顶部加 v2.1 默认行为变更说明；新增「v2.1 输出模式（record / download / both）」段（含 record mode 与 9 类 artifact_type 关系矩阵）
- **CLAUDE.md**：v2.1 升级要点段；6 skill 表标 v2.1 升级；shared 文件计数 7 → 8；skill 调用约定新增 record mode 默认条目
- **README.md**：v2.1 顶引；6 命令表更新；新增「v2.1 核心新概念」段（默认 record / 三模式 / 与 learning 子系统对齐）；自然语言触发段加 metadata only / both 触发词；roadmap 标 v2.1 完成
- **plugin.json**：version 2.0.1 → 2.1.0；description 加 v2.1 默认行为说明；keywords 新增 `metadata-only` / `online-reference` / `record-mode`

### Breaking Changes（仅 workflow 与默认值层，不动 MCP 接口）

- **studio Phase 4 默认输出从 binary 改为 record markdown**——v2.0 用户脚本若依赖 `nlm-artifacts/<file>.<ext>` 路径下的二进制，需显式加 `--mode download` 或迁到 `--mode both`
- **learn 默认走 record**——v2.0 学习闭环用户的本地 mp3/mp4/pdf 不再自动产生；如需保留旧行为加 `--with-download` 或 `--download-only`
- 不影响：MCP 接口（download_artifact / studio_create / studio_status 调用方式与签名均不变）；现有 v2.0 录制的文件路径；focus prompt 模板与 view 子参数

### Migration（v2.0 → v2.1）

- **保留 v2.0 行为**：单步 `/mj-nlm:studio` 调用加 `--mode download`；编排器 `/mj-nlm:learn` 加 `--download-only` 或 `--with-download`（推荐后者，留下 record 沉淀）
- **采纳 v2.1 默认**：直接执行不带 mode 的命令；首次执行时按 H6 提示提供 record 输出路径（建议 mj-system / mj-agent 项目用 `learning/<topic>/_nlm/`）
- **历史 artifact 补录 record markdown**：v2.1 不提供独立 skill；如频繁补录，按 `artifact-metadata-template.md` 手动填一份；v2.x 路线图考虑加 mj-nlm-record skill
- **NLM artifact-level URL 调研**：v2.1 采用回退方案 B（`artifact_url` 与 `notebook_url` 同值，body 内含「在 notebook 内定位本制品」段）；v2.2 路线图含 NLM API 能力调研，若上游暴露 artifact 直链则 record 模板自动升级

### Known Issues / Roadmap

- v2.1 NotebookLM artifact-level URL 暂回退方案 B（仅 notebook_url），若官方后续暴露则 v2.2 自动升级 record 模板
- v2.1 不提供 mj-nlm-record 独立 skill；历史 artifact 补录需按模板手动填；v2.x 视使用频率决定是否加
- v2.1 record markdown 路径默认提示 `learning/<topic>/_nlm/`，依赖用户 vault 已有该层级；mj-system / mj-agent learning 子系统 Phase 0 落地后此默认路径自动可用

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
