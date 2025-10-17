@echo off
echo ========================================
echo   STARTING TAX INTELLIGENCE PLATFORM
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

echo [1/5] Checking Node.js version...
node --version
echo.

REM Check if backend dependencies are installed
if not exist "backend-example\node_modules" (
    echo [2/5] Installing backend dependencies...
    cd backend-example
    call npm install
    cd ..
    echo.
) else (
    echo [2/5] Backend dependencies already installed ✓
    echo.
)

REM Check if frontend dependencies are installed
if not exist "node_modules" (
    echo [3/5] Installing frontend dependencies (this may take a few minutes)...
    call npm install
    echo.
) else (
    echo [3/5] Frontend dependencies already installed ✓
    echo.
)

echo [4/5] Starting backend server on port 3001...
start "Backend Server" cmd /k "cd backend-example && node server.js"
timeout /t 3 /nobreak >nul
echo Backend server started ✓
echo.

echo [5/5] Starting frontend server on port 8080...
start "Frontend Server" cmd /k "npm run dev"
timeout /t 5 /nobreak >nul
echo Frontend server starting ✓
echo.

echo ========================================
echo   SERVERS STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Backend:  http://localhost:3001
echo Frontend: http://localhost:8080
echo.
echo Two new windows have opened:
echo   1. Backend Server (port 3001)
echo   2. Frontend Server (port 8080)
echo.
echo Wait 10-15 seconds, then open your browser to:
echo   http://localhost:8080
echo.
echo To stop the servers, close both terminal windows.
echo.
pause