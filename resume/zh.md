# 周景潇

**13626566112** · **2241470466@qq.com** · **github.com/juice094**
**AI 应用开发 / 后端开发 / 数据工程** · 上海/杭州/深圳 · 2026.07 可到岗

---

## 个人简介

大三在读，独立设计并维护三个生产级 Rust 系统（合计 47 个 workspace crate、27 万行代码、2,500+ 测试全通过）。从协议栈到 Agent 内核到编译器管线，均从零构建。具备独立闭环能力：发现问题 → 设计实验 → 实现系统 → 写论文。寻求 AI 基础设施 / 后端系统方向的实习机会。

---

## 教育背景

**甘肃农业大学** · 数据科学与大数据技术 · 工学学士（预计 2027.06）
信息科学技术学院 · 均分 83 / 核心课 86 · 专业前 10%

---

## 技能

**语言**：Rust（主力，3 年，3 个大型 Workspace 项目）、Python（研究，数据分析与实验脚本）

**系统**：tokio 异步运行时、TLS 1.3 / rustls、NAT 穿透（STUN/UPnP/Relay）、SQLite WAL、Protobuf（prost）

**AI / Agent**：MCP 协议（stdio/SSE/HTTP/WebSocket 四传输）、ReAct + Plan Agent 循环、BM25 + 向量混合检索、Multi-Agent 并行调度、本地 LLM 推理（Candle GGUF）

**工程**：Cargo Workspace 分层架构、Contract-First 设计、CI/CD 架构不变量检查、零 production panic 基线

---

## 研究经历

### RAG 系统中输出结构的实证研究（2026.06 — 至今）

独立完成，导师指导下推进。围绕检索增强生成中输出格式与内容质量的交互关系，构建了受控实验框架。

- 设计并执行多模型 × 多领域 × 多检索深度的受控实验（~40 条件，3000+ 样本），系统评估不同参数规模下输出结构的变化规律
- 提出行为层面的观测框架，将模型输出分解为格式维度与内容维度两个独立评分轴，通过统计检验度量二者的共变关系
- 跨四种模型架构验证了核心观测框架的普适性
- 主动识别实验中的测量 artifact，设计统一评分协议修正统计推断管道
- 论文撰写中（manuscript in progress）

---

## 项目经历

### Clarity — 本地优先 AI Agent 运行时
**Rust** · 22 活跃 workspace crates · 1,889 测试全通过 · 2026.04 - 至今

从零构建的本地 AI 运行时，单二进制编排 LLM、MCP 工具、记忆系统与多 Agent 协作，零 Python/Node.js/Ollama 外部依赖。

- **设计 Contract-First 分层架构**：contract 层零内部依赖，core/frontend 严格单向引用。新功能平均只改 1 层，编译时零循环引用
- **实现 ReAct + Plan 双模式 Agent 循环**：Plan Mode 将复杂多步任务的步骤遗漏率从约 40% 降到接近零，配套四层 Approval 审批链（Interactive/Smart/Plan/Yolo）
- **构建混合记忆系统**：SQLite + BM25 + 向量搜索 + 四级压缩归档。支持长期记忆持久化与上下文窗口溢出防护
- **落地跨前端 SPMC 事件总线**：设计 WireMessage/ViewCommand 统一协议，使 egui 桌面端、ratatui 终端、Axum Web IDE、无头 CLI、系统托盘、移动端 FFI 六入口共享同一 Agent 内核，各前端不互相 import
- **解决 Pretext 文字测量精度问题**：为 egui 聊天界面实现 Pretext 后端，1000 条消息渲染高度偏差降至 1.45%，estimate/render 双阶段测量耗时分别 74µs 和 136µs/msg
- **工程基线**：1554 lib + 275 bin + 34 doc + 26 集成测试全通过，Clippy 零 warning，生产代码零 unwrap/expect

### syncthing-rust — P2P 文件同步引擎
**Rust** · 13 workspace crates · 58,848 行 · 392 测试通过 · 2026.04 - 至今

Go Syncthing 的 Rust 重实现，BEP 协议 wire 级兼容。支持跨平台 P2P 文件同步，单二进制 ~13MB。

- **实现 BEP 协议栈**：基于 prost + rustls + ed25519-dalek，完整还原 BEP over TLS 消息格式、LZ4 压缩帧与握手语义。配套 wire_compat 集成测试验证与 Go Syncthing 的跨语言互操作
- **构建多路径 NAT 穿透**：UDP 广播 + HTTPS mTLS Global Discovery + STUN + UPnP + Relay v1，覆盖 LAN/公网/中继三种网络环境
- **解决 Windows 文件共享冲突**：针对反病毒/编辑器文件锁定，实现指数退避重命名回退 + 三路文本合并冲突解决 + Simple/Staggered 版本归档
- **实现预测性健康检查与自适应并发**：通过事件流评估失败率与状态翻转趋势，FolderOrchestrator 动态调整扫描/拉取并发。变更检测延迟约 1 秒
- **工程基线**：392 passed / 6 ignored / 0 failed，Clippy 零 warning，单静态二进制 ~13MB

### devbase — 开发者工作空间世界模型编译器
**Rust** · 12 workspace crates · 71 MCP 工具 · 616+ 测试 · 2026.04 - 至今

将本地 Git 仓库、PARA 笔记、Skill 脚本与 YAML 工作流编译为 AI 可推理的结构化上下文。

- **设计三层编译架构**：感知层（tree-sitter 多语言代码解析 + Git 历史分析）→ 编码层（SQLite Registry 统一实体-关系模型）→ 编译层（知识引擎生成摘要与关键词），以 MCP 协议暴露 71 个 stdio 工具
- **零云端依赖实现语义检索**：设计 SQLite BLOB + 自定义 cosine_similarity UDF 替代外部向量数据库，配合 Candle/Ollama 本地 embedding 后端，默认构建零 ML 运行时依赖
- **建立架构治理体系**：定义 G1-G7 / RF-1-RF-7 架构红线，CI 强制依赖注入、测试密封性与零 production panic。生产代码 unwrap/expect/panic 数量为 0
- **工程约束**：CLI 入口 src/main.rs 控制在 836 行，内部 crate:: 引用超过 5 个禁止拆 crate

---

## 语言与认证

- 日语专业四级（72 分）
- AI 应用工程师（中级）— 工业和信息化部认证
