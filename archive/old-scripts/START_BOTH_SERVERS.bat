@echo off
REM ========================================
REM Navi Tax Application - Complete Startup
REM ========================================
REM This script starts both Backend and Frontend servers
REM ========================================

echo.
echo ========================================
echo   NAVI TAX APPLICATION STARTUP
echo ========================================
echo.

REM Set project root directory
set PROJECT_ROOT=c:\Users\HomeLaptop\Downloads\navi-tax-35-main
set BACKEND_DIR=%PROJECT_ROOT%\docs\backend-example
set FRONTEND_DIR=%PROJECT_ROOT%\web

REM ========================================
REM STEP 1: Check Backend Prerequisites
REM ========================================
echo [STEP 1/4] Checking Backend Prerequisites...
echo.

if not exist "%BACKEND_DIR%\.env" (
    echo [ERROR] Backend .env file not found!
    echo.
    echo Please create: %BACKEND_DIR%\.env
    echo.
    echo Required contents:
    echo SUPABASE_URL=your_supabase_url
    echo SUPABASE_SERVICE_KEY=your_service_key
    echo PORT=3001
    echo.
    pause
    exit /b 1
)

if not exist "%BACKEND_DIR%\node_modules" (
    echo [INFO] Installing backend dependencies...
    cd /d "%BACKEND_DIR%"
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install backend dependencies!
        pause
        exit /b 1
    )
    echo [OK] Backend dependencies installed
    echo.
)

echo [OK] Backend prerequisites satisfied
echo.

REM ========================================
REM STEP 2: Check Frontend Prerequisites
REM ========================================
echo [STEP 2/4] Checking Frontend Prerequisites...
echo.

if not exist "%FRONTEND_DIR%\node_modules" (
    echo [INFO] Installing frontend dependencies...
    cd /d "%FRONTEND_DIR%"
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies!
        pause
        exit /b 1
    )
    echo [OK] Frontend dependencies installed
    echo.
)

echo [OK] Frontend prerequisites satisfied
echo.

REM ========================================
REM STEP 3: Start Backend Server
REM ========================================
echo [STEP 3/4] Starting Backend Server...
echo.

REM Check if backend is already running
netstat -ano | findstr ":3001" >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Port 3001 is already in use!
    echo.
    choice /C YN /M "Do you want to kill the existing process and restart"
    if errorlevel 2 (
        echo [INFO] Using existing backend server on port 3001
        goto :start_frontend
    )
    
    REM Kill process on port 3001
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3001"') do (
        echo [INFO] Killing process %%a on port 3001...
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)

echo [INFO] Starting backend on port 3001...
start "Navi Tax - Backend Server (Port 3001)" cmd /k "cd /d %BACKEND_DIR% && echo Backend Server Starting... && echo. && node server.js"

REM Wait for backend to start
echo [INFO] Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Verify backend is running
netstat -ano | findstr ":3001" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend server started successfully on http://localhost:3001
    echo.
) else (
    echo [ERROR] Backend server failed to start!
    echo Please check the backend window for errors.
    echo.
    pause
    exit /b 1
)

REM ========================================
REM STEP 4: Start Frontend Server
REM ========================================
:start_frontend
echo [STEP 4/4] Starting Frontend Server...
echo.

REM Check if frontend is already running
netstat -ano | findstr ":5173" >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Port 5173 is already in use!
    echo.
    choice /C YN /M "Do you want to kill the existing process and restart"
    if errorlevel 2 (
        echo [INFO] Using existing frontend server on port 5173
        goto :success
    )
    
    REM Kill process on port 5173
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173"') do (
        echo [INFO] Killing process %%a on port 5173...
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)

echo [INFO] Starting frontend on port 5173...
cd /d "%FRONTEND_DIR%"
start "Navi Tax - Frontend Server (Port 5173)" cmd /k "echo Frontend Server Starting... && echo. && npm run dev"

REM Wait for frontend to start
echo [INFO] Waiting for frontend to initialize...
timeout /t 8 /nobreak >nul

REM ========================================
REM SUCCESS
REM ========================================
:success
echo.
echo ========================================
echo   STARTUP COMPLETE!
echo ========================================
echo.
echo [OK] Backend Server:  http://localhost:3001
echo [OK] Frontend App:    http://localhost:5173
echo.
echo ========================================
echo   IMPORTANT NOTES:
echo ========================================
echo.
echo 1. Two terminal windows are now open:
echo    - Backend Server (Port 3001)
echo    - Frontend Server (Port 5173)
echo.
echo 2. KEEP BOTH WINDOWS OPEN while using the app
echo.
echo 3. To stop the servers:
echo    - Close both terminal windows, OR
echo    - Press Ctrl+C in each window
echo.
echo 4. Access the application at:
echo    http://localhost:5173
echo.
echo ========================================
echo   TROUBLESHOOTING:
echo ========================================
echo.
echo - If backend fails: Check %BACKEND_DIR%\.env
echo - If frontend fails: Run "npm install" in %FRONTEND_DIR%
echo - If ports are busy: Close other Node.js processes
echo.
echo ========================================

REM Open browser automatically
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo [INFO] Browser should open automatically...
echo.
echo Press any key to close this window (servers will keep running)
pause >nul