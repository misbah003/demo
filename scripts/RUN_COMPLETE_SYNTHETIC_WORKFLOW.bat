@echo off
echo ============================================================
echo 🤖 COMPLETE SYNTHETIC DATA WORKFLOW
echo ============================================================
echo.
echo This will run the complete workflow:
echo   1. Generate synthetic data
echo   2. Train models with synthetic data
echo   3. Compare original vs synthetic performance
echo.
echo ⚠️  This may take 5-15 minutes depending on data size
echo.
echo ============================================================
echo.
pause

echo.
echo ============================================================
echo STEP 1/3: GENERATING SYNTHETIC DATA
echo ============================================================
echo.
python ..\ml\generate_synthetic_data.py

if errorlevel 1 (
    echo.
    echo ❌ Error generating synthetic data!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo STEP 2/3: TRAINING MODELS WITH SYNTHETIC DATA
echo ============================================================
echo.
python ..\ml\train_with_synthetic_data.py

if errorlevel 1 (
    echo.
    echo ❌ Error training models!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo STEP 3/3: COMPARING ORIGINAL VS SYNTHETIC
echo ============================================================
echo.
python ..\ml\compare_original_vs_synthetic.py

if errorlevel 1 (
    echo.
    echo ❌ Error comparing results!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 🎉 COMPLETE WORKFLOW FINISHED!
echo ============================================================
echo.
echo ✅ Synthetic data generated
echo ✅ Models trained
echo ✅ Comparison complete
echo.
echo 📁 Check these folders for results:
echo    - synthetic_data/
echo    - synthetic_models_XXX_samples/
echo    - comparison_*.csv and comparison_*.png
echo.
echo ============================================================
pause