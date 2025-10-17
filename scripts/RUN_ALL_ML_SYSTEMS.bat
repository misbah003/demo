@echo off
echo ========================================
echo  Complete ML Pipeline
echo ========================================
echo  1. Time Series Forecasting (ARIMA/SARIMA/Prophet/LSTM)
echo  2. Anomaly Detection (Random Forest/XGBoost/Logistic Regression)
echo ========================================
echo.
echo Installing all required packages...
pip install statsmodels prophet tensorflow xgboost scikit-learn pandas openpyxl matplotlib seaborn --quiet
echo.
echo ========================================
echo  STEP 1: Time Series Forecasting
echo ========================================
echo.
python ..\ml\time_series_forecasting.py
echo.
echo ========================================
echo  STEP 2: Anomaly Detection Classification
echo ========================================
echo.
python ..\ml\anomaly_detection_classification.py
echo.
echo ========================================
echo  ALL SYSTEMS COMPLETE!
echo ========================================
echo.
echo Output folders:
echo   - ..\models\time_series_models\
echo   - ..\models\anomaly_detection_models\
echo.
pause