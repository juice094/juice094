# 个人简历

---

## 基本信息

- **姓名**：周景潇
- **电话**：13626566112
- **邮箱**：2241470466@qq.com
- **GitHub**：[github.com/juice094](https://github.com/juice094)
- **学校**：甘肃农业大学 · 信息科学技术学院 · 数据科学与大数据技术 · 本科 · 预计 2027.06
- **求职意向**：AI Agent 开发 / 后端开发 / 智能体平台研发
- **意向城市**：上海 · 北京 · 深圳 · 杭州 · 成都

---

## 个人简介

数据科学专业本科在读，**Rust 主力（3 年）**、**Python 熟练**、**Java/Go/TypeScript 熟悉**。独立设计并维护三个生产级 Rust 系统（合计 44+ workspace crate、~20 万行有效代码、2,500+ 测试全通过）。最深度的实践是**独立设计 22-crate 本地 AI Agent 运行时**——覆盖 LLM 编排、ReAct/Plan 双模式 Agent 循环、MCP 协议四传输实现、BM25+向量混合检索记忆系统、四层审批链与多前端共享内核。对 AI Agent 核心架构有从 0 到 1 的工程理解，具备将底层系统设计能力迁移到多语言业务栈的基础。

---

## 技能

| 类别 | 具体技能 |
|------|---------|
| **编程语言** | Rust（主力，3年，44+ workspace crate 经验）、Python（熟练，数据分析/实验脚本）、Java/Go/TypeScript/SQL（熟悉） |
| **AI / Agent** | ReAct / Plan Agent 循环、MCP 协议（stdio/SSE/HTTP/WebSocket 四传输全实现）、RAG、BM25 + 向量混合检索、Multi-Agent 调度、LLM Provider 抽象与容灾、Candle GGUF 本地推理 |
| **后端 / 系统** | tokio 异步运行时、Axum REST API、WebSocket、SPMC 事件总线、CI/CD（GitHub Actions）、零 unwrap 工程基线 |
| **数据库 / 存储** | SQLite（WAL / FTS5 / 自定义 UDF）、PostgreSQL、Redis、Tantivy BM25、sled、向量相似度检索 |
| **网络 / 协议** | TCP/TLS 1.3（rustls）、Protobuf（prost）、BEP P2P 协议、NAT 穿透（STUN/UPnP/Relay）、ed25519 设备身份 |
| **前端** | egui/eframe 桌面 GUI、ratatui TUI、Vue 3、HTML/CSS |
| **工程实践** | Cargo Workspace 架构设计、Contract-First、依赖注入、测试密封性、架构守卫规则（CI 强制）、零 panic 生产代码 |

---

## 项目经历

### Clarity — Rust 原生本地优先 AI Agent 运行时

> 独立项目 · 22 workspace crate · ~150K 行 Rust · 1,889 测试全通过 · 零 Clippy 警告
> [github.com/juice094/clarity](https://github.com/juice094/clarity) · 2026.04 — 至今

- **主导设计 22-crate Contract-First 架构**：以 `clarity-contract`（零内部依赖）为契约根节点，实现 TUI / 桌面 GUI / Web IDE / 无头 CLI / 系统托盘 / 移动端 FFI 六入口共享同一 Agent 内核。新功能平均只改 1 层，编译时零循环引用。默认零 Python/Node.js/Ollama 外部依赖，`cargo install` 即可运行。
- **实现 ReAct + Plan 双模式 Agent 循环与四层审批链**：ReAct 适合探索性任务（边想边做），Plan 适合结构性任务（先规划后执行，步骤遗漏率从 ~40% 降至接近零）。审批链覆盖 Interactive/Smart/Plan/Yolo 四种信任级别，所有决策记录在 OpLog 中可审计。
- **构建混合记忆系统**：SQLite FTS5 + BM25 + 向量搜索（cosine_similarity UDF）+ 四级压缩归档（今天/本周/长期/事实）。零外部向量数据库依赖，RRF 算法融合关键词与语义检索结果。
- **落地跨前端 SPMC 事件总线**：设计 `WireMessage` / `ViewCommand` 统一 UI 与 Agent 核心通信，13 种 `RenderLine` 变体支持文本/代码/工具调用/Plan/流式内容等渲染。各前端不互相 import，通过 `clarity-wire` 解耦。
- **完整实现 MCP 协议四传输**（stdio / SSE / HTTP / WebSocket），集成 6+ LLM Provider（OpenAI/Anthropic/DeepSeek/Kimi/Ollama/Candle GGUF），支持 Provider 网格负载均衡与熔断。
- **工程基线**：1,889 测试全通过（1,554 lib + 275 bin + 34 doc + 26 集成），`cargo clippy -D warnings` 零 warning，生产代码零 unwrap/expect/panic。12-job CI 全绿（ubuntu/windows/macos）。

### Devbase — 本地开发者工作空间世界模型编译器

> 独立项目 · 12 workspace crate + 主 crate · 616+ 测试 · 零 Clippy 警告
> [github.com/juice094/devbase](https://github.com/juice094/devbase) · 2026.05 — 至今

- **主导设计"世界模型编译器"三层架构**：感知层（tree-sitter + Tantivy + git2）→ 知识层（SQLite 图 + 向量 + 关系）→ 策略层（同步编排 + 工作流 DAG）。将分散的 Git 仓库、PARA 笔记、Skill 脚本编译为 AI 可推理的结构化上下文。
- **以 MCP 协议暴露 71 个 stdio 工具**（5 stable + 58 beta + 8 experimental），实现统一 `McpTool` trait 与幂等路由，覆盖代码解析、Git 分析、语义检索、知识库查询、工作流执行。Stability 分级 + 晋升流程保证工具质量。
- **在零云端依赖下实现语义检索**：设计 SQLite BLOB + 自定义 `cosine_similarity` UDF 的向量搜索方案，配合 Candle/Ollama 本地 embedding 后端，默认构建零 ML 运行时依赖。混合 RRF 融合 BM25 关键词 + 向量语义排序。
- **建立架构治理体系**：定义并落地 G1-G7 / RF-1-RF-7 七条架构红线，CI 强制依赖注入、测试密封性、零生产 panic。实现生产代码 `unwrap/expect/panic` 数量为 0，每次 schema 迁移前自动 SQLite 备份。

### Syncthing-Rust — P2P 文件同步守护进程

> 独立项目 · 13 workspace crate · ~58K 行 Rust · 392 测试全通过 · 零 Clippy 警告
> [github.com/juice094/syncthing-rust](https://github.com/juice094/syncthing-rust) · 2025.11 — 至今

- **独立实现完整 BEP over TLS 协议栈**：基于 prost + rustls + ed25519-dalek 实现与 Go Syncthing v2.1.0 的线路兼容，配套跨语言 `wire_compat` 集成测试验证。Protobuf 编解码、LZ4 压缩帧、TLS 1.3 双向认证。
- **构建多路径 NAT 穿透与设备发现**：LAN UDP 广播 + Global HTTPS mTLS + STUN + UPnP + Relay v1 五种发现机制协同，ParallelDialer 并行尝试所有地址，首个成功连接获胜。覆盖 LAN/公网/中继三种网络环境。
- **实现高可靠同步链路**：SHA-256 块级扫描（rayon 并行）+ 自适应并发拉取（RTT 反馈控制）+ 三路文本合并（similar crate）+ Simple/Staggered 版本归档。Windows 句柄共享冲突场景下实现指数退避重命名回退，零文件损坏。
- **生产部署**：Windows 11 ↔ Ubuntu 24.04 双节点稳定运行，单静态二进制 ~13MB（零运行时依赖：无 OpenSSL/GC/Python）。CI 矩阵 19 jobs 全绿（ubuntu/windows/macos）。

---

## 研究经历

### 检索增强生成中输出结构的实证研究（2026.03 — 至今）

[github.com/juice094/acr-select](https://github.com/juice094/acr-select)

- 围绕 RAG 系统中输出格式与内容质量的交互关系，设计并执行受控实验框架。
- 设计 ~40 实验条件、3,000+ 样本的多因子受控实验；跨 7 模型 × 4 架构验证框架普适性。
- 主动发现测量 artifact 并设计统一评分协议修正统计推断，论文撰写中。

---

## 教育背景

- **甘肃农业大学** · 信息科学技术学院 · 数据科学与大数据技术 · 工学学士 · 2023.09 — 2027.06
- GPA：整体 83 / 核心课程 86 · 专业前 10%
- **核心课程**：数据结构(90)、大数据挖掘与应用(97)、数据存储与处理技术(96)、数据库原理(86)、操作系统(87)、人工智能导论(86.5)、算法设计与分析(81)
- **证书**：AI 应用工程师（中级）— 工业和信息化部认证

---

## 其他

- **语言能力**：普通话（母语）、英语（技术文档读写）、日语（专业四级 72 分）
- **GitHub**：[github.com/juice094](https://github.com/juice094)
- **驾驶**：C1 驾照
