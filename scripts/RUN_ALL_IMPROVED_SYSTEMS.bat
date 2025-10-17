@echo off
echo ========================================
echo 🚀 RUN ALL IMPROVED ML SYSTEMS
echo ========================================
echo.
echo This will run:
echo   1. Improved Anomaly Detection (fixes overfitting)
echo   2. Improved Time Series Forecasting (improves MAPE)
echo.
echo Press any key to start...
pause >nul

echo.
echo ========================================
echo 🚨 STEP 1: IMPROVED ANOMALY DETECTION
echo ========================================
echo.
python ..\ml\anomaly_detection_classification_IMPROVED.py

echo.
echo ========================================
echo 🔮 STEP 2: IMPROVED TIME SERIES FORECASTING
echo ========================================
echo.
python ..\ml\time_series_forecasting_IMPROVED.py

echo.
echo ========================================
echo ✅ ALL IMPROVED SYSTEMS COMPLETE!
echo ========================================
echo.
echo Results saved in:
echo   - ..\models\anomaly_detection_models_IMPROVED\
echo   - ..\models\time_series_models_IMPROVED\
echo.
pause