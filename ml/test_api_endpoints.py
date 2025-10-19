"""
🧪 API ENDPOINT INTEGRATION TEST
=================================

Tests FastAPI endpoints for explainability service
Requires ml_api_with_explainability.py to be running on port 8000
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test API health check"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        
        data = response.json()
        print("  ✔️  API Status:")
        print(f"     - Status: {data.get('status')}")
        print(f"     - Version: {data.get('version')}")
        print(f"     - Models ready: {data.get('models_ready')}")
        print(f"     - Features: {len(data.get('features', []))} available")
        
        print("\n✅ Health check successful!")
        return True
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API. Is it running on port 8000?")
        print("   Start with: python ml/ml_api_with_explainability.py")
        return False
    except Exception as e:
        print(f"\n❌ Health check failed: {e}")
        return False


def test_status_endpoint():
    """Test detailed status endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Status Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        response.raise_for_status()
        
        data = response.json()
        print("  ✔️  API Details:")
        print(f"     - Status: {data.get('status')}")
        print(f"     - Explainability: {data.get('explainability_enabled')}")
        print(f"     - Methods: {', '.join(data.get('supported_methods', []))}")
        
        print("\n✅ Status endpoint successful!")
        return True
    except Exception as e:
        print(f"\n❌ Status endpoint failed: {e}")
        return False


def test_vat_explanation():
    """Test VAT prediction explanation endpoint"""
    print("\n" + "="*60)
    print("TEST 3: VAT Explanation Endpoint")
    print("="*60)
    
    try:
        # Prepare request
        payload = {
            "features": {
                "region": 1.0,
                "category": 2.0,
                "risk_level": 0.5,
                "transaction_count": 100.0,
                "average_transaction": 5000.0,
                "total_amount": 500000.0,
                "fraud_indicator": 0.0,
                "compliance_score": 0.9
            },
            "amount": 50000.0,
            "method": "shap"
        }
        
        print("  📤 Sending VAT explanation request...")
        response = requests.post(
            f"{BASE_URL}/api/explain-vat",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        print(f"  ✔️  Response structure:")
        print(f"     - Status: {data.get('status')}")
        print(f"     - Method: {data.get('method')}")
        print(f"     - Predicted: €{data.get('data', {}).get('prediction', 0):,.2f}")
        
        print("\n✅ VAT explanation endpoint successful!")
        return True
    except requests.exceptions.Timeout:
        print("\n⚠️  Request timed out. Models may be slow to load.")
        return False
    except Exception as e:
        print(f"\n❌ VAT explanation failed: {e}")
        return False


def test_anomaly_explanation():
    """Test anomaly detection explanation endpoint"""
    print("\n" + "="*60)
    print("TEST 4: Anomaly Detection Explanation")
    print("="*60)
    
    try:
        # Prepare request
        payload = {
            "data": {
                "feature_1": 1.0,
                "feature_2": 2.0,
                "feature_3": 3.0,
                "feature_4": 4.0,
                "feature_5": 5.0
            }
        }
        
        print("  📤 Sending anomaly explanation request...")
        response = requests.post(
            f"{BASE_URL}/api/explain-anomaly",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        print(f"  ✔️  Response structure:")
        print(f"     - Status: {data.get('status')}")
        print(f"     - Is Anomaly: {data.get('data', {}).get('is_anomaly')}")
        print(f"     - Score: {data.get('data', {}).get('anomaly_score')}")
        
        print("\n✅ Anomaly explanation endpoint successful!")
        return True
    except Exception as e:
        print(f"\n❌ Anomaly explanation failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🚀"*30)
    print("  API ENDPOINT INTEGRATION TEST SUITE")
    print("🚀"*30)
    
    print("\n⚠️  Make sure ml_api_with_explainability.py is running!")
    print("   You can start it with: python ml/ml_api_with_explainability.py")
    
    time.sleep(2)
    
    results = {}
    
    # Test 1: Health check
    results['health'] = test_health_check()
    
    # Only continue if API is responding
    if not results['health']:
        print("\n❌ Cannot proceed - API not responding")
        return results
    
    # Test 2: Status
    results['status'] = test_status_endpoint()
    
    # Test 3: VAT explanation
    results['vat'] = test_vat_explanation()
    
    # Test 4: Anomaly explanation
    results['anomaly'] = test_anomaly_explanation()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        print(f"  {status}: {test_name.upper()}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 API INTEGRATION SUCCESSFUL!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed or skipped")
    
    return results


if __name__ == "__main__":
    main()