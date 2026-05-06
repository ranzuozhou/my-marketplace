# CLAUDE.md — mj-nlm Plugin

## Plugin 概述

mj-nlm 是 MJ-AgentLab 组织（覆盖 mj-system 与 mj-agent 两个子项目）的 NotebookLM 学习闭环技能家族 Plugin。**v2.0 升级要点**：从「被动产出制品」重构为「学习闭环」（依据方法论文档），新增 1 个 orchestrator skill、3 份共享 prompt 模板与一套理解度量化指标。

## 6 个 Skill

| Skill | 命令 | 职责 | v 版本 |
|---|---|---|---|
| **auth** | `/mj-nlm:auth` | NLM 认证生命周期（登录、刷新、切换、排障） | v1（不动） |
| **build** | `/mj-nlm:build` | 知识库创建（扫描 → 导入 → 打标签 → 来源充足性预检 → 领域定向报告） | **v2 升级**（新增 P6/P7、双项目支持） |
| **manage** | `/mj-nlm:manage` | 知识库 CRUD + 分享 | v1（不动） |
| **query** | `/mj-nlm:query` | 知识问答（Single / Cross / Deep Research / Quiz Root Cause / Source Check / Self-Check） | **v2 升级**（新增 Mode D/E/F） |
| **studio** | `/mj-nlm:studio` | Studio 制品生成（9 种类型 × 4 view 视角 + 默认幻觉防护） | **v2 升级**（学习导向 prompt + 三版 + guardrails） |
| **learn** | `/mj-nlm:learn` | 学习闭环编排器（10 Phase + 5 Gate 一站式调度） | **v2 新增** |

## 双项目支持（v2 新增）

| project | 说明 | 命名示例 |
|---|---|---|
| `system` | MJ System 主项目 | `MJ-system-mod-DQV-20260506` |
| `agent` | MJ-AgentLab 项目 | `MJ-agent-code-mj_agent-20260506` |
| `multi` | 跨项目对齐 | `MJ-multi-cross-architecture-20260506` |
| `intel` | 情报系统（v1 沿用） | `MJ-intel-pipe-analysis-20260506` |

scope 按 project 区分（详见 `skills/mj-nlm-shared/naming-reference.md`）。

## MCP 依赖

本 plugin 通过 `.mcp.json` 自动注册 `notebooklm-mcp` MCP server。

**前置安装**（一次性）：
```bash
uv tool install notebooklm-mcp-cli --with socksio --force
nlm login
```

## Skill 调用约定

- 所有 skill 遵循 Phase 式工作流（Phase 0 认证检查 → 业务 Phase）
- 认证失败统一引导到 `/mj-nlm:auth`
- 破坏性操作（delete）需用户二次确认（`confirm=True`）
- v2 起所有 studio_create 默认追加幻觉防护约束句（可 `disable_guardrails=True` 关闭，但 `risk-class:high` tag 强制开）
- 共享参考资源位于 `skills/mj-nlm-shared/` 目录

## 文件结构

```
skills/
├── mj-nlm-auth/       # 认证技能 + troubleshooting 手册（v1）
├── mj-nlm-build/      # 知识库创建（v2，含 P6/P7）
├── mj-nlm-manage/     # 生命周期管理（v1）
├── mj-nlm-query/      # 知识问答（v2，6 种 Mode）
├── mj-nlm-studio/     # Studio 制品（v2，含 view + guardrails）
├── mj-nlm-learn/      # 学习闭环编排器（v2 新增）
└── mj-nlm-shared/     # 共享参考资源（7 份）
    ├── naming-reference.md          # 双项目 scope→路径映射 + 元 source 编号
    ├── material-classification.md   # 三分法 + 多源类型分类
    ├── artifact-type-reference.md   # 9 种 artifact_type + v2 横切子参数
    ├── focus-prompt-templates.md    # 学习导向 Intent Layer 模板（v2 重写）
    ├── risk-control-templates.md    # 来源/制品配比 + 幻觉防护约束（v2 新增）
    ├── learning-loop-templates.md   # 7 个 prompt 模板（领域定向/三版/错题/案例/核查/术语/自检，v2 新增）
    └── understanding-metrics.md     # 7 项理解度量化指标（v2 新增）
```

## 元 Source 编号约定（v2）

```
00a-导航-内容导航大纲          ← build Phase 4 创建
00b-导航-项目上下文            ← build Phase 4 创建
00c-定向-{topic}领域定向报告   ← build Phase 7 创建（v2 新增）
00d-预检-来源充足性报告        ← build Phase 6 创建（v2 新增）
01..N-{类别}-{描述}            ← 内容 Source

99-自检-理解度仪表盘-{YYYYMMDD}-{HHMM}  ← query Mode F 创建（仅 Note，不入 Source，v2 新增）
```
