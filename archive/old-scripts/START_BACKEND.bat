@echo off
echo ========================================
echo Starting Backend Server for Document Processing
echo ========================================
echo.

cd docs\backend-example

if not exist node_modules (
    echo Installing dependencies...
    call npm install
    echo.
)

if not exist .env (
    echo.
    echo ========================================
    echo ERROR: .env file not found!
    echo ========================================
    echo.
    echo Please create a .env file with your Supabase credentials:
    echo.
    echo SUPABASE_URL=your_supabase_url
    echo SUPABASE_SERVICE_KEY=your_supabase_service_key
    echo PORT=3001
    echo.
    echo Get credentials from: https://supabase.com/dashboard
    echo Project Settings ^> API
    echo.
    pause
    exit /b 1
)

echo Starting backend server on port 3001...
echo.
echo ========================================
echo KEEP THIS WINDOW OPEN!
echo ========================================
echo The backend must run while using the app.
echo.
echo To stop: Press Ctrl+C
echo.

node server.js