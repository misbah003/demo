@echo off
echo ========================================
echo START OPTIMIZED ML API SERVICE
echo ========================================
echo.
echo Starting ML API with optimized model...
echo API will be available at: http://localhost:5001
echo.
echo Endpoints:
echo - POST /predict        - Make a prediction
echo - POST /batch-predict  - Batch predictions
echo - GET  /model-info     - Get model metadata
echo - GET  /stats          - Get statistics
echo - GET  /health         - Health check
echo.
echo ========================================
echo.

cd /d "%~dp0\.."

python ml/ml_api_service_optimized.py

pause