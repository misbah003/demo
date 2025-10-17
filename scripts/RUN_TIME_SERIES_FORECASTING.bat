@echo off
echo ========================================
echo  Time Series Forecasting - VAT Collections
echo ========================================
echo.
echo Installing required packages...
pip install statsmodels prophet tensorflow scikit-learn pandas openpyxl matplotlib seaborn --quiet
echo.
echo ========================================
echo  Running Time Series Forecasting...
echo ========================================
echo.
python ..\ml\time_series_forecasting.py
echo.
echo ========================================
echo  Complete! Check ..\models\time_series_models\ folder
echo ========================================
pause