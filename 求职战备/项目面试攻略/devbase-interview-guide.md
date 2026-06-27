# Devbase 项目面试攻略

> 项目：本地开发者工作空间世界模型编译器 | 12 crate, 71 MCP 工具, 616+ 测试
> 候选人：周景潇 | 求职方向：AI Agent 开发 / 工具/平台开发

---

## 1. 项目介绍话术

### 30 秒版

> "Devbase 是我开发的开发者工作空间编译器。它扫描本地的 Git 仓库、Markdown 笔记和脚本，把它们编译成 AI Agent 可以直接理解和搜索的知识图谱。通过 MCP 协议暴露了 71 个工具，让 AI 能够了解你的整个开发环境。"

### 2 分钟版

> "Devbase 解决的核心问题是：当 AI Agent 帮你写代码时，它对你本地的项目结构、笔记系统、历史上下文一无所知。Devbase 就像一个'世界模型编译器'，把分散的开发资源——多个 Git repo、PARA 格式的 Markdown 笔记、YAML 工作流定义——编译成统一的知识图谱。
>
> 技术实现上有三层：感知层用 tree-sitter 做代码符号提取、Tantivy 做全文索引；知识层用 SQLite 做图存储、自定义代数做向量相似度；策略层有 YAML DAG 工作流引擎做任务编排。通过 MCP stdio 协议，任何 AI Agent 都可以使用它的 71 个工具——从代码搜索到笔记查询到工作流执行。
>
> 架构上有七条守卫规则强制执行：零 unwrap、依赖注入、隔离测试、schema 迁移备份等。636 个测试通过，零 Clippy 警告。"

---

## 2. 高频面试问题

### Q1: "世界模型编译器"这个抽象如何落地？（⭐⭐⭐⭐⭐）

**推荐回答**：
"这个隐喻来自编译器理论。传统编译器：源码 → 词法分析 → 语法分析 → AST → 代码生成。Devbase：工作空间文件 → tree-sitter 解析 → 知识图谱（Node/Edge）→ AI 可推理的上下文。

具体落地：
- **词法/语法分析**对应 tree-sitter 符号提取 + Tantivy 全文索引
- **AST**对应知识图谱——Node 是实体（仓库/文件/函数/笔记/技能），Edge 是关系（依赖/引用/包含/定义）
- **代码生成**对应——为 AI Agent 生成结构化的 `project-brief`、`impact-analysis`、`dependency-graph` 等上下文

这个设计让每个'编译阶段'可以独立优化。比如我可以在不改变知识图谱结构的情况下替换 tree-sitter 为其他解析器。"

### Q2: 为什么 Tantivy 而非 Elasticsearch？（⭐⭐⭐⭐）

**推荐回答**：
"三个原因：
1. **嵌入式 vs 独立服务**：Tantivy 是 Rust 库，编译进二进制；Elasticsearch 需要独立部署和运维。对于本地开发工具，零运维是刚需
2. **Rust 原生**：Tantivy 是 Rust 生态的一部分，类型安全、编译时检查。Elasticsearch 需要通过 HTTP API 或 Java 客户端调用——增加故障点
3. **规模匹配**：Tantivy 可以高效处理百万级文档。个人开发工作空间的规模（几千到几万个文件）完全在舒适区内，不需要 Elasticsearch 的分布式能力

Tantivy 本质上是 Rust 版的 Lucene——倒排索引、BM25 评分、分词器、查询解析——该有的功能都有。"

### Q3: 71 个 MCP 工具如何注册和路由？（⭐⭐⭐）

**推荐回答**：
"所有工具通过 `McpTool` trait 统一接口：

```rust
pub trait McpTool: Send + Sync {
    fn name(&self) -> &str;
    fn description(&self) -> &str;
    fn schema(&self) -> ToolSchema;
    fn stability(&self) -> Stability;
    async fn execute(&self, args: Value) -> Result<Value>;
}
```

注册方式：
- 每个工具在 `src/mcp/tools/` 下有独立文件
- `McpToolEnum` 枚举包含所有工具变体
- MCP server 启动时，遍历所有变体生成 tool list
- 请求到达时，按 tool name 路由到对应变体的 `execute`

稳定性分级：
- **Stable**（5个）：生产就绪，API 不变
- **Beta**（58个）：功能完善，API 可能调整
- **Experimental**（8个）：新功能，可能随时变化

新的工具想从 Beta 升到 Stable，需要 2 周无 bug 报告 + 完整测试覆盖。"

### Q4: 自定义 cosine_similarity SQL UDF 的考量？（⭐⭐⭐⭐）

**推荐回答**：
"SQLite 允许注册自定义函数。我注册了一个 `cosine_similarity(blob, blob) -> real` 函数。

好处：
1. **零额外依赖**：不需要 pgvector、Qdrant 或任何向量数据库
2. **与 SQL 查询无缝集成**：`SELECT * FROM docs WHERE cosine_similarity(emb, ?) > 0.7`
3. **事务安全**：向量和元数据在同一个 SQLite 事务中更新

限制：
1. **全表扫描**：没有向量索引（HNSW/IVF），大数据量时性能下降
2. **内存**：所有向量需要在每次查询时加载到内存

对于个人工作空间规模（< 10 万文档），这些限制可以接受。如果未来需要规模化，架构上可以切换到 sqlite-vec 或 pgvector 而不影响上层 API。"

### Q5: wikilink 双向链接 BFS 是什么？（⭐⭐⭐）

**推荐回答**：
"PARA 笔记系统支持 `[[note name]]` 和 `[[note#heading]]` 这样的 wikilink 语法。当一个笔记 A 链接到笔记 B，B 自动获得一个指向 A 的反向链接。

实现：
1. 扫描所有笔记，提取 wikilink（正则匹配 `[[...]]`）
2. 构建有向图：A → B 表示 A 链接到 B
3. BFS 遍历：从任意笔记出发，发现所有可达笔记
4. 反向链接查询：`SELECT * FROM edges WHERE target_id = ?`

面试中可展示的深度：讨论 BFS 在大图上的内存优化（迭代加深 vs 全图遍历）、增量更新策略（只重扫描变化的笔记）。"

### Q6: 7 条架构守卫规则的来源？（⭐⭐⭐⭐）

**推荐回答**：
"这些规则来自项目开发过程中的实际教训：

- **RF-1（禁止硬编码路径）**：早期版本用 `dirs::data_local_dir()` 硬编码路径，导致测试互相污染、跨平台问题。改为 `StorageBackend` trait 注入
- **RF-3（Schema 单一真相源）**：有一次更新了迁移文件但忘记更新 `SCHEMA_DDL`，导致新数据库和迁移后的数据库结构不同。现在 CI 自动检测两者是否一致
- **RF-6（零 unwrap）**：上线初期有用户报告 panic，但堆栈信息不够定位问题。改为 `Result<T, E>` + `anyhow::Context` 后错误消息更明确

总结：每一条规则背后都有一次生产事故。这些规则是'工程债务的利息'——遵守需要额外投入，但不遵守的代价更大。"

---

## 3. 与 Clarity 的协同关系

**面试中如何讲好"两个项目互补"的故事**：

> "Clarity 和 Devbase 是一个生态中的两个组件。Clarity 是 Agent 运行时——它负责执行、推理、工具调用。Devbase 是上下文引擎——它告诉 Agent 你的工作空间里有什么。
>
> 具体场景：用户说'帮我查一下我们用了哪些数据库'。Agent（Clarity）调用 Devbase 的 MCP 工具 —— Devbase 扫描所有 repo 的 Cargo.toml，找到 rusqlite/sled/duckdb 等依赖，返回结构化结果 —— Agent 用自然语言总结给用户。
>
> 这两个项目证明了我有从底层存储（SQLite schema 设计）到上层 Agent 交互（对话引擎）的全栈系统设计能力。"

---

## 4. 技术深挖问题

### 深挖1：现场设计一个新的 MCP 工具

**提示**："如果让你给 Devbase 添加一个 '跨 repo 重构影响分析' 的 MCP 工具，怎么设计？"

**推荐回答要点**：定义输入（目标函数签名）、输出（影响范围报告）、索引策略（预计算 vs 实时查询）、与现有 dependency_graph 模块的关系。

### 深挖2：混合搜索的性能优化

**推荐回答要点**：Tantivy 查询优化（early termination）、两阶段检索（BM25 粗排 → 向量精排）、缓存热查询结果、增量索引策略。

---

## 5. 项目亮点量化话术

- **71 个 MCP 工具** — 覆盖仓库管理、代码分析、知识检索、笔记系统、技能执行、工作流编排
- **7 条架构守卫** — CI 强制执行，每次违规都被自动阻止
- **schema v36** — 36 次顺序迁移，零数据丢失，每次迁移前自动备份
- **零外部向量数据库** — 自定义 SQLite cosine_similarity UDF
- **~8.7MB 单二进制** — 包含全文搜索引擎、代码解析器、笔记系统、工作流引擎

---

## 6. 反问面试官

1. "团队目前如何管理 AI Agent 的上下文——有没有类似 Devbase 这种'工作空间感知'的需求？"
2. "你们内部工具链的集成程度如何？有没有标准化 Agent-工具接口（类似 MCP）的打算？"
3. "团队的技术债管理方式是什么——有没有架构守卫规则或者自动化质量检查？"
4. "如果我加入，第一个季度最可能参与的项目或者解决的技术挑战是什么？"
5. "团队在开发者工具领域的技术愿景是什么？"
6. "目前的 CI/CD pipeline 有哪些痛点？"
