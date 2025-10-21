#!/usr/bin/env pwsh
<#
.SYNOPSIS
    COMPLETE DEPLOYMENT AUTOMATION SCRIPT
    Guides you through deploying to Render + Vercel in under 1 hour

.DESCRIPTION
    This script automates the deployment process with clear step-by-step instructions.
    You'll need to manually complete some steps on Render and Vercel websites.

.EXAMPLE
    .\DEPLOY_NOW.ps1

.NOTES
    Prerequisites:
    - GitHub account connected to Render and Vercel
    - Repository pushed to GitHub
    - Supabase project created and configured
#>

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 COMPLETE DEPLOYMENT PACKAGE" -ForegroundColor Cyan
Write-Host "   Vercel → Render → Supabase" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Colors
$success = "Green"
$warning = "Yellow"
$info = "Cyan"
$error_color = "Red"

function Step {
    param([string]$number, [string]$title, [string]$time)
    Write-Host ""
    Write-Host "╔━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╗" -ForegroundColor $info
    Write-Host "║ STEP $number : $title" -ForegroundColor $info
    Write-Host "║ ⏱️  Expected time: $time" -ForegroundColor $info
    Write-Host "╚━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╝" -ForegroundColor $info
}

function Instruction {
    param([string]$text, [int]$indent = 1)
    $spaces = " " * ($indent * 2)
    Write-Host "$spaces $text"
}

function Important {
    param([string]$text)
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: $text" -ForegroundColor $warning
    Write-Host ""
}

function Success {
    param([string]$text)
    Write-Host "✅ $text" -ForegroundColor $success
}

function Copy-ToClipboard {
    param([string]$text)
    $text | Set-Clipboard
    Write-Host "   (Copied to clipboard)" -ForegroundColor $warning
}

# ============================================================
# STEP 0: Pre-deployment checks
# ============================================================

Step "0" "PRE-DEPLOYMENT CHECKS" "2 minutes"

Write-Host ""
Write-Host "Checking your environment..." -ForegroundColor $info
Write-Host ""

# Check if in correct directory
if (-not (Test-Path "render.yaml")) {
    Write-Host "❌ ERROR: Not in project root directory" -ForegroundColor $error_color
    Write-Host "   Please run this from the project root (navi-tax-35-main)" -ForegroundColor $error_color
    exit 1
}
Success "Found render.yaml"

if (-not (Test-Path "vercel.json")) {
    Write-Host "❌ ERROR: vercel.json not found" -ForegroundColor $error_color
    exit 1
}
Success "Found vercel.json"

if (-not (Test-Path "optimized_models_25000_samples")) {
    Write-Host "❌ ERROR: Models not found" -ForegroundColor $error_color
    exit 1
}
Success "Found trained models"

# Check Git status
$gitStatus = git status --short
if ($gitStatus) {
    Write-Host ""
    Important "You have uncommitted changes. Commit them first:"
    Write-Host "   git add ." -ForegroundColor $warning
    Write-Host "   git commit -m 'Your message'" -ForegroundColor $warning
    Write-Host "   git push" -ForegroundColor $warning
    Read-Host "Press Enter to continue"
}
else {
    Success "Git repository is clean"
}

Write-Host ""
Success "All pre-deployment checks passed!"

# ============================================================
# STEP 1: Backend Deployment (Render)
# ============================================================

Step "1" "DEPLOY BACKEND TO RENDER" "25 minutes"

Write-Host ""
Instruction "1. Go to: https://dashboard.render.com"
Instruction "2. Click: 'New +' → 'Web Service'"
Instruction "3. Connect your GitHub repository:"
Write-Host ""
Write-Host "   Repository: Select 'misbah003/demo' (or your repo)" -ForegroundColor $warning
Write-Host "   Branch: 'master' (or 'main' if different)" -ForegroundColor $warning
Write-Host ""
Instruction "4. Configure the service:"
Write-Host ""
Write-Host "   Name: navi-tax-ml-api" -ForegroundColor $warning
Write-Host "   Region: Frankfurt" -ForegroundColor $warning
Write-Host "   Runtime: Python 3.9" -ForegroundColor $warning
Write-Host "   Build Command: pip install -r requirements.txt" -ForegroundColor $warning
Write-Host "   Start Command: gunicorn -w 2 -b 0.0.0.0:\$PORT --timeout 120 ml.ml_api_service_optimized:app" -ForegroundColor $warning
Write-Host ""
Instruction "5. Click 'Create Web Service'"
Write-Host ""
Write-Host "⏳ Waiting for build... (15-20 minutes)" -ForegroundColor $warning
Instruction "You can monitor progress on the dashboard"

Write-Host ""
Important "Click 'Deploys' tab and wait for status to be 'Live' (green)"

Write-Host ""
Instruction "6. Once deployment is complete:"
Instruction "   - Go to 'Settings' tab" 2
Instruction "   - Copy your service URL (e.g., https://navi-tax-ml-api.onrender.com)" 2
Write-Host ""
Write-Host "   Save this URL - you'll need it next!" -ForegroundColor $warning

$renderUrl = Read-Host "📍 Enter your Render service URL (https://navi-tax-ml-api.onrender.com)"

if ($renderUrl -match "^https?://.+\.onrender\.com$") {
    Success "Render backend deployed!"
    Write-Host "URL: $renderUrl" -ForegroundColor $success
}
else {
    Write-Host "❌ Invalid URL format" -ForegroundColor $error_color
    $renderUrl = Read-Host "Please enter a valid URL (https://...)"
}

# ============================================================
# STEP 2: Verify Backend Health
# ============================================================

Step "2" "VERIFY BACKEND HEALTH" "5 minutes"

Write-Host ""
Instruction "Testing backend endpoints..."
Write-Host ""

$healthUrl = "$renderUrl/health"
Write-Host "Testing: $healthUrl" -ForegroundColor $warning

try {
    $response = Invoke-WebRequest -Uri $healthUrl -TimeoutSec 30 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Success "Backend is responding!"
        Success "Status: Healthy and ready"
    }
}
catch {
    Important "Backend may still be starting up (can take 1-2 min on first request)"
    Write-Host "You can verify manually at: $healthUrl" -ForegroundColor $info
}

# ============================================================
# STEP 3: Update Frontend Environment
# ============================================================

Step "3" "UPDATE FRONTEND ENVIRONMENT" "2 minutes"

Write-Host ""
Instruction "Updating web/.env.production with your Render URL..."

$envFile = "web\.env.production"
if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw
    $updated = $content -replace "VITE_BACKEND_URL=.*", "VITE_BACKEND_URL=$renderUrl"
    Set-Content $envFile $updated
    Success "Updated VITE_BACKEND_URL"
    Write-Host ""
    Write-Host "File content:" -ForegroundColor $info
    Get-Content $envFile | Select-Object -First 15 | Write-Host
}
else {
    Write-Host "❌ ERROR: web/.env.production not found" -ForegroundColor $error_color
}

# ============================================================
# STEP 4: Commit and Push
# ============================================================

Step "4" "COMMIT AND PUSH TO GITHUB" "2 minutes"

Write-Host ""
Instruction "Committing changes to GitHub..."

git add web/.env.production
git commit -m "chore: update backend URL for production deployment"
git push

Success "Changes pushed to GitHub!"

# ============================================================
# STEP 5: Deploy Frontend (Vercel)
# ============================================================

Step "5" "DEPLOY FRONTEND TO VERCEL" "15 minutes"

Write-Host ""
Instruction "1. Go to: https://vercel.com/dashboard"
Instruction "2. Click: 'Add New +' → 'Project'"
Instruction "3. Select your repository"
Write-Host ""
Instruction "4. Configure build settings:"
Write-Host ""
Write-Host "   Framework: Vite" -ForegroundColor $warning
Write-Host "   Build Command: cd web && npm run build" -ForegroundColor $warning
Write-Host "   Output Directory: web/dist" -ForegroundColor $warning
Write-Host ""
Instruction "5. Add environment variables:"
Write-Host ""
Write-Host "   VITE_SUPABASE_PROJECT_ID: ikqcakganqabiscsibyim" -ForegroundColor $warning
Write-Host "   VITE_SUPABASE_PUBLISHABLE_KEY: (from web/.env.production)" -ForegroundColor $warning
Write-Host "   VITE_SUPABASE_URL: https://ikqcakganqabiscsibyim.supabase.co" -ForegroundColor $warning
Write-Host "   VITE_BACKEND_URL: $renderUrl" -ForegroundColor $warning
Write-Host ""
Instruction "6. Click 'Deploy'"
Write-Host ""
Write-Host "⏳ Waiting for build and deployment... (10-15 minutes)" -ForegroundColor $warning

Important "Monitor progress on Vercel dashboard"

Write-Host ""
Instruction "Once complete, you'll get a deployment URL!"

$vercelUrl = Read-Host "📍 Enter your Vercel deployment URL (https://...vercel.app)"

# ============================================================
# STEP 6: Verification
# ============================================================

Step "6" "VERIFY DEPLOYMENT" "10 minutes"

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
            Write-Host " ✅" -ForegroundColor $success
        }
    }
    catch {
        Write-Host " ⚠️ (may need to warm up)" -ForegroundColor $warning
    }
}

# ============================================================
# FINAL SUMMARY
# ============================================================

Write-Host ""
Write-Host "=" * 70 -ForegroundColor $success
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor $success
Write-Host "=" * 70 -ForegroundColor $success

Write-Host ""
Write-Host "📊 YOUR PRODUCTION SYSTEM:" -ForegroundColor $info
Write-Host ""
Write-Host "🌍 Frontend:  $vercelUrl" -ForegroundColor $success
Write-Host "⚙️  Backend:   $renderUrl" -ForegroundColor $success
Write-Host "🗄️  Database: Supabase (configured)" -ForegroundColor $success
Write-Host ""

Write-Host "📚 NEXT STEPS:" -ForegroundColor $info
Write-Host ""
Write-Host "1. Test your application:"
Write-Host "   - Visit: $vercelUrl" -ForegroundColor $warning
Write-Host "   - Sign up with an account" -ForegroundColor $warning
Write-Host "   - Make a prediction" -ForegroundColor $warning
Write-Host "   - Check SHAP explanations" -ForegroundColor $warning
Write-Host ""
Write-Host "2. Monitor performance:"
Write-Host "   - Render dashboard: https://dashboard.render.com" -ForegroundColor $warning
Write-Host "   - Vercel analytics: https://vercel.com/dashboard" -ForegroundColor $warning
Write-Host "   - Supabase console: https://supabase.co/dashboard" -ForegroundColor $warning
Write-Host ""
Write-Host "3. Run full verification tests:"
Write-Host "   - See: DEPLOYMENT_VERIFICATION.md" -ForegroundColor $warning
Write-Host ""
Write-Host "4. Troubleshooting:"
Write-Host "   - See: DEPLOYMENT_FREEMIUM_GUIDE.md (Troubleshooting section)" -ForegroundColor $warning
Write-Host ""

Write-Host "🎯 COST:" -ForegroundColor $info
Write-Host "   €0/month (completely free tier)" -ForegroundColor $success
Write-Host ""

Write-Host "💾 Save these URLs for future reference:" -ForegroundColor $warning
Write-Host "   Frontend:  $vercelUrl"
Write-Host "   Backend:   $renderUrl"
Write-Host ""

Read-Host "Press Enter to finish"

Write-Host ""
Write-Host "✨ Your production system is now LIVE! ✨" -ForegroundColor $success
Write-Host ""