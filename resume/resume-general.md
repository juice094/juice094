# 个人简历

> **注意**：本文件为通用版简历模板。请将 `[ ]` 中的占位信息替换为真实内容后使用。

---

## 基本信息

- **姓名**：[你的姓名]
- **电话**：[你的手机号]
- **邮箱**：[你的邮箱]
- **GitHub**：[你的 GitHub 主页链接]
- **学校**：[学校名称] · [专业] · [预计毕业时间]
- **求职意向**：AI Agent 开发 / 后端开发 / 智能体平台研发

---

## 个人简介

计算机相关专业本科在读，**Python 熟练**、**Rust 主力**、**Java 熟悉**。在校期间系统学习过后端开发与软件工程课程，个人独立完成多个 Rust 系统级项目，最深度的实践是**独立设计并实现 22-crate 的本地 AI 运行时**，覆盖 LLM 编排、RAG 记忆系统、Multi-Agent 调度、多前端交互与本地安全存储。对智能体核心架构有从 0 到 1 的工程理解，具备将底层设计能力迁移到 Python/Java 业务栈的基础。

---

## 技能

- **编程语言**：Python（熟练）、Rust（主力）、Java（熟悉）
- **后端 / 系统**：tokio、Axum、REST API、WebSocket、SQLite、Git、Linux 基础
- **AI / Agent**：ReAct / Plan 循环、RAG、BM25、向量检索、MCP、Multi-Agent 调度、LLM Provider 抽象
- **工程实践**：Cargo Workspace、CI/CD、单元测试 / 集成测试、代码审查、零 warning 工程基线

---

## 项目经历

### Clarity — Rust 原生本地优先 AI 运行时

> 独立项目 · 22 workspace crates · ~150K 行 Rust

- **主导设计 22-crate 本地 AI 运行时架构**，实现 TUI / 桌面 GUI / Web IDE / 无头 CLI / 系统托盘 / 移动端 FFI 六入口共享同一 Agent 内核，默认零 Python / Node.js / Ollama 外部依赖。
- **实现智能体核心与记忆系统**：基于 ReAct / Plan 双循环设计 Agent 内核；构建 SQLite + BM25 + 向量搜索 + 四级压缩归档的混合记忆系统，支持长期记忆与上下文压缩。
- **落地跨前端 SPMC 事件总线协议**，设计 `WireMessage` / `ViewCommand` 统一 UI 与 Agent 核心通信，实现 egui / ratatui / Axum 多前端解耦与流式响应。
- **建立工程基线**：维护 1,554+ lib / 275 bin / 34 doc / 26 集成测试全通过，`cargo clippy -D warnings` 零 warning。

### Devbase — 本地开发者工作空间世界模型编译器

> 独立项目 · 12 workspace crates + 主 crate · Rust

- **主导设计本地优先的开发者上下文引擎**，通过 tree-sitter + SQLite + Tantivy 将代码库、PARA 笔记、Skill 脚本与 YAML 工作流编译为 AI 可推理的结构化上下文。
- **以 MCP 协议暴露 71 个 stdio 工具**，实现统一 `McpTool` trait 与幂等路由，支持外部 AI Agent 查询与调用本地能力。
- **在零云端依赖约束下实现语义检索**：设计 SQLite BLOB + 自定义 `cosine_similarity` UDF 的向量搜索方案，配合 Candle / Ollama 本地 embedding 后端，默认构建零 ML 运行时依赖。
- **建立项目级架构治理**：落地 G1–G7 / RF-1–RF-7 架构红线，通过 CI 强制依赖注入、测试密封性与零生产 panic，实现生产代码 `unwrap/expect/panic` 数量为 0。

### Syncthing-Rust — P2P 文件同步守护进程

> 独立项目 · 13 workspace crates · ~58K 行 Rust

- **独立设计 13-crate Workspace 架构**，将 BEP 协议、网络传输、同步状态机、嵌入式存储、REST API 按职责分层，通过 trait 层实现库间解耦。
- **完成 BEP over TLS 协议栈的 Rust 实现**，基于 prost + rustls + ed25519-dalek 实现与 Go Syncthing 的线路兼容，配套跨语言 `wire_compat` 集成测试。
- **实现高可靠文件同步链路**：针对 Windows 句柄共享冲突设计指数退避重命名回退，实现三路文本合并与 Simple / Staggered 版本归档策略。
- **实现预测性健康检查与自适应并发**：通过事件流评估失败率、watcher 丢事件与状态翻转趋势，动态调整扫描 / 拉取并发，提升高负载稳定性。

---

## 教育背景

- **[学校名称]** · [学院/专业] · [本科] · [入学时间] – [预计毕业时间]
- **相关课程**：Python 程序设计、Java 程序设计、数据结构、操作系统、计算机网络、数据库原理 [根据实际课表调整]
- **荣誉 / 证书**：[如有，可补充，例如奖学金、英语等级、竞赛奖项]

---

## 其他

- **语言**：普通话（母语）、英语 [CET-4/CET-6/托福/雅思 等]
- **个人博客 / 技术笔记**：[如有，可补充链接]
