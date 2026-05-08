# mj-nlm — NotebookLM Learning-Loop Plugin for Claude Code

> **v2.1 — 全在线 + Metadata-Only 默认行为**：studio Phase 4 默认输出元信息 markdown（record mode），二进制 download 降级为显式 opt-in；对齐 learning 子系统「markdown 进 git，binary 永不入 git」约束。
>
> **v2.0 — MJ-AgentLab 学习闭环版**：从"被动产出制品"重构为"学习闭环"（依据方法论文档），覆盖 mj-system + mj-agent 双项目。

MJ-AgentLab NotebookLM 技能家族，把 NotebookLM 多媒体当作「理解脚手架」，先降低进入陌生主题的成本，再用领域定向报告 / 三版生成 / Quiz 错题反馈 / 来源核查 / 理解度自检完成完整学习闭环。

## 6 个命令

| 命令 | 说明 |
|---|---|
| `/mj-nlm:auth` | NLM 认证（登录、刷新、切换账号、故障排查） |
| `/mj-nlm:build` | 创建知识库（扫描 → 导入 → 打标签 → **来源充足性预检 → 领域定向报告**） |
| `/mj-nlm:manage` | 管理知识库（Notebook / Source / Tag CRUD + 分享） |
| `/mj-nlm:query` | 知识问答（**6 种 Mode**：Single / Cross / Deep Research / Quiz Root Cause / Source Check / Self-Check） |
| `/mj-nlm:studio` | Studio 制品生成（9 种类型 × **4 view 视角** + **默认幻觉防护** + **v2.1 record/download/both 三输出模式**，默认 record） |
| `/mj-nlm:learn` | **学习闭环编排器**：10 Phase + 5 Gate 一键走完「来源准备 → 领域定向 → mind_map → video → slide → audio → quiz → 错题 root cause → 来源核查 → 理解度仪表盘」（**v2.1 默认走 record，加 `--with-download` 才本地化**） |

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

### 学习闭环编排器 `/mj-nlm:learn`

依方法论 §11 的最佳推荐流程一站式调度，10 Phase + 5 Gate 分阶段交互（关键关口要求用户审定 / 修改 / 跳过）。

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
/mj-nlm:learn             # 测试 v2 新 skill 加载
/mcp                       # 确认 notebooklm-mcp 可用
```

## 快速上手

### 推荐入口（v2）：完整学习闭环

```
/mj-nlm:learn DQV
```

skill 会引导你：
1. 准备 5 类来源（原始 / 入门 / 案例 / 反例 / 困惑笔记）
2. 自动 build 含领域定向报告
3. Gate 1：审定定向报告
4. 依次生成 mind_map / video / slide / audio
5. 每个制品都有 Gate 决策（接受 / 重生 / 跳过）
6. 生成 quiz + flashcards
7. 用户答 quiz → Mode D 错题 root cause → Gate 7（重生针对性材料 / 跳过）
8. Mode F 理解度 7 项自检 → 仪表盘 Note
9. Mode E 来源核查
10. Handoff：含 24h 复述预约

### 单步使用

```
/mj-nlm:build              # 仅构建知识库（含 v2 P6/P7）
/mj-nlm:studio             # 仅生成单个制品（含 v2 view + guardrails）
/mj-nlm:query              # 仅问答（6 种 Mode）
/mj-nlm:manage             # 生命周期管理
/mj-nlm:auth               # 认证维护
```

## 自然语言触发

除了斜杠命令，也支持自然语言触发：

- "走完 NLM 学习闭环 / 一站式学习" → `/mj-nlm:learn`
- "建知识库 / 生成领域定向报告" → `/mj-nlm:build`
- "生成三版音频 / 零基础版+结构版+挑战版" → `/mj-nlm:studio`
- "只要 metadata / 不下载 / 在线引用 / online reference" → `/mj-nlm:studio --mode record`（v2.1 默认）
- "metadata + 本地副本 / 学习+归档" → `/mj-nlm:studio --mode both`
- "我做完 quiz 错了 5 题，分析下" → `/mj-nlm:query` Mode D
- "刚才的回答靠谱吗，能找到来源吗" → `/mj-nlm:query` Mode E
- "做一次理解度自检" → `/mj-nlm:query` Mode F

## 设计哲学（来自方法论 §12）

> **不要让 NotebookLM 替你学习；要让它把新内容拆成更容易学习、复习、提问和验证的形态。**
>
> Video 负责进入，Slide 负责结构，Audio 负责重复，Mind Map 负责关系，Quiz 负责检验，原文负责查证。

## 未实现 / 未来 v2.x roadmap

- ✅ v2.0.1：mj-agent 实际目录路径定稿（6-scope 方案 B：code / tool / skill / prompt / docs / cross）
- ✅ v2.1：默认 record mode（全在线 + 元信息 markdown），二进制 download 降级为 opt-in
- v2.2：Hooks 自动检测过期 24h 复述提醒 + 调研 NLM artifact-level URL 暴露能力（v2.1 回退方案 B → 若 NLM 暴露则升级）
- v2.3：marketplace 层"知识库健康度"看板（汇总 quiz 命中率与 source check 通过率）
- v2.4：移除 v1 `legacy_*` prompt 别名
- v2.x：英文 prompt 模板支持（v2.0 仅中文）；按需评估独立 mj-nlm-record skill（用于历史 artifact 补录）

## 许可

MIT License
