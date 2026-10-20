from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import nsmap
from pptx.oxml import parse_xml

# 创建演示文稿
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 颜色定义
PRIMARY = RGBColor(0x1a, 0x1a, 0x2e)
ACCENT = RGBColor(0x25, 0x63, 0xeb)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x66, 0x66, 0x66)
LIGHT_GRAY = RGBColor(0x99, 0x99, 0x99)
BG_LIGHT = RGBColor(0xF8, 0xF9, 0xFA)

def add_background(slide, color=WHITE):
    """为幻灯片添加纯色背景"""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_textbox(slide, left, top, width, height, text, font_size=18, bold=False,
                color=PRIMARY, align=PP_ALIGN.LEFT, font_name="Microsoft YaHei"):
    """添加文本框"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = align
    return txBox

def add_shape_text(slide, left, top, width, height, text, font_size=14,
                   fill_color=None, text_color=WHITE, bold=False):
    """添加带背景的形状文本"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    if fill_color:
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = text_color
    p.alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.name = "Microsoft YaHei"
    return shape

def add_bullet_list(slide, left, top, width, height, items, font_size=16,
                    color=PRIMARY, bullet_color=ACCENT):
    """添加项目符号列表"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = "Microsoft YaHei"
        p.level = 0
        p.space_after = Pt(10)
    return txBox

def add_section_title(slide, title, subtitle=None):
    """添加章节标题"""
    # 顶部装饰条
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0),
                                  Inches(13.333), Inches(0.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()

    add_textbox(slide, Inches(0.8), Inches(0.6), Inches(12), Inches(0.9),
                title, font_size=36, bold=True, color=PRIMARY)
    if subtitle:
        add_textbox(slide, Inches(0.8), Inches(1.35), Inches(12), Inches(0.5),
                    subtitle, font_size=18, color=GRAY)

# ===== 第1页：封面 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局
add_background(slide, PRIMARY)

# 姓名
add_textbox(slide, Inches(0), Inches(2.2), Inches(13.333), Inches(1.2),
            "周景潇", font_size=60, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# 目标岗位
add_textbox(slide, Inches(0), Inches(3.6), Inches(13.333), Inches(0.8),
            "AI Agent 开发 / 后端系统开发 / 智能体平台研发",
            font_size=28, color=WHITE, align=PP_ALIGN.CENTER)

# 装饰线
line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.5), Inches(4.5),
                               Inches(2.333), Inches(0.05))
line.fill.solid()
line.fill.fore_color.rgb = ACCENT
line.line.fill.background()

# 联系方式
add_textbox(slide, Inches(0), Inches(5.0), Inches(13.333), Inches(0.6),
            "甘肃农业大学 · 数据科学与大数据技术 · 本科 2027 届",
            font_size=18, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
add_textbox(slide, Inches(0), Inches(5.5), Inches(13.333), Inches(0.6),
            "📞 13626566112  ·  ✉ 2241470466@qq.com  ·  🔗 github.com/juice094",
            font_size=16, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# ===== 第2页：个人简介 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_section_title(slide, "个人简介", "独立用 Rust 构建生产级系统")

intro_text = """独立用 Rust 从零构建过三个系统级项目：跨设备保持一致的本地 AI Agent、无需云盘的 P2P 文件同步工具、面向开发者的 AI 知识库。

熟悉异步服务、嵌入式存储、网络协议和跨平台 UI，工程上追求零警告、零 panic、可单二进制分发。"""

add_textbox(slide, Inches(1.0), Inches(2.2), Inches(11.333), Inches(2.5),
            intro_text, font_size=22, color=PRIMARY)

# 关键词标签
keywords = ["Rust 主力", "AI Agent", "MCP 协议", "P2P 网络", "RAG 检索", "零 panic 工程"]
for i, kw in enumerate(keywords):
    row = i // 3
    col = i % 3
    add_shape_text(slide, Inches(1.0 + col * 4.0), Inches(5.0 + row * 0.9),
                   Inches(3.5), Inches(0.6), kw, font_size=16,
                   fill_color=ACCENT, text_color=WHITE, bold=True)

# ===== 第3页：技术能力 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_section_title(slide, "技术能力", "主要用 Rust 写系统级软件，Python 做数据分析与实验")

tech_items = [
    "异步与网络：Tokio、Axum、Tower、reqwest、WebSocket、rustls",
    "存储与检索：SQLite、rusqlite、Tantivy、BM25、embedding 向量搜索",
    "AI Agent：ReAct / Plan 双模式、MCP 协议、Multi-Agent 编排、RAG 检索增强",
    "分布式与 P2P：BEP 协议、STUN、UPnP、Relay、NAT 穿透",
    "跨平台 UI：egui、ratatui、UniFFI",
    "安全：ChaCha20-Poly1305、TLS 1.3、自签名设备证书",
    "工程化：Cargo Workspace、GitHub Actions、Clippy、tracing、criterion"
]
add_bullet_list(slide, Inches(1.0), Inches(2.1), Inches(11.333), Inches(5.0),
                tech_items, font_size=19)

# ===== 第4页：Clarity =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, BG_LIGHT)
add_section_title(slide, "项目经历：Clarity", "让 AI 助手跨设备保持一致人格的本地 Agent 系统")

add_textbox(slide, Inches(1.0), Inches(1.9), Inches(11.333), Inches(0.6),
            "Rust · 21 workspace crate · ~150K LOC · 测试全绿 · 零 panic · 2026.04 — 至今",
            font_size=16, color=GRAY)

clarity_items = [
    "本地优先的 AI Agent 运行时：ReAct + Plan 双模式执行，步骤遗漏率从约 40% 降到接近零",
    "MCP 工具协议三传输实现（stdio / SSE / WebSocket），LLM 可调本地文件、搜索、shell 等能力",
    "SQLite 单文件混合记忆检索：手写向量相似度 UDF + BM25 关键词检索，零外部向量数据库依赖",
    "桌面 GUI（egui）、终端 UI（ratatui）、后台服务、移动端 FFI（UniFFI）共享同一 Agent 内核"
]
add_bullet_list(slide, Inches(1.0), Inches(2.6), Inches(11.333), Inches(4.0),
                clarity_items, font_size=19)

# ===== 第5页：syncthing-rust =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_section_title(slide, "项目经历：syncthing-rust", "无需云盘的 P2P 文件同步工具")

add_textbox(slide, Inches(1.0), Inches(1.9), Inches(11.333), Inches(0.6),
            "Rust · 9 library crate + 5 命令二进制 · 413 tests · ~16 MB 单二进制 · 2025.11 — 至今",
            font_size=16, color=GRAY)

sync_items = [
    "从零实现 Syncthing BEP 协议，protobuf 编解码，wire_compat 集成测试验证与 Go 版线路兼容",
    "多路径 NAT 穿透：UDP 本地广播、全球发现、STUN、UPnP、Relay 中继回退",
    "块级文件同步 + Windows 句柄冲突退避 + 三路文本合并 + Simple/Staggered 版本归档"
]
add_bullet_list(slide, Inches(1.0), Inches(2.6), Inches(11.333), Inches(4.0),
                sync_items, font_size=19)

# ===== 第6页：devbase =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, BG_LIGHT)
add_section_title(slide, "项目经历：devbase", "把代码和笔记编译成 AI 能理解的上下文")

add_textbox(slide, Inches(1.0), Inches(1.9), Inches(11.333), Inches(0.6),
            "Rust · 12 workspace crate + 主 crate · ~59K LOC · 81 MCP 工具 · 2026.01 — 至今",
            font_size=16, color=GRAY)

devbase_items = [
    "通过 MCP 协议暴露 81 个 stdio 工具，覆盖代码符号检索、Git 分析、笔记搜索、YAML 工作流执行",
    "零云端依赖语义检索：Tantivy 全文/符号索引 + SQLite BLOB 存 embedding + 手写 cosine_similarity UDF",
    "YAML DAG 工作流引擎：支持 Skill、子工作流、并行、条件判断、循环 5 种步骤类型"
]
add_bullet_list(slide, Inches(1.0), Inches(2.6), Inches(11.333), Inches(4.0),
                devbase_items, font_size=19)

# ===== 第7页：研究经历 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_section_title(slide, "研究经历", "检索增强生成中输出结构的实证研究")

add_textbox(slide, Inches(1.0), Inches(2.0), Inches(11.333), Inches(2.0),
            "围绕 RAG 系统中“输出格式如何影响内容质量”设计受控实验：40 个实验条件、3000+ 样本、跨 4 种模型架构验证。论文撰写中。",
            font_size=22, color=PRIMARY)

add_textbox(slide, Inches(1.0), Inches(4.2), Inches(11.333), Inches(0.6),
            "github.com/juice094/acr-select", font_size=18, color=ACCENT)

# 亮点数据
stats = [("40", "实验条件"), ("3000+", "样本"), ("4", "模型架构")]
for i, (num, label) in enumerate(stats):
    add_textbox(slide, Inches(1.5 + i * 4.0), Inches(5.2), Inches(3.5), Inches(0.8),
                num, font_size=40, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(1.5 + i * 4.0), Inches(5.9), Inches(3.5), Inches(0.5),
                label, font_size=18, color=GRAY, align=PP_ALIGN.CENTER)

# ===== 第8页：其他 + 结尾 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, PRIMARY)

add_textbox(slide, Inches(0), Inches(1.8), Inches(13.333), Inches(1.0),
            "期待加入", font_size=32, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_textbox(slide, Inches(0), Inches(2.9), Inches(13.333), Inches(0.8),
            "AI Agent 开发 / 后端系统开发 / 智能体平台研发",
            font_size=26, color=ACCENT, align=PP_ALIGN.CENTER)

other_items = [
    "认证：AI 应用工程师（中级）— 工业和信息化部认证",
    "语言：日语专业四级（CJT-4）· 大学英语四级（CET-4）",
    "到岗时间：2026.07；可实习 3–6 个月，每周 5 天",
    "公网可访问：Clarity Web 前端（Vercel）、syncthing-rust P2P 节点（日本 VPS）"
]
add_bullet_list(slide, Inches(2.5), Inches(4.0), Inches(8.333), Inches(2.5),
                other_items, font_size=17, color=WHITE)

# 保存
prs.save(r'C:\Users\22414\dev\juice094\resume\周景潇-求职综合展示.pptx')
print("PPT 已生成：C:\\Users\\22414\\dev\\juice094\\resume\\周景潇-求职综合展示.pptx")
