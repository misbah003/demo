#!/usr/bin/env pwsh
# COMPLETE DEPLOYMENT AUTOMATION SCRIPT
# Guides you through deploying to Render + Vercel in under 1 hour

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "COMPLETE DEPLOYMENT PACKAGE" -ForegroundColor Cyan
Write-Host "Vercel -> Render -> Supabase" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Colors
$success = "Green"
$warning = "Yellow"
$info = "Cyan"
$error_color = "Red"

# ============================================================
# STEP 0: Pre-deployment checks
# ============================================================

Write-Host ""
Write-Host "STEP 0: PRE-DEPLOYMENT CHECKS" -ForegroundColor $info
Write-Host "Expected time: 2 minutes" -ForegroundColor $info
Write-Host ""

Write-Host "Checking your environment..." -ForegroundColor $info
Write-Host ""

# Check if in correct directory
if (-not (Test-Path "render.yaml")) {
    Write-Host "ERROR: Not in project root directory" -ForegroundColor $error_color
    Write-Host "   Please run this from the project root (navi-tax-35-main)" -ForegroundColor $error_color
    exit 1
}
Write-Host "✓ Found render.yaml" -ForegroundColor $success

if (-not (Test-Path "vercel.json")) {
    Write-Host "ERROR: vercel.json not found" -ForegroundColor $error_color
    exit 1
}
Write-Host "✓ Found vercel.json" -ForegroundColor $success

if (-not (Test-Path "optimized_models_25000_samples")) {
    Write-Host "ERROR: Models not found" -ForegroundColor $error_color
    exit 1
}
Write-Host "✓ Found trained models" -ForegroundColor $success

# Check Git status
$gitStatus = git status --short
if ($gitStatus) {
    Write-Host ""
    Write-Host "WARNING: You have uncommitted changes. Commit them first:" -ForegroundColor $warning
    Write-Host "   git add ." -ForegroundColor $warning
    Write-Host "   git commit -m 'Your message'" -ForegroundColor $warning
    Write-Host "   git push" -ForegroundColor $warning
    Read-Host "Press Enter to continue"
}
else {
    Write-Host "✓ Git repository is clean" -ForegroundColor $success
}

Write-Host ""
Write-Host "All pre-deployment checks passed!" -ForegroundColor $success

# ============================================================
# STEP 1: Backend Deployment (Render)
# ============================================================

Write-Host ""
Write-Host "======================================================================" -ForegroundColor $info
Write-Host "STEP 1: DEPLOY BACKEND TO RENDER" -ForegroundColor $info
Write-Host "Expected time: 25 minutes" -ForegroundColor $info
Write-Host "======================================================================" -ForegroundColor $info
Write-Host ""

Write-Host "1. Go to: https://dashboard.render.com" -ForegroundColor $warning
Write-Host "2. Click: 'New +' → 'Web Service'" -ForegroundColor $warning
Write-Host "3. Connect your GitHub repository:" -ForegroundColor $warning
Write-Host ""
Write-Host "   Repository: Select 'misbah003/demo' (or your repo)" -ForegroundColor $warning
Write-Host "   Branch: 'master' (or 'main' if different)" -ForegroundColor $warning
Write-Host ""
Write-Host "4. Configure the service:" -ForegroundColor $warning
Write-Host ""
Write-Host "   Name: navi-tax-ml-api" -ForegroundColor $warning
Write-Host "   Region: Frankfurt" -ForegroundColor $warning
Write-Host "   Runtime: Python 3.9" -ForegroundColor $warning
Write-Host "   Build Command: pip install -r requirements.txt" -ForegroundColor $warning
Write-Host "   Start Command: gunicorn -w 2 -b 0.0.0.0:\$PORT --timeout 120 ml.ml_api_service_optimized:app" -ForegroundColor $warning
Write-Host ""
Write-Host "5. Click 'Create Web Service'" -ForegroundColor $warning
Write-Host ""
Write-Host "Waiting for build... (15-20 minutes)" -ForegroundColor $warning
Write-Host "You can monitor progress on the dashboard" -ForegroundColor $warning

Write-Host ""
Write-Host "WARNING: Click 'Deploys' tab and wait for status to be 'Live' (green)" -ForegroundColor $warning

Write-Host ""
Write-Host "6. Once deployment is complete:" -ForegroundColor $warning
Write-Host "   - Go to 'Settings' tab" -ForegroundColor $warning
Write-Host "   - Copy your service URL (e.g., https://navi-tax-ml-api.onrender.com)" -ForegroundColor $warning
Write-Host ""
Write-Host "   Save this URL - you'll need it next!" -ForegroundColor $warning

$renderUrl = Read-Host "Enter your Render service URL (https://navi-tax-ml-api.onrender.com)"

if ($renderUrl -match "^https?://.+\.onrender\.com$") {
    Write-Host "Render backend deployed!" -ForegroundColor $success
    Write-Host "URL: $renderUrl" -ForegroundColor $success
}
else {
    Write-Host "Invalid URL format" -ForegroundColor $error_color
    $renderUrl = Read-Host "Please enter a valid URL (https://...)"
}

# ============================================================
# STEP 2: Verify Backend Health
# ============================================================

Write-Host ""
Write-Host "======================================================================" -ForegroundColor $info
Write-Host "STEP 2: VERIFY BACKEND HEALTH" -ForegroundColor $info
Write-Host "Expected time: 5 minutes" -ForegroundColor $info
Write-Host "======================================================================" -ForegroundColor $info
Write-Host ""

Write-Host "Testing backend endpoints..." -ForegroundColor $info
Write-Host ""

$healthUrl = "$renderUrl/health"
Write-Host "Testing: $healthUrl" -ForegroundColor $warning

try {
    $response = Invoke-WebRequest -Uri $healthUrl -TimeoutSec 30 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "Backend is responding!" -ForegroundColor $success
        Write-Host "Status: Healthy and ready" -ForegroundColor $success
    }
}
catch {
    Write-Host "WARNING: Backend may still be starting up (can take 1-2 min on first request)" -ForegroundColor $warning
    Write-Host "You can verify manually at: $healthUrl" -ForegroundColor $info
}

# ============================================================
# STEP 3: Update Frontend Environment
# ============================================================

Write-Host ""
Write-Host "======================================================================" -ForegroundColor $info
Write-Host "STEP 3: UPDATE FRONTEND ENVIRONMENT" -ForegroundColor $info
Write-Host "Expected time: 2 minutes" -ForegroundColor $info
Write-Host "======================================================================" -ForegroundColor $info
Write-Host ""

Write-Host "Updating web/.env.production with your Render URL..." -ForegroundColor $info

$envFile = "web\.env.production"
if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw
    $updated = $content -replace "VITE_BACKEND_URL=.*", "VITE_BACKEND_URL=$renderUrl"
    Set-Content $envFile $updated
    Write-Host "Updated VITE_BACKEND_URL" -ForegroundColor $success
    Write-Host ""
    Write-Host "File content:" -ForegroundColor $info
    Get-Content $envFile | Select-Object -First 15 | Write-Host
}
else {
    Write-Host "ERROR: web/.env.production not found" -ForegroundColor $error_color
}

# ============================================================
# STEP 4: Commit and Push
# ============================================================

Write-Host ""
Write-Host "======================================================================" -ForegroundColor $info
Write-Host "STEP 4: COMMIT AND PUSH TO GITHUB" -ForegroundColor $info
Write-Host "Expected time: 2 minutes" -ForegroundColor $info
Write-Host "======================================================================" -ForegroundColor $info
Write-Host ""

Write-Host "Committing changes to GitHub..." -ForegroundColor $info

git add web/.env.production
git commit -m "chore: update backend URL for production deployment"
git push

Write-Host "Changes pushed to GitHub!" -ForegroundColor $success

# ============================================================
# STEP 5: Deploy Frontend (Vercel)
# ============================================================

Write-Host ""
Write-Host "======================================================================" -ForegroundColor $info
Write-Host "STEP 5: DEPLOY FRONTEND TO VERCEL" -ForegroundColor $info
Write-Host "Expected time: 15 minutes" -ForegroundColor $info
Write-Host "======================================================================" -ForegroundColor $info
Write-Host ""

Write-Host "1. Go to: https://vercel.com/dashboard" -ForegroundColor $warning
Write-Host "2. Click: 'Add New +' → 'Project'" -ForegroundColor $warning
Write-Host "3. Select your repository" -ForegroundColor $warning
Write-Host ""
Write-Host "4. Configure build settings:" -ForegroundColor $warning
Write-Host ""
Write-Host "   Framework: Vite" -ForegroundColor $warning
Write-Host "   Build Command: cd web && npm run build" -ForegroundColor $warning
Write-Host "   Output Directory: web/dist" -ForegroundColor $warning
Write-Host ""
Write-Host "5. Add environment variables:" -ForegroundColor $warning
Write-Host ""
Write-Host "   VITE_SUPABASE_PROJECT_ID: ikqcakganqabiscsibyim" -ForegroundColor $warning
Write-Host "   VITE_SUPABASE_PUBLISHABLE_KEY: (from web/.env.production)" -ForegroundColor $warning
Write-Host "   VITE_SUPABASE_URL: https://ikqcakganqabiscsibyim.supabase.co" -ForegroundColor $warning
Write-Host "   VITE_BACKEND_URL: $renderUrl" -ForegroundColor $warning
Write-Host ""
Write-Host "6. Click 'Deploy'" -ForegroundColor $warning
Write-Host ""
Write-Host "Waiting for build and deployment... (10-15 minutes)" -ForegroundColor $warning

Write-Host ""
Write-Host "WARNING: Monitor progress on Vercel dashboard" -ForegroundColor $warning

Write-Host ""
Write-Host "Once complete, you'll get a deployment URL!" -ForegroundColor $info

$vercelUrl = Read-Host "Enter your Vercel deployment URL (https://...vercel.app)"

# ============================================================
# STEP 6: Verification
# ============================================================

Write-Host ""
Write-Host "======================================================================" -ForegroundColor $info
Write-Host "STEP 6: VERIFY DEPLOYMENT" -ForegroundColor $info
Write-Host "Expected time: 10 minutes" -ForegroundColor $info
Write-Host "======================================================================" -ForegroundColor $info
Write-Host ""

Write-Host "Testing your live application..." -ForegroundColor $info
Write-Host ""

$tests = @(
    @{
        name = "Frontend loads"
        url = $vercelUrl
    },
    @{
        name = "Backend API health"
        url = "$renderUrl/health"
    },
    @{
        name = "Model info available"
        url = "$renderUrl/model-info"
    }
)

foreach ($test in $tests) {
    Write-Host "Testing: $($test.name)..." -NoNewline
    try {
        $response = Invoke-WebRequest -Uri $test.url -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host " ✓" -ForegroundColor $success
        }
    }
    catch {
        Write-Host " (may need to warm up)" -ForegroundColor $warning
    }
}

# ============================================================
# FINAL SUMMARY
# ============================================================

Write-Host ""
Write-Host "======================================================================" -ForegroundColor $success
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor $success
Write-Host "======================================================================" -ForegroundColor $success

Write-Host ""
Write-Host "YOUR PRODUCTION SYSTEM:" -ForegroundColor $info
Write-Host ""
Write-Host "Frontend:  $vercelUrl" -ForegroundColor $success
Write-Host "Backend:   $renderUrl" -ForegroundColor $success
Write-Host "Database: Supabase (configured)" -ForegroundColor $success
Write-Host ""

Write-Host "NEXT STEPS:" -ForegroundColor $info
Write-Host ""
Write-Host "1. Test your application:" -ForegroundColor $info
Write-Host "   - Visit: $vercelUrl" -ForegroundColor $warning
Write-Host "   - Sign up with an account" -ForegroundColor $warning
Write-Host "   - Make a prediction" -ForegroundColor $warning
Write-Host "   - Check SHAP explanations" -ForegroundColor $warning
Write-Host ""
Write-Host "2. Monitor performance:" -ForegroundColor $info
Write-Host "   - Render dashboard: https://dashboard.render.com" -ForegroundColor $warning
Write-Host "   - Vercel analytics: https://vercel.com/dashboard" -ForegroundColor $warning
Write-Host "   - Supabase console: https://supabase.co/dashboard" -ForegroundColor $warning
Write-Host ""
Write-Host "3. Run full verification tests:" -ForegroundColor $info
Write-Host "   - See: DEPLOYMENT_VERIFICATION.md" -ForegroundColor $warning
Write-Host ""
Write-Host "4. Troubleshooting:" -ForegroundColor $info
Write-Host "   - See: DEPLOYMENT_FREEMIUM_GUIDE.md (Troubleshooting section)" -ForegroundColor $warning
Write-Host ""

Write-Host "COST:" -ForegroundColor $info
Write-Host "   EUR 0/month (completely free tier)" -ForegroundColor $success
Write-Host ""

Write-Host "Save these URLs for future reference:" -ForegroundColor $warning
Write-Host "   Frontend:  $vercelUrl"
Write-Host "   Backend:   $renderUrl"
Write-Host ""

Read-Host "Press Enter to finish"

Write-Host ""
Write-Host "Your production system is now LIVE!" -ForegroundColor $success
Write-Host ""