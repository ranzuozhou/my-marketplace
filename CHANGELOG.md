# Changelog

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- `.github/ISSUE_TEMPLATE/` 目录补齐:5 个 issue 模板(feature / bugfix / documentation / maintain / hotfix)+ `config.yml`(禁用空白 issue、Discussions 入口)。此前 `mp-git-issue` skill 声明读取这些模板但目录不存在

### Fixed
- `.github/PULL_REQUEST_TEMPLATE/*.md` 编码修复:6 个 PR 模板(feature / bugfix / documentation / maintain / hotfix / release)原为 GBK 双编码产生的 mojibake,已重写为正确 UTF-8 中文内容

## [1.4.0] - 2026-04-20

### Added
- 新增插件: mj-drawio v0.1.0 — draw.io 图表生成与 mj-system 模板(Windows 专用),3 个 skill(create / export / template)+ 4 个预置模板 + XML 预校验脚本

## [1.3.0] - 2026-03-24

### Added
- mp-git: 新增 `mp-git-release` 技能 — 7 步交互式版本发布工作流
- mp-git: 新增 SPEC 设计文档 `docs/design/mp-git/[SPEC]_MP_Git_Release_Skill.md`

### Fixed
- `bump-version.ps1` plugin scope 补充 README.md 到目标文件列表

### Changed
- README.md 插件版本表更新

## [1.2.0] - 2026-03-20

### Added
- 新增 flora-ptm 插件：研究报告批量分析与多媒体转化（3 skills: digest, synthesize, produce）
- 项目级 Claude Code settings（permissions + enabledPlugins）

## [1.1.1] - 2026-03-18

### Changed
- README.md 优化：添加徽章、三级安装说明、使用示例、贡献指引

## [1.1.0] - 2026-03-18

### Added
- 新增 mp-git 插件：Marketplace Git 工作流（9 skills）
- 新增 mp-dev 插件：插件开发生命周期工具链（6 skills）
- 项目文档体系：CLAUDE.md、docs/ 目录（6 篇指南/手册）
- README.md 添加文档链接

## [1.0.0] - 2026-03-18

### Added
- 初始发布：1 个 Plugin（mj-nlm），5 个 Skill（auth, build, manage, query, studio）
- Plugin Marketplace 元数据结构（marketplace.json）
- 仓库基础设施：VERSION、CI/CD、PR 模板、开发者脚本
