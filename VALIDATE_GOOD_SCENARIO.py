"""
✅ VALIDATE GOOD SCENARIO TEST
==============================

Definitive test to answer:
"Is the model even CAPABLE of returning high predictions?"

If this test returns a low prediction despite all positive signals,
the model has a CRITICAL BIAS problem.

Usage:
    python VALIDATE_GOOD_SCENARIO.py
"""

import requests
import json
import pandas as pd
from datetime import datetime

ML_API_URL = "http://localhost:8000"
PREDICT_ENDPOINT = f"{ML_API_URL}/predict"
EXPLAIN_ENDPOINT = f"{ML_API_URL}/explain"

def check_api():
    """Verify API is running"""
    try:
        response = requests.get(f"{ML_API_URL}/health", timeout=2)
        return True
    except:
        print("❌ ERROR: ML API is not running!")
        print("   Please start it first with: python ml_api.py")
        return False

def format_currency(value):
    """Format as currency"""
    return f"€{value:,.2f}"

def test_scenario(name, description, data, expected_range):
    """Test a single scenario"""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    print(f"Description: {description}")
    print(f"\nInput Data:")
    for key, value in data.items():
        print(f"  {key:25}: {value}")
    
    # Make prediction
    try:
        pred_response = requests.post(PREDICT_ENDPOINT, json=data, timeout=5).json()
        refund = pred_response.get('predicted_refund_amount', 0)
        recommendation = pred_response.get('recommendation', 'N/A')
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return None
    
    # Get SHAP explanation
    try:
        shap_response = requests.post(EXPLAIN_ENDPOINT, json=data, timeout=5).json()
    except:
        shap_response = {}
    
    print(f"\n📊 PREDICTION RESULT:")
    print(f"  Predicted Refund: {format_currency(refund)}")
    print(f"  Recommendation: {recommendation}")
    print(f"  Expected Range: {format_currency(expected_range[0])} - {format_currency(expected_range[1])}")
    
    # Evaluate
    in_range = expected_range[0] <= refund <= expected_range[1]
    status = "✅ PASS" if in_range else "❌ FAIL"
    print(f"  Result: {status}")
    
    # Show SHAP if available
    if "all_features" in shap_response:
        base_value = shap_response.get('base_value', 0)
        features = shap_response.get('all_features', [])
        
        print(f"\n🎯 SHAP ANALYSIS:")
        print(f"  Base Value: {format_currency(base_value)}")
        print(f"  Prediction: {format_currency(refund)}")
        print(f"  Net Change: {format_currency(refund - base_value)}")
        
        print(f"\n  Top 5 Features by Impact:")
        for i, feat in enumerate(features[:5], 1):
            impact = "▲" if feat['shap_value'] > 0 else "▼"
            print(f"    {i}. {feat['feature']:30} {impact} {feat['shap_value']:>10,.2f}")
    
    return {
        "name": name,
        "refund": refund,
        "in_range": in_range,
        "recommendation": recommendation
    }

def run_comprehensive_validation():
    """Run complete validation suite"""
    
    print("\n" + "✅ "*35)
    print("GOOD SCENARIO VALIDATION TEST")
    print("Determining if Model Can Produce High Refunds")
    print("✅ "*35)
    
    if not check_api():
        return
    
    results = []
    
    # Test 1: BASELINE (for comparison)
    print("\n" + "🔄 "*35)
    print("PHASE 1: BASELINE TEST (Current Failing Test)")
    baseline = test_scenario(
        name="Baseline - Original Failing Test",
        description="The test from test_shap.http that returns low refund",
        data={
            "Amount": 50000,
            "VAT_Rate": 19,
            "Risk_Score": 0.3,
            "Annual_Turnover": 500000,
            "Category": "Retail",
            "Region": "East",
            "Filing_Status": "On Time",
            "Compliance_Flag": "Compliant",
            "Refund_Eligible": "Yes",
            "Is_Anomaly": "No"
        },
        expected_range=(2000, 8000)  # Currently ~€3,620
    )
    results.append(baseline)
    
    # Test 2: GOOD SCENARIO (All positive signals)
    print("\n" + "✅ "*35)
    print("PHASE 2: GOOD SCENARIO (All Positive Signals)")
    good = test_scenario(
        name="Good Scenario - All Positive Signals",
        description="High amount, high turnover, low risk, compliant, on-time filing",
        data={
            "Amount": 100000,      # 2x baseline
            "VAT_Rate": 19,        # Standard VAT
            "Risk_Score": 0.1,     # Very low risk (vs 0.3)
            "Annual_Turnover": 1000000,  # 2x baseline
            "Category": "Manufacturing",
            "Region": "North",
            "Filing_Status": "On Time",  # Best filing status
            "Compliance_Flag": "Compliant",
            "Refund_Eligible": "Yes",
            "Is_Anomaly": "No"
        },
        expected_range=(10000, 30000)  # Should be significantly higher
    )
    results.append(good)
    
    # Test 3: EXCELLENT SCENARIO (Premium case)
    print("\n" + "⭐ "*35)
    print("PHASE 3: EXCELLENT SCENARIO (Premium Case)")
    excellent = test_scenario(
        name="Excellent Scenario - Premium Case",
        description="Maximum legitimate values for all positive signals",
        data={
            "Amount": 250000,      # High transaction
            "VAT_Rate": 25,        # High VAT rate (some countries)
            "Risk_Score": 0.05,    # Minimal risk
            "Annual_Turnover": 2000000,  # Large business
            "Category": "Manufacturing",
            "Region": "West",
            "Filing_Status": "On Time",  # Best filing status
            "Compliance_Flag": "Compliant",
            "Refund_Eligible": "Yes",
            "Is_Anomaly": "No"
        },
        expected_range=(20000, 60000)  # Should be very high
    )
    results.append(excellent)
    
    # Test 4: RISKY SCENARIO (For contrast)
    print("\n" + "🔴 "*35)
    print("PHASE 4: RISKY SCENARIO (For Contrast)")
    risky = test_scenario(
        name="Risky Scenario - High Risk",
        description="Similar to baseline but with high risk and anomalies",
        data={
            "Amount": 50000,
            "VAT_Rate": 19,
            "Risk_Score": 0.8,     # High risk
            "Annual_Turnover": 500000,
            "Category": "Retail",
            "Region": "South",
            "Filing_Status": "Late",  # Late filing
            "Compliance_Flag": "Compliant",
            "Refund_Eligible": "Yes",
            "Is_Anomaly": "Yes"    # Anomaly detected
        },
        expected_range=(0, 5000)  # Should be low
    )
    results.append(risky)
    
    # Analysis
    print("\n" + "="*70)
    print("📋 ANALYSIS & DIAGNOSIS")
    print("="*70)
    
    baseline_refund = baseline['refund']
    good_refund = good['refund']
    excellent_refund = excellent['refund']
    risky_refund = risky['refund']
    
    print(f"\n1️⃣ BASELINE REFUND: {format_currency(baseline_refund)}")
    print(f"   Good Scenario: {format_currency(good_refund)}")
    print(f"   Ratio: {good_refund / baseline_refund:.2f}x")
    
    if good_refund > baseline_refund * 1.5:
        print(f"   ✅ Model IS RESPONSIVE - Good scenario is {((good_refund/baseline_refund - 1)*100):.0f}% higher")
    else:
        print(f"   ❌ Model IS CONSERVATIVE - Only {((good_refund/baseline_refund - 1)*100):.0f}% increase despite better signals")
    
    print(f"\n2️⃣ EXCELLENT SCENARIO: {format_currency(excellent_refund)}")
    if excellent_refund > 20000:
        print(f"   ✅ Model CAN produce high refunds")
    else:
        print(f"   ❌ Model struggles to produce high refunds even in premium cases")
    
    print(f"\n3️⃣ RISK SENSITIVITY: {format_currency(risky_refund)}")
    if risky_refund < baseline_refund:
        print(f"   ✅ Model correctly reduces refund for risky case")
    else:
        print(f"   ❌ Model doesn't penalize risky cases properly")
    
    print(f"\n4️⃣ OVERALL VERDICT:")
    
    all_pass = all(r['in_range'] for r in results)
    good_pass = good['in_range']
    excellent_pass = excellent['in_range']
    
    if all_pass:
        print(f"   ✅ MODEL IS WELL-CALIBRATED")
        print(f"      All scenarios returned predictions within expected ranges")
    elif good_pass and excellent_pass:
        print(f"   🟡 MODEL IS PARTIALLY RESPONSIVE")
        print(f"      Good scenarios work, but baseline is too conservative")
        print(f"      Recommendation: Reduce conservatism in model calibration")
    elif good_refund > baseline_refund * 2:
        print(f"   ⚠️  MODEL IS OVERLY CONSERVATIVE")
        print(f"      Response is weak even with strong positive signals")
        print(f"      Recommendation: Recalibrate feature weights or rebalance training data")
    else:
        print(f"   🔴 CRITICAL: MODEL HAS SEVERE BIAS")
        print(f"      Model barely responds to positive signals")
        print(f"      Recommendation: Complete model retraining with balanced data required")
    
    print(f"\n5️⃣ KEY METRICS:")
    print(f"   Baseline → Good Improvement: {((good_refund/baseline_refund - 1)*100):+.0f}%")
    print(f"   Baseline → Excellent Improvement: {((excellent_refund/baseline_refund - 1)*100):+.0f}%")
    print(f"   Risk Sensitivity: {((baseline_refund - risky_refund)/baseline_refund*100):.0f}% reduction for high risk")
    
    # Recommendations
    print(f"\n" + "="*70)
    print("💡 NEXT STEPS")
    print("="*70)
    
    if good_refund > baseline_refund * 2:
        print(f"\n✅ Model is RESPONSIVE. Next:")
        print(f"   1. Run SHAP_DIAGNOSTIC_ANALYSIS.py for feature sensitivity")
        print(f"   2. Run ANALYZE_TRAINING_DATA.py for data quality check")
        print(f"   3. Consider feature reweighting in ml_api_service_optimized.py")
    else:
        print(f"\n❌ Model needs investigation. Next:")
        print(f"   1. Check data quality with ANALYZE_TRAINING_DATA.py")
        print(f"   2. Verify feature encoding in ml_api_service_optimized.py")
        print(f"   3. Review training data for systematic bias")
        print(f"   4. Consider retraining model with balanced data")
    
    print(f"\n" + "="*70)

if __name__ == "__main__":
    run_comprehensive_validation()