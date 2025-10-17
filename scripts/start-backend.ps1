Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Email Backend Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location backend-example

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please configure your Gmail credentials:" -ForegroundColor Yellow
    Write-Host "1. Copy backend-example\.env.example to backend-example\.env"
    Write-Host "2. Edit .env and add your Gmail credentials"
    Write-Host "3. See SETUP_EMAIL_INSTRUCTIONS.md for detailed steps"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting backend server on port 3001..." -ForegroundColor Green
Write-Host "Keep this window open while using the app." -ForegroundColor Yellow
Write-Host ""
node server.js