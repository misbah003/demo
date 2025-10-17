# ========================================
# Navi Tax Application - Complete Startup
# ========================================
# This script starts ML API, Backend, and Frontend
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NAVI TAX - COMPLETE STARTUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting all services:" -ForegroundColor Yellow
Write-Host "  1. ML API (Port 8000)" -ForegroundColor Yellow
Write-Host "  2. Backend (Port 3001)" -ForegroundColor Yellow
Write-Host "  3. Frontend (Port 8080)" -ForegroundColor Yellow
Write-Host ""

# Set project directories
$ProjectRoot = "C:\Users\HomeLaptop\Downloads\navi-tax-35-main"
$BackendDir = "$ProjectRoot\docs\backend-example"
$FrontendDir = "$ProjectRoot\web"
$MLDir = "$ProjectRoot\ml"

# ========================================
# STEP 1: Check Prerequisites
# ========================================
Write-Host "[STEP 1/4] Checking Prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Backend .env
if (-not (Test-Path "$BackendDir\.env")) {
    Write-Host "[ERROR] Backend .env file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please create: $BackendDir\.env"
    Write-Host ""
    Write-Host "Required contents:"
    Write-Host "SUPABASE_URL=your_supabase_url"
    Write-Host "SUPABASE_SERVICE_KEY=your_service_key"
    Write-Host "PORT=3001"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found! Please install Python 3.8+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js not found! Please install Node.js" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[OK] All prerequisites satisfied" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 2: Start ML API
# ========================================
Write-Host "[STEP 2/4] Starting ML API..." -ForegroundColor Yellow
Write-Host ""

# Check if port 8000 is in use
$MLPort = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($MLPort) {
    Write-Host "[WARNING] Port 8000 is already in use!" -ForegroundColor Yellow
    Write-Host "[INFO] Using existing ML API on port 8000" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "[INFO] Starting ML API on port 8000..." -ForegroundColor Cyan
    Write-Host "[INFO] This may take 30-60 seconds for models to load..." -ForegroundColor Cyan
    
    # Start ML API in new window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$ProjectRoot'; Write-Host 'ML API Starting...' -ForegroundColor Green; Write-Host 'Loading models (this takes 30-60 seconds)...' -ForegroundColor Yellow; Write-Host ''; .\START_ADVANCED_ML_API.bat" -WindowStyle Normal
    
    Write-Host "[INFO] Waiting for ML API to initialize..." -ForegroundColor Cyan
    Start-Sleep -Seconds 15
    
    Write-Host "[OK] ML API window opened (still loading models)" -ForegroundColor Green
    Write-Host ""
}

# ========================================
# STEP 3: Start Backend Server
# ========================================
Write-Host "[STEP 3/4] Starting Backend Server..." -ForegroundColor Yellow
Write-Host ""

# Check if port 3001 is in use
$BackendPort = Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue
if ($BackendPort) {
    Write-Host "[WARNING] Port 3001 is already in use!" -ForegroundColor Yellow
    Write-Host "[INFO] Using existing backend server on port 3001" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "[INFO] Starting backend on port 3001..." -ForegroundColor Cyan
    
    # Install backend dependencies if needed
    if (-not (Test-Path "$BackendDir\node_modules")) {
        Write-Host "[INFO] Installing backend dependencies..." -ForegroundColor Yellow
        Set-Location $BackendDir
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Failed to install backend dependencies!" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    
    # Start backend in new window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$BackendDir'; Write-Host 'Backend Server Starting...' -ForegroundColor Green; Write-Host ''; node server.js" -WindowStyle Normal
    
    Write-Host "[INFO] Waiting for backend to initialize..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    
    # Verify backend started
    $BackendPort = Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue
    if ($BackendPort) {
        Write-Host "[OK] Backend server started successfully" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "[WARNING] Backend may still be starting..." -ForegroundColor Yellow
        Write-Host "Please check the backend window for status." -ForegroundColor Yellow
        Write-Host ""
    }
}

# ========================================
# STEP 4: Start Frontend Server
# ========================================
Write-Host "[STEP 4/4] Starting Frontend Server..." -ForegroundColor Yellow
Write-Host ""

# Check if port 8080 is in use
$FrontendPort = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
if ($FrontendPort) {
    Write-Host "[WARNING] Port 8080 is already in use!" -ForegroundColor Yellow
    Write-Host "[INFO] Using existing frontend server on port 8080" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "[INFO] Starting frontend on port 8080..." -ForegroundColor Cyan
    
    # Install frontend dependencies if needed
    if (-not (Test-Path "$FrontendDir\node_modules")) {
        Write-Host "[INFO] Installing frontend dependencies..." -ForegroundColor Yellow
        Set-Location $FrontendDir
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Failed to install frontend dependencies!" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    
    # Start frontend in new window
    Set-Location $FrontendDir
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$FrontendDir'; Write-Host 'Frontend Server Starting...' -ForegroundColor Green; Write-Host ''; npm run dev" -WindowStyle Normal
    
    Write-Host "[INFO] Waiting for frontend to initialize..." -ForegroundColor Cyan
    Start-Sleep -Seconds 8
    
    Write-Host "[OK] Frontend server started" -ForegroundColor Green
    Write-Host ""
}

# ========================================
# SUCCESS
# ========================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  STARTUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[OK] ML API:          http://localhost:8000" -ForegroundColor Green
Write-Host "[OK] Backend Server:  http://localhost:3001" -ForegroundColor Green
Write-Host "[OK] Frontend App:    http://localhost:8080" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  IMPORTANT NOTES:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Three PowerShell windows are now open:"
Write-Host "   - ML API (Port 8000) - Still loading models..."
Write-Host "   - Backend Server (Port 3001)"
Write-Host "   - Frontend Server (Port 8080)"
Write-Host ""
Write-Host "2. KEEP ALL WINDOWS OPEN while using the app"
Write-Host ""
Write-Host "3. ML API takes 30-60 seconds to fully load"
Write-Host "   Check the ML API window for 'Application startup complete'"
Write-Host ""
Write-Host "4. Once ML API is ready, restart the backend:"
Write-Host "   - Press Ctrl+C in backend window"
Write-Host "   - Run: .\START_BACKEND.bat"
Write-Host ""
Write-Host "5. To stop all servers:"
Write-Host "   - Close all PowerShell windows, OR"
Write-Host "   - Press Ctrl+C in each window"
Write-Host ""
Write-Host "6. Access the application at:"
Write-Host "   http://localhost:8080"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# Open browser automatically
Write-Host ""
Write-Host "[INFO] Opening browser in 5 seconds..." -ForegroundColor Cyan
Write-Host "[INFO] (Waiting for servers to stabilize)" -ForegroundColor Cyan
Start-Sleep -Seconds 5
Start-Process "http://localhost:8080"

Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  NEXT STEPS:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Wait for ML API to show: 'Application startup complete'" -ForegroundColor Yellow
Write-Host "2. Then restart backend to connect to ML API" -ForegroundColor Yellow
Write-Host "3. Refresh browser to see '🤖 ML Active (95%)' badge" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to close this window (servers will keep running)..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")