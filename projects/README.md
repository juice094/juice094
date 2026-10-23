# 项目架构说明

每个项目对应一个独立代码仓库，这里只保存架构决策与设计取舍，方便需要时查阅。

| 项目 | 一句话 | 状态 | 文档 | 代码 |
|---|---|---|---|---|
| **syncthing-rust** | Syncthing BEP 协议的 Rust 实现，与 Go 版本线格式互通 | 维护中 · v3.0.5 | [syncthing-rust.md](./syncthing-rust.md) | [juice094/syncthing-rust](https://github.com/juice094/syncthing-rust) |
| **Clarity** | 本地优先的分布式人格连续运行时 | 已归档（2026-08） · v0.3.3 | [clarity.md](./clarity.md) | [juice094/clarity](https://github.com/juice094/clarity) |
| **devbase** | 开发者工作区编译器：代码上下文、知识记忆与 Agent 推理路径 | 已收尾（2026-06） · v0.20.1 | [devbase.md](./devbase.md) | [juice094/devbase](https://github.com/juice094/devbase) |

本文档只描述设计与实现，不评价项目价值。已归档与已收尾的项目不再维护，也不提供支持承诺。
