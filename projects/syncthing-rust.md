# syncthing-rust — P2P File Sync Protocol

> **Wire-compatible Rust implementation of the Syncthing BEP protocol. 8 crates, 59K LOC.**
>
> https://github.com/juice094/syncthing-rust

---

## What It Does

A from-scratch Rust implementation of the Block Exchange Protocol (BEP) — the protocol that powers Syncthing. Wire-compatible with the Go implementation: the two can sync with each other.

Binary size: ~12MB static. Memory: 170MB stable under load.

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
| Crates | 8 |
| Binaries | 5 |
| Lines of Rust | 59,000 |
| Binary size | ~12MB static |
| Memory | 170MB stable |
| Discovery | LAN + Global (UDP, HTTPS, STUN, UPnP, Relay) |
