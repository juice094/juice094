# 贡献指南 (Contributing Guidelines)

感谢你关注 `juice094` 仓库。这是一个以文档和静态资产为主的仓库，我们非常欢迎任何形式的修正、建议和补充。

## 1. 提交 Issue

在提交 PR 之前，建议先搜索是否已存在相关的 Issue。如果发现新的问题，请根据 Issue 模板提交：

- **Bug 报告**：文档中的链接失效、拼写错误、代码示例跑不通等问题。
- **功能请求**：希望增加某方面的笔记、项目说明或自动化脚本。

## 2. 修改与提交规范

### 2.1 分支策略
- 请基于 `main` 分支创建你的工作分支，例如：`fix/typo-in-readme` 或 `docs/add-rag-notes`。
- 请勿直接在 `main` 分支上提交 PR。

### 2.2 提交信息 (Commit Message)
按照仓库现有的约定，请使用以下前缀：
- `docs: ` 修改或新增 Markdown 文档、注释
- `ci: ` 修改 GitHub Actions 工作流
- `chore: ` 修改脚本、依赖或非业务代码的杂项
- `fix: ` 修复链接、拼写错误

示例：
```text
docs: 修正 Clarity 架构文档中的指标描述
```

### 2.3 文档风格
- 保持现有的简体中文语言风格，代码、命令、文件路径保留英文原样。
- 笔记新增后，请在 `notes/README.md` 中添加对应的索引。
- 简历中的经历描述请使用 STAR 法则，并尽量包含量化指标。

## 3. 提交 Pull Request

1. Fork 本仓库并创建你的分支。
2. 完成修改后，如果在本地修改了简历源文件（`.md`），建议在本地运行 `.\resume\build-resume.ps1` 检查 PDF 是否正常生成。
3. 确保没有引入无用的依赖或无关的代码改动。
4. 提交 PR 时，请按照 [PR 模板](.github/pull_request_template.md) 中的检查清单进行自检。
5. 等待维护者 Review。