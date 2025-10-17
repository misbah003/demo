@echo off
echo ========================================
echo TRAIN OPTIMIZED ML MODEL
echo ========================================
echo.
echo This will train an optimized ML model with:
echo - Full hyperparameter tuning
echo - 5-fold cross-validation
echo - Expected R^2: 0.72-0.78 (72-78%%)
echo - Training time: 30-60 minutes
echo.
echo ========================================
echo.

cd /d "%~dp0\.."

echo Starting training...
echo.
python ml/train_optimized_models.py

echo.
echo ========================================
echo Training complete!
echo ========================================
echo.
echo Next steps:
echo 1. Test model: python ml/test_optimized_model.py
echo 2. Start API: python ml/ml_api_service_optimized.py
echo 3. Read guide: OPTIMIZED_MODEL_INTEGRATION_GUIDE.md
echo.

pause