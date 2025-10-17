# ========================================
# Navi Tax Application - PowerShell Startup
# ========================================
# This script starts both Backend and Frontend servers
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NAVI TAX APPLICATION STARTUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set project directories
$ProjectRoot = "c:\Users\HomeLaptop\Downloads\navi-tax-35-main"
$BackendDir = "$ProjectRoot\docs\backend-example"
$FrontendDir = "$ProjectRoot\web"

# ========================================
# STEP 1: Check Backend Prerequisites
# ========================================
Write-Host "[STEP 1/4] Checking Backend Prerequisites..." -ForegroundColor Yellow
Write-Host ""

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

if (-not (Test-Path "$BackendDir\node_modules")) {
    Write-Host "[INFO] Installing backend dependencies..." -ForegroundColor Yellow
    Set-Location $BackendDir
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install backend dependencies!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[OK] Backend dependencies installed" -ForegroundColor Green
    Write-Host ""
}

Write-Host "[OK] Backend prerequisites satisfied" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 2: Check Frontend Prerequisites
# ========================================
Write-Host "[STEP 2/4] Checking Frontend Prerequisites..." -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path "$FrontendDir\node_modules")) {
    Write-Host "[INFO] Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location $FrontendDir
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install frontend dependencies!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[OK] Frontend dependencies installed" -ForegroundColor Green
    Write-Host ""
}

Write-Host "[OK] Frontend prerequisites satisfied" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 3: Start Backend Server
# ========================================
Write-Host "[STEP 3/4] Starting Backend Server..." -ForegroundColor Yellow
Write-Host ""

# Check if port 3001 is in use
$BackendPort = Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue
if ($BackendPort) {
    Write-Host "[WARNING] Port 3001 is already in use!" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Kill existing process and restart? (Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        $ProcessId = $BackendPort.OwningProcess
        Write-Host "[INFO] Killing process $ProcessId on port 3001..." -ForegroundColor Yellow
        Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    } else {
        Write-Host "[INFO] Using existing backend server on port 3001" -ForegroundColor Cyan
    }
}

# Start backend if not running
$BackendPort = Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue
if (-not $BackendPort) {
    Write-Host "[INFO] Starting backend on port 3001..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$BackendDir'; Write-Host 'Backend Server Starting...' -ForegroundColor Green; Write-Host ''; node server.js" -WindowStyle Normal
    
    Write-Host "[INFO] Waiting for backend to initialize..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    
    # Verify backend started
    $BackendPort = Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue
    if ($BackendPort) {
        Write-Host "[OK] Backend server started successfully on http://localhost:3001" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "[ERROR] Backend server failed to start!" -ForegroundColor Red
        Write-Host "Please check the backend window for errors." -ForegroundColor Red
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[OK] Backend server is running on http://localhost:3001" -ForegroundColor Green
    Write-Host ""
}

# ========================================
# STEP 4: Start Frontend Server
# ========================================
Write-Host "[STEP 4/4] Starting Frontend Server..." -ForegroundColor Yellow
Write-Host ""

# Check if port 5173 is in use
$FrontendPort = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if ($FrontendPort) {
    Write-Host "[WARNING] Port 5173 is already in use!" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Kill existing process and restart? (Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        $ProcessId = $FrontendPort.OwningProcess
        Write-Host "[INFO] Killing process $ProcessId on port 5173..." -ForegroundColor Yellow
        Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    } else {
        Write-Host "[INFO] Using existing frontend server on port 5173" -ForegroundColor Cyan
    }
}

# Start frontend if not running
$FrontendPort = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if (-not $FrontendPort) {
    Write-Host "[INFO] Starting frontend on port 5173..." -ForegroundColor Cyan
    Set-Location $FrontendDir
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$FrontendDir'; Write-Host 'Frontend Server Starting...' -ForegroundColor Green; Write-Host ''; npm run dev" -WindowStyle Normal
    
    Write-Host "[INFO] Waiting for frontend to initialize..." -ForegroundColor Cyan
    Start-Sleep -Seconds 8
}

# ========================================
# SUCCESS
# ========================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  STARTUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[OK] Backend Server:  http://localhost:3001" -ForegroundColor Green
Write-Host "[OK] Frontend App:    http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  IMPORTANT NOTES:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Two PowerShell windows are now open:"
Write-Host "   - Backend Server (Port 3001)"
Write-Host "   - Frontend Server (Port 5173)"
Write-Host ""
Write-Host "2. KEEP BOTH WINDOWS OPEN while using the app"
Write-Host ""
Write-Host "3. To stop the servers:"
Write-Host "   - Close both PowerShell windows, OR"
Write-Host "   - Press Ctrl+C in each window, OR"
Write-Host "   - Run STOP_SERVERS.ps1"
Write-Host ""
Write-Host "4. Access the application at:"
Write-Host "   http://localhost:5173"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# Open browser automatically
Write-Host ""
Write-Host "[INFO] Opening browser..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Press any key to close this window (servers will keep running)..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")