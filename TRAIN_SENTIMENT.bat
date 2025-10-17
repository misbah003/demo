@echo off
REM ========================================
REM Train Sentiment Analysis Model ONLY
REM ========================================

echo.
echo ========================================
echo   TRAIN SENTIMENT ANALYSIS
echo ========================================
echo.
echo This will train sentiment analysis model
echo Estimated time: 1-2 minutes
echo.
pause

cd /d "%~dp0"

echo.
echo Starting training...
echo.

python ml\sentiment_analysis.py

echo.
echo ========================================
echo Training Complete!
echo ========================================
echo.
pause