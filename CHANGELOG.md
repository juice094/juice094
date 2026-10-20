# 更新日志 (Changelog)

本项目的所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [1.1.1] - 2026-10-20

### Changed
- 简历与项目文档的全部项目指标改用 GitHub API 可验证来源（commit 数、release 版本、star），删除 crate 数、LOC、测试数等手写值。
- Clarity 标注为已归档（2026-08），devbase 标注为已收尾（2026-06），syncthing-rust 标注为持续维护。
- README 精选项目按活跃度重排，syncthing-rust 升至首位。
- `archive/resumes` 合并进 `archive/resume`。

### Added
- `docs/SESSION-REPORT-2026-10-20.md`：本轮整理的完整记录。
- `AGENTS.md` 新增「数据可信性规则」小节。

### Removed
- 简历中所有 `acr-select` 死链（仓库 404）。
- 「vibe coding ~27 万行」「双稀缺组合」「双闭环能力」等不可验证表述。
- 简历中的 QQ 邮箱，统一为 Gmail。

### Fixed
- syncthing-rust 时间线：2025.11 → 2026.04（仓库实际创建时间）。
- `keyword-arsenal.md` 中 devbase 工具数：81 → 71。

## [1.1.0] - 2026-10-20

### Added
- `AGENTS.md` 新增「仓库定性」章节：策展型作品集定位、T2 成熟标准、分区生命周期表，作为后续改动的裁判依据。
- 新增 `archive/README.md`，显式声明存档面为 Archived、不维护。
- 新增 `projects/README.md`、`research/README.md` 作为展示面索引，README 底部徽章改为指向具体文件。

### Changed
- `README.md` 重构：标题与正文不再出现真名；删除技术栈罗列，改为量化指标（crates / LOC / 项目数）；新增「精选项目」文字块；四行两列表格改为单列 + `<details>` 折叠，仅默认展开贡献日历；底部导航改为徽章按钮。
- 联系方式统一为 `humiao2007@gmail.com`，Résumé 徽章指向 `resume/en.md`。
- `archive/` 成为唯一归档目录，`.archive/` 内容迁入并删除，`.gitignore` 移除对应规则。
- `resume/` 顶层的已完成历史版本（`zh-v4` 系列、达摩院与通用定向的命名 PDF、`周景潇-求职综合展示-v4.pptx`、`给老师.md`）移入 `archive/resume/`，顶层文件数 75 → 16。`zh-keda-ai-agent.md/.pdf` 保留原位——它是 `build-resume.ps1` 的唯一源文件，不是历史版本。
- `profile/` 中未被 README 引用的 `calendar-*`、`stats-*` 移入 `archive/profile/`。

### Removed
- 删除根目录孤儿文件 `metrics.svg`、`metrics-light.svg`、`metrics-dark.svg`、`notes.zip`（全仓无引用）。
- 删除 `readme-stats.yml` 中 `Followup`、`WakaTime` 共 4 个 step；删除对应 `profile/followup-*`、`profile/wakatime-*` 卡片（前者数据全为 0 且条形图坐标异常，后者因缺少 API Key 恒为 0）。
- 删除与贡献日历信息重复的第三方 `ghchart` 热力图。

### Fixed
- `.gitignore` 补充 `*.zip`，防止打包物再次误提交。

## [1.0.0] - 2025-10-20

### Added
- 初始化仓库标准文档结构。
- 新增 `LICENSE` (MIT)、`CONTRIBUTING.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md`。
- 新增 `.github/ISSUE_TEMPLATE/` 规范与 PR 模板。
- 新增 `CHANGELOG.md` 记录重大变更。

### Changed
- 重构 `README.md`，移除主页大篇幅简历展示，改为以“核心项目、技术笔记、简历指引”为主的技术资产导航枢纽。
- 在 README 中补充了环境配置与简历本地构建指南。