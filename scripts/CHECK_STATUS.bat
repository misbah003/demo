@echo off
echo ========================================
echo   CHECKING SERVER STATUS
echo ========================================
echo.

netstat -ano | findstr :3001 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [BACKEND]  ✓ Running on port 3001
    echo            http://localhost:3001
) else (
    echo [BACKEND]  ✗ Not running on port 3001
)

echo.

netstat -ano | findstr :8080 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [FRONTEND] ✓ Running on port 8080
    echo            http://localhost:8080
    echo.
    echo ========================================
    echo   ALL SERVERS RUNNING!
    echo ========================================
    echo.
    echo Open your browser to:
    echo   http://localhost:8080
) else (
    echo [FRONTEND] ✗ Not running on port 8080
    echo.
    echo If you just started the servers, wait 10-15 seconds
    echo and run this script again.
)

echo.
pause