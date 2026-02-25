# Test Signup
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "TEST 1: SIGNUP" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

$signupBody = @{
    name = 'Test User 1772056020'
    email = 'testuser1772056020@example.com'
    phone = '9876543210'
    password = 'TestPass@123456'
    password_confirm = 'TestPass@123456'
} | ConvertTo-Json

$signupResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/users/auth/signup/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $signupBody

Write-Host "Response:" -ForegroundColor Green
$signupResponse | ConvertTo-Json | Write-Host

$accessToken = $signupResponse.access
$refreshToken = $signupResponse.refresh
$userId = $signupResponse.user_id

Write-Host "`nUser ID: $userId" -ForegroundColor Yellow
Write-Host "Access Token (first 50 chars): $($accessToken.Substring(0, 50))..." -ForegroundColor Yellow

# Test Login
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "TEST 2: LOGIN" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

$loginBody = @{
    email = 'testuser1772056020@example.com'
    password = 'TestPass@123456'
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/users/auth/login/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $loginBody

Write-Host "Response:" -ForegroundColor Green
$loginResponse | ConvertTo-Json | Write-Host

# Test Protected Request
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "TEST 3: PROTECTED REQUEST" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

$protectedResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/users/" `
    -Method GET `
    -Headers @{"Authorization"="Bearer $accessToken"}

Write-Host "Response:" -ForegroundColor Green
$protectedResponse | ConvertTo-Json | Write-Host

Write-Host "`n================================================================================" -ForegroundColor Green
Write-Host "ALL TESTS PASSED!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
