# 周景潇

**数据科学与大数据技术 · 大三在读 · 本科 2027 届** · 上海 / 北京 / 深圳 / 杭州 / 成都

📞 13626566112 · 📧 2241470466@qq.com · 🔗 github.com/juice094

**求职意向**：AI Agent 开发 / 后端系统开发 / 智能体平台研发

---

## 教育背景

**甘肃农业大学** · 数据科学与大数据技术 · 工学学士 · 2023.09 — 2027.06
- 信息科学技术学院 · 均分 83 / 核心课 86 · 专业前 10%
- 主修课程：数据结构与算法、操作系统、计算机网络、数据库原理、分布式系统、机器学习、大数据技术基础、数据可视化

---

## 技术技能

1. **Rust 系统开发**：主力语言，独立完成 3 个生产级 Rust 项目，核心代码约 6 万行；主导 21 crate 的 Cargo Workspace 架构设计与持续演进。
2. **Python AI 工程**：用于算法验证、测试自动化与 AI 项目落地，核心代码约 2 万行。
3. **Tokio 异步生态**：构建高并发 Agent loop、后台任务调度与多设备状态管理。
4. **网络服务**：Axum + Tower + reqwest + tokio-tungstenite，实现 HTTP/WebSocket 网关与安全客户端。
5. **嵌入式存储**：SQLite + rusqlite，实现零外部依赖的数据持久化，支撑记忆、会话、设备身份等核心状态。
6. **混合检索**：BM25 + embedding 向量搜索，手写 `cosine_similarity` SQLite UDF 完成 RAG 记忆召回。
7. **AI Agent 架构**：ReAct + Plan 双模式 Agent loop，降低长任务步骤遗漏率。
8. **MCP 协议**：实现 stdio / SSE / WebSocket 三传输工具调用与发现机制。
9. **Multi-Agent 协作**：sub-agent 并行编排与注册表机制，实现多 Agent 协同任务执行。
10. **P2P 分布式系统**：BEP 协议、NAT 穿透（STUN / UPnP / Relay）、块级文件同步与冲突解决。
11. **跨平台 UI**：egui / ratatui 构建桌面/终端界面，UniFFI 暴露移动端 FFI。
12. **安全与密码学**：ChaCha20-Poly1305 静态加密、rustls TLS、自签名设备证书。

---

## 项目经历

### Clarity — 本地优先分布式 AI Agent Runtime

> Rust 原生 AI Agent 运行时，支持同一身份跨设备保持人格、记忆与社会关系一致。21 crate Cargo Workspace，约 15 万行 Rust，测试基线全绿，Clippy 0 warning。
> github.com/juice094/clarity · 2026.04 - 至今

**背景与挑战**：现有 AI 助手处理多步骤任务时常因上下文窗口限制和工具调用链路断裂导致步骤遗漏；云端方案存在隐私与延迟问题。需要构建一个本地优先、跨设备一致的 Agent 运行时。

- **自研 ReAct + Plan 双模式 Agent Loop**：针对 ReAct 在长任务中容易遗漏步骤的问题，设计显式 Plan 模式，将长任务拆分为检查点并强制"计划-执行"校验；两种模式共享同一工具注册表，避免重复实现。Plan 模式显著降低复杂任务步骤遗漏率。
- **零外部依赖的本地记忆与混合检索**：基于 SQLite + rusqlite 构建记忆层，手写 `cosine_similarity` UDF 计算向量相似度，结合 BM25 全文检索与 embedding 向量搜索；数据以单文件 SQLite 存储，无需外部数据库即可支持关键词 + 语义混合召回。
- **MCP 三传输工具协议与跨平台 UI**：实现 MCP 协议，支持 stdio（本地进程）、SSE（服务器推送）、WebSocket（双向实时）三种传输；用 egui 构建桌面 GUI、ratatui 构建 TUI、headless 提供服务端入口，并通过 UniFFI 暴露移动核心，多入口共享同一 Agent 内核。

---

### syncthing-rust — 兼容 Go 官方实现的 P2P 文件同步引擎

> Syncthing BEP 协议的 Rust 实现，与官方 Go 客户端线路兼容。9 个 library crate + 5 个 command binary，约 5.3 万行 Rust，413 passed / 6 ignored / 0 failed 测试基线。
> github.com/juice094/syncthing-rust · 2025.11 - 至今

**背景与挑战**：官方 Syncthing 基于 Go 实现，Rust 生态缺乏生产级兼容实现。挑战在于必须保证与官方 Go 客户端的线缆级协议兼容，同时处理 NAT 后设备无法直连、并发修改冲突等复杂场景。

- **BEP 协议精确复刻与跨语言兼容**：基于 `prost` 实现 Hello / ClusterConfig / Index / Request / Response 等消息编解码；实现 BEP over TLS 握手与自定义证书验证；配套 `wire_compat` 集成测试对比 Go 官方线路二进制数据，验证跨语言互操作。
- **多路径 NAT 穿透与连接降级**：集成 UDP 本地广播、HTTPS 全球发现、STUN 公网地址探测、UPnP 端口映射与 Relay Protocol v1；当直连失败时自动 fallback 到 relay，覆盖 LAN / 公网 / 中继三种网络环境。
- **高可靠文件同步与冲突解决**：实现 scanner / puller / index-handler / block-server 全链路块级同步；针对 Windows 句柄共享冲突实现指数退避重命名回退；基于 base/local/remote 实现文本三路合并；支持 Simple / Staggered 版本归档策略，降低并发冲突与数据丢失风险。

---

### devbase — 开发者工作空间"世界模型编译器"

> 本地优先的开发者知识库管理器，将代码库、笔记、Skill 与工作流编译为 AI 可推理的结构化上下文。12 个 workspace crates + 主 crate，约 5.9 万行 Rust，`src/main.rs` 836 行，81 个 MCP stdio 工具。
> github.com/juice094/devbase · 2026.01 - 至今

**背景与挑战**：AI 工具需要可推理的代码/笔记/工作流上下文，但云端方案存在隐私与延迟问题；现有工具割裂且依赖繁重。需要构建一个零外部依赖、高内聚的开发者基础设施。

- **世界模型编译器与 81 个 MCP 工具**：用 Rust 2024 构建 devbase，集成 tree-sitter 多语言解析、SQLite WAL 关系存储、Tantivy BM25、PARA/WikiLink 知识管理；所有能力通过 MCP stdio 协议暴露为 81 个工具，人类可通过 ratatui 仪表盘使用，AI 客户端可通过 `devbase mcp` 调用全部能力。
- **SQLite + Tantivy 混合语义检索**：Tantivy 负责 BM25 全文/符号索引；SQLite BLOB 存储 embedding，注册自定义 `cosine_similarity` 标量函数计算向量相似度；默认 feature 下无需 Candle/Ollama 即可运行关键词检索，开启 embedding feature 后可本地生成 embedding。
- **YAML DAG 工作流引擎与 Workspace 治理**：定义 Skill / Subworkflow / Parallel / Condition / Loop 5 种 step 类型，实现 YAML 解析、依赖验证、拓扑调度（Kahn 算法）、变量插值与 SQLite 持久化执行状态；以 `devbase-core-types` 为根节点拆分 12 个 workspace crate，子 crate 禁止反向依赖主库，`src/` 生产代码 unwrap/expect/panic 数量为 0。

---

## 研究经历

### 检索增强生成中输出结构的实证研究（2026.03 — 至今）

代码仓库：[acr-select](https://github.com/juice094/acr-select)

围绕 RAG 系统中输出格式与内容质量的交互关系，设计并执行受控实验框架。设计 ~40 实验条件、3000+ 样本的多因子受控实验；提出格式-内容双维度观测框架；跨四种模型架构验证框架普适性；主动发现测量 artifact 并设计统一评分协议修正统计推断。论文撰写中（manuscript in progress）。

---

## 奖项与认证

- AI 应用工程师（中级）— 工业和信息化部认证
- 日语专业四级（72 分）
- 大学英语四级（CET-4）

---

## 自我评价

大三在读，2025.11-2026.06 独立设计并交付三个生产级 Rust 系统。从 BEP 协议栈到 Agent 内核到开发者工作空间编译器，均从零构建。具备独立闭环能力：发现问题 → 设计实验 → 实现系统 → 迭代优化。对 AI Agent 核心架构有从 0 到 1 的工程理解——Contract-First 分层、ReAct/Plan 双模式循环、MCP 协议三传输、混合记忆系统。Rust + AI Agent 双稀缺组合，具备将底层系统设计能力迁移到多语言业务栈的基础。

---

### 公网部署经验

| 项目 | 平台 | 说明 |
|------|------|------|
| **Clarity** Web 前端 | Vercel | Rust→Wasm 编译后通过 CDN 全球边缘分发 |
| **syncthing-rust** P2P 守护进程 | 日本 VPS | 跨墙部署 P2P 文件同步节点，通过 Tailscale 与国内 Windows 桌面端组网 |

---

*本版简历基于源码审计数据生成，已修正：clarity crate 数、syncthing-rust 测试数与二进制大小、devbase MCP 工具数量、ed25519 设备证书表述等。*
