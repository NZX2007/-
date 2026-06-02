@echo off
echo ==========================================
echo   HUST Auto Course - Browser Launcher
echo ==========================================
echo.
echo  Enter the URL you want to visit:
echo  (Press Enter for HUST default)
echo.
set /p target_url="URL: "

if "%target_url%"=="" (
    set target_url=https://smartcourse.hust.edu.cn
)

if not "%target_url:~0,4%"=="http" (
    set target_url=https://%target_url%
)

echo.
echo Starting Edge Debug Mode...
echo Target: %target_url%
echo.

REM Close existing Edge
taskkill /F /IM msedge.exe 2>nul
taskkill /F /IM msedgewebview2.exe 2>nul

REM Wait 3 seconds
timeout /t 3 /nobreak >nul

REM Start Edge with debug port
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="C:\Users\23327\edge_debug_temp" %target_url%

echo.
echo ==========================================
echo   Edge started successfully!
echo   Debug port: 9222
echo ==========================================
echo.
echo  Please login and open course page
echo  Then run: py semi_auto_course_v5_virtual.py
echo.
pause