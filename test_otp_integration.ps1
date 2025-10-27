# Test OTP Integration End-to-End
# This script tests the complete OTP flow

Write-Host "🧪 Testing OTP Integration" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Test 1: Backend OTP endpoint
Write-Host "`n1. Testing backend OTP endpoint..." -ForegroundColor Yellow
$otpTest = Invoke-WebRequest -Uri "https://navi-tax-ml-api.onrender.com/api/send-otp" -Method POST -ContentType "application/json" -Body '{"to": "test@example.com", "otpCode": "123456"}'

if ($otpTest.StatusCode -eq 200) {
    Write-Host "✅ Backend OTP endpoint working" -ForegroundColor Green
    $response = $otpTest.Content | ConvertFrom-Json
    if ($response.success -eq $true -and $response.message -eq "OTP email sent successfully") {
        Write-Host "✅ SendGrid integration confirmed" -ForegroundColor Green
    } else {
        Write-Host "❌ Unexpected response: $($response | ConvertTo-Json)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Backend OTP endpoint failed: $($otpTest.StatusCode)" -ForegroundColor Red
}

# Test 2: Frontend build
Write-Host "`n2. Testing frontend build..." -ForegroundColor Yellow
Set-Location "c:\Users\HomeLaptop\Downloads\navi-tax-35-main\web"
$buildResult = npm run build 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend builds successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
    Write-Host $buildResult -ForegroundColor Red
}

# Test 3: Frontend dev server
Write-Host "`n3. Testing frontend dev server..." -ForegroundColor Yellow
$frontendTest = Invoke-WebRequest -Uri "http://localhost:8081" -Method GET

if ($frontendTest.StatusCode -eq 200) {
    Write-Host "✅ Frontend dev server accessible" -ForegroundColor Green
    if ($frontendTest.Content -match "Tax Intelligence") {
        Write-Host "✅ Frontend content loading correctly" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Frontend content may not be loading correctly" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Frontend dev server not accessible: $($frontendTest.StatusCode)" -ForegroundColor Red
}

# Test 4: Check InputOTP component integration
Write-Host "`n4. Verifying InputOTP component integration..." -ForegroundColor Yellow
$authFile = Get-Content "c:\Users\HomeLaptop\Downloads\navi-tax-35-main\web\src\pages\Auth.tsx"

if ($authFile -match "InputOTP" -and $authFile -match "InputOTPGroup" -and $authFile -match "InputOTPSlot") {
    Write-Host "✅ InputOTP component properly integrated" -ForegroundColor Green
} else {
    Write-Host "❌ InputOTP component not found in Auth.tsx" -ForegroundColor Red
}

Write-Host "`n🎉 OTP Integration Test Complete!" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "To test the full flow manually:" -ForegroundColor White
Write-Host "1. Open http://localhost:8081 in your browser" -ForegroundColor White
Write-Host "2. Navigate to the auth page" -ForegroundColor White
Write-Host "3. Enter an email and request OTP" -ForegroundColor White
Write-Host "4. Check your email for the verification code" -ForegroundColor White
Write-Host "5. Enter the 6-digit code using the individual input slots" -ForegroundColor White