---
type: CareerDoc
title: "周景潇 — 个人简历（老油条版）"
tags: [resume, career, mentor-review]
timestamp: 2026-06-25T20:00:00+08:00
---

# 周景潇

**手机：** 13626566112 | **邮箱：** 2241470466@qq.com | **GitHub：** [github.com/juice094](https://github.com/juice094)
**求职意向：** AI 应用开发 / 后端开发 / 数据工程 · 上海/杭州/深圳 · 2026.07 可到岗

---

## 教育背景

**甘肃农业大学** · 数据科学与大数据技术 · 工学学士（预计 2027.06）
信息科学技术学院 | 均分 83 / 核心课 86 | 专业前 10%

核心课程：数据结构(90)、大数据挖掘与应用(97)、数据存储与处理技术(96)、数据库原理(86)、操作系统(87)、人工智能导论(86.5)

---

## 技能

- **精通 Rust**：3 个开源项目、44 crates、2000+ 测试、零 unwrap/expect 生产代码。用于 Agent 运行时、P2P 协议栈、工作空间编译器
- **熟练 Python**：数据分析与实验脚本（Pandas/NumPy），耦合论文 40 个实验条件的全量分析
- **熟练 MCP / Agent 生态**：MCP stdio/SSE/WebSocket 三传输、ReAct/Plan 双模式 Agent、RAG 检索增强、Candle 本地推理
- **熟练搜索与存储**：Tantivy BM25 全文检索、纯 SQL 向量搜索（cosine_similarity UDF）、SQLite WAL
- **掌握**：Go、TypeScript、Vue 3、Hadoop/Spark/Kafka（课程级）
- **工程实践**：测试驱动开发、CI/CD 门禁、多 crate 架构拆分、OpLog 审计

---

## 研究经历

### 格式-内容耦合的行为机制研究（2026.06 — 至今）

**独立完成。** 「框架跟着数据走，数据不跟着框架走。」

在 7 个语言模型（0.6B–8B，Qwen/Llama/Gemma/Phi3 四架构）× 3 个领域（农业 QA、HotpotQA 多跳推理、TriviaQA）× 2 个检索深度（k=1,3）的 40 个实验条件、3000+ 样本上——

- **发现耦合不随容量单调递减**。HotpotQA 上 7B 耦合（r=+0.20）而 0.6B 不解耦（r≈0），推翻"参数量越大越解耦"的直觉
- **提出"生成预算窗口"统一解释两种耦合模式**。0.6B 农业 QA：undershoot（输出截断→格式内容一起垮）；7B HotpotQA：overshoot（冗长犹豫→格式差+内容错）
- **主动验证并撤回三个伪机制假说**。注意力稀释、输出膨胀被 H1/H2 反方向数据排除；"方向翻转"经统一评分尺后证实为测量 artifact——认了
- **跨四架构验证**。窗口假说在 Qwen/Llama/Gemma/Phi3 上成立，四种架构在窗口外走四条不同路径
- 论文 v9.1（10 页）撰写中，拟投 NLP workshop

---

## 项目经历

### Clarity — AI Agent 运行时框架
**Rust** · 22 crates · 1227 tests · ~150K 行 | github.com/juice094/clarity | 2026.04 - 至今

- 将 22 个 crate 拆为 contract/core/frontend 三层，contract 层零依赖→新增功能平均只改 1 层，编译时零循环引用
- 实现 ReAct + Plan 双模式 Agent 循环，Plan Mode 将复杂任务步骤遗漏从 ~40% 降到接近 0
- 集成 MCP stdio/SSE/WebSocket 三传输 + BM25/向量混合检索 + Candle 本地 GGUF 推理 + 四层 Approval 审批链
- 1227 个测试通过，生产代码零 unwrap/expect，clippy 零 warning

### devbase — 开发者工作空间编译器
**Rust** · 13 crates · 71 MCP 工具 · 500+ tests | github.com/juice094/devbase | 2026.04 - 至今

- 从零搭建 71 个 MCP 工具的工作空间编译器，覆盖代码解析→索引→检索→推理调用全 pipeline，预编译二进制 ~8.7MB
- 用纯 SQL 实现 cosine_similarity UDF 向量搜索，替换外部向量数据库，部署步骤从 4 步减到 1 步
- 集成 tree-sitter 多语言代码解析 + Tantivy BM25 全文索引 + SQLite WAL + OpLog 审计，500+ 测试通过

### syncthing-rust — P2P 文件同步引擎
**Rust** · 9 crates + 5 binaries · 327+ tests | github.com/juice094/syncthing-rust | 2026.04 - 至今

- 将 Syncthing BEP 协议栈拆为协议/传输/同步/存储四层，9 crate + 5 binary 的分层架构，单二进制 ~12MB 静态编译
- 从零实现 prost 协议编解码、TCP+TLS 传输层、UDP/HTTPS/STUN/UPnP 设备发现、Relay v1 中继
- 通过 Tailscale 集成解决 NAT/防火墙穿透，跨网络环境可复现验证；clippy 零 warning

### student-era — 课程与自学归档
Python / Vue / PyTorch / Hadoop | github.com/juice094/student-era | 2023.09 - 至今

Vue 3 + ECharts 数据可视化仪表盘、PyTorch 计算机视觉、Hadoop/Spark/Kafka 大数据处理、GIS 遥感分析、数值方法、网络安全与信息检索。基于 WSL2 完成全链路动手实践。

---

## 语言与认证

- 日语专业四级（72 分）
- AI 应用工程师（中级）— 工业和信息化部认证

---

## 自评

**有：** 一个从假说到实验到论文的独立研究闭环（框架跟数据走，不可算的不说，不显著就认）。三个 Rust 系统项目的架构拆分能力（44 crates / 2000+ 测试 / 零 unwrap）。

**缺：** 无实习（没见过生产环境 review/上线/oncall）。无合作发表（没走过同行评议）。广度不够（没碰分布式/DB 内核/大规模 ML）。大三没毕业。

---

_给能帮我改的人。不包装，不改口。看完告诉我哪里该砍、哪里该补。_
