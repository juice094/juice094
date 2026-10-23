<div align="center">

# juice094

[![GitHub](https://img.shields.io/badge/GitHub-juice094-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/juice094)
[![Email](https://img.shields.io/badge/Email-humiao2007%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:humiao2007@gmail.com)
[![Résumé](https://img.shields.io/badge/Résumé-English%20%7C%20Markdown-2ea44f?style=for-the-badge&logo=markdown&logoColor=white)](./resume/en.md)

</div>

<p align="center">
  <a href="#项目">项目</a> ·
  <a href="#show-me-the-code">Show me the code</a> ·
  <a href="./projects/README.md">项目架构</a> ·
  <a href="./notes/README.md">技术笔记</a> ·
  <a href="./research/README.md">研究草稿</a> ·
  <a href="./resume/en.md">简历</a>
</p>

## 项目

**仍在维护**

- **[syncthing-rust](https://github.com/juice094/syncthing-rust)** — Syncthing BEP 协议的 Rust 实现，与官方 Go 版本线格式互通，可互相同步。三平台预编译单文件，无需运行时依赖。当前版本 v3.0.5。

**已收尾 / 已归档（源码可读，不再维护）**

- **[Clarity](https://github.com/juice094/clarity)** — 本地优先的分布式人格运行时，单一身份跨模型与设备。v0.3.3 后归档。
- **[devbase](https://github.com/juice094/devbase)** — 开发者工作区编译器，把代码上下文、知识记忆与 Agent 推理路径放进一个 Rust 引擎。v0.20.1 后收尾。

## Show me the code

> 最新可运行产物：**syncthing-rust v3.0.5** — *Data-Loss Hardening + E2E Race Elimination*

~~~bash
# 单文件静态二进制，零运行时依赖
curl -LO https://github.com/juice094/syncthing-rust/releases/download/v3.0.5/syncthing-x86_64-linux
chmod +x syncthing-x86_64-linux
./syncthing-x86_64-linux --help

# 启动后 TUI 实时同步状态，同时暴露 REST API 与 Prometheus /metrics
./syncthing-x86_64-linux
~~~

| 平台 | Release 资产 | 大小 |
|---|---|---|
| Linux x86_64 | [`syncthing-x86_64-linux`](https://github.com/juice094/syncthing-rust/releases/download/v3.0.5/syncthing-x86_64-linux) | 12.3 MB |
| macOS x86_64 | [`syncthing-x86_64-darwin`](https://github.com/juice094/syncthing-rust/releases/download/v3.0.5/syncthing-x86_64-darwin) | 10.5 MB |
| Windows x86_64 | [`syncthing-x86_64-windows.exe`](https://github.com/juice094/syncthing-rust/releases/download/v3.0.5/syncthing-x86_64-windows.exe) | 15.3 MB |

**源码与架构**：[syncthing-rust 源码](https://github.com/juice094/syncthing-rust) · [架构决策表](./projects/syncthing-rust.md) · 19 个 MCP tools 供 Agent 直接调用

