# Auth Troubleshooting — NLM 认证故障排查

## 常见错误对照表

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Authentication required` | 未登录或 token 过期 | `refresh_auth()` → `nlm login` |
| `Invalid credentials` | Token 无效 | `nlm login` 重新登录 |
| `Permission denied` | 账号无权限 | 确认 Google 账号有 NLM 访问权限 |
| `Network error` / `Connection refused` | MCP 服务未启动 | 检查 MCP 服务配置，重启 Claude Code |
| `Rate limited` | 请求频率过高 | 等待 1 分钟后重试 |
| `Server error (500)` | NLM 服务端问题 | 等待后重试，或检查 Google 服务状态 |

---

## 降级路径详解

### Level 1: refresh_auth()

**适用场景**：Token 过期但 session cookie 仍有效（通常 1-2 小时内过期的情况）。

**执行**：
```
refresh_auth()
```

**成功标志**：返回无错误信息。

**失败后**：进入 Level 2。

---

### Level 2: nlm login（CLI）

**适用场景**：Level 1 失败，需要重新完成 OAuth 流程。

**执行**：
```bash
# Linux/macOS
nlm login

# Windows（需 UTF-8 编码）
PYTHONIOENCODING=utf-8 nlm login
```

**流程**：
1. CLI 输出一个 URL
2. 在浏览器中打开该 URL
3. 使用 Google 账号登录并授权
4. 浏览器显示成功页面，CLI 自动获取 token

**常见问题**：
- **浏览器未打开**：手动复制 URL 到浏览器
- **Windows 编码错误**：确保设置 `PYTHONIOENCODING=utf-8`
- **防火墙拦截**：检查本地端口（CLI 会启动临时 HTTP 服务器接收回调）

**失败后**：进入 Level 3。

---

### Level 3: save_auth_tokens()（手动 Cookie）

**适用场景**：CLI 登录不可用（如无 GUI 浏览器的远程环境、CI/CD）。

**获取 Cookie 详细步骤**：

1. 在有浏览器的设备上打开 `https://notebooklm.google.com`
2. 使用目标 Google 账号登录
3. 打开浏览器开发者工具（F12 或 Ctrl+Shift+I）
4. 切换到 **Application**（Chrome）或 **Storage**（Firefox）标签
5. 在左侧导航中找到 **Cookies** → `https://notebooklm.google.com`
6. 复制所有 cookie 的 Name=Value 对，格式为：
   ```
   cookie1_name=cookie1_value; cookie2_name=cookie2_value; ...
   ```
7. 使用以下命令保存：

```
save_auth_tokens(cookies="{复制的 cookie 字符串}")
```

**注意**：
- Cookie 有效期有限（通常几小时到几天）
- 修改密码或登出会使 Cookie 立即失效
- 建议尽快转到 Level 2 的正常登录流程

---

## 账号切换

### 查看可用 profile

```bash
nlm login list
```

### 切换到指定 profile

```bash
nlm login switch {profile_name}
```

MCP 服务会立即使用新 profile 的凭据，无需重启。

### 添加新 profile

```bash
nlm login --profile {new_profile_name}
```

完成 OAuth 登录后，新 profile 自动保存。

---

## 环境特定问题

### Windows

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `UnicodeEncodeError` | 终端编码非 UTF-8 | `PYTHONIOENCODING=utf-8 nlm login` |
| `python` 命令无效 | Windows Store stub | 使用 `uv run python` 或 `py` |

### WSL

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 浏览器无法打开 | WSL 无 GUI | 手动复制 URL 到 Windows 浏览器 |

### 远程服务器

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 无浏览器 | 无 GUI 环境 | 使用 Level 3（手动 Cookie）或端口转发 |

---

## 验证认证状态

认证完成后，使用以下命令验证：

```
server_info()
```

**正常返回**：包含服务版本和连接状态信息。

**仍然失败**：检查以下可能原因：
1. MCP 服务配置错误 → 检查 Claude Code MCP 设置
2. 网络问题 → 确认可访问 `notebooklm.google.com`
3. Google 账号限制 → 确认账号可正常使用 NotebookLM
