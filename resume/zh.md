# 周景潇

**13626566112** · **2241470466@qq.com** · **[github.com/juice094](https://github.com/juice094)**
**AI 应用开发 / 后端开发 / 数据工程** · 上海/杭州/深圳 · 2026.07 可到岗

---

## 教育背景

**甘肃农业大学** · 数据科学与大数据技术 · 工学学士（预计 2027.06）
信息科学技术学院 · 均分 83 / 核心课 86 · 专业前 10%

---

## 技能

| 领域 | 技术 |
|:---|:---|
| **语言** | Rust（主力，3 年）、Python（研究）、TypeScript/Vue（课程）、Go（阅读级） |
| **系统** | tokio 异步、TLS 1.3、UDP/TCP、NAT 穿透、SQLite WAL |
| **AI / Agent** | MCP 协议（stdio/SSE/WebSocket）、ReAct+Plan Agent、RAG、BM25+向量搜索 |
| **工程** | 62-crate workspace 管理、TDD、CI/CD、OpLog 审计 |

---

## 研究经历

### 格式-内容耦合的行为机制研究（2026.06 — 至今）

**独立完成。** 7 模型 × 4 架构 × 3 领域，40 实验条件，3000+ 样本。

- 发现耦合不随参数量单调递减——7B 耦合（r=+0.20）而 0.6B 不解耦，推翻直觉
- 提出「生成预算窗口」统一 undershoot/overshoot 两种耦合模式
- 跨 Qwen/Llama/Gemma/Phi3 四架构验证：窗口假说成立，四条不同的失败路径
- 主动识别并撤回三个伪机制假说，方向翻转经统一评分尺证实为测量 artifact
- 论文 10 页（TACL 格式），拟投 NLP workshop

---

## 项目经历

### Clarity — AI Agent 运行时
**Rust** · 25 crates · 1,243 tests · 152K LOC · [github.com/juice094/clarity](https://github.com/juice094/clarity) · 2026.04 - 至今

本地优先的 AI Agent 运行时，单二进制编排 LLM、MCP 工具、记忆系统。
- Contract/Core/Frontend 三层架构，contract 层零依赖，新功能平均只改 1 层
- ReAct + Plan 双模式 Agent，Plan Mode 将步骤遗漏从 ~40% 降到接近 0
- MCP 三传输 + BM25/向量混合检索 + 四层 Approval 审批链 + ChaCha20 加密存储
- 5 种 UI 后端（TUI/egui/Slint/Tauri/headless），移动端 FFI 绑定

### devbase — 开发者工作空间编译器
**Rust** · 12 crates · 71 MCP 工具 · 56K LOC · [github.com/juice094/devbase](https://github.com/juice094/devbase) · 2026.04 - 至今

代码上下文 + 知识记忆 + Agent 推理的统一编译器。
- 纯 SQL cosine_similarity UDF → 去外部向量 DB，部署步骤 4→1
- tree-sitter 多语言解析 + Tantivy BM25 + SQLite WAL + OpLog 审计
- 预编译二进制 ~8.7MB

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
