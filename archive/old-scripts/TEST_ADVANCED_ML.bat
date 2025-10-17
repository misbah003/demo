@echo off
echo ========================================
echo TESTING ADVANCED ML MODELS
echo ========================================
echo.

cd ml

echo.
echo ========================================
echo Test 1: Advanced NER Extraction
echo ========================================
python advanced_ner_extraction.py
echo.
pause

echo.
echo ========================================
echo Test 2: Advanced Time Series Forecasting
echo ========================================
python advanced_time_series_forecasting.py
echo.
pause

echo.
echo ========================================
echo Test 3: Advanced Document Classification
echo ========================================
python advanced_document_classifier.py
echo.
pause

echo.
echo ========================================
echo ✅ ALL TESTS COMPLETE!
echo ========================================
echo.
echo Check the output above for any errors.
echo If all tests passed, you can start the API.
echo.
pause