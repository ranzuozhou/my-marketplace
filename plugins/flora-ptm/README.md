# flora-ptm — Paper-to-Media Plugin for Claude Code

研究报告批量分析与多媒体转化插件，利用 NotebookLM 将多份研究报告整理为易于吸收的音频、视频、幻灯片等多媒体材料。

## 功能

| 命令 | 说明 |
|------|------|
| `/flora-ptm:digest` | 导入报告 → 逐篇精华提取 → Deep Research 富化 |
| `/flora-ptm:synthesize` | 跨报告关系分析 → 综述生成 → 智能分库 |
| `/flora-ptm:produce` | 学习路径推荐 → Focus Prompt 设计 → 媒体制作 |

## 前置条件

- **Claude Code** v2.1+
- **NotebookLM MCP CLI**：
  ```bash
  uv tool install notebooklm-mcp-cli --with socksio --force
  ```
- **Google 认证**：
  ```bash
  nlm login
  ```

## 安装方式

### 通过 Marketplace 安装（推荐）

```
/plugin marketplace add ranzuozhou/my-marketplace
/plugin install flora-ptm@my-marketplace
```

### 本地开发安装

```bash
claude --plugin-dir "D:\workspace\10-software-project\projects\my-marketplace\plugins\flora-ptm"
```

## 验证安装

```
/plugin                    # 确认 flora-ptm 出现在列表
/flora-ptm:digest          # 测试 skill 加载
/mcp                       # 确认 notebooklm-mcp 可用
```

## 自然语言触发

除了斜杠命令，也支持自然语言触发：

- "帮我分析这些论文" → `/flora-ptm:digest`
- "这些报告之间有什么关系" → `/flora-ptm:synthesize`
- "生成学习材料" → `/flora-ptm:produce`
- "把分析结果变成播客" → `/flora-ptm:produce`

## Settings 配置

在项目根目录创建 `.claude/flora-ptm.local.md` 文件以自定义默认偏好：

```yaml
---
default_learning_path: quick-digest  # quick-digest | deep-learning | visual-first | comprehensive
output_directory: flora-output       # 输出目录（相对于当前工作目录）
language: zh                         # 媒体语言 (BCP-47)
max_notebooks: 3                     # 分库上限
audio_format: deep_dive              # 默认音频格式
---
```

所有设置均为可选，未配置时使用默认值。

## 完整工作流示例

### 1. 导入并分析论文

```
用户：帮我分析 D:/papers/ 目录下的论文，主题是"LLM安全"
→ /flora-ptm:digest
→ 扫描目录发现 8 个 PDF
→ 创建 FLORA-LLM安全-Staging-20260319
→ 逐篇分析 → Deep Research 补充
```

### 2. 生成综述并分库

```
用户：帮我生成综述
→ /flora-ptm:synthesize
→ 发现 staging notebook → 关系分析
→ 聚类为 2 组：对齐技术 + 攻击防御
→ 创建 2 个 target notebook
```

### 3. 制作学习材料

```
用户：做成播客和幻灯片
→ /flora-ptm:produce
→ 发现 2 个 target notebook
→ 用户选择"视觉优先"路径
→ 生成 slide_deck + infographic + video
→ 下载到 flora-output/LLM安全-20260319/
```

## 许可

MIT License
