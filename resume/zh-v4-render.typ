// 通用简历 —— 借用了 resume-damo.typ 的版式，右侧 Logo 区域留白

#set page(
  paper: "a4",
  margin: (top: 1.2cm, bottom: 1.0cm, left: 1.3cm, right: 1.3cm),
)

#set text(
  font: ("Noto Serif SC", "Noto Sans SC", "SimSun", "Microsoft YaHei"),
  size: 9pt,
  lang: "zh",
)

// ===== 颜色定义 =====
#let primary = rgb("#1a1a2e")
#let accent = rgb("#2563eb")
#let gray = rgb("#666666")
#let light-gray = rgb("#999999")
#let border-color = rgb("#e0e0e0")

// ===== 布局辅助 =====
#let section-title(title) = {
  v(0.35em)
  block(
    stroke: (bottom: 0.8pt + border-color),
    width: 100%,
  )[
    #set text(size: 11pt, weight: "bold", fill: primary)
    #title
  ]
  v(0.15em)
}

#let dated-item(date, title, subtitle: none) = {
  grid(
    columns: (1fr, auto),
    column-gutter: 0.5em,
    row-gutter: 0.1em,
    align(left)[
      #set text(weight: "bold", fill: primary)
      #title
    ],
    align(right)[
      #set text(size: 9pt, fill: gray)
      #date
    ],
  )
  if subtitle != none {
    text(size: 9pt, fill: gray)[#subtitle]
  }
}

#let bullet-list(items) = {
  for item in items {
    [- #item]
  }
}

#set list(spacing: 0.5em)

// ===== 文档开始 =====

// --- 头部：姓名 + 联系方式 ---
#align(center)[
  #text(size: 24pt, weight: "bold", fill: primary)[周景潇]
  #v(0.15em)
  #text(size: 9pt, fill: gray)[
    甘肃农业大学 · 信息科学技术学院 · 数据科学与大数据技术 · 大三在读 · 预计 2027.06 \
    上海 / 北京 / 深圳 / 杭州 / 成都 \
    13626566112 \| 2241470466\@qq.com \| #link("https://github.com/juice094")[github.com/juice094]
  ]
  #v(0.3em)
  #box(height: 1.2pt, width: 80%, fill: accent)
  #v(0.25em)
  #text(size: 10pt, fill: primary)[*求职意向：AI Agent 开发 / 后端系统开发 / 智能体平台研发*]
]

// --- 个人简介 ---
#section-title[个人简介]

独立用 Rust 从零构建过三个系统级项目：一个跨设备保持一致的 AI Agent、一个无需云盘的 P2P 文件同步工具、一个把代码和笔记编译成 AI 可理解上下文的开发者知识库。熟悉异步服务、嵌入式存储、网络协议和跨平台 UI，工程上追求零警告、零 panic、可单二进制分发。

// --- 技术能力 ---
#section-title[技术能力]

#set text(size: 9.5pt)

我主要用 *Rust* 写系统级软件，也常用 *Python* 做数据分析、测试脚本和实验验证。

在项目中实际用过这些技术：
- *异步与网络*：Tokio、Axum、Tower、reqwest、WebSocket、rustls
- *存储与检索*：SQLite、rusqlite、Tantivy、BM25、embedding 向量搜索
- *AI Agent*：ReAct / Plan 双模式、MCP 协议、Multi-Agent 编排、RAG 检索增强
- *分布式与 P2P*：BEP 协议、STUN、UPnP、Relay、NAT 穿透
- *跨平台 UI*：egui、ratatui、UniFFI
- *安全*：ChaCha20-Poly1305、TLS 1.3、自签名设备证书
- *工程化*：Cargo Workspace、GitHub Actions、Clippy、tracing、criterion

// --- 项目经历 ---
#section-title[项目经历]

#set text(size: 9.5pt)

// Clarity
#dated-item("2026.04 — 至今", [Clarity — 让 AI 助手跨设备保持一致人格的本地 Agent 系统], subtitle: [Rust · 21 workspace crate · ~150K LOC · 测试全绿 · 零 panic · #link("https://github.com/juice094/clarity")[github.com/juice094/clarity]])
#v(0.08em)
#bullet-list((
  [本地优先的 AI Agent 运行时：ReAct + Plan 双模式执行，步骤遗漏率从约 40% 降到接近零。],
  [MCP 工具协议三传输实现（stdio / SSE / WebSocket），LLM 可调本地文件、搜索、shell 等能力。],
  [SQLite 单文件混合记忆检索：手写向量相似度 UDF + BM25 关键词检索，零外部向量数据库依赖。],
  [桌面 GUI（egui）、终端 UI（ratatui）、后台服务、移动端 FFI（UniFFI）共享同一 Agent 内核。],
))

#v(0.12em)

// syncthing-rust
#dated-item("2025.11 — 至今", [syncthing-rust — 无需云盘的 P2P 文件同步工具], subtitle: [Rust · 9 library crate + 5 命令二进制 · 413 tests · ~16 MB 单二进制 · #link("https://github.com/juice094/syncthing-rust")[github.com/juice094/syncthing-rust]])
#v(0.08em)
#bullet-list((
  [从零实现 Syncthing BEP 协议，protobuf 编解码，wire_compat 集成测试验证与 Go 版线路兼容。],
  [多路径 NAT 穿透：UDP 本地广播、全球发现、STUN、UPnP、Relay 中继回退。],
  [块级文件同步 + Windows 句柄冲突退避 + 三路文本合并 + Simple/Staggered 版本归档。],
))

#v(0.12em)

// devbase
#dated-item("2026.01 — 至今", [devbase — 把代码和笔记编译成 AI 能理解的上下文], subtitle: [Rust · 12 workspace crate + 主 crate · ~59K LOC · 81 MCP 工具 · #link("https://github.com/juice094/devbase")[github.com/juice094/devbase]])
#v(0.08em)
#bullet-list((
  [通过 MCP 协议暴露 81 个 stdio 工具，覆盖代码符号检索、Git 分析、笔记搜索、YAML 工作流执行。],
  [零云端依赖语义检索：Tantivy 全文/符号索引 + SQLite BLOB 存 embedding + 手写 cosine_similarity UDF。],
  [YAML DAG 工作流引擎：支持 Skill、子工作流、并行、条件判断、循环 5 种步骤类型。],
))

// --- 研究经历 ---
#section-title[研究经历]

#set text(size: 9.5pt)

#dated-item("2026.03 — 至今", [检索增强生成中输出结构的实证研究], subtitle: [#link("https://github.com/juice094/acr-select")[github.com/juice094/acr-select]])
#v(0.08em)
围绕 RAG 系统中“输出格式如何影响内容质量”设计受控实验：40 个实验条件、3000+ 样本、跨 4 种模型架构验证。论文撰写中。

// --- 其他 ---
#section-title[其他]

#set text(size: 9.5pt)

- 认证：AI 应用工程师（中级）— 工业和信息化部认证
- 语言：日语专业四级（CJT-4）· 大学英语四级（CET-4）
- 到岗时间：2026.07；可实习 3–6 个月，每周 5 天
- 公网可访问：Clarity Web 前端（Vercel）、syncthing-rust P2P 节点（日本 VPS）
