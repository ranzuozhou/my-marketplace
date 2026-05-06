# Artifact Type Reference — Studio 制品类型速查

## 9 种 artifact_type 参数速查

| # | artifact_type | 中文名 | 输出格式 | 适用场景 |
|---|--------------|--------|---------|---------|
| 1 | `audio` | 音频播客 | MP4/MP3 | 通勤学习、新人入门、知识分享 |
| 2 | `video` | 视频概述 | MP4 | 可视化讲解、技术演示 |
| 3 | `infographic` | 信息图 | PNG | 架构可视化、流程展示 |
| 4 | `slide_deck` | 幻灯片 | PDF/PPTX | 技术分享、团队培训、评审演示 |
| 5 | `report` | 报告文档 | Markdown | 简报、学习指南、博客文章 |
| 6 | `flashcards` | 闪卡 | JSON/Markdown/HTML | 知识记忆、培训测验 |
| 7 | `quiz` | 测验 | JSON/Markdown/HTML | 培训考核、自测 |
| 8 | `data_table` | 数据表 | CSV | 结构化数据提取、对比分析 |
| 9 | `mind_map` | 思维导图 | JSON | 知识图谱、概念关系可视化 |

---

## 制品特性详情

### audio（音频播客）

- **风格**：双人对话式播客
- **子参数**：
  - `audio_format`：`deep_dive`（默认，深入讨论）| `brief`（简要概述）| `critique`（批评分析）| `debate`（辩论）
  - `audio_length`：`short` | `default`（默认）| `long`
- **下载**：`download_artifact(artifact_type="audio", output_path="podcast.mp3")`

### video（视频概述）

- **风格**：AI 生成的可视化视频讲解
- **子参数**：
  - `video_format`：`explainer`（默认，讲解式）| `brief`（简要）| `cinematic`（电影风格）
  - `visual_style`：`auto_select`（默认）| `classic` | `whiteboard` | `kawaii` | `anime` | `watercolor` | `retro_print` | `heritage` | `paper_craft`
- **下载**：`download_artifact(artifact_type="video", output_path="overview.mp4")`

### infographic（信息图）

- **风格**：可视化信息图
- **子参数**：
  - `orientation`：`landscape`（默认）| `portrait` | `square`
  - `detail_level`：`concise` | `standard`（默认）| `detailed`
  - `infographic_style`：`auto_select`（默认）| `sketch_note` | `professional` | `bento_grid` | `editorial` | `instructional` | `bricks` | `clay` | `anime` | `kawaii` | `scientific`
- **下载**：`download_artifact(artifact_type="infographic", output_path="info.png")`

### slide_deck（幻灯片）

- **风格**：演示文稿，支持逐页修订
- **子参数**：
  - `slide_format`：`detailed_deck`（默认，详细版）| `presenter_slides`（演讲者版）
  - `slide_length`：`short` | `default`（默认）
- **修订**：`studio_revise(notebook_id, artifact_id, slide_instructions=[{"slide": 3, "instruction": "添加流程图"}], confirm=True)` — 仅此类型支持，修订会创建新 artifact
- **下载**：`download_artifact(artifact_type="slide_deck", output_path="slides.pdf")` 或 `slide_deck_format="pptx"` 下载 PPTX 格式

### report（报告文档）

- **风格**：结构化文本报告，通过 `report_format` 选择子类型
- **子参数**：
  - `report_format`：`Briefing Doc`（默认，简报文档）| `Study Guide`（学习指南）| `Blog Post`（博客文章）| `Create Your Own`（自定义）
  - `custom_prompt`：当 `report_format="Create Your Own"` 时必填，定义自定义报告格式
- **下载**：`download_artifact(artifact_type="report", output_path="report.md")`

> **注意**：原 `briefing_doc` 和 `study_guide` 不是独立的 artifact_type，而是 `report` 的 `report_format` 子参数。

### flashcards（闪卡）

- **风格**：问答式记忆卡片
- **子参数**：
  - `difficulty`：`easy` | `medium`（默认）| `hard`
- **下载**：`download_artifact(artifact_type="flashcards", output_path="cards.json")` 或 `output_format="markdown|html"`

### quiz（测验）

- **风格**：多选题测验
- **子参数**：
  - `question_count`：题目数量（整数，默认 2）
  - `difficulty`：`easy` | `medium`（默认）| `hard`
- **下载**：`download_artifact(artifact_type="quiz", output_path="quiz.json")` 或 `output_format="markdown|html"`

### data_table（数据表）

- **风格**：从 notebook 内容提取的结构化数据表
- **子参数**：
  - `description`：**必填**，描述要提取的数据内容
- **下载**：`download_artifact(artifact_type="data_table", output_path="data.csv")`

### mind_map（思维导图）

- **风格**：概念关系可视化图
- **子参数**：
  - `title`：思维导图标题（默认 "Mind Map"）
- **下载**：`download_artifact(artifact_type="mind_map", output_path="mindmap.json")`

---

## MJ System 推荐组合

### 按场景

| 场景 | 第一制品 | 第二制品 | 第三制品 |
|------|---------|---------|---------|
| 新人入职培训 | `audio`（brief） | `report`（Study Guide） | `flashcards` |
| 技术分享演示 | `slide_deck` | `infographic` | — |
| 架构评审准备 | `report`（Briefing Doc） | `mind_map` | `audio`（deep_dive） |
| 知识体系建设 | `mind_map` | `report`（Study Guide） | `quiz` |
| 深度技术学习 | `audio`（deep_dive） | `report`（Study Guide） | `flashcards` |
| 数据分析对比 | `data_table` | `infographic` | — |

### 按制品生成顺序建议

1. 先生成 `mind_map` — 确认知识结构合理
2. 再生成目标制品（如 `slide_deck`、`audio`）
3. 最后生成补充制品（如 `quiz`、`flashcards`）

---

## studio_create 参数参考

```
studio_create(
    notebook_id: str,           # 目标 notebook ID（必填）
    artifact_type: str,         # 上述 9 种之一（必填）
    focus_prompt: str = "",     # 内容引导（见 focus-prompt-templates.md）
    language: str = "",         # BCP-47 语言代码（如 "zh"、"en"、"ja"）
    source_ids: list = None,    # 限定 source 范围（默认全部）
    confirm: bool = True,       # 需用户确认（必填 True）
    # 以下为各 artifact_type 的子参数，仅在对应类型时生效
    audio_format: str,          # audio 专用
    audio_length: str,          # audio 专用
    video_format: str,          # video 专用
    visual_style: str,          # video 专用
    orientation: str,           # infographic 专用
    detail_level: str,          # infographic 专用
    infographic_style: str,     # infographic 专用
    slide_format: str,          # slide_deck 专用
    slide_length: str,          # slide_deck 专用
    report_format: str,         # report 专用
    custom_prompt: str,         # report（Create Your Own）专用
    difficulty: str,            # flashcards / quiz 专用
    question_count: int,        # quiz 专用
    description: str,           # data_table 专用（必填）
    title: str,                 # mind_map 专用
    # v2 新增子参数（horizontal）
    view: str = "default",      # 学习视角：default | foundation | structural | challenge
    disable_guardrails: bool = False,  # 跳过默认幻觉防护约束（仅推荐内部技术分享场景）
    focus_prompt_template: str = None, # legacy_* 模板别名（迁移期使用）
)
```

## v2 新增子参数详解

### `view`（学习视角，对所有 artifact_type 生效）

来自方法论 §8「同一内容生成三版」。在 v2 中，可对同一 notebook 同一 artifact_type 生成三个难度版本：

| view | 模板路径 | 适用 |
|---|---|---|
| `default`（默认） | `focus-prompt-templates.md#{artifact_type}（默认）` | v1 兼容，单一版本 |
| `foundation` | `focus-prompt-templates.md#{artifact_type} + view=foundation` | 零基础版：少术语、多类比 |
| `structural` | `focus-prompt-templates.md#{artifact_type} + view=structural` | 结构版：概念地图、适用边界 |
| `challenge` | `focus-prompt-templates.md#{artifact_type} + view=challenge` | 挑战版：反例、迁移题 |

**调用示例**：

```python
# 三版连续生成
for view in ("foundation", "structural", "challenge"):
    studio_create(
        notebook_id=nb_id,
        artifact_type="audio",
        view=view,
        focus_prompt=...,
        language="zh",
        confirm=True,
    )
```

文件命名后缀：`{title}-{view}.{ext}`，如 `DQV技术概述-foundation.mp3`。

### `disable_guardrails`（关闭幻觉防护约束）

默认 `False`：所有 studio_create 在拼接 focus_prompt 时自动追加 `risk-control-templates.md §2` 中的固定约束句。

设 `True` 时跳过追加，仅推荐用于：
- 内部技术分享场景（受众已知来源、不会作为外部决策依据）
- v1 prompt 向后兼容（迁移期）
- 测试场景

**安全提醒**：高风险类别 notebook（含医疗 / 法律 / 财务 / 合同 / 考试关键词，详见 `risk-control-templates.md §3`）禁止 disable_guardrails，调用方在 build skill 已自动标记 `risk-class:high` tag，studio 检测到此 tag 强制忽略 `disable_guardrails=True` 设置。

### `focus_prompt_template`（v1 兼容别名）

`legacy_*` 别名（v2.0 / v2.1 / v2.2 仍可用，v2.3 抛 deprecation warning，v2.4 移除）。详见 `focus-prompt-templates.md` 末尾的 v1→v2 兼容性表。

## download_artifact 参数参考

```
download_artifact(
    notebook_id: str,           # 目标 notebook ID（必填）
    artifact_type: str,         # 与 studio_create 相同（必填）
    output_path: str,           # 本地保存路径（必填）
    artifact_id: str = None,    # 指定制品 ID（默认下载最新）
    output_format: str = "json",# quiz/flashcards 专用：json|markdown|html
    slide_deck_format: str = "pdf"  # slide_deck 专用：pdf|pptx
)
```

## studio_revise 参数参考（仅限 slide_deck）

```
studio_revise(
    notebook_id: str,           # 目标 notebook ID（必填）
    artifact_id: str,           # 要修订的 slide_deck ID（必填，从 studio_status 获取）
    slide_instructions: list,   # 修订指令列表（必填）
                                # 格式：[{"slide": 1, "instruction": "修改标题"}, ...]
    confirm: bool = True        # 需用户确认（必填 True）
)
```

## studio_status 参数参考

```
studio_status(
    notebook_id: str,           # 目标 notebook ID
    action: str = None,         # 可选："rename"
    new_title: str = None       # action="rename" 时的新标题
)
```
