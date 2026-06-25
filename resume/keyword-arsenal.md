# 简历关键词库

> **用途**：整合 clarity / syncthing-rust / devbase 三个项目的简历素材，作为写简历时的弹药库。
> **原始素材**：
> - clarity：`C:/Users/22414/dev/clarity/docs/development/resume-assets.md`
> - syncthing-rust + devbase：`C:/Users/22414/Desktop/新建 文本文档 (6).txt`

---

## 1. 项目总览

| 项目 | 定位 | 代码规模 | 核心架构 | 最有区分度的技术点 |
|---|---|---|---|---|
| **clarity** | Rust 原生本地优先个人 AI 运行时 | 22 crates, ~150K 行 | Contract-First 分层 + SPMC 事件总线 + 多前端共享内核 | Candle GGUF 本地推理、BM25+向量混合记忆、UniFFI 移动端 FFI |
| **syncthing-rust** | Syncthing BEP 协议 Rust 重写，P2P 文件同步守护进程 | 13 crates, ~58K 行 | Workspace 分层 + Trait-Based 抽象 + 事件驱动 | BEP 协议互操作、rustls + ed25519 设备证书、预测性健康检查 |
| **devbase** | 本地优先开发者工作空间"世界模型编译器" | 12 workspace crates + 主 crate | 三层架构 + 依赖注入 + MCP Contract-First | tree-sitter 多语言解析、SQLite + Tantivy 混合检索、71 个 MCP 工具 |

---

## 2. 合并技术关键词

按使用场景分组，写简历时根据目标岗位挑选 5-10 个嵌入。

### 语言 / 运行时
Rust 2024 / Rust 2021 · tokio · async/await · Cargo Workspace · Feature Flags

### 存储 / 数据库
SQLite (WAL) · rusqlite · sled · Tantivy · BM25 · 向量搜索 · BLOB 序列化 · R2D2 · Connection Pool

### 网络 / 协议
Axum · tower-http · WebSocket · SSE · REST API · JSON-RPC · MCP (Model Context Protocol) · BEP 协议 · TLS 1.3 / rustls · ed25519 · STUN · UPnP · Relay · NAT 穿透 · P2P 文件同步

### AI / LLM / Agent
Candle · GGUF · ReAct / Plan Agent 循环 · Approval 四层机制 · Multi-Agent 调度 · 子代理并行 · RAG · 混合检索 (BM25 + Vector) · 四级压缩归档 · Embedding · Ollama

### 前端 / UI
egui / eframe · ratatui · crossterm · Slint · TUI · Win32 API · 系统托盘 · UniFFI · 移动端 FFI

### 安全 / 加密
ChaCha20-Poly1305 · rustls · ed25519-dalek · 设备证书派生 · 本地 Secret 加密 · OAuth Device Flow

### 代码解析 / 工程智能
tree-sitter · 多语言符号提取 · 调用图 · PARA / Vault · Wikilink · BFS 图遍历 · YAML DAG · Workflow Engine

### 工程实践 / DevOps
GitHub Actions · CI/CD 矩阵 · cargo-deny · cargo-audit · Clippy 零 warning · 集成测试 · 回归测试 · 性能基准 · 架构不变量 · Hermetic Testing · 单二进制分发

---

## 3. 合并能力关键词

| 维度 | 关键词 |
|---|---|
| 架构设计 | Contract-First · 严格分层架构 · 事件驱动架构 · 多前端共享内核 · 插件化工具生态 · 依赖注入 · Trait-Based 抽象 · 依赖倒置 |
| 分布式 / 网络 | P2P 协议实现 · NAT 穿透与多路径发现 · 跨平台文件系统抽象 · 设备身份与 TLS 互操作 · 预测性健康检查 · 自适应并发控制 |
| AI Infra | 本地优先 AI 运行时 · 零外部依赖 · 混合记忆系统 · RAG · Multi-Agent 调度 · MCP 协议集成 · Provider Failover |
| 工程治理 | 架构不变量 · CI 红线 · 零生产 panic · 零 warning 基线 · 测试密封性 · 代码量 / 测试基线管理 |
| 性能 / 稳定性 | 异步并发调度 · 背压控制 · 事件流趋势分析 · 自适应节流 · 性能基准测试 · 回归测试 · 单二进制分发 |

---

## 4. 精选简历 Bullet Points

以下每条都可独立放入简历。建议每个项目选 2-3 条，按目标岗位调整顺序。

### clarity（AI 运行时 / AI Infra / Rust 系统）
1. **主导 Rust 原生本地优先 AI 运行时架构设计**，用 22 个 workspace crate 实现 TUI/桌面 GUI/Web IDE/CLI/系统托盘/移动端 FFI 六入口共享同一 Agent 内核，`cargo install` 即可运行，零 Python/Node.js/Ollama 外部依赖。
2. **实现混合记忆系统与本地 LLM 推理栈**，整合 SQLite + BM25 + 向量搜索 + 四级压缩归档，接入 Candle GGUF 本地推理；配套 `enc2:` 加密 Secret 与 `ReliableProvider` 链式 failover。
3. **落地跨前端 SPMC 事件总线协议**，设计 `WireMessage`/`ViewCommand` 统一 UI ↔ Agent 通信，使 egui/ratatui/Axum 等前端不互相 import、不重复实现业务逻辑，支撑流式响应与状态回放。
4. **统一 Claw/OpenClaw 协议边界**，决策 Gateway WebSocket 为内部唯一协议、OpenClaw JSON-RPC 为外部 fallback，由 `ClawConnectionManager` 自动检测 dialect，消除 UI 层协议泄漏。
5. **建立零 warning、零失败工程基线**：推动 `cargo clippy -D warnings` 全绿，维护 1,554+ lib / 275 bin / 34 doc / 26 集成测试全通过；引入 Pretext 文字测量使 1000 条消息渲染高度偏差降至 1.45%。

### syncthing-rust（P2P / 分布式 / 网络协议）
1. **独立设计并实现 13-crate Rust Workspace 架构**，将 BEP 协议、网络传输、同步状态机、嵌入式存储、REST API 按职责分层，通过 `syncthing-core` trait 层实现库间解耦，支撑 58,848 行代码的可持续演进。
2. **完成 BEP over TLS 协议栈的 Rust 实现**，基于 prost + rustls + ed25519-dalek 实现与 Go Syncthing 的线路兼容，配套 `wire_compat` 集成测试验证跨语言互操作。
3. **构建高可靠文件同步链路**：针对 Windows 句柄共享冲突实现指数退避重命名回退，设计三路文本合并与 Simple/Staggered 版本归档策略，解决双向同步中的并发冲突与数据丢失风险。
4. **实现预测性健康检查与自适应并发机制**：通过事件流评估失败率、watcher 丢事件和状态翻转趋势，由 FolderOrchestrator 与 Puller 动态调整扫描/拉取并发，提升高负载下的稳定性。
5. **主导生产级工程实践**：`cargo test --workspace` 基线 392 passed / 0 failed，Clippy 0 warnings，release 单二进制约 13 MB，并建立 72h 耐久压测与多云 CI/CD 矩阵。

### devbase（DevTools / AI 上下文工程 / 知识管理）
1. **主导设计并实现本地优先的开发者工作空间"世界模型编译器"**，通过 tree-sitter + SQLite + Tantivy 将代码库、PARA 笔记、Skill 与工作流编译为 AI 可推理的结构化上下文，并以 MCP 协议暴露 71 个 stdio 工具。
2. **在零云端依赖约束下实现语义检索能力**：设计 SQLite BLOB + 自定义 `cosine_similarity` UDF 的向量搜索方案，配合 Candle/Ollama 本地 embedding 后端，使默认构建保持零 ML 运行时依赖。
3. **建立项目级架构治理体系**：定义并落地 G1–G7/RF-1–RF-7 架构红线，通过 `scripts/invariant-checks/run-checks.ps1` 在 CI 强制依赖注入、测试密封性、零生产 panic 等规则，实现生产代码 `unwrap/expect/panic` 数量为 0。
4. **设计并实现 12 crate 的 Cargo Workspace 拆分策略**，以 `devbase-core-types` 为无耦合根节点，严格控制 crate 间依赖方向，避免子 crate 反向耦合主库。
5. **实现事件驱动的 ratatui 终端仪表盘与 YAML DAG 工作流引擎**，支持 5 种 step 类型、拓扑调度、变量插值和子工作流递归，CLI 入口 `src/main.rs` 控制在 836 行以内。

---

## 5. 按岗位类型的关键词组合建议

| 目标岗位 | 推荐关键词组合 | 建议重点展开的项目 |
|---|---|---|
| Rust 后端 / 系统开发 | tokio · async/await · Axum · REST API · SQLite · CI/CD · 零 warning 基线 | syncthing-rust / devbase |
| AI Infra / LLM 平台 | Candle · GGUF · MCP · ReAct/Plan · RAG · BM25+向量 · Multi-Agent · Provider Failover | clarity |
| DevTools / 开发者体验 | MCP · tree-sitter · Tantivy · YAML DAG · 世界模型编译器 · 71 个 MCP 工具 | devbase |
| 分布式 / P2P / 网络协议 | BEP · rustls · ed25519 · NAT 穿透 · 预测性健康检查 · 自适应并发 | syncthing-rust |
| 全栈 / 多前端 | egui · ratatui · Axum · WebSocket · SPMC · 多前端共享内核 | clarity |

---

## 6. 待验证 / 待补充数据

以下数据若写入简历，需先核实或避免绝对化表述。

- [ ] clarity 实际生产运行中的请求量、并发数、QPS（本地运行时，通常无服务端指标）。
- [ ] clarity 精确 Rust 源文件数量（约 200+）。
- [ ] syncthing-rust 72h 耐久压测完成度（v3.1.0 准入线，尚未完成）。
- [ ] syncthing-rust 测试覆盖率百分比（未配置 cargo-tarpaulin）。
- [ ] devbase 实际管理仓库数 / QPS / 并发请求量（本地 CLI，无服务端指标）。
- [ ] devbase 测试覆盖率百分比（未配置 cargo-tarpaulin）。

---

## 7. 使用建议

1. **不要直接复制所有 bullet points**。一页简历通常只能容纳 3-4 个项目经历，每个项目 2-3 条，优先选与目标岗位 JD 最匹配的内容。
2. **嵌入关键词时自然一点**。不要罗列技术名词，而是让关键词出现在"动词 + 方案 + 成果"的句式里。
3. **量化优先**。已核实的数据直接写；待验证的数据用"约"、"基线"、"目标"等词弱化，或面试时补充说明。
4. **下一步**：把目标岗位 JD 贴给 `resume-craft` skill，让它基于本关键词库帮你生成 ATS 友好的最终简历。
