@echo off
echo ============================================================
echo 🤖 SYNTHETIC DATA GENERATOR
echo ============================================================
echo.
echo This will generate realistic synthetic tax data for training
echo.
echo ⚠️  WARNING: Use ONLY for training/testing purposes!
echo    Do NOT use synthetic data for production decisions!
echo.
echo ============================================================
echo.

python ..\ml\generate_synthetic_data.py

echo.
echo ============================================================
echo.
pause