# Devbase 开发者学习路线图

> **目标读者**：有 Rust 基础，想理解"开发者工作空间世界模型编译器"架构的开发者
> **项目规模**：12 workspace crates + 主 crate，71 MCP 工具，616+ 测试，schema v36
> **预计总学习时间**：入门 1 周 → 进阶 3 周 → 精通 6 周

---

## 1. 前置知识要求

### 1.1 Rust 基础

| 技能 | 要求等级 | 在项目中的体现 |
|------|---------|---------------|
| 所有权/生命周期 | ⭐⭐⭐⭐ | AppContext DI 容器，StorageBackend trait |
| trait 系统 | ⭐⭐⭐⭐⭐ | McpTool trait，模块化架构 |
| 并发（rayon + crossbeam） | ⭐⭐⭐ | 并行扫描、channel 通信 |
| serde 序列化 | ⭐⭐⭐⭐ | TOML/YAML/JSON 配置 |
| Cargo workspace | ⭐⭐⭐⭐ | 12 个独立 crate |

### 1.2 领域知识

| 领域 | 重要程度 | 学习资源 |
|------|---------|---------|
| 全文搜索（倒排索引/BM25） | ⭐⭐⭐⭐⭐ | Tantivy 文档 |
| SQLite 内部机制（WAL/迁移） | ⭐⭐⭐⭐ | sqlite.org |
| tree-sitter 语法树 | ⭐⭐⭐ | tree-sitter.github.io |
| MCP 协议 | ⭐⭐⭐⭐ | modelcontextprotocol.io |
| PARA 笔记方法论 | ⭐⭐⭐ | fortelabs.com/blog/para |

---

## 2. 架构总览：三层世界模型

```
交互层 (Interaction)
  CLI (clap)  │  TUI (ratatui)  │  MCP Server (71 tools)
        ↓ 命令/查询/工具调用
编译层 (Compilation)
  感知(Perceive) → 知识(Knowledge) → 策略(Strategy)
  tree-sitter        SQLite Graph       sync orchestrator
  Tantivy BM25       Vectors+Relations   workflow DAG
  git2 diff          Embeddings          health guard
        ↓ 读写
可靠性层 (Reliability)
  SQLite WAL  │  Tantivy Index  │  OpLog Audit  │  Backup
```

核心隐喻：**"世界模型编译器"** — 将开发者本地工作空间（Git repos + PARA 笔记 + 技能 + 工作流）编译为 AI 可推理的结构化知识图谱，类似编译器将源码编译为 AST/IR。

---

## 3. 阶段一：核心类型与存储（⭐⭐ | 2-3 天）

### 3.1 devbase-core-types（叶子 crate）

路径：`crates/devbase-core-types/src/lib.rs`

```rust
struct Node {
    id: NodeId,
    node_type: NodeType, // Repo, File, Symbol, Note, Skill, Workflow
    properties: HashMap<String, Value>,
}

struct Edge {
    from: NodeId, to: NodeId,
    edge_type: EdgeType, // DependsOn, References, Contains, DefinedIn
}
```

### 3.2 Registry（SQLite Schema v36）

路径：`src/registry/`

关键特性：36 个顺序迁移（`v01.rs` → `v36.rs`），每次迁移前自动备份 SQLite 数据库，`SCHEMA_DDL` 作为单一真相源。

```rust
pub fn migrate(conn: &Connection) -> Result<()> {
    let current_version = get_schema_version(conn)?;
    while current_version < CURRENT_SCHEMA_VERSION {
        backup_database(conn)?;
        apply_migration(conn, current_version + 1)?;
    }
    Ok(())
}
```

### 3.3 StorageBackend + AppContext（DI 容器）

路径：`src/storage.rs`

```rust
pub trait StorageBackend: Send + Sync {
    fn data_dir(&self) -> &Path;
    fn config_dir(&self) -> &Path;
    fn open_db(&self) -> Result<Connection>;
    fn open_tantivy_index(&self, name: &str) -> Result<Index>;
}
```

面试要点：
- **RF-1/G1**：禁止硬编码路径 — 必须通过 `StorageBackend` 注入
- **RF-2/G2**：测试用 `tempfile` + 注入 `StorageBackend` — 完全隔离，不污染真实环境

---

## 4. 阶段二：感知层（⭐⭐⭐ | 4-6 天）

### 4.1 Semantic Index（tree-sitter 代码解析）

路径：`src/semantic_index/` | 支持语言：Rust, Python, TypeScript, Go

```
源文件 → tree-sitter 解析 → CST → 符号提取(SymbolNode)
                                 → 调用图提取(CallEdge)
                                 → 差异分析(DiffResult)
```

**为什么选 tree-sitter 而非正则？**
- 容错解析：语法错误时仍能产生部分 AST
- 多语言统一接口
- 增量解析：只重解析变化部分（git diff 驱动）

### 4.2 Vault Scanner（PARA 笔记）

路径：`src/vault/`

| 模块 | 功能 |
|------|------|
| `scanner` + `indexer` | 发现/索引 Markdown 文件 |
| `frontmatter` | YAML 元数据提取（`devbase-vault-frontmatter` crate） |
| `wikilink` | `[[note]]` / `[[note#heading]]` 解析（`devbase-vault-wikilink` crate） |
| `backlinks` | BFS 构建双向链接图 |

### 4.3 Knowledge Engine

路径：`src/knowledge_engine/` — 从 README 和代码结构自动提取模块知识

---

## 5. 阶段三：知识层 — 搜索与索引（⭐⭐⭐⭐ | 5-7 天）

### 5.1 Tantivy BM25 + 向量混合搜索

路径：`src/search/hybrid.rs`

```rust
struct HybridSearchEngine {
    tantivy_index: Index,      // BM25 全文索引
    sqlite_db: Connection,     // 向量存储(cosine_similarity UDF)
}
```

### 5.2 自定义 Cosine Similarity SQL UDF

零外部向量数据库依赖：SQLite 自定义函数实现向量相似度计算。

```sql
SELECT chunk_id, cosine_similarity(embedding, ?1) as sim
FROM embeddings WHERE sim > 0.7 ORDER BY sim DESC LIMIT 20;
```

面试追问"为什么不用 pgvector/Qdrant？"→ 本地优先原则，个人规模不需要分布式向量数据库。

### 5.3 RRF 融合算法

```
score_rrf(doc) = Σ (1 / (60 + rank_i(doc)))
```

BM25 捕获关键词匹配，向量捕获语义相似，RRF 融合两者排名。

---

## 6. 阶段四：策略层（⭐⭐⭐⭐ | 5-7 天）

### 6.1 Workflow DAG 执行器

路径：`src/workflow/` | 5 种步骤类型：skill / subworkflow / parallel / condition / loop

```yaml
steps:
  - id: scan-repos
    type: skill
    skill: repo-scanner
  - id: index-parallel
    type: parallel
    steps: [{skill: index-rust}, {skill: index-python}]
  - id: build-graph
    type: skill
    skill: graph-builder
    depends_on: [index-parallel]
```

循环依赖检测：拓扑排序 — 不能完成则存在环。

### 6.2 Sync Orchestrator

路径：`src/sync/` — 检测变更 → 按依赖排序 → 并行同步 → 聚合 → 更新知识图谱

### 6.3 Skill Runtime

路径：`src/skill_runtime/` — 生命周期：发现 → 解析 → 注册 → 依赖解析 → 执行 → 评分

```markdown
---
name: embed-repo
description: 为代码仓库生成向量嵌入
inputs: [{name: repo_path, type: path, required: true}]
outputs: [{name: embedding_index, type: tantivy_index_path}]
---
```

---

## 7. 阶段五：交互层（⭐⭐⭐ | 4-5 天）

### CLI：`src/main.rs`（<1000 行 RF-4）+ `src/commands/`

```bash
devbase scan / query "lang:rust" / tui / mcp
```

### TUI 仪表盘：`src/tui/` — Git 状态矩阵 + 批量同步 + 知识图谱浏览

### MCP Server：`src/mcp/` — 71 个工具

```rust
pub trait McpTool: Send + Sync {
    fn name(&self) -> &str;
    fn stability(&self) -> Stability; // Stable/Beta/Experimental
    async fn execute(&self, args: Value) -> Result<Value>;
}
```

| 类别 | Stable | Beta | Experimental |
|------|--------|------|-------------|
| 仓库/代码/知识/笔记/技能/工作流/会话/其他 | 5 | 58 | 8 |

---

## 8. 阶段六：架构守卫（⭐⭐⭐⭐ | 3-4 天）

| 规则 | 内容 | 动机 |
|------|------|------|
| RF-1 | 禁止硬编码路径 | 测试隔离、跨平台 |
| RF-2 | 测试用 tempfile + 注入 StorageBackend | 可重复性 |
| RF-3 | SCHEMA_DDL 与 migrate.rs 同步 | 数据一致性 |
| RF-4 | main.rs < 1000 行 | 关注点分离 |
| RF-5 | 禁止模块间循环依赖 | 架构清晰 |
| RF-6 | 零 unwrap/expect/panic | 健壮性 |
| RF-7 | 提取限制 | 防止过早抽象 |

---

## 9. 源码阅读顺序

**第一优先**（骨架）：
1. `Cargo.toml` → 2. `crates/devbase-core-types/src/lib.rs` → 3. `src/storage.rs` → 4. `src/lib.rs` → 5. `src/main.rs`

**第二优先**（核心）：
6. `src/registry/` → 7. `src/search/hybrid.rs` → 8. `src/semantic_index/` → 9. `src/vault/backlinks.rs`

**第三优先**（上层）：
10. `src/mcp/` → 11. `src/workflow/executor.rs` → 12. `src/tui/`

---

## 10. 实践练习

**入门**：运行 scan/query/tui → **进阶**：添加 MCP 工具/新语言支持/创建 SKILL.md → **精通**：新融合算法/新步骤类型 → **贡献级**：修 bug + 完整测试 + PR

---

## 11. 面试深度参考

- **"世界模型编译器"** — 将分散的工作空间编译为 AI 可推理的知识图谱
- **为什么 Tantivy 而非 ES？** — 嵌入式零运维，Rust 原生，个人规模足够
- **为什么自定义 cosine_similarity UDF？** — 本地优先，避免引入新基础设施
- **71 个 MCP 工具如何保证质量？** — Stability 分级 + 独立测试 + 晋升流程
- **PARA vs 普通文件夹？** — 分类策略不同 + wikilink 双向链接

---

> **下一步**：阅读 [`devbase-interview-guide.md`](../项目面试攻略/devbase-interview-guide.md) 进行面试模拟。
