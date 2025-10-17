@echo off
echo ========================================
echo ADVANCED ML/AI SYSTEM SETUP
echo ========================================
echo.
echo This will install all required ML libraries:
echo - TensorFlow (Deep Learning)
echo - spaCy (NLP/NER)
echo - Transformers (BERT)
echo - Prophet (Time Series)
echo - ARIMA/LSTM models
echo.
echo This may take 10-15 minutes...
echo.
pause

cd ml

echo.
echo ========================================
echo Step 1: Installing Python Dependencies
echo ========================================
pip install -r requirements_advanced_ml.txt

echo.
echo ========================================
echo Step 2: Downloading spaCy English Model
echo ========================================
python -m spacy download en_core_web_sm

echo.
echo ========================================
echo Step 3: Testing Installations
echo ========================================
python -c "import tensorflow; print('✅ TensorFlow:', tensorflow.__version__)"
python -c "import spacy; print('✅ spaCy:', spacy.__version__)"
python -c "import transformers; print('✅ Transformers:', transformers.__version__)"
python -c "import prophet; print('✅ Prophet:', prophet.__version__)"
python -c "import statsmodels; print('✅ Statsmodels:', statsmodels.__version__)"

echo.
echo ========================================
echo ✅ SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Run: TEST_ADVANCED_ML.bat
echo 2. Start API: START_ADVANCED_ML_API.bat
echo.
pause