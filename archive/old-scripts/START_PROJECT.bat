@echo off
echo ========================================
echo Starting Navi Tax Application
echo ========================================
echo.

REM Check if backend is already running
tasklist /FI "IMAGENAME eq node.exe" 2>NUL | find /I /N "node.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Backend server is already running
) else (
    echo [STARTING] Backend server...
    start "Backend Server" cmd /k "cd /d c:\Users\HomeLaptop\Downloads\navi-tax-35-main\docs\backend-example && node server.js"
    timeout /t 3 /nobreak >nul
)

echo.
echo [STARTING] Frontend web application...
echo.
echo ========================================
echo IMPORTANT:
echo ========================================
echo 1. Backend runs on: http://localhost:3001
echo 2. Frontend will run on: http://localhost:5173
echo 3. Keep both windows open!
echo.
echo To stop: Close both terminal windows or press Ctrl+C
echo.

cd /d c:\Users\HomeLaptop\Downloads\navi-tax-35-main\web
npm run dev