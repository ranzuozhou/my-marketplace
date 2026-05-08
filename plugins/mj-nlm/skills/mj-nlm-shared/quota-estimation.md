# NLM Quota & Time Estimation — 配额与耗时预告（v2.3）

> mj-nlm 大多数操作通过 NotebookLM 的网络/AI 调用完成，单次 wrapper 可能消耗 5-30 分钟。Phase 0 的 preflight 通过后，必须告知用户预计耗时与调用次数，让用户决定是否启动、是否后台等。
>
> v2.3 把原 risk-control-templates.md §6 抽出独立成文，并扩展为双 wrapper（learn-make + learn-test）口径。

## 单调用耗时基线

> 实测中位值；上下浮动 ±50% 取决于 source 数 / 网络 / NLM 当前负载。

### 一次性调用（每次 invoke 一次）

| 调用 | 中位耗时 | 备注 |
|---|---|---|
| `notebook_list` | ~2 秒 | preflight L2 用 |
| `notebook_describe` | ~3 秒 | preflight L3 用 |
| `notebook_create` | ~5 秒 | build Phase 1 |
| `notebook_query`（一次问答） | ~30 秒 | 含 NLM 检索 + 生成 |
| `studio_create` 启动 | ~2 秒 | 异步任务，不算生成耗时 |
| `studio_status`（轮询） | ~1 秒 / 次 | 通常每 5 秒轮一次 |
| `tag` / `note` CRUD | ~2 秒 | |

### Per-source（导入）

| 调用 | 中位耗时 | 备注 |
|---|---|---|
| `source_add` (file) | 10-30 秒 | 视文件大小 |
| `source_add` (url) | ~15 秒 | NLM 自爬 |
| `source_add` (drive) | 10-20 秒 | NLM 内调 Drive API |

### Per-artifact（studio_create 完成时长）

> 从 `studio_create` 启动到 `studio_status=COMPLETED` 的总时长。

| Artifact 类型 | 中位耗时 | 备注 |
|---|---|---|
| `mind_map` | ~30 秒 | 最快 |
| `quiz` | ~30 秒 | |
| `flashcards` | ~30 秒 | |
| `data_table` | ~45 秒 | |
| `infographic` | ~45 秒 | |
| `report` | ~60 秒 | 含 briefing doc 拼装 |
| `slide_deck` | ~2 分钟 | NLM 渲染图片层耗时 |
| `audio` | ~3 分钟 | TTS 合成 |
| `video` | ~3 分钟 | NLM 视频合成（与 audio 接近） |

`--triple-view` 三版生成 = 单制品类型 × 3 倍耗时。

---

## Wrapper 级配额预告

### `/mj-nlm:learn-make <topic>`（v2.2 新增 wrapper 1）

**Phase 0 的 preflight 通过后，按用户多选的制品组合显示**：

```
预计执行：
  build phase: 1 × notebook_create + N × source_add + 1 × notebook_query (00c 定向)
                ≈ 5 秒 + N × 15 秒 + 30 秒  [N = source 数]
  studio phase: M × studio_create + M × studio_status × ~6 次轮询
                ≈ M 个制品对应耗时之和（见上表）

总耗时（默认全 7 类制品 + 12 sources）：
  build: ~3 分钟
  studio (7 制品默认 default view):
    mind_map (30s) + video (3min) + slide_deck (2min) + audio (3min) +
    report (1min) + infographic (45s) + data_table (45s)
  ≈ 11 分钟
  ───
  合计 ≈ 14 分钟
```

**`--triple-view` 加成**：studio 部分 × 3 倍 → 总耗时约 36-40 分钟。

**`--with-download` 加成**：每个 artifact 多 ~10-30 秒下载（大约总加 1-3 分钟）。

### `/mj-nlm:learn-test <notebook_id>`（v2.2 新增 wrapper 2）

```
预计执行（默认勾 quiz + flashcards 锁定）：
  Phase 2a: 2 × studio_create
            ≈ 2 × 30 秒 = 1 分钟

如选 --rootcause:
  Phase 2b: notebook_query × 错题数（视用户实测）
            ≈ 错题数 × 30 秒  [一般 3-5 题，约 90-150 秒]

如选 --selfcheck:
  Phase 2c: 1 × notebook_query (Mode F) + 1 × note_create
            ≈ 30 秒 + 2 秒 = ~30 秒

如选 --sourcecheck:
  Phase 2d: 1 × notebook_query (Mode E)
            ≈ 30 秒

总耗时:
  默认（quiz + flashcards 锁定）: ~1 分钟
  --full（5 类全开 + 假设 5 错题）: ~5 分钟
```

### `/mj-nlm:build <topic>`（底层）

```
build skill 单步执行（无 wrapper）：
  notebook_create + N × source_add + 4 × note_create (00a/00b/00d/00c) + 2 × notebook_query (P6/P7)
  ≈ 5 秒 + N × 15 秒 + 8 秒 + 60 秒  [N = source 数]

中位场景（12 sources）：
  ≈ 5 + 180 + 8 + 60 = ~4 分钟
```

### `/mj-nlm:studio <notebook_id>`（底层）

单次单制品：见上方 [Per-artifact](#per-artifactstudio_create-完成时长) 表。

### `/mj-nlm:query <notebook_id>`（底层）

| Mode | 中位耗时 | 备注 |
|---|---|---|
| A 单库问答 | ~30 秒 | 1 × notebook_query |
| B 跨库问答 | ~60 秒 | 多 notebook 并行 |
| C Deep Research | ~5 分钟 | NLM 深度模式 |
| D Quiz Root Cause | ~30 秒 / 错题 | per 错题 1 query |
| E Source Check | ~30 秒 | 1 × notebook_query |
| F Understanding Self-Check | ~60 秒 | 1 query + 1 note_create |

---

## 总耗时报告模板（用于 Phase 0 输出）

各 skill 在 preflight 通过后、Phase 1 启动前，建议输出如下结构供用户决策：

```
预计耗时与调用：
  - 总时长：~XX 分钟（中位）；最坏 +50%
  - MCP 调用：N 次（含 source_add × A / studio_create × B / notebook_query × C）
  - 后台等待为主，可挂起；中途中断会丢失未持久化状态
  - 配额提示：NotebookLM 当日 source 上传限额约 50（公布的软上限），未公布的 studio_create 限额按"每天勿连续生成 20+ 制品"经验保守

是否继续？(y / n / 跳到 Phase 2 多选改组合)
```

---

## NotebookLM 公开/经验配额

| 项目 | 值 | 来源 |
|---|---|---|
| 单 notebook source 上限 | 300 | NotebookLM Plus 文档 |
| 单 notebook 制品 (studio) 上限 | 未公布 | 经验：单 notebook 累 50+ 制品后开始拒绝 |
| 单日 source 上传 | ~50 | 经验软限 |
| 单日 studio_create | 未公布 | 经验：连续 20+ 后开始失败 |
| query rate limit | ~10 / min | 经验，超过会被节流 ~30 秒 |
| 单文件大小 | 200MB | NotebookLM 上传限 |
| 单 source 字数限 | ~500K 字 | 超过会被截 |

> 经验值来自 mj-nlm v1-v2.2 实测；NLM 未公布精确数字。

---

## Reference

- `→ ./preflight-checklist.md` — preflight 三级（Auth / MCP health / Notebook scope），通过后才显示本表
- `→ ./artifact-type-reference.md` — 9 种 artifact_type 详细定义
- `→ ./risk-control-templates.md` — 来源 / 制品配比矩阵 + 幻觉防护
