#!/usr/bin/env python3
"""
🔍 CORS & API Deployment Verification Test

Tests:
1. /health endpoint responds quickly (no 502)
2. CORS headers are present in responses
3. /predict endpoint accepts requests
4. Preflight OPTIONS requests work
"""

import requests
import json
from datetime import datetime

# API URLs
PROD_API = "https://navi-tax-ml-api.onrender.com"
FRONTEND_ORIGIN = "https://ai-powered-tax-ml.vercel.app"

# Test data
SAMPLE_PREDICTION = {
    "businessType": "Manufacturing",
    "turnover": 700000,
    "vatPaid": 550000,
    "vatClaimed": 678990,
    "category": "Electronics",
    "region": "Uttar Pradesh",
    "filingStatus": "Filed",
    "riskScore": 0.3
}

print("\n" + "="*70)
print("🔍 CORS & API DEPLOYMENT VERIFICATION TEST")
print("="*70)

# ============================================================================
# TEST 1: Check /health endpoint
# ============================================================================
print("\n[TEST 1] Checking /health endpoint...")
try:
    response = requests.get(f"{PROD_API}/health", timeout=5)
    print(f"  Status Code: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    if response.status_code == 200:
        print("  ✅ PASS: /health endpoint is working")
    else:
        print(f"  ❌ FAIL: Expected 200, got {response.status_code}")
        
except requests.exceptions.Timeout:
    print("  ❌ FAIL: /health endpoint timed out (likely still initializing)")
except Exception as e:
    print(f"  ❌ FAIL: {type(e).__name__}: {e}")

# ============================================================================
# TEST 2: Check CORS headers on /health (simulating browser origin)
# ============================================================================
print("\n[TEST 2] Checking CORS headers on /health...")
try:
    headers = {"Origin": FRONTEND_ORIGIN}
    response = requests.get(f"{PROD_API}/health", headers=headers, timeout=5)
    
    cors_origin = response.headers.get("Access-Control-Allow-Origin")
    cors_methods = response.headers.get("Access-Control-Allow-Methods")
    cors_headers = response.headers.get("Access-Control-Allow-Headers")
    
    print(f"  Access-Control-Allow-Origin: {cors_origin}")
    print(f"  Access-Control-Allow-Methods: {cors_methods}")
    print(f"  Access-Control-Allow-Headers: {cors_headers}")
    
    if cors_origin:
        print("  ✅ PASS: CORS headers present")
    else:
        print("  ❌ FAIL: No CORS headers in response")
        
except Exception as e:
    print(f"  ❌ FAIL: {type(e).__name__}: {e}")

# ============================================================================
# TEST 3: Preflight OPTIONS request (browser sends this before POST)
# ============================================================================
print("\n[TEST 3] Testing preflight OPTIONS request...")
try:
    headers = {
        "Origin": FRONTEND_ORIGIN,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"
    }
    response = requests.options(f"{PROD_API}/predict", headers=headers, timeout=5)
    
    print(f"  Status Code: {response.status_code}")
    
    cors_origin = response.headers.get("Access-Control-Allow-Origin")
    cors_methods = response.headers.get("Access-Control-Allow-Methods")
    
    print(f"  Access-Control-Allow-Origin: {cors_origin}")
    print(f"  Access-Control-Allow-Methods: {cors_methods}")
    
    if response.status_code in [200, 204] and cors_origin:
        print("  ✅ PASS: Preflight request successful with CORS headers")
    else:
        print(f"  ❌ FAIL: Preflight failed or missing CORS headers")
        
except Exception as e:
    print(f"  ❌ FAIL: {type(e).__name__}: {e}")

# ============================================================================
# TEST 4: POST /predict endpoint
# ============================================================================
print("\n[TEST 4] Testing /predict endpoint with sample data...")
try:
    headers = {
        "Origin": FRONTEND_ORIGIN,
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{PROD_API}/predict",
        json=SAMPLE_PREDICTION,
        headers=headers,
        timeout=10
    )
    
    print(f"  Status Code: {response.status_code}")
    
    if response.status_code == 200:
        prediction = response.json()
        print(f"  Predicted Refund: ₹{prediction.get('predictedRefund', 'N/A'):,}")
        print(f"  Approval Probability: {prediction.get('approvalProbability', 'N/A')}%")
        print(f"  Recommendation: {prediction.get('recommendation', 'N/A')}")
        print("  ✅ PASS: /predict endpoint working correctly")
    else:
        print(f"  Response: {response.text[:200]}")
        print(f"  ❌ FAIL: Expected 200, got {response.status_code}")
        
except Exception as e:
    print(f"  ❌ FAIL: {type(e).__name__}: {e}")

# ============================================================================
# TEST 5: Check wrapped format also works
# ============================================================================
print("\n[TEST 5] Testing wrapped data format (backward compatibility)...")
try:
    headers = {
        "Origin": FRONTEND_ORIGIN,
        "Content-Type": "application/json"
    }
    wrapped_data = {"data": SAMPLE_PREDICTION}
    response = requests.post(
        f"{PROD_API}/predict",
        json=wrapped_data,
        headers=headers,
        timeout=10
    )
    
    print(f"  Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("  ✅ PASS: Wrapped format also works")
    else:
        print(f"  Response: {response.text[:200]}")
        print(f"  ❌ FAIL: Expected 200, got {response.status_code}")
        
except Exception as e:
    print(f"  ❌ FAIL: {type(e).__name__}: {e}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("📋 VERIFICATION COMPLETE")
print("="*70)
print("\n💡 Next Steps:")
print("1. Wait 2-5 minutes after deployment for Render to update")
print("2. Refresh the frontend and try making a prediction")
print("3. Check browser DevTools (F12) → Network tab for request/response headers")
print("4. Look for green requests (200 status) with CORS headers present")
print("\n✅ If all tests above pass, the API is ready for production!")
print("="*70 + "\n")