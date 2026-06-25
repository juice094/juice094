# 简历 LaTeX 模板库

> 本目录存放成熟的中文简历 LaTeX 模板，作为参考和备用方案。当前主用模板仍为仓库根目录下的 `resume/resume-template.tex`。

## 已拉取的模板

### 1. billryan-resume

- **来源**：https://github.com/billryan/resume
- **特点**：最经典的中文简历模板之一，XeLaTeX 编译，开箱即用，排版稳重大气
- **适用**：应届生 / 技术岗 / 一页纸简历
- **主文件**：
  - `resume.cls`：文档类定义
  - `resume.tex`：示例简历（中文）
  - `resume_photo.tex`：带照片的示例简历
  - `zh_CN-Adobefonts_external.sty` / `zh_CN-Adobefonts_internal.sty`：中文字体配置
- **许可证**：MIT（见目录内 `LICENSE`）

### 2. liweitianux-resume

- **来源**：https://github.com/liweitianux/resume
- **特点**：专为应届生设计，支持中英文，集成 Font Awesome 5 图标，排版现代
- **适用**：需要图标装饰、追求视觉辨识度的技术/学术岗位
- **主文件**：
  - `resume.cls`：文档类定义
  - `resume-zh.tex`：中文示例简历
  - `resume-en.tex`：英文示例简历
  - `resume-zh+en.pdf`：示例输出
- **许可证**：模板基于 YACC / Plasmati Graduate CV，原仓库未显式声明 LICENSE；使用时请遵守其 README 中的引用说明。

## 使用建议

| 场景 | 推荐模板 |
|---|---|
| 当前主用（已配置 pandoc 一键构建） | `resume/resume-template.tex` |
| 想要更稳重、保守的排版 | `billryan-resume/resume.tex` |
| 想要更现代、带图标的排版 | `liweitianux-resume/resume-zh.tex` |

## 注意事项

- 这些模板通常需要安装指定中文字体（如 Adobe 思源宋体/黑体），编译前请阅读各自 README 的字体要求。
- 如果直接复制 `.tex` 文件使用，请保留原作者的 LICENSE / README / 引用说明。
