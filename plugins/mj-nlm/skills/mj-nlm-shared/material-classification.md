# Material Classification — 材料分类与敏感过滤规则

## 三分法分类

所有文件按扩展名分为三类，每类有明确的处理路径。

### 直传（Direct Upload）

可直接通过 `source_add(source_type="file")` 上传的文件。NLM 原生支持解析。

| 扩展名 | 说明 |
|--------|------|
| `.md` | Markdown 文档 |
| `.txt` | 纯文本 |
| `.pdf` | PDF 文档 |

### 需转换（Text Conversion）

NLM 不直接支持的代码/配置文件。需要 Read 内容 → 敏感过滤 → 以 `source_add(source_type="text")` 导入。

| 扩展名 | 类型描述 | 文件头标注 |
|--------|---------|----------|
| `.py` | Python 代码 | `类型: Python 代码` |
| `.sql` | SQL 脚本 | `类型: SQL 脚本` |
| `.yaml` / `.yml` | YAML 配置 | `类型: YAML 配置` |
| `.json` | JSON 配置/数据 | `类型: JSON 配置` |
| `.toml` | TOML 配置 | `类型: TOML 配置` |
| `.sh` | Shell 脚本 | `类型: Shell 脚本` |
| `.ps1` | PowerShell 脚本 | `类型: PowerShell 脚本` |
| `.dockerfile` / `Dockerfile` | Docker 配置 | `类型: Dockerfile` |
| `.ini` / `.cfg` | INI 配置 | `类型: 配置文件` |

### 不导入（Skip）

敏感文件、二进制文件或无分析价值的文件。自动跳过。

| 模式 | 说明 |
|------|------|
| `.pyc` | Python 编译缓存 |
| `.pyo` | Python 优化缓存 |
| `.log` | 日志文件 |
| `.env` | 环境变量（含敏感凭据） |
| `.env.*` | 环境变量变体 |
| `.git/*` | Git 内部文件 |
| `__pycache__/*` | Python 缓存目录 |
| `.venv/*` / `venv/*` | 虚拟环境 |
| `node_modules/*` | Node.js 依赖 |
| `.idea/*` / `.vscode/*` | IDE 配置 |
| `*.lock` | 锁文件（uv.lock、package-lock.json） |
| `*.egg-info/*` | Python 包元数据 |
| `*.whl` / `*.tar.gz` | 分发包 |
| `*.png` / `*.jpg` / `*.gif` / `*.svg` | 图片（NLM 不解析） |
| `*.xlsx` / `*.xls` / `*.csv` | 数据文件（按需判断） |

---

## 敏感过滤

### 文件级排除

以下文件在扫描阶段直接排除，不进入材料清单：

| 文件名模式 | 原因 |
|-----------|------|
| `.env` / `.env.*` | 包含数据库密码、API 密钥 |
| `credentials*` | 凭据文件 |
| `*secret*` | 密钥文件 |
| `*.pem` / `*.key` / `*.crt` | SSL/TLS 证书和密钥 |
| `docker/03-setup-n8n-owner.sh` | 含 n8n 账号密码逻辑 |

### 行级过滤

对"需转换"类文件，在 Read 内容后、导入前，逐行执行正则替换：

**正则模式**（大小写不敏感）：

```regex
(?i)(password|passwd|secret|token|api_key|apikey|access_key|private_key)\s*[:=]\s*\S+
```

**替换为**：

```
{匹配的键名} = [REDACTED]
```

**示例**：

| 原始行 | 过滤后 |
|--------|--------|
| `POSTGRES_PASSWORD=mypassword123` | `POSTGRES_PASSWORD = [REDACTED]` |
| `api_key: "sk-abc123"` | `api_key = [REDACTED]` |
| `token = os.getenv("SECRET_TOKEN")` | 保留原样（值是 getenv 调用，非明文） |

**智能排除**：以下模式不过滤（非明文凭据）：
- 值为 `os.getenv(...)` / `os.environ[...]` 的环境变量读取
- 值为 `{{...}}` 的模板占位符
- 值为 `"PLACEHOLDER"` 或 `"TODO"` 的占位值
- 注释行（以 `#` 开头）中的说明文本

---

## 文件大小限制

### 限制规则

| 类别 | 限制 | 处理 |
|------|------|------|
| 直传文件 | 无硬性限制（NLM 自行处理） | 直接上传 |
| 需转换文件 | 500 KB | 超限触发 H6 |
| 单个 notebook | 50 个 source（NLM 上限） | 超限触发 H4b |

### H6 超大文件处理选项

当 text 类文件超过 500KB 时：

| 选项 | 说明 |
|------|------|
| 截断 | 保留前 N 行（默认 2000 行），添加 `[... 文件截断，完整版本 {行数} 行 ...]` 标记 |
| 拆分 | 按自然边界（class/function 定义）拆分为多个 source |
| 跳过 | 不导入该文件，记录到 Note 1 的"未导入文件"列表 |

---

## 文件头元数据模板

所有"需转换"文件在导入时添加以下头部信息：

```
=== 文件信息 ===
路径: {项目相对路径，POSIX 格式}
类型: {文件类型描述}
说明: {基于路径和内容推断的简要描述}
================

{过滤后的文件内容}
```

**示例**：

```
=== 文件信息 ===
路径: src/CollectionNodes/DataQualityValidator/application/validation_service.py
类型: Python 代码
说明: DQV 验证服务主逻辑，包含三阶段处理流水线
================

from typing import List, Optional
...
```
