@echo off
echo ========================================
echo Checking What Services Are Running
echo ========================================
echo.

echo Checking ML API (Port 8000)...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/health' -TimeoutSec 2 -UseBasicParsing; Write-Host '✅ ML API is RUNNING' -ForegroundColor Green } catch { Write-Host '❌ ML API is NOT running' -ForegroundColor Red }"
echo.

echo Checking Backend (Port 3001)...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3001/api/health' -TimeoutSec 2 -UseBasicParsing; Write-Host '✅ Backend is RUNNING' -ForegroundColor Green } catch { Write-Host '❌ Backend is NOT running' -ForegroundColor Red }"
echo.

echo Checking Frontend (Port 5173)...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5173' -TimeoutSec 2 -UseBasicParsing; Write-Host '✅ Frontend is RUNNING' -ForegroundColor Green } catch { Write-Host '❌ Frontend is NOT running' -ForegroundColor Red }"
echo.

echo ========================================
echo Node.js Processes Running:
echo ========================================
tasklist /FI "IMAGENAME eq node.exe" 2>nul
echo.

echo ========================================
echo Python Processes Running:
echo ========================================
tasklist /FI "IMAGENAME eq python.exe" 2>nul
echo.

echo ========================================
echo To stop all Node.js processes:
echo   Get-Process -Name node ^| Stop-Process -Force
echo.
echo To stop all Python processes:
echo   Get-Process -Name python ^| Stop-Process -Force
echo ========================================
pause