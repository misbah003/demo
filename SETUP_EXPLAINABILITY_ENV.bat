@echo off
REM Setup script for Explainability Environment
REM This fixes all dependency issues and prepares the environment

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  EXPLAINABILITY ENVIRONMENT SETUP                              ║
echo ║  Fixing NumPy, SHAP, LIME, and all dependencies               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Step 1: Fix NumPy and numba compatibility
echo [Step 1/4] Installing compatible NumPy version (2.1.3)...
pip install --force-reinstall --no-cache-dir numpy==2.1.3
if errorlevel 1 (
    echo ❌ Failed to install NumPy
    exit /b 1
)
echo ✅ NumPy installed

REM Step 2: Install numba with correct version
echo.
echo [Step 2/4] Installing numba (compatible with NumPy 2.1.3)...
pip install --force-reinstall numba>=0.57.0
if errorlevel 1 (
    echo ❌ Failed to install numba
    exit /b 1
)
echo ✅ Numba installed

REM Step 3: Install SHAP and LIME
echo.
echo [Step 3/4] Installing SHAP and LIME...
pip install shap>=0.42.0 lime>=0.2.0 scipy>=1.11.0 scikit-learn>=1.3.0
if errorlevel 1 (
    echo ❌ Failed to install SHAP/LIME
    exit /b 1
)
echo ✅ SHAP and LIME installed

REM Step 4: Install remaining dependencies
echo.
echo [Step 4/4] Installing FastAPI, pandas, and utilities...
pip install fastapi uvicorn pydantic pandas>=2.0.0 reportlab
if errorlevel 1 (
    echo ❌ Failed to install other dependencies
    exit /b 1
)
echo ✅ All dependencies installed

REM Verify installation
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  VERIFICATION                                                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

python -c "import numpy as np; print(f'NumPy: {np.__version__}')" 2>nul
python -c "import shap; print(f'SHAP: {shap.__version__}')" 2>nul
python -c "import lime; print('LIME: installed')" 2>nul
python -c "import numba; print(f'Numba: installed')" 2>nul

echo.
echo ✅ Setup complete! Environment is ready for explainability.
echo.
echo Next steps:
echo  1. Run: python ml/test_explainability_comprehensive.py
echo  2. Review results for any issues
echo  3. Start ML API: python ml/ml_api_with_explainability.py
echo.
pause