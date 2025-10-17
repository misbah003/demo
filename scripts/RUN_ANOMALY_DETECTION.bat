@echo off
echo ========================================
echo  Anomaly Detection Classification
echo ========================================
echo.
echo Installing required packages...
pip install xgboost scikit-learn pandas openpyxl matplotlib seaborn --quiet
echo.
echo ========================================
echo  Running Anomaly Detection...
echo ========================================
echo.
python ..\ml\anomaly_detection_classification.py
echo.
echo ========================================
echo  Complete! Check ..\models\anomaly_detection_models\ folder
echo ========================================
pause