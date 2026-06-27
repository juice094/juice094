// 阿里达摩院定向简历 — Typst 模板
// 编译: typst compile resume-damo.typ

#set page(
  paper: "a4",
  margin: (top: 1.8cm, bottom: 1.5cm, left: 1.8cm, right: 1.8cm),
)

#set text(
  font: ("Noto Serif SC", "Noto Sans SC", "SimSun", "Microsoft YaHei"),
  size: 10pt,
  lang: "zh",
)

// ===== 颜色定义 =====
#let primary = rgb("#1a1a2e")
#let accent = rgb("#e94560")
#let gray = rgb("#666666")
#let light-gray = rgb("#999999")
#let border-color = rgb("#e0e0e0")

// ===== 布局辅助 =====
#let section-title(title) = {
  v(0.6em)
  block(
    stroke: (bottom: 1pt + border-color),
    width: 100%,
  )[
    #set text(size: 12pt, weight: "bold", fill: primary)
    #title
  ]
  v(0.3em)
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
    [
      - #item
    ]
  }
}

// ===== 文档开始 =====

// --- 头部：姓名 + 联系方式 + Logo ---
#grid(
  columns: (1fr, auto),
  column-gutter: 1em,
  // 左侧：姓名 + 联系方式
  [
    #set text(size: 24pt, weight: "bold", fill: primary)
    #set par(leading: 0.65em)
    周景潇

    #set text(size: 9pt, weight: "regular", fill: gray)
    #set par(leading: 0.5em)

    甘肃农业大学 · 信息科学技术学院 · 数据科学与大数据技术 · 大三在读 · 预计 2027.06 \
    杭州（优先）· 北京 \
    2241470466\@qq.com \| 13626566112 \
    #link("https://github.com/juice094")[github.com/juice094]
  ],
  // 右侧：达摩院 Logo — 高度限制为页眉区域
  align(right + horizon)[
    #box(
      height: 2.2cm,  // 控制 Logo 总高度在 2.2cm 以内
      image("damo-logo.png", fit: "cover"),
    )
  ],
)

// --- 分隔线 ---
#v(0.5em)
#block(stroke: (top: 1.5pt + accent), width: 100%)

// --- 求职意向 ---
#set text(size: 10pt, fill: primary)
#align(center)[
  *求职意向：AI Agent 基础设施开发 / 大模型系统工程（达摩院）*
]

// --- 个人简介 ---
#section-title[个人简介]

数据科学专业大三在读，*Rust 主力（3年）*、*Python 熟练*、*Java/Go 熟悉*。2025.11-2026.06 独立设计并交付三个生产级 Rust 系统（合计 44+ workspace crate、2,500+ 测试全通过）。核心方向是 *AI Agent 基础设施*——独立实现 22-crate 本地 AI Agent 运行时，深度覆盖 ReAct/Plan 双模式 Agent 循环、MCP 协议四传输全实现、BM25+向量混合检索记忆系统、Candle GGUF 本地推理（已支持 Qwen2/Qwen2.5 系列）。同时独立完成一项 RAG 系统输出结构的实证研究（7 模型 × 4 架构 × 3,000+ 样本）。对将 Agent 架构从本地原型推向规模化部署有强烈的工程兴趣。

// --- 技能 ---
#section-title[技能]

#set text(size: 9.5pt)

*语言：* Rust（主力，3年，44+ workspace crate 架构经验）、Python（熟练，实验/数据分析）、Java/Go/TypeScript（熟悉） \
*AI Agent：* ReAct + Plan 双模式 Agent、MCP 协议四传输全实现、Multi-Agent 并行调度、四层审批链（Interactive/Smart/Plan/Yolo） \
*LLM/推理：* 6+ Provider 集成（OpenAI/Anthropic/DeepSeek/Kimi/Ollama/Candle GGUF）、Qwen2/Qwen2.5 本地推理、Provider 网格负载均衡与熔断 \
*RAG/检索：* BM25 + 向量混合检索（RRF 融合）、SQLite FTS5 + 自定义 cosine_similarity UDF、四级记忆压缩、Candle 本地 Embedding \
*系统工程：* tokio、Axum、SPMC 事件总线、TLS 1.3（rustls）、Protobuf（prost）、零 unwrap 工程基线、Contract-First 架构 \
*研究能力：* 独立完成 RAG 实证研究（7 模型 × 4 架构 × 3,000+ 样本）、实验设计与统计检验、LaTeX 学术写作

// --- 项目经历 ---
#section-title[项目经历]

#set text(size: 9.5pt)

// Clarity
#dated-item("2026.04 -- 至今", [Clarity —— Rust 原生本地优先 AI Agent 运行时], subtitle: [Rust · 22 workspace crate · 1,889 tests · ~150K LOC · 独立项目])
#v(0.15em)
单二进制编排 LLM、MCP 工具、记忆系统与多 Agent 协作，六前端共享同一 Agent 内核。默认零 Python/Node.js/Ollama 外部依赖，`cargo install` 即可运行。
#bullet-list((
  [设计 Contract-First 22-crate 分层架构——contract（零内部依赖）为契约根节点，新功能平均只改 1 层，编译时零循环引用。TUI/桌面 GUI/Web IDE/CLI/系统托盘/移动端 FFI 六入口共享 Agent 内核],
  [实现 ReAct + Plan 双模式 Agent 循环与四层审批链（Interactive/Smart/Plan/Yolo）。Plan Mode 将步骤遗漏率从 ~40% 降至接近零，所有工具调用决策可审计],
  [构建 BM25 + 向量混合记忆系统（RRF 融合）+ 四级压缩归档（今天/本周/长期/事实）。SQLite FTS5 + 自定义 cosine_similarity UDF，零外部向量数据库依赖],
  [完整实现 MCP 协议四传输（stdio/SSE/HTTP/WebSocket），集成 6+ LLM Provider 含 Candle GGUF 本地推理（支持 Qwen2/Qwen2.5）。Provider 网格负载均衡与熔断],
  [工程基线：1,889 测试全通过（1,554 lib + 275 bin + 34 doc + 26 集成），Clippy 零 warning，生产代码零 unwrap/expect/panic，12-job CI 全绿（ubuntu/windows/macos）],
))

#v(0.3em)

// Devbase
#dated-item("2026.05 -- 至今", [Devbase —— 本地开发者工作空间世界模型编译器], subtitle: [Rust · 12 workspace crate + 主 crate · 71 MCP 工具 · 616+ tests · 独立项目])
#v(0.15em)
将本地 Git 仓库、PARA 笔记、Skill 脚本与 YAML 工作流编译为 AI 可推理的结构化上下文。
#bullet-list((
  [设计三层编译架构（感知 → 知识 → 策略）：tree-sitter 多语言 AST 解析 + Tantivy BM25 索引 + SQLite 图存储],
  [以 MCP 协议暴露 71 个 stdio 工具（5 stable + 58 beta + 8 experimental），统一 McpTool trait 与幂等路由，Stability 分级体系保证工具质量],
  [零云端依赖语义检索：SQLite BLOB + 自定义 cosine_similarity UDF + Candle/Ollama 本地 embedding。七条架构红线 CI 强制零生产 panic，schema 迁移自动备份],
))

#v(0.3em)

// Syncthing-rust
#dated-item("2025.11 -- 至今", [Syncthing-Rust —— P2P 文件同步守护进程], subtitle: [Rust · 13 workspace crate · 392 tests · ~13MB 单二进制 · 独立项目 · 部署于日本 VPS])
#v(0.15em)
Go Syncthing BEP 协议 wire 级兼容的 Rust 重新实现。生产部署于 Windows 11 ↔ Ubuntu 24.04 双节点 via Tailscale。
#bullet-list((
  [完整实现 BEP over TLS 协议栈：prost + rustls + ed25519-dalek，跨语言 wire_compat 集成测试验证与 Go Syncthing v2.1.0 互操作],
  [多路径 NAT 穿透：LAN UDP 广播 + Global HTTPS mTLS + STUN + UPnP + Relay v1。ParallelDialer 并行尝试所有地址，首个成功的连接获胜],
  [高可靠同步链路：SHA-256 块级扫描（rayon 并行）+ 自适应并发拉取（RTT 反馈）+ 三路文本合并 + Simple/Staggered 版本归档。Windows 句柄共享冲突指数退避回退],
  [零运行时依赖（无 OpenSSL/GC/Python），单静态二进制 ~13MB，零 Clippy warning。CI 矩阵 19 jobs 全绿],
))

// --- 研究经历 ---
#section-title[研究经历]

#set text(size: 9.5pt)

#dated-item("2026.03 -- 至今", [RAG 系统中输出结构的实证研究], subtitle: [独立完成 · #link("https://github.com/juice094/acr-select")[github.com/juice094/acr-select]])
#v(0.15em)
#bullet-list((
  [设计 ~40 实验条件、3,000+ 样本的多因子受控实验，跨 7 模型 × 4 架构（含 Qwen 系列）验证框架普适性],
  [提出格式-内容双维度观测框架，主动发现测量 artifact 并设计统一评分协议修正统计推断],
  [论文撰写中（manuscript in progress）；实验框架可复用于后续 RAG 系统评估；成果直接指导 Clarity 中 RAG 记忆系统的参数调优],
))

// --- 与达摩院的匹配度 ---
#section-title[与达摩院的匹配度]

#set text(size: 9pt)

#table(
  columns: (auto, 1fr),
  stroke: none,
  inset: 4pt,
  align: (left, left),
  [*通义千问开源生态*], [Candle GGUF 本地推理已支持 Qwen2/Qwen2.5；熟悉 GGUF 格式与量化部署],
  [*Agent 框架/工具调用*], [完整实现 MCP 协议四传输 + ReAct/Plan 双模式 Agent + 四层审批链],
  [*RAG/检索增强*], [BM25+向量混合检索 + RRF 融合 + 四级记忆压缩 + RAG 输出结构实证研究],
  [*AI 基础设施/系统工程*], [三个生产级 Rust 系统（44+ crate，2,500+ 测试），零 panic 工程基线],
  [*多模态/文档理解*], [支持 PDF/md/txt/Word 多格式文档解析和索引],
  [*开源社区贡献*], [3 个活跃开源项目，完整的 CI/CD 和文档体系],
)

// --- 教育 ---
#section-title[教育背景]

#set text(size: 9.5pt)

#dated-item("2023.09 -- 2027.06", [甘肃农业大学 · 信息科学技术学院], subtitle: [数据科学与大数据技术 · 工学学士（预计）])
#v(0.15em)
均分 83 / 核心课 86 · 专业前 10% \
核心课程：数据结构(90)、大数据挖掘与应用(97)、数据存储(96)、数据库原理(86)、操作系统(87)、人工智能导论(86.5)

// --- 认证与语言 ---
#section-title[认证与语言]

#set text(size: 9.5pt)

- AI 应用工程师（中级）—— 工业和信息化部认证
- 日语专业四级（72 分）· 英语（技术文档读写、论文写作）· C1 驾照

// --- 其他 ---
#section-title[其他]

#set text(size: 9.5pt)

- 可到岗时间：2026.07；可实习 3--6 个月，每周 5 天
- 多个项目公网可访问：Clarity（Vercel）、student-era（Vercel）、syncthing-rust（日本 VPS）
