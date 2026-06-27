# 个人简历（科大讯飞 AI Agent 开发岗 · 针对性版本）

> **注意**：本文件针对"科大讯飞 AI Agent 开发"岗位定制。请将 `[ ]` 中的占位信息替换为真实内容后使用。

---

## 基本信息

- **姓名**：周景潇
- **电话**：13626566112
- **邮箱**：2241470466@qq.com
- **GitHub**：github.com/juice094
- **学校**：甘肃农业大学 · 数据科学与大数据技术 · 预计 2027.06
- **求职意向**：AI Agent 开发 / 智能体平台研发

---

## 个人简介

数据科学专业大三在读，**Rust 主力（3年）**、**Python 熟练**、**Java 熟悉**。2025.11-2026.06 独立设计并实现 **22-crate 本地 AI Agent 运行时**（1,889 测试全通过，零 Clippy 警告），深度覆盖 LLM 智能体核心架构、RAG 混合检索系统、四级记忆压缩、MCP 协议四传输实现（stdio/SSE/HTTP/WebSocket）、Multi-Agent 并行调度与后端服务开发。熟悉 ReAct / Plan 双模式 Agent 循环、BM25 + 向量混合检索（RRF 融合）、四层审批链与事件驱动架构。MCP 协议是国内最早的系统性实践者之一。具备将底层 Agent 架构设计能力迁移到 Python/Java 业务栈的工程基础。

---

## 技能

- **编程语言**：Rust（主力，3年，44+ workspace crate 经验）、Python（熟练，数据分析/实验脚本）、Java/Go/TypeScript（熟悉）
- **AI Agent 核心**：ReAct / Plan 双模式循环、任务规划与分解、对话状态管理、意图识别、流程工程、MCP 协议（stdio/SSE/HTTP/WebSocket 四传输全实现）、Multi-Agent 并行调度与 Handoff
- **RAG / 记忆系统**：BM25 + 向量混合检索（RRF 融合）、四级压缩归档（今天/本周/长期/事实）、SQLite FTS5 + 自定义 cosine_similarity UDF、Candle GGUF 本地 Embedding、零外部向量数据库依赖
- **后端 / 工程**：tokio 异步运行时、Axum REST API、WebSocket、SPMC 事件总线、CI/CD（GitHub Actions 12-job 矩阵）、零 unwrap/expect/panic 工程基线、Contract-First 架构设计
- **LLM Provider 生态**：OpenAI / Anthropic / DeepSeek / Kimi / Ollama / Candle GGUF 六种 Provider 集成，Provider 网格负载均衡与熔断，OAuth Device Flow 认证

---

## 项目经历

### Clarity — Rust 原生本地优先 AI 运行时

> 独立项目 · 22 workspace crates · ~150K 行 Rust · 与岗位 6 项职责高度匹配

- **设计和实现基于 LLM 的智能体核心架构**：基于 ReAct / Plan 双循环实现 Agent 内核，支持任务规划、对话管理、工具调用与 Approval 四层审批机制，覆盖"意图识别 → 推理 → 行动 → 反馈"完整流程工程。
- **开发并优化 RAG 与记忆管理系统**：构建 SQLite + BM25 + 向量搜索 + 四级压缩归档的混合记忆系统，提升本地模型在垂直领域的上下文理解与长期记忆能力。
- **实现 Multi-Agent 协作与工具生态**：设计 `clarity-subagents` 子代理并行调度器，集成 MCP 协议客户端（stdio / SSE / HTTP / WebSocket），构建可扩展的智能体工具平台。
- **参与后端服务开发与性能优化**：基于 Axum 实现 Gateway WebSocket / REST 服务，通过 SPMC 事件总线解耦 UI 与 Agent 核心，支撑多前端流式响应与高并发消息处理。
- **建立工程基线**：维护 1,889 测试全通过（1,554 lib + 275 bin + 34 doc + 26 集成），`cargo clippy -D warnings` 零 warning，单二进制即可运行。12-job CI 全绿（ubuntu/windows/macos）。

### Devbase — 本地开发者工作空间 AI 上下文引擎

> 独立项目 · 12 workspace crates + 主 crate · Rust

- **构建 AI 可推理的结构化上下文系统**：通过 tree-sitter 多语言解析 + SQLite + Tantivy 将代码库、PARA 笔记、Skill 脚本与 YAML 工作流编译为结构化上下文，以 MCP 协议暴露 **71 个 stdio 工具**（5 stable + 58 beta + 8 experimental），服务本地 AI Agent 推理。
- **在零云端依赖下实现语义检索**：设计 SQLite BLOB + 自定义 `cosine_similarity` UDF 的向量搜索方案，配合 Candle / Ollama 本地 embedding 后端，保持默认构建零 ML 运行时依赖。混合 RRF 融合 BM25 关键词 + 向量语义排序。

### Syncthing-Rust — P2P 文件同步守护进程

> 独立项目 · 13 workspace crates · ~58K 行 Rust

- **后端服务开发与稳定性优化**：实现 Axum REST API、事件总线与配置热重载；通过预测性健康检查与自适应并发控制，动态调整扫描 / 拉取任务，提升高负载下的系统稳定性。
- **协议互操作性实现**：基于 prost + rustls + ed25519-dalek 完成 BEP over TLS 协议栈，配套跨语言 `wire_compat` 测试验证与 Go Syncthing 的线路兼容。

---

## 教育背景

- **甘肃农业大学** · 数据科学与大数据技术 · 本科 · 预计 2027.06
- **相关课程**：数据结构(90)、大数据挖掘与应用(97)、数据存储与处理技术(96)、数据库原理(86)、操作系统(87)、人工智能导论(86.5)
- **证书**：AI 应用工程师（中级）— 工业和信息化部认证

---

## 其他

- **语言**：普通话（母语）、日语专业四级（72 分）
- **GitHub**：github.com/juice094
