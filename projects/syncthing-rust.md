# syncthing-rust — P2P File Sync Protocol

> **Wire-compatible Rust implementation of the Syncthing BEP protocol. 423 commits, v3.0.5, 7 stars.**
>
> https://github.com/juice094/syncthing-rust
>
> **状态**：持续维护（最近发布 2026-10）

---

## What It Does

A from-scratch Rust implementation of the Block Exchange Protocol (BEP) — the protocol that powers Syncthing. Wire-compatible with the Go implementation: the two can sync with each other.

Binary size: 10.5—15.3MB by platform（macOS 10.5MB / Linux 12.3MB / Windows 15.3MB）.

---

## Architecture

```
binaries (5)
  ├── syncthing          Main daemon (TUI + REST API + sync engine)
  ├── syncthing-cli      Command-line control
  ├── syncthing-tray     Windows system tray
  ├── syncthing-bench    Performance benchmarking
  └── syncthing-mcp-bridge   MCP integration

protocol stack
  ├── bep-protocol       BEP wire format (prost/Protobuf)
  ├── syncthing-net      TLS 1.3 + TCP/UDP transport
  │                      Discovery: UDP broadcast, HTTPS, STUN, UPnP, Relay v1
  └── syncthing-sync     Block-level delta synchronization

storage
  ├── syncthing-db       Block index + metadata store
  ├── syncthing-fs       Filesystem abstraction + change monitoring
  └── syncthing-versioner  File versioning strategies

api
  └── syncthing-api      REST API + configuration management
```

---

## Key Technical Decisions

| Decision | Why |
|:---|:---|
| **prost for Protobuf** | Compile-time codegen → zero runtime reflection |
| **TLS 1.3 for transport** | Required for BEP wire compatibility |
| **NAT traversal stack** | STUN + UPnP + Relay v1 → connects behind any NAT |
| **Block-level delta sync** | Only transfer changed blocks, not whole files |
| **Tailscale integration** | Verified cross-NAT reproducibility |
| **4-layer protocol split** | Protocol / Transport / Sync / Storage → each testable in isolation |

---

## Scale

| Metric | Value |
|:---|:---|
| Commits | 423 |
| Latest release | v3.0.5（2026-10） |
| Stars | 7 |
| Release assets | 3 平台预编译（macOS 10.5MB / Linux 12.3MB / Windows 15.3MB） |
| Discovery | LAN + Global (UDP, HTTPS, STUN, UPnP, Relay) |

> crate 数与代码行数未纳入本表——需要仓库内实测，暂无可自动获取的来源。
