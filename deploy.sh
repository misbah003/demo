#!/bin/bash

# VAT ML Model Production Deployment Script
echo "🚀 VAT ML Model Production Deployment"
echo "===================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not available. Please install docker-compose."
    exit 1
fi

echo "✅ Docker and docker-compose found"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs models/ml_models

# Build and start services
echo "🐳 Building and starting Docker services..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check health
echo "🔍 Checking service health..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ ML API is healthy!"
else
    echo "❌ ML API health check failed"
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "Services running:"
echo "  • ML API: http://localhost"
echo "  • Nginx Proxy: http://localhost (with rate limiting)"
echo ""
echo "API Endpoints:"
echo "  • GET  /                      - API documentation"
echo "  • GET  /health                - Health check"
echo "  • GET  /model-info            - Model metadata"
echo "  • GET  /monitoring            - Monitoring statistics"
echo "  • GET  /drift-status          - Model drift detection"
echo "  • GET  /economic-indicators   - Economic indicators"
echo "  • GET  /time-series-forecast  - VAT forecasting"
echo "  • POST /predict               - Make prediction"
echo "  • POST /batch-predict         - Batch predictions"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"