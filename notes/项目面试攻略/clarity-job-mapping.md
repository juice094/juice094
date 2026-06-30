# Clarity 岗位映射与术语速查

> 根据目标岗位，决定简历突出 Clarity 的哪些模块、使用哪些专业术语。
> 术语不是越多越好，关键是和岗位能力模型对齐。

---

## 一、岗位 → 简历重点 → 术语

| 目标岗位 | 简历重点 | 该深挖的术语 |
|:---|:---|:---|
| **Rust 系统工程师 / 后端基础架构** | workspace 拆分、工程纪律、并发、网络、存储 | Tokio、Axum、rustls、parking_lot、zero unwrap、contract-first、workspace 模块化 |
| **AI Agent / LLM Infra 工程师** | ReAct/Plan、MCP、tool registry、多模型抽象 | MCP protocol、ReAct、Plan、tool use、multi-provider LLM abstraction、sub-agent orchestration |
| **本地优先 / 隐私计算 / 分布式系统** | local-first、多设备同步、身份自持、离线可用 | local-first、self-sovereign identity、eventual consistency、CRDT、delta sync、AP under CAP |
| **数据库 / 搜索 / RAG 工程师** | SQLite 向量检索、BM25 + embedding 混合搜索 | SQLite UDF、BM25、vector search、hybrid retrieval、RAG retrieval |
| **跨平台 / 移动端 Rust 工程师** | egui、TUI、UniFFI、多入口 | egui、ratatui、immediate mode GUI、UniFFI、FFI bindings、cdylib/staticlib |
| **安全 / 密码学工程师** | 静态加密、密钥管理、TLS | ChaCha20-Poly1305、AEAD、secret management、rustls、key derivation |

---

## 二、术语安全度分级

写简历时，不同来源的术语需要不同程度的解释。

### 工业标准 / 经典框架（可直接写）

`tokio`、`serde`、`axum`、`tower-http`、`reqwest`、`tokio-tungstenite`、`rustls`、`rusqlite`、`chrono`、`uuid`、`regex`、`clap`、`tracing`、`anyhow`/`thiserror`、`parking_lot`、`rayon`、`criterion`、`rand`、`egui`/`eframe`、`ratatui`、`uniffi`、`syntect`、`pulldown-cmark`、`chacha20poly1305`、`ring`

### 新兴 / 有辨识度但需解释

- **candle-core / candle-transformers**：HuggingFace Rust ML 框架，本地推理方案
- **MCP (Model Context Protocol)**：Anthropic 2024 提出的 Agent 工具协议
- **tiktoken-rs**：OpenAI BPE tokenizer 的 Rust 社区实现

### 自研模块 / 必须说明是"自己做的"

所有 `clarity-*` crate，如 `clarity-core`、`clarity-memory`、`clarity-mcp`、`clarity-gateway`、`clarity-wire`、`clarity-secrets`、`clarity-subagents` 等。简历中应表述为"自研 XX 模块"，而非外部框架。

---

## 三、使用建议

1. **先定岗位，再挑模块**。
   不要试图在一份简历里同时强调"分布式系统""RAG""移动端 FFI""密码学"，会分散重点。

2. **每个术语都要能 defend**。
   写"CRDT"就要讲清楚是 state-based / op-based / delta-based；写"self-sovereign identity"就要说明私钥如何生成和恢复。

3. **优先用标准框架背书自研模块**。
   例如："基于 Tokio + Axum 构建网关，自研 clarity-mcp 实现 MCP 三传输协议"。

4. **避免把自研 crate 和外部框架混为一谈**。
   错误："使用 clarity-core、tokio、axum 等框架。"
   正确："基于 Tokio + Axum，自研 clarity-core 实现 ReAct/Plan 双模式 Agent loop。"

---

## 四、快速自检

投某个岗位前，问自己：

- [ ] 我是否突出了该岗位最看重的 2-3 个技术点？
- [ ] 我写的每个专业术语，都能在面试中解释清楚原理和 Clarity 中的具体实现？
- [ ] 我的量化指标（crate 数、测试数、性能数据）是否和岗位关注点一致？
- [ ] 我是否避免了把产品语言（"御坂网络""人格连续"）直接当技术语言用？
