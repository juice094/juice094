<div align="center">

# 酒宿 · Zhou Jingxiao

> Rust, AI Agents, Distributed Systems — built from scratch.

[![GitHub followers](https://img.shields.io/github/followers/juice094?style=social)](https://github.com/juice094)
[![GitHub stars](https://img.shields.io/github/stars/juice094?affiliations=OWNER&style=social)](https://github.com/juice094?tab=repositories)

<img src="https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white">
<img src="https://img.shields.io/badge/AI_Systems-4B32C3?style=flat-square&logo=openai&logoColor=white">
<img src="https://img.shields.io/badge/Distributed-FF6B35?style=flat-square&logo=databricks&logoColor=white">
<img src="https://img.shields.io/badge/P2P-00ADD8?style=flat-square&logo=syncthing&logoColor=white">
<img src="https://img.shields.io/badge/Open_Source-3DA639?style=flat-square&logo=opensourceinitiative&logoColor=white">

</div>

---

## About

大三在读（2004年生，2027届），甘肃农业大学数据科学与大数据技术专业。2025.11-2026.06 独立设计和交付了三个生产级 Rust 系统 —— 从 AI Agent 运行时到 P2P 协议栈到开发者编译器。实战覆盖 LLM 编排、MCP 协议、RAG 检索、NAT 穿透、Contract-First 架构设计。同时独立完成一项 RAG 输出结构的实证研究（跨 7 模型 × 4 架构 × 3,000+ 样本）。AI 应用工程师（中级）认证。

项目均部署于公网 —— Clarity 前端和课程项目跑在 Vercel，syncthing-rust 的 P2P 节点部署在日本 VPS 上，通过 Tailscale 和国内桌面端组网。

**目前在找**：2027 届 AI Agent 开发 / 后端系统 / 基础设施方向的实习机会。

---

这三个项目共享一套工程哲学 —— Contract-First 架构、零 unwrap/expect/panic 的编译期安全策略、单二进制零运行时依赖的分发模型。它们各自的定位是这样的：

```
                        ┌──────────────────────────────┐
                        │    Clarity (22 crates)        │
                        │   本地 AI Agent 运行时         │
                        │   tokio · MCP · 6前端 · 记忆  │
                        └──────┬───────────┬───────────┘
                               │           │
              ┌────────────────▼──┐    ┌───▼─────────────────┐
              │  devbase          │    │  syncthing-rust      │
              │  (12 crates)      │    │  (13 crates)         │
              │  世界模型编译器     │    │  P2P 文件同步引擎     │
              │  71个MCP工具      │    │  BEP协议 + TLS 1.3   │
              │  tree-sitter解析  │    │  4种NAT发现机制      │
              └───────────────────┘    └──────────────────────┘
```

- **Clarity** 是 Agent 运行时 —— 负责推理、工具调用、记忆管理
- **devbase** 是上下文引擎 —— 告诉 Agent 你的工作空间里有什么
- **syncthing-rust** 是传输层 —— 让文件在设备之间安全流动

三者可以串联工作：devbase 提供上下文 → Clarity 执行 Agent 任务 → syncthing-rust 同步产出到其他设备。这种"协议栈"式的项目组合，体现的是对系统分层设计的理解 —— 每层有清晰的职责边界和稳定的接口契约。

---

## Projects

Clarity、devbase、syncthing-rust 是三个主力项目。此外还有课程项目集（student-era）、Rust 工具库（pretext-rust）、以及一项仍在进行的 RAG 实证研究（acr-select）。

### 主力项目

<table>
<tr>
<td width="33%">
<h4 align="center">🧠 Clarity</h4>
<p align="center">
  <img src="https://img.shields.io/badge/Rust-red?style=flat-square&logo=rust">
  <img src="https://img.shields.io/badge/22_crates-blue?style=flat-square">
  <img src="https://img.shields.io/badge/1889_tests-green?style=flat-square">
  <img src="https://img.shields.io/badge/MCP-purple?style=flat-square">
</p>
<p align="center">
本地优先的 AI Agent 运行时。ReAct/Plan 双模式循环，MCP 协议四传输全实现，BM25+向量混合记忆，Candle GGUF 本地推理。六种前端共享同一 Agent 内核。
</p>
<p align="center">
<a href="https://github.com/juice094/clarity">🔗 Repo</a> · <a href="projects/clarity.md">📄 Details</a>
</p>
</td>
<td width="33%">
<h4 align="center">🔄 syncthing-rust</h4>
<p align="center">
  <img src="https://img.shields.io/badge/Rust-red?style=flat-square&logo=rust">
  <img src="https://img.shields.io/badge/13_crates-blue?style=flat-square">
  <img src="https://img.shields.io/badge/wire_compat-Go_Syncthing-green?style=flat-square">
  <img src="https://img.shields.io/badge/TLS_1.3-orange?style=flat-square">
</p>
<p align="center">
Go Syncthing BEP 协议的 Rust 重新实现。TLS 1.3 双向认证，四种 NAT 穿透机制，块级增量同步，三路文本合并。单二进制 ~13MB，部署在日本 VPS 上。
</p>
<p align="center">
<a href="https://github.com/juice094/syncthing-rust">🔗 Repo</a> · <a href="projects/syncthing-rust.md">📄 Details</a>
</p>
</td>
<td width="33%">
<h4 align="center">🗺️ devbase</h4>
<p align="center">
  <img src="https://img.shields.io/badge/Rust-red?style=flat-square&logo=rust">
  <img src="https://img.shields.io/badge/12_crates-blue?style=flat-square">
  <img src="https://img.shields.io/badge/71_MCP_tools-purple?style=flat-square">
  <img src="https://img.shields.io/badge/SQLite_WAL-blue?style=flat-square">
</p>
<p align="center">
开发者工作空间编译器。tree-sitter 代码解析 + Tantivy BM25 全文搜索 + 自定义 SQL cosine_similarity UDF 实现零外部依赖的语义检索。以 MCP 协议暴露 71 个工具给 AI Agent。
</p>
<p align="center">
<a href="https://github.com/juice094/devbase">🔗 Repo</a> · <a href="projects/devbase.md">📄 Details</a>
</p>
</td>
</tr>
</table>

### 其他项目与课程作品

| Project | Description |
|:---|:---|
| [student-era](https://github.com/juice094/student-era) | 课程项目集入口 —— Vue 3 / PyTorch / Hadoop / GIS 等多课程归档 |
| [acr-select](https://github.com/juice094/acr-select) | RAG 输出结构实证研究 —— 7模型 × 4架构 × 3,000+样本的受控实验 |
| [pretext-rust](https://github.com/juice094/pretext-rust) | Rust 移植的 Pretext 多语言文字测量与断行库 |
| [personal-portal](https://github.com/juice094/personal-portal) | Vue 3 + Glassmorphism 风格的个人主页入口 |
| [steamtools-accelerator](https://github.com/juice094/steamtools-accelerator) | Rust 实现的 HTTP/HTTPS 反向代理与流量劫持工具 |

---

## Repository Layout

```
juice094/
├── README.md
├── resume/                            ← 简历（4版 md + 2版 PDF）
│   ├── resume-general.md              # 海投通用版
│   ├── zh.md                          # 技术深挖版（STAR 格式）
│   ├── resume-keda-ai-agent.md        # 科大讯飞定向
│   ├── resume-damo-academy.md         # 阿里达摩院定向
│   ├── 周景潇-简历.pdf                # LaTeX 编译
│   ├── 周景潇-简历-达摩院-typst.pdf    # Typst 编译
│   └── templates/                     # LaTeX + Typst 模板
├── 求职战备/                           ← 面试备考资料库（13份文档）
│   ├── 学习路线图/                     # 三项目分级学习路径
│   ├── 项目面试攻略/                   # 15-20 个 Q&A + 话术 + 反问
│   ├── 通用八股/                       # Rust / AI-Agent / 系统设计 / 后端综合
│   └── 面经/                           # 公司特点 + 薪资 + BQ 策略
├── projects/                          # 各项目详细文档
├── research/                          # RAG 学术研究
├── scripts/                           # 工具脚本（定时推送等）
└── .agents/skills/                    # Claude Code Agent 技能定义
```

---

## Skills

<div align="center">

<table>
<tr>
<td align="center" width="25%">

**Languages**
<br>
<img src="https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white">
<img src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white">

</td>
<td align="center" width="25%">

**Systems**
<br>
<img src="https://img.shields.io/badge/tokio-async-red?style=flat-square&logo=rust">
<img src="https://img.shields.io/badge/TLS_1.3-secure-green?style=flat-square">
<img src="https://img.shields.io/badge/SQLite-WAL-blue?style=flat-square&logo=sqlite">
<img src="https://img.shields.io/badge/P2P-NAT_traversal-orange?style=flat-square">

</td>
<td align="center" width="25%">

**AI / Agent**
<br>
<img src="https://img.shields.io/badge/MCP-protocol-purple?style=flat-square">
<img src="https://img.shields.io/badge/BM25-search-teal?style=flat-square">
<img src="https://img.shields.io/badge/RAG-evaluation-indigo?style=flat-square">
<img src="https://img.shields.io/badge/Multi--model-orch-gray?style=flat-square">

</td>
<td align="center" width="25%">

**Engineering**
<br>
<img src="https://img.shields.io/badge/44+-crates-blue?style=flat-square">
<img src="https://img.shields.io/badge/2500+-tests-green?style=flat-square">
<img src="https://img.shields.io/badge/CI/CD-automation-yellow?style=flat-square">
<img src="https://img.shields.io/badge/LaTeX-academic-red?style=flat-square">

</td>
</tr>
</table>

</div>

---

<div align="center">

## Stats

<img height="160" src="https://github-readme-stats.vercel.app/api?username=juice094&show_icons=true&theme=radical&hide_border=true&count_private=true">
<img height="160" src="https://github-readme-stats.vercel.app/api/top-langs/?username=juice094&layout=compact&theme=radical&hide_border=true">

---

📚 大三在读 · 2027届 · 甘肃农业大学大数据
&nbsp;&nbsp;·&nbsp;&nbsp;
📜 AI 应用工程师（中级）
&nbsp;&nbsp;·&nbsp;&nbsp;
📄 RAG 实证研究（论文撰写中）
&nbsp;&nbsp;·&nbsp;&nbsp;
🔍 寻求 2027 AI Agent / 后端 / 系统 实习
&nbsp;&nbsp;·&nbsp;&nbsp;
🌐 项目部署于 Vercel + 日本 VPS

---

### 📋 Resume

[通用版](resume/resume-general.md) · [深挖版](resume/zh.md) · [讯飞定向](resume/resume-keda-ai-agent.md) · [达摩院定向](resume/resume-damo-academy.md) · [通用PDF](resume/周景潇-简历.pdf) · [达摩院PDF](resume/周景潇-简历-达摩院-typst.pdf)

[📁 求职战备资料库](求职战备/) —— 学习路线图 · 面试攻略 · 八股文 · 面经

---

### 📬 [GitHub](https://github.com/juice094)

<sub>Holland CIE · Enneagram 7w8 · PDP Owl 🦉 · MBTI ENTJ · DISC DC</sub>

</div>
