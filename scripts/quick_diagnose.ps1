# Quick Diagnostic Script for Delete Issues
Write-Host "Running Quick Diagnostics..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Check if backend port is open
Write-Host "1. Checking if backend is running on port 3001..." -ForegroundColor Yellow
$portTest = Test-NetConnection -ComputerName localhost -Port 3001 -WarningAction SilentlyContinue
if ($portTest.TcpTestSucceeded) {
    Write-Host "   Backend port 3001 is OPEN" -ForegroundColor Green
} else {
    Write-Host "   Backend port 3001 is CLOSED" -ForegroundColor Red
    Write-Host "   Start backend: node backend-example/server.js" -ForegroundColor Yellow
    Write-Host ""
    exit
}
Write-Host ""

# Test 2: Check backend health endpoint
Write-Host "2. Testing backend health endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:3001/health" -Method Get -TimeoutSec 5
    Write-Host "   Backend is responding" -ForegroundColor Green
    Write-Host "   Status: $($health.status)" -ForegroundColor Gray
} catch {
    Write-Host "   Backend not responding" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    exit
}
Write-Host ""

# Test 3: Check if documents endpoint works
Write-Host "3. Testing documents endpoint..." -ForegroundColor Yellow
try {
    $docs = Invoke-RestMethod -Uri "http://localhost:3001/api/documents" -Method Get -TimeoutSec 5
    if ($docs.success) {
        Write-Host "   Documents endpoint working" -ForegroundColor Green
        Write-Host "   Found $($docs.documents.Count) document(s)" -ForegroundColor Gray
        
        if ($docs.documents.Count -gt 0) {
            Write-Host ""
            Write-Host "   First document:" -ForegroundColor Gray
            Write-Host "   - Filename: $($docs.documents[0].filename)" -ForegroundColor Gray
            Write-Host "   - ID: $($docs.documents[0].id)" -ForegroundColor Gray
        }
    } else {
        Write-Host "   Documents endpoint returned error" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   Documents endpoint failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: Check frontend port
Write-Host "4. Checking if frontend is running on port 5173..." -ForegroundColor Yellow
$frontendTest = Test-NetConnection -ComputerName localhost -Port 5173 -WarningAction SilentlyContinue
if ($frontendTest.TcpTestSucceeded) {
    Write-Host "   Frontend port 5173 is OPEN" -ForegroundColor Green
} else {
    Write-Host "   Frontend port 5173 is CLOSED" -ForegroundColor Yellow
    Write-Host "   Start frontend: npm run dev" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: Check Node.js version
Write-Host "5. Checking Node.js version..." -ForegroundColor Yellow
$nodeVersion = node --version
Write-Host "   Node.js: $nodeVersion" -ForegroundColor Gray
Write-Host ""

# Summary
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host ""

if ($portTest.TcpTestSucceeded -and $health.status -eq "ok") {
    Write-Host "Backend is running and healthy" -ForegroundColor Green
    Write-Host ""
    Write-Host "If delete is still failing:" -ForegroundColor Yellow
    Write-Host "1. Check browser console (F12) for errors" -ForegroundColor White
    Write-Host "2. Check backend terminal for error logs" -ForegroundColor White
    Write-Host "3. Verify document ID is valid" -ForegroundColor White
    Write-Host "4. Check Supabase RLS policies" -ForegroundColor White
    Write-Host ""
    Write-Host "See TROUBLESHOOTING_DELETE.md for detailed help" -ForegroundColor Cyan
} else {
    Write-Host "Issues detected - fix the errors above first" -ForegroundColor Red
}
Write-Host ""