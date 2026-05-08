# CLAUDE.md — mj-nlm Plugin

## Plugin 概述

mj-nlm 是 MJ-AgentLab 组织（覆盖 mj-system 与 mj-agent 两个子项目）的 NotebookLM 学习闭环技能家族 Plugin。

**v2.4.1 升级要点**（cache 描述诚实化 patch，**非破坏性**）：
- v2.4 SKILL.md 与 preflight-checklist.md 写的"5min TTL 缓存"实际是 Claude conversation 自然 memory，不是技术 cache
- 调研 `notebooklm-mcp-cli` v0.6.5 源码：`server_info` / `refresh_auth` 是 LOCAL check（毫秒级），`notebook_list` 是真网络（1-3 秒，但缓存它会让刚建/刚删 notebook 反映不准）
- v2.4.1 重写 5 处 cache 段为诚实描述（同 turn LLM memory / 跨 turn 重跑）；删除从未实现的 `--force-recheck` flag 引用
- ~~v2.5 候选~~ preflight 5min 缓存升级为真实现：**abandoned**（ROI 低）

**v2.4 升级要点**（preflight 实施落地，**非破坏性**）：
- v2.3 的 `mj-nlm-shared/preflight-checklist.md` 由文档级模板正式编入 6 个 skill 的 Phase 0 实施段：
  - `build` / `manage` / `query` / `studio` 4 底层 skill 显式 Phase 0 + H0a/b/c 段
  - `learn-make` / `learn-test` 2 wrapper Phase 0 加隐式 preflight 注解，委托子 skill 完整 preflight
- `auth` skill 不动（自身就是 troubleshooter）
- 仅文档结构改动，无 MCP 调用语义变更；用户体验上：故障从 Phase 7 后移晚发现 → Phase 0 早发现

**v2.3 升级要点**（deprecation removal + 启动规范，**轻量 BREAKING 已经过 v2.2 公告期**）：
- 删除 `/mj-nlm:learn` skill（v2.0 引入，v2.2 deprecated）；改用 `/mj-nlm:learn-make` + `/mj-nlm:learn-test` 串联
- 新增 2 份共享规范：
  - `mj-nlm-shared/preflight-checklist.md` — 三级启动冒烟（L1 Auth / L2 MCP health / L3 Notebook scope）
  - `mj-nlm-shared/quota-estimation.md` — 单调用基线 + 双 wrapper 配额预告（v2.0/v2.1 卡 Phase 7 的根因前移到 Phase 0）
- 共享文档总数 8 → 10；skill 总数 8 → 7

**v2.2 升级要点**（高层入口整合，**非破坏性**）：
- 新增 2 个 high-level wrapper skill：
  - `/mj-nlm:learn-make` — 生成学习资料（编排 build + studio 上游 7 类制品）
  - `/mj-nlm:learn-test` — 生成考察资料（编排 studio quiz/flashcards + 可选 query Mode D/E/F）
- 用户对外只需记 2 个 high-level 命令，底层 skill 仍可独立调用
- 命令形态：`/mj-nlm:learn-make <topic>` → `/mj-nlm:learn-test <notebook_id>`

**v2.1 升级要点**（默认行为变更，**非破坏性**）：
- studio Phase 4 默认输出**元信息 markdown**（record mode），而非 download 二进制；download 降级为 `--mode download` 显式 opt-in
- 新增共享模板 `mj-nlm-shared/artifact-metadata-template.md`（≤ 50 行 record 范式）
- learn skill Phase 8 / 编排默认走 record；显式 `--with-download` 才同时 download
- 对齐 mj-system / mj-agent learning 子系统约束：markdown 进 git，binary 永不入 git

**v2.0 升级要点**：从「被动产出制品」重构为「学习闭环」（依据方法论文档），新增 1 个 orchestrator skill、3 份共享 prompt 模板与一套理解度量化指标。

## 7 个 Skill（v2.3: 8 - 1 = 5 底层 + 2 high-level wrapper）

### High-level wrapper（v2.2 新增，对外推荐入口）

| Skill | 命令 | 职责 | v 版本 |
|---|---|---|---|
| **learn-make** | `/mj-nlm:learn-make` | **生成学习资料**：编排 build + studio 上游 7 类制品（mind_map/video/slide/audio/report/infographic/data_table） | v2.2 |
| **learn-test** | `/mj-nlm:learn-test` | **生成考察资料**：编排 studio quiz/flashcards + 可选 query Mode D（错题归因）/F（自检）/E（来源核查） | v2.2 |

### 底层 skill（独立可调用，wrapper 内部调度）

| Skill | 命令 | 职责 | v 版本 |
|---|---|---|---|
| **auth** | `/mj-nlm:auth` | NLM 认证生命周期（登录、刷新、切换、排障） | v1（不动） |
| **build** | `/mj-nlm:build` | 知识库创建（扫描 → 导入 → 打标签 → 来源充足性预检 → 领域定向报告） | v2 升级（新增 P6/P7、双项目支持） |
| **manage** | `/mj-nlm:manage` | 知识库 CRUD + 分享 | v1（不动） |
| **query** | `/mj-nlm:query` | 知识问答（Single / Cross / Deep Research / Quiz Root Cause / Source Check / Self-Check） | v2 升级（新增 Mode D/E/F） |
| **studio** | `/mj-nlm:studio` | Studio 制品生成（9 种类型 × 4 view 视角 + 默认幻觉防护 + v2.1 record/download/both 三模式） | v2.1（默认 record mode） |

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

- 所有 skill 遵循 Phase 式工作流（Phase 0 preflight → 业务 Phase）
- **v2.3 起 Phase 0 标准化为三级 preflight**（详见 `mj-nlm-shared/preflight-checklist.md`）：L1 Auth Token / L2 NLM Service Health / L3 Notebook scope（条件触发）
- 认证失败统一引导到 `/mj-nlm:auth`
- 破坏性操作（delete）需用户二次确认（`confirm=True`）
- v2 起所有 studio_create 默认追加幻觉防护约束句（可 `disable_guardrails=True` 关闭，但 `risk-class:high` tag 强制开）
- **v2.1 起 studio Phase 4 默认输出 record markdown**（`--mode record`），而非 download 二进制；download 与 both 为显式 opt-in
- **v2.2 起对外推荐入口为 `/mj-nlm:learn-make` + `/mj-nlm:learn-test` 两个 wrapper**；底层 5 skill 仍可独立调用（advanced 路径）
- **v2.3 起 preflight 通过后必须按 `mj-nlm-shared/quota-estimation.md` 模板告知用户预计耗时与配额消耗**
- 共享参考资源位于 `skills/mj-nlm-shared/` 目录

## 文件结构

```
skills/
├── mj-nlm-auth/        # 认证技能 + troubleshooting 手册（v1）
├── mj-nlm-build/       # 知识库创建（v2，含 P6/P7）
├── mj-nlm-manage/      # 生命周期管理（v1）
├── mj-nlm-query/       # 知识问答（v2，6 种 Mode）
├── mj-nlm-studio/      # Studio 制品（v2，含 view + guardrails；v2.1 三输出模式）
├── mj-nlm-learn-make/  # 学习侧编排器 wrapper 1（v2.2 新增）
├── mj-nlm-learn-test/  # 考察侧编排器 wrapper 2（v2.2 新增）
└── mj-nlm-shared/      # 共享参考资源（10 份）
    ├── preflight-checklist.md       # NLM 启动冒烟三级 checklist（v2.3 新增）
    ├── quota-estimation.md          # 配额与耗时预告（v2.3 新增，从 risk-control §6 抽出）
    ├── naming-reference.md          # 双项目 scope→路径映射 + 元 source 编号
    ├── material-classification.md   # 三分法 + 多源类型分类
    ├── artifact-type-reference.md   # 9 种 artifact_type + v2 横切子参数 + v2.1 三输出模式
    ├── artifact-metadata-template.md  # NLM 制品元信息记录范式（v2.1 新增）
    ├── focus-prompt-templates.md    # 学习导向 Intent Layer 模板（v2 重写）
    ├── risk-control-templates.md    # 来源/制品配比 + 幻觉防护约束（v2 新增；v2.3 起 §6 配额抽出到 quota-estimation.md）
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
