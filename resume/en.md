# Zhou Jingxiao

**13626566112** · **2241470466@qq.com** · **github.com/juice094**
**AI / Backend / Systems Engineering** · Shanghai/Hangzhou/Shenzhen · Available 2026.07

---

## Summary

Junior-year CS student. Independently designed and maintains three production-grade Rust systems (47 workspace crates, 270K+ lines, 2,500+ tests passing). Built from protocol stacks to agent kernels to compiler pipelines. Seeks internship in AI infrastructure / backend systems.

---

## Education

**Gansu Agricultural University** · Data Science & Big Data Technology · B.Eng. (Expected 2027.06)
GPA 83/100 · Core courses 86/100 · Top 10%

---

## Skills

**Languages**: Rust (primary, 3yr, 3 large workspace projects), Python (research, data analysis)

**Systems**: tokio async, TLS 1.3/rustls, NAT traversal (STUN/UPnP/Relay), SQLite WAL, Protobuf (prost)

**AI/Agent**: MCP protocol (stdio/SSE/HTTP/WebSocket), ReAct + Plan agent loops, BM25 + vector hybrid search, multi-agent parallel scheduling, local LLM inference (Candle GGUF)

**Engineering**: Cargo workspace layered architecture, contract-first design, CI/CD invariant enforcement, zero production panic baseline

---

## Research

### Empirical Study of Output Structure in RAG (2026.06 — present)

Independent research under faculty guidance. Built a controlled experiment framework to study format-content interaction in retrieval-augmented generation.

- Designed and executed multi-model × multi-domain × multi-depth controlled experiments (~40 conditions, 3,000+ samples)
- Proposed a behavioral observation framework decomposing model output into format and content dimensions with independent scoring axes
- Cross-validated the framework across four model architectures
- Identified measurement artifacts in the analysis pipeline and designed a unified scoring protocol
- Manuscript in progress

---

## Projects

### Clarity — Local-First AI Agent Runtime
**Rust** · 22 active workspace crates · 1,889 tests passing · 2026.04 - present

Single-binary local AI runtime: LLM orchestration, MCP tools, memory systems, multi-agent collaboration. Zero Python/Node.js/Ollama dependencies.

- **Contract-First layered architecture**: zero-dependency contract crate, strict unidirectional core/frontend references. New features touch 1 layer on average, zero circular dependencies at compile time
- **ReAct + Plan dual-mode agent loop**: Plan Mode reduced multi-step task omission rate from ~40% to near zero, with 4-tier Approval chain
- **Hybrid memory system**: SQLite + BM25 + vector search + 4-tier compression. Context overflow protection with long-term memory persistence
- **Cross-frontend SPMC event bus**: single Agent kernel shared across 6 entry points (egui desktop, ratatui terminal, Axum Web IDE, headless CLI, system tray, mobile FFI)
- **Pretext text measurement**: 1.45% height deviation on 1,000 messages; 74µs/136µs estimate/render per message
- **Engineering baseline**: 1,554 lib + 275 bin + 34 doc + 26 integration tests passing, Clippy zero warnings, zero production unwrap/expect

### syncthing-rust — P2P File Sync Engine
**Rust** · 13 workspace crates · 58,848 LOC · 392 tests passing · 2026.04 - present

Wire-compatible Rust reimplementation of Go Syncthing BEP protocol. Single static binary ~13MB.

- **BEP protocol stack**: prost + rustls + ed25519-dalek; complete BEP over TLS message format, LZ4 compression frames, and handshake semantics; wire_compat integration tests verify cross-language interop
- **Multi-path NAT traversal**: UDP broadcast + HTTPS mTLS Global Discovery + STUN + UPnP + Relay v1
- **Windows file sharing conflict resolution**: exponential backoff rename retry + three-way text merge + versioning strategies
- **Predictive health checks**: event-driven failure rate and state flip trend analysis; FolderOrchestrator dynamically adjusts scan/pull concurrency. ~1s change detection latency

### devbase — Developer Workspace World Model Compiler
**Rust** · 12 workspace crates · 71 MCP tools · 616+ tests · 2026.04 - present

Compiles local Git repos, PARA notes, Skill scripts, and YAML workflows into AI-inferrable structured context.

- **Three-layer compiler architecture**: perception (tree-sitter multi-language parsing + Git analysis) → encoding (SQLite Registry entity-relation model) → compilation (knowledge engine); 71 MCP stdio tools
- **Zero-cloud semantic search**: SQLite BLOB + custom cosine_similarity UDF replacing external vector DB; Candle/Ollama local embedding backends; zero ML runtime dependency by default
- **Architecture governance**: G1-G7/RF-1-RF-7 invariant enforcement via CI; zero production unwrap/expect/panic
- **Engineering constraints**: CLI entry point capped at 836 lines; crate split requires >5 internal crate:: references

---

## Languages & Certifications

- Japanese Proficiency Test Band 4 (72/100)
- AI Application Engineer (Intermediate) — MIIT Certified
