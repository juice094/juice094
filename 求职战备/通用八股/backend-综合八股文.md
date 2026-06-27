# 后端综合八股文（数据库 + 网络 + 操作系统）

> 候选人：周景潇 | 数据科学专业 | 熟悉 SQLite/PostgreSQL/Redis/Tantivy/sled
> 求职方向：AI Agent 开发 / 后端开发

---

## 一、数据库核心

### 1. ACID 事务

| 特性 | 含义 | 违反场景 |
|------|------|---------|
| **A**tomicity | 要么全做，要么全不做 | 转账一半崩溃 |
| **C**onsistency | 事务前后数据完整性约束不变 | 外键约束违反 |
| **I**solation | 并发事务互不干扰 | 脏读/不可重复读/幻读 |
| **D**urability | 提交后数据永久保存 | 数据库崩溃丢数据 |

### 2. 索引

**B+Tree 索引**：所有数据在叶子节点，内部节点只存 key。叶子节点链表连接 → 范围查询 O(log N + K)。

**覆盖索引**：查询列全在索引中，不需要回表（Using index）。

**联合索引最左前缀**：INDEX(a, b, c) → 能命中 WHERE a=? 和 WHERE a=? AND b=?，不能命中 WHERE b=? 或 WHERE c=?。

**索引下推（ICP）**：MySQL 5.6+，把 WHERE 条件下推到存储引擎层过滤，减少回表次数。

### 3. JOIN 算法

| 算法 | 原理 | 适用 |
|------|------|------|
| Nested Loop | 外层每行扫内层 | 小表驱动大表 |
| Hash Join | 小表建哈希，大表探测 | 等值连接，无索引 |
| Merge Join | 两表按 JOIN key 排序后合并 | 有索引/已排序 |

### 4. 数据库锁

- **行锁**（Record Lock）：锁索引记录
- **间隙锁**（Gap Lock）：锁索引间隙，防幻读（MySQL RR 级别）
- **Next-Key Lock** = Record + Gap，MySQL 默认
- **意向锁**：表级锁的快速判断（有不兼容时不需要遍历所有行锁）

### 5. WAL（Write-Ahead Log）

写入流程：数据修改 → 先写 WAL → 再修改数据页 → Checkpoint 时将 WAL 刷到数据文件。崩溃恢复：重放 WAL 中未 checkpoint 的记录。

**为什么需要 WAL**？直接写数据页是随机写（慢），WAL 是顺序追加（快）。WAL 将随机写转为顺序写。

### 6. SQLite 特殊性

- **嵌入式**：库文件编译进应用，无独立服务进程
- **单写者**：任意时刻只有一个写事务（WAL 模式下可并发读）
- **WAL 模式**：写 WAL 文件 + 读原始数据库 → 读写并发。非 WAL 模式读写互斥
- **适用场景**：移动端、桌面应用、嵌入式设备、个人工具。不适合高并发 Web 服务

### 7. PostgreSQL vs MySQL

| 维度 | PostgreSQL | MySQL |
|------|-----------|-------|
| MVCC | 多版本行 + XID | Undo log + Read View |
| 索引 | B-Tree, Hash, GIN, GiST, BRIN, SP-GiST | B+Tree, Hash, Full-text, Spatial |
| 扩展 | 自定义类型/函数/语言/索引 | 插件化存储引擎 |
| JSON | JSONB 原生高效 | JSON 函数 |
| 复制 | 流复制，逻辑复制 | 异步/半同步复制 |
| 适用 | 复杂查询、分析、GIS | 简单读写、Web 应用 |

### 8. Redis

**数据结构速查**：
- **String**：缓存/计数器/分布式锁
- **Hash**：对象属性存储
- **List**：消息队列（LPUSH/RPOP）
- **Set**：去重集合、交集/并集
- **ZSet**：排行榜（score 排序）
- **Stream**：持久化消息队列（类似 Kafka 轻量版）

**持久化**：
- **RDB**：定期全量快照。恢复快，可能丢失最近数据
- **AOF**：追加每条写命令。数据安全，恢复慢，文件大
- **混合**：Redis 5.0+ 支持

**淘汰策略**：noeviction / allkeys-lru / volatile-lru / allkeys-lfu / volatile-lfu / volatile-ttl / allkeys-random

### 9. 缓存与数据库一致性

**Cache-Aside 模式**：读 cache miss → 读 DB → 写 cache / 写 DB → 删 cache

**延迟双删**：写 DB 前删 cache → 写 DB → 延迟 N ms → 再删 cache（防止并发读回写脏数据）

### 10. sled（Rust 嵌入式 KV）

- **数据结构**：COW B+Tree（Copy-on-Write）
- **事务**：乐观并发，写时复制节点
- **适用**：读多写少、元数据存储
- **状态**：已停止维护，替代方案 redb / libsql

---

## 二、网络协议

### 1. TCP 三次握手

```
Client                    Server
  |--- SYN (seq=x) ------->|
  |<-- SYN+ACK (x+1,y) ---|
  |--- ACK (y+1) -------->|
```

**为什么三次不是两次？** — 防止历史连接。如果网络中有延迟的旧 SYN，两次握手会导致 Server 为无效连接分配资源。第三次握手让 Client 确认连接有效。

### 2. TCP 四次挥手

```
Client                    Server
  |--- FIN (seq=u) ------->|  (Client: 我不发了)
  |<-- ACK (u+1) ----------|
  |<-- FIN (seq=v) --------|  (Server: 我也不发了)
  |--- ACK (v+1) -------->|  (TIME_WAIT 2MSL)
```

**为什么 TIME_WAIT 2MSL？** — 确保最后的 ACK 到达 Server（如果丢失，Server 重发 FIN）；让旧连接的所有报文在网络中消失。

### 3. TCP 拥塞控制

**慢启动**：cwnd 从 1 MSS 开始，每 RTT 翻倍。**拥塞避免**：达到 ssthresh 后线性增长。**快速重传**：收到 3 个重复 ACK 立即重传。**快速恢复**：不降到慢启动，而是降到新 ssthresh。

### 4. HTTP 版本对比

| 版本 | 连接 | 队头阻塞 | 特点 |
|------|------|---------|------|
| HTTP/1.1 | 持久连接 + 管线化 | 有（HTTP 层） | 顺序处理 |
| HTTP/2 | 单连接多路复用 | 有（TCP 层） | 二进制帧、HPACK、Server Push |
| HTTP/3 | QUIC (UDP) | 无 | 0-RTT、连接迁移 |

### 5. TLS 1.3 握手

```
Client                                    Server
  |-- ClientHello (keyshare) ----------->|
  |<-- ServerHello (keyshare) -----------|
  |    {EncryptedExtensions}             |
  |    {Certificate}                     |
  |    {CertificateVerify}               |
  |    {Finished}                        |
  |-- {Finished} ----------------------->|
  
1-RTT 完成！（vs TLS 1.2 的 2-RTT）
```

### 6. NAT 穿透（候选人的独特优势）

| 技术 | 原理 | 成功率 |
|------|------|--------|
| **STUN** | 查询公网 IP:Port | 高（非 Symmetric NAT） |
| **TURN** | 中继转发 | 100%（需要中继服务器） |
| **UPnP/PMP** | 请求路由器映射端口 | 取决于路由器 |
| **ICE** | 候选收集 + 连接检查 | 综合方案 |

**NAT 类型**：Full Cone → Restricted Cone → Port Restricted Cone → Symmetric（穿透难度递增）

### 7. WebSocket

HTTP 升级握手 → 全双工二进制帧 → 心跳保活（ping/pong）。适用：实时聊天、游戏、协作编辑。

---

## 三、操作系统

### 1. 进程 vs 线程 vs 协程

| 维度 | 进程 | 线程 | 协程 |
|------|------|------|------|
| 调度 | OS | OS | 用户态（运行时） |
| 内存 | 独立地址空间 | 共享 | 共享 |
| 切换开销 | 最大 | 中等 | 最小 |
| 通信 | IPC | 共享内存 | 直接调用 |

### 2. 虚拟内存

物理地址空间的抽象。页表映射虚拟地址 → 物理地址。TLB 缓存页表项。缺页 → 从磁盘加载 → 更新页表。

### 3. I/O 模型

| 模型 | 调用 | 内核行为 |
|------|------|---------|
| 阻塞 I/O | read() 阻塞 | 等待数据 → 拷贝 |
| 非阻塞 I/O | read() 立即返回 | 无数据返回 EAGAIN |
| I/O 多路复用 | select/poll/epoll | 通知可读/可写 |
| 异步 I/O | aio_read() | 内核完成所有操作后通知 |

**epoll 原理**：红黑树存储注册的 fd，就绪链表存储可操作的 fd 事件。`epoll_wait()` 只返回就绪的 fd（vs select 需要遍历所有 fd，O(N)）。

### 4. epoll 的 LT vs ET

- **LT（Level Triggered）**：fd 就绪则一直通知，直到处理完毕。默认模式
- **ET（Edge Triggered）**：fd 状态变化时通知一次。需要非阻塞 I/O + 循环读写直到 EAGAIN。效率更高，编程更复杂

---

## 四、高频场景题

### 慢 SQL 排查

1. `EXPLAIN SELECT ...` → 看 type（ALL = 全表扫描 = 问题）、key（使用的索引）、rows（扫描行数）
2. 常见问题：缺索引、索引失效（函数/类型转换/最左前缀）、回表太多
3. 解决：加索引/覆盖索引/重写 SQL/分库分表（最后手段）

### 设计短链接系统

1. 生成短码：Hash（MD5/SHA 截取 + 冲突处理）或 自增 ID → base62 编码
2. 存储：ID → 长 URL 映射（KV 存储）
3. 访问：短码 → 查映射 → 302 重定向
4. 高并发：缓存热 key，预生成短码池
5. 扩展：分片策略（按短码前缀）

### 分布式 ID 生成器

- **Snowflake**：41bit 时间戳 + 10bit 机器 ID + 12bit 序列号。依赖时钟同步
- **号段模式**：从 DB 批量获取 ID 区间本地分配。减少 DB 访问
- **Redis**：`INCR` 原子递增。简单但依赖 Redis 持久化

---

## 五、候选人数据库实践经验速查

| 经验 | 项目 | 面试话术 |
|------|------|---------|
| SQLite WAL | Clarity/Devbase | "WAL 让读写并发——读不阻塞写，个人本地工具场景的最佳选择" |
| FTS5 全文索引 | Clarity | "SQLite 内置全文搜索，配合 BM25 做关键词检索，不需外部 ES" |
| 自定义 cosine_similarity UDF | Devbase | "SQLite 允许注册自定义函数——向量存 BLOB，查询时零拷贝重解释为 &[f32] 计算相似度" |
| Tantivy BM25 | Devbase | "Rust 版 Lucene——在 Devbase 中索引代码符号和笔记，支持中文分词" |
| sled KV | Syncthing-rust | "COW B+Tree 在元数据场景读性能优秀——通过 trait 抽象隔离，未来可迁移" |
| LRU 缓存 | Clarity/Syncthing-rust | "内存敏感场景下性价比最高的淘汰策略——简单、可预测、适合热点数据" |

---

## 六、TCP 面试必知：11 种状态与 TIME_WAIT

TIME_WAIT 为什么是 2MSL？MSL 是报文在网络中的最大存活时间。第一个 MSL 确保最后的 ACK 到达对端（丢失则对端重发 FIN）；第二个 MSL 让旧连接的所有残余报文消失（防止被新连接误收）。Linux 默认 60s，Windows 120s。

TIME_WAIT 过多→端口耗尽。解决方案：tcp_tw_reuse、连接池复用、调低 MSL（谨慎）。

---

## 七、Redis 高频速答

### Redis 为什么快？
1. 所有数据在内存（持久化异步）；2. 单线程执行无锁竞争（6.0+ 多线程 I/O 但执行仍是单线程）；3. 高效数据结构（SDS/ziplist/skiplist）；4. epoll I/O 多路复用。

### 缓存与 DB 一致性最终方案？
- 强一致：不用缓存，直接查 DB
- 准实时：Cache-Aside + 延迟双删 + 消息队列异步重试
- 最终一致：Canal/Binlog 监听 DB 变更 → 异步更新缓存
- 候选人实践："频繁变更数据设短 TTL(30s)，让不一致窗口可控"

### 高可用 Redis 集群
数据层：Redis Cluster（16384 slots）+ master-replica
哨兵层：Sentinel 监控 + 自动 failover
代理层：Smart Client 或 Proxy
运维层：监控+备份（RDB+AOF 混合）

---

## 八、候选人网络/P2P 项目深度展示

| 技术点 | 项目 | 面试展示 |
|--------|------|---------|
| TLS 1.3 设备身份 | Syncthing-rust | Ed25519 密钥→DeviceID 派生流程图 |
| NAT 穿透组合 | Syncthing-rust | ParallelDialer 同时尝试 LAN/STUN/UPnP/Global |
| mTLS 双向认证 | Syncthing-rust | 对比 JWT vs mTLS 在服务间通信的适用场景 |
| BEP 协议帧 | Syncthing-rust | 长度前缀 + LZ4 压缩帧 wire format |
| 自适应并发 | Syncthing-rust | RTT → ConcurrencyPolicy 反馈闭环 |
| SPMC 事件总线 | Clarity | MPSC/Broadcast/SPMC 语义差异对比 |

---

## 九、后端场景题速答模板

### 线上服务突然变慢？
1. 确定范围（是否全局/是否特定接口）→ 2. 系统指标（CPU/内存/IO/网络）→ 3. 依赖检查（DB 慢查询/Redis 延迟/下游超时）→ 4. 外部因素（流量突增/GC 停顿/连接池耗尽）→ 5. 修复验证（限流/熔断/扩容/索引优化）

### 如何保证接口幂等性？
1. 数据库唯一约束：INSERT ON CONFLICT DO NOTHING；2. Token 机制：一次性消费；3. 状态机：不可逆状态转换；4. 分布式锁：相同请求抢同一锁
候选人实践："Devbase 的 MCP 工具全部用 ON CONFLICT DO UPDATE——外部 Agent 重试不产生副作用"

### 短链接系统设计（扩展）
6. 短码冲突处理：预生成池 + 号段 + 数据库唯一约束兜底
7. 跳转优化：301（永久）vs 302（临时）根据场景选择，302 可保留统计能力
8. 安全：短码随机化防遍历、限流防刷、黑名单 URL 过滤
