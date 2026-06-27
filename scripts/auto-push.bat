@echo off
cd /d C:\Users\22414\dev\juice094

:: Generate timestamp: 2026-06-28 14:07
for /f "tokens=1-6 delims=/-:. " %%a in ('wmic os get localdatetime ^| findstr [0-9]') do (
    set YYYY=%%a
    set MM=%%b
    set DD=%%c
    set HH=%%d
    set MIN=%%e
)
set TIMESTAMP=%YYYY:~0,4%-%MM%-%DD% %HH%:%MIN%

git add -A
git commit --allow-empty -m "chore: 定时同步 %TIMESTAMP%" >nul 2>&1
git push 2>&1
