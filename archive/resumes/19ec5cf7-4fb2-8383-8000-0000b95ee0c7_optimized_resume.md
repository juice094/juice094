---
title: "个人简历 — 优化版"
date: 2026-06-14
version: optimized
---

# 周景潇

**手机：** 136****6112 | **邮箱：** 2241470466@qq.com | **GitHub：** github.com/juice094

---

## 教育背景

**甘肃农业大学** — 工学学士（预计），数据科学与大数据技术  
2023.09 - 2027.06 | 信息科学技术学院

- 均分 83，核心专业课均分 86，专业排名前 10%
- 核心课程：数据结构(90)、数据库原理(86)、大数据挖掘与应用(97)、数据存储与处理技术(96)、操作系统(87)

---

## 技能清单

| 类别 | 技术栈 |
|------|--------|
| **编程语言** | **Rust**（主力）、Python、Go、TypeScript、SQL |
| **前端框架** | Vue 3、Next.js、eframe/egui |
| **数据库与检索** | SQLite、Tantivy BM25、向量搜索、Hadoop / Spark / Kafka |
| **AI / Agent** | MCP 工具生态、ReAct / Plan 双模式 Agent、RAG 检索增强、Candle 本地推理 |
| **网络与协议** | P2P 协议设计、TCP+TLS、WebSocket / SSE、prost 编解码、NAT 穿透 |
| **工程实践** | 测试驱动开发（2000+ 测试）、CI/CD 门禁、多 crate 架构拆分、OpLog 审计 |

---

## 项目经历

### Clarity — AI Agent 运行时框架
**项目发起人 / 核心维护者** | 2026.04 - 至今 | github.com/juice094/clarity

为解决 AI 工具链碎片化与云端依赖问题，设计"本地优先、单二进制、零外部运行时依赖"的 Agent 框架。主导 14 个 Rust crate 的模块拆分与接口契约设计，建立 contract 层零内部依赖、core 层零前端依赖的架构约束。实现 ReAct / Plan 双模式 Agent 循环、多 Agent 协作调度、MCP stdio/SSE/WebSocket 三传输、BM25+向量混合记忆检索、Candle 本地 GGUF 推理、eframe/egui 桌面 GUI 与四层 Approval 审批链。**累计 1100+ lib 测试通过，生产代码零 unwrap/expect。**

- **技术亮点**：MCP 三传输适配层；BM25+向量混合检索实现上下文精准召回；core 层与前端完全解耦
- **质量门禁**：clippy 0 warning；所有 public API 强制文档注释；四层审批链保障 Agent 行为可控

---

### devbase — 开发者工作空间编译器
**项目发起人 / 核心维护者** | 2026.04 - 至今 | github.com/juice094/devbase

面向多仓库、多智能体协作场景，设计并迭代 71 个 MCP 工具的开发者工作空间编译器。主导从原始代码/笔记到结构化情境的完整 pipeline：tree-sitter 解析 → Tantivy BM25 + SQL 向量索引 → 检索 → 推理调用。集成 ratatui 终端仪表盘、SQLite WAL 并发存储与 OpLog 审计机制。**500+ 测试通过，Schema 迁移自动备份。**

- **技术亮点**：纯 SQL 实现 cosine_similarity UDF 向量搜索；tree-sitter 多语言代码结构化解析；Workflow YAML 编排 Skill 生命周期
- **质量门禁**：Registry 写入强制 OpLog 审计留痕；健康检查自动化；Skill 发布流程标准化

---

### syncthing-rust — P2P 文件同步引擎
**项目发起人 / 核心维护者** | 2026.04 - 至今 | github.com/juice094/syncthing-rust

以 Rust 重写 Syncthing BEP 协议栈，主导 8 个 crate 的协议-传输-同步分层架构。负责 prost 协议编解码、TCP+TLS 传输层、设备发现与 Relay 中继、文件索引与块级同步、REST API 服务。独立解决 P2P/NAT/防火墙穿透问题，实现 Version Vector 冲突消解。**lib 测试 327+ 通过，跨网络部署验证可行。**

- **技术亮点**：Tailscale 集成绕过防火墙包检测；Windows 系统托盘与 TUI 双端支持；协议握手栈完整自研
- **质量门禁**：clippy 0 warning；跨网络场景可复现验证

---

## 资格认证

- AI 应用工程师（中级）— 工业和信息化部认证
- 日语专业四级（72 分）
- C1 驾驶证

---

## 自我评价

大数据专业大三在读，前 10%。近三个月主导 3 个 Rust 开源项目，累计 2000+ 测试通过，核心训练是复杂系统的架构拆分、接口约束与质量兜底。擅长从第一性原理拆解问题，习惯用笔记系统沉淀知识与进度。对 MCP/Agent 生态、检索系统、P2P 协议有实践级理解。

---

_存档于 2026-06-14。本版为 ATS 优化版，1 页结构，纯文本格式。_
