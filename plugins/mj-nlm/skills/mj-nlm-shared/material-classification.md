# Material Classification v2 — 材料分类与敏感过滤规则

> v2 版本说明：v2 在原"三分法（直传 / 需转换 / 不导入）"基础上新增"多源类型"分类（url / youtube / drive / image / audio），覆盖方法论 §5「准备来源」推荐的 5 类来源材料。

## 三分法分类（本地文件，v1 沿用）

所有本地文件按扩展名分为三类，每类有明确的处理路径。

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

## 多源类型分类（v2 新增）

方法论 §5 建议每个 notebook 放入 **5 类来源**：原始材料 / 入门材料 / 案例材料 / 反例 / 困惑笔记。这些来源往往不只是本地文件，还包括网页、YouTube、Google Drive 等。v2 在此扩展 NLM 多源类型。

### 来源类型矩阵

| source_type | 调用形式 | 适用场景 | NLM 处理方式 | v2 推荐用途 |
|---|---|---|---|---|
| `file` | `source_add(source_type="file", file_path=...)` | 本地文件（按"三分法"分类） | 见上 | 原始材料、规范、代码 |
| `text` | `source_add(source_type="text", text=..., title=...)` | 文本内容（含转换的代码） | 直接索引 | 困惑笔记、转换后的代码、外部摘录 |
| `url` | `source_add(source_type="url", url=...)` | 网页 | **仅提取正文文本**（无样式、图片） | 案例材料、社区讨论、博客 |
| `youtube` | `source_add(source_type="url", url="https://www.youtube.com/...")` | 公开 YouTube 视频 | **仅提取字幕 / 自动转录**（无音视频本身） | 入门材料、社区案例 |
| `drive` | `source_add(source_type="drive", document_id=...)` | Google Docs / Slides | NLM 原生支持 | 协作笔记、共享 SOP |

### 各类型注意事项

#### url（网页）

- NLM 仅导入正文文本，**不导入图片、视频、嵌入内容**
- JS 渲染的页面可能导入失败（建议用浏览器"另存为 mhtml/PDF"再 file 导入）
- 长文章建议先存为 PDF 再 file 导入（更稳定的解析）
- **批量导入**：`urls="<url1>, <url2>"` 逗号分隔

#### youtube（公开视频）

- 必须是公开视频，私有视频无法导入
- NLM 仅取**字幕（caption）或自动转录文本**，不取音视频本身
- 没有字幕的视频导入后内容空白
- **不要**用 YouTube 链接代替音频文件 source；如需音频内容直接用 `source_type="audio"`（如 NLM 支持）

#### drive（Google Docs/Slides）

- 需 OAuth 已授权（NLM 与 Google 账号联动）
- 文档需已分享给 NLM 账号或同账号下
- Slides 自动提取文本（保留章节顺序）
- 大型文档建议拆分多个 source

#### image / audio / video（多媒体源）

- NLM 不直接解析图片，建议手动 OCR 或截图描述后用 text 导入
- audio source（如 NLM CLI 支持）：直接导入会触发自动转录；转录质量影响下游 NLM 检索精度
- video：建议先 YouTube 上传或转 audio 后导入

### 来源类型与方法论 §5 推荐 5 类来源对应

| 5 类来源 | 推荐 source_type | 备注 |
|---|---|---|
| 原始材料（你真正想理解的） | file (PDF/MD) / drive | 主体内容，应占 source 总数 50%+ |
| 入门材料 | youtube / url / file (PDF) | 可选；零基础时强烈推荐 |
| 案例材料 | url（社区讨论 / Reddit / HN） / file | 暴露真实使用中的坑 |
| 反例 / 批评材料 | url / file | 防止只看正面叙事 |
| 自己的困惑笔记 | text | 告诉 NLM "我目前卡在哪里"，影响领域定向报告生成质量 |

### 来源充足性预检（v2，build Phase 6）

所有 source 添加完成后，build skill 会扫描：

- source 数量（< 5 → 警告 underloaded；> 50 → 触发 H4b）
- 总字数（< 5K / 5K-30K / 30K-100K / > 100K → 见 `risk-control-templates.md §1`）
- 来源类型分布（如全是 youtube 字幕 → 警告"来源单一可能影响领域定向准确性"）

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
