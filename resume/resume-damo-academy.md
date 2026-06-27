# 个人简历（阿里达摩院 · AI Agent / 大模型基础设施方向）

> **投递建议**：阿里达摩院 —— AI 系统工程 / 大模型 Agent 基础设施 / 开源 LLM 生态方向
> 通义千问（Qwen）系列模型的开源生态、Agent 框架、推理部署优化等方向与候选人技术栈高度匹配

---

## 基本信息

- **姓名**：周景潇
- **电话**：13626566112
- **邮箱**：2241470466@qq.com
- **GitHub**：[github.com/juice094](https://github.com/juice094)
- **学校**：甘肃农业大学 · 信息科学技术学院 · 数据科学与大数据技术 · 本科 · 预计 2027.06
- **求职意向**：AI Agent 基础设施开发 / 大模型系统工程 / Agent 框架研发
- **意向城市**：杭州（优先）· 北京

---

## 个人简介

数据科学专业本科在读，**Rust 主力（3年）**、**Python 熟练**、**Java/Go 熟悉**。具备**研究+工程双闭环能力**：独立从实验设计走到系统实现再走到论文撰写，同时维护三个生产级 Rust 系统（合计 44+ workspace crate、2,500+ 测试全通过）。核心方向是 **AI Agent 基础设施**——独立设计并实现 22-crate 本地 AI Agent 运行时，深度覆盖 ReAct/Plan 双模式 Agent 循环、MCP 协议全传输实现、BM25+向量混合检索记忆系统、Candle GGUF 本地推理（已支持 Qwen2/Qwen2.5 系列）。同时独立完成一项 RAG 系统输出结构的实证研究（7 模型 × 4 架构 × 3,000+ 样本）。对将 Agent 架构从本地原型推向规模化部署有强烈的工程兴趣。

---

## 技能

| 类别 | 具体技能 |
|------|---------|
| **编程语言** | Rust（主力，3年，44+ workspace crate 架构经验）、Python（熟练，实验设计/数据分析）、Java/Go/TypeScript（熟悉） |
| **AI Agent 核心** | ReAct / Plan 双模式 Agent 循环、MCP 协议（stdio/SSE/HTTP/WebSocket 四传输全实现）、Multi-Agent 并行调度、四层审批链（Interactive/Smart/Plan/Yolo）、对话状态管理 |
| **LLM / 推理** | 6+ Provider 集成（OpenAI/Anthropic/DeepSeek/Kimi/Ollama/Candle GGUF）、**Qwen2/Qwen2.5 GGUF 本地推理**、Provider 网格负载均衡与熔断、Token 预算控制、流式响应处理 |
| **RAG / 检索** | BM25 + 向量混合检索（RRF 融合）、SQLite FTS5 + 自定义 cosine_similarity UDF、四级记忆压缩归档、Candle 本地 Embedding、PDF/md/txt 多格式文档解析 |
| **系统工程** | tokio 异步运行时、Axum REST API、SPMC 事件总线、TLS 1.3（rustls）、Protobuf（prost）、零 unwrap 工程基线、Contract-First 架构 |
| **数据库 / 存储** | SQLite（WAL / FTS5 / 自定义 UDF）、PostgreSQL、Redis、Tantivy BM25、sled |
| **工程实践** | Cargo Workspace 架构设计、CI/CD（GitHub Actions 12-job 矩阵）、测试密封性、架构守卫规则（CI 强制）、零 panic 生产代码、OpLog 审计 |
| **研究能力** | 实验设计与统计检验、多因子受控实验、LaTeX 学术写作、独立完成实证研究全流程 |

---

## 项目经历

### Clarity — Rust 原生本地优先 AI Agent 运行时（核心项目）

> 独立项目 · 22 workspace crate · ~150K 行 Rust · 1,889 测试全通过 · 零 Clippy 警告
> [github.com/juice094/clarity](https://github.com/juice094/clarity) · 2026.04 — 至今

- **主导设计 22-crate Contract-First Agent 运行时架构**：以 `clarity-contract`（零内部依赖）为契约根节点，实现 TUI / 桌面 GUI / Web IDE / 无头 CLI / 系统托盘 / 移动端 FFI 六入口共享同一 Agent 内核。新功能平均只改 1 层，编译时零循环引用。
- **实现 ReAct + Plan 双模式 Agent 循环**：ReAct 适合探索性任务（边推理边执行），Plan 适合结构性任务（先规划后验证，步骤遗漏率从 ~40% 降至接近零）。四层审批链覆盖 Interactive/Smart/Plan/Yolo 四种信任级别，所有工具调用决策可审计。
- **构建混合记忆系统**：SQLite FTS5 + BM25 关键词检索 + 向量语义搜索（cosine_similarity UDF）+ 四级压缩归档（今天/本周/长期/事实）。RRF 融合算法，零外部向量数据库依赖。
- **完整实现 MCP 协议四传输**（stdio/SSE/HTTP/WebSocket），集成 6+ LLM Provider 包括 **Candle GGUF 本地推理（支持 Qwen2/Qwen2.5/DeepSeek-R1-Distill）**，实现 Provider 网格负载均衡与熔断。SPMC 事件总线解耦多前端通信。
- **工程基线**：1,889 测试全通过，`cargo clippy -D warnings` 零 warning，生产代码零 unwrap/expect/panic，单二进制 `cargo install` 即可运行。12-job CI 全绿（ubuntu/windows/macos）。

### Devbase — 本地开发者工作空间世界模型编译器

> 独立项目 · 12 workspace crate + 主 crate · 71 MCP 工具 · 616+ 测试
> [github.com/juice094/devbase](https://github.com/juice094/devbase) · 2026.05 — 至今

- **主导设计"世界模型编译器"三层架构**：感知层（tree-sitter 多语言 AST 解析 + Tantivy BM25 索引 + git2 变更检测）→ 知识层（SQLite 图存储 + 向量嵌入 + 实体关系）→ 策略层（同步编排 + YAML DAG 工作流引擎）。将分散的开发资源编译为 AI 可推理的结构化上下文。
- **以 MCP 协议暴露 71 个 stdio 工具**，实现统一 `McpTool` trait 与幂等路由，Stability 分级体系（5 stable + 58 beta + 8 experimental）保证工具质量。
- **零云端依赖语义检索**：SQLite BLOB + 自定义 `cosine_similarity` UDF 替代向量数据库，Candle/Ollama 本地 embedding，默认构建零 ML 运行时依赖。七条架构红线 CI 强制零生产 panic。

### Syncthing-Rust — P2P 文件同步守护进程（体现系统工程深度）

> 独立项目 · 13 workspace crate · 392 测试全通过 · ~13MB 单静态二进制
> [github.com/juice094/syncthing-rust](https://github.com/juice094/syncthing-rust) · 2025.11 — 至今

- **完整实现 BEP over TLS 协议栈**（prost + rustls + ed25519-dalek），与 Go Syncthing v2.1.0 线级兼容，跨语言 `wire_compat` 集成测试验证。多路径 NAT 穿透（LAN UDP/Global mTLS/STUN/UPnP/Relay v1），生产部署于 Windows ↔ Ubuntu 双节点。
- 证明独立交付复杂分布式协议栈的系统工程能力——从 Protobuf 编解码到 TLS 双向认证到块级增量同步到冲突解决的全链路实现。

---

## 研究经历

### 检索增强生成中输出结构的实证研究（2026.03 — 至今）

[github.com/juice094/acr-select](https://github.com/juice094/acr-select)

> **独立完成**。与达摩院 Qwen 团队可能关注的 RAG 系统优化方向直接相关。

- **S（情境）**：RAG 系统的输出质量不仅取决于检索准确性，还受输出格式（JSON/Markdown/Natural Language）与检索深度的交互影响——现有研究对此缺乏系统性实证分析。
- **T（任务）**：设计跨模型、跨架构、跨领域的受控实验框架，量化评估输出结构与检索配置的交互效应。
- **A（行动）**：
  - 设计 ~40 实验条件、3,000+ 样本的多因子受控实验
  - 提出**格式-内容双维度观测框架**，独立于特定模型架构
  - 跨 7 模型 × 4 架构（OpenAI/Anthropic/DeepSeek/Kimi/Qwen 等）验证框架普适性
  - 主动发现并修正测量 artifact，设计统一评分协议确保统计推断的可靠性
  - 在实验过程中纠正了三个预设的机制假设（经过数据验证后主动放弃），确保结论的实证严格性
- **R（结果）**：论文撰写中（manuscript in progress）；实验框架可复用于后续 RAG 系统评估研究；研究成果直接指导了 Clarity 中 RAG 记忆系统的参数调优。

---

## 教育背景

- **甘肃农业大学** · 信息科学技术学院 · 数据科学与大数据技术 · 工学学士 · 2023.09 — 2027.06
- GPA：整体 83 / 核心课程 86 · 专业前 10%
- **核心课程**：数据结构(90)、大数据挖掘与应用(97)、数据存储与处理技术(96)、数据库原理(86)、操作系统(87)、人工智能导论(86.5)、算法设计与分析(81)
- **证书**：AI 应用工程师（中级）— 工业和信息化部认证

---

## 与达摩院的匹配度

| 达摩院方向 | 候选人对应经验 |
|-----------|--------------|
| **通义千问（Qwen）开源生态** | Candle GGUF 本地推理已支持 Qwen2/Qwen2.5；熟悉 GGUF 格式与量化部署 |
| **Agent 框架 / 工具调用** | 完整实现 MCP 协议四传输 + ReAct/Plan 双模式 Agent + 四层审批链 |
| **RAG / 检索增强** | BM25+向量混合检索 + RRF 融合 + 四级记忆压缩 + RAG 输出结构实证研究 |
| **AI 基础设施 / 系统工程** | 三个生产级 Rust 系统（44+ crate，2,500+ 测试），零 panic 工程基线 |
| **多模态 / 文档理解** | 支持 PDF/md/txt/Word 多格式文档解析和索引 |
| **开源社区贡献** | 3 个活跃开源项目，完整的 CI/CD 和文档体系 |

---

## 其他

- **语言能力**：普通话（母语）、英语（技术文档读写、论文写作）、日语（专业四级 72 分）
- **GitHub**：[github.com/juice094](https://github.com/juice094)
- **可到岗时间**：2026.07；可实习 3-6 个月，每周 5 天
- **驾驶**：C1 驾照
