# Question Patterns Reference

mp-dev 共享交互模式参考文件。定义 4 种交互模式及其模板，供所有 mp-dev skill 使用。

---

## 4 种交互模式

| 模式 | 名称 | 用途 | 使用场景 |
|------|------|------|---------|
| **P1** | Information Collection | 收集必要信息 | scaffold（名称、描述、技能列表）、skill-author（目标 plugin、skill 名）、release（scope） |
| **P2** | Scope Confirmation | 确认操作范围 | validate（--scope）、changelog（层级判断）、release（scope 确认）、test（阶段选择） |
| **P3** | Destructive Confirmation | 破坏性操作确认 | test Phase 2（源切换）、release Step 2（版本写入）、scaffold（覆盖已有文件） |
| **P4** | Result Display | 结果展示 | validate（校验报告）、changelog（生成的条目）、release（发布摘要）、scaffold（创建摘要） |

---

## P1: Information Collection 信息收集

**用途**：在执行操作前，收集用户尚未提供的必要信息。

**模板**：

```
需要补充以下信息：

| 项目 | 当前值 | 需要 |
|------|--------|------|
| <参数1> | <已知值 或 "未提供"> | <说明> |
| <参数2> | <已知值 或 "未提供"> | <说明> |

请提供缺失的信息，或输入 "默认" 使用默认值。
默认值：<列出默认值>
```

**使用 AskUserQuestion**：当信息不足时，通过 AskUserQuestion 收集，一次收集所有缺失信息（避免多轮追问）。

**示例（scaffold）**：

```
需要补充以下信息：

| 项目 | 当前值 | 需要 |
|------|--------|------|
| 插件名称 | 未提供 | 如 mp-xxx |
| 插件描述 | 未提供 | 中文，50-150 字符 |
| 技能列表 | 未提供 | 逗号分隔，如 "auth, build, query" |

请提供缺失的信息。
默认值：version=1.0.0, author=ranzuozhou, license=MIT
```

---

## P2: Scope Confirmation 范围确认

**用途**：确认操作影响的范围，避免误操作。

**模板**：

```
操作范围确认：

  范围: <scope 值>
  影响: <受影响的文件/目录列表>

确认以上范围？(Y/n)
```

**示例（validate）**：

```
操作范围确认：

  范围: mp-dev
  影响:
    - plugins/mp-dev/.claude-plugin/plugin.json (V1)
    - plugins/mp-dev/ 目录结构 (V2)
    - plugins/mp-dev/skills/*/SKILL.md (V3)
    - plugins/mp-dev/CHANGELOG.md (V6)

确认以上范围？(Y/n)
```

---

## P3: Destructive Confirmation 破坏性确认

**用途**：执行不可逆或有风险的操作前，要求用户明确确认。

**Hard Block**：必须等待用户明确输入确认词才继续。不可自动跳过。

**模板**：

```
⚠ 即将执行破坏性操作：

  操作: <操作描述>
  影响: <影响描述>
  风险: <风险说明>

此操作不可自动恢复。请输入 "确认执行" 继续，或输入 "取消" 放弃。
```

**示例（release Step 2）**：

```
⚠ 即将执行破坏性操作：

  操作: 写入版本号 1.0.0 → 1.1.0
  影响:
    - plugins/mp-dev/.claude-plugin/plugin.json
    - .claude-plugin/marketplace.json
  风险: 版本号写入后需要 git 操作才能回滚

DryRun 结果已展示。请输入 "确认执行" 继续，或输入 "取消" 放弃。
```

**示例（test Phase 2）**：

```
⚠ 即将执行破坏性操作：

  操作: 切换 Claude Code plugin 源到本地
  影响: ~/.claude/plugins/sources.json
  风险: 影响当前 Claude Code 的 plugin 加载

已创建备份。请输入 "确认执行" 继续，或输入 "取消" 放弃。
```

---

## P4: Result Display 结果展示

**用途**：操作完成后，展示结构化的结果摘要。

**模板**：

```
<操作名称> 完成

<结构化结果>

下一步:
  - <推荐操作 1> → /<skill-command>
  - <推荐操作 2> → /<skill-command>
```

**示例（scaffold）**：

```
插件脚手架创建完成

  插件名称: mp-example
  目录:     plugins/mp-example/
  文件:
    ✓ .claude-plugin/plugin.json
    ✓ CLAUDE.md
    ✓ README.md
    ✓ CHANGELOG.md
    ✓ skills/mp-example-auth/SKILL.md
    ✓ skills/mp-example-query/SKILL.md
    ✓ skills/mp-example-shared/
  注册:     marketplace.json 已更新

下一步:
  - 编写 SKILL.md → /mp-dev:skill-author
  - 校验结构   → /mp-dev:validate
```

**示例（validate）**：

```
结构校验完成

  Scope: all
  结果: 7 PASS / 0 FAIL / 1 WARN

  V1 plugin.json schema     PASS
  V2 Directory structure     PASS
  V3 SKILL.md frontmatter   PASS
  V4 marketplace.json       PASS
  V5 Version sync           PASS
  V6 CHANGELOG existence    PASS
  V7 Trigger word quality   WARN  (mp-dev-test: 英文触发词仅 2 个)

下一步:
  - 修复 WARN 项 → /mp-dev:skill-author
  - 开始测试     → /mp-dev:test
```

---

## 跨 Skill 使用矩阵

| 模式 | scaffold | skill-author | validate | test | changelog | release |
|------|----------|-------------|----------|------|-----------|---------|
| **P1** Information Collection | ✓ | ✓ | - | - | - | ✓ |
| **P2** Scope Confirmation | - | - | ✓ | ✓ | ✓ | ✓ |
| **P3** Destructive Confirmation | ✓* | - | - | ✓ | - | ✓ |
| **P4** Result Display | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

*scaffold 的 P3 仅在覆盖已有文件时触发。
