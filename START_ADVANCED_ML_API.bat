@echo off
echo ========================================
echo STARTING ADVANCED ML API SERVICE
echo ========================================
echo.
echo This will start the ML API with:
echo - Advanced NER (spaCy + BERT)
echo - Document Classification (CNN + Transformers)
echo - Time Series Forecasting (ARIMA + Prophet + LSTM)
echo.
echo API will be available at:
echo   http://localhost:8000
echo.
echo API Documentation:
echo   http://localhost:8000/docs
echo.
echo ========================================
echo KEEP THIS WINDOW OPEN!
echo ========================================
echo.

cd ml
python ml_api_service_advanced.py

pause