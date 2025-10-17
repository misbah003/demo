@echo off
echo ========================================
echo Starting Email Backend Server
echo ========================================
echo.

cd backend-example

if not exist node_modules (
    echo Installing dependencies...
    call npm install
    echo.
)

if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please configure your Gmail credentials:
    echo 1. Copy backend-example\.env.example to backend-example\.env
    echo 2. Edit .env and add your Gmail credentials
    echo 3. See SETUP_EMAIL_INSTRUCTIONS.md for detailed steps
    echo.
    pause
    exit /b 1
)

echo Starting backend server on port 3001...
echo Keep this window open while using the app.
echo.
node server.js