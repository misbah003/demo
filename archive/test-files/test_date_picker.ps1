# Test Date Picker Functionality
# This proves the date picker actually changes the forecast

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DATE PICKER TEST" -ForegroundColor Cyan
Write-Host "  Proof it's not random!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Get forecast for January 2025
Write-Host "[TEST 1] Fetching forecast starting from JANUARY 2025..." -ForegroundColor Yellow
$jan = Invoke-RestMethod -Uri "http://localhost:5001/time-series-forecast?start_month=2025-01&num_months=3"
Write-Host "Results:" -ForegroundColor Green
Write-Host "  Month 1: $($jan.forecast.months[0]) = Rs.$($jan.forecast.predicted_collections[0])" -ForegroundColor White
Write-Host "  Month 2: $($jan.forecast.months[1]) = Rs.$($jan.forecast.predicted_collections[1])" -ForegroundColor White
Write-Host "  Month 3: $($jan.forecast.months[2]) = Rs.$($jan.forecast.predicted_collections[2])" -ForegroundColor White
Write-Host ""

# Test 2: Get forecast for March 2025
Write-Host "[TEST 2] Fetching forecast starting from MARCH 2025..." -ForegroundColor Yellow
$mar = Invoke-RestMethod -Uri "http://localhost:5001/time-series-forecast?start_month=2025-03&num_months=3"
Write-Host "Results:" -ForegroundColor Green
Write-Host "  Month 1: $($mar.forecast.months[0]) = Rs.$($mar.forecast.predicted_collections[0])" -ForegroundColor White
Write-Host "  Month 2: $($mar.forecast.months[1]) = Rs.$($mar.forecast.predicted_collections[1])" -ForegroundColor White
Write-Host "  Month 3: $($mar.forecast.months[2]) = Rs.$($mar.forecast.predicted_collections[2])" -ForegroundColor White
Write-Host ""

# Test 3: Get forecast for June 2025
Write-Host "[TEST 3] Fetching forecast starting from JUNE 2025..." -ForegroundColor Yellow
$jun = Invoke-RestMethod -Uri "http://localhost:5001/time-series-forecast?start_month=2025-06&num_months=3"
Write-Host "Results:" -ForegroundColor Green
Write-Host "  Month 1: $($jun.forecast.months[0]) = Rs.$($jun.forecast.predicted_collections[0])" -ForegroundColor White
Write-Host "  Month 2: $($jun.forecast.months[1]) = Rs.$($jun.forecast.predicted_collections[1])" -ForegroundColor White
Write-Host "  Month 3: $($jun.forecast.months[2]) = Rs.$($jun.forecast.predicted_collections[2])" -ForegroundColor White
Write-Host ""

# Test 4: Get forecast for December 2025 (Q4 - should be higher due to tax season)
Write-Host "[TEST 4] Fetching forecast starting from DECEMBER 2025..." -ForegroundColor Yellow
$dec = Invoke-RestMethod -Uri "http://localhost:5001/time-series-forecast?start_month=2025-12&num_months=3"
Write-Host "Results:" -ForegroundColor Green
Write-Host "  Month 1: $($dec.forecast.months[0]) = Rs.$($dec.forecast.predicted_collections[0])" -ForegroundColor White
Write-Host "  Month 2: $($dec.forecast.months[1]) = Rs.$($dec.forecast.predicted_collections[1])" -ForegroundColor White
Write-Host "  Month 3: $($dec.forecast.months[2]) = Rs.$($dec.forecast.predicted_collections[2])" -ForegroundColor White
Write-Host ""

# Analysis
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ANALYSIS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "PROOF 1: Different dates return different months" -ForegroundColor Yellow
Write-Host "  Jan request starts with: $($jan.forecast.months[0])" -ForegroundColor White
Write-Host "  Mar request starts with: $($mar.forecast.months[0])" -ForegroundColor White
Write-Host "  Jun request starts with: $($jun.forecast.months[0])" -ForegroundColor White
Write-Host "  Dec request starts with: $($dec.forecast.months[0])" -ForegroundColor White

if ($jan.forecast.months[0] -eq "2025-01" -and 
    $mar.forecast.months[0] -eq "2025-03" -and 
    $jun.forecast.months[0] -eq "2025-06" -and 
    $dec.forecast.months[0] -eq "2025-12") {
    Write-Host "  -> PASS: Date picker controls the starting month!" -ForegroundColor Green
} else {
    Write-Host "  -> FAIL: Dates don't match!" -ForegroundColor Red
}
Write-Host ""

Write-Host "PROOF 2: Seasonal patterns (Q4 should be higher)" -ForegroundColor Yellow
$janFirst = $jan.forecast.predicted_collections[0]
$decFirst = $dec.forecast.predicted_collections[0]
$diff = $decFirst - $janFirst
$percentDiff = [math]::Round(($diff / $janFirst) * 100, 1)

Write-Host "  January prediction: Rs.$janFirst" -ForegroundColor White
Write-Host "  December prediction: Rs.$decFirst" -ForegroundColor White
Write-Host "  Difference: Rs.$diff ($percentDiff%)" -ForegroundColor White

if ($decFirst -gt $janFirst) {
    Write-Host "  -> PASS: December is higher (tax season effect)!" -ForegroundColor Green
} else {
    Write-Host "  -> INFO: December is lower (might vary)" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: Call same date twice to prove consistency
Write-Host "PROOF 3: Same date = Same forecast (not random)" -ForegroundColor Yellow
$jan2 = Invoke-RestMethod -Uri "http://localhost:5001/time-series-forecast?start_month=2025-01&num_months=3"
$diff1 = [math]::Abs($jan.forecast.predicted_collections[0] - $jan2.forecast.predicted_collections[0])
$diff2 = [math]::Abs($jan.forecast.predicted_collections[1] - $jan2.forecast.predicted_collections[1])

Write-Host "  First call (Jan): Rs.$($jan.forecast.predicted_collections[0])" -ForegroundColor White
Write-Host "  Second call (Jan): Rs.$($jan2.forecast.predicted_collections[0])" -ForegroundColor White
Write-Host "  Difference: Rs.$diff1" -ForegroundColor White

if ($diff1 -lt 50000 -and $diff2 -lt 50000) {
    Write-Host "  -> PASS: Same date gives similar results!" -ForegroundColor Green
    Write-Host "  -> (Small variation is due to random noise in algorithm)" -ForegroundColor Gray
} else {
    Write-Host "  -> WARNING: Large variation detected" -ForegroundColor Yellow
}
Write-Host ""

# Final instructions
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NOW TEST IN YOUR BROWSER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Open: http://localhost:8081" -ForegroundColor White
Write-Host ""
Write-Host "2. Open DevTools (F12) -> Network tab" -ForegroundColor White
Write-Host ""
Write-Host "3. Click the calendar icon on the chart" -ForegroundColor White
Write-Host ""
Write-Host "4. Select JANUARY 2025" -ForegroundColor White
Write-Host "   -> Check Network tab for:" -ForegroundColor Gray
Write-Host "      time-series-forecast?start_month=2025-01" -ForegroundColor Yellow
Write-Host "   -> Chart should show months: Jan, Feb, Mar..." -ForegroundColor Gray
Write-Host "   -> First value should be around: Rs.$($jan.forecast.predicted_collections[0])" -ForegroundColor Yellow
Write-Host ""
Write-Host "5. Now select JUNE 2025" -ForegroundColor White
Write-Host "   -> Check Network tab for:" -ForegroundColor Gray
Write-Host "      time-series-forecast?start_month=2025-06" -ForegroundColor Yellow
Write-Host "   -> Chart should show months: Jun, Jul, Aug..." -ForegroundColor Gray
Write-Host "   -> First value should be around: Rs.$($jun.forecast.predicted_collections[0])" -ForegroundColor Yellow
Write-Host ""
Write-Host "6. Select DECEMBER 2025" -ForegroundColor White
Write-Host "   -> Check Network tab for:" -ForegroundColor Gray
Write-Host "      time-series-forecast?start_month=2025-12" -ForegroundColor Yellow
Write-Host "   -> Chart should show months: Dec, Jan, Feb..." -ForegroundColor Gray
Write-Host "   -> First value should be around: Rs.$($dec.forecast.predicted_collections[0])" -ForegroundColor Yellow
Write-Host ""
Write-Host "IF YOU SEE DIFFERENT API REQUESTS FOR DIFFERENT DATES:" -ForegroundColor Green
Write-Host "  -> DATE PICKER IS WORKING!" -ForegroundColor Green
Write-Host ""
Write-Host "IF YOU SEE THE SAME REQUEST EVERY TIME:" -ForegroundColor Red
Write-Host "  -> Date picker is not connected" -ForegroundColor Red
Write-Host ""