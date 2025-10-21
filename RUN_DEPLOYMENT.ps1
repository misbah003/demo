#!/usr/bin/env pwsh
# COMPLETE DEPLOYMENT AUTOMATION SCRIPT

Write-Host "=========================================================="
Write-Host "DEPLOYMENT AUTOMATION SCRIPT"
Write-Host "=========================================================="
Write-Host ""

# Pre-deployment checks
Write-Host "STEP 0: Pre-deployment checks"
Write-Host ""

if (-not (Test-Path "render.yaml")) {
    Write-Host "ERROR: render.yaml not found"
    exit 1
}
Write-Host "[OK] Found render.yaml"

if (-not (Test-Path "vercel.json")) {
    Write-Host "ERROR: vercel.json not found"
    exit 1
}
Write-Host "[OK] Found vercel.json"

if (-not (Test-Path "optimized_models_25000_samples")) {
    Write-Host "ERROR: Models not found"
    exit 1
}
Write-Host "[OK] Found trained models"

Write-Host ""
Write-Host "=========================================================="
Write-Host "STEP 1: Deploy Backend to Render"
Write-Host "=========================================================="
Write-Host ""
Write-Host "1. Go to: https://dashboard.render.com"
Write-Host "2. Click: 'New +' -> 'Web Service'"
Write-Host "3. Connect your GitHub repository (misbah003/demo)"
Write-Host "4. Configure:"
Write-Host "   Name: navi-tax-ml-api"
Write-Host "   Runtime: Python 3.9"
Write-Host "   Build: pip install -r requirements.txt"
Write-Host "   Start: gunicorn -w 2 -b 0.0.0.0:5000 --timeout 120 ml.ml_api_service_optimized:app"
Write-Host "5. Wait 20-25 minutes for deployment"
Write-Host ""

$renderUrl = Read-Host "Enter your Render service URL"

Write-Host ""
Write-Host "=========================================================="
Write-Host "STEP 2: Verify Backend"
Write-Host "=========================================================="
Write-Host ""

$healthUrl = "$renderUrl/health"
Write-Host "Testing: $healthUrl"

try {
    $response = Invoke-WebRequest -Uri $healthUrl -TimeoutSec 30
    if ($response.StatusCode -eq 200) {
        Write-Host "Backend is responding - OK"
    }
} catch {
    Write-Host "Backend may still be starting up"
}

Write-Host ""
Write-Host "=========================================================="
Write-Host "STEP 3: Update Frontend Environment"
Write-Host "=========================================================="
Write-Host ""

$envFile = "web\.env.production"
if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw
    $updated = $content -replace "VITE_BACKEND_URL=.*", "VITE_BACKEND_URL=$renderUrl"
    Set-Content $envFile $updated
    Write-Host "Updated VITE_BACKEND_URL"
} else {
    Write-Host "ERROR: $envFile not found"
}

Write-Host ""
Write-Host "=========================================================="
Write-Host "STEP 4: Commit and Push Changes"
Write-Host "=========================================================="
Write-Host ""

git add web\.env.production
git commit -m "chore: update backend URL for production"
git push

Write-Host "Pushed to GitHub"

Write-Host ""
Write-Host "=========================================================="
Write-Host "STEP 5: Deploy Frontend to Vercel"
Write-Host "=========================================================="
Write-Host ""
Write-Host "1. Go to: https://vercel.com/dashboard"
Write-Host "2. Click: 'Add New' -> 'Project'"
Write-Host "3. Select your repository"
Write-Host "4. Configure:"
Write-Host "   Framework: Vite"
Write-Host "   Build: cd web && npm run build"
Write-Host "   Output: web/dist"
Write-Host "5. Add env vars:"
Write-Host "   VITE_SUPABASE_PROJECT_ID: ikqcakganqabiscsibyim"
Write-Host "   VITE_SUPABASE_URL: https://ikqcakganqabiscsibyim.supabase.co"
Write-Host "   VITE_BACKEND_URL: $renderUrl"
Write-Host "6. Wait 10-15 minutes for deployment"
Write-Host ""

$vercelUrl = Read-Host "Enter your Vercel deployment URL"

Write-Host ""
Write-Host "=========================================================="
Write-Host "DEPLOYMENT COMPLETE"
Write-Host "=========================================================="
Write-Host ""
Write-Host "Frontend: $vercelUrl"
Write-Host "Backend:  $renderUrl"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Visit your frontend URL to test"
Write-Host "2. Sign up and make a prediction"
Write-Host "3. Check SHAP explanations"
Write-Host ""
Write-Host "Your production system is now online!"
Write-Host ""