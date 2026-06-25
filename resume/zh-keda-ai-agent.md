# 周景潇

**13626566112** · **2241470466@qq.com** · **[github.com/juice094](https://github.com/juice094)**
**AI 应用开发 / 后端开发 / 智能体平台研发** · 北京/上海/杭州/深圳 · 2026.07 可到岗 · 可实习 3-6 个月，每周 5 天

---

## 教育背景

**甘肃农业大学** · 数据科学与大数据技术 · 工学学士（预计 2027.06）
信息科学技术学院 · 均分 83 / 核心课 86 · 专业前 10%

---

## 技能

- **语言**：Rust（主力）、Python（熟练，学校授课 + 项目脚本）、Java（熟悉，学校授课）、TypeScript/Vue（课程）、Go（阅读级）
- **系统**：tokio 异步、TLS 1.3、UDP/TCP、NAT 穿透、SQLite WAL
- **AI / Agent**：MCP 协议（stdio/SSE/WebSocket）、ReAct+Plan Agent、RAG、BM25+向量搜索
- **工程**：62-crate workspace 管理、TDD、CI/CD、OpLog 审计

---

## 研究经历

### RAG 系统中输出结构的实证研究（2026.06 — 至今）

**独立完成。** 多模型 × 多架构 × 多领域的受控实验设计。

- 设计并执行大规模受控实验，系统评估检索增强生成（RAG）中输出格式与内容质量的交互
- 提出行为层面的观测框架，发现并验证跨架构的一致行为模式
- 主动识别实验中的测量 artifact，修正统计推断流程
- 研究成果直接指导 clarity / devbase 中 RAG 系统的设计与调优
- 论文撰写中（manuscript in progress）

---

## 项目经历

### Clarity — AI Agent 运行时
**Rust** · 25 crates · 1,243 tests · 152K LOC · [github.com/juice094/clarity](https://github.com/juice094/clarity) · 2026.04 - 至今

本地优先的 AI Agent 运行时，单二进制编排 LLM、MCP 工具、记忆系统。

- 设计和实现基于 LLM 的智能体核心架构：ReAct + Plan 双模式 Agent、任务规划与 Approval 四层审批链；Contract/Core/Frontend 三层解耦，Plan Mode 将步骤遗漏从 ~40% 降到接近 0
- 开发并优化 RAG 与记忆管理系统：BM25/向量混合检索 + 四级压缩归档 + SQLite WAL，支撑长期记忆与垂直领域上下文理解
- 实现 Multi-Agent 工具生态：MCP 三传输（stdio/SSE/WebSocket）+ 内置工具库 + 子代理并行调度，构建可扩展的智能体平台
- 5 种 UI 后端（TUI/egui/Slint/Tauri/headless），移动端 FFI 绑定；单二进制零 Python/Node.js/Ollama 外部依赖

### devbase — 开发者工作空间编译器
**Rust** · 12 crates · 71 MCP 工具 · 56K LOC · [github.com/juice094/devbase](https://github.com/juice094/devbase) · 2026.04 - 至今

代码上下文 + 知识记忆 + Agent 推理的统一编译器。

- 实现 RAG 检索与记忆系统：tree-sitter 多语言解析 + Tantivy BM25 全文检索 + 自定义 SQL cosine_similarity UDF 向量搜索，去外部向量 DB，部署步骤 4→1
- 以 MCP 协议暴露 71 个 stdio 工具，支持外部 AI Agent 查询代码库、知识笔记与工作流
- SQLite WAL + OpLog 审计，预编译二进制 ~8.7MB

### syncthing-rust — P2P 文件同步引擎
**Rust** · 8 crates · 5 binaries · 59K LOC · [github.com/juice094/syncthing-rust](https://github.com/juice094/syncthing-rust) · 2026.04 - 至今

Go Syncthing 的 Rust 重实现，BEP 协议 wire 级兼容。

- prost 协议编解码 + TLS 1.3 + TCP/UDP 传输层
- LAN/Global 发现：UDP 广播 + HTTPS + STUN + UPnP + Relay v1
- Block 级增量同步，Tailscale 集成跨 NAT 可复现

---

## 语言与认证

- 日语专业四级（72 分）
- AI 应用工程师（中级）— 工业和信息化部认证
