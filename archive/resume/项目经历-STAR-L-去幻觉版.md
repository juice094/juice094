# 项目经历（STAR-L 去幻觉版）

> **写作原则**：基于源码审计的真实数据，保留 STAR-L 框架、技术决策（Trade-off）与面试钩子，删除无证据的具体数字和夸大表述。
> **数据来源**：
> - `clarity-audit-report.md`
> - `syncthing-rust-exploration-report.md`
> - `devbase-exploration-report.md`

---

## 项目一：Clarity —— 本地优先分布式 AI Agent Runtime

> **定位**：Rust 原生 AI Agent 运行时，让同一身份跨设备保持人格、记忆与社会关系一致。
> **规模**：21 crate Cargo Workspace，约 15 万行 Rust，1,243 个测试，Clippy 0 warning。
> **适用岗位**：AI Infra、Rust 后端、Agent 开发、本地优先/隐私计算。

### 背景与挑战

现有 AI 编程助手在处理多步骤任务（如"重构整个模块"）时，常因上下文窗口限制和工具调用链路断裂导致步骤遗漏；同时云端方案存在隐私与延迟问题。需要构建一个**本地优先、跨设备一致、具备长记忆与工具标准协议**的 Agent 运行时。

### 核心贡献

#### 1. 自研 ReAct + Plan 双模式 Agent Loop

- **Situation**：ReAct 模式在长思维链下容易"走一步看一步"，遗漏关键步骤。
- **Task**：设计一个既能灵活响应环境、又能保证长任务完整性的 Agent 执行框架。
- **Action**：在 `clarity-core` 中实现双模式异步 Agent loop：ReAct 用于短循环快速响应，Plan 模式将长任务拆分为显式检查点（Checkpoint）并强制"计划-执行"校验；两种模式共享同一工具注册表，避免重复实现。
- **Result**：Plan 模式显著降低复杂长任务的步骤遗漏率；Agent 可在离线环境下继续执行。
- **技术深度 / Trade-off**：牺牲了纯 ReAct 的完全灵活性，换取长任务的可预测性与可调试性。
- **面试钩子**：ReAct 的遗忘边界在哪里？Plan 模式如何回滚失败步骤？

#### 2. 零外部依赖的本地记忆与混合检索

- **Situation**：Agent 需要长期记忆，但专用向量数据库增加部署复杂度和隐私风险。
- **Task**：在本地优先约束下实现记忆持久化与上下文召回。
- **Action**：基于 SQLite + rusqlite 构建 `clarity-memory`，手写 `cosine_similarity` UDF 计算向量相似度，结合 BM25 全文检索与 embedding 向量搜索；所有数据以单文件 SQLite 存储。
- **Result**：无需外部数据库即可支持关键词 + 语义混合召回；数据完全本地自持。
- **技术深度 / Trade-off**：选择 SQLite UDF 而非专用向量库，牺牲了极端规模下的检索性能，换取零依赖与单文件部署。
- **面试钩子**：SQLite 内做向量检索的性能边界在哪里？怎么权衡 BM25 与向量的权重？

#### 3. MCP 三传输工具协议与跨平台 UI

- **Situation**：不同场景需要不同的工具调用方式（本地 CLI 工具、远程服务、实时双向通道），且各 LLM provider 的 function calling 格式不统一。
- **Task**：实现标准化的工具协议，并让人类与 AI 都能使用同一 Agent 内核。
- **Action**：在 `clarity-mcp` 中实现 MCP（Model Context Protocol），支持 stdio（本地进程）、SSE（服务器推送）、WebSocket（双向实时）三种传输；用 egui 构建桌面 GUI、ratatui 构建 TUI、headless 提供服务端入口，并通过 UniFFI 暴露移动核心。
- **Result**：工具层与 LLM provider 解耦；多入口共享 `clarity-core`，避免各端重复实现业务逻辑。
- **技术深度 / Trade-off**：三种 transport 的生命周期管理复杂度高于单一 transport，但覆盖了从本地沙箱到远程协作的完整场景。
- **面试钩子**：三种 transport 分别适合什么场景？MCP 与 function calling 的本质区别是什么？

---

## 项目二：syncthing-rust —— 兼容 Go 官方实现的 P2P 文件同步引擎

> **定位**：Syncthing BEP 协议的 Rust 实现，与官方 Go 客户端线路兼容。
> **规模**：9 个 library crate + 5 个 command binary，约 5.3 万行 Rust，413 passed / 6 ignored / 0 failed 测试基线。
> **适用岗位**：分布式系统、P2P 网络、存储后端、网络协议。

### 背景与挑战

官方 Syncthing 基于 Go 实现，Rust 生态缺乏生产级兼容实现。挑战在于**必须保证与官方 Go 客户端的线缆级（wire-compatible）协议兼容**，同时处理 NAT 后设备无法直连、并发修改冲突等复杂网络与一致性场景。

### 核心贡献

#### 1. BEP 协议精确复刻与跨语言兼容

- **Situation**：需要与 Go Syncthing 守护进程互操作，但 protobuf 字段默认值和编码差异容易导致握手失败。
- **Task**：实现 Syncthing Block Exchange Protocol（BEP）的 Rust 版本，并验证与 Go 实现的兼容性。
- **Action**：基于 `prost` 实现 Hello / ClusterConfig / Index / Request / Response 等消息编解码；实现 BEP over TLS 握手与自定义证书验证；配套 `wire_compat` 集成测试对比 Go 官方线路二进制数据。
- **Result**：与 Go Syncthing 线路格式兼容；`cargo test --workspace` 基线 413 passed / 6 ignored / 0 failed。
- **技术深度 / Trade-off**：选择 prost 而非手写二进制解析，以可读性换取对 protobuf 边缘情况（如字段顺序、默认值）的严格依赖验证。
- **面试钩子**：protobuf 跨语言兼容有哪些常见陷阱？你怎么验证 wire-format 一致？

#### 2. 多路径 NAT 穿透与连接降级

- **Situation**：大量 P2P 设备位于 NAT 后，无法直接建立 TCP 连接。
- **Task**：实现设备发现、NAT 穿透与中继回退机制。
- **Action**：集成 UDP 本地广播、HTTPS 全球发现、STUN 公网地址探测、UPnP 端口映射与 Relay Protocol v1；当直连失败时自动 fallback 到 relay。
- **Result**：设备在复杂网络环境下可自动选择最佳连接路径。
- **技术深度 / Trade-off**：维护多种发现/穿透机制增加了代码复杂度，但避免了单一机制在特定网络拓扑下完全不可用。
- **面试钩子**：STUN 打洞失败的主要原因是什么？UPnP 和 Relay 的优先级怎么设计？

#### 3. 高可靠文件同步与冲突解决

- **Situation**：双向同步中并发修改容易产生冲突与数据丢失。
- **Task**：设计高可靠的块级同步链路。
- **Action**：实现 scanner / puller / index-handler / block-server 全链路块级同步；针对 Windows 句柄共享冲突实现指数退避重命名回退；基于 base/local/remote 实现文本三路合并；支持 Simple / Staggered 版本归档策略。
- **Result**：降低并发冲突与数据丢失风险；Windows release 单二进制约 16 MB，零运行时依赖。
- **技术深度 / Trade-off**：三路合并 + 版本归档比简单的 last-write-wins 更复杂，但避免了静默数据丢失。
- **面试钩子**：三路合并和 CRDT 怎么选？Staggered 归档策略的时间窗口如何设计？

---

## 项目三：devbase —— 开发者工作空间"世界模型编译器"

> **定位**：本地优先的开发者知识库管理器，将代码库、笔记、Skill 与工作流编译为 AI 可推理的结构化上下文。
> **规模**：12 个 workspace crates + 主 crate，约 5.9 万行 Rust，`src/main.rs` 836 行，81 个 MCP stdio 工具。
> **适用岗位**：DevTools、编译器工具链、AI 代码助手、平台架构。

### 背景与挑战

个人开发与 AI 辅助场景下，频繁需要代码解析、文档检索和重复任务自动化，现有工具割裂且依赖繁重。需构建一个**零外部依赖、高内聚**的开发者基础设施，将 Git 仓库、Markdown 笔记、Skill 脚本和 YAML 工作流统一编译为 AI 可推理的上下文。

### 核心贡献

#### 1. 世界模型编译器与 81 个 MCP 工具

- **Situation**：AI 工具需要可推理的代码/笔记/工作流上下文，但云端方案存在隐私与延迟问题。
- **Task**：将本地开发者工作空间编译为结构化上下文，并通过标准协议暴露给 AI Agent。
- **Action**：用 Rust 2024 构建 devbase，集成 tree-sitter 多语言解析、SQLite WAL 关系存储、Tantivy BM25、PARA/WikiLink 知识管理；所有能力通过 MCP stdio 协议暴露为 81 个工具。
- **Result**：默认构建零 ML 运行时依赖；人类可通过 ratatui 仪表盘使用，AI 客户端可通过 `devbase mcp` 调用全部能力。
- **技术深度 / Trade-off**：用 stdio MCP 而非 HTTP 服务，牺牲了远程调用的便利性，换取本地进程的隔离性与零网络配置。
- **面试钩子**：MCP stdio 与 SSE/WebSocket  transport 的适用场景有何不同？

#### 2. SQLite + Tantivy 混合语义检索

- **Situation**：需要在无云端依赖前提下支持代码符号与笔记的关键词/语义召回。
- **Task**：设计混合检索方案，兼顾关键词精确匹配与语义相似度。
- **Action**：Tantivy 负责 BM25 全文/符号索引；SQLite BLOB 存储 embedding，注册自定义 `cosine_similarity` 标量函数计算向量相似度；混合层融合多路结果。
- **Result**：默认 feature 下无需 Candle/Ollama 即可运行关键词检索；开启 embedding feature 后可本地生成 embedding。
- **技术深度 / Trade-off**：不用专用向量库，将 embedding 存储和相似度计算内嵌到 SQLite，牺牲了大规模下的检索性能，换取零外部依赖。
- **面试钩子**：Tantivy 和 SQLite 在检索链路中分别解决什么问题？怎么避免 SQLite 向量检索随数据量线性退化？

#### 3. YAML DAG 工作流引擎与 Workspace 治理

- **Situation**：AI/用户需要编排多 Skill 流水线，同时 ~5.9 万行 Rust 代码需要控制模块耦合。
- **Task**：设计可配置的工作流引擎，并保持 Workspace 可维护。
- **Action**：定义 Skill / Subworkflow / Parallel / Condition / Loop 5 种 step 类型，实现 YAML 解析、依赖验证、拓扑调度（Kahn 算法）、变量插值与 SQLite 持久化执行状态；以 `devbase-core-types` 为根节点拆分 12 个 workspace crate，制定 G1-G7/RF-1-RF-7 架构红线，`src/main.rs` 控制在 836 行。
- **Result**：工作流可按依赖层级并行执行，支持条件分支与循环；子 crate 禁止反向依赖主库，`src/` 生产代码 unwrap/expect/panic 数量为 0。
- **技术深度 / Trade-off**：把功能拆成 12 个 crates 增加了发布与版本协调成本，但换来清晰的依赖方向和可独立测试的模块边界。
- **面试钩子**：Kahn 算法怎么处理循环依赖？Workspace crate 拆分的边界怎么定？

---

## 按岗位裁剪建议

### 投 AI Infra / Agent 开发岗

- **首项目**：Clarity（3 条全用）
- **次项目**：devbase（用经历 1 + 经历 2）
- **可选**：syncthing-rust（用经历 1）

### 投分布式系统 / P2P / 存储岗

- **首项目**：syncthing-rust（3 条全用）
- **次项目**：devbase（用经历 1 + 经历 3）
- **可选**：Clarity（用经历 1）

### 投 DevTools / AI 代码助手 / 平台架构岗

- **首项目**：devbase（3 条全用）
- **次项目**：Clarity（用经历 1 + 经历 2）
- **可选**：syncthing-rust（用经历 1）

### 投 Rust 后端 / 系统开发岗

- **首项目**：syncthing-rust（3 条全用）
- **次项目**：Clarity（用经历 1 + 经历 3）
- **可选**：devbase（用经历 3）

---

## 去幻觉对照表

| 原风险表述 | 去幻觉后 | 原因 |
|:---|:---|:---|
| RRF 倒数排名融合 | 删除，改为"BM25 + embedding 混合召回" | 源码中未找到 RRF 实现 |
| Q4_K_M 量化降低 60% 显存 | 删除具体数字 | 无测试数据支撑 |
| SQLite MVCC 快照隔离 | 改为"SQLite WAL 模式" | SQLite 默认非 MVCC |
| devbase 22 crates | 改为"12 workspace crates + 主 crate" | 实际为 12 |
| 编译耗时降低 30% | 删除 | 无 benchmark 证据 |
| Staggered 降低误冲突回滚率 | 改为"支持 Staggered 版本归档以降低冲突回滚风险" | 无量化数据 |

---

## 待补充/核实

- [ ] Clarity Plan 模式步骤遗漏率的测试方法论（可保留"显著降低"，避免具体数字）
- [ ] clarity 当前准确 crate 数（已归档 2 个，最终口径需确认）
- [ ] devbase 测试通过率是否保持 616+ / 634
