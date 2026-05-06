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
| `agent` | MJ-AgentLab 项目（Agent / LangGraph / MCP 服务） | `MJ-agent-agent-EmailAgent-20260505` |
| `multi` | 跨项目对齐 | `MJ-multi-cross-architecture-20260505` |
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

| scope | 说明 | 适用 |
|---|---|---|
| `agent` | 单 Agent | 聚焦一个 Agent 的实现、提示词、工具集 |
| `tool` | 工具 / MCP | Agent 调用的 tool 或 MCP server |
| `workflow` | 工作流 / LangGraph | 多 Agent / 多 tool 编排的工作流 |
| `cross` | 全局 / 跨域 | Agent 框架、共享 prompt、跨 Agent 设计 |

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

### project=agent（v2 新增，待用户提供 mj-agent 真实目录后定稿）

> ⚠️ 以下路径为**占位符默认值**，基于通用 Agent / LangGraph 项目布局推测。实际使用前需用户提供 mj-agent 仓库目录树确认或修正。修正方式：直接更新本文件相应小节。

#### agent + agent（单 Agent）

候选扫描目录：
- `agents/{AgentName}/` — Agent 主目录（含 prompt.py / tools.py / config.yaml 等）
- `docs/agents/{AgentName}/` — Agent 设计文档
- `prompts/{AgentName}/` — 独立 prompt 文件（如有）
- `evals/{AgentName}/` — Agent 评测集（如有）

#### agent + tool（工具 / MCP）

候选扫描目录：
- `tools/{ToolName}/` — tool 实现
- `mcp/{ToolName}/` — MCP server 定义（如有）
- `docs/tools/{ToolName}/`
- `.mcp.json`（如位于根）

#### agent + workflow（LangGraph / 编排）

候选扫描目录：
- `workflows/{WorkflowName}/` 或 `langgraph/{WorkflowName}/`
- `docs/workflows/{WorkflowName}/`
- `graphs/{WorkflowName}/`（如使用此命名）

#### agent + cross（全局）

候选扫描目录：
- `docs/`
- `CLAUDE.md`
- `prompts/shared/`
- `agents/_base/` 或 `agents/_shared/`（基类、共享逻辑）

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
- 服务名 / Agent 名可用缩写：`DQV`、`AEC`、`QVL`、`QCM`、`EmailAgent`、`PlannerAgent`

**示例**：`DQV`、`collection-pipeline`、`ops-etl`、`api-architecture`、`EmailAgent`、`langgraph-orchestration`、`mcp-tools`

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
| `Agent`（v2 新增） | Agent prompt / config | `06-Agent-EmailAgent提示词` |
| `工具`（v2 新增） | tool / MCP 实现 | `09-工具-EmailFetchTool` |
| `工作流`（v2 新增） | LangGraph / 编排 | `04-工作流-邮件分类管道` |

### 序号规则（v2 扩展）

- `00a` / `00b` 保留给原元知识 source（导航大纲 / 项目上下文）
- `00c` **v2 新增**，保留给领域定向报告（每个 notebook 一份）
- `00d` **v2 新增**，保留给来源充足性预检报告
- `00e`-`00z` 预留未来元 source 扩展
- 内容 source 从 `01` 开始，按导入顺序递增
- 同类别文件序号连续（如架构 01-04，代码 05-09）
- `99` **v2 新增**，保留给 Note 类元数据（理解度仪表盘等，不作为 Source 入库）
- 建议排列：`导航 → 定向 → 预检 → 架构 → 接口 → 代码 → Agent → 工具 → 工作流 → 数据库 → 配置 → 规范 → 测试 → 技能 → 运维 → 自检`

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
| **v2 新增** | `learn-loop` | 标记此 notebook 走过完整 /mj-nlm:learn 闭环 | 由 learn skill 自动添加 |
| **v2 新增** | `risk-class:{level}` | 风险等级（来自 risk-control-templates §3） | `high` / 默认无标 |

### 示例

**单模块 DQV（v1 兼容）**：
```
mj-system, system, mod, dqv, data-quality-validator, python, postgresql
```

**单 Agent（v2 新增）**：
```
mj-system, agent, agent, emailagent, email-agent, langgraph, mcp, 学习
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
