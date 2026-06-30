# AGENTS.md — juice094 工作区指南

> 本文件面向 AI 编程 Agent。目标读者对该项目一无所知，阅读后即可安全地修改、生成或审查仓库内容。
> 项目文档与注释主要使用**简体中文**；Agent 应以中文回复用户，保留文件路径、命令、标识符原样。

---

## 项目概述

`juice094` 是周景潇的**个人技术主页 / 求职作品集仓库**，不是单一可运行程序。

仓库核心内容：

- `README.md`：GitHub 主页入口，介绍三个主力 Rust 项目及求职意向。
- `projects/`：三个主力项目（Clarity、devbase、syncthing-rust）的架构说明文档。
- `resume/`：多版本 Markdown 简历、LaTeX / Typst 模板、生成脚本与 PDF 输出。
- `notes/`：学习笔记库，包括项目学习路线、项目面试攻略、通用技术笔记、面经分享。
- `research/`：RAG 输出结构实证研究草稿。
- `scripts/` 与 `.claude/scripts/`：Windows 定时自动 push 脚本。
- `.agents/skills/`：Claude Code Agent 技能定义（简历优化、简历审查、面试模拟）。
- `.github/workflows/build.yml`：简历 PDF 自动构建 CI。

**注意**：真正的应用程序代码位于独立的 GitHub 仓库（见 README 与 `projects/*.md`），并不在本仓库中维护。本仓库只保存面向招聘方、面试官和合作者的文档资产。

---

## 仓库结构

```text
juice094/
├── README.md                     # GitHub 个人主页入口
├── AGENTS.md                     # 本文件
├── .gitignore                    # 忽略 Obsidian、LaTeX 产物、简历预览图
├── .github/workflows/build.yml   # 简历 PDF CI
├── .agents/
│   └── skills/                   # Agent 技能定义（MIT LICENSE）
│       ├── resume-craft/SKILL.md
│       ├── resume-reviewer/SKILL.md
│       └── interview-simulator/SKILL.md
├── .claude/
│   ├── scheduled_tasks.json      # 当前为空列表
│   └── scripts/                  # auto-push.bat / schedule-push.ps1
├── projects/
│   ├── clarity.md
│   ├── devbase.md
│   └── syncthing-rust.md
├── resume/
│   ├── *.md                      # 简历源文件（zh / en / 定向版）
│   ├── *.pdf
│   ├── *.tex / templates/        # LaTeX + Typst 模板
│   └── build-resume.ps1          # 本地 Pandoc 构建脚本
├── notes/                          # 学习笔记库
│   ├── README.md                   # 笔记库总索引
│   ├── 学习路线图/
│   ├── 项目面试攻略/
│   ├── 通用八股/
│   └── 面经/
├── research/
│   └── coupling-paper.md
└── scripts/
    ├── auto-push.bat
    └── schedule-push.ps1
```

---

## 技术栈与运行时

- **内容类型**：纯 Markdown 文档 + LaTeX / Typst 模板 + PowerShell / Batch 脚本。
- **无应用代码**：本仓库不含 `Cargo.toml`、`package.json`、`pyproject.toml` 等应用级配置；`.gitignore` 仅处理文档产物。
- **主要语言**：简体中文；简历/面试资料以中文为主。
- **Obsidian**：`.obsidian/` 为本地 Obsidian 工作区配置，已加入 `.gitignore`，不应提交。
- **第三方模板**：`resume/templates/` 包含 `billryan-resume`（MIT）与 `liweitianux-resume`，仅作备用参考。当前主模板仍是根目录下的 `resume/resume-template.tex`。

---

## 构建、生成与自动化命令

### 本地构建简历 PDF

主入口脚本：

```powershell
.\resume\build-resume.ps1
```

该脚本使用 `resume/zh-keda-ai-agent.md` + `resume/resume-template.tex`，通过 Pandoc + XeLaTeX 生成 `resume/zh-keda-ai-agent.pdf`。

通用命令示例：

```bash
# GitHub Actions 中的默认构建
pandoc resume/zh.md -o resume/zh.pdf --pdf-engine=xelatex \
  -V mainfont="Noto Serif CJK SC" \
  -V geometry:margin=1in \
  -V fontsize=11pt

# 使用自定义 LaTeX 模板
pandoc resume/zh-keda-ai-agent.md -o resume/zh-keda-ai-agent.pdf \
  --template=resume/resume-template.tex \
  --pdf-engine=xelatex \
  -V CJKmainfont="SimSun"
```

依赖：

- [Pandoc](https://pandoc.org/)
- TeX Live（`xelatex`）
- `ctex` 宏包及中文字体（如 SimSun / Noto Serif CJK SC）

### CI 自动构建

`.github/workflows/build.yml`：

- 触发条件：`push` 改动 `resume/zh.md` 或 `resume/en.md`，或手动触发 `workflow_dispatch`。
- Runner：`ubuntu-latest`。
- 安装 `pandoc`、`texlive-xetex`、`texlive-latex-recommended`、`texlive-latex-extra`。
- 构建 `resume/zh.pdf` 与 `resume/en.pdf`。
- 以 `github-actions[bot]` 身份自动 commit / push 生成的 PDF。

### 定时同步脚本

- `scripts/auto-push.bat` / `.claude/scripts/auto-push.bat`：执行 `git add -A`、`git commit --allow-empty`（提交信息带时间戳）、`git push`。
- `scripts/schedule-push.ps1` / `.claude/scripts/schedule-push.ps1`：注册 Windows 计划任务 `juice094-auto-push`，默认每 2 小时执行一次。
- 用途：保持 GitHub 活跃图/备份本地文档，不含业务逻辑。

---

## 代码 / 文档风格与约定

### 语言与提交信息

- 文档、注释、提交信息主要使用**中文**。
- Git 提交信息采用约定式前缀：`docs:`、`ci:`、`chore:`、`feat:`、`fix:` 等。
- 文件路径、命令、标识符、GitHub 链接保留英文原样。

### 简历风格

- 使用 **STAR 法则**（Situation-Task-Action-Result）描述项目经历。
- 强调**量化指标**：crate 数量、测试数量、性能数据、二进制大小、准确率等。
- **真实性第一**：禁止编造数据、项目、公司或证书。
- 定向简历命名：`resume/resume-<公司>-<岗位>.md`。
- 保持 ATS 友好：单栏、标准标题、常见字体、避免复杂表格承载关键信息。

### 项目文档风格

- `projects/*.md` 使用架构图、决策表、指标表；所有数字应与 `README.md` 保持一致。
- 技术术语统一：Contract-First、ReAct/Plan、MCP、BEP、TLS 1.3、NAT 穿透等。

### 学习笔记风格

- 使用层级标题、表格、Checklist、天数计划。
- 新增文档后应在 `notes/README.md` 的索引中更新路径与说明。

---

## 测试与质量

- **无单元测试 / 集成测试**：本仓库为静态文档集合，没有测试套件。
- **简历质量检查**：由 `.agents/skills/resume-reviewer/SKILL.md` 定义，流程包括：
  - PDF 可视化检查（`pdftoppm` 转 PNG）。
  - PDF 文本完整性检查（`pdftotext`）。
  - LaTeX 模板检查（ctex、中文字体、页边距、`\tightlist`）。
  - Markdown 源文件检查（标题、表格、占位符）。
- **面试内容质量**：由 `.agents/skills/interview-simulator/SKILL.md` 定义；每次追问只包含 1 个问题，禁止复合提问。

---

## 安全与隐私

- 本仓库为 **public** GitHub 仓库。
- 简历中已包含公开联系方式（手机号、邮箱、GitHub）。编辑时应避免添加以下敏感信息：
  - 身份证号、住址、家庭详细信息
  - 银行账户、支付信息
  - 密码、API Key、Token、私钥
- `.gitignore` 已排除 `.obsidian/`、LaTeX 构建产物、简历预览 PNG。
- `research/coupling-paper.md` 中的 RAG 研究论文处于待提交状态，不要提前泄露详细实验数据或完整手稿。

---

## AI Agent 技能

`.agents/skills/` 下有三个 Claude Code 技能：

| 技能 | 文件 | 用途 |
|------|------|------|
| `resume-craft` | `.agents/skills/resume-craft/SKILL.md` | 根据目标 JD 优化简历：关键词匹配、STAR 改写、ATS 检查。 |
| `resume-reviewer` | `.agents/skills/resume-reviewer/SKILL.md` | 检查 PDF / Markdown / LaTeX 简历的排版与内容质量。 |
| `interview-simulator` | `.agents/skills/interview-simulator/SKILL.md` | 模拟面试官追问训练，覆盖行为、技术、案例面试。 |

---

## 常见任务速查

| 任务 | 命令 / 操作 |
|------|-------------|
| 生成简历 PDF | `.\resume\build-resume.ps1` 或手动 `pandoc ...` |
| 注册定时 push | 管理员 PowerShell 中执行 `.\scripts\schedule-push.ps1` |
| 手动触发简历 CI | GitHub Actions → *Build Resume PDF* → *Run workflow* |
| 更新项目架构说明 | 编辑 `projects/<project>.md`，保持与 `README.md` 数据一致 |
| 更新学习笔记 | 编辑 `notes/` 下对应文件，并更新 `notes/README.md` 索引 |
| 新增 Agent 技能 | 在 `.agents/skills/<skill>/SKILL.md` 中定义，遵循现有 YAML frontmatter |

---

## 注意事项

- 不要在本仓库中初始化 Cargo、npm、Python 等应用项目；代码仓库在独立的 GitHub 组织中。
- 修改 `README.md`、简历、项目文档前，先核对数字/指标是否与其他文件一致（如 crate 数、测试数、时间范围、联系方式）。
- 新增脚本优先使用 PowerShell / Batch；若引入新语言或新依赖，需说明理由并在文档中记录安装步骤。
- 遵循用户级 `.agents/AGENTS.md`（Ponytail 原则）：能用现有工具就不新增依赖，能删则不增，保持最小可行方案。
