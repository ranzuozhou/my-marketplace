# Naming Reference — NLM 技能家族命名规范

## Notebook 命名规范

### 格式

```
MJ-{project}-{scope}-{topic}-{YYYYMMDD}
```

### project 可选值

| project | 说明 | 示例 |
|---------|------|------|
| `system` | MJ System 主项目 | `MJ-system-mod-DQV-20260315` |
| `agent` | AgentLab 项目 | `MJ-agent-cross-architecture-20260315` |
| `intel` | 情报系统 | `MJ-intel-pipe-analysis-20260315` |
| `multi` | 跨项目 | `MJ-multi-cross-shared-infra-20260315` |

### scope 可选值

| scope | 说明 | 适用场景 |
|-------|------|---------|
| `mod` | 单模块 | 聚焦一个服务的代码 + 设计文档 |
| `pipe` | 管道链路 | 多服务串联的数据流（如收集→验证→分发） |
| `layer` | 数据层 | 数据仓库某一层（如 ODS→DWD ETL） |
| `cross` | 全局/跨域 | 项目架构、全局规范、跨服务设计 |

### topic 命名规则

- 使用 kebab-case（小写 + 连字符）
- 简洁描述核心主题，1-3 个单词
- 服务名可用缩写：`DQV`、`AEC`、`QVL`、`QCM`

**示例**：`DQV`、`collection-pipeline`、`ops-etl`、`api-architecture`、`全链路`

---

## Scope → 默认扫描范围映射

### mod（单模块）

扫描目录：
- `src/{NodeType}/{Service}/` — 服务源代码
- `docs/design/{Service}/` — 服务设计文档
- `.claude/skills/mj-{相关skill}/` — 相关技能定义
- `sql/` 中与该服务相关的文件（按服务缩写 grep）

**判断 NodeType**：根据 `main.py` 中的服务注册，或按 CLAUDE.md 中的 Active Services 表查找。

| 服务 | NodeType | 路径 |
|------|----------|------|
| AutoEmailCollector | CollectionNodes | `src/CollectionNodes/AutoEmailCollector/` |
| DataQualityValidator | CollectionNodes | `src/CollectionNodes/DataQualityValidator/` |
| QueryVolumeLoader | ProcessingNodes | `src/ProcessingNodes/QueryVolumeLoader/` |
| StageAreaCleaner | CollectionNodes | `src/CollectionNodes/StageAreaCleaner/` |
| QueryCommonMetrics | ComputationNodes | `src/ComputationNodes/QueryCommonMetrics/` |
| FileCleaner | SysToolkit | `components/SysToolkit/` |

### pipe（管道链路）

扫描目录：
- `src/` 涉及的多个模块目录
- `sql/` 相关层和域的脚本
- `docs/design/` 涉及的多个服务目录
- `.claude/skills/mj-{相关skill}/`

**常见管道**：
- 数据收集管道：AEC → DQV → QVL
- 指标计算管道：QVL → QCM

### layer（数据层）

扫描目录：
- `sql/{层号}-{域}/` — 数据层 SQL 脚本
- `docs/infrastructure/database/` — 数据库架构文档
- `.claude/skills/mj-etl-*/` — ETL 技能

**层号对应**：
- `00-global/` — 全局（数据库、扩展、Schema）
- `10-ops/` — 运维追踪域
- `20-biz/` — 业务指标域

### cross（全局/跨域）

扫描目录：
- `docs/` — 全部文档
- `CLAUDE.md` — 项目配置
- `components/` — 共享组件
- `.claude/skills/` — 全量技能定义
- 用户指定的额外目录

---

## Source 命名规范

### 格式

```
[序号]-[类别标签]-[描述]
```

### 类别标签

| 标签 | 适用文件类型 | 示例 |
|------|------------|------|
| `导航` | 元知识 Source（从 Note 转换） | `00a-导航-内容导航大纲` |
| `架构` | SPEC、GUIDE、ADR、架构图 | `01-架构-DQV技术规范` |
| `代码` | .py 源代码 | `05-代码-validation_service` |
| `数据库` | .sql 脚本 | `08-数据库-dqv_etl_functions` |
| `配置` | .yaml、.toml、.json 配置 | `10-配置-db_config` |
| `规范` | STANDARD 类文档 | `12-规范-命名规范` |
| `测试` | test 相关文件 | `14-测试-DQV集成测试` |
| `接口` | API 文档、router 定义 | `03-接口-router定义` |
| `技能` | SKILL.md 及支撑文件 | `15-技能-mj-doc-author` |
| `运维` | RUNBOOK、部署、CI/CD | `16-运维-Docker部署手册` |

### 序号规则

- `00a`-`00z` 保留给元知识 Source（导航类，从 Note 转换），排在所有内容 Source 之前
- 内容 Source 按导入顺序递增，从 `01` 开始
- 同类别文件序号连续（如架构类 01-04，代码类 05-09）
- 建议按 `导航 → 架构 → 接口 → 代码 → 数据库 → 配置 → 规范 → 测试 → 技能 → 运维` 排列

---

## Tag 命名规范

### 标签体系

| 类型 | 标签 | 说明 | 要求 |
|------|------|------|------|
| **必选** | `mj-system` | 项目标识 | 所有 notebook 必须 |
| **必选** | `{project}` | 项目域 | 如 `system`、`agent` |
| **必选** | `{scope}` | 范围类型 | 如 `mod`、`pipe`、`layer`、`cross` |
| **推荐** | `{topic}` | 主题 | 如 `dqv`、`etl`（小写） |
| **推荐** | `{service}` | 涉及服务全名 | 如 `data-quality-validator` |
| **可选** | `{purpose}` | 用途 | 如 `培训`、`架构评审`、`知识沉淀` |
| **可选** | `{技术栈}` | 技术标签 | 如 `python`、`postgresql`、`fastapi` |

### 示例

**单模块 DQV**：
```
mj-system, system, mod, dqv, data-quality-validator, python, postgresql
```

**跨管道知识库**：
```
mj-system, system, pipe, collection-pipeline, auto-email-collector, data-quality-validator, 培训
```

**全局架构**：
```
mj-system, system, cross, architecture, 架构评审
```
