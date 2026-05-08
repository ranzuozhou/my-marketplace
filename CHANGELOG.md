# Changelog

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [1.9.1] - 2026-05-08

### Highlights

mj-nlm v2.4.1 patch — 诚实化 v2.4 cache 描述。调研 `notebooklm-mcp-cli` v0.6.5 源码后确认：v2.4 SKILL.md 与 preflight-checklist.md 写的"5min TTL 缓存 + 内存级 dict"实际是 Claude conversation 自然 memory，不是技术 cache。本 patch 重写相关段落 + 沉淀 v2.5 候选 abandoned 决策依据。

### Versions

| Plugin | Version | 变更 |
|---|---|---|
| my-marketplace | **1.9.0 → 1.9.1** | mj-nlm patch bump |
| **mj-nlm** | **2.4.0 → 2.4.1** | **patch**：cache 描述诚实化 + v2.5 候选 abandoned 沉淀 |
| mp-git | 1.1.0 | 无变更 |
| mp-dev | 1.0.0 | 无变更 |
| flora-ptm | 1.0.0 | 无变更 |
| mj-drawio | 0.1.0 | 无变更 |

### Changed — mj-nlm v2.4.0 → v2.4.1

- **mj-nlm-shared/preflight-checklist.md §缓存策略** 重写：v2.4.1 诚实化段含实际机制（同 turn LLM memory / 跨 turn 重跑）+ 单调用真实开销表 + v2.5 候选 abandoned 4 条决策依据
- **build / manage / studio / query** 4 个 skill Phase 0 缓存段统一改为引述 preflight-checklist §缓存策略
- 删除 `--force-recheck` flag 引用（从未实现）

### v2.5 Roadmap 更新（abandoned + 重排）

- ~~v2.5 候选：preflight 5min 缓存机制升级为真实现~~ → **abandoned**（v2.4.1 调研发现 ROI 低）
- v2.5 重命名为：NLM artifact-level URL 暴露调研（之前 v2.6 候选）
- 详见 `plugins/mj-nlm/CHANGELOG.md#[2.4.1]` § Roadmap 更新

## [1.9.0] - 2026-05-08

### Highlights

mj-nlm v2.4 minor bump — preflight 实施落地：把 v2.3 的 `mj-nlm-shared/preflight-checklist.md` 模板从文档级正式编入 6 个 skill（build / manage / query / studio 显式 Phase 0 + H-point；learn-make / learn-test wrapper 隐式 preflight 注解）。auth 不动。**非破坏性**；故障从 Phase 7 后移晚发现 → Phase 0 早发现。

### Versions

| Plugin | Version | 变更 |
|---|---|---|
| my-marketplace | **1.8.0 → 1.9.0** | mj-nlm minor bump |
| **mj-nlm** | **2.3.0 → 2.4.0** | **minor bump**：6 skill Phase 0 编入 preflight 实施 + shared 集成点状态更新 |
| mp-git | 1.1.0 | 无变更 |
| mp-dev | 1.0.0 | 无变更 |
| flora-ptm | 1.0.0 | 无变更 |
| mj-drawio | 0.1.0 | 无变更 |

### Changed — mj-nlm v2.3.0 → v2.4.0

- **build skill** Phase 0 由 "Auth Check" 替换为 "Preflight Check"（L1+L2 + H0a/b/c + 5min 缓存）；workflow dot graph P0/H1 标签同步
- **manage / studio / query** 3 个 skill 各插入新 Phase 0 Preflight Check 段（L1+L2，L3 隐式由 Phase 1 首次 MCP 覆盖）
- **learn-make / learn-test** 2 wrapper Phase 0 头部加 v2.4 隐式 Preflight 引述（委托子 skill 完整 preflight）
- **shared/preflight-checklist.md** 集成点段加"v2.4 实施状态"列，6 skill 全部标 ✅
- 详见 `plugins/mj-nlm/CHANGELOG.md#[2.4.0]`

## [1.8.0] - 2026-05-08

### Highlights

mj-nlm v2.3 minor bump — deprecation removal + preflight & quota 共享规范：完成 v2.2 forward-announce 的 `/mj-nlm:learn` skill 移除；新增 `mj-nlm-shared/preflight-checklist.md` + `mj-nlm-shared/quota-estimation.md` 两份共享规范，把 NLM 启动冒烟检查（auth / MCP / notebook scope）和耗时配额预告（双 wrapper + 底层 skill）前移到 Phase 0，缓解 v2.0/v2.1 学习闭环卡 Phase 7 的根因 + 用户对耗时无预期 两个 UX 痛点。**轻量 BREAKING（已经过 v2.2 ~2 周公告期）**。

### Versions

| Plugin | Version | 变更 |
|---|---|---|
| my-marketplace | **1.7.0 → 1.8.0** | mj-nlm minor bump |
| **mj-nlm** | **2.2.0 → 2.3.0** | **minor bump**：删除 deprecated learn skill + 2 新 shared 文档（preflight + quota） |
| mp-git | 1.1.0 | 无变更 |
| mp-dev | 1.0.0 | 无变更 |
| flora-ptm | 1.0.0 | 无变更 |
| mj-drawio | 0.1.0 | 无变更 |

### Changed — mj-nlm v2.2.0 → v2.3.0

- **删除 `mj-nlm-learn/` skill**（v2.2 forward-announce 完成）；所有调用改用 `/mj-nlm:learn-make` + `/mj-nlm:learn-test` 串联
- **新增 2 shared 文档**：`mj-nlm-shared/preflight-checklist.md`（启动冒烟三级 checklist + 5min 缓存）+ `mj-nlm-shared/quota-estimation.md`（单调用基线 + 双 wrapper 配额预告 + NLM 配额上限）
- **risk-control-templates.md §6** 抽出 → quota-estimation.md（保留单行 stub）
- **build / studio / query / learn-make / learn-test / 2 shared docs** 内全部 `/mj-nlm:learn` 引用改为 wrapper 双命令
- **plugin.json / marketplace.json description** 同步删除 `learn[deprecated]` 标识，加 v2.3 preflight/quota 说明；keywords +`preflight` / `quota-estimation`
- **CLAUDE.md / README.md**：v2.3 升级要点段；8 skill → 7 skill 表；shared 8 → 10 份；roadmap v2.3 ✅；v2.4-v2.6 重排

详见 `plugins/mj-nlm/CHANGELOG.md#[2.3.0]`。

## [1.7.0] - 2026-05-08

### Highlights

mj-nlm v2.2 minor bump — 高层入口整合：新增 `/mj-nlm:learn-make`（生成学习资料）+ `/mj-nlm:learn-test`（生成考察资料）两个 high-level wrapper；旧 `/mj-nlm:learn` 标 deprecated（v2.3 删除）。用户对外只需记 2 个命令，底层 6 skill 仍可独立调用。**非破坏性 UX 优化**。

### Versions

| Plugin | Version | 变更 |
|---|---|---|
| my-marketplace | **1.6.0 → 1.7.0** | mj-nlm minor bump |
| **mj-nlm** | **2.1.0 → 2.2.0** | **minor bump**：2 新 wrapper skill (learn-make / learn-test) + learn deprecated + 元数据同步 |
| mp-git | 1.1.0 | 无变更 |
| mp-dev | 1.0.0 | 无变更 |
| flora-ptm | 1.0.0 | 无变更 |
| mj-drawio | 0.1.0 | 无变更 |

### Changed — mj-nlm v2.1.0 → v2.2.0

- **新增 2 wrapper skill**：
  - `mj-nlm-learn-make`：编排 build + studio 上游 7 类制品（mind_map/video/slide/audio/report/infographic/data_table），4 Phase + 4 H-points；启动标志 `<topic>` / `--resume` / `--triple-view` / `--with-download` / `--download-only`
  - `mj-nlm-learn-test`：编排 studio quiz/flashcards + 可选 query Mode D/E/F，3 Phase（含 4 子分支）+ 5 H-points；启动标志 `<nb_id>` / `--full` / `--rootcause` / `--selfcheck` / `--sourcecheck`
- **mj-nlm-learn 标 deprecated**：frontmatter `[DEPRECATED v2.2]` 前缀；body 顶加完整 Phase 对照迁移段；保留至 v2.3 删除
- **plugin.json**：2.1.0 → 2.2.0；description 加 v2.2 高层入口；keywords +`learn-orchestration` / `high-level-wrapper` / `learn-make` / `learn-test`
- **CLAUDE.md / README.md**：6 skill 表 → 8 skill 表（拆 high-level wrapper + 底层）；新增 v2.2 升级要点段；自然语言触发段加 wrapper 触发词

详见 `plugins/mj-nlm/CHANGELOG.md#[2.2.0]`。

### Deprecated

- mj-nlm `/mj-nlm:learn` skill — v2.3 计划删除（约 2-3 周观察期），由 wrapper 1+2 串联替代

### Migration

| v2.1 入口 | v2.2 替代 |
|---|---|
| `/mj-nlm:learn <topic>` | `/mj-nlm:learn-make <topic>` → `/mj-nlm:learn-test <nb_id>` |
| `/mj-nlm:learn --triple-view` | `/mj-nlm:learn-make --triple-view` |
| `/mj-nlm:learn --with-download` | `/mj-nlm:learn-make --with-download` |
| `/mj-nlm:learn --resume <nb_id>` | `/mj-nlm:learn-make --resume <nb_id>`（共享 `learn-phase:G{N}-passed` tag） |
| `/mj-nlm:learn --quiz-only` | `/mj-nlm:learn-test <nb_id>`（默认即等价） |

底层 `/mj-nlm:auth` / `/mj-nlm:build` / `/mj-nlm:manage` / `/mj-nlm:query` / `/mj-nlm:studio` 完全不动，独立可调路径全保留。

## [1.6.0] - 2026-05-08

### Highlights

mj-nlm v2.1 minor bump — Studio Phase 4 与 learn 编排默认输出形态从 download 改为 record（元信息 markdown），对齐 learning 子系统约束。download 路径保留为显式 opt-in，向后兼容。

### Versions

| Plugin | Version | 变更 |
|---|---|---|
| my-marketplace | **1.5.1 → 1.6.0** | mj-nlm minor bump |
| **mj-nlm** | **2.0.1 → 2.1.0** | **minor bump**：默认 record mode + 元信息 markdown 模板 + learn --with-download / --download-only 标志 |
| mp-git | 1.1.0 | 无变更 |
| mp-dev | 1.0.0 | 无变更 |
| flora-ptm | 1.0.0 | 无变更 |
| mj-drawio | 0.1.0 | 无变更 |

### Changed — mj-nlm v2.0.1 → v2.1.0

- **studio Phase 4 三模式**：`--mode record`（默认）/ `--mode download`（opt-in）/ `--mode both`（学习+归档）；默认输出形态从二进制改为元信息 markdown
- **learn 默认 record + 两个新标志**：`--with-download`（默认 record 之外同时下载）/ `--download-only`（跳过 record 仅下载，v2.0 兼容）
- **新增共享模板** `mj-nlm-shared/artifact-metadata-template.md`：frontmatter schema + ≤ 50 行 body 范式 + 与 mj-system / mj-agent learning 子系统对齐说明
- **shared 文件计数** 7 → 8

详见 `plugins/mj-nlm/CHANGELOG.md#[2.1.0]`。

### Breaking Changes（仅默认值层，不动 MCP 接口）

- studio Phase 4 默认输出从 binary 改为 record markdown — v2.0 用户脚本若依赖 `nlm-artifacts/<file>.<ext>` 路径下的二进制，需显式加 `--mode download` 或迁到 `--mode both`
- learn 默认走 record — v2.0 学习闭环用户的本地 mp3/mp4/pdf 不再自动产生；保留旧行为用 `--with-download`

### Migration

- 沿用 v2.0 行为：`/mj-nlm:studio --mode download` 或 `/mj-nlm:learn --download-only` / `--with-download`
- 采纳 v2.1 默认：直接执行；按 H6 提示填 record 输出路径（mj-system / mj-agent 项目建议 `learning/<topic>/_nlm/`）
- MCP 接口与现有 v2.0 已下载的文件路径不变

## [1.5.1] - 2026-05-06

### Highlights

mj-nlm 大版本升级 + 路径定稿（含两次合并：PR #18 v2.0.0 学习闭环重构、PR #19 v2.0.1 mj-agent 6-scope 路径定稿）。

### Versions

| Plugin | Version | 变更 |
|---|---|---|
| my-marketplace | **1.4.1 → 1.5.1** | mj-nlm major bump |
| **mj-nlm** | **1.0.0 → 2.0.1** | **major bump**：学习闭环重构 + mj-agent 路径定稿 |
| mp-git | 1.1.0 | 无变更 |
| mp-dev | 1.0.0 | 无变更 |
| flora-ptm | 1.0.0 | 无变更 |
| mj-drawio | 0.1.0 | 无变更 |

### Changed — mj-nlm v1.0.0 → v2.0.0（PR #18）

从「被动产出制品」重构为「学习闭环」（依据 NotebookLM 多媒体学习方法论），覆盖范围扩展到 MJ-AgentLab 双子项目（mj-system + mj-agent）。

- **新增 skill**：`mj-nlm-learn`（top-level orchestrator，10 Phase + 5 Gate 一键调度 build/studio/query）
- **build 升级**：+Phase 6 来源充足性预检（输出 `00d-预检-` 元 source）+Phase 7 领域定向报告（输出 `00c-定向-` 元 source 作为学习地图锚）+双项目支持
- **studio 升级**：+三版生成（foundation / structural / challenge view 子参数）+默认幻觉防护约束（disable_guardrails 子参数）+focus-prompt 模板重写为学习导向
- **query 升级**：+Mode D 错题 root cause +Mode E 来源核查（5 级标注）+Mode F 7 项理解度自检（仪表盘 Note）
- **shared 升级**：3 新文件（risk-control-templates / learning-loop-templates / understanding-metrics）+4 改写/扩展（focus-prompt / naming / material-classification / artifact-type）

详见 `plugins/mj-nlm/CHANGELOG.md#[2.0.0]`。

### Fixed — mj-nlm v2.0.0 → v2.0.1（PR #19）

定稿 v2.0 留下的 mj-agent 路径占位符：依据 mj-agent develop 实际目录（单 agent 单包，LangChain 1.x + LangGraph 1.1.8），把 4 scope 占位（agent/tool/workflow/cross 配 `agents/<Name>/` 等假设路径）替换为方案 B 的 6 scope（code / tool / skill / prompt / docs / cross 配真实 `src/mj_agent/...` 路径）。

详见 `plugins/mj-nlm/CHANGELOG.md#[2.0.1]`。

### Breaking Changes

仅 workflow 与产物层，不动 MCP 接口：

- mj-nlm build 输出元 source 从 2 个增至 4 个（新增 `00c-定向-` `00d-预检-`）
- mj-nlm studio 默认追加幻觉防护约束句（`disable_guardrails=True` 关闭，但 `risk-class:high` tag 强制开启）
- mj-nlm v1 focus-prompt 模板保留为 `legacy_*` 别名（v2.3 弃用、v2.4 移除）

### Migration

- 现有 mj-nlm v1 notebook 的命名格式（`MJ-{project}-{scope}-{topic}-{YYYYMMDD}`）不变
- 旧 `MJ-agent-agent-*` 命名仍可用，但新 mj-agent notebook 应改用 v2.0.1 6-scope（如 `MJ-agent-tool-sql-introspect-20260506`）
- 现有 v1 `focus_prompt` 字符串调用不需修改即可继续工作（v2 默认在末尾追加约束句）

## [1.4.1] - 2026-04-21

### Added
- `.github/ISSUE_TEMPLATE/` 目录补齐:5 个 issue 模板(feature / bugfix / documentation / maintain / hotfix)+ `config.yml`(禁用空白 issue、Discussions 入口)。此前 `mp-git-issue` skill 声明读取这些模板但目录不存在

### Fixed
- `.github/PULL_REQUEST_TEMPLATE/*.md` 编码修复:6 个 PR 模板(feature / bugfix / documentation / maintain / hotfix / release)原为 GBK 双编码产生的 mojibake,已重写为正确 UTF-8 中文内容
- 根 README.md 插件数量/技能数量描述从 "4 个插件,23 个技能" 更正为 "5 个插件,27 个技能"(反映 v1.4.0 新增的 mj-drawio)

## [1.4.0] - 2026-04-20

### Added
- 新增插件: mj-drawio v0.1.0 — draw.io 图表生成与 mj-system 模板(Windows 专用),3 个 skill(create / export / template)+ 4 个预置模板 + XML 预校验脚本

## [1.3.0] - 2026-03-24

### Added
- mp-git: 新增 `mp-git-release` 技能 — 7 步交互式版本发布工作流
- mp-git: 新增 SPEC 设计文档 `docs/design/mp-git/[SPEC]_MP_Git_Release_Skill.md`

### Fixed
- `bump-version.ps1` plugin scope 补充 README.md 到目标文件列表

### Changed
- README.md 插件版本表更新

## [1.2.0] - 2026-03-20

### Added
- 新增 flora-ptm 插件：研究报告批量分析与多媒体转化（3 skills: digest, synthesize, produce）
- 项目级 Claude Code settings（permissions + enabledPlugins）

## [1.1.1] - 2026-03-18

### Changed
- README.md 优化：添加徽章、三级安装说明、使用示例、贡献指引

## [1.1.0] - 2026-03-18

### Added
- 新增 mp-git 插件：Marketplace Git 工作流（9 skills）
- 新增 mp-dev 插件：插件开发生命周期工具链（6 skills）
- 项目文档体系：CLAUDE.md、docs/ 目录（6 篇指南/手册）
- README.md 添加文档链接

## [1.0.0] - 2026-03-18

### Added
- 初始发布：1 个 Plugin（mj-nlm），5 个 Skill（auth, build, manage, query, studio）
- Plugin Marketplace 元数据结构（marketplace.json）
- 仓库基础设施：VERSION、CI/CD、PR 模板、开发者脚本
