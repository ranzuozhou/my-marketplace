# Naming Reference v2 — NLM 技能家族命名规范

> v2 版本说明：v2 扩展双项目支持（mj-system + mj-agent）的 scope→扫描路径映射，新增元 source 编号约定（00c 定向 / 00d 预检 / 99 自检）。

## Notebook 命名规范

### 格式

```
MJ-{project}-{scope}-{topic}-{YYYYMMDD}
```

### project 可选值（v2）

| project | 说明 | 示例 |
|---|---|---|
| `system` | MJ System 主项目（数据处理与分析平台） | `MJ-system-mod-DQV-20260315` |
| `agent` | MJ-AgentLab 项目（LangChain 1.x + LangGraph，单 agent 单包结构） | `MJ-agent-code-mj_agent-20260506` |
| `multi` | 跨项目对齐 | `MJ-multi-cross-architecture-20260506` |
| `intel` | 情报系统（v1 沿用） | `MJ-intel-pipe-analysis-20260315` |

> v2 起 `agent` project 进入正式支持；`intel`/`multi` 沿用 v1 定义。

---

## scope 可选值（v2，按 project 区分）

### project=system（MJ System，沿用 v1）

| scope | 说明 | 适用 |
|---|---|---|
| `mod` | 单模块 | 聚焦一个服务的代码 + 设计文档 |
| `pipe` | 管道链路 | 多服务串联的数据流（收集 → 验证 → 分发） |
| `layer` | 数据层 | 数据仓库某一层（ODS → DWD ETL） |
| `cross` | 全局 / 跨域 | 项目架构、全局规范、跨服务设计 |

### project=agent（MJ-AgentLab，v2 新增）

mj-agent 是单 agent 单包项目（`src/mj_agent/` 一个包即一个 LangGraph agent），使用 dual-track 文档框架（Code-Side + Agent-Side）。scope 按内部组成切分：

| scope | 说明 | 适用 |
|---|---|---|
| `code` | 主代码包 | `src/mj_agent/` 整包（agent.py / config / llm / state / integrations） |
| `tool` | 单个 tool | `src/mj_agent/tools/{ToolName}/`，如 `tools/sql/{guardrail,execute,introspect}.py` |
| `skill` | 单个 SKILL.md（Track B） | `src/mj_agent/skills/{SkillName}/SKILL.md` 及关联资源 |
| `prompt` | Prompt 资产（Track B） | `src/mj_agent/prompts/`（含 `system.md`） |
| `docs` | Track A 文档 | `docs/{adr,rule,infrastructure,assessments}/` 单选或组合 |
| `cross` | 全局 / 跨 track | `CLAUDE.md` + `pyproject.toml` + `langgraph.json` + `plans/` + `.env.example` + 双 track 概览 |

### project=multi（跨项目）

只支持 `cross` scope，用于 system + agent 联合知识库。

---

## Scope → 默认扫描范围映射

### project=system

#### system + mod

- `src/{NodeType}/{Service}/` — 服务源代码
- `docs/design/{Service}/` — 服务设计文档
- `.claude/skills/mj-{相关 skill}/` — 相关技能
- `sql/` 中按服务缩写 grep 相关文件

NodeType 判断（按 main.py 注册或 CLAUDE.md 中的 Active Services 表）：

| 服务 | NodeType | 路径 |
|---|---|---|
| AutoEmailCollector | CollectionNodes | `src/CollectionNodes/AutoEmailCollector/` |
| DataQualityValidator | CollectionNodes | `src/CollectionNodes/DataQualityValidator/` |
| QueryVolumeLoader | ProcessingNodes | `src/ProcessingNodes/QueryVolumeLoader/` |
| StageAreaCleaner | CollectionNodes | `src/CollectionNodes/StageAreaCleaner/` |
| QueryCommonMetrics | ComputationNodes | `src/ComputationNodes/QueryCommonMetrics/` |
| FileCleaner | SysToolkit | `components/SysToolkit/` |

#### system + pipe

- `src/` 涉及的多个模块目录
- `sql/` 相关层与域脚本
- `docs/design/` 涉及的多个服务目录
- `.claude/skills/mj-{相关 skill}/`

常见管道：
- 数据收集管道：AEC → DQV → QVL
- 指标计算管道：QVL → QCM

#### system + layer

- `sql/{层号}-{域}/` — 数据层 SQL
- `docs/infrastructure/database/` — 数据库架构文档
- `.claude/skills/mj-etl-*/`

层号对应：
- `00-global/` — 全局（数据库、扩展、Schema）
- `10-ops/` — 运维追踪域
- `20-biz/` — 业务指标域

#### system + cross

- `docs/` — 全部
- `CLAUDE.md`
- `components/` — 共享组件
- `.claude/skills/`（全量）
- 用户指定额外目录

---

### project=agent（v2，依据 mj-agent develop 实际目录）

> mj-agent 是单 agent 单包项目（LangChain 1.x + LangGraph 1.1.8 + Python 3.13），主入口 `langgraph.json` → `src/mj_agent/agent.py:make_graph()`。文档分两 track（详见 `docs/rule/[STANDARD]_MJ_Agent_Documentation_Meta_Framework_v2.0.md`）。

#### agent + code（主代码包）

扫描目录：
- `src/mj_agent/` — 主包（含 `agent.py` / `config.py` / `llm.py` / `state.py`）
- `src/mj_agent/integrations/` — 基础设施（如 `mj_system_db.py`）
- `src/mj_agent/tools/` — 全部 tool 子目录（含 `tools/sql/`）
- `langgraph.json` — LangGraph Studio 入口
- `pyproject.toml` — 依赖与 ruff/pytest 配置
- `tests/unit/` — 单元测试（按需，规模大时 H4b）

> code scope 默认包含 prompts/ 与 skills/ 子目录的元数据，但不深入它们的全文（细节走 `prompt` / `skill` scope）。

#### agent + tool（单个 tool）

扫描目录：
- `src/mj_agent/tools/{ToolName}/` 或 `src/mj_agent/tools/{tool_module}.py`
- `src/mj_agent/tools/__init__.py` — `ALL_TOOLS` 注册
- 相关测试 `tests/unit/tools/{ToolName}/`（如有）
- 相关 ADR：`docs/adr/[ADR]_*_{tool 主题}.md`（如 ADR-006 数据边界）

> 当前已存在的 tool 子集：`tools/sql/{guardrail,execute,introspect}.py`，三件套各自独立 source 或合并一个 notebook。

#### agent + skill（Track B SKILL.md）

扫描目录：
- `src/mj_agent/skills/{SkillName}/` — SKILL.md 与子文档
- `src/mj_agent/skills/{SkillName}/SKILL.md` — 主文档（loader 会 strip frontmatter）
- 相关 EVAL：`docs/.../EVAL/{SkillName}/`（Phase 2 起强制）
- 相关 PROMPT 引用：`src/mj_agent/prompts/<相关>.md`（如本 skill 引用）

#### agent + prompt（Track B PROMPT 资产）

扫描目录：
- `src/mj_agent/prompts/system.md` — 系统提示
- `src/mj_agent/prompts/*.md` — 其他 prompt（按命名取）
- 相关 EVAL：`docs/.../EVAL/{prompt_name}/`
- `docs/rule/[STANDARD]_MJ_Agent_Agent_Side_Documentation_Framework_v1.0.md` — Track B 规范

#### agent + docs（Track A 文档）

扫描目录（按用户聚焦点选择子集）：
- `docs/INDEX.md` — 文档入口
- `docs/adr/` — 决策记录（已有 ADR-000..011）
- `docs/rule/` — STANDARD 文档（Meta_Framework / Code-Side / Agent-Side / Markdown / Commit Convention）
- `docs/infrastructure/` — 基础设施 GUIDE（如 `git/`）
- `docs/assessments/` — ASSESSMENT 文档
- `docs/_templates/` — TEMPLATE_{ADR,SKILL,PROMPT,CONTRACT}.md（参考用，可不导入）
- `docs/archive/` — 已归档（不导入，除非主题明确针对历史）

> Track A 与 Track B 的文档边界详见 `docs/adr/[ADR]_012_Two_Track_Documentation_Governance.md`。

#### agent + cross（全局 / 跨 track）

扫描目录：
- `CLAUDE.md` — 项目主指南（双 track 元规则）
- `README.md`
- `pyproject.toml` — 依赖、scope 别名、pytest/ruff 配置
- `langgraph.json` — 编排入口
- `.env.example` — 环境变量约定
- `plans/` — roadmap（如 `mj-agent-roadmap-v1.6.md`）
- `config/README.md` — secrets 管理（不导入 `secrets.enc`）
- `.github/workflows/` — CI 配置（如有需要）

---

### project=multi + cross

- mj-system 的 `docs/`
- mj-agent 的 `docs/`
- 跨项目对齐文档（如 `docs/cross/`）
- 用户指定额外目录

---

## topic 命名规则

- kebab-case（小写 + 连字符）
- 简洁描述核心主题，1-3 单词
- 服务名 / Agent 模块名可用缩写：`DQV`、`AEC`、`QVL`、`QCM`、`mj_agent`、`sql-tool`、`introspect`

**示例**：`DQV`、`collection-pipeline`、`ops-etl`、`api-architecture`、`mj_agent`、`sql-introspect`、`sql-guardrail`、`system-prompt`、`adr-suite`、`code-side-framework`

---

## Source 命名规范

### 格式

```
[序号]-[类别标签]-[描述]
```

### 类别标签（v2 扩展）

| 标签 | 适用文件类型 | 示例 |
|---|---|---|
| `导航` | 元 source（从 Note 转换的导航大纲与项目上下文） | `00a-导航-内容导航大纲` |
| `定向` | 元 source（领域定向报告，**v2 新增**） | `00c-定向-DQV领域定向报告` |
| `预检` | 元 source（来源充足性预检报告，**v2 新增**） | `00d-预检-来源充足性报告` |
| `自检` | Note（理解度仪表盘，**v2 新增**，仅 Note 不转 Source） | `99-自检-理解度仪表盘-20260505` |
| `架构` | SPEC / GUIDE / ADR / 架构图 | `01-架构-DQV技术规范` |
| `代码` | .py 源代码 | `05-代码-validation_service` |
| `数据库` | .sql 脚本 | `08-数据库-dqv_etl_functions` |
| `配置` | .yaml / .toml / .json 配置 | `10-配置-db_config` |
| `规范` | STANDARD 类文档 | `12-规范-命名规范` |
| `测试` | test 相关文件 | `14-测试-DQV集成测试` |
| `接口` | API 文档 / router 定义 | `03-接口-router定义` |
| `技能` | SKILL.md 及支撑文件 | `15-技能-mj-doc-author` |
| `运维` | RUNBOOK / 部署 / CI/CD | `16-运维-Docker部署手册` |
| `Agent核心`（v2 新增） | mj-agent 主代码（agent.py / config.py / state.py / llm.py） | `02-Agent核心-make_graph` |
| `工具`（v2 新增） | tool 实现（如 `tools/sql/{guardrail,execute,introspect}.py`） | `09-工具-sql_introspect` |
| `Skill`（v2 新增） | Track B SKILL.md 及子文档 | `06-Skill-sql-explorer` |
| `Prompt`（v2 新增） | Track B PROMPT 资产（含 system.md） | `07-Prompt-system_v3` |
| `集成`（v2 新增） | integrations/（外部系统对接，如 mj_system_db.py） | `11-集成-mj_system_db` |

### 序号规则（v2 扩展）

- `00a` / `00b` 保留给原元知识 source（导航大纲 / 项目上下文）
- `00c` **v2 新增**，保留给领域定向报告（每个 notebook 一份）
- `00d` **v2 新增**，保留给来源充足性预检报告
- `00e`-`00z` 预留未来元 source 扩展
- 内容 source 从 `01` 开始，按导入顺序递增
- 同类别文件序号连续（如架构 01-04，代码 05-09）
- `99` **v2 新增**，保留给 Note 类元数据（理解度仪表盘等，不作为 Source 入库）
- 建议排列：`导航 → 定向 → 预检 → 架构 → 接口 → 代码 → Agent核心 → 工具 → Skill → Prompt → 集成 → 数据库 → 配置 → 规范 → 测试 → 技能 → 运维 → 自检`

---

## Tag 命名规范

### 标签体系（v2 扩展）

| 类型 | 标签 | 说明 | 要求 |
|---|---|---|---|
| **必选** | `mj-system` | 组织标识（MJ-AgentLab） | 所有 notebook 必须 |
| **必选** | `{project}` | 项目域 | `system` / `agent` / `multi` / `intel` |
| **必选** | `{scope}` | 范围类型 | 按 project 取对应 scope 集 |
| **推荐** | `{topic}` | 主题（小写） | 如 `dqv`、`emailagent` |
| **推荐** | `{service或agent全名}` | 涉及实体全名 | 如 `data-quality-validator`、`email-agent` |
| **可选** | `{purpose}` | 用途 | 如 `培训`、`架构评审`、`知识沉淀`、**`学习`（v2）** |
| **可选** | `{技术栈}` | 技术标签 | 如 `python`、`postgresql`、`fastapi`、**`langgraph`、`mcp`（v2）** |
| **v2 新增** | `learn-loop` | 标记此 notebook 走过完整学习闭环（v2.3 起：`/mj-nlm:learn-make` + `/mj-nlm:learn-test` 串联） | 由 wrapper skill 自动添加 |
| **v2 新增** | `risk-class:{level}` | 风险等级（来自 risk-control-templates §3） | `high` / 默认无标 |

### 示例

**单模块 DQV（v1 兼容）**：
```
mj-system, system, mod, dqv, data-quality-validator, python, postgresql
```

**Agent 主代码包（v2 新增）**：
```
mj-system, agent, code, mj_agent, langchain, langgraph, python, 学习
```

**Agent 单 tool（v2 新增）**：
```
mj-system, agent, tool, sql-introspect, 数据边界, postgresql, 学习
```

**Agent Track A 文档（v2 新增）**：
```
mj-system, agent, docs, dual-track-framework, adr-suite, 架构评审
```

**跨项目对齐（v2 新增）**：
```
mj-system, multi, cross, agent-system-bridge, 架构评审, learn-loop
```

**经过 learn 闭环 + 高风险**：
```
mj-system, system, cross, security-architecture, learn-loop, risk-class:high
```

---

## 元 Source 编号速查

```
00a-导航-内容导航大纲          ← Phase 4 创建（v1 v2 通用）
00b-导航-项目上下文            ← Phase 4 创建（v1 v2 通用）
00c-定向-{topic}领域定向报告   ← Phase 7 创建（v2 新增）
00d-预检-来源充足性报告        ← Phase 6 创建（v2 新增）
01..N-{类别}-{描述}            ← 内容 Source（v1 v2 通用）

99-自检-理解度仪表盘-{YYYYMMDD}  ← Note 形式（v2 新增，不入 Source）
```

排序约定：在 NLM UI 上元 source 自动排在最前（按字典序），便于人工检索。
