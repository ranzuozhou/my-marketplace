## Release 标题
<!-- 格式: Release vX.Y.Z — <主题> -->

## Highlights
<!-- 从 CHANGELOG.md [Unreleased] 提取的核心变更 -->

### Versions
| Plugin | Version |
|--------|---------|
| marketplace | x.y.z |
| mj-nlm | x.y.z |
| mp-git | x.y.z |
| mp-dev | x.y.z |
| flora-ptm | x.y.z |
| mj-drawio | x.y.z |

## 审核要点
- [ ] CHANGELOG.md 完整性（`[Unreleased]` 已转为正式版本节）
- [ ] VERSION 文件与 marketplace.json 版本一致
- [ ] 各 plugin.json 版本号与 marketplace.json plugins 数组一致
- [ ] 无残留调试代码
- [ ] 无未关闭的阻塞性 Issue

## Details
详细变更请参阅 [CHANGELOG.md](../../CHANGELOG.md)

> **Version bump 前置**：发布前需执行 `scripts/bump-version.ps1`
