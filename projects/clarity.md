# Clarity — AI Agent Runtime

> **面向具身智能的本地优先分布式人格连续运行时**
>
> https://github.com/juice094/clarity

---

## 一句话

Clarity 不是"又一个本地大模型客户端"。它是一个**分布式人格连续层**——让同一个 AI 身份能在不同模型、不同设备、不同网络边界之间，保持人格、记忆和社会关系的一致性。

---

## 起源：从会话隔离到身份连续

现有的 AI 助手启动在不同终端时，会面临上下文会话隔离、角色扮演断裂、跨日连续性和跨会话继承问题。Clarity 的灵感来自《魔法禁书目录》的"御坂网络"——一个共享记忆、独立身体的分布式个体网络。

## 分布式 AI 身份的四层模型

| 层级 | 含义 | Clarity 映射 |
|:---|:---|:---|
| **Identity（身份认同层）** | 我是谁、我的价值观、我的社会关系、我对用户的长期承诺 | `clarity-contract` capability/personality token, `clarity-secrets` 加密的身份密钥 |
| **Personality（人格配置层）** | 角色扮演、语气、工作风格、伦理边界 | `clarity-core::personality`、skills/、系统提示模板 |
| **Memory Graph（记忆图谱层）** | 事实记忆、情感记忆、关系记忆、项目上下文 | `clarity-memory`（SQLite + BM25 + 向量 + 归档） |
| **Avatar/Instance（分身实例层）** | 运行在具体设备上的模型实例，能力各异 | egui / tui / Axum / headless / 系统托盘 / UniFFI 移动核心 |

关键设计：Identity 和 Personality 是网络级共享的；Memory 是分级同步的；Avatar 是本地自治的。

## 三个核心机制

### 1. 分身自治 + 离线连续性
每个 avatar 本地持有完整的人格配置和最近 N 条/最关键的 memory 子集。断网时像"失联的御坂妹妹"一样继续工作。重连后通过 delta merge 同步记忆增量。

### 2. 记忆联邦与脱敏合并
敏感场景下 avatar 先在本地完成推理，只把脱敏后的抽象记忆/结论/关系更新广播到网络。原始隐私数据不上云，知识图谱和关系权重可共享，冲突时以高信任设备/最近修改为准。

### 3. 同一意识的多模型表达
云端模型负责复杂推理，本地模型负责隐私敏感任务，移动端小模型负责简单提醒——共享同一个 Identity，但能力不同、知识边界不同。用户面对的不是"三个不同的 AI"，而是"同一个 AI 在不同身体上的不同形态"。

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
