# juice094

<p align="center">
  <img src="./metrics.svg" alt="GitHub Metrics" width="100%">
</p>

<p align="center">
  <a href="./projects/">项目架构</a> ·
  <a href="./notes/">技术笔记</a> ·
  <a href="./research/">研究草稿</a> ·
  <a href="./resume/">个人履历</a>
</p>

---

这里用于沉淀日常开发与学习过程中的系统架构文档、技术笔记与研究草稿。具体业务代码均在独立仓库中维护。

## 📂 核心内容导航

| 资产分类 | 内容说明 | 目录链接 |
| :--- | :--- | :--- |
| **项目架构** | 核心项目的系统架构、决策记录与性能指标。 | [projects/](./projects/) |
| **个人履历** | 多版本 Markdown 源文件、PDF 输出及 LaTeX / Typst 模板。 | [resume/](./resume/) |
| **技术笔记** | 学习路线图、面试攻略、通用八股与面经分享。 | [notes/](./notes/) |
| **学术草稿** | RAG 输出结构实证研究草稿。 | [research/](./research/) |
| **自动化脚本** | Windows 定时备份与简历自动构建脚本。 | [scripts/](./scripts/) |

## 🧩 核心项目索引

| 项目名称 | 核心特性 | 架构文档 |
| :--- | :--- | :--- |
| **Clarity** | 高并发、低延迟的分布式基础设施组件。 | [projects/clarity.md](./projects/clarity.md) |
| **devbase** | 面向开发者的本地环境/容器化基础底座。 | [projects/devbase.md](./projects/devbase.md) |
| **syncthing-rust** | 高效节点同步工具（BEP 协议）。 | [projects/syncthing-rust.md](./projects/syncthing-rust.md) |

<details>
<summary>本地构建指南（点击展开）</summary>

由于本仓库为纯文档仓库，无需配置复杂的应用运行环境。

**构建简历 PDF**：依赖 [Pandoc](https://pandoc.org/) 与 TeX Live（需包含 `xelatex` 及中文字体支持如 `ctex`）。

    .\resume\build-resume.ps1

**阅读技术笔记**：笔记使用纯 Markdown 编写，可直接用 VS Code 预览；也可将 `notes/` 目录作为 [Obsidian](https://obsidian.md/) Vault 打开（需自行生成 `.obsidian/` 配置）。

</details>

## 📁 目录结构

    juice094/
    ├── projects/             # 核心项目架构文档
    ├── notes/                # 技术学习笔记库
    ├── research/             # 学术论文草稿
    ├── resume/               # 个人履历与联系方式
    ├── scripts/              # Windows 自动化脚本
    ├── .agents/              # AI Agent 技能定义
    ├── .github/workflows/    # GitHub Actions（自动化构建）
    └── AGENTS.md             # AI Agent 工作区指南

## 🤝 贡献与反馈

如果你在阅读文档时发现链接失效、文案错误，或对项目架构有疑问，欢迎提交 Issue 或 Pull Request。在提交前，请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 📄 License

本项目采用 [MIT License](./LICENSE) 开源协议。