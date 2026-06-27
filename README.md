<div align="center">

# 酒宿 · Zhou Jingxiao

> *"I write my own protocols. Rust + AI + Distributed Systems."*

[![GitHub followers](https://img.shields.io/github/followers/juice094?style=social)](https://github.com/juice094)
[![GitHub stars](https://img.shields.io/github/stars/juice094?affiliations=OWNER&style=social)](https://github.com/juice094?tab=repositories)

<img src="https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white">
<img src="https://img.shields.io/badge/AI_Systems-4B32C3?style=flat-square&logo=openai&logoColor=white">
<img src="https://img.shields.io/badge/Distributed-FF6B35?style=flat-square&logo=databricks&logoColor=white">
<img src="https://img.shields.io/badge/P2P-00ADD8?style=flat-square&logo=syncthing&logoColor=white">
<img src="https://img.shields.io/badge/Open_Source-3DA639?style=flat-square&logo=opensourceinitiative&logoColor=white">

</div>

---

## Abstract

Systems builder. 2004年生，大三在读（2027届），甘肃农业大学大数据。2025.11-2026.06 独立设计并交付三个生产级 Rust 系统（合计 44+ crates / 2,500+ 测试），覆盖 P2P 同步协议、AI agent 运行时、开发者工具链。一项 RAG 学术研究（manuscript in progress）。多项目部署于 Vercel + 日本 VPS。AI 应用工程师（中级）。寻求 2027 AI Agent / 后端 / 系统 实习。

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Clarity (22 crates)                   │
│              本地优先 AI Agent 运行时                      │
│    tokio · MCP四传输 · SQLite+向量 · 6前端 · ChaCha20     │
│    多模型调度 · 子代理编排 · Wire 通信协议                  │
└────────────┬──────────────────────┬──────────────────────┘
             │                      │
    ┌────────▼────────┐    ┌───────▼────────┐
    │   devbase       │    │ syncthing-rust │
    │  (12 crates)    │    │  (13 crates)   │
    │ 世界模型编译器    │    │ P2P 同步协议    │
    │ 71 MCP工具      │    │ BEP · TLS · NAT │
    │ Workflow · Sync │    │ Block-level Δ  │
    └────────┬────────┘    └───────┬────────┘
             │                      │
             └──────────┬───────────┘
                        │
              ┌─────────▼─────────┐
              │    acr-select     │
              │   学术研究 (Python) │
              │  RAG评估 · 论文   │
              └───────────────────┘
```

---

## 🎓 Student Portfolio

> Course projects archive — organized under [`student-era`](https://github.com/juice094/student-era).

| Project | Stack | Course |
|:---|:---|:---|
| [student-era](https://github.com/juice094/student-era) | Vue 3 / Python / JS / ECharts | 多课程归档入口 — 论文 · 简历 · 实验报告 |
| [ml-course-experiments](https://github.com/juice094/ml-course-experiments) | PyTorch / ResNet18 / scikit-learn | 机器学习 — 苹果检测 · 天气预测 |
| [course-design-web-frontend](https://github.com/juice094/course-design-web-frontend) | Vue 3 / pnpm | 2026春 Web 前端课程设计 |
| [course-design-canvas-game](https://github.com/juice094/course-design-canvas-game) | HTML5 Canvas / JavaScript | 2026春 Canvas 游戏开发 |
| [vue-web-worker-lab](https://github.com/juice094/vue-web-worker-lab) | Vue 3 / Web Worker | 2026春 数值计算与多线程实验 |

> *Consolidation in progress — these will migrate under `student-era` as a unified student portfolio.*

---

## ⚡ Featured Projects

<table>
<tr>
<td width="33%">
<h4 align="center">
  <img src="https://img.shields.io/badge/22_crates-150K_LOC-blue?style=flat-square">
  <br>🧠 Clarity
</h4>
<p align="center"><strong>Local-first AI agent runtime</strong></p>
<p align="center">
  <img src="https://img.shields.io/badge/Rust-red?style=flat-square&logo=rust&logoColor=white">
  <img src="https://img.shields.io/badge/tests-1889-brightgreen?style=flat-square">
  <img src="https://img.shields.io/badge/MCP-protocol-purple?style=flat-square">
</p>
<p align="center">
Multi-model scheduling · sub-agent parallelism<br>
5 UI backends · ChaCha20 secrets<br>
SQLite + BM25 + embedding memory
</p>
<p align="center">
<a href="https://github.com/juice094/clarity">🔗 Repo</a> · <a href="projects/clarity.md">📄 Details</a>
</p>
</td>
<td width="33%">
<h4 align="center">
  <img src="https://img.shields.io/badge/13_crates-58K_LOC-blue?style=flat-square">
  <br>🔄 syncthing-rust
</h4>
<p align="center"><strong>P2P file sync protocol</strong></p>
<p align="center">
  <img src="https://img.shields.io/badge/Rust-red?style=flat-square&logo=rust&logoColor=white">
  <img src="https://img.shields.io/badge/wire_compatible-Go_Syncthing-green?style=flat-square">
  <img src="https://img.shields.io/badge/TLS-1.3-orange?style=flat-square">
</p>
<p align="center">
BEP protocol · NAT traversal<br>
STUN/UPnP/Relay · LAN+Global discovery<br>
Block-level delta sync · 13MB binary · VPS deployed
</p>
<p align="center">
<a href="https://github.com/juice094/syncthing-rust">🔗 Repo</a> · <a href="projects/syncthing-rust.md">📄 Details</a>
</p>
</td>
<td width="33%">
<h4 align="center">
  <img src="https://img.shields.io/badge/12_crates-56K_LOC-blue?style=flat-square">
  <br>🗺️ devbase
</h4>
<p align="center"><strong>World Model Compiler</strong></p>
<p align="center">
  <img src="https://img.shields.io/badge/Rust-red?style=flat-square&logo=rust&logoColor=white">
  <img src="https://img.shields.io/badge/71_MCP_tools-purple?style=flat-square">
  <img src="https://img.shields.io/badge/SQLite_WAL-blue?style=flat-square">
</p>
<p align="center">
Skill runtime · Vault management<br>
Workflow engine · Sync protocol<br>
Embedding providers · Syncthing client
</p>
<p align="center">
<a href="https://github.com/juice094/devbase">🔗 Repo</a> · <a href="projects/devbase.md">📄 Details</a>
</p>
</td>
</tr>
</table>

### More

| Project | |
|:---|:---|
| [pretext-rust](https://github.com/juice094/pretext-rust) | Rust port of Pretext: multilingual text measurement & line-breaking |
| [personal-portal](https://github.com/juice094/personal-portal) | Vue 3 + Glassmorphism personal homepage portal |
| [steamtools-accelerator](https://github.com/juice094/steamtools-accelerator) | HTTP/HTTPS reverse proxy & traffic hijacking in Rust |
| [skills-DBA](https://github.com/juice094/skills-DBA) | `[Archived]` Skill database admin: local index, search, multi-source sync |

---

## 📁 Project Structure

```
juice094/
├── README.md                          ← 你在这里
├── resume/                            ← 简历目录
│   ├── resume-general.md              # 海投通用版
│   ├── zh.md                          # 技术深挖版
│   ├── resume-keda-ai-agent.md        # 科大讯飞定向
│   ├── resume-damo-academy.md         # 阿里达摩院定向
│   ├── 周景潇-简历.pdf                # LaTeX编译 (104KB)
│   ├── 周景潇-简历-达摩院-typst.pdf    # Typst编译 (170KB)
│   └── templates/                     # LaTeX + Typst 模板
├── 求职战备/                           ← AI面试备考资料库
│   ├── 学习路线图/                     # 3项目分级学习路径
│   ├── 项目面试攻略/                   # 15-20 Q&A + 话术
│   ├── 通用八股/                       # Rust/AI-Agent/系统设计/后端综合
│   ├── 面经/                           # 公司特点 + 薪资 + BQ
│   └── SESSION-REPORT.md              # 本次会话交付清单
├── projects/                          # 项目详情
├── research/                          # RAG 学术研究
├── scripts/                           # 定时推送等工具脚本
├── .github/workflows/                 # CI/CD
└── .agents/skills/                    # 面试模拟 + 简历审查 Agent
```

---

## 📄 Research

<table>
<tr>
<td>

### Format-Content Interaction in RAG
*Independent research · manuscript in progress*

> Studying how retrieval-augmented generation interacts with output structure across model scales and architectures.

<img src="https://img.shields.io/badge/RAG-evaluation-indigo?style=flat-square">
<img src="https://img.shields.io/badge/LLM_analysis-purple?style=flat-square">
<img src="https://img.shields.io/badge/manuscript_in_progress-blue?style=flat-square">

<p>
<a href="research/coupling-paper.md">📄 Details</a>
</p>

</td>
</tr>
</table>

---

## 🛠 Skills

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

## 📊 Stats

<div align="center">

<img height="160" src="https://github-readme-stats.vercel.app/api?username=juice094&show_icons=true&theme=radical&hide_border=true&count_private=true">
<img height="160" src="https://github-readme-stats.vercel.app/api/top-langs/?username=juice094&layout=compact&theme=radical&hide_border=true">

</div>

---

## Currently

<div align="center">

📚 大三在读 · 2027届 · 甘肃农业大学大数据
&nbsp;&nbsp;·&nbsp;&nbsp;
📜 AI 应用工程师（中级）
&nbsp;&nbsp;·&nbsp;&nbsp;
📄 RAG 输出结构实证研究（论文撰写中）
&nbsp;&nbsp;·&nbsp;&nbsp;
🔍 寻求 2027 AI Agent / 后端 / 系统 实习
&nbsp;&nbsp;·&nbsp;&nbsp;
🌐 Vercel + 日本 VPS 部署

</div>

---

<div align="center">

### 📋 Resume

[通用版](resume/resume-general.md) · [技术深挖版](resume/zh.md) · [科大讯飞定向](resume/resume-keda-ai-agent.md) · [阿里达摩院定向](resume/resume-damo-academy.md) · [PDF](resume/周景潇-简历.pdf) · [达摩院PDF](resume/周景潇-简历-达摩院-typst.pdf)

### 🛡️ 求职战备

[📁 求职战备资料库](求职战备/) — 13 份文档：学习路线图 · 项目面试攻略 · 通用八股文 · 面经

### 📬 Connect · [GitHub](https://github.com/juice094)

</div>
