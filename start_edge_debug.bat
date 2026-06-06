@echo off
echo ==========================================
echo   Start Edge Debug Mode
echo ==========================================
echo.
echo  Enter URL to visit (press Enter for default):
echo.
set /p target_url="URL: "

if "%target_url%"=="" (
    set target_url=https://smartcourse.hust.edu.cn
)

if not "%target_url:~0,4%"=="http" (
    set target_url=https://%target_url%
)

echo.
echo Target: %target_url%
echo.

taskkill /F /IM msedge.exe 2>nul
taskkill /F /IM msedgewebview2.exe 2>nul

timeout /t 2 /nobreak >nul

echo Starting Edge...
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --remote-allow-origins=* %target_url%

echo.
echo ==========================================
echo   Edge closed.
echo ==========================================
pause