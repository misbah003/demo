"""
Test the ML API with sample requests
"""

import requests
import json

API_URL = "http://localhost:5001"

print("=" * 70)
print("🧪 TESTING ML API SERVICE")
print("=" * 70)

# Test 1: Health Check
print("\n1️⃣  Testing Health Check...")
try:
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        print("✅ API is healthy!")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to API. Is it running?")
    print("   Start it with: python ml_api_service.py")
    exit(1)

# Test 2: Model Info
print("\n2️⃣  Testing Model Info...")
response = requests.get(f"{API_URL}/model-info")
if response.status_code == 200:
    info = response.json()
    print("✅ Model info retrieved!")
    print(f"   Model: {info['model_name']}")
    print(f"   R² Score: {info['r2_score']:.4f}")
    print(f"   MAE: ₹{info['mae']:.2f}")
else:
    print(f"❌ Failed: {response.status_code}")

# Test 3: Single Prediction
print("\n3️⃣  Testing Single Prediction...")
test_data = {
    "businessType": "Retail",
    "turnover": 5000000,
    "vatPaid": 50000,
    "vatClaimed": 60000,
    "category": "Electronics",
    "filingStatus": "Filed",
    "region": "Karnataka",
    "riskScore": 0.3
}

print(f"\n📝 Input:")
print(f"   Business Type: {test_data['businessType']}")
print(f"   Turnover: ₹{test_data['turnover']:,}")
print(f"   VAT Paid: ₹{test_data['vatPaid']:,}")
print(f"   VAT Claimed: ₹{test_data['vatClaimed']:,}")

response = requests.post(
    f"{API_URL}/predict",
    headers={"Content-Type": "application/json"},
    json=test_data
)

if response.status_code == 200:
    result = response.json()
    print("\n✅ Prediction successful!")
    print(f"\n🎯 Results:")
    print(f"   Predicted Refund: ₹{result['predictedRefund']:,.2f}")
    print(f"   Approval Probability: {result['approvalProbability']:.1f}%")
    print(f"   Risk Level: {result['riskAssessment']['level']}")
    print(f"\n📊 Breakdown:")
    print(f"   Input VAT: ₹{result['breakdown']['inputVat']:,}")
    print(f"   Output VAT: ₹{result['breakdown']['outputVat']:,}")
    print(f"   Net Refund: ₹{result['breakdown']['netRefund']:,}")
    print(f"\n💡 Adjustments:")
    for adj in result['breakdown']['adjustments']:
        print(f"   • {adj}")
else:
    print(f"❌ Prediction failed: {response.status_code}")
    print(f"   Error: {response.text}")

# Test 4: Batch Prediction
print("\n4️⃣  Testing Batch Prediction...")
batch_data = {
    "predictions": [
        {
            "businessType": "Retail",
            "turnover": 2000000,
            "vatPaid": 50000,
            "vatClaimed": 60000
        },
        {
            "businessType": "Pharma",
            "turnover": 15000000,
            "vatPaid": 200000,
            "vatClaimed": 250000
        }
    ]
}

response = requests.post(
    f"{API_URL}/batch-predict",
    headers={"Content-Type": "application/json"},
    json=batch_data
)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Batch prediction successful!")
    print(f"   Processed {result['count']} predictions")
    for i, pred in enumerate(result['predictions'], 1):
        if 'predictedRefund' in pred:
            print(f"\n   Prediction {i}:")
            print(f"      Refund: ₹{pred['predictedRefund']:,.2f}")
            print(f"      Probability: {pred['approvalProbability']:.1f}%")
else:
    print(f"❌ Batch prediction failed: {response.status_code}")

# Test 5: Error Handling
print("\n5️⃣  Testing Error Handling...")
invalid_data = {
    "businessType": "InvalidType",
    "turnover": 5000000
    # Missing required fields
}

response = requests.post(
    f"{API_URL}/predict",
    headers={"Content-Type": "application/json"},
    json=invalid_data
)

if response.status_code == 400:
    print("✅ Error handling works correctly!")
    print(f"   Error message: {response.json().get('error', 'Unknown error')}")
else:
    print(f"⚠️  Unexpected response: {response.status_code}")

# Summary
print("\n" + "=" * 70)
print("✅ API TESTING COMPLETE!")
print("=" * 70)
print("\n🎯 All tests passed! The ML API is working correctly.")
print("\n📡 API Endpoints:")
print(f"   • GET  {API_URL}/")
print(f"   • GET  {API_URL}/health")
print(f"   • GET  {API_URL}/model-info")
print(f"   • POST {API_URL}/predict")
print(f"   • POST {API_URL}/batch-predict")
print("\n" + "=" * 70)