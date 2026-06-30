# syncthing-rust 项目探索报告

> 生成时间：2026-06-29
> 探索目录：`C:/Users/22414/dev/syncthing-rust`
> 目标：为简历提供准确素材，并核对现有描述的真实性

---

## 1. 项目概览

| 维度 | 现状 |
|---|---|
| **一句话定位** | Syncthing BEP 协议的 Rust 实现，零运行时依赖、单静态二进制，与官方 Go Syncthing 守护进程线路兼容。 |
| **Workspace 成员** | **14 个**：9 个 library crate + 5 个 command/binary crate |
| **Rust 代码规模** | 约 **53K–54K 行**（library 约 39K 行，cmd 约 14K 行） |
| **源文件数** | 223 个 `.rs`/`.proto` 文件 |
| **当前测试基线** | **413 passed / 6 ignored / 0 failed**（单元+集成），另有 9 个 doc-test passed |
| **Release 二进制** | Windows 下 `syncthing.exe` 实测 **16 MB**（非 13 MB） |
| **当前版本** | v3.0.4 |

### Crate 清单与代码量

| 路径 | 角色 | 行数 |
|---|---|---:|
| `crates/bep-protocol` | BEP 协议编解码 + Hello/ClusterConfig/Index/Request/Response | 1,866 |
| `crates/syncthing-core` | 核心类型：DeviceId、FileInfo、VersionVector、错误类型 | 2,540 |
| `crates/syncthing-net` | TCP+TLS、ConnectionManager、拨号、发现、Relay、STUN、UPnP | 15,093 |
| `crates/syncthing-sync` | Scanner、Puller、IndexHandler、watcher、合并、冲突解决、编排器 | 9,283 |
| `crates/syncthing-fs` | 文件系统抽象、ignore、scanner、watcher | 2,969 |
| `crates/syncthing-db` | 元数据 + block-cache（sled） | 2,558 |
| `crates/syncthing-api` | REST API（Axum，Go-layout 兼容） | 4,394 |
| `crates/syncthing-versioner` | Simple / Staggered 版本归档 | 672 |
| `crates/syncthing-test-utils` | 测试工具、harness | 780 |
| `cmd/syncthing` | CLI + TUI + daemon + tray + monitor + stress_test | 12,896 |
| `cmd/syncthing-bench` | 同步基准测试 | 243 |
| `cmd/syncthing-cli` | 证书/ID/指标 CLI | 149 |
| `cmd/syncthing-mcp-bridge` | MCP stdio → REST 桥接 | 513 |
| `cmd/syncthing-tray` | Windows 系统托盘入口（薄 wrapper，61 行） | 61 |

---

## 2. 架构与 crate 职责

```
┌─────────────────────────────────────────────────────────────────┐
│  cmd/syncthing         CLI / TUI / daemon / tray / monitor      │
│  cmd/syncthing-*       bench / cli / mcp-bridge / tray          │
├─────────────────────────────────────────────────────────────────┤
│  crates/syncthing-api        REST API (Axum) + RBAC API keys    │
├─────────────────────────────────────────────────────────────────┤
│  crates/syncthing-sync       Scanner / Puller / IndexHandler      │
│                              Watcher / Merge / ConflictResolver   │
│                              FolderOrchestrator / HealthPredictor │
├─────────────────────────────────────────────────────────────────┤
│  crates/syncthing-fs         文件系统抽象、ignore、watcher        │
│  crates/syncthing-versioner  Simple / Staggered 版本归档        │
│  crates/syncthing-db         sled 元数据 + block cache            │
├─────────────────────────────────────────────────────────────────┤
│  crates/syncthing-net        TCP+TLS / ConnectionManager          │
│                              ParallelDialer / Relay v1            │
│                              STUN / UPnP / Local+Global Discovery │
├─────────────────────────────────────────────────────────────────┤
│  crates/bep-protocol         BEP codec (prost) + handshake        │
├─────────────────────────────────────────────────────────────────┤
│  crates/syncthing-core       DeviceId / FileInfo / Vector / Error │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 关键技术栈

| 技术 | 在项目中支撑的功能 | 证据路径 |
|---|---|---|
| **tokio** | 全异步运行时、并发调度、后台任务 | `Cargo.toml` workspace |
| **rustls / tokio-rustls** | BEP over TLS、Relay TLS、设备证书握手、ALPN `bep/1.0` / `bep-relay` | `crates/syncthing-net/src/tls.rs` |
| **ed25519-dalek** | ⚠️ 仅列在 `Cargo.toml`，**源码中未实际使用** | `Cargo.toml` 工作区依赖 |
| **rcgen** | 自签名证书生成 | `crates/syncthing-net/src/tls.rs:367` |
| **prost** | BEP protobuf 编解码 | `crates/bep-protocol/src/messages/mod.rs` |
| **lz4** | BEP 消息压缩 | `crates/syncthing-net/Cargo.toml` |
| **sled** | 元数据与 block cache 持久化 | `crates/syncthing-db/Cargo.toml` |
| **Axum / tower-http** | REST API、Prometheus `/metrics` | `crates/syncthing-api/Cargo.toml` |
| **notify** | 文件系统 watcher、增量扫描脏路径 | `crates/syncthing-sync/src/watcher.rs` |
| **sha2** | SHA-256 文件/块哈希、设备 ID 派生 | `crates/syncthing-sync/src/scanner.rs` |
| **rayon / num_cpus** | 并行扫描哈希 | `crates/syncthing-fs/Cargo.toml` |
| **igd** | UPnP/IGD 端口映射 | `crates/syncthing-net/src/upnp.rs` |
| **similar** | 文本三路合并 diff | `crates/syncthing-sync/src/merge.rs` |
| **dashmap / parking_lot** | 并发连接表、锁 | 多处 |

---

## 4. 关键技术点核实

### 4.1 BEP 协议 ✅ 已实现

- `bep-protocol` crate 完整实现 `Hello`、`ClusterConfig`、`Index`、`IndexUpdate`、`Request`、`Response`、`Ping`、`Close` 等消息类型。
- 使用 `prost` 编解码，字段 tag 与 Go `bep.pb.go` 对齐。
- 集成测试 `crates/bep-protocol/tests/wire_compat.rs` 验证 wire-format roundtrip。

### 4.2 rustls + 设备证书 ⚠️ 部分属实

- **rustls 真实使用**：`crates/syncthing-net/src/tls.rs` 配置 TLS，ALPN `bep/1.0`，自定义证书验证器。
- **设备 ID 派生**：从证书 DER 的 SHA-256 派生 DeviceId（`derive_device_id`）。
- **ed25519 不属实**：`ed25519-dalek` 仅列在 `Cargo.toml`，源码中**没有调用**。证书生成使用 `rcgen::KeyPair::generate()`，默认算法为 **ECDSA P-256**，不是 Ed25519。

### 4.3 预测性健康检查 ✅ 已实现

`cmd/syncthing/src/health_predictor.rs` 订阅同步事件，滑动窗口评估：
- 扫描/拉取失败率
- watcher 丢事件
- 文件夹状态翻转
- 增量扫描占比下降

并可对 `FolderOrchestrator` 进行 throttle 调节。

### 4.4 自适应并发控制 ✅ 已实现

`crates/syncthing-sync/src/puller/concurrency.rs` 实现 `ConcurrencyPolicy` + `RttTracker`：
- 根据 RTT 动态调整 downloads/blocks 并发档位（2/4 → 8/16）。
- 直连、Relay 有独立档位。
- 指数移动平均平滑 RTT。

### 4.5 NAT 穿透 / STUN / UPnP / Relay ✅ 已实现

| 能力 | 状态 | 证据 |
|---|---|---|
| **STUN** | ✅ | `crates/syncthing-net/src/stun/mod.rs`：完整 Binding Request/Response、XOR-MAPPED-ADDRESS、NAT 类型检测 |
| **UPnP** | ✅ | `crates/syncthing-net/src/upnp.rs`：基于 `igd` 发现网关、添加/移除 TCP/UDP 映射、自动续约 |
| **Relay v1** | ✅ | `crates/syncthing-net/src/relay/`：client/server/dial/pool/protocol，与 Go relay 互操作 |
| **本地发现** | ✅ | `crates/syncthing-net/src/discovery/local.rs`：UDP 广播 Announce |
| **全球发现** | ✅ | `crates/syncthing-net/src/discovery/global.rs`：HTTPS mTLS 向 global server 注册/查询 |

### 4.6 三路文本合并 / 版本归档 ✅ 已实现

- **三路合并**：`crates/syncthing-sync/src/merge.rs`，基于 `similar` diff，支持 git 风格冲突标记。
- **冲突解决**：`crates/syncthing-sync/src/conflict_resolver.rs`：版本向量不可比较时识别冲突，文本文件走 merge，二进制走 rename。
- **Simple 版本归档**：`crates/syncthing-versioner/src/simple.rs`，`.stversions/` 目录，保留 N 份。
- **Staggered 版本归档**：`crates/syncthing-versioner/src/staggered.rs`，4 个时间窗口（30s/1h/1d/1w）。

### 4.7 P2P 文件同步核心逻辑 ✅ 已实现

- **扫描器**：`crates/syncthing-sync/src/scanner.rs`：递归扫描、`.stignore`、SHA-256 分块（默认 128KB）、检测删除/修改/新增。
- **拉取器**：`crates/syncthing-sync/src/puller/mod.rs`：按块请求、并发下载、临时文件、版本归档、三路合并。
- **索引处理**：`crates/syncthing-sync/src/index_handler.rs`：处理远端 Index/IndexUpdate。
- **块服务**：`crates/syncthing-sync/src/block_server.rs`：响应远端块请求。
- **编排器**：`crates/syncthing-sync/src/orchestrator.rs`：多 folder 扫描/拉取并发控制、抖动、优先级。

---

## 5. 与现有简历描述的一致性检查

| 简历描述 | 核实结果 | 说明 |
|---|---|---|
| **"13 crates, ~58K 行"** | ❌ 不准确 | 实际是 **9 个 library crate + 5 个 cmd binary = 14 workspace 成员**；代码约 **53K–54K 行**。 |
| **"BEP 协议互操作"** | ✅ 有证据 | `crates/bep-protocol/tests/wire_compat.rs` 验证 wire format；README 称与 Go v2.1.0 互操作。 |
| **"rustls + ed25519 设备证书"** | ⚠️ 部分夸大 | **rustls 真实使用**；设备证书存在；但 **ed25519-dalek 源码中未使用**，证书生成实际用 rcgen 默认 ECDSA P-256。建议改为 **"rustls + 自签名设备证书"**。 |
| **"预测性健康检查"** | ✅ 有证据 | `cmd/syncthing/src/health_predictor.rs` 完整实现。 |
| **"自适应并发控制"** | ✅ 有证据 | `crates/syncthing-sync/src/puller/concurrency.rs` + `RttTracker`。 |
| **"三路文本合并与 Simple/Staggered 版本归档策略"** | ✅ 有证据 | `merge.rs` + `syncthing-versioner/src/{simple,staggered}.rs`。 |
| **"392 passed / 0 failed 测试基线"** | ⚠️ 数据过期 | 当前基线为 **413 passed / 6 ignored / 0 failed**（含 9 doc tests）。 |
| **"release 单二进制约 13 MB"** | ❌ 不准确 | Windows release `syncthing.exe` 实测 **16 MB**；README 同样写 ~13 MB，与事实不符。 |
| **"72h 耐久压测"** | ❌ 未完成 | 脚本 `scripts/churn_72h.ps1` 存在，但尚未完成。简历写"建立 72h 耐久压测"会误导为已完成。 |

---

## 6. 简历可用素材

### 6.1 可直接使用的项目 bullet points

1. **独立实现 Syncthing BEP 协议的 Rust 协议栈**：基于 `prost` 完成 Hello/ClusterConfig/Index/Request/Response 编解码，配套 `wire_compat` 集成测试验证与 Go Syncthing 的线路格式兼容。

2. **构建零运行时依赖的 P2P 文件同步守护进程**：设计 9 library crate + 5 command binary 的分层 Workspace，实现 scanner/puller/index-handler/block-server 全链路，覆盖块级拉取、SHA-256 校验、临时文件回滚与版本归档。

3. **实现多路径网络发现与中继回退**：集成 UDP 本地广播、HTTPS 全球发现、STUN 公网地址探测、UPnP 端口映射与 Relay Protocol v1，NAT 后无法直连时自动 fallback 到 relay。

4. **落地预测性健康检查与自适应拉取并发**：事件流趋势评估失败率、watcher 丢事件与状态翻转；`RttTracker` 根据链路 RTT 动态调整 downloads/blocks 并发档位。

5. **实现文本三路合并与 Simple/Staggered 版本归档**：基于 base/local/remote 的文本三路合并生成 git 风格冲突标记；版本归档支持 keep=N 与 4 时间窗口策略，解决双向同步冲突。

6. **维护生产级工程基线**：`cargo test --workspace` 413 passed / 6 ignored / 0 failed，Clippy `-D warnings`，结构化 JSON 日志、Prometheus `/metrics`、Windows 托盘与 TUI。

### 6.2 可放入"技术技能"的条目

- Rust 系统编程 / Cargo Workspace 治理
- Tokio 异步并发与后台任务调度
- BEP 协议与 P2P 文件同步机制
- rustls + 自签名设备证书 + TLS 双向认证
- STUN / UPnP / Relay v1 NAT 穿透与多路径发现
- 文件分块哈希（SHA-256）、增量扫描、watcher 事件驱动同步
- 文本三路合并与版本向量冲突检测
- Axum REST API / Prometheus 指标 / 结构化日志
- 预测性健康检查与自适应并发控制
- 零运行时依赖单二进制分发

### 6.3 需要谨慎表述或避免夸大的地方

| 问题 | 建议表述 |
|---|---|
| "13 crates" | 改为 **"9 个 library crate + 5 个命令二进制"** 或 **"14 workspace 成员"**。 |
| "~58K 行" | 改为 **"约 5.3 万行 Rust 代码"** 或按 library/cmd 拆分说明。 |
| "ed25519 设备证书" | 改为 **"rustls + 自签名设备证书"**；如确需提 ed25519，需先改造证书生成逻辑。 |
| "release 单二进制约 13 MB" | 改为 **"release 单二进制约 16 MB"**（Windows 实测），或去掉具体数字写"单二进制分发"。 |
| "392 passed / 0 failed" | 更新为 **"413 passed / 6 ignored / 0 failed"**。 |
| "72h 耐久压测" | 改为 **"设计 72h 耐久压测脚本与计划"**；不要写"完成"或"通过"。 |

---

## 7. 关键源码路径速查

| 技术点 | 路径 |
|---|---|
| BEP 消息定义 | `crates/bep-protocol/src/messages/mod.rs` |
| BEP 握手 | `crates/bep-protocol/src/handshake.rs` |
| BEP wire-compat 测试 | `crates/bep-protocol/tests/wire_compat.rs` |
| TLS / 设备证书 | `crates/syncthing-net/src/tls.rs` |
| 连接管理 / 竞争解决 | `crates/syncthing-net/src/manager/{mod.rs,handshake.rs}` |
| 并行拨号器 | `crates/syncthing-net/src/dialer/mod.rs` |
| STUN | `crates/syncthing-net/src/stun/mod.rs` |
| UPnP | `crates/syncthing-net/src/upnp.rs` |
| Relay v1 | `crates/syncthing-net/src/relay/{mod.rs,server.rs,dial.rs,pool.rs}` |
| 发现管理 | `crates/syncthing-net/src/discovery/mod.rs` |
| Scanner | `crates/syncthing-sync/src/scanner.rs` |
| Puller | `crates/syncthing-sync/src/puller/mod.rs` |
| 自适应并发 | `crates/syncthing-sync/src/puller/concurrency.rs` |
| 三路合并 | `crates/syncthing-sync/src/merge.rs` |
| 冲突解决 | `crates/syncthing-sync/src/conflict_resolver.rs` |
| Folder Orchestrator | `crates/syncthing-sync/src/orchestrator.rs` |
| Simple 版本归档 | `crates/syncthing-versioner/src/simple.rs` |
| Staggered 版本归档 | `crates/syncthing-versioner/src/staggered.rs` |
| 健康预测器 | `cmd/syncthing/src/health_predictor.rs` |
| 72h 压测脚本 | `scripts/churn_72h.ps1` |
