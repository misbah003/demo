@echo off
REM ========================================
REM Navi Tax Application - Stop All Servers
REM ========================================

echo.
echo ========================================
echo   STOPPING NAVI TAX SERVERS
echo ========================================
echo.

REM Stop Backend (Port 3001)
echo [INFO] Checking for backend server on port 3001...
netstat -ano | findstr ":3001" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Stopping backend server...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3001"') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    echo [OK] Backend server stopped
) else (
    echo [INFO] Backend server is not running
)

echo.

REM Stop Frontend (Port 5173)
echo [INFO] Checking for frontend server on port 5173...
netstat -ano | findstr ":5173" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Stopping frontend server...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173"') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    echo [OK] Frontend server stopped
) else (
    echo [INFO] Frontend server is not running
)

echo.
echo ========================================
echo   ALL SERVERS STOPPED
echo ========================================
echo.
pause