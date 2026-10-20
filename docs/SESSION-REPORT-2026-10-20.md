# 会话报告：仓库整理与数据可信化

> 日期：2026-10-20
> 范围：README 重构 → 仓库结构整理 → 派生层建设 → 数据审计与修正

---

## 1. 起点与终点

**起点问题**（用户最初反馈）：

> 首屏图表太多、两列表格在移动端不可读、部分图表信息重复、链接不够具体。

**终点结论**：

布局问题只是表层。逐层深入后，真正的问题是——**公开面所有项目数字都无法验证，且相当一部分与事实不符**。本次收尾时，公开面已不存在无法从 GitHub API 获取的数字。

---

## 2. 关键发现

### 2.1 三个展示项目的真实状态

| 项目 | 简历原写 | 实测 |
|---|---|---|
| Clarity | 2026.04 — 至今 | **已归档**，最后推送 2026-08-11 |
| devbase | 2026.04 / 2026.01 — 至今 | 停滞，最后推送 2026-06-27 |
| syncthing-rust | 2025.11 — 至今 | 活跃，v3.0.5（2026-10-18），7 star |

三个仓库均在 **2026-04-15 同日创建**（相隔 15 分钟），简历中的「2025.11 开始」早于仓库创建时间。

### 2.2 数字冲突

同一指标最多存在 4 个版本：

| 指标 | 版本 A | 版本 B | 差异 |
|---|---|---|---|
| Clarity 测试数 | 1,889（手写简历） | 1,243（projects/ 与 YAML） | 646 |
| Clarity crates | 22 | 23 | 1 |
| syncthing 二进制 | 12MB | 13MB | 1MB |
| 三项目 crates 合计 | 44+ | 47 / 43（两种算法） | 对不上 |
| 三项目测试合计 | 2,500+ | 2,897 / 2,251 | 对不上 |

`git log -S` 证明 1,889 与 1,243 在**同一次提交中就已并存**，是两套口径从未统一，不是新旧覆盖。

### 2.3 账户真实活跃度

| 维度 | 公开 | 私密 |
|---|---|---|
| 仓库数 | 9 | 16 |
| 磁盘占用 | 126 MB | 1,071 MB |
| 30 天内活跃 | 3 | 9 |

**公开面展示的是过时快照，真实行为轨迹在私密侧持续生成。**

### 2.4 死链与矛盾表述

- `acr-select` 仓库 404，但在 4 个简历文件中被引用
- `zh.md` 写「vibe coding ~27 万行」，与 README 的 built from scratch 直接矛盾
- 「Rust + AI Agent 双稀缺组合」「研究+工程双闭环能力」为不可验证 claim

---

## 3. 执行动作

### 阶段 1：布局与结构

- README：隐藏真名、单列折叠布局、Gmail 邮箱、删除重复 ghchart
- `AGENTS.md`：新增「仓库定性」章节与分区表
- 删除 8 个孤儿/零值文件（metrics 系列 SVG、notes.zip、followup 与 wakatime 卡片）
- `archive/` 统一归档，`resume/` 顶层大幅收缩
- 新增 `projects/README.md`、`research/README.md`

### 阶段 2：派生层

- `scripts/aggregate_stats.py`：只读元数据与语言字节，不下载代码
- `.github/workflows/aggregate-stats.yml`：每日聚合，产出 `profile/stats.json`
- 首次运行结果：25 仓库 / 9 公开 / 16 私密 / 1.17 GB

### 阶段 3：简历数据可信化

- 邮箱统一 Gmail（6 文件）
- 删除 vibe coding、双稀缺组合、双闭环能力
- 删除 `acr-select` 死链
- Clarity 标注已归档（2026-08）、devbase 标注已收尾（2026-06）
- 手写数字替换为可验证指标：1,026 / 489 / 423 commits，v0.3.3 / v0.20.1 / v3.0.5
- 新增 `resume/METRICS-AUDIT.md`

### 阶段 4：项目文档对齐

- `projects/` 三份文档头部标注状态
- Scale 表改用 commit 数、release 版本、release 资产大小
- 删除 crate 数、代码行数、测试数，并注明「需仓库内实测」
- README 首屏指标改为 1,938 commits，精选项目重排（活跃优先）

### 阶段 5：收尾

- `archive/resumes` 合并进 `archive/resume`
- `keyword-arsenal.md`、`resume-assets-combined.md` 清理残留旧数字
- 本报告

---

## 4. 数据可信性规则（本次确立）

公开面出现的项目指标，只允许三类来源：

1. **commit 数** — GitHub commits API
2. **release 版本与资产大小** — GitHub releases API
3. **star 数** — GitHub 仓库元数据

任何无法从 API 获取的数字（crate 数、LOC、测试数），**要么删除，要么标注「需实测」**，不保留手写值。

---

## 5. 遗留项

| 项 | 说明 | 优先级 |
|---|---|---|
| `resume/data/resume.yaml` + `build.py` | 实验性脚手架，内容未追平手写版，未接入 CI。AGENTS.md 已标注「不要删除任一条，也不要让 B 接管 CI」 | 中 |
| `resume/METRICS-AUDIT.md` | 审计记录，含旧数字对照，有意保留作为历史证据 | — |
| 研究经历「至今」 | 无公开仓库可验证，保留原状；简历已注明「代码与实验数据暂未公开」 | 低 |
| `notes/README.md` 真名 | 仓库内页含真名，用户已确认「README 不出现即可」 | — |
| crate 数 / LOC / 测试数 | 需要读 Cargo.toml 与测试文件，超出当前「不落盘代码」边界 | 低 |

---

## 6. 当前仓库结构

- **根目录**：README.md、AGENTS.md、CHANGELOG.md、LICENSE、SECURITY.md、CONTRIBUTING.md、CODE_OF_CONDUCT.md
- **projects/**：3 份项目文档 + README 索引，全部带状态标注
- **resume/**：17 个顶层文件，含 METRICS-AUDIT.md、手写主链 md/pdf、实验性脚手架目录（data/configs/templates）
- **profile/**：10 个 SVG + stats.json
- **notes/**、**research/**：展示面
- **archive/**：profile / resume / supporting 三个子目录
- **scripts/**：aggregate_stats.py + auto-push
- **docs/**：本报告
- **.github/workflows/**：build.yml、readme-stats.yml、aggregate-stats.yml

---

## 7. 后续建议

1. **决定简历是否还需要多版本生成**：需要则回填 `resume.yaml`，不需要则归档脚手架，`resume/` 收敛为单链。
2. **若要恢复 crate/LOC/测试数**：在 CI 中读取 Cargo.toml 与测试列表，算完即弃，只写数字到 metrics.json。
3. **定期复核**：aggregate-stats.yml 每天自动更新账户级数据；项目级指标建议每月人工触发一次 API 复核。
