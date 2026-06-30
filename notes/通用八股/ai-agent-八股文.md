# AI Agent 面试八股文

> 候选人：周景潇 | 2026-06-27 | 独立开发 Clarity (AI Agent 运行时) + Devbase (AI 世界模型编译器)
> 求职方向：AI Agent 开发 / AI 应用开发
> 核心经验：MCP 协议全实现、ReAct/Plan Agent、RAG 混合搜索、Candle GGUF 本地推理

---

## 1. LLM 基础（必考）

### 1.1 Transformer 架构核心

**Self-Attention 计算**：
```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V

Q = X * W_q  (Query: 我要找什么)
K = X * W_k  (Key: 我有什么)
V = X * W_v  (Value: 我的内容)
```

**Multi-Head Attention**：多个 Attention 头并行计算，每个头关注不同的语义子空间（语法/语义/指代）。

**为什么除以 sqrt(d_k)**？防止点积过大导致 softmax 梯度消失。

**FFN（前馈网络）**：两层全连接 + 激活函数，增加非线性表达能力。

**Layer Normalization**：在特征维度（而非 batch 维度）归一化，稳定训练。

### 1.2 Tokenization

| 方法 | 原理 | 代表模型 |
|------|------|---------|
| BPE | 从字符开始，合并高频字符对 | GPT 系列 |
| SentencePiece | BPE/Unigram + 空格处理 | LLaMA, T5 |
| tiktoken | BPE 变体，速度优化 | OpenAI 模型 |

**面试要点**：Tokenization 影响 —— 中文 token 效率低于英文（一个汉字 = 1-2 token vs 一个英文词 = 1-3 token）、多语言、代码 tokenization 的质量直接影响推理效果。

### 1.3 Context Window

Attention 的复杂度是 O(n² * d)，n 是 token 数。长上下文的解决方案：
- **FlashAttention**：分块计算 + IO 优化，不改变复杂度但降低常数
- **RoPE**：旋转位置编码，扩展性好
- **Sliding Window**：限制注意力窗口
- **稀疏 Attention**：只计算部分位置

### 1.4 采样策略

| 策略 | 参数 | 效果 |
|------|------|------|
| **Temperature** | 0-2 | 越高越随机，越低越确定。0 = 贪婪 |
| **Top-k** | k=40/50 | 只从概率最高的 k 个 token 中采样 |
| **Top-p (Nucleus)** | p=0.9 | 累积概率达 p 的最小 token 集合中采样 |
| **Beam Search** | beam=4 | 保留 k 条最优路径，适合翻译等确定性任务 |

**面试要点**：Temperature=0 不完全确定性（硬件浮点差异），Top-p 比 Top-k 更灵活（词汇量不同时）。

---

## 2. Agent 架构（核心考点）

### 2.1 ReAct 模式

```
Loop:
  Thought: 分析当前状态，决定下一步
  Action: 调用工具或生成回复
  Observation: 观察工具结果
  → 回到 Thought
```

**关键特性**：
- 交错推理和行动，每一步根据上一步调整
- 适合探索性任务（不知道需要几步，每步依赖前步结果）
- 需要工具描述清晰、错误处理健壮

### 2.2 Plan-and-Execute vs ReAct

| 维度 | ReAct | Plan-and-Execute |
|------|-------|-----------------|
| 规划时机 | 逐步（每个 step 动态决策） | 预先（开始前生成完整计划） |
| 适应性 | 高（中间结果改变后续） | 低（计划固定，可重规划） |
| Token 消耗 | 更高（多次 LLM 调用） | 更低（一次规划 + 执行） |
| 适用场景 | 探索、调试、不确定性高 | 明确任务、可分解步骤 |
| 失败处理 | 立即调整 | 步骤失败 → 触发重规划 |

### 2.3 Tool Use / Function Calling

**工具描述格式（OpenAI 风格）**：
```json
{
  "type": "function",
  "function": {
    "name": "read_file",
    "description": "Read contents of a file",
    "parameters": {
      "type": "object",
      "properties": {
        "path": {"type": "string", "description": "File path"}
      },
      "required": ["path"]
    }
  }
}
```

**工具调用的完整流程**：
1. 用户输入 + 系统提示 + 工具列表 → 发送给 LLM
2. LLM 返回 tool_call（包含 function name + arguments JSON）
3. 框架解析 tool_call，路由到实际函数
4. 执行工具，获取结果
5. 将 tool_result 追加到对话历史 → 继续推理
6. 直到 LLM 返回最终文本回复（无 tool_call）

### 2.4 Multi-Agent 系统

**协作模式**：
- **顺序**：Agent A 输出 → Agent B 输入（流水线）
- **并行**：多个 Agent 同时工作不同子任务
- **辩论**：两个 Agent 从不同角度分析同一个问题，综合结论
- **层级**：Manager Agent 分配任务给 Worker Agents

**面试要点**：Multi-Agent 的核心挑战 —— 上下文传递（父子 Agent 的信息共享）、冲突解决（意见不一致时）、任务分解粒度、成本控制（N 个 Agent = N 倍 Token 消耗）。

### 2.5 Agent 记忆系统

**三层记忆模型**：
1. **短期记忆**：对话上下文窗口（自动管理，有长度限制）
2. **工作记忆**：scratchpad、中间计算结果（工具结果缓存）
3. **长期记忆**：向量存储（语义检索）+ 结构化存储（精确查询）

**上下文窗口管理**：
- 滑动窗口：丢弃最早的消息
- 分层摘要：旧消息 → 摘要压缩（通过 LLM）
- 关键信息提取：只保留决定性的信息

### 2.6 Agent 安全

- **Prompt Injection 防御**：用户输入和系统提示分层，工具调用参数白名单验证
- **工具沙盒**：文件操作限制目录、Shell 操作白名单命令
- **审批链**：关键操作（删除、推送、敏感 API 调用）需要人工确认
- **审计日志**：所有工具调用和决策可追溯

---

## 3. MCP 协议（候选人核心优势）

### 3.1 三大原语

| 原语 | 方向 | 用途 |
|------|------|------|
| **Tool** | Server → Client 描述，Client → Server 调用 | Agent 执行操作 |
| **Resource** | Server → Client | 暴露结构化数据（文件、数据库 schema） |
| **Prompt** | Server → Client | 预定义提示模板 |

### 3.2 传输层对比

| 传输 | 连接模型 | 延迟 | 适用场景 |
|------|---------|------|---------|
| **stdio** | 子进程 stdin/stdout | 最低 | 本地工具 |
| **SSE** | HTTP 长连接单向流 | 低 | 远程通知 |
| **HTTP** | 请求-响应 | 中 | 远程工具调用 |
| **WebSocket** | 双向持久连接 | 低 | 实时交互 |

### 3.3 MCP vs OpenAI Function Calling

| 维度 | MCP | OpenAI FC |
|------|-----|-----------|
| 标准化 | 是（跨模型、跨厂商） | 否（OpenAI 专有） |
| 工具发现 | 动态（list_tools） | 静态（启动时定义） |
| 资源暴露 | 支持（Resources） | 不支持 |
| 传输 | 多种 | 仅 HTTP |
| 生态 | 增长中 | 成熟（OpenAI 生态） |

---

## 4. RAG 检索增强生成（必考）

### 4.1 完整 Pipeline

```
文档 → 分块(Chunking) → 嵌入(Embedding) → 索引(Indexing)
                                              ↓
查询 → 嵌入 → 检索(Retrieval) → 重排序(Reranking) → 生成(Generation)
```

### 4.2 分块策略

| 策略 | 方法 | 适用场景 |
|------|------|---------|
| 固定大小 | N 字符/token 切割 | 通用，最简单 |
| 递归分割 | 按段落→句子→词 逐级切割 | Markdown/代码 |
| 语义分割 | 用 embedding 找语义边界 | 长文档 |
| HyDE | 生成假设答案再检索 | 提升召回率 |

### 4.3 BM25 + 向量混合搜索

候选人 Clarity 项目中的实践：
- **BM25**：处理精确关键词匹配（函数名、变量名、API 名称）
- **向量搜索**：处理语义相似（"数据库连接" ≈ "DB pool"）
- **RRF 融合**：`score(doc) = Σ 1/(60 + rank_i(doc))`

**面试要点**：为什么混合搜索优于纯向量？—— 向量搜索对罕见术语（API 名称）不敏感，BM25 可以弥补；纯 BM25 不懂同义词，向量可以弥补。

### 4.4 评估指标

| 指标 | 含义 |
|------|------|
| Hit Rate | 正确答案是否在检索结果中 |
| MRR | 第一个正确答案的平均排名倒数 |
| NDCG | 考虑排序位置的评分 |
| Faithfulness | 生成内容是否忠实于检索结果 |
| Answer Relevancy | 生成内容是否回答了问题 |

---

## 5. 本地推理（候选人的差异化优势）

### 5.1 GGUF 格式

GGUF 是量化后模型的文件格式，包含：模型架构定义 + 量化权重 + tokenizer 配置。一个文件即可加载完整的推理模型。

### 5.2 推理引擎对比

| 引擎 | 语言 | 特点 |
|------|------|------|
| llama.cpp | C++ | 最成熟，GGUF 标准制定者 |
| Candle | Rust | HuggingFace 出品，可嵌入 Rust 应用 |
| Ollama | Go | 封装 llama.cpp，HTTP API |
| vLLM | Python | 高吞吐，PagedAttention |

候选人选择 Candle 的理由：纯 Rust 嵌入，零 Python/外部进程依赖，`cargo build` 即可获得推理能力。

### 5.3 量化技术

| 方法 | 精度 | 模型大小（相对 FP16） |
|------|------|---------------------|
| INT8 | 接近无损 | 50% |
| INT4 (GGML) | 轻微损失 | 25% |
| GPTQ | 有校准数据时效果好 | 25% |
| AWQ | 保护关键权重 | 25% |

---

## 6. AI 应用工程化

### 6.1 Token 预算控制

候选人实践：per-turn + daily 双重预算。达到上限后 Agent 强制总结当前进度并停止推理。

### 6.2 速率限制

- **Token Bucket**：固定速率补充 token，突发可消耗桶内积累
- **指数退避**：429 错误后延迟 1s → 2s → 4s → 8s ... 重试

### 6.3 Provider 网格

- 负载均衡：最少 pending 请求优先
- 熔断：连续失败 N 次 → 移出池 → 冷却后重试
- 自适应路由：简单任务（本地模型/廉价 API）→ 复杂任务（高端模型）

---

## 7. 开放性问题

### 设计一个 AI 代码审查系统

要点：
1. 代码解析（tree-sitter AST 提取）
2. 变更分析（git diff → 结构化变更）
3. 审查维度：正确性、安全、性能、风格
4. 多 Agent 并行审查（各自不同维度）
5. 结果聚合和优先级排序

### Agent 安全防护

要点：
1. 输入层：用户输入和系统提示分层，Prompt Injection 检测
2. 工具层：参数白名单、路径沙盒、权限最小化
3. 输出层：敏感信息过滤
4. 审计层：全链路日志

---

## 8. 面试深水区追问（2026高频）

### Q: Agent 如何评估自己工具调用的质量？

在 Clarity 中，每个工具调用后被评估三个维度——1) 是否解决了当前子问题（LLM self-evaluation）；2) 是否有更好的工具可替代（tool suggestion 机制）；3) 调用是否产生副作用（写入操作标记，触发审批升级）。连续 3 次低质量工具调用触发策略降级——从 Yolo 降到 Smart 模式。

### Q: 如何设计一个不依赖具体 LLM 的 Agent 框架？

Contract-First 设计——定义抽象的 `LlmProvider` trait，Agent 循环只依赖 trait 接口。在 Clarity 中切换 OpenAI 到 Anthropic 只需改变 provider 配置，Agent 逻辑零改动。关键抽象点：chat/stream/token_count/model_info 四个核心能力。

### Q: 多 Agent 系统中如何防止信息污染和上下文爆炸？

三重隔离：1) 每个 sub-agent 有独立上下文窗口，不共享对话历史；2) sub-agent 完成后输出结构化摘要而非完整对话；3) 父 Agent 决定信息路由，类似 TCP/IP 路由层。

### Q: 如何处理 Agent 的过度自信问题？

四层防御：1) 置信度校准（high/medium/low 标注）；2) 交叉验证（Multi-Agent debate）；3) 人类回路（高风险操作强制审批）；4) 事后审计（全链路可追溯）。

---

## 9. MCP 协议深度问题

### Q: MCP 的 security model 和 OAuth 有什么不同？

MCP auth 基于 capability——server 声明它提供哪些 tools/resources/prompts，client 获取能力列表。OAuth 是 scope-based（你能访问什么API），MCP 更细粒度——一个 tool 就是一个能力单元。

### Q: 为什么 MCP 设计了三种 primitive 而非只有 Tool？

Tool = Agent主动调用（动作），Resource = Agent被动访问（数据），Prompt = Agent获取模板（指导）。三者对应 Agent 的三种信息需求：执行能力、上下文数据、行为规范。

### Q: MCP stdio 传输的消息边界如何定义？

基于 JSON-RPC 2.0 的换行符分隔（newline-delimited JSON）。实际实现中需处理：1) 消息跨多个 read buffer；2) 空消息过滤；3) 超长消息截断保护。Clarity 中使用 BufReader + read_line 逐行处理。

---

## 10. RAG 系统评估与调优速查

| 问题 | 症状 | 诊断 | 修复 |
|------|------|------|------|
| 检索不到相关文档 | Hit Rate 低 | 检查 embedding 模型 | 切换 domain-specific embedding |
| 检索到不相关文档 | Precision 低 | 检查 BM25 权重 | 调整 RRF 融合权重 |
| 生成与检索无关 | Faithfulness 低 | 检查 prompt 约束 | 强化引用要求 |
| 上下文过长 | Token 溢出 | 检查 chunk size | 减小 chunk 或分层摘要 |
| 多语言效果差 | 非英文 Hit Rate 低 | 检查 tokenizer 语言覆盖 | 使用多语言 embedding（BGE-M3） |

---

## 11. 候选人 AI Agent 项目面试展示清单

| 展示点 | 项目 | 话术关键句 |
|--------|------|-----------|
| Agent 双模式 | Clarity | "ReAct 适合探索，Plan 适合结构化——通过任务复杂度自动选择" |
| MCP 四传输全实现 | Clarity | "国内最早系统性实现 MCP 四传输的实践者之一" |
| BM25+向量混合 | Clarity | "不用向量数据库，用 SQLite UDF 零拷贝实现语义搜索" |
| 四级记忆压缩 | Clarity | "模仿人脑记忆模型——工作记忆→短期→长期→事实" |
| Provider 网格 | Clarity | "6 Provider + 熔断 + 自适应路由——服务网格的 LLM 版本" |
| 71 MCP 工具 | Devbase | "7条架构红线保证工具质量和幂等性" |
| RAG 实证研究 | acr-select | "7模型×4架构×3000样本——用数据指导系统设计" |

---

## 12. 热门开放性问题参考回答

### 设计一个支持多轮对话的 AI 客服 Agent

1. 意图识别层：NLU 提取用户意图和实体
2. 对话管理层：状态机管理流程（问候→信息收集→解决→确认→结束）
3. 知识检索层：RAG 检索产品文档+FAQ+历史工单
4. 工具调用层：查订单（API）、退款（需审批）、转人工（Handoff）
5. 记忆层：短期（本轮对话）+ 长期（用户画像+历史）
6. 安全层：敏感信息脱敏、操作二次确认、审计日志

### Agent 如何从单步任务进化到多步复杂任务

关键变化：1) 从函数调用到 Plan-and-Execute——先分解再执行；2) 从无状态到有状态——需追踪中间结果和子任务状态；3) 从容错到鲁棒——单步失败不导致整体失败，需重试/重规划；4) 从同步到异步——长任务需后台执行+进度通知；5) 从单 Agent 到 Multi-Agent——不同阶段可能需要不同专业 Agent。在 Clarity 中通过 `agent/jumpy/` 模块实现 Plan 模式状态机追踪，每个子步骤有 pending/running/success/failed 四种状态。
