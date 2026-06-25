# 一键构建简历 PDF
# 用法：右键此文件 → 使用 PowerShell 运行
# 或 PowerShell 中执行：.\resume\build-resume.ps1

$ErrorActionPreference = "Stop"

$resumeName = "zh-keda-ai-agent"
$source = "$PSScriptRoot\$resumeName.md"
$template = "$PSScriptRoot\resume-template.tex"
$output = "$PSScriptRoot\$resumeName.pdf"

if (-not (Test-Path $source)) {
    Write-Error "源文件不存在: $source"
    exit 1
}

if (-not (Test-Path $template)) {
    Write-Error "模板文件不存在: $template"
    exit 1
}

Write-Host "正在生成 PDF: $output" -ForegroundColor Cyan

& "C:\Program Files\Pandoc\pandoc.exe" `
    $source `
    -o $output `
    --template=$template `
    --pdf-engine=xelatex `
    -V CJKmainfont="SimSun"

if ($LASTEXITCODE -eq 0) {
    Write-Host "生成成功: $output" -ForegroundColor Green
} else {
    Write-Error "PDF 生成失败，请检查上方错误信息"
    exit 1
}
