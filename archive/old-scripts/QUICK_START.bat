@echo off
REM Quick Start Guide for VAT ML System
echo.
echo ========================================
echo   VAT ML System - Quick Start
echo ========================================
echo.
echo IMPORTANT: Read this first!
echo.
echo 1. Model Accuracy: R^2 = 0.258 (25.8%%)
echo    - This is LOW accuracy
echo    - Based on SYNTHETIC data
echo    - NOT for real financial decisions
echo.
echo 2. License: MIT License
echo    - You CAN deploy as your own
echo    - You CAN use commercially
echo    - You CAN modify freely
echo.
echo 3. Docker Status: Installed
echo    - Ready for deployment
echo.
echo ========================================
echo   Choose Deployment Option:
echo ========================================
echo.
echo [1] Deploy with Docker (Recommended)
echo [2] Run locally without Docker
echo [3] View deployment guide
echo [4] Check model status
echo [5] Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto docker_deploy
if "%choice%"=="2" goto local_deploy
if "%choice%"=="3" goto view_guide
if "%choice%"=="4" goto check_model
if "%choice%"=="5" goto end

:docker_deploy
echo.
echo Starting Docker deployment...
echo.
call deploy.bat
goto end

:local_deploy
echo.
echo Starting local deployment...
echo.
echo Checking if model exists...
if not exist "models\ml_models\vat_refund_predictor.pkl" (
    echo.
    echo ERROR: Model not found!
    echo Please train the model first:
    echo   cd ml
    echo   python train_vat_ml_models.py
    echo.
    pause
    goto end
)
echo.
echo Starting ML API service...
cd ml
python ml_api_service.py
goto end

:view_guide
echo.
echo Opening deployment guide...
start DEPLOYMENT_GUIDE.md
goto end

:check_model
echo.
echo ========================================
echo   Model Status Check
echo ========================================
echo.
if exist "models\ml_models\vat_refund_predictor.pkl" (
    echo [OK] Model file exists
) else (
    echo [ERROR] Model file NOT found
    echo Please train the model first:
    echo   cd ml
    echo   python train_vat_ml_models.py
)
echo.
if exist "models\ml_models\model_metadata.json" (
    echo [OK] Metadata file exists
    echo.
    echo Model Performance:
    type models\ml_models\model_metadata.json | findstr "model_name r2_score mae"
) else (
    echo [ERROR] Metadata file NOT found
)
echo.
echo ========================================
pause
goto end

:end
echo.
echo Thank you for using VAT ML System!
echo.
pause