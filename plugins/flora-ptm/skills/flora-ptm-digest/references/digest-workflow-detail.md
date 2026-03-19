# Digest 工作流详情

本文档包含 flora-ptm-digest 的详细工作流补充信息，由 SKILL.md 引用。

---

## 文件分类规则

在 Phase 1 目录扫描时，按以下规则分类处理：

### 支持的文件类型

| 扩展名 | 导入方式 | source_type | 备注 |
|--------|----------|-------------|------|
| `.pdf` | 直接文件导入 | `file` | NLM 原生支持 |
| `.md` | 文件导入 | `file` | Markdown 文本 |
| `.txt` | 文件导入 | `file` | 纯文本 |
| URL | URL 导入 | `url` | 网页内容自动提取 |

### 自动排除的文件

以下文件在扫描时自动排除（H3 安全策略）：

| 模式 | 原因 |
|------|------|
| `.env`, `.env.*` | 环境变量，可能含密钥 |
| `credentials*`, `*secret*` | 凭证文件 |
| `*.key`, `*.pem`, `*.p12` | 加密密钥 |
| `*.exe`, `*.dll`, `*.so` | 二进制文件，NLM 不支持 |
| `*.zip`, `*.tar.*`, `*.rar` | 压缩包，需先解压 |
| `node_modules/`, `.git/`, `__pycache__/` | 项目元数据目录 |

### 推荐的分析变体选择

在导入时记录每个 source 的推荐分析变体（用于 Phase 2）：

| 特征 | 推荐变体 | 判断依据 |
|------|----------|----------|
| PDF + 来源含 arxiv/doi/scholar/ieee/acm | 学术论文版 | URL 特征 |
| PDF + 文件名含公司/机构名 | 行业报告版 | 文件名模式 |
| URL 含 medium/substack/blog/zhihu/mp.weixin | 博客/观点文章版 | URL 特征 |
| 其他 | 通用版 | 默认 |

---

## 错误处理三级策略

在 `source_add()` 导入时，如果遇到错误，按以下三级策略处理：

### L1: 重试

- **触发**: `source_add()` 返回临时性错误（网络超时、服务暂时不可用）
- **策略**: 等待 5 秒后重试同一操作
- **次数**: 最多 1 次重试

### L2: 降级

- **触发**: L1 重试仍然失败
- **策略**: 更换导入方式
  - `file` 类型失败 → 读取文件内容，改用 `source_add(source_type="text", text=file_content)` 导入
  - `url` 类型失败 → 提示用户手动复制网页内容或提供本地保存的文件
- **限制**: text 类型有字符数限制（约 500K 字符），超大文件可能需要截断

### L3: 跳过

- **触发**: L2 降级仍然失败
- **策略**: 跳过该 source，在元数据 note 中记录 `import_status: "failed"`，附上错误信息
- **告知用户**: 列出跳过的文件及失败原因

---

## 元数据 Note 详细格式

`元数据-源材料清单` note 的完整 JSON 格式：

```json
{
  "topic": "LLM安全",
  "created_at": "2026-03-19",
  "notebook_id": "staging_notebook_id",
  "total_sources": 8,
  "successful_imports": 7,
  "failed_imports": 1,
  "sources": [
    {
      "index": 1,
      "source_id": "abc123",
      "original_path": "D:/papers/attention-is-all-you-need.pdf",
      "original_url": null,
      "source_type": "file",
      "filename": "attention-is-all-you-need.pdf",
      "import_status": "success",
      "recommended_variant": "学术论文版",
      "file_size_bytes": 1234567
    },
    {
      "index": 2,
      "source_id": "def456",
      "original_path": null,
      "original_url": "https://example.com/llm-safety-blog",
      "source_type": "url",
      "filename": null,
      "import_status": "success",
      "recommended_variant": "博客/观点文章版",
      "file_size_bytes": null
    },
    {
      "index": 3,
      "source_id": null,
      "original_path": "D:/papers/corrupted-file.pdf",
      "original_url": null,
      "source_type": "file",
      "filename": "corrupted-file.pdf",
      "import_status": "failed",
      "error": "L3: file unreadable after text fallback",
      "recommended_variant": null,
      "file_size_bytes": 0
    }
  ]
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `topic` | 用户提供的研究主题 |
| `created_at` | 创建日期（ISO 格式） |
| `notebook_id` | Staging notebook 的 NLM ID |
| `total_sources` | 尝试导入的总数 |
| `successful_imports` | 成功导入数 |
| `failed_imports` | 失败数 |
| `sources[].index` | 导入顺序序号 |
| `sources[].source_id` | NLM 分配的 source ID（失败时为 null） |
| `sources[].original_path` | 本地文件路径（URL 类型为 null） |
| `sources[].original_url` | URL 地址（文件类型为 null） |
| `sources[].import_status` | `success` / `failed` |
| `sources[].recommended_variant` | 推荐的分析 prompt 变体 |

---

## Source ID 映射更新流程

导入完成后需要更新元数据 note，因为 `source_add()` 返回的 source_id 可能不完整：

1. 调用 `notebook_get(notebook_id)` 获取 notebook 的完整信息
2. 从返回结果的 sources 列表中提取所有 `source_id` 和 `source_name`
3. 按 `source_name` 与元数据 note 中的 `filename` 匹配，更新 `source_id`
4. 调用 `note(action="update")` 更新元数据 note

这一步确保后续 Phase 2 逐篇分析时可以准确使用 `source_ids` 参数。
