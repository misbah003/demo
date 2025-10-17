# Check Backend Server Status
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend Server Status Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$backendPath = "c:\Users\HomeLaptop\Downloads\navi-tax-35-main\docs\backend-example"

# Check if backend folder exists
if (Test-Path $backendPath) {
    Write-Host "[OK] Backend folder found" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Backend folder not found at: $backendPath" -ForegroundColor Red
    exit 1
}

# Check if server.js exists
$serverFile = Join-Path $backendPath "server.js"
if (Test-Path $serverFile) {
    Write-Host "[OK] server.js found" -ForegroundColor Green
} else {
    Write-Host "[ERROR] server.js not found" -ForegroundColor Red
    exit 1
}

# Check if node_modules exists
$nodeModules = Join-Path $backendPath "node_modules"
if (Test-Path $nodeModules) {
    Write-Host "[OK] Dependencies installed (node_modules found)" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Dependencies not installed" -ForegroundColor Yellow
    Write-Host "         Run: cd $backendPath; npm install" -ForegroundColor Yellow
}

# Check if .env exists
$envFile = Join-Path $backendPath ".env"
if (Test-Path $envFile) {
    Write-Host "[OK] .env file found" -ForegroundColor Green
    
    # Check if .env has required variables
    $envContent = Get-Content $envFile -Raw
    if ($envContent -match "SUPABASE_URL") {
        Write-Host "[OK] SUPABASE_URL configured" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] SUPABASE_URL not found in .env" -ForegroundColor Yellow
    }
    
    if ($envContent -match "SUPABASE_SERVICE_KEY") {
        Write-Host "[OK] SUPABASE_SERVICE_KEY configured" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] SUPABASE_SERVICE_KEY not found in .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "[ERROR] .env file not found" -ForegroundColor Red
    Write-Host "        Create .env file with:" -ForegroundColor Yellow
    Write-Host "        SUPABASE_URL=your_url" -ForegroundColor Yellow
    Write-Host "        SUPABASE_SERVICE_KEY=your_key" -ForegroundColor Yellow
    Write-Host "        PORT=3001" -ForegroundColor Yellow
}

Write-Host ""

# Check if backend is running
Write-Host "Checking if backend is running on port 3001..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3001" -Method GET -TimeoutSec 2 -ErrorAction Stop
    Write-Host "[OK] Backend server is RUNNING on port 3001" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Backend server is NOT running" -ForegroundColor Yellow
    Write-Host "          Start it with: START_BACKEND.bat" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the backend server:" -ForegroundColor White
Write-Host "  1. Double-click START_BACKEND.bat" -ForegroundColor White
Write-Host "  OR" -ForegroundColor White
Write-Host "  2. Run: cd $backendPath; node server.js" -ForegroundColor White
Write-Host ""
Write-Host "Keep the terminal window open while using the app!" -ForegroundColor Yellow
Write-Host ""