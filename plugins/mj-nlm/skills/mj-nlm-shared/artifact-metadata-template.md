# Artifact Metadata Template — NLM 制品元信息记录范式（v2.1）

> v2.1 起 mj-nlm 默认产物路径为「在线 + 项目侧 metadata markdown 记录」，不再强制 download 二进制到本地。本文件给出元信息 markdown 的固定 schema 与填写规范。

## 用途

每生成一个 NotebookLM Studio 制品（artifact），项目侧仅留**一份 record markdown**：
- 不复述制品内容（让用户在线读 NotebookLM）
- 仅记录访问入口、focus prompt 关键参数、与项目侧学习文档的双向关联
- 大小约束：**body ≤ 50 行**（不含 frontmatter）

适用方向：
- mj-system / mj-agent learning 子系统（`learning/<topic>/_nlm/<artifact>.md`）
- 任何需要把 NLM 在线产物登记进 git 而不污染 binary 的场景

---

## Frontmatter Schema

```yaml
---
type: "nlm-artifact-record"           # 固定值，便于检索
notebook_id: "<uuid>"                 # NotebookLM notebook ID
notebook_title: "MJ-system-mod-DQV-20260506"  # build skill 命名
artifact_id: "<artifact uuid 或 unknown>"     # 若 API 不返回则填 unknown
artifact_type: "audio"                # 9 种之一：audio | video | infographic | slide_deck | report | flashcards | quiz | data_table | mind_map
view: "default"                       # default | foundation | structural | challenge（v2 三版机制）
notebook_url: "https://notebooklm.google.com/notebook/<id>"  # 必填
artifact_url: "<notebook_url 同值或 NLM 暴露的 artifact 直链>"  # v2.1 回退方案 B：未暴露则与 notebook_url 相同
sources_count: 12                     # 生成时 notebook 拥有的 source 数
focus_prompt_summary: "<1 行说明本制品 prompt 主题>"
guardrails_enabled: true              # 与 studio_create 时 disable_guardrails 取反
created: "2026-05-08T14:32:00Z"       # ISO8601 UTC
expires: "unknown"                    # NotebookLM 未文档化 TTL，保持 unknown；如官方公布则填实
related_learning_doc: "[[../[LEARNING]_DQV_overview]]"  # 项目侧关联学习文档（可空）
state: "active"                       # active | archived
version: "v1.0"                       # record markdown 自身版本（与 NLM 制品无关）
---
```

### 字段填写规则

| 字段 | 来源 | 备注 |
|---|---|---|
| `notebook_id` / `notebook_title` | `notebook_describe()` | build skill Phase 0 命名，强制 `MJ-{project}-{scope}-{topic}-{YYYYMMDD}` |
| `artifact_id` | `studio_status()` 返回 | NotebookLM 当前不保证暴露；未拿到填 `unknown` |
| `artifact_type` / `view` | studio_create 调用参数 | 9 种 × 4 view 详见 `→ ./artifact-type-reference.md` |
| `artifact_url` | **v2.1 回退方案 B**：与 `notebook_url` 同值 | 若 NLM 后续暴露 artifact-level URL，可由 studio Phase 4 自动填实 |
| `sources_count` | `notebook_describe()` 返回的 source 列表长度 | |
| `focus_prompt_summary` | studio Phase 2.3 拼接的三层 prompt 摘要 | 只写一行，不复述完整 prompt |
| `guardrails_enabled` | `not disable_guardrails`（high-risk tag 强制 true） | |
| `related_learning_doc` | 用户侧学习子系统路径 | 双向 wikilink，详见 §对齐 |

---

## Body 范式（≤ 50 行）

```markdown
# <Notebook 标题> · <Artifact Type> (<view>)

## 主题（2-3 行）

<本制品要解释什么 / 解决什么学习问题，1-3 句话>

## 在线访问

- [打开 NotebookLM](<artifact_url 或 notebook_url>)
- 在 notebook 内定位本制品：在 NotebookLM 的 Studio 面板中按 `<artifact_type>` + 标题 `<生成时使用的中文标题>` 找到（v2.1 NLM 暂不暴露 artifact-level 直链）
- 若链接失效：搜 notebook 标题 `<notebook_title>` 重新打开

## Focus Prompt（关键参数，不复述全文）

- 学习视角：<view>
- 锚定 source：<00c-定向-{topic}领域定向报告 + 主体 sources>
- 防护约束：<enabled / disabled + 原因>
- 子参数（如适用）：<audio_format=brief / report_format=Briefing Doc / ...>

## 与项目的关系

- 解读对象：<[[../../docs/rule/[STANDARD]_X]] 或 [[../../mj-agent/...]]>
- 衍生学习文档：<[[../[LEARNING]_*]]>
- 来源 sources 概要（≤ 5 项要点）：
  - <source 1 简介>
  - <source 2 简介>
  - ...

## 变更历史

- v1.0 / 2026-05-08：初次记录
```

**约束**：
- ≤ 50 行 markdown body（不含 frontmatter）
- 不复述 NotebookLM 已生成的完整内容（让用户在线读）
- 仅记录**元信息 + 项目侧链接 + 一行学习意图**
- "在 notebook 内定位本制品"段是 v2.1 回退方案 B 的关键——若用户/未来版本拿到 artifact-level URL 可缩短为单行链接

---

## 完整可复制模板

```markdown
---
type: "nlm-artifact-record"
notebook_id: "<uuid>"
notebook_title: "<MJ-{project}-{scope}-{topic}-{YYYYMMDD}>"
artifact_id: "unknown"
artifact_type: "<audio | video | infographic | slide_deck | report | flashcards | quiz | data_table | mind_map>"
view: "<default | foundation | structural | challenge>"
notebook_url: "https://notebooklm.google.com/notebook/<id>"
artifact_url: "https://notebooklm.google.com/notebook/<id>"
sources_count: 0
focus_prompt_summary: "<1 行 prompt 主题>"
guardrails_enabled: true
created: "<YYYY-MM-DDTHH:MM:SSZ>"
expires: "unknown"
related_learning_doc: ""
state: "active"
version: "v1.0"
---

# <Notebook 标题> · <Artifact Type> (<view>)

## 主题

<2-3 行>

## 在线访问

- [打开 NotebookLM](<URL>)
- 在 notebook 内定位本制品：Studio 面板 → `<artifact_type>` → 标题 `<中文标题>`
- 若链接失效：搜 notebook 标题 `<notebook_title>`

## Focus Prompt（关键参数）

- 学习视角：<view>
- 锚定 source：<00c-定向-{topic}领域定向报告>
- 防护约束：<enabled | disabled + 原因>
- 子参数：<...>

## 与项目的关系

- 解读对象：<wikilink>
- 衍生学习文档：<wikilink>
- 来源 sources 概要：
  - <...>

## 变更历史

- v1.0 / <YYYY-MM-DD>：初次记录
```

---

## 命名与存放

### 文件命名

`<artifact_type>-<view>-<short-topic>.md`

例：
- `audio-foundation-dqv-overview.md`
- `slide_deck-default-langgraph-agent-design.md`
- `mind_map-default-mj-system-architecture.md`

### 存放路径

| 调用方 | 默认路径 | 说明 |
|---|---|---|
| **mj-system learning 子系统** | `learning/<topic>/_nlm/<file>.md` | 与 [LEARNING]_*.md 同级 |
| **mj-agent learning 子系统** | `learning/<topic>/_nlm/<file>.md` | 同上 |
| **临时探索** | 用户自选；建议 `<vault>/_scratch/_nlm/` | 不入 git |

`_nlm/` 子目录把元信息文件与正式 [LEARNING]_*.md 区分开，便于 archive。

---

## 与 mj-system / mj-agent learning 子系统对齐

mj-system learning 子系统约束：

- ✅ markdown 学习文档进 git（团队共享）
- ❌ mp3 / mp4 / pdf 等二进制**永不入 git**（17-55MB / 单文件）
- ✅ NotebookLM 产物**全部在线托管**

本模板与该约束的对齐点：

| 学习子系统侧 | 本模板侧 |
|---|---|
| `learning/<topic>/_nlm/<artifact>.md` 路径 | studio Phase 4 record mode 默认输出位置 |
| record markdown frontmatter `type: nlm-artifact-record` | 本模板 `type` 字段固定值 |
| `related_learning_doc: [[../[LEARNING]_*]]` | 本模板对应字段 |
| `state: active / archived` | 本模板 `state` 字段 |

### 双向 wikilink

- record → learning：`[[../[LEARNING]_*]]`（在 record 的 frontmatter `related_learning_doc` + body "与项目的关系"段）
- learning → record：`[[./_nlm/<artifact>]]`（在 [LEARNING]_*.md 的"配套 NLM 制品"段）

---

## 何时由谁写

| 触发场景 | 调用 skill | 写入位置 | 备注 |
|---|---|---|---|
| 新生成 artifact（默认 record mode） | `/mj-nlm:studio --mode record`（或默认） | 用户提供路径，建议 `learning/<topic>/_nlm/` | studio Phase 4 record 分支自动渲染 |
| 生成学习资料（默认） | `/mj-nlm:learn-make`（Phase 3 循环默认走 record） | 同上 | wrapper 编排 studio --mode record |
| 生成考察资料（默认） | `/mj-nlm:learn-test`（Phase 2a quiz/flashcards 默认走 record） | 同上 | wrapper 编排 studio --mode record |
| 既要 metadata 又要 download | `/mj-nlm:studio --mode both` 或 wrapper `--with-download` | record 写 `_nlm/`，binary 用户自存（不入 git） | 学习+归档场景 |
| 历史 artifact 补录（无 record） | 手动按本模板填写 | 同上 | v2.1/v2.3 均不提供独立 skill；如频繁可考虑独立 mj-nlm-record skill |

---

## 与 download 路径的对比

| 维度 | record mode（v2.1 默认） | download mode（v2.1 opt-in） |
|---|---|---|
| 输出 | metadata markdown（≤ 50 行 body） | 二进制（mp3 / mp4 / pdf / png / json / csv） |
| 大小 | < 4 KB | 5-55 MB |
| 入 git | ✅ 是 | ❌ 永不 |
| 离线访问 | ❌ 否（需 NLM 在线） | ✅ 是 |
| 可分享给团队 | ✅ 通过 git + NLM 链接 | ⚠ 需走二进制分发 |
| 适用场景 | 学习闭环、团队共享、长期沉淀 | 离线分享、外部演示、归档备份 |

`--mode both` 同时输出两者（学习+归档场景）。

---

## Reference

- **`→ ./artifact-type-reference.md`** — 9 种 artifact_type 与 v2 横切子参数（含 `view` / `disable_guardrails`）
- **`→ ./focus-prompt-templates.md`** — Intent Layer 模板（`focus_prompt_summary` 来源）
- **`→ ./naming-reference.md`** — notebook_title 命名规范（`MJ-{project}-{scope}-{topic}-{YYYYMMDD}`）
- **`→ ../mj-nlm-studio/SKILL.md`** — Phase 4 record / download / both 三分支
