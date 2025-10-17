@echo off
echo ========================================
echo 🔮 IMPROVED TIME SERIES FORECASTING
echo ========================================
echo.
echo This script improves MAPE by:
echo   1. Auto-tuning ARIMA parameters
echo   2. Adding exogenous variables
echo   3. Walk-forward validation
echo   4. Ensemble forecasting
echo.
echo Press any key to start...
pause >nul

python ..\ml\time_series_forecasting_IMPROVED.py

echo.
echo ========================================
echo ✅ COMPLETE!
echo ========================================
echo.
echo Check results in: ..\models\time_series_models_IMPROVED\
echo.
pause