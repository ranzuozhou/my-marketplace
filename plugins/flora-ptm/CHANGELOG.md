# Changelog

All notable changes to the flora-ptm plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-03-19

### Added
- 初始发布：3 个 Skill（digest, synthesize, produce）
- NotebookLM MCP 集成（共享 mj-nlm 的 notebooklm-mcp 服务器）
- SessionStart hook 检测进行中的工作流
- 共享参考文件（prompt-templates, analysis-prompts, naming-reference）
- 4 种预设学习路径（快速消化、深度学习、视觉优先、全覆盖）
- 按报告类型的分析 prompt 变体（学术论文、行业报告、博客/观点文章）
- 智能分库决策逻辑（基于主题聚类自动确定 notebook 数量）
- Tag 系统实现技能间状态传递
