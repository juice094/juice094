# Zhou Jingxiao

> Building production-grade systems in **Rust** — AI Agent runtimes, P2P protocols, and developer tooling.

<p>
  <img src="https://img.shields.io/badge/Rust-CE422B?style=flat-square&logo=rust&logoColor=white">
  <img src="https://img.shields.io/badge/AI_Agent_Systems-4B32C3?style=flat-square&logo=openai&logoColor=white">
  <img src="https://img.shields.io/badge/Distributed_Systems-FF6B35?style=flat-square&logo=databricks&logoColor=white">
</p>

I'm an undergraduate student at Gansu Agricultural University, majoring in Data Science and Big Data Technology. Over the past year I independently designed and delivered three system-level Rust projects: a local-first AI Agent runtime, a wire-compatible P2P file-sync reimplementation, and a developer workspace compiler.

I care about **local-first architecture**, **zero external dependencies**, and **single-binary distribution**. Production code aims for zero unwrap/expect/panic.

---

## Projects

### 🧠 [Clarity](https://github.com/juice094/clarity) · [Details](projects/clarity.md)

Local-first AI Agent runtime with persistent memory across devices. ReAct/Plan execution loop, MCP protocol, BM25 + vector hybrid retrieval, shared Agent kernel across desktop / terminal / headless / mobile FFI.

`23 crates · 152K LOC · 1,243 tests`

### 🔄 [syncthing-rust](https://github.com/juice094/syncthing-rust) · [Details](projects/syncthing-rust.md)

Rust reimplementation of the Syncthing BEP protocol, wire-compatible with the official Go client. TLS 1.3, multi-path NAT traversal, block-level delta sync.

`8 crates · 5 binaries · 59K LOC`

### 🗺️ [devbase](https://github.com/juice094/devbase) · [Details](projects/devbase.md)

Developer workspace compiler that turns repos, notes, and YAML workflows into structured context for AI. tree-sitter parsing, Tantivy search, SQLite embedding store, declarative workflow engine.

`12 crates · 71 MCP tools · 56K LOC`

### More

| Project | Description |
|:---|:---|
| [acr-select](https://github.com/juice094/acr-select) | Empirical study on output structure in RAG systems |
| [student-era](https://github.com/juice094/student-era) | Course projects archive — Vue, PyTorch, Hadoop, GIS |
| [pretext-rust](https://github.com/juice094/pretext-rust) | Rust port of Pretext text measurement library |

---

## Stack

Rust · Tokio · Axum · SQLite · Tantivy · MCP · BEP · TLS 1.3 · NAT traversal

---

## GitHub Stats

<img height="170" src="https://github-readme-stats.vercel.app/api/top-langs/?username=juice094&layout=compact&theme=dark&hide_border=true">

---

📄 [Resume](resume/) · 🔬 [Research](research/) · 📬 2241470466@qq.com · 🐙 [github.com/juice094](https://github.com/juice094)
