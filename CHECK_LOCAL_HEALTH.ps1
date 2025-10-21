# ========================================
# Local Services Health Check
# ========================================
# Quick diagnostic to verify all services are running

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LOCAL SERVICES HEALTH CHECK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check ports
Write-Host "[1/4] Checking Port Availability..." -ForegroundColor Yellow
Write-Host ""

$Ports = @{
    "8000" = "ML API"
    "3001" = "Backend"
    "5173" = "Frontend"
}

$AllRunning = $true

foreach ($Port in $Ports.GetEnumerator()) {
    $Connection = Get-NetTCPConnection -LocalPort $Port.Key -ErrorAction SilentlyContinue
    if ($Connection) {
        Write-Host "[OK] Port $($Port.Key) - $($Port.Value) is RUNNING" -ForegroundColor Green
    } else {
        Write-Host "[X] Port $($Port.Key) - $($Port.Value) is NOT running" -ForegroundColor Red
        $AllRunning = $false
    }
}

Write-Host ""

# Check connectivity
Write-Host "[2/4] Testing Service Connectivity..." -ForegroundColor Yellow
Write-Host ""

# Test ML API
try {
    $Response = Invoke-WebRequest -Uri "http://localhost:8000/ml/health" -ErrorAction Stop
    Write-Host "[OK] ML API responding: $($Response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "[X] ML API not responding" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor DarkRed
}

# Test Backend
try {
    $Response = Invoke-WebRequest -Uri "http://localhost:3001/health" -ErrorAction Stop
    Write-Host "[OK] Backend responding: $($Response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "[X] Backend not responding" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor DarkRed
}

# Test Frontend
try {
    $Response = Invoke-WebRequest -Uri "http://localhost:5173/" -ErrorAction Stop
    Write-Host "[OK] Frontend responding: $($Response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "[X] Frontend not responding" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor DarkRed
}

Write-Host ""

# Check environment files
Write-Host "[3/4] Checking Environment Configuration..." -ForegroundColor Yellow
Write-Host ""

$ProjectRoot = "C:\Users\HomeLaptop\Downloads\navi-tax-35-main"
$BackendEnv = "$ProjectRoot\docs\backend-example\.env"
$FrontendEnv = "$ProjectRoot\web\.env"

if (Test-Path $BackendEnv) {
    Write-Host "[OK] Backend .env exists" -ForegroundColor Green
    # Check for required keys
    $Content = Get-Content $BackendEnv
    if ($Content -match "SUPABASE_URL") {
        Write-Host "    [OK] SUPABASE_URL configured" -ForegroundColor Green
    } else {
        Write-Host "    [!] SUPABASE_URL not configured" -ForegroundColor Yellow
    }
} else {
    Write-Host "[!] Backend .env not found - will be created on startup" -ForegroundColor Yellow
}

if (Test-Path $FrontendEnv) {
    Write-Host "[OK] Frontend .env exists" -ForegroundColor Green
} else {
    Write-Host "[!] Frontend .env not found - will be created on startup" -ForegroundColor Yellow
}

Write-Host ""

# Check node_modules
Write-Host "[4/4] Checking Dependencies..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path "$ProjectRoot\docs\backend-example\node_modules") {
    Write-Host "[OK] Backend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[!] Backend dependencies not installed" -ForegroundColor Yellow
    Write-Host "    Run: npm install (in docs/backend-example)" -ForegroundColor Yellow
}

if (Test-Path "$ProjectRoot\web\node_modules") {
    Write-Host "[OK] Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[!] Frontend dependencies not installed" -ForegroundColor Yellow
    Write-Host "    Run: npm install (in web)" -ForegroundColor Yellow
}

Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
if ($AllRunning) {
    Write-Host "  OK - ALL SERVICES RUNNING" -ForegroundColor Green
} else {
    Write-Host "  WARNING - SOME SERVICES NOT RUNNING" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Run: .\START_ALL_SERVERS_SPLIT.ps1" -ForegroundColor Yellow
    Write-Host "  2. Wait for services to initialize (1-2 minutes)" -ForegroundColor Yellow
    Write-Host "  3. Run this check again" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Quick links
Write-Host "Quick Links:" -ForegroundColor Cyan
Write-Host "  Frontend..... http://localhost:5173" -ForegroundColor Cyan
Write-Host "  Backend...... http://localhost:3001" -ForegroundColor Cyan
Write-Host "  ML API....... http://localhost:8000" -ForegroundColor Cyan
Write-Host ""