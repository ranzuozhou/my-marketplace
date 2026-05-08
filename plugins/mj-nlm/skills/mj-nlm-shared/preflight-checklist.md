# NLM Preflight Checklist — 启动冒烟检查（v2.3）

> mj-nlm 任何一个 skill 在 Phase 0 进入业务流程前都应跑一次轻量 preflight，避免用户走完一半才命中认证 / 服务问题。
>
> v2.3 把这套 checklist 显式化，统一规范"什么算可以推进 Phase 1"。

## 目的

mj-nlm 的子 skill 大多耗时长（build 含 source 导入；studio 制品 30s-3min；wrapper 一次跑 7+ 调用）。**任何在 Phase 0 没发现的故障，都会在用户已等了 1-10 分钟后才暴露**——这是 v2.0/v2.1 学习闭环卡 Phase 7 的根因。

preflight 把"硬故障检测"前移到 Phase 0：花 ~5 秒确认 token + MCP 健康，再决定是否进 Phase 1。

## 三级 Preflight

### Level 1 — Auth Token（强制，所有 skill）

| 检查 | 命令 | 通过条件 |
|---|---|---|
| Token 状态 | `mj-nlm-mcp__refresh_auth()` 等价的 status 调用 | 返回 OK；token 未过期 |

失败处理：
- 立即退出，引导 `/mj-nlm:auth`（按 auth skill troubleshooting 修复）
- **不**自动尝试 refresh（避免吞掉用户应该看到的认证错误）

### Level 2 — NLM Service Health（强制，所有 skill）

| 检查 | 命令 | 通过条件 |
|---|---|---|
| MCP 进程在跑 | `mj-nlm-mcp__server_info()` | 返回 server metadata |
| 列 notebook 权限可用 | `mj-nlm-mcp__notebook_list()` | 返回 200 + notebook 数组（即使空数组也算通过） |

失败处理：
- `server_info` 失败 → 提示用户重启 MCP（`uv tool reinstall notebooklm-mcp-cli` 或 `nlm login`）
- `notebook_list` PERMISSION_DENIED → 引导 `/mj-nlm:auth`
- `notebook_list` 其他错误 → 报告原始错误，让用户判断

### Level 3 — Notebook-scoped Health（条件，仅当 skill 已知 notebook_id）

| 检查 | 命令 | 通过条件 |
|---|---|---|
| 该 notebook 可读 | `mj-nlm-mcp__notebook_describe(notebook_id)` | 返回 notebook metadata |
| query 权限可用（高敏感场景） | `mj-nlm-mcp__notebook_query(notebook_id, "ping")` 或类似 noop | 返回 ≥1 字符串响应（不关心内容） |

失败处理：
- notebook_describe NOT_FOUND → 让用户确认 notebook_id；可能是用户记错或 notebook 被删
- notebook_query PERMISSION_DENIED → 这是 v2.0 学习闭环卡 Phase 7 的典型故障；走 `/mj-nlm:auth` 重新认证

**何时触发 Level 3**：
- `learn-make --resume <notebook_id>`（必须确认 resume 目标可达）
- `learn-test <notebook_id>`（必须确认 quiz 调度对象可达）
- query / studio / manage 直接传 notebook_id 入参时（已有现行 Phase 0 逻辑覆盖，本 checklist 是规范化）

---

## 缓存策略（v2.4.1 诚实化）

> v2.4 设计文档原本写"5min TTL 缓存 + 内存级 dict"——v2.4.1 调研后确认这是 Claude conversation 自然 memory，不是真实现的技术 cache。本节澄清实际机制与单调用真实开销。

### 实际机制

- **同 turn 内**：Claude 已知刚跑过 preflight，不会重复跑（自然 LLM behavior，无需 prompt 强制）
- **跨 turn / 跨 skill 调用**：preflight 重新执行；用户在 Claude Code 一个 session 内多次调用 `/mj-nlm:learn-make` / `/mj-nlm:build` 等，每次进 Phase 0 都会重跑一次

### 单调用真实开销（v2.4.1 调研结论）

| 工具 | 性质 | 中位耗时 | 缓存价值 |
|---|---|---|---|
| `server_info` | LOCAL check（不发 Google API） | 毫秒级 | 极低 |
| `refresh_auth` | disk reload（仅 Chrome headless 触发时慢） | 毫秒级（命中 disk） | 极低 |
| `notebook_list` | live Google API | 1-3 秒 | 中等，但有副作用 |

**为什么不实现真 5min TTL 缓存**（v2.5 候选 abandoned 决策记录）：

1. server_info / refresh_auth 真实开销可忽略，缓存收益≈0
2. notebook_list 真有开销，但它是用户**日常 API**（不只用于 preflight）；缓存它会让刚建/刚删的 notebook 反映不准确，副作用大于收益
3. 真实现需要 fork [`notebooklm-mcp-cli`](https://github.com/jacob-bd/notebooklm-mcp-cli)（v0.6.5，活跃开发）+ 加 cache 层 + 维护 fork——长尾成本高
4. 跨 turn 重跑的实际用户体验影响小：notebook_list 1-3 秒 + L1/L2 毫秒级 = 单次 ≤ 4 秒；wrapper 总耗时本来就在 12-40 分钟量级

### 强制重跑

由于不存在技术 cache，无需 `--force-recheck` flag——跨 turn 自动重跑。同 turn 内若用户切了账号（`nlm login switch`），调一次 `/mj-nlm:auth` 即可在 Claude conversation 中刷新认知。

---

## 集成点（v2.3 文档化 / v2.4 实施落地）

| Skill | 触发位置 | 默认级别 | v2.4 实施状态 |
|---|---|---|---|
| `mj-nlm:auth` | 已有完整自查流程，不需 preflight | — | — |
| `mj-nlm:build` | Phase 0（替代原 Auth Check） | L1 + L2 | ✅ 显式 Phase 0 段 + 三 H-point (H0a/b/c) |
| `mj-nlm:manage` | Phase 0（Workflow 后插入） | L1 + L2 | ✅ 显式 Phase 0 段 |
| `mj-nlm:query` | Phase 0；L3 由 Phase 1 首次 query 隐式覆盖 | L1 + L2 + (L3 条件) | ✅ 显式 Phase 0 段 |
| `mj-nlm:studio` | Phase 0；L3 由 Phase 1 `notebook_describe` 隐式覆盖 | L1 + L2 + L3 | ✅ 显式 Phase 0 段 |
| `mj-nlm:learn-make` | Phase 0 Notebook Locate 前置注解（隐式 preflight） | L1 + L2 + (L3 条件) | ✅ 注解 + 委托 build/studio 子 skill 完整 preflight |
| `mj-nlm:learn-test` | Phase 0 Notebook Locate 前置注解（隐式 preflight） | L1 + L2 + L3 | ✅ 注解 + 委托 studio/query 子 skill 完整 preflight |

---

## H-Point 模板（嵌入各 skill 的 Phase 0）

```markdown
### Phase 0: Preflight Check

| Level | 检查 | 工具 | 期望 |
|---|---|---|---|
| L1 | Auth token | refresh_auth status | OK |
| L2a | MCP server | server_info | metadata |
| L2b | Notebook list | notebook_list | 200 + array |
| L3* | Notebook reachable | notebook_describe(<id>) | metadata |
| L3* | Query permission | notebook_query(<id>, ping) | response |

*L3 仅当 skill 入参带 notebook_id 时触发。

| H | 触发 | 行为 |
|---|---|---|
| **H0a** | L1 fail | Hard block → `/mj-nlm:auth` |
| **H0b** | L2a fail | Hard block → 用户重启 MCP |
| **H0c** | L2b PERMISSION_DENIED | Hard block → `/mj-nlm:auth` |
| **H0d** | L2b 其他错误 | Soft warn → 报错 + 用户判断是否继续 |
| **H0e** | L3 NOT_FOUND | Hard block → 用户确认 notebook_id |
| **H0f** | L3 PERMISSION_DENIED | Hard block → `/mj-nlm:auth`（典型 token scope 问题） |

通过条件：L1 + L2 全 OK，L3（如触发）也 OK → 进 Phase 1。
```

---

## Reference

- `→ ../mj-nlm-auth/SKILL.md` — Level 1/2 失败时的修复路径
- `→ ./quota-estimation.md` — preflight 通过后给用户的耗时预告（互补：preflight 防故障 / quota 防意外）
