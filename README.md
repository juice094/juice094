# juice094

<p align="center">
  <img src="./metrics.svg" alt="GitHub Metrics" width="800">
</p>

<p align="center">
  <em>持续构建，持续学习。</em>
</p>

<p align="center">
  <a href="./projects/">项目架构</a> ·
  <a href="./resume/">简历档案</a> ·
  <a href="./notes/">技术笔记</a> ·
  <a href="./research/">研究草稿</a>
</p>

---

## 📖 关于本仓库

本仓库是 juice094 的个人技术资产库，维护**核心项目架构文档、各方向求职简历、通用技术笔记与研究草稿**。

> 核心业务代码托管在独立的 GitHub 仓库中，本仓库仅保留面向招聘方、面试官和合作者的文档资产。详细身份信息与求职方向见 [resume/](./resume/)。

## 📂 核心内容导航

| 资产分类 | 内容说明 | 目录链接 |
| :--- | :--- | :--- |
| **项目架构** | 核心项目的系统架构、决策记录与性能指标。 | [projects/](./projects/) |
| **求职简历** | 多版本 Markdown 源文件、PDF 输出及 LaTeX / Typst 模板。 | [resume/](./resume/) |
| **技术笔记** | 学习路线图、面试攻略、通用八股与面经分享。 | [notes/](./notes/) |
| **学术研究** | RAG 输出结构实证研究草稿（待投递）。 | [research/](./research/) |
| **自动化脚本** | Windows 定时备份与简历自动构建脚本。 | [scripts/](./scripts/) |

## 🧩 核心项目索引

| 项目名称 | 核心特性 | 架构文档 |
| :--- | :--- | :--- |
| **Clarity** | 高并发、低延迟的分布式基础设施组件。 | [projects/clarity.md](./projects/clarity.md) |
| **devbase** | 面向开发者的本地环境/容器化基础底座。 | [projects/devbase.md](./projects/devbase.md) |
| **syncthing-rust** | 高效节点同步工具（BEP 协议）。 | [projects/syncthing-rust.md](./projects/syncthing-rust.md) |

## 🚀 快速开始

由于本仓库为纯文档仓库，**无需配置复杂的应用运行环境**。若你需要本地生成或预览文档资产，请参考以下指引：

### 1. 本地构建简历 PDF

简历构建依赖 [Pandoc](https://pandoc.org/) 与 TeX Live（需包含 `xelatex` 及中文字体支持如 `ctex`）。

```powershell
# 在根目录下运行
.\resume\build-resume.ps1
```
该命令会读取 `resume/zh-keda-ai-agent.md` 和 `resume/resume-template.tex`，输出 `resume/zh-keda-ai-agent.pdf`。

### 2. 阅读技术笔记

笔记使用纯 Markdown 编写。你可以直接使用 VS Code 的 Markdown 预览，或者使用你喜欢的 Markdown 编辑器。如果你使用 [Obsidian](https://obsidian.md/)，可以直接将 `notes/` 目录作为 Vault 打开（仓库未提交 `.obsidian/` 配置文件，你需要自行生成）。

## 📁 目录结构

```text
juice094/
├── projects/             # 核心项目架构文档（Clarity、devbase、syncthing-rust）
├── resume/               # 简历源文件、模板与 PDF 输出
├── notes/                # 技术学习笔记库（八股、面经、路线图）
├── research/             # 学术论文草稿
├── scripts/              # Windows 自动化脚本
├── .agents/              # AI Agent 技能定义
├── .github/workflows/    # GitHub Actions（简历 PDF 自动构建）
└── AGENTS.md             # AI Agent 工作区指南
```

## 🤝 贡献与反馈

如果你在阅读文档时发现链接失效、文案错误，或对项目架构有疑问，欢迎提交 Issue 或 Pull Request。在提交前，请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 📄 License

本项目采用 [MIT License](./LICENSE) 开源协议。