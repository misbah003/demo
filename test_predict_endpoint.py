#!/usr/bin/env python
"""Test the /predict endpoint locally"""
import json
import os
import sys
from pathlib import Path

# Add ml directory to path
ml_dir = Path(__file__).parent / 'ml'
sys.path.insert(0, str(ml_dir))

# Test data matching frontend format
test_request = {
    "data": {
        "businessType": "Manufacturing",
        "turnover": 500000,
        "vatPaid": 50000,
        "vatClaimed": 45000,
        "category": "Electronics",
        "region": "Maharashtra",
        "filingStatus": "Filed",
        "riskScore": 0.3
    }
}

print("=" * 60)
print("Testing /predict Endpoint")
print("=" * 60)
print(f"\n📝 Request payload:")
print(json.dumps(test_request, indent=2))

try:
    from ml.ml_api_with_explainability import app, predict_vat_refund
    from pydantic import BaseModel
    
    # Define PredictionRequest model
    class PredictionRequest(BaseModel):
        data: dict
    
    # Create request object
    request = PredictionRequest(**test_request)
    
    print("\n⏳ Calling predict_vat_refund...")
    import asyncio
    response = asyncio.run(predict_vat_refund(request))
    
    print("\n✅ Response received:")
    print(json.dumps(response, indent=2))
    
    # Validate response format
    required_fields = ['predictedRefund', 'approvalProbability', 'recommendation', 'riskAssessment', 'modelInfo', 'breakdown']
    for field in required_fields:
        if field not in response:
            print(f"❌ Missing field: {field}")
        else:
            print(f"✓ {field}: Present")
    
    print("\n✅ Test passed!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)