## 事故描述
<!-- 一句话描述生产环境中用户看到的问题 -->

## 关联 Issue
Closes #

## 影响范围
<!-- 受影响的用户、功能或插件 -->

## 根因分析
<!-- 问题的根本原因 -->

## 修复方案
<!-- 本次变更做了什么 -->

## 回滚预案
<!-- 必填：如修复引入新问题，如何回滚 -->
如修复引入新问题，执行以下步骤：
1. `git revert <merge-commit-sha>` 回滚合并
2. `git push origin main`
3. `release.yml` 会自动处理 tag/Release（如已触发）

## 自检结果
- [ ] 仅包含 `fix` 类型的 commit
- [ ] 合并后计划同步到 develop
- [ ] 回滚预案已明确
- [ ] Commit message 符合 `<type>(<scope>): <summary>` 规范

> **允许的 commit types**: `fix`
