# 分库逻辑详情

本文档包含 flora-ptm-synthesize Phase 3 智能分库的详细决策逻辑。

---

## 分库数量决策

基于 Phase 1 关系分析的聚类结果中的实际组数 N 直接决定目标 notebook 数量：

| 聚类组数 N | 目标 notebook 数 | 处理方式 |
|-----------|-----------------|----------|
| N = 1 | 1 | 所有报告归入同一 notebook |
| N = 2 | 2 | 每组各自一个 notebook |
| N = 3 | 3 | 每组各自一个 notebook |
| N > 3 | 3 | 合并最相似的组至 3 组以内 |

### 合并策略（N > 3 时）

当聚类产生超过 3 个组时，需要合并：

1. **相似度判断**: 从关系分析的「观点对比」和「方法论对比」部分，识别哪些组之间有最强的互补或递进关系
2. **合并优先级**: 优先合并
   - 方法论相近的组
   - 有递进关系（基础→应用）的组
   - 报告数量最少的组（归入最相关的大组）
3. **用户覆盖**: 合并结果在 Phase 4 展示，用户可以调整

---

## Source 数量计算

每个目标 notebook 的 source 总数 = 原始报告数 + meta-knowledge 数

### Meta-knowledge 数量（固定部分）

| 类型 | 数量 | 说明 |
|------|------|------|
| 精简短文 | = 该组原始报告数 | 每篇报告一个 |
| 综述 | 1 | 跨文献综述（所有 notebook 共享同一份） |
| 关系分析 | 1 | 关系分析（所有 notebook 共享同一份） |

### 计算公式

```
target_sources = original_reports + original_reports + 2
               = 2 × original_reports + 2
```

其中：
- `original_reports` = 该组包含的原始报告数
- 第一个 `original_reports` = 原始文件/URL 重新导入
- 第二个 `original_reports` = 每篇的精简短文（text source）
- `2` = 综述 + 关系分析（text source）

### 安全上限

| 阈值 | 说明 |
|------|------|
| 45 | 每个 notebook 的 source 上限（NLM 限制 50，留 5 余量） |
| 21 | 每组最大原始报告数（`2 × 21 + 2 = 44 < 45`） |

---

## 超限处理

### 场景 1: 单组超限

如果 N = 1 且原始报告数 > 21：

1. **尝试拆分为 2 组**: 调用 `notebook_query()` 要求按子主题将报告拆分为 2 组
2. 若拆分后每组仍超限 → 拆分为 3 组
3. 若 3 组仍超限 → 提示用户精简（移除低优先级报告）

### 场景 2: 多组中某组超限

如果某个组的原始报告数 > 21：

1. 将该组进一步拆分为子组
2. 子组数量 = ceil(原始报告数 / 21)
3. 总 notebook 数不超过 3：若拆分导致超出 3 个 → 提示用户精简

### 场景 3: 用户调整导致超限

用户在 Phase 4 调整分组后，重新计算每个 notebook 的 source 数。超限时立即警告并建议调整。

---

## 导航笔记内容

每个目标 notebook 创建一个导航笔记（不是 text source，而是 note），内容包含：

### 模板

```markdown
# 导航 — {topic}/{subtopic}

## Source 来源映射

| 序号 | Source 名称 | 原始来源 | 类别 |
|------|------------|---------|------|
| 1 | {source_name} | {original_path_or_url} | 原文 |
| 2 | 00a-精简-{name} | （精简短文） | 精简 |
| ... | 00b-综述-{topic} | （跨文献综述） | 综述 |
| ... | 00c-关系-{topic} | （关系分析） | 关系 |

## 推荐阅读顺序

1. 先读 `00b-综述-{topic}` — 建立全局视角
2. 再读 `00c-关系-{topic}` — 理解报告间关系
3. 按兴趣选读 `00a-精简-*` — 了解各篇要点
4. 最后深读感兴趣的原文 source

## 本库主题概要

{subtopic 的一句话描述，来自聚类分析}
```

---

## 边界情况

| 情况 | 处理 |
|------|------|
| 只有 1 篇报告 | N=1，单一 notebook，跳过关系分析和聚类 |
| 2 篇报告 | N=1（通常），除非用户明确要求分库 |
| 所有报告主题完全不同 | N = 报告数（但上限 3），合并最不相关的组 |
| 元数据 note 中有失败的 source | 跳过失败 source，仅重新导入成功的 |
| 精简短文 note 缺失 | 警告用户，建议重新运行 `/flora-ptm:digest` Phase 2 |

---

## 执行顺序

Phase 4 执行分库时，按以下顺序操作每个目标 notebook：

1. `notebook_create(title="FLORA-{topic}-{subtopic}-{YYYYMMDD}")`
2. 逐个重新导入原始 source（从元数据 note 读取路径/URL）
   - 使用与 digest 相同的错误处理策略（L1→L2→L3）
3. 逐个添加精简短文作为 text source
   - 读取 Staging notebook 中的 `精简-*` note 内容
   - `source_add(source_type="text", text=content)` 命名为 `00a-精简-{name}`
4. 添加综述和关系分析作为 text source
5. 创建导航笔记 `note(action="create")`
6. 打标签 `tag(action="add", tags="flora,target,{topic},{subtopic}")`
7. 校验 source 总数（`notebook_get()` 确认）
