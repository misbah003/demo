#!/usr/bin/env python
"""
Test script to verify CORS and /health endpoint fixes
"""
import requests
import json
import time

# Test URLs (for local testing, use http://localhost:8000)
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test /health endpoint for Render health checks"""
    print("\n" + "="*60)
    print("🏥 Testing /health endpoint (for Render deployment)")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"📋 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ /health endpoint working correctly!")
            return True
        else:
            print("❌ /health endpoint returned unexpected status")
            return False
    except Exception as e:
        print(f"❌ Error testing /health: {e}")
        return False

def test_predict_endpoint():
    """Test /predict endpoint with sample data"""
    print("\n" + "="*60)
    print("🎯 Testing /predict endpoint (VAT Refund Prediction)")
    print("="*60)
    
    payload = {
        "data": {
            "businessType": "Manufacturing",
            "turnover": 700000,
            "vatPaid": 550000,
            "vatClaimed": 678990,
            "category": "Electronics",
            "region": "Uttar Pradesh",
            "filingStatus": "Filed",
            "riskScore": 0.3
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Status: {response.status_code}")
        print(f"📋 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if "predictedRefund" in data and "approvalProbability" in data:
                print(f"✅ Prediction successful!")
                print(f"   💰 Predicted Refund: ₹{data['predictedRefund']:,.2f}")
                print(f"   📊 Approval Probability: {data['approvalProbability']}%")
                print(f"   ⚠️  Risk Level: {data['riskAssessment']['level']}")
                return True
            else:
                print("❌ Response missing required fields")
                return False
        else:
            print(f"❌ Prediction failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing /predict: {e}")
        return False

def test_cors_headers():
    """Test CORS headers in response"""
    print("\n" + "="*60)
    print("🔐 Testing CORS Headers")
    print("="*60)
    
    try:
        # Send OPTIONS request for preflight
        response = requests.options(
            f"{BASE_URL}/predict",
            headers={
                "Origin": "https://ai-powered-tax-ml.vercel.app",
                "Access-Control-Request-Method": "POST"
            },
            timeout=5
        )
        
        print(f"✅ OPTIONS Status: {response.status_code}")
        
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin", "NOT FOUND"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods", "NOT FOUND"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers", "NOT FOUND"),
        }
        
        print(f"📋 CORS Headers:")
        for header, value in cors_headers.items():
            print(f"   {header}: {value}")
        
        if cors_headers["Access-Control-Allow-Origin"] != "NOT FOUND":
            print("✅ CORS headers present!")
            return True
        else:
            print("❌ CORS headers missing")
            return False
            
    except Exception as e:
        print(f"❌ Error testing CORS: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "🚀 NAVI TAX ML API - CORS & HEALTH CHECK TEST 🚀".center(60))
    print("="*60)
    
    results = {
        "health": False,
        "cors": False,
        "predict": False
    }
    
    # Run tests
    results["health"] = test_health_endpoint()
    time.sleep(1)
    results["cors"] = test_cors_headers()
    time.sleep(1)
    results["predict"] = test_predict_endpoint()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.upper().ljust(15)} {status}")
    
    all_passed = all(results.values())
    print("="*60)
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED! API is ready for deployment.")
        exit(0)
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        exit(1)