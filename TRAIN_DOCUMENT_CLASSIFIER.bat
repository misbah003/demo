@echo off
REM ========================================
REM Train Document Classification Model ONLY
REM ========================================

echo.
echo ========================================
echo   TRAIN DOCUMENT CLASSIFIER
echo ========================================
echo.
echo This will train CNN model for document classification
echo Estimated time: 5-10 minutes
echo.
pause

cd /d "%~dp0"

echo.
echo Starting training...
echo.

python ml\train_document_classifier.py

echo.
echo ========================================
echo Training Complete!
echo ========================================
echo.
pause