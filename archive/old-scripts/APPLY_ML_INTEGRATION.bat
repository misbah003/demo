@echo off
echo ========================================
echo ML/AI INTEGRATION - QUICK START
echo ========================================
echo.
echo This script will help you integrate the ML system.
echo.
echo WHAT THIS DOES:
echo   1. Checks if ML API is running
echo   2. Tests ML API endpoints
echo   3. Guides you through code changes
echo.
echo ========================================
echo.

echo Step 1: Checking ML API Status...
echo.

curl -s http://localhost:8000/ > nul 2>&1
if %errorlevel% equ 0 (
    echo [32m✅ ML API is RUNNING on port 8000[0m
    echo.
    curl http://localhost:8000/
    echo.
) else (
    echo [33m⚠️  ML API is NOT running[0m
    echo.
    echo Please start the ML API first:
    echo   START_ADVANCED_ML_API.bat
    echo.
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Testing ML API Endpoints...
echo ========================================
echo.

echo Testing /api/extract-entities...
curl -s -X POST http://localhost:8000/api/extract-entities ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Invoice INV-001 GST: 27AABCU9603R1ZM Amount: Rs. 50000 Date: 2024-01-15\"}" > nul 2>&1

if %errorlevel% equ 0 (
    echo [32m✅ Entity extraction endpoint working[0m
) else (
    echo [31m❌ Entity extraction endpoint failed[0m
)

echo.
echo Testing /api/classify-document...
curl -s -X POST http://localhost:8000/api/classify-document ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"VAT Invoice for goods sold\"}" > nul 2>&1

if %errorlevel% equ 0 (
    echo [32m✅ Classification endpoint working[0m
) else (
    echo [31m❌ Classification endpoint failed[0m
)

echo.
echo ========================================
echo Step 3: Code Changes Required
echo ========================================
echo.
echo You need to make changes to 4 files:
echo.
echo   1. docs\backend-example\server.js
echo   2. web\supabase\functions\user-vat-forecast\index.ts
echo   3. web\src\components\DocumentProcessor.tsx
echo   4. docs\backend-example\.env
echo.
echo [33mDETAILED INSTRUCTIONS:[0m
echo   Open: INTEGRATION_CODE_CHANGES.md
echo.
echo This file contains:
echo   - Exact code to add/replace
echo   - Line numbers
echo   - Before/After examples
echo.
echo ========================================
echo Step 4: Quick Reference
echo ========================================
echo.
echo [36mDOCUMENTATION FILES:[0m
echo   📘 🚀_ML_INTEGRATION_GUIDE.md      - Complete integration guide
echo   📝 INTEGRATION_CODE_CHANGES.md     - Exact code changes
echo   ✅ ✅_ML_INSTALLATION_COMPLETE.md  - Installation summary
echo.
echo [36mAPI DOCUMENTATION:[0m
echo   🌐 http://localhost:8000/docs      - Swagger UI (interactive)
echo   🌐 http://localhost:8000/          - API health check
echo.
echo [36mTESTING:[0m
echo   1. Make the code changes (see INTEGRATION_CODE_CHANGES.md)
echo   2. Restart backend: START_BACKEND.bat
echo   3. Upload a test document
echo   4. Check console for "ML API Status: ONLINE ✅"
echo.
echo ========================================
echo.

echo [32mML API is ready for integration! 🚀[0m
echo.
echo Next steps:
echo   1. Open INTEGRATION_CODE_CHANGES.md
echo   2. Follow the code changes
echo   3. Test with a document upload
echo.

pause