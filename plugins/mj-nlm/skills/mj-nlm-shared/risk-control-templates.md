# Risk Control Templates — 来源充足性预检 + 幻觉防护

> 方法论文档 §10 风险控制的工程化落地。承载：来源/制品配比矩阵、默认幻觉防护约束句、高风险内容白名单、Source Check 模板。

## 1. 来源 vs 制品长度配比矩阵

build skill Phase 6（来源充足性预检）使用本表评估"已有 source 总字数"与"用户请求生成的制品类型"是否匹配。

| 来源总字数 | 推荐生成 | 警告（提示降级） | 禁止生成 |
|---|---|---|---|
| `< 5K` | flashcards / mind_map / data_table / report(Briefing Doc, short) | infographic / quiz / audio_brief | audio_long / video / slide_deck(detailed) |
| `5K – 30K` | 上述全部 + audio_brief / slide_deck(short) / report(Study Guide) | audio_long | video(long) |
| `30K – 100K` | 全部类型 | — | — |
| `> 100K` | 全部，但建议拆分为多个聚焦 notebook | — | — |

**字数计算口径**：所有 source 内容总字符数（含转换的代码 source 但不含元 source `00x`）。

**触发逻辑**：

```python
def assess_artifact_feasibility(total_chars: int, artifact_type: str, sub_params: dict) -> Verdict:
    if total_chars < 5000:
        forbidden = {"audio_long", "video", "slide_deck_detailed"}
        warned = {"infographic", "quiz", "audio_brief"}
    elif total_chars < 30000:
        forbidden = {"video_long"}
        warned = {"audio_long"}
    elif total_chars < 100000:
        forbidden, warned = set(), set()
    else:
        return SUGGEST_SPLIT
    
    key = f"{artifact_type}_{sub_params.get('length', 'default')}"
    if key in forbidden: return BLOCK
    if key in warned: return WARN_DOWNGRADE
    return ALLOW
```

**降级建议表**：

| 用户请求 | 来源不足时建议替代 |
|---|---|
| `audio_long` | `audio_brief` 或 `report(Briefing Doc)` |
| `video` | `infographic` 或 `slide_deck(short)` |
| `slide_deck(detailed)` | `slide_deck(short)` 或 `mind_map` |
| `quiz(question_count=20)` | `quiz(question_count=5)` 或 `flashcards` |

---

## 2. 默认幻觉防护约束句

所有 studio_create 调用的 `focus_prompt` 在拼接 Intent + Content 两层之后，**自动追加**以下固定约束（除非显式 `disable_guardrails=True`）：

```text

【约束】
- 所有关键判断必须引用具体来源（source 名称或章节）；来源中没有的内容请明确标注「推断」或「背景知识」。
- 不要编造来源中没有的案例、数据、人名、机构名、统计数字、年份。
- 如来源不足以支撑请求长度，请明确说"来源不足"，不要凑长度。
- 参考 notebook 中编号 `00c-定向-` 的领域定向报告，理解学习路径与适用边界；编号 `00a-导航-` 的导航大纲理解材料逻辑关系；编号 `00b-导航-` 的项目上下文理解知识库定位。
- 对于矛盾的来源，请并列呈现并标注分歧，不要选边或调和。
```

### 子参数：`disable_guardrails`

仅在以下场景可关闭：
- 用户明确为内部技术分享生成（受众已知来源、不会作为外部决策依据）
- 老 v1 prompt 兼容（迁移期）
- 测试场景

调用方式：

```python
studio_create(
    notebook_id=...,
    artifact_type="audio",
    focus_prompt=...,
    disable_guardrails=True,  # 跳过约束追加
    confirm=True
)
```

---

## 3. 高风险内容白名单（强制 Source Check）

以下场景**必须**在 studio 生成完成后，触发一次 query Mode E 来源核查（详见 `→ ./learning-loop-templates.md#来源核查交互提示词`）：

| 场景关键词 | 风险类别 | 强制核查理由 |
|---|---|---|
| 医疗 / 临床 / 用药 / 病例 | 医疗建议 | 错误信息可能直接危害健康 |
| 法律 / 合同 / 条款 / 案例 | 法律建议 | 错误条款解读可能造成法律风险 |
| 财务 / 投资 / 估值 / 税务 | 财务建议 | 错误计算或假设导致经济损失 |
| 考试 / 标准 / 认证 / 评分 | 考试规则 | NotebookLM 易混淆相似考点 |
| 安全 / 漏洞 / 攻击 / 渗透 | 安全建议 | 错误防护方案可能引入漏洞 |

**触发方式**：build skill Phase 7 生成领域定向报告后，扫描 source 标题与摘要中的关键词，匹配则在 notebook 元数据 Note 中标记 `risk_class=high`。learn orchestrator 在 P9（来源核查阶段）检测到此标记则不允许跳过。

---

## 4. Source Check 提示词模板

query skill Mode E（来源核查）使用以下 prompt 让 NLM 对上一轮回答中的关键结论逐条标注：

```text
【任务】对以下结论列表，逐条标注其在本 notebook 来源中的依据等级。

【结论列表】
{结论列表，每条单独编号}

【输出格式】每条结论一行：
[编号] [等级] | 来源章节或推断说明
等级取值：
- DIRECT：在来源中有明确陈述（给出 source 名称 + 章节/段落定位）
- INFERRED：来源中有支持证据，但结论是综合推断（说明推断链）
- BACKGROUND：基于一般背景知识，来源中没有直接依据
- UNCERTAIN：来源信息不足以判断
- CONTRADICTED：来源中有相反证据（指出矛盾点）

【约束】
- 不要重新陈述结论，只标注等级和依据
- 等级判断必须严格，宁可标 UNCERTAIN 也不要拔高到 DIRECT
- 一条结论可以引用多个 source（用逗号分隔）
```

**消费**：query skill 解析 NLM 返回，统计「DIRECT 占比」作为「来源核查通过率」指标，回填 `understanding-metrics.md` 的指标 6。

---

## 5. 来源/制品配比预检报告模板

build skill Phase 6 预检结果作为 `00d-预检-来源充足性报告` Source 入库，模板：

```markdown
# 来源充足性报告 — {notebook_name}

## 来源统计
- Source 总数：{count}（含 {meta_count} 个元 source）
- 内容总字数：{total_chars}（不含元 source）
- 平均每 source：{avg_chars} 字符
- 最大 source：{max_chars} 字符（{max_source_name}）
- 最小 source：{min_chars} 字符（{min_source_name}）

## 来源类型分布
- 直传文件（pdf/md/txt）：{n} 个
- 转换文件（py/sql/yaml）：{n} 个
- 网页/YouTube：{n} 个

## 制品可行性矩阵

| 制品类型 | 评估 | 建议 |
|---|---|---|
| audio_brief | ✅ 推荐 / ⚠️ 警告 / ❌ 禁止 | {建议} |
| audio_long | ... | ... |
| video | ... | ... |
| slide_deck_short | ... | ... |
| slide_deck_detailed | ... | ... |
| infographic | ... | ... |
| report_briefing | ... | ... |
| report_study_guide | ... | ... |
| flashcards | ... | ... |
| quiz | ... | ... |
| data_table | ... | ... |
| mind_map | ... | ... |

## 风险类别
- 高风险标记：{risk_class}（none / high）
- 触发关键词：{keywords or "—"}

## 后续建议
{基于矩阵的下一步建议，如"建议先生成 mind_map 与 flashcards 验证来源覆盖度"}
```

---

## 6. 配额与成本提示

→ 详见独立文档：[`./quota-estimation.md`](./quota-estimation.md)（v2.3 起）

该文档覆盖：单调用耗时基线 / 双 wrapper（learn-make + learn-test）配额预告 / build / studio / query 单步耗时 / NotebookLM 公开+经验配额。

各 skill 在 Phase 0 preflight 通过后，必须按 quota-estimation.md 给出的总耗时报告模板告知用户预计耗时。
