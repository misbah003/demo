#!/usr/bin/env python
"""Test /predict endpoint with edge cases"""
import json
import sys
from pathlib import Path

ml_dir = Path(__file__).parent / 'ml'
sys.path.insert(0, str(ml_dir))

from ml.ml_api_with_explainability import predict_vat_refund
from pydantic import BaseModel
import asyncio

class PredictionRequest(BaseModel):
    data: dict

test_cases = [
    {
        "name": "Normal case",
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
    },
    {
        "name": "High risk",
        "data": {
            "businessType": "Trading",
            "turnover": 200000,
            "vatPaid": 20000,
            "vatClaimed": 18000,
            "category": "Textiles",
            "region": "Gujarat",
            "filingStatus": "Not Filed",
            "riskScore": 0.8
        }
    },
    {
        "name": "Large refund",
        "data": {
            "businessType": "Services",
            "turnover": 2000000,
            "vatPaid": 200000,
            "vatClaimed": 180000,
            "category": "IT Services",
            "region": "Bangalore",
            "filingStatus": "Filed",
            "riskScore": 0.2
        }
    },
    {
        "name": "Zero VAT claimed",
        "data": {
            "businessType": "Retail",
            "turnover": 100000,
            "vatPaid": 5000,
            "vatClaimed": 0,
            "category": "Retail",
            "region": "Delhi",
            "filingStatus": "Filed",
            "riskScore": 0.4
        }
    }
]

print("Testing /predict endpoint with edge cases...")
print("=" * 60)

passed = 0
failed = 0

async def test_case(case):
    global passed, failed
    try:
        request = PredictionRequest(**{"data": case["data"]})
        response = await predict_vat_refund(request)
        
        # Validate response
        assert 'predictedRefund' in response, "Missing predictedRefund"
        assert 'approvalProbability' in response, "Missing approvalProbability"
        assert 'recommendation' in response, "Missing recommendation"
        assert 'riskAssessment' in response, "Missing riskAssessment"
        assert 'modelInfo' in response, "Missing modelInfo"
        assert 'breakdown' in response, "Missing breakdown"
        
        # Validate value ranges
        assert isinstance(response['predictedRefund'], (int, float)), "predictedRefund not numeric"
        assert response['predictedRefund'] >= 0, "predictedRefund is negative"
        assert 0 <= response['approvalProbability'] <= 100, "approvalProbability out of range"
        assert response['recommendation'] in ['auto_approve', 'manual_review'], f"Invalid recommendation: {response['recommendation']}"
        assert response['riskAssessment']['level'] in ['low', 'medium', 'high'], f"Invalid risk level: {response['riskAssessment']['level']}"
        
        print(f"OK: {case['name']}")
        print(f"    Refund: {response['predictedRefund']}, Risk: {response['riskAssessment']['level']}, Approval: {response['approvalProbability']}%")
        passed += 1
        
    except Exception as e:
        print(f"FAIL: {case['name']}")
        print(f"    Error: {e}")
        failed += 1

async def run_tests():
    for case in test_cases:
        await test_case(case)

asyncio.run(run_tests())

print("=" * 60)
print(f"Results: {passed} passed, {failed} failed")

if failed == 0:
    print("ALL TESTS PASSED ✓")
    sys.exit(0)
else:
    print("SOME TESTS FAILED")
    sys.exit(1)