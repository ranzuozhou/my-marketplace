# Flora PTM 命名、标签与目录规范

本文档是 flora-ptm 插件的命名权威参考，被所有三个技能引用。

---

## Notebook 命名

| 类型 | 格式 | 示例 |
|------|------|------|
| Staging（暂存） | `FLORA-{topic}-Staging-{YYYYMMDD}` | `FLORA-LLM安全-Staging-20260319` |
| Target（目标） | `FLORA-{topic}-{subtopic}-{YYYYMMDD}` | `FLORA-LLM安全-对齐技术-20260319` |

**命名规则**：
- `{topic}` — 用户提供的研究主题名称，中文或英文均可
- `{subtopic}` — 来自 synthesize Phase 1 聚类结果的组名
- `{YYYYMMDD}` — 创建日期，使用 ISO 格式
- 所有前缀统一为 `FLORA-`，便于与其他 notebook 区分

---

## Source 命名

在目标 notebook 中，source 按类别编号以控制阅读顺序：

| 序号前缀 | 类别 | 用途 | 示例 |
|----------|------|------|------|
| `00a-` | 精简 | 逐篇精华提取 | `00a-精简-Attention Is All You Need` |
| `00b-` | 综述 | 跨文献综述 | `00b-综述-LLM安全` |
| `00c-` | 关系 | 关系分析 | `00c-关系-LLM安全` |
| `00d-` | 导航 | 内容索引与阅读顺序 | `00d-导航-LLM安全-对齐技术` |
| （无前缀） | 原文 | 原始报告 source | （保留原文件名） |

---

## Note 命名

Staging notebook 中的 note 命名：

| Note 类型 | 格式 | 说明 |
|-----------|------|------|
| 精简短文 | `精简-{source_name}` | 每篇报告的结构化分析 |
| 关系分析 | `关系分析-{topic}` | 跨报告关系分析结果 |
| 综述 | `综述-{topic}` | 跨文献综述 |
| 导航笔记 | `导航-{topic}` | 内容索引与推荐阅读顺序 |
| 元数据清单 | `元数据-源材料清单` | 固定名称，记录所有 source 的原始路径/URL |

---

## Tag 体系

Flora PTM 使用 NLM tag 系统实现技能间状态传递：

| Notebook 类型 | Tag 组合 | 用途 |
|--------------|----------|------|
| Staging | `flora`, `staging`, `{topic}` | digest 产出，synthesize 输入 |
| Target | `flora`, `target`, `{topic}`, `{subtopic}` | synthesize 产出，produce 输入 |

**Tag 查询模式**：
- 查找 staging: `tag(action="select", query="flora,staging")`
- 查找 target: `tag(action="select", query="flora,target")`
- 查找特定主题: `tag(action="select", query="flora,{topic}")`

---

## 输出目录

媒体产物的本地输出目录结构（相对于当前工作目录）：

```
{output_directory}/{topic}-{YYYYMMDD}/
├── audio/          # MP3/MP4 音频文件
├── slides/         # PDF/PPTX 幻灯片
├── reports/        # Markdown 报告文档
├── visual/         # PNG 信息图、思维导图
└── study/          # JSON/MD 闪卡、测验
```

- `{output_directory}` — 默认为 `flora-output`，可在 `.claude/flora-ptm.local.md` 中自定义
- 子目录按 artifact_type 分类，便于后续消费

---

## 元数据 Note 格式

`元数据-源材料清单` note 使用 JSON 格式记录所有导入的 source 信息：

```json
{
  "topic": "{topic}",
  "created_at": "{YYYY-MM-DD}",
  "sources": [
    {
      "source_id": "nlm_source_id_here",
      "original_path": "/path/to/file.pdf",
      "source_type": "file",
      "filename": "file.pdf",
      "import_status": "success"
    },
    {
      "source_id": "nlm_source_id_here",
      "original_url": "https://example.com/article",
      "source_type": "url",
      "filename": null,
      "import_status": "success"
    }
  ]
}
```

此 note 是 synthesize 分库时重新导入原始 source 的唯一依据。
