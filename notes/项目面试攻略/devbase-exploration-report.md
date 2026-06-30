# devbase 项目探索报告

> 生成时间：2026-06-29
> 探索目录：`C:/Users/22414/dev/devbase`
> 目标：为简历中的"项目经历"和"技术技能"模块提供准确素材，并检查现有简历描述的真实性

---

## 1. 项目概览

| 项目 | 内容 |
|---|---|
| **名称/版本** | `devbase` v0.20.1 |
| **定位** | 本地优先的开发者工作空间数据库与知识库管理器 |
| **一句话定位** | "开发者工作空间的世界模型编译器"——用 Rust 将本地 Git 仓库、Markdown 笔记、Skill 脚本和 YAML 工作流编译为 AI 可直接推理的结构化上下文，并通过 MCP stdio 工具与 ratatui 仪表盘对外服务。 |
| **Rust Edition** | 2024（rustc 1.95+） |
| **代码规模** | 约 **58,814 行 Rust**（`src/` 52,470 行 + `crates/` 4,781 行），不含 target/ |
| **Workspace Crates** | **12 个** |
| **主入口** | `src/main.rs` 共 **836 行** |
| **测试** | 仓库内共有 **634 个 `#[test]`/`#[tokio::test]`** 属性，README 标注 "616+ passed" 基本属实 |

---

## 2. 架构与 Crate 职责

### 12 个 Workspace Crate

| # | Crate | 职责 | 关键依赖 |
|---|---|---|---|
| 1 | `devbase-core-types` | 知识图基础类型：`Node`、`Edge`、`NodeType` | `chrono` |
| 2 | `devbase-registry` | SQLite Registry 核心操作：实体、关系、调用图、死代码 | `rusqlite` |
| 3 | `devbase-embedding` | 本地 Embedding 生成协议：`CandleProvider` / `OllamaProvider` | `candle-*`, `tokenizers`, `ureq` |
| 4 | `devbase-vault-wikilink` | Markdown WikiLink `[[...]]` 解析与反向链接索引 | 纯 std |
| 5 | `devbase-vault-frontmatter` | Markdown YAML frontmatter 解析 | 纯 std |
| 6 | `devbase-skill-runtime-types` | Skill 运行时类型：`SkillMeta`、`SkillType`、执行状态 | `chrono`, `serde` |
| 7 | `devbase-skill-runtime-parser` | `SKILL.md` frontmatter 解析 | `anyhow` |
| 8 | `devbase-symbol-links` | 代码符号关系计算：签名相似度 Jaccard / 同文件聚类 | `rusqlite` |
| 9 | `devbase-sync-protocol` | 轻量目录同步协议 + 版本向量冲突检测 | `walkdir`, `serde` |
| 10 | `devbase-syncthing-client` | Syncthing REST API 客户端 | `reqwest` |
| 11 | `devbase-workflow-model` | YAML 工作流数据模型与 5 种 step 类型 | `serde`, `serde_yaml` |
| 12 | `devbase-workflow-interpolate` | 工作流变量插值：`${inputs.x}`、`${steps.y.outputs.z}` | `regex` |

### 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│ 交互层 (Application / Protocol)                              │
│   src/main.rs 836 行 → commands/ → tui/ (ratatui) → mcp/     │
│   对外：CLI / TUI 仪表盘 / MCP stdio Server                  │
├─────────────────────────────────────────────────────────────┤
│ 编译层 (Semantic / Knowledge)                                │
│   registry/  SQLite 关系存储 + 迁移                          │
│   search/     Tantivy BM25 + 向量混合检索                    │
│   semantic_index/  tree-sitter 符号/调用图提取               │
│   vault/      PARA 笔记 + WikiLink + BFS 图遍历              │
│   skill_runtime/  Skill 发现→安装→执行→评分→发布             │
│   workflow/   YAML DAG 引擎：解析/验证/调度/执行/插值        │
├─────────────────────────────────────────────────────────────┤
│ 可靠层 (Physical / Storage)                                  │
│   SQLite WAL (registry.db) + OpLog 审计                      │
│   Tantivy 全文/符号索引                                       │
│   自定义 cosine_similarity SQLite UDF                        │
└─────────────────────────────────────────────────────────────┘
           ↑
crates/ 12 个零内部耦合子 crate，以 devbase-core-types 为根
```

---

## 3. 关键技术栈

| 技术 | 在项目中支撑的功能 | 关键源码位置 |
|---|---|---|
| **tree-sitter** | 多语言代码解析：函数/结构体/枚举/特征/调用图提取 | `src/semantic_index/symbol.rs`, `src/semantic_index/call_graph.rs` |
| **tantivy** | BM25 全文检索：仓库符号索引、Vault 笔记索引 | `src/search.rs`, `src/search/symbol_index.rs` |
| **rusqlite** | SQLite 关系存储：Registry、OpLog、Agent Memory、向量 BLOB | `src/registry/migrate.rs`, `src/registry/agent_context.rs` |
| **serde + serde_yaml** | YAML 工作流解析、Skill frontmatter、配置序列化 | `crates/devbase-workflow-model/src/step_type.rs`, `crates/devbase-skill-runtime-parser/` |
| **tokio** | 异步 MCP Server、外部 HTTP 调用、守护进程 | `src/main.rs`, `src/mcp/mod.rs` |
| **ratatui + crossterm** | 终端仪表盘 TUI | `src/tui/` |
| **git2** | Git 仓库状态扫描、历史、同步 | `src/scan.rs`, `src/vault/history.rs` |
| **reqwest** | GitHub / arXiv / Syncthing REST 调用 | `src/mcp/tools/external.rs`, `crates/devbase-syncthing-client/` |
| **r2d2 + r2d2_sqlite** | SQLite 连接池 | `src/storage.rs` |
| **walkdir** | 仓库/Vault 目录遍历 | `src/scan.rs`, `src/vault/scanner.rs` |
| **blake3** | 内容摘要 | `src/digest.rs` |
| **rayon** | 并行索引 | `src/search.rs` 等 |

---

## 4. 关键技术点核实

### 4.1 MCP 工具数量

**重要不一致**：README / AGENTS.md / CLAUDE.md 均写 **71 个 MCP 工具**，但实际注册数量为 **81 个**。

证据：`src/mcp/mod.rs` 中 `McpToolEnum` 枚举从 `Scan` 到 `CodeGraph` 共 **81 个变体**。

### 4.2 tree-sitter 多语言解析

**属实**。`src/semantic_index/symbol.rs` 使用 `tree_sitter::Parser` 根据扩展名选择语言，支持 Rust/Python/TypeScript/Go。

### 4.3 SQLite + Tantivy 混合检索

**属实**。Tantivy BM25 + SQLite 回退 + 自定义 `cosine_similarity` UDF 向量检索。

### 4.4 YAML DAG 工作流引擎

**属实**。5 种 step 类型（Skill/Subworkflow/Parallel/Condition/Loop），拓扑调度（Kahn 算法），变量插值。

### 4.5 PARA / Vault / Wikilink 知识管理

**属实**。PARA 目录结构、WikiLink 反向链接、BFS 图遍历。

### 4.6 G1–G7 / RF-1–RF-7 架构红线

**文档完整，但机械 enforcement 有限**。CI 脚本仅检查部分规则（G5 新增 unwrap、T11、T12、模块提取）。

### 4.7 依赖注入与测试密封性

**属实**。`StorageBackend` trait + `AppContext` 中央依赖注入容器。

### 4.8 零生产 panic / unwrap / expect

**基本属实**。
- `src/` 生产代码：0 处
- `crates/devbase-workflow-interpolate`：2 处 `expect`（基于正则捕获组不变量）

### 4.9 12 Crate 的 Cargo Workspace 拆分

**属实**。

---

## 5. 与现有简历描述的一致性检查

| 简历描述 | 状态 | 说明 |
|---|---|---|
| 12 workspace crates + 主 crate | ✅ 准确 | `crates/` 12 目录 |
| tree-sitter 多语言解析 | ✅ 准确 | 有代码证据 |
| SQLite + Tantivy 混合检索 | ✅ 准确 | 有代码证据 |
| 71 个 MCP 工具 | ⚠️ 过时 | 实际 **81** 个 |
| G1–G7/RF-1–RF-7 架构红线 | ✅ 存在 | 但 CI 仅部分机械检查 |
| 零生产 panic | ⚠️ 基本准确 | `src/` 为 0；workspace crate 有 2 处 expect |
| YAML DAG 工作流引擎 | ✅ 准确 | 5 种 step 类型 + 拓扑调度 |
| 836 行以内的 src/main.rs | ✅ 准确 | 836 行 |

---

## 6. 简历可用素材

### 6.1 项目经历 Bullet Points（STAR 法则）

1. **主导本地优先的开发者工作空间"世界模型编译器"**
   - Situation：AI 工具需要可推理的代码/笔记/工作流上下文，但云端方案有隐私与延迟问题。
   - Task：将本地 Git 仓库、PARA 笔记、Skill 脚本和 YAML 工作流编译为结构化上下文。
   - Action：用 Rust 2024 构建 devbase，集成 tree-sitter 多语言解析、SQLite WAL 关系存储、Tantivy BM25、自定义 cosine_similarity SQLite UDF。
   - Result：通过 **81 个 MCP stdio 工具**和 ratatui 仪表盘对外服务，默认构建零 ML 运行时依赖。

2. **实现 SQLite + Tantivy 混合语义检索**
   - Task：在无云端依赖前提下支持代码符号与笔记的语义/关键词召回。
   - Action：Tantivy 负责 BM25 全文/符号索引；SQLite BLOB 存储 embedding，并注册自定义标量函数 `cosine_similarity` 做向量相似度计算；混合层融合多路结果。
   - Result：默认 feature 下无需 Candle/Ollama 即可运行关键词检索；开启 embedding feature 后可本地生成 embedding。

3. **设计并实现 YAML DAG 工作流引擎**
   - Task：让 AI/用户能够编排多 Skill 流水线。
   - Action：定义 Skill/Subworkflow/Parallel/Condition/Loop 5 种 step 类型，实现 YAML 解析、依赖验证、拓扑调度、变量插值和 SQLite 持久化执行状态。
   - Result：工作流可按依赖层级并行执行，支持循环与条件分支。

4. **落地 12 crate 的 Cargo Workspace 拆分与架构红线**
   - Task：控制 ~5.9 万行 Rust 代码的模块耦合。
   - Action：以 `devbase-core-types` 为无耦合根节点，提取 registry、vault、skill、workflow、sync 等 12 个 workspace crate；制定 G1-G7/RF-1-RF-7 架构红线；`src/main.rs` 控制在 836 行。
   - Result：子 crate 禁止反向依赖主库；`src/` 生产代码 unwrap/expect/panic 数量为 0。

5. **构建 ratatui 终端仪表盘与 MCP stdio Server**
   - Task：为人类开发者和 AI Agent 提供统一入口。
   - Action：实现跨仓库 Git 状态仪表盘、Vault 笔记搜索/图遍历、Skill 发现与执行；所有能力通过 `McpTool` trait 暴露为 MCP 工具。
   - Result：人类可用 `devbase tui`，AI 客户端可通过 `devbase mcp` 调用 81 个工具。

### 6.2 技术技能模块技能点

1. Rust 系统开发 / Cargo Workspace 治理
2. tree-sitter 多语言代码解析与符号/调用图提取
3. Tantivy 全文检索（BM25）
4. SQLite 嵌入式数据库 + rusqlite + 自定义 UDF
5. 混合检索（BM25 + 向量相似度）
6. MCP stdio 工具设计与实现
7. YAML DAG 工作流引擎
8. tokio 异步运行时
9. ratatui / crossterm 终端 UI
10. 依赖注入与测试密封性设计

### 6.3 需谨慎表述或避免夸大的地方

| 建议表述 | 风险 | 建议修改 |
|---|---|---|
| "71 个 MCP 工具" | 实际为 81 个 | 改为 "81 个 MCP 工具" |
| "零生产 panic/unwrap/expect" | workspace crate 有 2 处 expect | 改为 "`src/` 生产代码零 unwrap/expect/panic" |
| "CI 强制 G1-G7/RF-1-RF-7" | CI 仅检查部分规则 | 改为 "定义并维护 G1-G7/RF-1-RF-7 架构红线，核心规则纳入 CI invariant checks" |
| "约 5.9 万行代码" | 含注释/空行/测试 | 可写 "约 5.9 万行 Rust（含测试与 workspace crates）" |

---

## 7. 关键源码路径索引

| 主题 | 文件路径 |
|---|---|
| main.rs 836 行 | `src/main.rs` |
| 12 crates 列表 | `crates/` |
| MCP 工具枚举（81 个） | `src/mcp/mod.rs` |
| tree-sitter 符号提取 | `src/semantic_index/symbol.rs` |
| tree-sitter 调用图 | `src/semantic_index/call_graph.rs` |
| Tantivy 索引 | `src/search.rs` |
| 混合检索 | `src/search/hybrid.rs` |
| cosine_similarity UDF | `src/registry/agent_context.rs` |
| 工作流 5 step 类型 | `crates/devbase-workflow-model/src/step_type.rs` |
| 工作流拓扑调度 | `src/workflow/scheduler.rs` |
| PARA 目录结构 | `src/vault/scanner.rs` |
| WikiLink 解析 | `crates/devbase-vault-wikilink/src/lib.rs` |
| Vault BFS 图遍历 | `src/vault/mod.rs` |
| 依赖注入 StorageBackend | `src/storage.rs` |
| G1-G7/RF-1-RF-7 定义 | `AGENTS.md`, `CLAUDE.md` |
