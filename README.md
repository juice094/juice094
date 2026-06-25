<div align="center">

# 酒宿 · Zhou Jingxiao

> *"I write my own protocols. Rust + AI + Distributed Systems."*

[![GitHub followers](https://img.shields.io/github/followers/juice094?style=social)](https://github.com/juice094)
[![GitHub stars](https://img.shields.io/github/stars/juice094?affiliations=OWNER&style=social)](https://github.com/juice094?tab=repositories)

<img src="https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white">
<img src="https://img.shields.io/badge/AI_Systems-4B32C3?style=flat-square&logo=openai&logoColor=white">
<img src="https://img.shields.io/badge/Distributed-FF6B35?style=flat-square&logo=databricks&logoColor=white">
<img src="https://img.shields.io/badge/P2P-00ADD8?style=flat-square&logo=syncthing&logoColor=white">
<img src="https://img.shields.io/badge/AGPL--3.0-3DA639?style=flat-square&logo=gnu&logoColor=white">

</div>

---

## Abstract

Systems builder. 大三，甘肃农业大学大数据。独立设计并实现三个生产级 Rust 系统（合计 **62 crates / 26 万行 / 1,200+ 测试**），覆盖 P2P 同步协议、AI agent 运行时、开发者工具链。一项 RAG 学术研究（manuscript in progress）。AI 应用工程师（中级）。寻求 2027 后端/系统/AI 基础设施实习。

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Clarity (25 crates)                   │
│              本地优先 AI Agent 运行时                      │
│    tokio · MCP · SQLite+向量 · 5种UI · ChaCha20加密       │
│    多模型调度 · 子代理编排 · Wire 通信协议                  │
└────────────┬──────────────────────┬──────────────────────┘
             │                      │
    ┌────────▼────────┐    ┌───────▼────────┐
    │   devbase       │    │ syncthing-rust │
    │  (12 crates)    │    │  (8 crates)    │
    │ 世界模型编译器    │    │ P2P 同步协议    │
    │ Vault · Skill   │    │ BEP · TLS · NAT │
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

## ⚡ Featured Projects

<table>
<tr>
<td width="33%">
<h4 align="center">
  <img src="https://img.shields.io/badge/25_crates-152K_LOC-blue?style=flat-square">
  <br>🧠 Clarity
</h4>
<p align="center"><strong>Local-first AI agent runtime</strong></p>
<p align="center">
  <img src="https://img.shields.io/badge/Rust-red?style=flat-square&logo=rust&logoColor=white">
  <img src="https://img.shields.io/badge/tests-1243-brightgreen?style=flat-square">
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
  <img src="https://img.shields.io/badge/8_crates-59K_LOC-blue?style=flat-square">
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
Block-level delta sync · REST API
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
| [turbovec](https://github.com/juice094/turbovec) | Vector index on TurboQuant, Rust + Python bindings |
| [skills-DBA](https://github.com/juice094/skills-DBA) | Skill database admin: local index, search, multi-source sync |

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
<img src="https://img.shields.io/badge/62-crates-blue?style=flat-square">
<img src="https://img.shields.io/badge/1200+-tests-green?style=flat-square">
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

📚 Junior year, Big Data, Gansu Agricultural University
&nbsp;&nbsp;·&nbsp;&nbsp;
📜 AI Application Engineer (Intermediate)
&nbsp;&nbsp;·&nbsp;&nbsp;
📄 Research: generation-budget window in RAG
&nbsp;&nbsp;·&nbsp;&nbsp;
🔍 Seeking 2027 backend / systems / AI infra internships

</div>

---

<div align="center">

### 📋 Resume · [中文](resume/zh.md) · [English](resume/en.md)

### 📬 Connect · [GitHub](https://github.com/juice094)

<sub>Holland CIE · Enneagram 7w8 · PDP Owl 🦉 · MBTI ENTJ · DISC DC</sub>

</div>
