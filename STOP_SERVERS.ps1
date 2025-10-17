# ========================================
# Navi Tax Application - Stop All Servers
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STOPPING NAVI TAX SERVERS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Stop Backend (Port 3001)
Write-Host "[INFO] Checking for backend server on port 3001..." -ForegroundColor Yellow
$BackendPort = Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue
if ($BackendPort) {
    Write-Host "[INFO] Stopping backend server..." -ForegroundColor Yellow
    $ProcessId = $BackendPort.OwningProcess
    Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Backend server stopped (PID: $ProcessId)" -ForegroundColor Green
} else {
    Write-Host "[INFO] Backend server is not running" -ForegroundColor Cyan
}

Write-Host ""

# Stop Frontend (Port 5173)
Write-Host "[INFO] Checking for frontend server on port 5173..." -ForegroundColor Yellow
$FrontendPort = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if ($FrontendPort) {
    Write-Host "[INFO] Stopping frontend server..." -ForegroundColor Yellow
    $ProcessId = $FrontendPort.OwningProcess
    Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Frontend server stopped (PID: $ProcessId)" -ForegroundColor Green
} else {
    Write-Host "[INFO] Frontend server is not running" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ALL SERVERS STOPPED" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"