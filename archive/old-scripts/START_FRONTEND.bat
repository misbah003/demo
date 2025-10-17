@echo off
echo ========================================
echo Starting Frontend (React + Vite)
echo ========================================
echo.

cd web

if not exist node_modules (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Starting frontend on port 5173...
echo.
echo ========================================
echo KEEP THIS WINDOW OPEN!
echo ========================================
echo The frontend must run while using the app.
echo.
echo To stop: Press Ctrl+C
echo.
echo Open in browser: http://localhost:5173
echo.

npm run dev