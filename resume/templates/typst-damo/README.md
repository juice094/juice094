# Typst 简历模板 — 阿里达摩院定向

## 快速开始

### 1. 安装 Typst

```bash
# Windows (scoop)
scoop install typst

# 或直接下载二进制
# https://github.com/typst/typst/releases

# macOS
brew install typst

# Linux
cargo install typst-cli
```

### 2. 准备达摩院 Logo

将达摩院 Logo 放在本目录下，命名为 `damo-logo.png`。

Logo 建议：透明背景 PNG，宽度 > 400px。模板中 Logo 高度被限制在 **2.2cm**（约 83px@300dpi），不会出现"Logo 太大"的问题。

如果暂时没有 Logo，用占位图替代：

```bash
# 生成一个占位图（需要 ImageMagick）
magick -size 400x120 xc:transparent \
  -fill '#1a1a2e' -font Arial -pointsize 24 \
  -gravity center -annotate 0 "DAMO Academy" \
  damo-logo.png
```

### 3. 编译

```bash
cd resume/templates/typst-damo
typst compile resume-damo.typ resume-damo.pdf
```

## Logo 大小控制说明

模板第 69-72 行：

```typst
#box(
  height: 2.2cm,  // 控制 Logo 总高度在 2.2cm 以内
  image("damo-logo.png", fit: "cover"),
)
```

- `height: 2.2cm` — Logo 高度上限，对应页眉区域。如果 Logo 太高会挤压下方内容
- `fit: "cover"` — 保持宽高比，缩放到指定高度
- 调整这个值可以改变 Logo 大小：推荐范围 1.8cm-2.5cm

## 字体

模板默认使用 `Noto Serif SC` / `Noto Sans SC`（Google Noto 中文字体）。

如果系统没有安装，Typst 会 fallback 到系统默认字体。Windows 用户可以改用：

```typst
#set text(font: ("SimSun", "Microsoft YaHei"), ...)
```
