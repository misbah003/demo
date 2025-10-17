@echo off
echo ========================================
echo 🚨 IMPROVED ANOMALY DETECTION
echo ========================================
echo.
echo This script fixes overfitting by:
echo   1. Removing data leakage
echo   2. Adding cross-validation
echo   3. Detecting overfitting
echo.
echo Press any key to start...
pause >nul

python ..\ml\anomaly_detection_classification_IMPROVED.py

echo.
echo ========================================
echo ✅ COMPLETE!
echo ========================================
echo.
echo Check results in: ..\models\anomaly_detection_models_IMPROVED\
echo.
pause