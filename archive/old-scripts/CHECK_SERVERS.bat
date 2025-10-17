@echo off
REM ========================================
REM Navi Tax Application - Server Status Check
REM ========================================

echo.
echo ========================================
echo   NAVI TAX SERVER STATUS
echo ========================================
echo.

REM Check Backend (Port 3001)
echo [BACKEND SERVER - Port 3001]
netstat -ano | findstr ":3001" >nul 2>&1
if %errorlevel% equ 0 (
    echo Status: RUNNING
    echo URL: http://localhost:3001
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3001"') do (
        echo Process ID: %%a
    )
) else (
    echo Status: NOT RUNNING
)

echo.
echo ========================================
echo.

REM Check Frontend (Port 5173)
echo [FRONTEND SERVER - Port 5173]
netstat -ano | findstr ":5173" >nul 2>&1
if %errorlevel% equ 0 (
    echo Status: RUNNING
    echo URL: http://localhost:5173
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173"') do (
        echo Process ID: %%a
    )
) else (
    echo Status: NOT RUNNING
)

echo.
echo ========================================
echo.

REM Overall Status
netstat -ano | findstr ":3001" >nul 2>&1
set backend_running=%errorlevel%

netstat -ano | findstr ":5173" >nul 2>&1
set frontend_running=%errorlevel%

if %backend_running% equ 0 (
    if %frontend_running% equ 0 (
        echo [OK] Both servers are running!
        echo.
        echo Access the application at:
        echo http://localhost:5173
    ) else (
        echo [WARNING] Backend is running but Frontend is NOT
        echo.
        echo Run START_BOTH_SERVERS.bat to start frontend
    )
) else (
    if %frontend_running% equ 0 (
        echo [WARNING] Frontend is running but Backend is NOT
        echo.
        echo Run START_BOTH_SERVERS.bat to start backend
    ) else (
        echo [ERROR] Both servers are NOT running
        echo.
        echo Run START_BOTH_SERVERS.bat to start both servers
    )
)

echo.
echo ========================================
echo.
pause