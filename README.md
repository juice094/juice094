# Hi, I'm 周景潇 (Zhou Jingxiao)

I'm an undergraduate student building production-grade systems in **Rust**.

Currently independent-maintaining 3 system-level projects — an AI Agent runtime, a P2P file-sync protocol stack, and a developer workspace compiler. 40+ workspace crates, 2,500+ tests, zero `unwrap`/`expect`/`panic` in production code.

---

## About

I believe good infrastructure should be **local-first**, **zero-dependency**, and **single-binary distributable**.

Most of my work lives in Rust: async services, embedded storage, network protocols, and cross-platform UIs. I care about compile-time safety, minimal deployment surfaces, and systems that keep working when the network doesn't.

---

## Currently Building

### [Clarity](https://github.com/juice094/clarity) — Local-first AI Agent runtime

A runtime that lets the same AI assistant keep its personality, memory, and social context across your phone, laptop, and server — without uploading private data to the cloud.

- ReAct + Plan dual-mode execution loop
- MCP protocol with stdio / SSE / WebSocket transports
- SQLite-based hybrid memory retrieval with custom vector-similarity UDF
- Shared Agent kernel across TUI, egui GUI, headless, and mobile FFI

`23 crates · 152K LOC · 1,243 tests`

### [syncthing-rust](https://github.com/juice094/syncthing-rust) — P2P file sync, no cloud needed

A Rust reimplementation of the Syncthing BEP protocol, wire-compatible with the official Go client.

- TLS 1.3 + rustls transport
- Multi-path NAT traversal: UDP broadcast, STUN, UPnP, Relay
- Block-level delta sync and version archiving
- Deployed on a VPS, syncing with a Windows desktop over Tailscale

`8 lib crates + 5 binaries · 59K LOC`

### [devbase](https://github.com/juice094/devbase) — Developer workspace compiler

Turns code repos, Markdown notes, and YAML workflows into structured context that AI agents can reason over.

- tree-sitter parsing for multi-language symbol extraction
- Tantivy + SQLite embedding store, no external vector database
- YAML DAG workflow engine with skills, sub-workflows, parallelism, and conditionals
- Exposes 71 stdio tools via MCP protocol

`12 crates + main crate · 56K LOC`

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

## By the numbers

- **40+** workspace crates across personal projects
- **2,500+** tests passing, **0** production `unwrap`/`expect`/`panic`
- **3** system-level Rust projects shipped independently
- **1** empirical study on RAG output structure in progress

---

## Connect

- Email: [2241470466@qq.com](mailto:2241470466@qq.com)
- GitHub: [github.com/juice094](https://github.com/juice094)
- Resume: [resume/](resume/)
