@echo off
cd /d C:\Users\22414\dev\juice094

:: Generate timestamp: 2026-06-28 14:07
for /f "usebackq tokens=*" %%a in (`powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd HH:mm'"`) do (
    set TIMESTAMP=%%a
)

git add -A
git commit --allow-empty -m "chore: 定时同步 %TIMESTAMP%" >nul 2>&1
git push 2>&1
