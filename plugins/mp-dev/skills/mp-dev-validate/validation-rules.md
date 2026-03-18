# Validation Rules Reference

mp-dev:validate 技能的校验规则参考文件。定义 V1-V7 共 7 条校验规则，镜像 CI `.github/workflows/ci.yml` 检查。

---

## 校验规则总表

| 规则 | 名称 | 类型 | 说明 |
|------|------|------|------|
| **V1** | plugin.json schema | 自动 | 验证 plugin.json 必填字段 |
| **V2** | Directory structure | 自动 | 验证目录结构完整性 |
| **V3** | SKILL.md frontmatter | 自动 | 验证 frontmatter 的 name + description |
| **V4** | marketplace.json consistency | 自动 | 验证 marketplace.json 与实际目录一致 |
| **V5** | Version sync | 自动 | 验证 VERSION ↔ marketplace.json ↔ plugin.json 版本同步 |
| **V6** | CHANGELOG existence | 自动 | 验证 CHANGELOG.md 存在 |
| **V7** | Trigger word quality | 判断 | 验证触发词数量、长度、独立性 |

---

## V1: plugin.json Schema

**检查目标**：`plugins/<name>/.claude-plugin/plugin.json`

**必填字段**（6 个）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 插件名称 |
| `description` | string | 插件描述 |
| `version` | string | 语义化版本号 |
| `author` | object | 作者信息（含 `name` 子字段） |
| `license` | string | 开源协议 |
| `skills` | string | 技能目录路径 |

**错误信息模板**：
```
[V1][FAIL] plugins/<name>/.claude-plugin/plugin.json missing required field: <field>
```

---

## V2: Directory Structure

**检查目标**：每个 `plugins/<name>/` 目录

**必须存在的项目**（5 项）：

| 项目 | 类型 | 路径 |
|------|------|------|
| plugin.json | 文件 | `.claude-plugin/plugin.json` |
| CLAUDE.md | 文件 | `CLAUDE.md` |
| README.md | 文件 | `README.md` |
| CHANGELOG.md | 文件 | `CHANGELOG.md` |
| skills 目录 | 目录 | `skills/` |

**错误信息模板**：
```
[V2][FAIL] plugins/<name> missing required file: <item>
[V2][FAIL] plugins/<name> missing required directory: skills
```

---

## V3: SKILL.md Frontmatter

**检查目标**：`plugins/<name>/skills/<skill-dir>/SKILL.md`

**跳过规则**：目录名以 `-shared` 结尾的跳过（共享资源目录，不含 SKILL.md）。

**必填 frontmatter 字段**：

| 字段 | 验证方式 |
|------|---------|
| `name:` | 文件前 20 行内包含 `^name:` |
| `description:` | 文件前 20 行内包含 `^description:` |

**错误信息模板**：
```
[V3][FAIL] plugins/<name>/skills/<skill-dir>/SKILL.md missing frontmatter field: <field>
[V3][FAIL] plugins/<name>/skills/<skill-dir>/ missing SKILL.md
[V3][SKIP] plugins/<name>/skills/<shared-dir>/ (shared resource, not a skill)
```

---

## V4: marketplace.json Consistency

**检查目标**：`.claude-plugin/marketplace.json`

**检查项**：
1. marketplace.json 必须包含字段：`name`, `owner`, `metadata`, `plugins`
2. `plugins` 数组中每个条目的 `name` 必须对应存在 `plugins/<name>/` 目录

**错误信息模板**：
```
[V4][FAIL] marketplace.json missing required field: <field>
[V4][FAIL] marketplace.json references plugin '<name>' but directory plugins/<name>/ not found
```

---

## V5: Version Sync

**检查目标**：VERSION 文件、marketplace.json、各 plugin.json

**同步规则**：

| 比较对 | 说明 |
|--------|------|
| `VERSION` ↔ `marketplace.json metadata.version` | 仓库级版本 |
| `plugins/<name>/.claude-plugin/plugin.json version` ↔ `marketplace.json plugins[name].version` | 插件级版本 |

**错误信息模板**：
```
[V5][FAIL] VERSION (<v1>) != marketplace.json metadata.version (<v2>)
[V5][FAIL] <name> plugin.json (<v1>) != marketplace.json plugins[<name>].version (<v2>)
```

---

## V6: CHANGELOG Existence

**检查目标**：根目录和各插件目录

**必须存在**：
- `CHANGELOG.md`（根目录）
- `plugins/<name>/CHANGELOG.md`（每个插件目录）

**错误信息模板**：
```
[V6][FAIL] Root CHANGELOG.md not found
[V6][FAIL] plugins/<name>/CHANGELOG.md not found
```

---

## V7: Trigger Word Quality（判断型检查）

**检查目标**：各 SKILL.md 的 `description` 字段内容

**质量要求**：

| 维度 | 要求 | 判断方式 |
|------|------|---------|
| 中文触发词 | >= 3 个 | Claude 阅读 description，识别中文短语 |
| 英文触发词 | >= 3 个 | Claude 阅读 description，识别英文短语 |
| 字符长度 | 50-300 字符 | 字符计数 |
| 独立性 | 不与同 plugin 内其他 skill 重叠 | Claude 对比多个 SKILL.md 的触发词 |

**输出格式**：
```
[V7][PASS] <skill-name>: 中文触发词 N 个，英文触发词 N 个，长度 N 字符
[V7][WARN] <skill-name>: 中文触发词不足 3 个（当前 N 个）
[V7][WARN] <skill-name>: description 长度 N 字符，建议 50-300 字符
[V7][WARN] <skill-name> 与 <other-skill> 触发词重叠：<重叠词>
```

> V7 为判断型检查，由 Claude 阅读 SKILL.md 后给出评估，不由 validate_plugin.py 自动化。

---

## --scope 参数行为

| 参数 | 行为 |
|------|------|
| 无（默认） | 检查所有 plugins 目录 + 根目录 |
| `--scope <plugin-name>` | 仅检查指定 plugin 的 V1-V3、V5（plugin 级）、V6（plugin 级） |
| `--scope marketplace` | 仅检查 V4、V5（仓库级）、V6（根目录） |

---

## 输出格式

```
╔══════════════════════════════════════════════╗
║  mp-dev:validate — 结构校验报告              ║
╠══════════════════════════════════════════════╣
║  Scope: all / <plugin-name>                  ║
╠═════╤═══════════════════════╤════════════════╣
║  ID │ 检查项                │ 结果           ║
╠═════╪═══════════════════════╪════════════════╣
║  V1 │ plugin.json schema    │ PASS / FAIL    ║
║  V2 │ Directory structure   │ PASS / FAIL    ║
║  V3 │ SKILL.md frontmatter  │ PASS / FAIL    ║
║  V4 │ marketplace.json      │ PASS / FAIL    ║
║  V5 │ Version sync          │ PASS / FAIL    ║
║  V6 │ CHANGELOG existence   │ PASS / FAIL    ║
║  V7 │ Trigger word quality  │ PASS / WARN    ║
╠═════╧═══════════════════════╧════════════════╣
║  总计: N PASS / N FAIL / N WARN             ║
╚══════════════════════════════════════════════╝
```

FAIL 项附带详细错误信息。
