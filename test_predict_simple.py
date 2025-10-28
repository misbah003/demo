#!/usr/bin/env python
"""Test the /predict endpoint locally - simplified version"""
import json
import os
import sys
from pathlib import Path

# Add ml directory to path
ml_dir = Path(__file__).parent / 'ml'
sys.path.insert(0, str(ml_dir))

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

print("Testing /predict endpoint...")

try:
    from ml.ml_api_with_explainability import app, predict_vat_refund
    from pydantic import BaseModel
    
    class PredictionRequest(BaseModel):
        data: dict
    
    request = PredictionRequest(**test_request)
    
    print("Calling predict_vat_refund...")
    import asyncio
    response = asyncio.run(predict_vat_refund(request))
    
    print("Response received:")
    print(json.dumps(response, indent=2))
    
    required_fields = ['predictedRefund', 'approvalProbability', 'recommendation', 'riskAssessment', 'modelInfo', 'breakdown']
    all_present = True
    for field in required_fields:
        if field not in response:
            print(f"Missing field: {field}")
            all_present = False
        else:
            print(f"OK: {field}")
    
    if all_present:
        print("TEST PASSED")
        sys.exit(0)
    else:
        print("TEST FAILED - Missing fields")
        sys.exit(1)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)