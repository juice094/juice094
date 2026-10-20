# 周景潇

**数据科学与大数据技术 · 大三在读 · 本科 2027 届** · 上海 / 北京 / 深圳 / 杭州 / 成都

📞 13626566112 · 📧 2241470466@qq.com · 🔗 github.com/juice094

**求职意向**：AI Agent 开发 / 后端系统开发 / 智能体平台研发

---

## 核心亮点

- **3 个独立交付的生产级 Rust 系统**：AI Agent 运行时、P2P 文件同步引擎、开发者知识库编译器，累计 21+14+12=47 workspace crates，测试基线全绿。
- **AI Agent 全栈能力**：自研 ReAct/Plan 双模式 Agent loop，实现 MCP 协议 stdio/SSE/WebSocket 三传输，落地 81 个 MCP 工具，支撑代码/笔记/工作流的 AI 可推理上下文。
- **底层系统工程能力**：从零实现 BEP 协议栈、NAT 穿透（STUN/UPnP/Relay）、SQLite 嵌入式存储与混合检索、TLS 设备证书与 P2P 安全传输。
- **工程基线扎实**：Clippy 0 warning，生产代码零 unwrap/expect/panic，单二进制分发，具备公网部署与跨国运维经验。

---

## 技术技能

| 领域 | 技术栈 |
|:---|:---|
| **语言** | Rust（主力）、Python、SQL |
| **异步 / 网络** | Tokio、Axum、Tower、reqwest、WebSocket、rustls |
| **存储 / 检索** | SQLite、rusqlite、Tantivy、BM25、embedding vector search |
| **AI / Agent** | ReAct、Plan、MCP、Multi-Agent 编排、RAG、Candle / GGUF |
| **分布式 / P2P** | BEP 协议、STUN、UPnP、Relay、NAT 穿透、块级同步 |
| **安全** | ChaCha20-Poly1305、TLS 1.3、自签名设备证书 |
| **跨平台** | egui、ratatui、headless、UniFFI |
| **工程化** | Cargo Workspace、GitHub Actions、Clippy、tracing、criterion |

---

## 项目经历

### Clarity — 本地优先 AI Agent Runtime

> Rust 原生 Agent 运行时，21 crate Workspace，约 15 万行 Rust，测试基线全绿，Clippy 0 warning。github.com/juice094/clarity

- **自研 ReAct + Plan 双模式 Agent loop**，将长任务步骤遗漏率从 ~40% 降至接近零，两种模式共享统一工具注册表。
- **实现 MCP 协议三传输**（stdio / SSE / WebSocket），让 LLM 可安全调用本地文件、搜索、shell 等工具，与具体 LLM provider 解耦。
- **构建零外部依赖的记忆系统**：SQLite + BM25 + embedding 混合检索，手写 `cosine_similarity` UDF，单文件部署即可支撑长期记忆与上下文召回。
- **实现跨平台多入口**：egui 桌面 GUI + ratatui 终端 UI + headless 服务端 + UniFFI 移动端 FFI，四端共享同一 Agent 内核。

### syncthing-rust — P2P 文件同步引擎

> Go Syncthing 的 Rust 兼容实现，9 lib + 5 binary crate，约 5.3 万行 Rust，413 passed / 0 failed 测试基线。github.com/juice094/syncthing-rust

- **从零实现 BEP 协议栈**，基于 prost 完成编解码，配套 wire_compat 集成测试验证与 Go Syncthing 的线缆级兼容。
- **落地多路径 NAT 穿透**：STUN + UPnP + Relay v1 + 本地/全球发现，覆盖 LAN / 公网 / 中继三种网络环境。
- **构建高可靠同步链路**：scanner / puller / index-handler / block-server 全链路块级同步，文本三路合并 + Simple/Staggered 版本归档，降低并发冲突导致的数据丢失风险。
- **Windows release 单二进制约 16 MB，零运行时依赖**，已在日本 VPS 与国内 Windows 桌面跨国组网运行。

### devbase — 开发者工作空间"世界模型编译器"

> 本地优先开发者知识库，12 workspace crates + 主 crate，约 5.9 万行 Rust，81 个 MCP stdio 工具。github.com/juice094/devbase

- **以 MCP 协议暴露 81 个 stdio 工具**，覆盖代码解析、Git 分析、知识检索、Skill 执行、YAML 工作流，人类用 ratatui 仪表盘，AI 用 `devbase mcp`。
- **实现 SQLite + Tantivy 混合语义检索**：Tantivy 负责 BM25 全文/符号索引，SQLite BLOB 存 embedding + 自定义 cosine_similarity UDF，无需专用向量库。
- **设计 YAML DAG 工作流引擎**：5 种 step 类型 + Kahn 拓扑调度 + 变量插值 + SQLite 执行状态持久化，支持条件分支与循环。
- **实践 Workspace 治理与架构红线**：`src/main.rs` 控制在 836 行，子 crate 禁止反向依赖主库，生产代码 unwrap/expect/panic = 0。

---

## 研究经历

**检索增强生成中输出结构的实证研究** · 2026.03 — 至今 · [acr-select](https://github.com/juice094/acr-select)

- 设计 40 实验条件、3000+ 样本的多因子受控实验，提出格式-内容双维度观测框架。
- 跨 4 种模型架构验证框架普适性，论文撰写中。

---

## 教育背景

**甘肃农业大学** · 数据科学与大数据技术 · 工学学士 · 2023.09 — 2027.06
- 信息科学技术学院 · 均分 83 / 核心课 86 · 专业前 10%
- 主修：数据结构与算法、操作系统、计算机网络、数据库原理、分布式系统、机器学习

---

## 奖项与认证

- AI 应用工程师（中级）— 工业和信息化部认证
- 日语专业四级（72 分）· 大学英语四级（CET-4）

---

## 公网部署经验

| 项目 | 平台 | 说明 |
|------|------|------|
| Clarity Web 前端 | Vercel | Rust→Wasm 编译后 CDN 边缘分发 |
| syncthing-rust P2P 节点 | 日本 VPS | 跨国组网，Tailscale + Windows 桌面端实际运维 |
