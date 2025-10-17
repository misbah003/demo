@echo off
REM ========================================
REM Verify Complete ML Implementation
REM ========================================

echo.
echo ========================================
echo   VERIFY ML IMPLEMENTATION
echo ========================================
echo.
echo This script will verify that all ML
echo components are properly implemented.
echo.
pause

cd /d "%~dp0"

echo.
echo ========================================
echo Step 1: Checking Project Structure
echo ========================================
echo.

echo Checking ML scripts...
if exist "ml\train_all_models.py" (
    echo [OK] train_all_models.py found
) else (
    echo [MISSING] train_all_models.py
)

if exist "ml\train_document_classifier.py" (
    echo [OK] train_document_classifier.py found
) else (
    echo [MISSING] train_document_classifier.py
)

if exist "ml\sentiment_analysis.py" (
    echo [OK] sentiment_analysis.py found
) else (
    echo [MISSING] sentiment_analysis.py
)

if exist "ml\test_document_classifier.py" (
    echo [OK] test_document_classifier.py found
) else (
    echo [MISSING] test_document_classifier.py
)

if exist "ml\test_sentiment_analysis.py" (
    echo [OK] test_sentiment_analysis.py found
) else (
    echo [MISSING] test_sentiment_analysis.py
)

if exist "ml\integrate_trained_models.py" (
    echo [OK] integrate_trained_models.py found
) else (
    echo [MISSING] integrate_trained_models.py
)

echo.
echo ========================================
echo Step 2: Checking Trained Models
echo ========================================
echo.

if exist "models\document_classifier\cnn_model.h5" (
    echo [OK] Document Classifier: TRAINED
) else (
    echo [NOT TRAINED] Document Classifier
)

if exist "models\sentiment_analysis\sentiment_model.pkl" (
    echo [OK] Sentiment Analysis: TRAINED
) else (
    echo [NOT TRAINED] Sentiment Analysis
)

if exist "models\time_series_models\metadata.json" (
    echo [OK] Time Series: TRAINED
) else (
    echo [NOT TRAINED] Time Series
)

if exist "models\anomaly_detection_models\best_model.pkl" (
    echo [OK] Anomaly Detection: TRAINED
) else (
    echo [NOT TRAINED] Anomaly Detection
)

if exist "models\ml_models\vat_refund_predictor.pkl" (
    echo [OK] VAT Prediction: TRAINED
) else (
    echo [NOT TRAINED] VAT Prediction
)

echo.
echo ========================================
echo Step 3: Running Integration Check
echo ========================================
echo.

python ml\integrate_trained_models.py

echo.
echo ========================================
echo VERIFICATION COMPLETE
echo ========================================
echo.
echo Next steps:
echo   1. If models not trained: TRAIN_ALL_MODELS.bat
echo   2. Test models: python ml\test_document_classifier.py
echo   3. Start services: START_ALL_SERVERS.ps1
echo.
pause