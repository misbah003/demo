@echo off
echo ======================================================================
echo 🚀 STARTING VAT REFUND ML API SERVICE
echo ======================================================================
echo.

cd /d "%~dp0"

echo 📦 Checking if model exists...
if not exist "..\models\ml_models\vat_refund_predictor.pkl" (
    echo ❌ Model not found!
    echo.
    echo Please run: python ..\ml\train_vat_ml_models.py
    echo.
    pause
    exit /b 1
)

echo ✅ Model found!
echo.
echo 🚀 Starting Flask API on http://localhost:5001
echo.
echo Press Ctrl+C to stop the server
echo ======================================================================
echo.

python ..\ml\ml_api_service.py

pause