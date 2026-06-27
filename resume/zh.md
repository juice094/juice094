# 周景潇

**数据科学与大数据技术 · 大三在读 · 本科 2027 届** · 上海 / 北京 / 深圳 / 杭州 / 成都

📞 13626566112 · 📧 2241470466@qq.com · 🔗 github.com/juice094

**求职意向**：AI Agent 开发 / 后端系统开发 / 智能体平台研发

---

## 教育背景

**甘肃农业大学** · 数据科学与大数据技术 · 工学学士 · 2023.09 — 2027.06
- 信息科学技术学院 · 均分 83 / 核心课 86 · 专业前 10%
- 主修课程：数据结构与算法、操作系统、计算机网络、数据库原理、分布式系统、机器学习、大数据技术基础、数据可视化

---

## 技术技能

| # | 技能 | 熟练度 / 项目锚点 |
|:---|:---|:---|
| 1 | **Rust** | 主力语言，3 年。在校独立完成三个大型 Workspace 项目，有效代码 ~6 万行，vibe coding ~27 万行。从 BEP 协议栈到 Agent 内核到编译器管线，均从零构建。 |
| 2 | **Python** | 研究主力。数据分析、实验脚本、统计检验。有效代码 ~2 万行，vibe coding ~7 万。在耦合论文中用于 40+ 条件 × 3000+ 样本的统计分析与可视化。 |
| 3 | **SQLite** | 在 Clarity 中实现 BM25 + 向量混合检索记忆系统（SQLite BLOB + 自定义 cosine_similarity UDF）；在 devbase 中设计 SQLite Registry 统一实体-关系模型。 |
| 4 | **tokio / 异步 Rust** | Clarity 单二进制运行时底层引擎，管理 Agent 循环、MCP 工具并发调用、SPMC 事件总线。tracing + console-subscriber 做分布式诊断。 |
| 5 | **TLS / rustls** | 在 syncthing-rust 中实现 BEP over TLS 完整握手与消息加密，配合 prost + ed25519-dalek 还原 wire 级协议。wire_compat 集成测试验证跨语言互操作。 |
| 6 | **MCP 协议** | Clarity 中实现 stdio / SSE / HTTP / WebSocket 四传输，devbase 中以 MCP 协议暴露 71 个 stdio 工具。深刻理解协议分层、消息边界与生命周期管理。 |
| 7 | **Multi-Agent 协作** | Clarity 支持 Worker 并行调度与 Session Handoff；Plan Mode 将复杂多步任务的步骤遗漏率从 ~40% 降到接近零。 |
| 8 | **RAG / 检索增强** | 在 Clarity 中实现 BM25 + 向量混合检索 + SQLite 记忆持久化。在耦合论文中设计受控实验评估检索深度对输出结构的影响。支持 PDF / md / txt / Word 多种文档。 |
| 9 | **PyTorch** | 使用 ResNet18 + OpenCV 完成苹果质量分类（student-era/ml-apple-detection），训练 50 epoch。理解 DataLoader、transform、TensorBoard 诊断流程。 |
| 10 | **Protobuf / prost** | syncthing-rust 的 BEP 协议完全基于 protobuf 定义编译生成，Clarity 的 WireMessage 使用 prost 做跨前端消息序列化。 |
| 11 | **TypeScript / Vue 3** | student-era 多课程前端项目、personal-portal 个人主页。组件化开发、响应式布局、pnpm monorepo。 |

---

## 个人项目

### Clarity — 本地优先 AI Agent 运行时

**S**：从零构建的本地 AI 运行时，单二进制编排 LLM、MCP 工具、记忆系统与多 Agent 协作。零 Python / Node.js / Ollama 外部依赖。6 个前端入口共享同一 Agent 内核。

**T**：Rust · 22 workspace crates · tokio · SQLite · Candle GGUF · protobuf · egui / ratatui / Axum · [github.com/juice094/clarity](https://github.com/juice094/clarity) · 2026.04 - 至今

**A — R**：
| 做了什么 | 量化结果 |
|:---|:---|
| 设计 Contract-First 分层架构（contract 层零内部依赖、单向引用） | 新功能平均只改 1 层，编译时零循环引用 |
| 实现 ReAct + Plan 双模式 Agent 循环 + 四层 Approval 链 | Plan Mode 步骤遗漏率 ~40% → 接近零 |
| 构建混合记忆系统（SQLite + BM25 + 向量搜索 + 四级压缩归档） | 支持长期记忆持久化与上下文窗口溢出防护 |
| 设计跨前端 SPMC 事件总线（WireMessage 统一协议） | 6 前端共享同一内核，各前端不互相 import |
| 解决 egui Pretext 文字测量精度问题 | 1000 条消息渲染高度偏差 1.45%，estimate/render 分别 74µs / 136µs |
| 工程基线 | 1,889 测试全通过，Clippy 零 warning，零 unwrap/expect |

### 学生项目集 — [student-era](https://github.com/juice094/student-era)
**Vue 3 / Python / JavaScript** · 多课程归档 · 2025.09 - 至今

- **机器学习**：PyTorch + ResNet18 苹果质量检测（8 分类）、天气预测回归
- **Web 前端**：Vue 3 课程设计（组件化、响应式）、HTML5 Canvas 游戏开发
- **数据工程**：Hadoop/Spark/Kafka 课程实验、GIS 空间数据分析
- **学术写作**：农业论文编译、Zephyrus 论文分析

---

### syncthing-rust — P2P 文件同步引擎

**S**：Go Syncthing 的 Rust 重实现，BEP 协议 wire 级兼容。支持跨平台 P2P 文件同步，单二进制 ~13MB。

**T**：Rust · 13 workspace crates · prost + rustls + ed25519-dalek · STUN / UPnP / Relay

**A — R**：
| 做了什么 | 量化结果 |
|:---|:---|
| 实现完整 BEP 协议栈（握手、LZ4 压缩帧、消息序列化） | wire_compat 集成测试验证与 Go Syncthing 跨语言互操作 |
| 构建多路径 NAT 穿透（UDP 广播 + mTLS Discovery + STUN + UPnP + Relay） | 覆盖 LAN / 公网 / 中继三种网络环境 |
| 解决 Windows 文件共享冲突（指数退避重命名 + 三路合并 + 版本归档） | 反病毒/编辑器并发场景下零文件损坏 |
| 实现预测性健康检查 + 自适应并发控制 | 变更检测延迟 ~1s，动态调整扫描/拉取并发 |
| 工程基线 | 392 测试通过，零 Clippy warning，单二进制 ~13MB |

---

### devbase — 开发者工作空间世界模型编译器

**S**：将本地 Git 仓库、PARA 笔记、Skill 脚本与 YAML 工作流编译为 AI 可推理的结构化上下文。

**T**：Rust · 12 workspace crates · tree-sitter · SQLite · MCP · Candle / Ollama

**A — R**：
| 做了什么 | 量化结果 |
|:---|:---|
| 设计三层编译架构（感知→编码→编译），以 MCP 协议暴露工具 | 71 个 stdio MCP 工具，覆盖代码解析、Git 分析、知识检索 |
| SQLite BLOB + 自定义 cosine_similarity UDF 替代向量数据库 | 零云端依赖实现语义检索 |
| 建立 G1-G7 / RF-1-RF-7 架构红线 + CI 强制检查 | 生产代码 unwrap/expect/panic 数量 = 0 |
| CLI 入口规模控制 | src/main.rs 836 行，内部 crate:: 引用超 5 个即禁止拆 crate |

---

## 研究经历

### 检索增强生成中输出结构的实证研究（2026.03 — 至今）

代码仓库：[acr-select](https://github.com/juice094/acr-select)

| S | 围绕 RAG 系统中输出格式与内容质量的交互关系，设计并执行受控实验框架 |
|:---|:---|
| **T** | Python · 7 模型 × 4 架构 · 统计检验 · LaTeX |
| **A** | 设计 ~40 实验条件、3000+ 样本的多因子受控实验；提出格式-内容双维度观测框架；跨四种模型架构验证框架普适性；主动发现测量 artifact 并设计统一评分协议修正统计推断 |
| **R** | 论文撰写中（manuscript in progress）；实验框架可在后续研究中复用 |

---

## 奖项与认证

- AI 应用工程师（中级）— 工业和信息化部认证
- 日语专业四级（72 分）
- 大学英语四级（CET-4）

---

## 自我评价

大三在读，2025.11-2026.06 独立设计并交付三个生产级 Rust 系统（合计 44+ workspace crate、2,500+ 测试全通过）。从 BEP 协议栈到 Agent 内核到世界模型编译器，均从零构建。具备独立闭环能力：发现问题 → 设计实验 → 实现系统 → 写论文。对 AI Agent 核心架构有从 0 到 1 的工程理解——Contract-First 分层、ReAct/Plan 双模式循环、MCP 协议四传输、混合记忆系统。Rust + AI Agent 双稀缺组合，具备将底层系统设计能力迁移到多语言业务栈的基础。最深刻的工程教训：在 syncthing-rust 中花了两天排查一个 Windows 文件句柄泄漏 bug——最终发现是 drop 顺序问题，学会用 tracing span 做生命周期审计。
