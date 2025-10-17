@echo off
echo ========================================
echo Document Processing Fix - Test Script
echo ========================================
echo.

echo Step 1: Checking if backend is running...
curl -s http://localhost:3001/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Backend server is not running!
    echo.
    echo Please start the backend server first:
    echo   cd backend-example
    echo   node server.js
    echo.
    echo Or in a new terminal window:
    echo   npm start --prefix backend-example
    echo.
    pause
    exit /b 1
)

echo [OK] Backend server is running
echo.

echo Step 2: Running test script...
echo.
python test_processing.py

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
echo Check the output above for results.
echo.
echo Expected results:
echo   - 4-5 documents marked as "Compliant"
echo   - Confidence scores 70-100%%
echo   - 8-15 entities extracted per document
echo.
pause