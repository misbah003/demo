@echo off
REM VAT ML Model Production Deployment Script (Windows)
echo 🚀 VAT ML Model Production Deployment
echo ====================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not available. Please install docker-compose.
    exit /b 1
)

echo ✅ Docker and docker-compose found

REM Create necessary directories
echo 📁 Creating directories...
if not exist logs mkdir logs
if not exist models\ml_models mkdir models\ml_models

REM Build and start services
echo 🐳 Building and starting Docker services...
docker-compose up --build -d

REM Wait for services to be healthy
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check health
echo 🔍 Checking service health...
curl -f http://localhost/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ ML API is healthy!
) else (
    echo ❌ ML API health check failed
    pause
    exit /b 1
)

echo.
echo 🎉 Deployment completed successfully!
echo.
echo Services running:
echo   • ML API: http://localhost
echo   • Nginx Proxy: http://localhost (with rate limiting)
echo.
echo API Endpoints:
echo   • GET  /                      - API documentation
echo   • GET  /health                - Health check
echo   • GET  /model-info            - Model metadata
echo   • GET  /monitoring            - Monitoring statistics
echo   • GET  /drift-status          - Model drift detection
echo   • GET  /economic-indicators   - Economic indicators
echo   • GET  /time-series-forecast  - VAT forecasting
echo   • POST /predict               - Make prediction
echo   • POST /batch-predict         - Batch predictions
echo.
echo To stop services: docker-compose down
echo To view logs: docker-compose logs -f
echo.
pause