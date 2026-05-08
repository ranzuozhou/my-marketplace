# mj-nlm — NotebookLM Learning-Loop Plugin for Claude Code

> **v2.4 — Preflight 实施落地**：v2.3 的 `preflight-checklist.md` 模板正式编入 6 个 skill 的 Phase 0 实施段（build / manage / query / studio 显式 Phase 0 + H0a/b/c；learn-make / learn-test wrapper 加隐式 preflight 注解委托子 skill）。auth skill 不动。仅文档结构改动，**非破坏性**；故障从 Phase 7 后移晚发现 → Phase 0 早发现。
>
> **v2.3 — Deprecation removal + 启动规范**：移除 v2.2 forward-announce 的 `/mj-nlm:learn` skill；新增 2 份共享规范 `preflight-checklist.md`（启动冒烟三级 L1 Auth / L2 MCP health / L3 Notebook scope）+ `quota-estimation.md`（单调用基线 + 双 wrapper 配额预告）。skill 数 8 → 7；shared 文档 8 → 10。**轻量 BREAKING（v2.2 已公告期 ~2 周）**。
>
> **v2.2 — 高层入口整合**：新增 `/mj-nlm:learn-make`（生成学习资料）+ `/mj-nlm:learn-test`（生成考察资料）两个 high-level wrapper。用户对外只需记 2 个命令，底层 skill 仍可独立调用。
>
> **v2.1 — 全在线 + Metadata-Only 默认行为**：studio Phase 4 默认输出元信息 markdown（record mode），二进制 download 降级为显式 opt-in；对齐 learning 子系统「markdown 进 git，binary 永不入 git」约束。
>
> **v2.0 — MJ-AgentLab 学习闭环版**：从"被动产出制品"重构为"学习闭环"（依据方法论文档），覆盖 mj-system + mj-agent 双项目。

MJ-AgentLab NotebookLM 技能家族，把 NotebookLM 多媒体当作「理解脚手架」，先降低进入陌生主题的成本，再用领域定向报告 / 三版生成 / Quiz 错题反馈 / 来源核查 / 理解度自检完成完整学习闭环。

## 7 个命令（v2.3: 8 - 1 = 5 底层 + 2 high-level wrapper）

### High-level wrapper（v2.2 新增，对外推荐入口）

| 命令 | 说明 |
|---|---|
| `/mj-nlm:learn-make` | **生成学习资料 wrapper**：编排 `build` + `studio` 上游 7 类制品（mind_map / video / slide / audio / report / infographic / data_table）；默认 record mode；支持 `--triple-view` / `--with-download` / `--download-only` / `--resume` |
| `/mj-nlm:learn-test` | **生成考察资料 wrapper**：编排 `studio` quiz/flashcards + 可选 `query` Mode D（错题归因）/ F（自检）/ E（来源核查）；默认锁定 quiz + flashcards，其他三项需勾选；支持 `--full` / `--rootcause` / `--selfcheck` / `--sourcecheck` |

### 底层 skill（独立可调用，wrapper 内部调度）

| 命令 | 说明 |
|---|---|
| `/mj-nlm:auth` | NLM 认证（登录、刷新、切换账号、故障排查） |
| `/mj-nlm:build` | 创建知识库（扫描 → 导入 → 打标签 → 来源充足性预检 → 领域定向报告） |
| `/mj-nlm:manage` | 管理知识库（Notebook / Source / Tag CRUD + 分享） |
| `/mj-nlm:query` | 知识问答（6 种 Mode：Single / Cross / Deep Research / Quiz Root Cause / Source Check / Self-Check） |
| `/mj-nlm:studio` | Studio 制品生成（9 种类型 × 4 view 视角 + 默认幻觉防护 + v2.1 record/download/both 三输出模式，默认 record） |

## v2.2 核心新概念

### 高层入口（learn-make / learn-test）

v2.2 把 v2.0 引入的单一编排器 `/mj-nlm:learn` 拆为两个语义对偶的 wrapper：

- **学习侧**：`/mj-nlm:learn-make <topic>` —— 从 0 到 1 创建 notebook + 一键生成学习制品组合
- **考察侧**：`/mj-nlm:learn-test <notebook_id>` —— 在已有 notebook 上生成考察资料并按需触发归因 / 自检 / 核查

完整学习闭环 = `learn-make` 串 `learn-test`。这两个 wrapper 内部 100% 复用 `build` / `studio` / `query` 现有 Phase，不重写任何底层逻辑——纯 dispatch + 默认值 + AskUserQuestion 多选。

### 完整闭环示例

```
# Step 1: 生成学习资料
/mj-nlm:learn-make DQV
→ build → mind_map / video / slide / audio 4 份 record markdown 进 git

# Step 2: 生成考察资料
/mj-nlm:learn-test MJ-system-mod-DQV-20260508
→ quiz + flashcards 2 份 record；可加 --full 跑完错题归因 + 自检 + 核查
```

### 与 v2.1 的关系

v2.2 是 UX 优化层，**不动**底层 skill（auth / build / manage / studio / query 全保留独立调用能力）。v2.1 的 record mode 默认行为通过 wrapper 完整透传（`--with-download` / `--download-only` 标志均可用）。

---

## v2.1 核心新概念

### 默认 record mode（元信息 markdown）

studio Phase 4 默认不再调用 `download_artifact` 把二进制写到本地，而是渲染一份元信息 markdown 到用户指定路径（建议 `learning/<topic>/_nlm/<artifact>.md`），包含：

- frontmatter：notebook_id / artifact_type / view / focus_prompt_summary / 在线访问 URL / 与项目侧学习文档的双向 wikilink
- body（≤ 50 行）：主题、在线访问入口、focus prompt 关键参数、与项目的关系、变更历史

完整范式见 `skills/mj-nlm-shared/artifact-metadata-template.md`。

### 三输出模式（`--mode`）

| `--mode` | 输出 | 默认 | 适用 |
|---|---|---|---|
| `record` | 元信息 markdown（< 4 KB） | ✅ | 学习闭环、团队共享、长期沉淀；二进制不入 git |
| `download` | 二进制本地文件（5-55 MB） | — | 离线分享、外部演示、归档备份 |
| `both` | record + binary | — | 学习+归档场景 |

### 与 learning 子系统对齐

mj-system / mj-agent learning 子系统的强约束：
- ✅ markdown 学习文档进 git
- ❌ mp3 / mp4 / pdf 等二进制**永不入 git**（17-55 MB / 单文件）
- ✅ NotebookLM 产物**全部在线托管**

v2.1 默认行为正好对齐该约束，learn skill 编排默认走 record 路径。

---

## v2 核心新概念

### 学习地图：领域定向报告（00c）

每次 build 完成时自动生成 `00c-定向-{topic}领域定向报告` 元 source，包含：
- 领域归属与典型问题
- 原始困惑翻译（5 个新手日常问题 → 专业问题）
- 核心概念地图（10-15 概念，标出前置 / 高级 / 易误解）
- 术语翻译表（20 个，含日常语言 / 专业定义 / 最小例子 / 反例 / 常见误解）
- 5 个成功案例 + 5 个失败案例（机制分析）
- 学习路线
- 推荐 NLM 制品组合

后续所有 studio 制品强制引用之，确保「不只是漂亮的总结」。

### 三版生成（view 子参数）

同 notebook 同 artifact_type 可生成三个难度版本：
- `view=foundation` — 零基础版：少术语、多类比
- `view=structural` — 结构版：概念地图、适用边界
- `view=challenge` — 挑战版：反例、迁移题、诊断题

### 默认幻觉防护

所有 studio_create 调用自动追加固定约束句（来源引用、不编造案例、来源不足时明说）。`risk-class:high` notebook（医疗 / 法律 / 财务 / 合同 / 考试 / 安全）强制开启。

### 6 种 query 模式

新增 Mode D（Quiz 错题 root cause）、Mode E（Source Check 来源核查）、Mode F（7 项理解度自检 → 仪表盘 Note）。

## v2.3 核心新概念

### 启动冒烟与配额预告

v2.3 把 v2.0/v2.1 学习闭环卡 Phase 7 的根因（认证 / scope 故障晚发现）前移到 Phase 0：

- **`mj-nlm-shared/preflight-checklist.md`** — 三级 preflight：L1 Auth Token / L2 NLM Service Health（server_info + notebook_list） / L3 Notebook scope（条件触发）；含 5min 缓存策略 + H-point 模板
- **`mj-nlm-shared/quota-estimation.md`** — 单调用耗时基线（per-source / per-artifact） + 双 wrapper 配额预告 + build/studio/query 单步耗时 + NotebookLM 公开+经验配额上限

各 skill 在 Phase 0 通过 preflight 后，按 quota-estimation 的总耗时报告模板告知用户预计耗时与调用次数，让用户决定是否启动、是否后台等。

### Deprecation removal

`/mj-nlm:learn`（v2.0 引入 / v2.2 deprecated）已在 v2.3 移除。所有调用应改用 `/mj-nlm:learn-make` + `/mj-nlm:learn-test` 串联。Migration 见 `CHANGELOG.md#[2.3.0]`。

## 双项目支持

| project | 说明 |
|---|---|
| `system` | MJ System 主项目（数据处理与分析平台） |
| `agent` | MJ-AgentLab 项目（Agent / LangGraph / MCP 服务）— **v2 新增正式支持** |
| `multi` | 跨项目对齐 — **v2 新增** |
| `intel` | 情报系统（v1 沿用） |

## 前置条件

- **Claude Code** v2.1+
- **NotebookLM MCP CLI**：
  ```bash
  uv tool install notebooklm-mcp-cli --with socksio --force
  ```
- **Google 认证**：
  ```bash
  nlm login
  ```

## 安装方式

### 通过 Marketplace 安装（推荐）

```
/plugin marketplace add ranzuozhou/my-marketplace
/plugin install mj-nlm@my-marketplace
```

### 本地开发安装

```bash
claude --plugin-dir "D:\workspace\10-software-project\projects\my-marketplace\plugins\mj-nlm"
```

## 验证安装

```
/plugin                    # 确认 mj-nlm 出现在列表
/mj-nlm:learn-make        # 测试 v2.2 新 wrapper 加载
/mj-nlm:learn-test        # 测试 v2.2 新 wrapper 加载
/mcp                       # 确认 notebooklm-mcp 可用
```

## 快速上手

### 推荐入口（v2.2）：两个 wrapper 串联

**Step 1：生成学习资料**
```
/mj-nlm:learn-make DQV
```
wrapper 1 引导你：
1. notebook locate（无则触发 build：来源准备 + 领域定向报告）
2. AskUserQuestion 多选制品组合（mind_map / video / slide / audio / report / infographic / data_table）
3. 循环触发 studio（默认 record mode）
4. Handoff：record markdown 路径列表 + 提示下一步 learn-test

**Step 2：生成考察资料**
```
/mj-nlm:learn-test MJ-system-mod-DQV-20260508
```
wrapper 2 引导你：
1. 默认锁定生成 quiz + flashcards（record markdown 进 git，含 NotebookLM 在线答题 URL）
2. 用户在 NLM 在线答 quiz
3. 如勾选 `--full` 或选项 D/F/E：错题归因 → 7 项自检 → 来源核查
4. Handoff：考察 record + 仪表盘 Note 链接 + 24h 回访预约

### 单步使用（advanced）

```
/mj-nlm:build              # 仅构建知识库（含 v2 P6/P7）
/mj-nlm:studio             # 仅生成单个制品（含 v2 view + guardrails + v2.1 三模式）
/mj-nlm:query              # 仅问答（6 种 Mode）
/mj-nlm:manage             # 生命周期管理
/mj-nlm:auth               # 认证维护
```

## 自然语言触发

除了斜杠命令，也支持自然语言触发：

- "生成学习资料 / 一键学习材料 / 学习编排" → `/mj-nlm:learn-make`（v2.2 推荐）
- "生成考察资料 / 出题 / 出 quiz / 学习效果检验" → `/mj-nlm:learn-test`（v2.2 推荐）
- "建知识库 / 生成领域定向报告" → `/mj-nlm:build`（advanced 单步）
- "生成三版音频 / 零基础版+结构版+挑战版" → `/mj-nlm:studio` 或 `/mj-nlm:learn-make --triple-view`
- "只要 metadata / 不下载 / 在线引用 / online reference" → `/mj-nlm:studio --mode record`（v2.1 默认）
- "metadata + 本地副本 / 学习+归档" → `/mj-nlm:studio --mode both` 或 `/mj-nlm:learn-make --with-download`
- "我做完 quiz 错了 5 题，分析下" → `/mj-nlm:learn-test --rootcause`（v2.2 推荐）或 `/mj-nlm:query` Mode D
- "刚才的回答靠谱吗，能找到来源吗" → `/mj-nlm:query` Mode E
- "做一次理解度自检" → `/mj-nlm:learn-test --selfcheck`（v2.2 推荐）或 `/mj-nlm:query` Mode F

## 设计哲学（来自方法论 §12）

> **不要让 NotebookLM 替你学习；要让它把新内容拆成更容易学习、复习、提问和验证的形态。**
>
> Video 负责进入，Slide 负责结构，Audio 负责重复，Mind Map 负责关系，Quiz 负责检验，原文负责查证。

## 未实现 / 未来 v2.x roadmap

- ✅ v2.0.1：mj-agent 实际目录路径定稿（6-scope 方案 B：code / tool / skill / prompt / docs / cross）
- ✅ v2.1：默认 record mode（全在线 + 元信息 markdown），二进制 download 降级为 opt-in
- ✅ v2.2：高层入口整合（`/mj-nlm:learn-make` + `/mj-nlm:learn-test`），旧 `/mj-nlm:learn` 标 deprecated
- ✅ v2.3：移除 v2.2 deprecated 的 `/mj-nlm:learn` skill；新增 preflight-checklist + quota-estimation 两份共享规范
- v2.4：将 preflight L1+L2 实际编进各 skill Phase 0 实施代码（v2.3 仅文档化）；NLM artifact-level URL 暴露调研（v2.1 回退方案 B → 升级）
- v2.5：Hooks 自动检测过期 24h 复述提醒 + marketplace 层"知识库健康度"看板（汇总 quiz 命中率与 source check 通过率）
- v2.6：移除 v1 `legacy_*` prompt 别名
- v2.x：英文 prompt 模板支持（v2.0 仅中文）；按需评估独立 mj-nlm-record skill（用于历史 artifact 补录）

## 许可

MIT License
