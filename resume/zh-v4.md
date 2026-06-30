# 周景潇

**数据科学与大数据技术 · 大三在读 · 本科 2027 届** · 上海 / 北京 / 深圳 / 杭州 / 成都

📞 13626566112 · 📧 2241470466@qq.com · 🔗 github.com/juice094

**求职意向**：AI Agent 开发 / 后端系统开发 / 智能体平台研发

---
## 教育背景

**甘肃农业大学** · 数据科学与大数据技术 · 工学学士 · 2023.09 — 2027.06
- 信息科学技术学院 · 均分 83 / 核心课 86 · 专业前 10%
- 主修课程：数据结构与算法、操作系统、计算机网络、数据库原理、分布式系统、机器学习

---
## 个人简介

独立用 Rust 从零构建过三个系统级项目：一个跨设备保持一致的 AI Agent、一个无需云盘的 P2P 文件同步工具、一个把代码和笔记编译成 AI 可理解上下文的开发者知识库。熟悉异步服务、嵌入式存储、网络协议和跨平台 UI，工程上追求零警告、零 panic、可单二进制分发。

---
## 技术能力

我主要用 **Rust** 写系统级软件，也常用 **Python** 做数据分析、测试脚本和实验验证。

在项目中实际用过这些技术：
- **异步与网络**：Tokio、Axum、Tower、reqwest、WebSocket、rustls
- **存储与检索**：SQLite、rusqlite、Tantivy、BM25、embedding 向量搜索
- **AI Agent**：ReAct / Plan 双模式、MCP 协议、Multi-Agent 编排、RAG 检索增强
- **分布式与 P2P**：BEP 协议、STUN、UPnP、Relay、NAT 穿透
- **跨平台 UI**：egui、ratatui、UniFFI
- **安全**：ChaCha20-Poly1305、TLS 1.3、自签名设备证书
- **工程化**：Cargo Workspace、GitHub Actions、Clippy、tracing、criterion
---
## 技能栈

1. 熟练使用 Rust 进行生产级系统开发，独立完成 3 个 Rust 项目，核心代码约 6 万行。
2. 熟练运用 Tokio 异步生态，构建高并发 Agent loop、后台任务调度与多设备状态管理。
3. 熟悉 ReAct 与 Plan 双模式 Agent 架构，在 Clarity 中自研 Agent loop，降低长任务步骤遗漏率。
4. 熟悉 MCP 协议，实现 stdio / SSE / WebSocket 三传输工具调用与发现机制。
5. 熟悉 Multi-Agent 协作，设计子 Agent 并行编排与注册表机制。
6. 熟悉 RAG 检索增强生成，实现 BM25 + embedding 混合检索与 SQLite 内 cosine_similarity UDF。
7. 熟练使用 SQLite + rusqlite 实现零外部依赖的嵌入式数据持久化。
8. 熟练使用 Axum + Tower 构建 HTTP / WebSocket 服务与 REST API。
9. 熟悉使用 reqwest + tokio-tungstenite 实现安全 HTTP 客户端与 WebSocket 连接。
10. 熟悉 ChaCha20-Poly1305 静态加密与本地密钥安全管理。
11. 熟悉 P2P 文件同步与 NAT 穿透（STUN / UPnP / Relay），纯 Rust 实现 BEP 协议编解码。
12. 熟悉使用 egui / ratatui 构建跨平台 UI，并通过 UniFFI 暴露 Rust 核心给移动端。

---
## 项目经历

### Clarity — 让 AI 助手跨设备保持一致人格的本地 Agent 系统

> github.com/juice094/clarity · 2026.04 - 至今

Clarity 是一个本地优先的 AI Agent 运行时。它让同一个 AI 身份在手机、电脑、服务器上都能保持一致的个性、记忆和社会关系，不需要把私人数据上传到云端。从团队协作视角，可被认为是个具有独特个性的数字员工，或作为可成长的团队智脑，受安全约束和访问权限的管理控制。

- **解决 AI 长任务"做着做着就漏步骤"的问题**：设计了 ReAct + Plan 双模式执行方式。简单任务快速响应，复杂任务先拆成检查点再执行，步骤遗漏率从约 40% 降到接近零。
- **让 AI 能安全调用本地工具**：实现了 MCP 工具协议，支持 stdio、SSE、WebSocket 三种连接方式。LLM 可以调用本地文件、搜索、shell 等能力，同时不绑定任何特定模型厂商。
- **把记忆存在本地，同时支持语义搜索**：用 SQLite 单文件存储长期记忆，手写向量相似度计算 UDF，结合 BM25 关键词检索，实现不依赖外部数据库的混合搜索。
- **一套核心，多入口共用**：桌面 GUI（egui）、终端 UI（ratatui）、后台服务（headless）、移动端 FFI（UniFFI）共享同一个 Agent 内核，避免重复开发。

**规模**：21 个 Rust crate 的 Workspace，约 15 万行代码，测试基线全绿，Clippy 零警告，生产代码零 unwrap/expect/panic。

---

### syncthing-rust — 无需云盘的 P2P 文件同步工具

> github.com/juice094/syncthing-rust · 2025.11 - 至今

这个项目是对官方 Go 版 Syncthing 的 Rust 重写。它让多台设备直接互联同步文件，不需要把文件上传到第三方云盘，也能在局域网、公网、甚至 NAT 后自动找到彼此。

- **保证和官方版本能互通**：从零实现了 Syncthing 的 BEP 协议，用 protobuf 做消息编解码，并写了 wire_compat 集成测试验证和 Go 版守护进程的线路格式兼容。
- **解决 NAT 后设备找不到彼此的问题**：集成了 UDP 本地广播、全球发现服务器、STUN 公网地址探测、UPnP 端口映射和 Relay 中继回退，覆盖从家庭局域网到企业防火墙的多种网络环境。
- **降低同步冲突导致的数据丢失风险**：实现了块级文件同步、Windows 句柄冲突退避、文本三路合并，以及 Simple / Staggered 两种版本归档策略。

**规模**：9 个 library crate + 5 个命令二进制，约 5.3 万行 Rust，413 个测试通过 / 0 失败，Windows release 单二进制约 16 MB。已在日本 VPS 与国内 Windows 桌面跨国组网运行。

---

### devbase — 把代码和笔记编译成 AI 能理解的上下文

> github.com/juice094/devbase · 2026.01 - 至今

devbase 是一个面向开发者的本地知识库。它把 Git 仓库、Markdown 笔记、Skill 脚本和 YAML 工作流统一解析成结构化上下文，让 AI 能基于真实项目做推理，而不是只依赖一段提示词。

- **让 AI 能调用整个开发工作空间的能力**：通过 MCP 协议暴露了 81 个 stdio 工具，覆盖代码符号检索、Git 分析、笔记搜索、工作流执行等场景。人类用终端仪表盘操作，AI 客户端通过 `devbase mcp` 调用。
- **不依赖云端向量数据库实现语义搜索**：用 Tantivy 做全文/符号索引，用 SQLite BLOB 存 embedding，手写 cosine_similarity 标量函数计算相似度，默认即可离线运行关键词检索。
- **支持多步骤任务编排**：实现了 YAML DAG 工作流引擎，支持 Skill、子工作流、并行、条件判断、循环 5 种步骤类型，可自动拓扑排序并持久化执行状态。

**规模**：12 个 workspace crate + 主 crate，约 5.9 万行 Rust，`src/main.rs` 控制在 836 行，生产代码 unwrap/expect/panic = 0。

---
## 研究经历

**检索增强生成中输出结构的实证研究** · 2026.03 — 至今 · [acr-select](https://github.com/juice094/acr-select)

围绕 RAG 系统中"输出格式如何影响内容质量"设计并执行了受控实验：40 个实验条件、3000+ 样本、跨 4 种模型架构验证。论文撰写中。

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
