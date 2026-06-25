> **用途**：个人项目简历技术资产清单，按项目分章节、8 个维度整理。
> **生成日期**：2026-06-25
> **数据基线**：`AGENTS.md`、仓库实机验证、实际代码与文档

---

# 简历技术资产清单

## 目录

1. [Clarity —— Rust 本地优先 AI 运行时](#1-clarity--rust-本地优先-ai-运行时)
2. [syncthing-rust —— BEP 协议 P2P 文件同步守护进程](#2-syncthing-rust--bep-协议-p2p-文件同步守护进程)
3. [devbase —— 本地优先开发者工作空间世界模型编译器](#3-devbase--本地优先开发者工作空间世界模型编译器)

---

# 1. Clarity —— Rust 本地优先 AI 运行时

## 1.1 项目定位

Clarity 是一个 **Rust 原生的本地优先（local-first）个人 AI 运行时**，用同一套 Agent 内核支撑 TUI、桌面 GUI、Web IDE、无头 CLI、系统托盘和移动端 FFI 六种入口。它聚焦**编码/工程工作流**，在本地完成 LLM 编排、工具调用（MCP + 内置工具）、记忆持久化、审批流程与多 Agent 协作，**无需 Python/Node.js/Ollama 等外部运行时**。

目标用户是需要在本地安全、可控地运行 AI 协作者的开发者；典型场景包括代码审查、自动化脚本、本地知识库问答、CI 集成与多步骤工程任务执行。

---

## 1.2 模块结构与职责

| 模块/Crate | 一句话职责 |
|-----------|-----------|
| `clarity-contract` | 共享契约层：`LlmProvider`/`Tool`/`AgentError` 等 trait，零内部依赖（`crates/clarity-contract/src/`） |
| `clarity-wire` | UI ↔ Agent 的 SPMC 事件总线，承载 `WireMessage`/`ViewCommand`（`crates/clarity-wire/src/`） |
| `clarity-core` | Agent 内核：ReAct/Plan 循环、Approval、Skill、MCP 集成、后台任务、Thread 生命周期（`crates/clarity-core/src/agent/`） |
| `clarity-llm` | LLM provider 抽象 + 6+ 内置 provider + Candle GGUF 本地推理（`crates/clarity-llm/src/`） |
| `clarity-memory` | 混合记忆：SQLite + BM25 + 向量搜索 + chunking + 四级压缩归档（`crates/clarity-memory/src/`） |
| `clarity-mcp` | MCP 客户端：stdio / SSE / HTTP / WebSocket 四传输（`crates/clarity-mcp/src/`） |
| `clarity-tools` | 内置工具库：file / shell / web / devkit / team / task（`crates/clarity-tools/src/`） |
| `clarity-subagents` | 子代理执行器 + 并行调度，消费 `clarity-core`（`crates/clarity-subagents/src/`） |
| `clarity-thread-store` | Thread 持久化抽象，`ThreadStore` trait（`crates/clarity-thread-store/src/`） |
| `clarity-rollout` | JSONL rollout 持久化：事件日志、压缩、回放（`crates/clarity-rollout/src/`） |
| `clarity-openclaw` | OpenClaw/KimiClaw Gateway WebSocket 客户端与设备身份（`crates/clarity-openclaw/src/`） |
| `clarity-secrets` | ChaCha20-Poly1305 加密 Secret 存储（`enc2:`）（`crates/clarity-secrets/src/`） |
| `clarity-telemetry` | 统一遥测：WideEvent、metrics、traces、config audit（`crates/clarity-telemetry/src/`） |
| `clarity-gateway` | Axum HTTP/WebSocket 服务端 + Web IDE + session store（`crates/clarity-gateway/src/`） |
| `clarity-egui` | 桌面 GUI 主入口：eframe/egui + Pretext 三栏布局（`crates/clarity-egui/src/`） |
| `clarity-tui` | ratatui 终端界面（`crates/clarity-tui/src/`） |
| `clarity-claw` | 系统托盘常驻节点，仅通过 Gateway WebSocket 通信（`crates/clarity-claw/src/`） |
| `clarity-headless` | 无头 CLI，脚本/CI 场景（`crates/clarity-headless/src/`） |
| `clarity-mobile-core` | 移动端 UniFFI FFI 核心，暴露 Runtime/事件/配置/记忆接口（`crates/clarity-mobile-core/src/`） |
| `clarity-slint` | 实验性 Slint 桌面 GUI，不参与默认 CI（`crates/clarity-slint/src/`） |
| `clarity-anthropic-proxy` | Anthropic Messages API → DeepSeek 代理工具（`crates/clarity-anthropic-proxy/src/`） |
| `clarity-tauri` | **已归档**，被 workspace 排除（`crates/clarity-tauri/`） |

---

## 1.3 核心架构模式

| 架构模式 | 解决什么问题 | 在项目中的体现 |
|---------|-------------|---------------|
| **Contract-First** | 避免循环依赖，给 LLM/Tool/错误类型一个稳定契约 | `clarity-contract` 零内部依赖，所有 crate 都基于它构建；`crates/clarity-contract/src/lib.rs` |
| **严格分层架构** | 隔离前端、内核、基础设施，保证核心可测试、可移植 | `contract → infrastructure → core → presentation`；前端 crate 禁止互相 import（`AGENTS.md` §3 不变量） |
| **事件驱动（SPMC）** | 同一 Agent 状态被多个前端消费，避免 N×M 耦合 | `clarity-wire` 单生产者多消费者通道；`WireMessage` 是跨前端唯一协议（`crates/clarity-wire/src/`） |
| **多前端共享内核** | 一套 Agent 逻辑同时服务 GUI/TUI/Web/CLI/托盘 | 所有前端消费 `clarity-core` + `clarity-wire`，不重复实现业务逻辑 |
| **插件化工具生态（MCP）** | 让外部工具服务器以标准协议接入，不污染核心 | `clarity-mcp` 支持 stdio/SSE/HTTP/WS 四传输；`clarity-tools` 内置工具也走同一 `Tool` trait |
| **CQRS 式 UI 状态** | 命令与视图状态分离，支持流式更新与历史回放 | `ViewCommand` 驱动渲染，`ViewState` 单源化；`clarity-egui/src/ui/` 与 `clarity-core/src/ui/` |
| **本地优先 + 单二进制** | 降低部署成本，消除运行时依赖冲突 | 每个 bin crate 单二进制分发；默认内置 Candle GGUF；`cargo install` 即可运行 |
| **审批模式四层模型** | 在高风险工具调用与用户自由之间取得平衡 | `Interactive/Smart/Plan/Yolo` 四级 Approval；`clarity-core/src/approval/` |

---

## 1.4 关键技术栈

### 语言/运行时
- **Rust 2024 edition**，MSRV 1.85
- **tokio** 异步运行时

### 前端/交互
- **egui 0.31 / eframe 0.31** — 纯 Rust 即时模式桌面 GUI，零 Web 依赖
- **ratatui 0.30** — 终端 UI
- **Axum 0.7 / tower-http / SSE / WebSocket** — Web IDE 与服务端
- **Slint** — 实验性 GUI 栈

### AI/LLM
- **Candle** — 本地 GGUF 推理（Qwen2 / Qwen2.5 / DeepSeek-R1-Distill）
- **MCP（Model Context Protocol）** — 工具生态标准协议
- **ReAct / Plan Agent 循环** — 推理+行动模式

### 记忆/存储
- **SQLite（WAL）** — 结构化持久化
- **BM25** — 关键词检索
- **向量搜索** — 语义检索
- **四级压缩归档** — 上下文压缩与 token 爆炸防护

### 安全/通信
- **ChaCha20-Poly1305** — `enc2:` 加密 Secret 存储
- **rustls-tls** — 纯 Rust TLS；openssl 已从依赖树移除
- **tokio-tungstenite** — WebSocket
- **ed25519-dalek** — 设备身份签名

### 移动端/FFI
- **UniFFI 0.29** — Kotlin/Swift 绑定生成

### 构建/部署
- **cargo workspace** 管理 22+ crate
- **cargo-wix** — Windows MSI 打包
- **GitHub Actions CI** — 12-job 流水线

### 能体现技术深度的非大众选型
1. **Candle GGUF 本地推理**：不依赖 llama.cpp/Ollama，纯 Rust 推理栈
2. **BM25 + 向量混合记忆**：自研检索组合，而非直接上 Qdrant/Pinecone
3. **SPMC 事件总线替代 RPC**：前端与内核在同一进程内通过内存通道解耦
4. **Pretext 文字测量后端**：为 egui 聊天界面做精确高度估算与对齐回归
5. **UniFFI 移动 FFI**：把 Rust Agent 运行时封装为 Android/iOS 可调用的库

---

## 1.5 解决过的 3 个最硬核技术问题

### 问题 1：Pretext 三栏布局下的消息气泡高度精确估算
- **问题描述**：`clarity-egui` 聊天界面需要在不知道最终渲染宽度的情况下，提前估算 `MessageBubble` 高度以支撑虚拟滚动和右侧轨道布局；传统 egui 文本测量在复杂样式（行内代码、链接、不同字号）下偏差大，导致 1000+ 条消息时滚动跳变。
- **方案**：接入 `pretext-core` / `pretext-fontdb`，用 egui 字体栈作为 measurement backend，实现 `pretext::EguiFontMetrics`；将 `MessageBubble` 与 `widgets/rich_paragraph.rs` 迁移为 pretext-aware；默认启用 estimate + render 双阶段测量。
- **关键技术**：文字测量后端抽象、字体 metric 映射、对齐回归测试、release 性能基准。
- **可量化结果**：23 样本对齐回归测试通过，1000 条消息 release 基准下聚合高度偏差 ≈ **1.45%**，estimate 阶段 ≈ **74.4 µs/msg**，render 阶段 ≈ **135.7 µs/msg**。
- **相关路径**：`crates/clarity-egui/src/widgets/rich_paragraph.rs`、`crates/clarity-egui/src/components/chat/message_bubble.rs`（若存在）、`crates/clarity-egui/src/layout.rs`、`AGENTS.md` §11.1。

### 问题 2：Claw 协议 dialect 统一与解耦
- **问题描述**：早期 `clarity-egui` 直接通过协议标志 `claw_ws_uses_sessions_send` 决定发送方式，导致 UI 层泄漏 Claw/OpenClaw 协议细节；同时 `clarity-claw` 角色模糊，既想做内部托盘节点又想兼任外部 OpenClaw 适配器。
- **方案**：决策 Gateway WebSocket 为 Clarity 内部唯一协议；OpenClaw JSON-RPC 仅作为外部 KimiClaw/OpenClaw Gateway 互通的 fallback；由 `ClawConnectionManager` 根据检测到的 dialect 自行决定发送方法；删除 egui 层协议泄漏字段；明确 `clarity-claw` 只做 Gateway WebSocket 客户端/系统托盘节点，移除未使用的 federation coordinator/nodes/runtime 骨架。
- **关键技术**：协议 dialect 检测、职责边界重构、依赖方向审计、 dead code 清理。
- **可量化结果**：消除了 UI ↔ 协议之间的反向依赖；`clarity-claw` 代码体积收缩；协议映射关系写入 `docs/architecture/claw-protocol.md`。
- **相关路径**：`crates/clarity-openclaw/src/`、`crates/clarity-claw/src/`、`docs/architecture/claw-protocol.md`、`AGENTS.md` §11.1。

### 问题 3：零外部依赖的本地优先 AI 运行时
- **问题描述**：大多数 AI Agent 项目依赖 Python/Node.js/Ollama/llama.cpp 等外部运行时，导致安装复杂、版本冲突、离线场景受限。
- **方案**：用 Rust 完整实现 Agent 内核；LLM 推理用 Candle 原生 GGUF；记忆用 SQLite + 自研 BM25/向量；前端用 egui/ratatui/Axum 纯 Rust 栈；每个入口编译为单二进制；通过 `models.toml` + `enc2:` Secret + `ReliableProvider` failover 构建完整的本地 provider 体系。
- **关键技术**：Candle GGUF 集成、WAL SQLite、BM25+向量混合检索、ChaCha20-Poly1305、provider 抽象与 failover 链。
- **可量化结果**：22 个活跃 workspace crate、**1,554 lib tests / 275 bin tests / 34 doc tests / 26 集成测试全绿**、Clippy **零 warning**；单个 `cargo install` 即可运行。
- **相关路径**：`crates/clarity-llm/src/`、`crates/clarity-memory/src/`、`crates/clarity-secrets/src/`、`docs/development/provider-config.md`。

---

## 1.6 性能/规模/稳定性相关数据

| 指标 | 数值 | 来源/备注 |
|------|------|----------|
| 活跃 workspace crate 数 | 22 + 1 归档（`clarity-tauri`）+ 1 集成测试 crate | `Cargo.toml` / `AGENTS.md` |
| Rust 源文件数 | ~200+ | `docs/ARCHITECTURE.md` §2.1a（待精确统计） |
| lib 测试通过数 | **1,554 passed / 0 failed / 0 ignored** | 2026-06-25 实机验证 |
| bin 测试通过数 | **275 passed / 0 failed / 2 ignored** | 2026-06-25 实机验证 |
| doc 测试通过数 | **34 passed / 0 failed / 3 ignored** | 2026-06-25 实机验证 |
| 集成测试通过数 | **26 passed / 0 failed** | 2026-06-25 实机验证 |
| Clippy warning | **0** | `cargo clippy --workspace --lib --bins --tests --exclude clarity-slint -- -D warnings` |
| Pretext 高度偏差 | ≈ **1.45%** | 23 样本对齐回归测试（`AGENTS.md` §11.1） |
| Pretext estimate 耗时 | ≈ **74.4 µs/msg** | 1000 条消息 release 基准 |
| Pretext render 耗时 | ≈ **135.7 µs/msg** | 1000 条消息 release 基准 |
| unsafe 代码 | **1 处**（白名单，在 `clarity-memory`） | `AGENTS.md` §7.1 |
| 桌面 GUI 默认窗口 | 1280×800 | `AGENTS.md` §11.1 |
| 请求量/QPS/生产部署规模 | 待验证 | 项目定位为本地运行时，无公开服务端运行数据 |

---

## 1.7 简历专业化关键词

### 技术关键词
Rust 2024、tokio、egui、eframe、ratatui、Axum、tower-http、WebSocket、SSE、Candle、GGUF、MCP（Model Context Protocol）、SQLite、BM25、Vector Search、UniFFI、ChaCha20-Poly1305、rustls、ReAct、Plan、SPMC、WAL、JSONL、OAuth Device Flow、Cargo Workspace、CI/CD。

### 能力关键词
Contract-First 架构、严格分层架构、事件驱动架构、多前端共享内核、本地优先（Local-First）、零外部依赖、单二进制分发、混合检索（BM25 + Vector）、RAG、Multi-Agent 调度、审批模式设计、协议 dialect 统一、FFI 桥接、性能基准测试、回归测试、内存安全、零 unsafe 扩展、 Secret 加密存储、Provider Failover。

---

## 1.8 适合写在简历上的 3-5 条 Bullet Point

1. **主导 Rust 原生本地优先 AI 运行时架构设计**，用 22 个 workspace crate 实现 TUI/桌面 GUI/Web IDE/CLI/系统托盘/移动端 FFI 六入口共享同一 Agent 内核，实现 `cargo install` 即可运行，零 Python/Node.js/Ollama 外部依赖。

2. **实现混合记忆系统与本地 LLM 推理栈**，整合 SQLite + BM25 + 向量搜索 + 四级压缩归档，并接入 Candle GGUF 本地推理；配套 `models.toml` per-alias 配置、`enc2:` 加密 Secret、`ReliableProvider` 链式 failover。

3. **落地跨前端 SPMC 事件总线协议**，设计 `WireMessage`/`ViewCommand` 统一 UI ↔ Agent 通信，使 egui/ratatui/Axum 等前端不互相 import、不重复实现业务逻辑，支撑流式响应与状态回放。

4. **统一 Claw/OpenClaw 协议边界**，决策 Gateway WebSocket 为内部唯一协议、OpenClaw JSON-RPC 为外部 fallback，由 `ClawConnectionManager` 自动检测 dialect，消除 UI 层协议泄漏，并输出 `docs/architecture/claw-protocol.md`。

5. **建立零 warning、零失败的工程基线**：推动 `cargo clippy -D warnings` 全绿、维护 1,554+ lib / 275 bin / 34 doc / 26 集成测试全通过；引入 Pretext 文字测量使 1000 条消息渲染高度偏差降至 1.45%。

---

## 1.9 不确定/待验证项

- 精确 Rust 源文件数量（约 200+，需 `find crates -name '*.rs' | wc -l` 精确统计）。
- 实际生产运行中的请求量、并发数、QPS（项目为本地运行时，一般无公开服务端指标）。
- 部分子模块（如 `clarity-telemetry` GreptimeDB 后端）是否已在 CI 默认流程中启用。
- `clarity-anthropic-proxy` 的日均调用量或生产稳定性数据（该 crate 为工具二进制，无公开指标）。

---

# 2. syncthing-rust —— BEP 协议 P2P 文件同步守护进程

## 2.1 项目定位

syncthing-rust 是 Syncthing 官方 BEP（Block Exchange Protocol）协议的 Rust 重写实现，目标是与官方 Go 守护进程保持线路兼容，并提供单静态二进制、零运行时依赖的 P2P 文件同步守护进程。

目标场景：个人/小团队跨平台私有文件同步（Windows ↔ Linux ↔ macOS），强调端到端加密、无中心服务器、LAN + 公网多路径发现。

技术形态：异步守护进程（CLI + TUI + Windows 托盘）+ 内部 Workspace 库集合（协议/网络/同步/存储/API 分层 crate）。

---

## 2.2 模块结构与职责

| 模块 / Crate | 一句话职责 |
|-------------|-----------|
| `cmd/syncthing` | 主守护进程入口、TUI 主循环、Windows 托盘集成、daemon 启动编排（`src/tui/daemon_runner.rs`） |
| `cmd/syncthing-cli` | 命令行工具：生成证书、查看设备 ID、刷新指标 |
| `cmd/syncthing-bench` | 同步基准测试与压测工具 |
| `cmd/syncthing-mcp-bridge` | MCP stdio JSON-RPC → REST API 桥接 |
| `cmd/syncthing-tray` | Windows 系统托盘薄 wrapper |
| `crates/syncthing-core` | 核心类型、trait、常量；禁止依赖内部 crate，是整个 Workspace 的"只读契约层"（`src/traits/mod.rs`） |
| `crates/bep-protocol` | BEP 消息的 prost 编解码、握手、连接帧；禁止直接 I/O（`tests/wire_compat.rs` 验证 Go 互操作） |
| `crates/syncthing-net` | TCP+TLS 传输、ConnectionManager、拨号评分、NAT 发现（UDP/mTLS/STUN/UPnP/Relay v1） |
| `crates/syncthing-sync` | 扫描器、拉取器、索引处理器、文件夹状态机、冲突解决、FolderOrchestrator 统一调度 |
| `crates/syncthing-fs` | 文件系统抽象、`.stignore` 解析、文件监控（watcher） |
| `crates/syncthing-db` | 基于 sled 的元数据与块缓存存储，对外仅暴露 `BlockStore` trait |
| `crates/syncthing-api` | Axum REST API + 事件总线 + 配置热重载；禁止直接持有 ConnectionManagerHandle 等具体类型 |
| `crates/syncthing-versioner` | Simple / Staggered 文件版本归档策略 |

---

## 2.3 核心架构模式

| 架构模式 | 解决什么问题 | 在仓库中的体现 |
|---------|-------------|---------------|
| **Cargo Workspace 分层架构** | 隔离协议 / 网络 / 同步 / 存储 / API 的变更范围，避免循环依赖 | `crates/*` 按职责严格分层；`syncthing-core` 位于最底层 |
| **Trait-Based 抽象 / 依赖倒置** | 让 API 层依赖契约而非具体实现，便于测试和替换后端 | `BlockStore`、`SyncModel` 等 trait 定义在 `syncthing-core`；`syncthing-db` / `syncthing-sync` 分别实现 |
| **事件驱动（Event Bus）** | TUI、REST API、健康检查之间实时同步状态变化 | `syncthing-api` 事件总线 + TUI event bridge（`cmd/syncthing/src/tui/mod.rs`） |
| **Actor-like 异步并发** | 单连接会话、文件夹扫描、拉取任务独立运行，互不阻塞 | `BepSession`（`crates/syncthing-net/src/session/`）、FolderOrchestrator 通过 tokio task 调度 |
| **Contract-First 协议设计** | 保证与 Go Syncthing 的跨语言互操作性 | `bep-protocol` 基于 protobuf schema 用 prost 生成编解码；配套 `wire_compat` 集成测试 |
| **预测性健康节流** | 在失败率/丢事件/状态翻转趋势恶化前自动降速 | `cmd/syncthing/src/health_predictor.rs` |

---

## 2.4 关键技术栈

| 类别 | 选型 |
|------|------|
| 语言 | Rust（edition 2021，要求 1.85+） |
| 异步运行时 | Tokio |
| TLS / 身份 | rustls 0.23 + tokio-rustls + ed25519-dalek 设备身份证书 |
| 协议 | BEP（prost 0.12）+ LZ4 压缩 |
| 网络 | TCP + TLS，ParallelDialer，Relay v1，自研 DERP，可选 WebSocket |
| NAT 发现 | UDP 广播、HTTPS mTLS Global Discovery、STUN、UPnP/PCP/NAT-PMP |
| 存储 | sled 0.34（嵌入式 KV）+ LRU 缓存 |
| REST API | Axum 0.7 + tower-http |
| TUI | ratatui 0.30 + crossterm 0.28 |
| 托盘 | Windows Win32 API（windows = "0.58"） |
| CLI / 构建 | clap 4.5、Cargo、just |
| 日志/可观测性 | tracing + tracing-subscriber + tracing-appender |

### 体现技术深度的非大众选型
- **ed25519-dalek + rustls 自定义设备证书**：不依赖系统 CA，设备 ID 直接由 TLS 证书公钥派生，与 Go Syncthing 的身份模型互操作。
- **sled 嵌入式 KV 作为同步元数据引擎**：无外部数据库依赖，但用 `BlockStore` trait 抽象，避免 sled API 泄漏到同步逻辑层。
- **prost + 自定义 LZ4 帧层**：在 Rust 中完整还原 BEP 长度前缀帧与压缩语义，并通过 `bep-protocol/tests/wire_compat.rs` 与 Go 实现做跨语言验证。
- **Windows Win32 托盘 IPC**：`cmd/syncthing/src/tray.rs` 直接用 Win32 API 实现托盘图标、右键菜单与 daemon 启停通信。

---

## 2.5 解决过的 3 个最硬核技术问题

### 问题 1：与 Go Syncthing 的 BEP 线路兼容性
- **问题描述**：Rust 实现必须与官方 Go 守护进程的 BEP over TLS 消息格式、握手顺序、ClusterConfig/Index/Request 帧语义完全一致，否则无法互联互通。
- **方案**：基于 protobuf schema 用 prost 生成编解码；实现长度前缀帧 + LZ4 压缩；在 `bep-protocol/tests/wire_compat.rs` 中构造 Go 实现的真实消息样本做 golden test。
- **关键技术**：prost 代码生成、LZ4 块压缩、rustls TLS 1.3、ed25519 设备证书派生。
- **可量化结果**：BEP wire compatibility 集成测试通过 10 项；`cargo test --workspace` 当前基线 **392 passed / 6 ignored / 0 failed**（来源：AGENTS.md）。

### 问题 2：Windows 高并发文件同步的稳定性（共享冲突与冲突解决）
- **问题描述**：Windows 下反病毒/编辑器/桌面搜索常持有文件句柄，导致 `fs::rename(tmp, real)` 出现 `ERROR_SHARING_VIOLATION`；同时双向同步会产生版本冲突。
- **方案**：实现带指数退避的 `rename_with_retry()` 三层回退；三路文本合并生成 git 风格冲突标记；Simple/Staggered 版本控制归档到 `.stversions/`。
- **关键技术**：Windows 错误码处理、指数退避重试、三路合并（three-way merge）、版本归档策略抽象。
- **可量化结果**：生产环境在 Windows 11 ↔ Ubuntu 24.04 双节点上稳定运行（来源：`docs/KNOWN_ISSUES.md`、运营记录）。

### 问题 3：预测性健康检查与自适应并发控制
- **问题描述**：多文件夹并发扫描/拉取时，网络抖动或 watcher 丢事件会导致失败率上升、状态频繁翻转，需要自动节流而非简单失败重试。
- **方案**：在 `cmd/syncthing/src/health_predictor.rs` 中订阅同步事件，评估失败率、watcher 丢事件率、状态翻转趋势；FolderOrchestrator 据此动态调整扫描/拉取并发；Puller 基于块请求 RTT 动态调整 downloads/blocks 并发。
- **关键技术**：事件驱动趋势分析、滑动窗口统计、自适应并发控制、RTT 反馈换挡。
- **可量化结果**：变更检测延迟约 ~1 秒；具体 72h 长跑压测完成度 **待验证**（项目将其列为 v3.1.0 准入线，尚未完成）。

---

## 2.6 性能/规模/稳定性相关数据

| 指标 | 数值 / 状态 | 来源 |
|------|------------|------|
| Rust 代码量 | ~58,848 行（.rs 生产/测试文件总计） | `git ls-files` + `wc -l` |
| Workspace crate 数 | 13（8 个库 crate + 5 个命令行/工具 crate） | `crates/` + `cmd/` |
| 测试基线 | **392 passed / 6 ignored / 0 failed** | AGENTS.md / CONTRIBUTING.md |
| Clippy 警告 | **0 warnings**（含 `-W clippy::await_holding_lock`） | AGENTS.md |
| Release 二进制大小 | ~13 MB 单静态二进制 | README.md |
| 默认 BEP 端口 | 22001（避免与 Go 版 22000 冲突） | AGENTS.md |
| 默认 REST API 端口 | 8385（仅 loopback） | AGENTS.md |
| 块大小 | 128 KiB | AGENTS.md |
| BEP 心跳 | 30s | AGENTS.md |
| 最大 BEP 消息 | 128 MiB | AGENTS.md |
| 最大连接数 | 1000 | AGENTS.md |
| 日志轮转 | 按小时，保留 168 个文件（7 天） | AGENTS.md |
| CI 平台矩阵 | ubuntu-latest / windows-latest / macos-latest，19 jobs | AGENTS.md / `.github/workflows/ci.yml` |
| 生产部署 | ROG-X（Windows 11）↔ Gray-Cloud（Ubuntu 24.04）via Tailscale | `docs/GRAY_CLOUD_OPS_MANUAL.md` |
| 72h 耐久测试 | 基础设施已具备，v3.1.0 准入线，完成度待验证 | AGENTS.md |
| 测试覆盖率数值 | 待验证（仓库未显式展示覆盖率百分比） | — |

---

## 2.7 简历专业化关键词

### 技术关键词
Rust · Tokio · async/await · rustls · TLS 1.3 · ed25519 · Protobuf / prost · LZ4 · BEP 协议 · P2P 文件同步 · NAT 穿透 · STUN · UPnP · Relay · sled · Axum · REST API · ratatui · TUI · Win32 API · clap · GitHub Actions · cargo-deny · cargo-audit

### 能力关键词
分层架构设计 · Trait-Based 抽象 / 依赖倒置 · 事件驱动架构 · 异步并发调度 · 协议互操作性 · 跨平台文件系统抽象 · 冲突解决 / 三路合并 · 版本控制策略 · 预测性健康检查 · 自适应并发控制 · 嵌入式存储抽象 · NAT 穿透与多路径发现 · 零运行时依赖部署 · 单二进制分发 · 生产级测试策略 · CI/CD 矩阵设计

---

## 2.8 适合写在简历上的 5 条 Bullet Point

1. 独立设计并实现了 13-crate Rust Workspace 架构，将 BEP 协议、网络传输、同步状态机、嵌入式存储、REST API 按职责分层，通过 `syncthing-core` trait 层实现库间解耦，支撑 58,848 行代码的可持续演进。
2. 完成 BEP over TLS 协议栈的 Rust 实现，基于 prost + rustls + ed25519-dalek 实现与 Go Syncthing v2.1.0 的线路兼容，配套 `wire_compat` 集成测试验证跨语言互操作。
3. 构建高可靠文件同步链路：针对 Windows 句柄共享冲突实现指数退避重命名回退，设计三路文本合并与 Simple/Staggered 版本归档策略，解决双向同步中的并发冲突与数据丢失风险。
4. 实现预测性健康检查与自适应并发机制：通过事件流评估失败率、watcher 丢事件和状态翻转趋势，由 FolderOrchestrator 与 Puller 动态调整扫描/拉取并发，提升高负载下的稳定性。
5. 主导生产级工程实践：`cargo test --workspace` 基线 392 passed / 0 failed，Clippy 0 warnings，release 单二进制约 13 MB，并建立 72h 耐久压测与多云 CI/CD 矩阵。

---

# 3. devbase —— 本地优先开发者工作空间世界模型编译器

## 3.1 项目定位

devbase 是一个本地优先的开发者工作空间世界模型编译器：用 Rust 将开发者本地的 Git 仓库、PARA 笔记、Skill 脚本与 YAML 工作流编译成 AI 可直接推理的结构化上下文，并通过 MCP（Model Context Protocol）协议以 71 个 stdio 工具的形式暴露给 AI Agent。

目标用户是需要在本地统一管理代码、知识与工作流的开发者与 AI Agent；技术形态为 Rust CLI + TUI 仪表盘 + MCP Server，核心是一个本地数据库与索引引擎（SQLite + Tantivy），零云端依赖。

关键入口：`src/main.rs`（CLI 入口，836 行）、`src/lib.rs`（30+ 模块导出）、`src/mcp/mod.rs`（MCP 协议层与工具路由）。

---

## 3.2 模块结构与职责

### 主 crate（src/）

| 模块 | 职责 |
|------|------|
| `src/commands/` | 9 类 CLI 子命令实现（repo/skill/workflow/knowledge/analysis 等） |
| `src/tui/` | ratatui 终端仪表盘：事件循环、布局、状态机、渲染组件 |
| `src/mcp/` | MCP Server：71 个工具、trait 抽象、请求路由、stdio 通信 |
| `src/registry/` | SQLite Registry：schema 迁移、实体/关系、调用图、死代码检测 |
| `src/repository/` | 仓库业务抽象，封装 registry 的 CRUD 与查询语义 |
| `src/search/` | Tantivy BM25 + SQL 向量混合检索编排 |
| `src/semantic_index/` | tree-sitter 多语言符号提取与调用图 |
| `src/vault/` | PARA 笔记系统：扫描、frontmatter、wikilink、backlinks、BFS 图遍历 |
| `src/skill_runtime/` | Skill 全生命周期：发现 → 解析 → 执行 → 评分 → 发布 |
| `src/workflow/` | YAML DAG 工作流引擎：模型、解析、验证、调度、执行、变量插值 |
| `src/knowledge_engine/` | README 摘要、关键词生成、模块信息探测 |
| `src/sync/` | 仓库同步编排：策略、任务、并发控制 |
| `src/storage.rs` | StorageBackend trait + AppContext：全项目依赖注入容器 |

### Workspace Crates（crates/，12 个）

| Crate | 职责 |
|-------|------|
| `devbase-core-types` | 零耦合底层类型：Node / Edge / NodeType |
| `devbase-registry` | Registry 核心逻辑 |
| `devbase-embedding` | 本地文本嵌入：Candle + Ollama 后端 |
| `devbase-vault-wikilink` | WikiLink 解析器 |
| `devbase-vault-frontmatter` | Vault YAML frontmatter 解析 |
| `devbase-skill-runtime-parser` | Skill 元数据解析 |
| `devbase-skill-runtime-types` | Skill 运行时类型 |
| `devbase-symbol-links` | 符号相似度链接 |
| `devbase-sync-protocol` | 版本向量目录同步协议 |
| `devbase-syncthing-client` | Syncthing 集成客户端 |
| `devbase-workflow-model` | Workflow 数据模型 |
| `devbase-workflow-interpolate` | Workflow 变量插值 |

---

## 3.3 核心架构模式

### 1. 三层架构（交互层 → 编译层 → 可靠层）
- **文件**：`.knowledge/architecture/three-layer-model.md`
- **解决的问题**：把 AI 接口、知识编译、物理存储解耦，使 TUI/MCP/CLI 可以独立演进，底层存储变更不影响上层协议。
- **体现**：`src/mcp/`、`src/tui/` 属于交互层；`src/registry/`、`src/search/`、`src/vault/`、`src/skill_runtime/` 属于编译层；SQLite/Tantivy/git2 属于可靠层。

### 2. 依赖注入 + AppContext（替代全局状态）
- **文件**：`src/storage.rs`、`AGENTS.md` G1/RF-1
- **解决的问题**：禁止 `dirs::data_local_dir()` / `std::env::var_os` 硬编码，使测试可注入 tempfile + StorageBackend，实现密封测试。
- **体现**：所有 IO 边界通过 AppContext 传入，`src/test_utils.rs` 提供 `temp_db()`。

### 3. Contract-First 协议设计（MCP）
- **文件**：`src/mcp/mod.rs` 中的 `McpTool` trait、`src/mcp/tools/mod.rs`
- **解决的问题**：AI Agent 与本地能力之间通过标准化 JSON-RPC 契约交互，新增工具不破坏现有 Agent 调用。
- **体现**：71 个工具均实现统一 `McpTool` trait，注册需同时更新 `McpToolEnum` 与路由。

### 4. 插件化语言支持
- **文件**：`src/semantic_index/`、`Cargo.toml` features
- **解决的问题**：通过 Cargo feature 按需启用 tree-sitter 语言 grammar，保持默认构建零 ML 运行时依赖。
- **体现**：`lang-rust` / `lang-python` / `lang-js-ts` / `lang-go` feature flags。

### 5. 事件驱动 TUI
- **文件**：`src/tui/event.rs`、`src/tui/state/`
- **解决的问题**：终端 UI 与后台扫描/同步任务解耦，避免阻塞渲染。
- **体现**：AsyncNotification + 状态机，render 层纯消费。

---

## 3.4 关键技术栈

| 类别 | 技术 | 备注 |
|------|------|------|
| 语言 | Rust 2024 Edition（rustc 1.95+） | — |
| CLI | clap derive | 子命令见 `src/commands/` |
| 异步运行时 | tokio | — |
| 终端 UI | ratatui + crossterm | 非 Web 的本地 TUI |
| 数据库 | rusqlite + r2d2（SQLite WAL） | 本地优先核心存储 |
| 全文检索 | tantivy | BM25 代码符号 + Vault 笔记 |
| 语义向量 | SQLite BLOB + 自定义 cosine_similarity UDF | 非大众选型：零 ML 运行时依赖 |
| 代码解析 | tree-sitter + 多语言 grammar | Rust/Python/TS/Go |
| Git 操作 | git2 | — |
| 协议 | MCP（Model Context Protocol）stdio | 体现深度：71 个工具实现 |
| 工作流 | YAML + 自定义 DAG 调度 | `src/workflow/` |
| 序列化 | serde/serde_json/serde_yaml/toml | — |
| 构建/测试 | Cargo workspace、cargo-nextest（待验证）、tempfile、assert_cmd | — |
| 架构治理 | 自定义 invariant checks（`scripts/invariant-checks/run-checks.ps1`） | 体现深度：CI 级架构红线 |

### 特别能体现深度的选型
- **零云端 + 零默认 ML 依赖**：用 `cosine_similarity` SQL UDF 替代向量数据库或云端 embedding 服务。
- **MCP stdio 协议**：不自己做 RPC，直接对接 Kimi/Claude/Cursor 的 MCP 生态。
- **Cargo workspace 拆分约束**：内部 `crate::` 引用超过 5 个禁止拆 crate，强制控制耦合。

---

## 3.5 解决过的 3 个最硬核技术问题

### 问题 1：如何把无序的本地工作空间编译成 AI 可推理的结构化上下文？
- **问题描述**：开发者本地有 Git 仓库、Markdown 笔记、Skill 脚本、工作流，格式各异，AI 无法直接"看见"并推理它们的关系。
- **方案**：设计"世界模型编译器"三层架构
  - **感知**：`src/scan.rs` + `src/semantic_index/`（tree-sitter）提取代码符号、调用图、模块边界
  - **编码**：`src/registry/` 统一实体模型（entities / relations / vault_notes 等）
  - **编译**：`src/knowledge_engine/` 生成 README 摘要、关键词；`src/search/hybrid.rs` 融合 BM25 + 向量检索
- **关键技术/算法**：tree-sitter 多语言解析、SQLite 关系模型、RRF 混合排序、BFS wikilink 图遍历（`src/vault/backlinks.rs`）
- **可量化结果**：支持 Rust/Python/TS/Go 代码解析；71 个 MCP 工具可供 AI 查询上下文（工具数来源：`src/mcp/mod.rs`）。

### 问题 2：如何在零云端依赖的前提下实现语义检索？
- **问题描述**：本地工具不能依赖 OpenAI/Pinecone 等云端 embedding 服务，但需要给 AI 提供"相似代码/笔记"能力。
- **方案**：本地 embedding + SQL 向量相似度
  - `devbase-embedding` crate 支持 Candle（all-MiniLM-L6-v2）和 Ollama 后端
  - 向量以 BLOB 存入 SQLite
  - 自定义 `cosine_similarity` UDF 在 SQL 层直接计算相似度（`src/registry/migrate.rs`）
- **关键技术/算法**：Candle 本地推理、SQLite UDF、余弦相似度、BLOB 序列化
- **可量化结果**：默认构建零 ML 运行时依赖；embedding feature 需显式启用。

### 问题 3：如何保证 71 个 MCP 工具在持续扩展时不破坏 Agent 契约？
- **问题描述**：MCP 工具数量从早期的 10+ 增长到 71，任何 schema 变更都可能让外部 Agent 调用失败。
- **方案**：Contract-First + 幂等 + 架构不变量
  - 所有工具实现统一 `McpTool` trait（`src/mcp/mod.rs`）
  - 状态变更工具强制幂等：`ON CONFLICT ... DO UPDATE`
  - Breaking change 只能通过新增 tool（如 `_v2`）实现，不可修改现有 schema
  - CI 通过 `scripts/invariant-checks/run-checks.ps1` 强制 T11（工具不得直接调用 `rusqlite::Connection`）等规则
- **关键技术/算法**：JSON Schema 自描述、幂等 upsert、CI 架构不变量检查
- **可量化结果**：71 个工具（来源：`src/mcp/mod.rs` `McpToolEnum`）；生产代码 unwrap/expect/panic 数量为 0。

---

## 3.6 性能/规模/稳定性相关数据

| 指标 | 数值 | 来源/状态 |
|------|------|----------|
| 项目版本 | v0.20.1 | `Cargo.toml` / `AGENTS.md` |
| Rust Edition | 2024（rustc 1.95+） | `Cargo.toml` |
| Workspace Crates | 12 | `crates/` 目录 |
| MCP Tools | 71 | `src/mcp/mod.rs` `McpToolEnum` |
| Registry Schema 版本 | v36 | `src/registry/migrate.rs` |
| 测试函数 | 616+ | `cargo test --workspace -- --list` |
| `src/main.rs` 行数 | 836 行 | `wc -l src/main.rs` |
| 生产代码 unwrap/expect/panic | 0 | 架构不变量 G5/RF-6 |
| CI 架构不变量检查 | 通过 | `scripts/invariant-checks/run-checks.ps1` |
| TUI 异步事件循环 | 支持 | `src/tui/event.rs` |
| SQLite WAL 模式 | 启用 | `src/registry/migrate.rs` |
| QPS / 并发请求量 | 待验证 | 项目为本地 CLI，无服务端指标 |
| 实际管理仓库数 | 待验证 | 取决于用户本地 workspace |
| 测试覆盖率 | 待验证 | 未配置 cargo-tarpaulin 等工具 |

---

## 3.7 简历专业化关键词

### 技术关键词
- Rust 2024 / Cargo Workspace
- MCP（Model Context Protocol）
- SQLite WAL / rusqlite
- Tantivy / BM25
- tree-sitter
- git2
- ratatui / crossterm
- tokio
- Candle / Ollama / Embedding
- YAML DAG / Workflow Engine
- PARA / Vault / Wikilink
- Actor-less Async / Event-driven TUI
- SQL UDF / cosine_similarity
- R2D2 / Connection Pool
- Feature Flags / Conditional Compilation

### 能力关键词
- 本地优先架构设计
- AI 上下文工程 / Context Compiler
- 三层架构 / 依赖注入
- Contract-First API 设计
- 架构不变量 / CI 治理
- 零信任安全边界 / 幂等设计
- 测试密封性 / Hermetic Testing
- 多语言代码解析
- 混合检索（BM25 + Vector）
- 图遍历 / Backlinks
- Multi-Agent 工具生态
- Schema 迁移与版本治理
- Workspace Crate 拆分
- 事件驱动 UI
- 异步编排 / Sync Orchestrator

---

## 3.8 适合写在简历上的 5 条 Bullet Point

1. 主导设计并实现本地优先的开发者工作空间"世界模型编译器"，通过 tree-sitter + SQLite + Tantivy 将代码库、PARA 笔记、Skill 与工作流编译为 AI 可推理的结构化上下文，并以 MCP 协议暴露 71 个 stdio 工具。
2. 在零云端依赖约束下实现语义检索能力：设计 SQLite BLOB + 自定义 cosine_similarity UDF 的向量搜索方案，配合 Candle/Ollama 本地 embedding 后端，使默认构建保持零 ML 运行时依赖。
3. 建立项目级架构治理体系：定义并落地 G1–G7/RF-1–RF-7 架构红线，通过 `scripts/invariant-checks/run-checks.ps1` 在 CI 强制依赖注入、测试密封性、零生产 panic 等规则，实现生产代码 unwrap/expect/panic 数量为 0。
4. 设计并实现 12 crate 的 Cargo Workspace 拆分策略，以 `devbase-core-types` 为无耦合根节点，严格控制 crate 间依赖方向，避免子 crate 反向耦合主库。
5. 实现事件驱动的 ratatui 终端仪表盘与 YAML DAG 工作流引擎，支持 5 种 step 类型、拓扑调度、变量插值和子工作流递归，CLI 入口 `src/main.rs` 控制在 836 行以内（RF-4 ≤ 1000 行约束）。

---

## 使用建议

- 如果你是项目核心/独立开发者，可以把每个项目第 5 部分的 3 个问题作为面试时的"最有成就感项目"展开。
- 第 8 条的 bullet points 可以直接贴到简历项目经历里。
- 需要针对某个具体岗位（如 Rust 后端、AI Infra、DevTools）进一步调整侧重点时，可基于本清单裁剪。
