# 学习路径详细参数

本文档定义 flora-ptm-produce Phase 1 推荐的 4 种预设学习路径及其详细参数。

---

## 路径概览

| 路径名称 | 代码 | 制品数量 | 预计生成时间 | 目标用户场景 |
|----------|------|----------|-------------|-------------|
| 快速消化 | `quick-digest` | 3 | ~5-8 分钟 | 碎片时间快速了解 |
| 深度学习 | `deep-learning` | 4 | ~10-15 分钟 | 系统掌握+自我检测 |
| 视觉优先 | `visual-first` | 3 | ~8-12 分钟 | 视觉化思维者 |
| 全覆盖 | `comprehensive` | 5 | ~15-20 分钟 | 重要课题全方位吸收 |

---

## 快速消化（quick-digest）

**适合场景**: 通勤、运动、做家务时消化研究内容。重点是听觉输入+快速参考。

| 制品 | artifact_type | sub-params | 推荐消费方式 |
|------|--------------|------------|-------------|
| 概述音频 | `audio` | `audio_format="brief"`, `audio_length="short"` | 通勤时听 |
| 思维导图 | `mind_map` | `title="{topic} 知识结构"` | 听前/听后参考 |
| 简报文档 | `report` | `report_format="Briefing Doc"` | 快速翻阅要点 |

**推荐消费顺序**:
1. 先看思维导图建立整体框架
2. 听概述音频消化细节
3. 用简报文档查漏补缺

---

## 深度学习（deep-learning）

**适合场景**: 需要系统掌握研究内容，准备论文写作或技术分享。

| 制品 | artifact_type | sub-params | 推荐消费方式 |
|------|--------------|------------|-------------|
| 深度播客 | `audio` | `audio_format="deep_dive"`, `audio_length="long"` | 专注时间段收听 |
| 学习指南 | `report` | `report_format="Study Guide"` | 系统阅读+笔记 |
| 测验 | `quiz` | `question_count=15`, `difficulty="mixed"` | 自我检测 |
| 闪卡 | `flashcards` | `difficulty="mixed"` | 间隔重复记忆 |

**推荐消费顺序**:
1. 先读学习指南建立系统理解
2. 听深度播客补充理解维度
3. 用测验检查掌握程度
4. 用闪卡巩固关键概念

---

## 视觉优先（visual-first）

**适合场景**: 视觉化思维者，或需要准备演示/汇报的用户。

| 制品 | artifact_type | sub-params | 推荐消费方式 |
|------|--------------|------------|-------------|
| 幻灯片 | `slide_deck` | `slide_format="detailed_deck"`, `slide_length="default"` | 逐页阅读或演示 |
| 信息图 | `infographic` | `orientation="vertical"`, `detail_level="detailed"`, `infographic_style="auto"` | 打印或屏幕参考 |
| 解说视频 | `video` | `video_format="explainer"`, `visual_style="auto_select"` | 视觉化理解 |

**推荐消费顺序**:
1. 先看解说视频获取直觉理解
2. 用幻灯片逐步深入
3. 信息图作为持续参考

---

## 全覆盖（comprehensive）

**适合场景**: 重要研究课题，需要从多个维度全面吸收。

| 制品 | artifact_type | sub-params | 推荐消费方式 |
|------|--------------|------------|-------------|
| 深度播客 | `audio` | `audio_format="deep_dive"`, `audio_length="default"` | 专注收听 |
| 幻灯片 | `slide_deck` | `slide_format="detailed_deck"` | 系统浏览 |
| 简报文档 | `report` | `report_format="Briefing Doc"` | 要点参考 |
| 思维导图 | `mind_map` | `title="{topic} 知识结构"` | 结构参考 |
| 信息图 | `infographic` | `orientation="vertical"`, `detail_level="detailed"` | 全景参考 |

**推荐消费顺序**:
1. 先看思维导图和信息图建立全景
2. 听深度播客深入理解
3. 用幻灯片逐步梳理
4. 用简报文档查漏补缺

---

## 自定义组合

用户可以在人工判断点自由组合，可选的 artifact_type 完整列表：

| artifact_type | 说明 | 关键 sub-params |
|--------------|------|----------------|
| `audio` | 音频播客 | `audio_format`: brief/deep_dive/critique/debate; `audio_length`: short/default/long |
| `video` | 视频概述 | `video_format`: explainer/brief/cinematic; `visual_style`: auto_select/classic/whiteboard |
| `slide_deck` | 幻灯片 | `slide_format`: detailed_deck/presenter_slides; `slide_length`: short/default |
| `report` | 报告 | `report_format`: Briefing Doc/Study Guide/Blog Post/Create Your Own |
| `infographic` | 信息图 | `orientation`: vertical/horizontal; `detail_level`: overview/detailed; `infographic_style`: auto |
| `mind_map` | 思维导图 | `title`: 自定义标题 |
| `flashcards` | 闪卡 | `difficulty`: easy/mixed/hard |
| `quiz` | 测验 | `question_count`: 数字; `difficulty`: easy/mixed/hard |
| `data_table` | 数据表 | `description`: 必填，描述要提取的数据 |

---

## 输出文件映射

不同 artifact_type 的输出文件存放位置：

| artifact_type | 子目录 | 文件格式 |
|--------------|--------|---------|
| `audio` | `audio/` | `.mp3` 或 `.mp4` |
| `video` | `audio/` | `.mp4` |
| `slide_deck` | `slides/` | `.pdf`（默认）或 `.pptx` |
| `report` | `reports/` | `.md` |
| `infographic` | `visual/` | `.png` |
| `mind_map` | `visual/` | `.json` |
| `flashcards` | `study/` | `.json`（默认）或 `.md` / `.html` |
| `quiz` | `study/` | `.json`（默认）或 `.md` / `.html` |
| `data_table` | `study/` | `.csv` |
