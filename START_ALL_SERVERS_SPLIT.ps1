# ========================================
# Navi Tax - Split Architecture Local Testing
# ========================================
# This script tests the split architecture locally:
# Frontend (Port 8080) -> ML API (Port 8000) -> Supabase (Cloud Backend)
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NAVI TAX - SPLIT ARCHITECTURE TEST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Testing split architecture deployment:" -ForegroundColor Yellow
Write-Host "  1. ML API (Port 8000) - TensorFlow Model Server" -ForegroundColor Yellow
Write-Host "  2. Frontend (Port 8080) - React Web UI" -ForegroundColor Yellow
Write-Host "  3. Backend - Supabase Cloud (Edge Functions)" -ForegroundColor Yellow
Write-Host ""

# Set project directories
$ProjectRoot = "C:\Users\HomeLaptop\Downloads\navi-tax-35-main"
$BackendDir = "$ProjectRoot\docs\backend-example"
$FrontendDir = "$ProjectRoot\web"

# ========================================
# STEP 1: Verify Prerequisites
# ========================================
Write-Host "[STEP 1/5] Verifying Prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found! Install Python 3.8+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js not found! Install Node.js" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version 2>&1
    Write-Host "[OK] npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] npm not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# ========================================
# STEP 2: Setup Environment Variables
# ========================================
Write-Host "[STEP 2/5] Setting up Environment Variables..." -ForegroundColor Yellow
Write-Host ""

# Create .env for backend if it doesn't exist
$BackendEnvPath = "$BackendDir\.env"
if (-not (Test-Path $BackendEnvPath)) {
    Write-Host "[!] Creating local .env for backend..." -ForegroundColor Yellow
    @"
# Local development configuration
NODE_ENV=development
PORT=3001
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key
ML_API_URL=http://localhost:8000
CORS_ORIGIN=http://localhost:8080
"@ | Out-File -FilePath $BackendEnvPath -Encoding UTF8
    Write-Host "[OK] Created: $BackendEnvPath" -ForegroundColor Green
    Write-Host "    [!] UPDATE with your Supabase credentials!" -ForegroundColor Yellow
} else {
    Write-Host "[OK] Backend .env exists" -ForegroundColor Green
}

# Create .env for frontend if it doesn't exist
$FrontendEnvPath = "$FrontendDir\.env"
if (-not (Test-Path $FrontendEnvPath)) {
    Write-Host "[!] Creating local .env for frontend..." -ForegroundColor Yellow
    @"
# Local development configuration
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_anon_key
"@ | Out-File -FilePath $FrontendEnvPath -Encoding UTF8
    Write-Host "[OK] Created: $FrontendEnvPath" -ForegroundColor Green
    Write-Host "    [!] UPDATE with your Supabase credentials!" -ForegroundColor Yellow
} else {
    Write-Host "[OK] Frontend .env exists" -ForegroundColor Green
}

Write-Host ""

# ========================================
# STEP 3: Start ML API
# ========================================
Write-Host "[STEP 3/5] Starting ML API (Port 8000)..." -ForegroundColor Yellow
Write-Host ""

# Check if port 8000 is in use
$MLPort = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($MLPort) {
    Write-Host "[!] Port 8000 already in use - using existing service" -ForegroundColor Yellow
} else {
    Write-Host "[->] Launching ML API..." -ForegroundColor Cyan
    Write-Host "    (Loading models takes 30-60 seconds)" -ForegroundColor Gray
    
    Start-Process powershell -ArgumentList `
        "-NoExit", `
        "-Command", `
        "Set-Location '$ProjectRoot'; Write-Host 'ML API Starting...' -ForegroundColor Green; Write-Host 'Loading models (30-60s)...' -ForegroundColor Yellow; Write-Host ''; python ml\ml_api_service_optimized.py" `
        -WindowStyle Normal
    
    Write-Host "[->] Waiting for ML API to initialize (60 seconds for model loading)..." -ForegroundColor Cyan
    Write-Host "    This will check every 5 seconds for model status..." -ForegroundColor Gray
    
    $mlReady = $false
    $maxAttempts = 12
    $attempt = 0
    
    while (-not $mlReady -and $attempt -lt $maxAttempts) {
        Start-Sleep -Seconds 5
        $attempt++
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                $content = $response.Content | ConvertFrom-Json
                if ($content.status -eq "healthy") {
                    $mlReady = $true
                    Write-Host "    [OK] ML API models loaded and responding!" -ForegroundColor Green
                }
            }
        } catch {
            Write-Host "    [->] Waiting for models to load... (Attempt $attempt/$maxAttempts)" -ForegroundColor Cyan
        }
    }
    
    if (-not $mlReady) {
        Write-Host "    [!] ML API still loading, continuing anyway..." -ForegroundColor Yellow
    }
}

Write-Host "[OK] ML API window opened" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 4: Backend Status Check
# ========================================
Write-Host "[STEP 4/5] Backend Status Check..." -ForegroundColor Yellow
Write-Host ""

# This project uses Supabase for backend (serverless edge functions)
# No local backend server needs to be running
Write-Host "[OK] Backend: Using Supabase Edge Functions (cloud-based)" -ForegroundColor Green
Write-Host "     [NOTE] Supabase edge functions are deployed and don't need local startup" -ForegroundColor Cyan
Write-Host ""

# ========================================
# STEP 5: Start Frontend
# ========================================
Write-Host "[STEP 5/5] Starting Frontend (Port 8080)..." -ForegroundColor Yellow
Write-Host ""

# Check if port 8080 is in use
$FrontendPort = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
if ($FrontendPort) {
    Write-Host "[!] Port 8080 already in use - using existing service" -ForegroundColor Yellow
} else {
    # Install dependencies if needed
    if (-not (Test-Path "$FrontendDir\node_modules")) {
        Write-Host "[->] Installing frontend dependencies..." -ForegroundColor Cyan
        Set-Location $FrontendDir
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Failed to install frontend dependencies" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    
    Write-Host "[->] Launching Frontend Dev Server..." -ForegroundColor Cyan
    Set-Location $FrontendDir
    Start-Process powershell -ArgumentList `
        "-NoExit", `
        "-Command", `
        "Set-Location '$FrontendDir'; Write-Host 'Frontend Dev Server Starting...' -ForegroundColor Green; Write-Host ''; `$env:VITE_API_URL='http://localhost:8000'; npm run dev" `
        -WindowStyle Normal
    
    Write-Host "[->] Waiting for frontend to initialize (10 seconds)..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
}

Write-Host "[OK] Frontend Server window opened" -ForegroundColor Green
Write-Host ""

# ========================================
# SUCCESS & TESTING INSTRUCTIONS
# ========================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SPLIT ARCHITECTURE READY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services Running:" -ForegroundColor Green
Write-Host "  ML API................ http://localhost:8000" -ForegroundColor Green
Write-Host "  Frontend App.......... http://localhost:8080" -ForegroundColor Green
Write-Host "  Backend (Supabase).... Cloud-based (edge functions)" -ForegroundColor Green
Write-Host ""

Write-Host "Testing Checklist:" -ForegroundColor Cyan
Write-Host "  [ ] Frontend loads at http://localhost:8080" -ForegroundColor Cyan
Write-Host "  [ ] ML API is responsive at http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "  [ ] ML API shows models loaded successfully" -ForegroundColor Cyan
Write-Host "  [ ] Frontend can make predictions" -ForegroundColor Cyan
Write-Host "  [ ] SHAP explanations display correctly" -ForegroundColor Cyan
Write-Host ""

Write-Host "Important Notes:" -ForegroundColor Yellow
Write-Host "  * Keep BOTH windows open (ML API and Frontend)" -ForegroundColor Yellow
Write-Host "  * ML API takes 30-60 seconds to load models on first start" -ForegroundColor Yellow
Write-Host "  * Check ML API window for startup messages and model loading status" -ForegroundColor Yellow
Write-Host "  * Refresh frontend if needed after services fully initialize" -ForegroundColor Yellow
Write-Host "  * Supabase credentials are configured in .env files" -ForegroundColor Yellow
Write-Host ""

Write-Host "Testing API Endpoints:" -ForegroundColor Cyan
Write-Host "  ML API Health:       curl http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "  ML API Models Info:  curl http://localhost:8000/model-info" -ForegroundColor Cyan
Write-Host ""

# Open browser
Write-Host "[->] Opening browser in 5 seconds..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
Start-Process "http://localhost:8080"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Ready for Testing!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close this window (services keep running)..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")