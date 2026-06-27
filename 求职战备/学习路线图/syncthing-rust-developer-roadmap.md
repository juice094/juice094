# Syncthing-rust 开发者学习路线图

> **目标读者**：有 Rust 基础，对 P2P 协议和分布式文件同步感兴趣的开发者
> **项目规模**：13 workspace crates + 4 binaries，~58K 行 Rust，392 测试，v3.0.3
> **预计总学习时间**：入门 2 周 → 进阶 4 周 → 精通 8 周

---

## 1. 前置知识要求

### 1.1 Rust 基础

| 技能 | 要求等级 | 在项目中的体现 |
|------|---------|---------------|
| async/await + tokio | ⭐⭐⭐⭐⭐ | 数千并发连接管理、BepSession 状态机 |
| trait 系统 | ⭐⭐⭐⭐⭐ | SyncModel/FileSystem/BlockStore/ConnectionManager 等核心 trait |
| 错误处理 | ⭐⭐⭐⭐ | 零 unwrap 策略，thiserror/anyhow |
| rayon 并行 | ⭐⭐⭐⭐ | SHA-256 并行文件扫描 |
| prost/protobuf | ⭐⭐⭐ | BEP 消息编解码 |

### 1.2 领域知识

| 领域 | 重要程度 | 学习资源 |
|------|---------|---------|
| P2P 协议设计（BEP/BitTorrent） | ⭐⭐⭐⭐⭐ | Syncthing 官方 spec |
| TLS 1.3 + 密码学基础 | ⭐⭐⭐⭐⭐ | rustls/ring 文档 |
| NAT 穿透（STUN/TURN/ICE/UPnP） | ⭐⭐⭐⭐ | RFC 5389/5766/8445 |
| 文件系统 | ⭐⭐⭐ | OS 文件系统基础 |
| 冲突解决算法 | ⭐⭐⭐ | three-way merge (similar crate) |

### 1.3 开发环境

```bash
git clone https://github.com/juice094/syncthing-rust
cd syncthing-rust
cargo test --workspace          # 392 tests 应全部通过
cargo clippy --workspace --all-targets -- -D warnings
just check                      # 完整质量门禁
```

---

## 2. 架构总览

```
cmd/syncthing (主二进制)
    ↓ 依赖
┌─────────────────────────────────────────────┐
│  syncthing-api (REST + EventBus)            │
│  syncthing-net (TCP+TLS, Discovery, Relay)  │
│  syncthing-sync (Scanner, Puller, Folder)   │
│  syncthing-db (sled KV, Block Cache)        │
│  syncthing-fs (FileSystem trait)            │
│  syncthing-versioner (Simple/Staggered)     │
│  bep-protocol (Protobuf codec)              │
│  syncthing-core (traits + types) ← 叶子crate│
└─────────────────────────────────────────────┘
```

**核心设计原则**：syncthing-core 零内部依赖，所有 crate 通过 trait 解耦，零运行时依赖的静态二进制（~13MB）。

---

## 3. 阶段一：协议基础（⭐⭐ | 3-5 天）

### 3.1 syncthing-core（叶子 crate）

路径：`crates/syncthing-core/src/lib.rs`

关键类型：
```rust
// 设备身份
struct DeviceId([u8; 32]);  // SHA-256 of Ed25519 public key

// 文件信息
struct FileInfo {
    name: String,
    size: u64,
    blocks: Vec<BlockInfo>,  // 每个块的 SHA-256
    modified_s: i64,
}

// 核心 trait
trait SyncModel { /* ... */ }
trait FileSystem { /* ... */ }
trait BlockStore { /* ... */ }
trait ConnectionManager { /* ... */ }
```

### 3.2 bep-protocol（BEP 消息编解码）

路径：`crates/bep-protocol/src/`

**BEP 消息流**：
```
Device A                          Device B
   |                                 |
   |---- Hello (device_id) --------->|
   |<--- Hello (device_id) ----------|
   |                                 |
   |---- ClusterConfig (folders) --->|
   |<--- ClusterConfig (folders) ----|
   |                                 |
   |<--- Index (file list) ----------|
   |---- Index (file list) --------->|
   |                                 |
   |---- Request (block hashes) ---->|
   |<--- Response (block data) ------|
   |                                 |
   |<--- Request (block hashes) -----|
   |---- Response (block data) ----->|
```

**为什么 Protocol Buffers 而非 JSON/MessagePack？**
- 与 Go Syncthing 的线级兼容要求
- Protobuf 的向后兼容性保证
- 二进制编码比 JSON 更紧凑（节省 P2P 带宽）

**学习重点**：`Hello`, `ClusterConfig`, `Index`, `Request`, `Response` 五种消息的字段含义和序列化/反序列化。

---

## 4. 阶段二：网络安全层（⭐⭐⭐⭐ | 5-7 天）

### 4.1 TLS 1.3 设备身份

```rust
// 设备身份从 Ed25519 密钥对派生
let key_pair = Ed25519KeyPair::generate();
let cert = generate_self_signed_cert(&key_pair);
let device_id = DeviceId::from_public_key(key_pair.public_key());
// device_id 是 SHA-256(public_key) 的 base32 编码
```

**mTLS 双向认证**：连接双方都验证对方的证书和设备 ID 是否匹配。

### 4.2 ConnectionManager

路径：`crates/syncthing-net/src/manager/`

```rust
struct ConnectionManager {
    pool: HashMap<DeviceId, Connection>,
    dialer: ParallelDialer,       // 并行尝试多个地址
    address_scorer: AddressScorer, // 地址评分和排序
    reconnect_policy: ReconnectPolicy,
}
```

**连接建立流程**：
1. 从 Discovery 获取对端地址列表
2. 并行 dial 所有地址（ParallelDialer）
3. 第一个成功的连接获胜
4. TLS 握手 + 设备 ID 验证
5. 加入连接池

### 4.3 四种发现机制

| 机制 | 实现 | 适用场景 |
|------|------|---------|
| **LAN UDP 广播** | 255.255.255.255:21027 | 局域网自动发现 |
| **Global HTTPS mTLS** | discovery.syncthing.net | 广域网设备发现 |
| **STUN** | RFC 5389 | 获取公网地址 |
| **UPnP/PMP** | IGD 协议 | NAT 端口映射 |

### 4.4 NAT 穿透

```rust
// NAT 穿透组合策略
impl DiscoveryService {
    async fn discover(&self) -> Vec<SocketAddr> {
        let mut addrs = Vec::new();
        
        // 1. 本地发现 (LAN)
        addrs.extend(self.local_discovery().await);
        
        // 2. STUN 获取公网地址
        if let Some(public) = self.stun_query().await {
            addrs.push(public);
        }
        
        // 3. UPnP 端口映射
        if let Some(mapped) = self.upnp_map_port().await {
            addrs.push(mapped);
        }
        
        // 4. Global 发现服务器
        addrs.extend(self.global_discovery().await);
        
        addrs
    }
}
```

**阶段二练习**：
```bash
cargo test -p syncthing-net
cargo run --release -- init
cargo run --release -- devices list
```

---

## 5. 阶段三：同步引擎（⭐⭐⭐⭐⭐ | 7-10 天）

### 5.1 Scanner（文件扫描 + SHA-256）

路径：`crates/syncthing-sync/src/scanner/` + `crates/syncthing-fs/src/scanner/`

```
遍历文件夹
    ↓
对每个文件:
  ├─ 检查 .stignore
  ├─ 读文件内容
  ├─ 分块 (默认 128KB)
  ├─ SHA-256 每个块 (rayon 并行)
  └─ 生成 FileInfo { blocks: Vec<BlockInfo> }
```

**性能要点**：rayon 多线程并行计算 SHA-256，在 SSD 上可达到接近磁盘读取速度的扫描吞吐。

### 5.2 Puller（块请求 + 文件组装）

路径：`crates/syncthing-sync/src/puller/`

```
对比本地和远程 Index
    ↓
找出缺失的块
    ↓
发送 Request (block_hashes)
    ↓
接收 Response (block_data)
    ↓
验证 SHA-256 → 写入临时文件 → 原子重命名
```

**自适应并发控制**：
```rust
struct ConcurrencyPolicy {
    max_concurrent_requests: usize,
    rtt_tracker: RttTracker,  // 根据 RTT 调整并发数
}

impl ConcurrencyPolicy {
    fn adjust(&mut self, rtt: Duration) {
        if rtt < Duration::from_millis(50) {
            self.max_concurrent_requests = 16;  // 低延迟，高并发
        } else {
            self.max_concurrent_requests = 4;   // 高延迟，减少并发
        }
    }
}
```

### 5.3 冲突解决（三路合并）

路径：`crates/syncthing-sync/src/conflict_resolver.rs`

基于 `similar` crate 的三路文本合并：
```
Base (共同祖先):  Line 1\nLine 2\nLine 3
Local:           Line 1\nLine 2 modified\nLine 3
Remote:          Line 1\nLine 2\nLine 3 remote addition

Merge Result:    Line 1\nLine 2 modified\nLine 3 remote addition
```

如果三路合并失败 → 保留两个版本：`file.sync-conflict-<date>-<time>.<ext>`

### 5.4 FolderModel 和 FolderOrchestrator

```rust
struct FolderModel {
    folder_id: String,
    local_index: Index,   // 本地文件状态
    remote_indices: HashMap<DeviceId, Index>,  // 各远程设备的状态
}

struct FolderOrchestrator {
    folders: HashMap<String, FolderModel>,
    concurrency_policy: ConcurrencyPolicy,
    // 多文件夹的调度和资源分配
}
```

---

## 6. 阶段四：存储与 API（⭐⭐⭐ | 3-5 天）

### 6.1 syncthing-db（sled 存储）

路径：`crates/syncthing-db/src/`

**为什么选 sled 而非 SQLite/RocksDB？**
- sled 是纯 Rust 实现，零 C 依赖
- B+Tree 结构 + COW（Copy-on-Write）事务
- 嵌入式场景下性能优于 SQLite
- 但 sled 已停止维护，未来可能迁移到 redb 或 libsql

```rust
struct SledStore {
    db: sled::Db,
    block_cache: LruCache<BlockHash, Vec<u8>>,
}
```

### 6.2 syncthing-api（REST API）

路径：`crates/syncthing-api/src/rest/`

与 Go Syncthing API 布局兼容：
```
GET    /rest/config          配置管理
GET    /rest/db/status       数据库状态
GET    /rest/device/stats    设备统计
GET    /rest/folder/stats    文件夹统计
GET    /rest/system/status   系统状态
GET    /rest/events          SSE 事件流
```

### 6.3 syncthing-versioner（文件版本控制）

路径：`crates/syncthing-versioner/src/`

**Simple**：保留最近 N 个版本
```rust
struct SimpleVersioner { keep: usize }
// files/ → .stversions/file~20260627-120000
```

**Staggered**：按时间窗口保留
```
最近 30 天：每小时保留一个版本
30-365 天前：每天保留一个版本
1 年以上：每周保留一个版本
```

---

## 7. 阶段五：TUI 与系统托盘（⭐⭐⭐ | 3-4 天）

### 7.1 TUI 仪表盘

路径：`cmd/syncthing/src/tui/`

实时显示同步状态：文件夹列表、传输进度、设备连接状态、事件日志

### 7.2 系统托盘（Windows only）

路径：`cmd/syncthing/src/tray.rs`

功能：托盘图标状态指示 + 右键菜单（启动/停止/退出）+ 状态变化通知

---

## 8. 阶段六：工程质量（⭐⭐⭐ | 2-3 天）

### 零运行时依赖策略
- rustls（非 OpenSSL）：Rust 原生 TLS，零 C 依赖
- sled（非 RocksDB）：Rust 原生存储
- 单静态二进制 ~13MB（release + LTO + single codegen unit）

### 测试策略
```bash
cargo test --workspace           # 392 单元测试
cargo test --release -p syncthing --test e2e_sync  # E2E 同步测试
cargo test --workspace --all-features  # 全特性测试
```

### CI Pipeline（12 jobs）
fmt → clippy (ubuntu/windows/macos) → test → audit → cargo-deny → e2e → bench → release-check → doc-check

---

## 9. 源码阅读顺序

**第一优先**（协议 + 类型）：
1. `Cargo.toml` — workspace 结构
2. `crates/syncthing-core/src/lib.rs` — 核心 trait 和类型
3. `crates/bep-protocol/src/` — BEP 消息格式
4. `crates/syncthing-net/src/manager/` — 连接管理
5. `crates/syncthing-net/src/session/` — BepSession 状态机

**第二优先**（同步逻辑）：
6. `crates/syncthing-sync/src/scanner/` — 文件扫描
7. `crates/syncthing-sync/src/puller/` — 块拉取
8. `crates/syncthing-sync/src/folder_model/` — 文件夹模型
9. `crates/syncthing-sync/src/orchestrator/` — 多文件夹调度
10. `crates/syncthing-sync/src/conflict_resolver.rs` — 冲突解决

**第三优先**（外围）：
11. `crates/syncthing-db/src/` — sled 存储
12. `crates/syncthing-api/src/rest/` — REST API
13. `crates/syncthing-versioner/src/` — 版本控制
14. `cmd/syncthing/src/tui/` — TUI
15. `justfile` — 构建脚本

---

## 10. 实践练习路线

### 入门
- [ ] 搭建双节点测试环境（两台电脑或 VM）
- [ ] 用 init 命令配置第一个文件夹同步
- [ ] 理解 BEP 消息流（Wireshark 抓包分析）
- [ ] 理解 Hello/ClusterConfig/Index/Request/Response 五种消息

### 进阶
- [ ] 添加一个新字段到 ClusterConfig 消息（protobuf 修改流程）
- [ ] 实现一个新的版本控制策略（如 TimeBased rotation）
- [ ] 添加日志埋点追踪一次完整同步
- [ ] 修改 ConcurrencyPolicy 参数并 benchmark 对比

### 精通
- [ ] 实现一个新的发现机制（如 mDNS）
- [ ] 实现一个新的传输层插件
- [ ] 优化块请求的调度算法
- [ ] 实现增量同步优化（只传变更的块）

### 贡献级
- [ ] 修复 KNOWN_ISSUES.md 中的 bug
- [ ] 编写 E2E 测试覆盖新场景
- [ ] 提交包含测试+benchmark 的 PR
- [ ] 改进 syncthing-net 的重连策略

---

## 11. 面试深度参考

### BEP 协议设计
**Q**: 为什么 Syncthing 使用自定义 BEP 而非 BitTorrent 协议？
**A**: BitTorrent 是为只读内容分发设计的（swarm 共享同一内容），Syncthing 需要双向同步（每个设备既是 seeder 又是 leecher）。BEP 在此基础上扩展了 Index 交换和双向 Request/Response。

### TLS 设备身份
**Q**: 为什么 Ed25519 而非 RSA？
**A**: Ed25519 密钥更短（32 bytes vs 2048 bits），签名更快，安全级别相当。在 P2P 场景中，设备 ID 需要频繁交换和验证，短密钥优势明显。

### 块级同步
**Q**: 块大小如何选择？128KB vs 1MB 的 trade-off？
**A**: 小块的 dedup 效果好但元数据开销大；大块元数据开销小但重传浪费多。128KB 是经验上的平衡点 — 与 Syncthing 的 Go 版本保持一致确保线级兼容。

### sled 持久化
**Q**: sled 的事务模型和 WAL 有什么不同？
**A**: sled 使用 COW (Copy-on-Write) B+Tree，写入时复制修改的节点，旧版本可并发读取。相比 SQLite WAL，sled 的 COW 更适合读多写少的元数据场景。

### 零运行时依赖
**Q**: ~13MB 的二进制如何做到？
**A**: rustls (非 OpenSSL) + sled (非 RocksDB) + LTO + single codegen unit + strip symbols。

---

## 附录：关键文件索引

```
syncthing-rust/
├── Cargo.toml / justfile / CLAUDE.md / AGENTS.md
├── crates/
│   ├── syncthing-core/src/lib.rs          # 核心 trait + 类型
│   ├── bep-protocol/src/                  # BEP Protobuf
│   ├── syncthing-net/src/manager/         # 连接管理
│   ├── syncthing-net/src/session/         # BepSession
│   ├── syncthing-sync/src/scanner/        # 文件扫描
│   ├── syncthing-sync/src/puller/         # 块拉取
│   ├── syncthing-sync/src/folder_model/   # 文件夹模型
│   ├── syncthing-sync/src/orchestrator/   # 多文件夹调度
│   ├── syncthing-sync/src/conflict_resolver.rs
│   ├── syncthing-db/src/                  # sled 存储
│   ├── syncthing-fs/src/                  # 文件系统抽象
│   ├── syncthing-api/src/rest/            # REST API
│   └── syncthing-versioner/src/           # 版本控制
├── cmd/syncthing/src/
│   ├── main.rs / tui.rs / tray.rs
├── docs/design/topology.md                # 权威拓扑
├── docs/reports/BASELINE_*.md             # 性能基线
```

---

> **下一步**：阅读 [`syncthing-rust-interview-guide.md`](../项目面试攻略/syncthing-rust-interview-guide.md) 进行面试模拟。
