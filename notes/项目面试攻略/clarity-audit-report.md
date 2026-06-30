# Clarity 模块权责审计报告

> 生成时间：2026-06-29
> 审计范围：`C:/Users/22414/dev/clarity/crates/*`
> 对比基准：`juice094/projects/clarity.md`
> 状态：已标记需修正项，待后续开发中解决

---

## 审计方法

- 读取各 crate 的 `Cargo.toml` 描述
- 检查 `src/` 目录结构和关键文件
- 搜索核心功能关键词（`sync`、`merge`、`CRDT`、`transport`、`plan`、`react`、`candle` 等）
- 对比 `projects/clarity.md` 的架构描述

---

## 高优先级问题（必须修正简历/文档）

### 1. `clarity-memory`：文档严重夸大

| 项目 | 内容 |
|:---|:---|
| **文档声称** | "记忆联邦与脱敏合并"、"断网后通过 delta merge 同步记忆增量"、"冲突时以高信任设备/最近修改为准" |
| **实际实现** | 纯本地存储层：SQLite / 文件 / hybrid 后端 + BM25/向量检索 + 语义去重 |
| **缺失** | 跨设备同步、CRDT、delta sync、隐私脱敏、冲突仲裁 |
| **风险** | **最高**。面试问 memory sync 细节会直接穿帮 |
| **代码证据** | `compiler.rs:34` 的 `MergeConfig` 是按 cosine similarity 做语义去重；`backends/hybrid.rs:27` 的 `sync_handle` 是本地缓存刷盘 |

**建议表述**：
> `clarity-memory` 负责本地记忆的存储、检索与生命周期管理，支持 SQLite + BM25 + embedding vector search；跨设备同步由 `clarity-claw` 的 mesh 层处理。

**后续开发方向**：
- 若要让文档描述成立，需在 `clarity-memory` 或 `clarity-claw` 中实现 memory-level 的 delta sync
- 脱敏合并需要引入 PII 检测/redaction/差分隐私机制

---

### 2. `clarity-claw`：承担核心分布式职责，但不在架构图里

| 项目 | 内容 |
|:---|:---|
| **文档位置** | 未出现在 `projects/clarity.md` 架构图中 |
| **实际实现** | 完整的 mesh 网络层：`mesh/merger.rs`、`mesh/transport.rs`、`mesh/gateway_transport.rs`、`mesh/syncthing_transport.rs`、`mesh/crypto.rs` |
| **核心算法** | `merger.rs`: event-id 去重 + `(origin_clock, event_id)` 全序 + LWW |
| **职责** | 设备发现、连接管理、网关传输、Syncthing 传输、角色上下文合并 |
| **风险** | **高**。真正的分布式同步层被文档遗漏，导致架构描述不完整 |
| **代码证据** | `clarity-claw/src/mesh/merger.rs:1-20` 明确写着 `CRDT merger for Claw Mesh role contexts` |

**建议动作**：
- 把 `clarity-claw` 加入 `projects/clarity.md` 架构图
- 明确说明它负责跨设备角色上下文同步，而不是 `clarity-memory`

---

### 3. "脱敏合并"：无代码支撑

| 项目 | 内容 |
|:---|:---|
| **文档声称** | "只把脱敏后的抽象记忆/结论/关系更新广播到网络" |
| **实际实现** | 在 `clarity-memory`、`clarity-claw`、`clarity-contract` 中均未找到脱敏/匿名化/redaction/privacy 相关实现 |
| **缺失** | 数据脱敏算法、PII 检测、差分隐私、访问控制 |
| **风险** | **高**。涉及隐私计算的声明没有证据 |

**建议动作**：
- 若未实现，删除"脱敏合并"表述
- 可改为"敏感数据默认保留在本地，跨设备同步由用户配置决定"（前提是有配置逻辑）

---

## 中优先级问题（需要补充证据或修正措辞）

### 4. `clarity-core` 的 ReAct + Plan：有代码，但量化指标待验证

| 项目 | 内容 |
|:---|:---|
| **文档声称** | "Plan mode: step-missing rate dropped from ~40% to near 0" |
| **代码支撑** | `agent/plan.rs`、`agent/driver.rs`、`agent/executor.rs`、`agent/run/` 等文件存在 |
| **待确认** | 40% 指标是否有测试集支撑？是自动评估还是人工标注？ |
| **风险** | **中**。数字很好，但面试会追问 methodology |

**建议动作**：
- 准备这个指标的测试方法说明
- 如果数字来自小样本或主观评估，简历上改为定性表述

---

### 5. `clarity-llm`：本地推理有实现，但 candle 角色不清

| 项目 | 内容 |
|:---|:---|
| **文档/依赖** | `Cargo.toml` 声明 `candle-core`、`candle-transformers`、`hf-hub`、`tokenizers` |
| **代码发现** | 存在 `kalosm.rs`、`local_gguf.rs`，支持本地 GGUF 模型 |
| **待确认** | candle 是否实际使用？kalosm 是否内部依赖 candle？ |
| **风险** | **中**。如果 candle 依赖未实际使用，属于冗余依赖 |

**建议动作**：
- 检查 `kalosm` 的依赖链
- 如果 candle 未直接使用，考虑从 `Cargo.toml` 移除或改为 optional

---

### 6. `clarity-mcp`：三种 transport 文件都在，完整度待验证

| 项目 | 内容 |
|:---|:---|
| **文档声称** | MCP triple-transport: stdio / SSE / WebSocket |
| **代码发现** | `enhanced/stdio.rs`、`enhanced/sse.rs`、`enhanced/websocket.rs` 都存在 |
| **待确认** | 是否完整实现 MCP protocol handshake？是否通过官方测试？ |
| **风险** | **中**。有文件不等于完整实现 |

---

## 低风险 / 待进一步审计

| Crate | 文档权责 | 初步观察 | 风险 |
|:---|:---|:---|:---|
| `clarity-contract` | 零依赖接口契约 | 有 `capability.rs`、`federation.rs`、`diff.rs` 等 | 低 |
| `clarity-tools` | 内置工具 | 有 file/search/shell/computer/channel 等工具 | 低 |
| `clarity-channels` | 多平台消息通道 | 有 WeChat/Telegram/Discord/Slack 相关代码 | 低 |
| `clarity-gateway` | HTTP/WebSocket server | 基于 Axum，代码较完整 | 低 |
| `clarity-subagents` | 并行子 Agent 编排 | 有 `parallel.rs`、`registry.rs`、`builder.rs` | 中 |
| `clarity-secrets` | ChaCha20-Poly1305 加密 | 依赖正确，代码结构清晰 | 低 |
| `clarity-wire` | 内部通信协议 | 代码很小，可能只是 channel 包装 | 中 |
| `clarity-telemetry` | metrics/traces/audit | 有 `tracing_layer.rs`、`audit.rs`、`sink.rs` | 低 |
| `clarity-mobile-core` | 移动端 FFI | 使用 UniFFI，有 `.udl` 文件 | 中 |
| `clarity-anthropic-proxy` | 反向代理 | 小工具，代码简单 | 低 |
| `clarity-openclaw` | OpenClaw gateway | 有 discovery/connection_manager | 低 |

---

## 修正优先级

### 立即做

1. 修改 `projects/clarity.md`：
   - 把 `clarity-claw` 加入架构图
   - 修正 `clarity-memory` 的描述为本地存储层
   - 删除或弱化"脱敏合并"、"记忆联邦"等无代码支撑的表述
   - 修正"delta merge 同步记忆增量"为"`clarity-claw` mesh 层同步角色上下文"

2. 准备面试防御：
   - 如果面试官问 memory sync，要能说清楚边界
   - 如果问 CRDT，要说明是 CRDT-inspired + LWW，不是严格 CRDT

### 本周做

3. 验证核心数字：
   - ReAct/Plan 40% 指标的测试方法
   - MCP 三种 transport 的完整度
   - candle 依赖是否实际使用

4. 清理冗余依赖：
   - 如果 candle 未使用，从 `clarity-llm/Cargo.toml` 移除

### 后续可选

5. 补齐架构文档：
   - 给 `clarity-claw` 写专门说明
   - 明确 memory / claw / wire 的分层边界
