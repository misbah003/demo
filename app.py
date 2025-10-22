import sys
from pathlib import Path

# Add ml directory to path for imports
ml_dir = Path(__file__).parent / 'ml'
sys.path.insert(0, str(ml_dir))

from ml.ml_api_service_optimized import app