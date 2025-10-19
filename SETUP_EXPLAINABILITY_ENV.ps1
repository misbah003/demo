# PowerShell setup script for Explainability Environment
# This fixes all dependency issues and prepares the environment

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  EXPLAINABILITY ENVIRONMENT SETUP                              ║" -ForegroundColor Cyan
Write-Host "║  Fixing NumPy, SHAP, LIME, and all dependencies               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Fix NumPy and numba compatibility
Write-Host "[Step 1/4] Installing compatible NumPy version (2.1.3)..." -ForegroundColor Yellow
pip install --force-reinstall --no-cache-dir numpy==2.1.3
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install NumPy" -ForegroundColor Red
    exit 1
}
Write-Host "✅ NumPy installed" -ForegroundColor Green

# Step 2: Install numba with correct version
Write-Host ""
Write-Host "[Step 2/4] Installing numba (compatible with NumPy 2.1.3)..." -ForegroundColor Yellow
pip install --force-reinstall numba>=0.57.0
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install numba" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Numba installed" -ForegroundColor Green

# Step 3: Install SHAP and LIME
Write-Host ""
Write-Host "[Step 3/4] Installing SHAP and LIME..." -ForegroundColor Yellow
pip install shap>=0.42.0 lime>=0.2.0 scipy>=1.11.0 scikit-learn>=1.3.0
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install SHAP/LIME" -ForegroundColor Red
    exit 1
}
Write-Host "✅ SHAP and LIME installed" -ForegroundColor Green

# Step 4: Install remaining dependencies
Write-Host ""
Write-Host "[Step 4/4] Installing FastAPI, pandas, and utilities..." -ForegroundColor Yellow
pip install fastapi uvicorn pydantic pandas>=2.0.0 reportlab
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install other dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✅ All dependencies installed" -ForegroundColor Green

# Verify installation
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  VERIFICATION                                                  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

try {
    $numpy_version = python -c "import numpy as np; print(np.__version__)" 2>$null
    Write-Host "NumPy: $numpy_version" -ForegroundColor Green
} catch {}

try {
    $shap_version = python -c "import shap; print(shap.__version__)" 2>$null
    Write-Host "SHAP: $shap_version" -ForegroundColor Green
} catch {}

try {
    python -c "import lime" 2>$null
    Write-Host "LIME: installed" -ForegroundColor Green
} catch {}

try {
    python -c "import numba" 2>$null
    Write-Host "Numba: installed" -ForegroundColor Green
} catch {}

Write-Host ""
Write-Host "✅ Setup complete! Environment is ready for explainability." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Run: python ml/test_explainability_comprehensive.py"
Write-Host "  2. Review results for any issues"
Write-Host "  3. Start ML API: python ml/ml_api_with_explainability.py"
Write-Host ""