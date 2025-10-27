#!/usr/bin/env python
"""
🚀 ML API Entry Point for Deployment
=====================================

This script runs the ML API with proper port management for Render deployment.
It can run alongside the Express backend on different ports:
- ML API: Port 8000 (or ML_API_PORT env var)
- Backend: Port 3001 (handled by Express)

Usage:
    python ml_api.py              # Run on default port 8000
    ML_API_PORT=5000 python ml_api.py  # Run on custom port
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add ml directory to path
ml_dir = Path(__file__).parent / 'ml'
sys.path.insert(0, str(ml_dir))

# Set ML_API_PORT environment variable early so services can read it on import
if 'ML_API_PORT' not in os.environ:
    os.environ['ML_API_PORT'] = '8000'

def run_ml_api():
    """Run the ML API service"""
    
    # Get port from environment or use default
    ml_api_port = os.getenv('ML_API_PORT', '8000')
    
    print("=" * 60)
    print("🚀 NAVI TAX ML API")
    print("=" * 60)
    print(f"📍 Starting on port {ml_api_port}...")
    print(f"🌍 API will be available at: http://localhost:{ml_api_port}")
    print("=" * 60)
    print("")
    
    # Try to import and run the optimized ML API service
    try:
        # First, check which API service is available
        api_service = None
        
        # Use explainability first (has all features), then others as fallback
        if os.path.exists('ml/ml_api_with_explainability.py'):
            print("✅ Found ML API with Explainability support (Full features)")
            from ml.ml_api_with_explainability import app
            api_service = 'explainability'
        elif os.path.exists('ml/ml_api_service_advanced.py'):
            print("✅ Found Advanced ML API service")
            from ml.ml_api_service_advanced import app
            api_service = 'advanced'
        elif os.path.exists('ml/ml_api_service_optimized.py'):
            print("✅ Found Optimized ML API service (Fast startup)")
            from ml.ml_api_service_optimized import app
            api_service = 'optimized'
        else:
            print("⚠️  No ML API service found, using basic service")
            from ml.ml_api_service import app
            api_service = 'basic'
        
        print(f"🔧 Using {api_service} ML API service")
        print("")
        print("⏳ Loading models... (this may take 30-60 seconds on first startup)")
        print("")
        
        # Run with gunicorn in production or direct Flask in development
        if os.getenv('NODE_ENV') == 'production':
            print("📦 Running in PRODUCTION mode with Gunicorn")
            os.system(f"gunicorn --bind 0.0.0.0:{ml_api_port} --workers 1 --timeout 120 --access-logfile - --error-logfile - ml_api:app")
        else:
            print("🔧 Running in DEVELOPMENT mode")
            # Run Flask development server
            app.run(
                host='0.0.0.0',
                port=int(ml_api_port),
                debug=False,
                use_reloader=False,
                threaded=True
            )
    
    except ImportError as e:
        print(f"❌ Error importing ML API service: {e}")
        print("💡 Please ensure all ML models are trained and in the models/ directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running ML API: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    try:
        run_ml_api()
    except KeyboardInterrupt:
        print("\n\n⏹️  ML API stopped")
        sys.exit(0)