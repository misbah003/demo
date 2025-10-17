@echo off
REM ========================================
REM Train All ML Models
REM ========================================

echo.
echo ========================================
echo   TRAIN ALL ML MODELS
echo ========================================
echo.
echo This will train:
echo   1. Document Classification (CNN)
echo   2. Sentiment Analysis
echo   3. Time Series Forecasting
echo   4. Anomaly Detection
echo.
echo Estimated time: 10-30 minutes
echo.
pause

cd /d "%~dp0"

echo.
echo ========================================
echo Starting Training Pipeline...
echo ========================================
echo.

python ml\train_all_models.py

echo.
echo ========================================
echo Training Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Test models: python ml\test_document_classifier.py
echo   2. Integrate: python ml\integrate_trained_models.py
echo   3. Start ML API: START_ADVANCED_ML_API.bat
echo.
pause