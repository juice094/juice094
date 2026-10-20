# 简历数字一致性审计

> 生成于 2026-10-20。基准：`profile/stats.json`（GitHub API 全量口径）。
> 状态标记：**✅ 一致** / **⚠️ 冲突** / **❓ 待实测** / **❌ 无来源**

---

## 0. 账户级真实数据（机器生成，可信）

来源：`profile/stats.json`，2026-10-20T10:46:21Z

| 指标 | 值 |
|---|---|
| 仓库总数 | 25 |
| 公开 / 私密 | 9 / 16 |
| 总磁盘占用 | 1,226,475 KB（约 1.17 GB） |
| Rust 占比 | 40.07%（12,376,209 bytes） |
| TypeScript 占比 | 20.43% |
| Python 占比 | 14.32% |

**注意**：这是字节占比，不是 LOC。且包含全部 25 个仓库，与简历"三个项目"口径不同，不能直接替换简历数字，只能作为账户画像的背景事实。

---

## 0.5 仓库活跃度实测（2026-10-20，GitHub API）

### 全账户

| 维度 | 公开 | 私密 | 合计 |
|---|---|---|---|
| 仓库数 | 9 | 16 | 25 |
| 磁盘占用 | 126 MB | 1,071 MB | 约 1.17 GB |
| 30 天内活跃 | 3 | 9 | 12 |
| 90 天内活跃 | — | — | 17 |
| 已归档 | 3 | 0 | 3 |

**私密仓库活跃度分布**：30 天内 9 个、30—90 天 3 个、90—365 天 4 个、一年以上 0 个、已归档 0 个。

**私密仓库主语言分布**：Rust 4、Python 3、HTML 2、TypeScript 2、Java 1、PowerShell 1、Shell 1、未标注 2。

> 结论：账户的真实活跃度主要在私密侧。公开面 9 个仓库中，30 天内活跃的只有 3 个。

### 简历展示的三个公开项目

| 项目 | 已归档 | 最后推送 | 距今天数 | Star | 仓库大小 | GitHub 创建时间 |
|---|---|---|---|---|---|---|
| **Clarity** | **是** | 2026-08-11 | 70 | 2 | 65 MB | 2026-04-15 |
| **devbase** | 否 | 2026-06-27 | 115 | 0 | 3.4 MB | 2026-04-15 |
| **syncthing-rust** | 否 | 2026-10-18 | **2** | **7** | 17 MB | 2026-04-15 |

**关键发现**：

1. **Clarity 已归档**。GitHub 上归档即只读、不再维护。简历写「2026.04 — 至今」，与事实不符。
2. **devbase 停滞 115 天**。最后提交是文档调整，无代码活动。简历同样写「至今」。
3. **三个仓库均在 2026-04-15 同日创建**（相隔 15 分钟内）。简历中 syncthing-rust 写「2025.11 开始」、devbase 写「2026.01」，均早于仓库创建时间。
4. **只有 syncthing-rust 真正活跃**：2 天前发布 v3.0.5，7 star。简历将其排在第三位。

---

## 1. Clarity

| 来源 | crates | LOC | 测试数 |
|---|---|---|---|
| `projects/clarity.md` | 23 | 152,000 | 1,243 |
| `resume/data/resume.yaml` | 23 | 152K | 1,243 |
| `resume/zh.md` | 22 | — | 1,889 |
| `resume/en.md` | 22 | — | 1,889 |
| `resume/resume-general.md` | 22 | ~150K | 1,889 |
| `resume/resume-damo-academy.md` | 22 | ~150K | 1,889 |
| `resume/zh-keda-ai-agent.md` | 22 | — | 1,889 |

**冲突**：
- ⚠️ crates：23 vs 22
- ⚠️ LOC：152,000 vs ~150K（差 2,000）
- ❓ **测试数：1,243 vs 1,889**——这是全仓最严重的冲突

**1,889 的构成**（`en.md` 自洽）：1,554 lib + 275 bin + 34 doc + 26 integration = 1,889 ✅
**1,243 的构成**：未知，无任何文档解释。

`git log -S` 显示：两者在 `9184118`（求职战备体系）同一次提交中就已并存，之后 `ec7eb08`（6-30 脚手架）把 1,243 写进 `resume.yaml` 和 `projects/clarity.md`，而 6-27 的 `zh.md`/`en.md` 用的是 1,889。**不是新旧覆盖，是两套口径从未统一。**

**待确认**：在 clarity 仓库跑 `cargo test --all -- --list | wc -l`，确认当前真实测试总数。

---

## 2. syncthing-rust

| 来源 | crates | LOC | 二进制 | 开始时间 |
|---|---|---|---|---|
| `projects/syncthing-rust.md` | **8 + 5 binaries** | 59,000 | ~12MB | — |
| `resume/data/resume.yaml` | 8 + 5 | 59K | ~12MB | **2025.11** |
| `resume/zh.md` | **13** | — | **~13MB** | 2025.11 |
| `resume/en.md` | 13 | 58,848 | ~13MB | **2026.05** |
| `resume/resume-general.md` | 13 | ~58K | — | 2025.11 |
| `resume/resume-damo-academy.md` | 13 | — | ~13MB | 2025.11 |
| `resume/zh-keda-ai-agent.md` | 13 | 58,848 | — | **2026.04** |

**冲突**：
- ⚠️ crates：`8 library + 5 binaries` vs `13`。**其实不矛盾**——13 = 8 + 5，只是口径（library-only vs 全部 workspace member）不同。建议统一写「13 workspace crates（8 库 + 5 二进制）」。
- ⚠️ 二进制：12MB vs 13MB
- ⚠️ **开始时间：2025.11 / 2026.04 / 2026.05，三个版本**

**待确认**：真实开始时间；release build 后 `ls -lh target/release/syncthing` 的真实大小。

---

## 3. devbase

| 来源 | crates | LOC | MCP 工具 | 测试数 | 二进制 | 开始时间 |
|---|---|---|---|---|---|---|
| `projects/devbase.md` | 12 | 56,000 | 71 | — | ~8.7MB | — |
| `resume/data/resume.yaml` | 12 + 主 | 56K | 71 | — | — | **2026.01** |
| `resume/zh.md` | 12 | 56K | 71 | — | ~8.7MB | 2026.04 |
| `resume/en.md` | 12 | — | 71 | **616+** | — | 2026.04 |
| `resume/resume-general.md` | 12 + 主 | — | — | 616+ | — | **2026.05** |
| `resume/resume-damo-academy.md` | 12 + 主 | — | 71 | 616+ | — | — |
| `resume/zh-keda-ai-agent.md` | 12 | 56K | 71 | — | — | 2026.04 |

**冲突**：
- ⚠️ **开始时间：2026.01 / 2026.04 / 2026.05，三个版本**
- ⚠️ crates：「12」vs「12 + 主 crate」——同上，口径问题

**待确认**：真实开始时间。

---

## 4. 三项目合计

| 来源 | crates | LOC | 测试数 |
|---|---|---|---|
| `resume/zh.md` | **44+** | — | **2,500+** |
| `resume/en.md` | **47** | **270K+** | **2,500+** |
| `resume/resume-general.md` | **44+** | — | **2,500+** |
| `resume/resume-damo-academy.md` | **44+** | — | **2,500+** |

**验算**：
- crates：22 + 13 + 12 = **47**（用 1,889 那套）或 23 + 8 + 12 = **43**（用 1,243 那套）。**44+ 对不上任何一个**。
- 测试：1,889 + 392 + 616 = **2,897**；1,243 + 392 + 616 = **2,251**。**2,500+ 只接近后者，且仍差 249**。
- LOC：152K + 59K + 56K = **267K** ≈ 270K ✅（en.md 的 270K+ 大致成立）

**结论**：`2,500+ 测试` 是用旧数据（1,243 那套）算的，Clarity 测试数涨到 1,889 后**总数没同步**。`44+ crates` 两个算法都对不上。

---

## 5. 研究经历时间

| 来源 | 时间 |
|---|---|
| `resume/zh.md` | **2026.03** — 至今 |
| `resume/data/resume.yaml` | **2026.03** — 至今 |
| `resume/resume-general.md` | **2026.03** — 至今 |
| `resume/en.md` | **2026.06** — present |
| `resume/zh-keda-ai-agent.md` | **2026.06** — 至今 |
| `resume/resume-damo-academy.md` | 无时间 |

⚠️ **2026.03 vs 2026.06，两个版本。**

---

## 6. 联系方式

| 来源 | 邮箱 |
|---|---|
| `README.md` | humiao2007@gmail.com ✅ |
| `SECURITY.md` / `CODE_OF_CONDUCT.md` | humiao2007@gmail.com ✅ |
| `resume/zh.md` | **2241470466@qq.com** ⚠️ |
| `resume/en.md` | **2241470466@qq.com** ⚠️ |
| `resume/resume-general.md` | **2241470466@qq.com** ⚠️ |
| `resume/resume-damo-academy.md` | **2241470466@qq.com** ⚠️ |
| `resume/zh-keda-ai-agent.md` | **2241470466@qq.com** ⚠️ |
| `resume/data/resume.yaml` | **2241470466@qq.com** ⚠️ |

**所有简历仍是 QQ 邮箱**，与 README 已统一的 Gmail 不一致。

---

## 7. 表述风险（非数字，但同级严重）

### 7.1 `zh.md:23-24` 的「vibe coding」

> Rust：有效代码 ~6 万行，**vibe coding ~27 万行**
> Python：有效代码 ~2 万行，**vibe coding ~7 万**

三项目总 LOC ≈ 152K + 59K + 56K = 267K ≈ 27 万。这句话等于写「77% 的代码是 AI 生成的」，与 README 的 "built from scratch"、`summary` 的「独立从零构建」直接矛盾。

**建议**：删除该表述，或改为「累计 27 万行 Rust 代码」不带归因。

### 7.2 不可验证的自我评价

- `zh.md:122`：「Rust + AI Agent 双稀缺组合」
- `resume-general.md:19`：「具备研究+工程双闭环能力」
- `resume-damo:22`：同一句出现两次（重复）

**建议**：删除，用分项数字替代。

---

## 8. 待你确认的清单

> **2026-10-20 更新**：仓库活跃度与创建时间已通过 GitHub API 确认（见 0.5 节）。测试数与 crates 数无法从 API 获取，需仓库内实测，或按「拿不到就不写」原则直接删除。

按优先级排序，前 3 项阻塞其他所有修改：

| # | 问题 | 怎么确认 |
|---|---|---|
| 1 | Clarity 测试数：1,243 还是 1,889？当前是多少？ | clarity 仓库跑 `cargo test --all -- --list \| wc -l` |
| 2 | Clarity crates：22 还是 23？ | `cargo metadata --no-deps \| jq '.packages \| length'` |
| 3 | syncthing-rust 真实开始时间 | 看首个 commit 日期 |
| 4 | devbase 真实开始时间 | 同上 |
| 5 | 研究经历开始时间：2026.03 还是 2026.06 | 你记得的 |
| 6 | syncthing 二进制 12MB 还是 13MB | `ls -lh target/release/syncthing` |
| 7 | 简历邮箱统一为 Gmail？ | 你定 |
| 8 | 「vibe coding」表述删除？ | 你定 |

---

## 9. 确认后的统一策略

1. **单一数据源**：确认后的数字写入 `resume/data/metrics.json`（与 `stats.json` 并列，但只含三项目精确值）
2. **叙述不写数字**：简历正文改为「见 metrics.json」的占位，渲染时注入
3. **口径统一**：crates 一律写「N workspace crates（含 M 二进制）」；测试数一律写「X lib + Y bin + Z doc + W integration = 总」
4. **删除所有不可验证的 claim**
5. 完成后删除本审计文件，或移入 `archive/supporting/`
