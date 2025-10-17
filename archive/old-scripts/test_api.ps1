$body = @{
    businessType = "Manufacturing"
    turnover = 500000
    vatPaid = 90000
    vatClaimed = 50000
    category = "Electronics"
    region = "North"
    filingStatus = "On-Time"
    riskScore = 0.3
} | ConvertTo-Json

Write-Host "Sending request to API..."
Write-Host "Body: $body"

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5001/predict" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Success!"
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $_"
    Write-Host "Response: $($_.Exception.Response)"
}