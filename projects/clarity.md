# Clarity — AI Agent Runtime

> **Local-first AI agent runtime. Rust workspace, 25 crates, 152K LOC, 1,243 tests.**
>
> https://github.com/juice094/clarity

---

## What It Does

Clarity is a single-binary AI runtime that orchestrates LLMs, MCP tools, and memory systems. You run it locally. It manages sub-agents, schedules models, and persists everything.

Think of it as: your own personal AI infrastructure, not someone else's API.

---

## Architecture

```
apps (5 entry points)
  ├── tui        Terminal UI (ratatui)
  ├── egui       Desktop GUI (egui)
  ├── slint      Experimental GUI (Slint)
  ├── tauri      Web UI (Tauri + Vue)
  └── headless   CLI / daemon mode

core engine
  ├── clarity-core        Agent loop: ReAct + Plan modes
  ├── clarity-subagents    Parallel sub-agent orchestration
  ├── clarity-contract     Interface contracts
  └── clarity-tools        Built-in tools (file, search, shell)

LLM layer
  ├── clarity-llm          Multi-provider abstraction
  ├── clarity-anthropic-proxy  Anthropic → DeepSeek reverse proxy
  └── clarity-openclaw     OpenClaw gateway integration

tool & channel layer
  ├── clarity-mcp          MCP protocol: stdio / SSE / WebSocket
  └── clarity-channels     WeChat / Telegram / Discord / Slack

memory layer
  ├── clarity-memory       SQLite + BM25 + embedding vector search
  ├── clarity-thread-store  Conversation persistence
  └── clarity-rollout      JSONL rollout storage

infra
  ├── clarity-gateway      HTTP + WebSocket server
  ├── clarity-wire         Internal communication protocol
  ├── clarity-telemetry    Metrics, traces, config audit
  ├── clarity-secrets      ChaCha20-Poly1305 encrypted storage
  └── clarity-mobile-core  Android/iOS FFI bindings
```

---

## Key Technical Decisions

| Decision | Why |
|:---|:---|
| **Contract-core-frontend split** | Zero-dependency contract crate → new features only touch 1 layer |
| **ReAct + Plan dual mode** | Plan mode: step-missing rate dropped from ~40% to near 0 |
| **MCP triple-transport** | stdio (local tools), SSE (streaming), WebSocket (bidirectional) |
| **Pure SQL vector search** | `cosine_similarity` UDF in SQLite → no external vector DB needed |
| **ChaCha20-Poly1305 secrets** | Encrypted at rest, never in plaintext config |
| **5 UI backends** | TUI (terminal), egui (native), slint (embedded), tauri (web), headless (server) |

---

## Scale

| Metric | Value |
|:---|:---|
| Crates | 25 |
| Lines of Rust | 152,000 |
| Tests | 1,243 |
| Production code | Zero `unwrap`/`expect` |
| Lint | Clippy zero-warning |
| License | AGPL-3.0 |
