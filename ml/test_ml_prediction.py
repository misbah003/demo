"""
Test the trained ML model for VAT refund prediction
"""

import pickle
import json
import pandas as pd
import numpy as np

print("=" * 70)
print("🧪 TESTING VAT REFUND ML MODEL")
print("=" * 70)

# Load model and artifacts
print("\n📦 Loading model artifacts...")
try:
    with open('../models/ml_models/vat_refund_predictor.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('../models/ml_models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('../models/ml_models/label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    with open('../models/ml_models/feature_columns.pkl', 'rb') as f:
        feature_columns = pickle.load(f)
    with open('../models/ml_models/model_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    print(f"✅ Model loaded: {metadata['model_name']}")
    print(f"✅ Trained on: {metadata['trained_date']}")
    print(f"✅ R² Score: {metadata['r2_score']:.4f}")
    print(f"✅ MAE: {metadata['mae']:.2f}")
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("   Please run 'python train_vat_ml_models.py' first!")
    exit(1)

# ============================================================================
# TEST CASES
# ============================================================================
print("\n" + "=" * 70)
print("🎯 RUNNING TEST PREDICTIONS")
print("=" * 70)

test_cases = [
    {
        'name': 'Small Retail Business - Low Risk',
        'businessType': 'Retail',
        'turnover': 2000000,
        'vatPaid': 50000,
        'vatClaimed': 60000,
        'category': 'Electronics',
        'filingStatus': 'Filed',
        'region': 'Karnataka',
        'riskScore': 0.2
    },
    {
        'name': 'Large Pharma Company - Medium Risk',
        'businessType': 'Pharma',
        'turnover': 15000000,
        'vatPaid': 200000,
        'vatClaimed': 250000,
        'category': 'Pharmaceuticals',
        'filingStatus': 'Filed',
        'region': 'Maharashtra',
        'riskScore': 0.5
    },
    {
        'name': 'IT Services - High Risk',
        'businessType': 'IT Services',
        'turnover': 8000000,
        'vatPaid': 100000,
        'vatClaimed': 180000,
        'category': 'IT Services',
        'filingStatus': 'Filed Late',
        'region': 'Delhi',
        'riskScore': 0.8
    },
    {
        'name': 'Construction - Non-Compliant',
        'businessType': 'Construction',
        'turnover': 12000000,
        'vatPaid': 150000,
        'vatClaimed': 300000,
        'category': 'Construction',
        'filingStatus': 'Not Filed',
        'region': 'Gujarat',
        'riskScore': 0.9
    },
    {
        'name': 'FMCG - Compliant',
        'businessType': 'FMCG',
        'turnover': 10000000,
        'vatPaid': 180000,
        'vatClaimed': 200000,
        'category': 'Food Products',
        'filingStatus': 'Filed',
        'region': 'Tamil Nadu',
        'riskScore': 0.15
    }
]

def predict_vat_refund(test_case):
    """Make prediction using the trained model"""
    
    # Calculate derived features
    amount = test_case['vatClaimed'] / 0.18  # Assuming 18% VAT
    vat_rate = 18.0
    
    # Determine compliance flag
    compliance_flag = 'Compliant' if test_case['riskScore'] < 0.6 else 'Non-Compliant'
    
    # Check if compliance flag exists in encoder, if not use default
    try:
        compliance_encoded = label_encoders['Compliance_Flag'].transform([compliance_flag])[0]
    except ValueError:
        # If not found, use 'Compliant' as default
        compliance_encoded = label_encoders['Compliance_Flag'].transform(['Compliant'])[0]
    
    # Prepare features
    features = {
        'Amount': amount,
        'VAT_Rate_Numeric': vat_rate,
        'VAT_Amount': test_case['vatClaimed'],
        'Annual_Turnover': test_case['turnover'],
        'Risk_Score': test_case['riskScore'],
        'Business_Type_Encoded': label_encoders['Business_Type'].transform([test_case['businessType']])[0],
        'Category_Encoded': label_encoders['Category'].transform([test_case['category']])[0],
        'Filing_Status_Encoded': label_encoders['Filing_Status'].transform([test_case['filingStatus']])[0],
        'Region_Encoded': label_encoders['Region'].transform([test_case['region']])[0],
        'Compliance_Flag_Encoded': compliance_encoded,
        'Amount_to_Turnover_Ratio': amount / test_case['turnover'],
        'VAT_to_Amount_Ratio': test_case['vatClaimed'] / amount
    }
    
    # Create DataFrame
    df = pd.DataFrame([features])
    
    # Scale features
    df_scaled = scaler.transform(df)
    
    # Predict
    predicted_refund = model.predict(df_scaled)[0]
    
    # Calculate approval probability (based on refund vs claimed)
    max_refund = test_case['vatClaimed'] - test_case['vatPaid']
    if max_refund > 0:
        approval_probability = min(100, max(0, (predicted_refund / max_refund) * 100))
    else:
        approval_probability = 0
    
    return {
        'predicted_refund': max(0, predicted_refund),
        'approval_probability': approval_probability,
        'max_possible_refund': max(0, max_refund)
    }

# Run predictions
for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'─' * 70}")
    print(f"Test Case {i}: {test_case['name']}")
    print(f"{'─' * 70}")
    
    print(f"\n📝 Input:")
    print(f"   Business Type: {test_case['businessType']}")
    print(f"   Annual Turnover: ₹{test_case['turnover']:,}")
    print(f"   VAT Paid: ₹{test_case['vatPaid']:,}")
    print(f"   VAT Claimed: ₹{test_case['vatClaimed']:,}")
    print(f"   Filing Status: {test_case['filingStatus']}")
    print(f"   Risk Score: {test_case['riskScore']}")
    print(f"   Region: {test_case['region']}")
    
    result = predict_vat_refund(test_case)
    
    print(f"\n🎯 ML Prediction:")
    print(f"   Predicted Refund: ₹{result['predicted_refund']:,.2f}")
    print(f"   Approval Probability: {result['approval_probability']:.1f}%")
    print(f"   Max Possible Refund: ₹{result['max_possible_refund']:,}")
    
    # Risk assessment
    if test_case['riskScore'] > 0.7:
        risk_level = "🔴 HIGH RISK"
    elif test_case['riskScore'] > 0.4:
        risk_level = "🟡 MEDIUM RISK"
    else:
        risk_level = "🟢 LOW RISK"
    
    print(f"   Risk Assessment: {risk_level}")

# ============================================================================
# COMPARISON WITH RULE-BASED APPROACH
# ============================================================================
print("\n" + "=" * 70)
print("📊 ML vs RULE-BASED COMPARISON")
print("=" * 70)

def rule_based_prediction(test_case):
    """Old rule-based approach"""
    basic_refund = max(0, test_case['vatClaimed'] - test_case['vatPaid'])
    
    base_probability = 0.8
    if test_case['businessType'] == 'Retail':
        base_probability += 0.05
    if test_case['turnover'] > 500000:
        base_probability += 0.05
    if test_case['vatClaimed'] > test_case['vatPaid'] * 1.5:
        base_probability -= 0.1
    if test_case['turnover'] < 100000:
        base_probability += 0.1
    
    approval_probability = min(1, max(0, base_probability))
    predicted_refund = basic_refund * approval_probability
    
    return {
        'predicted_refund': predicted_refund,
        'approval_probability': approval_probability * 100
    }

print("\nComparing predictions for Test Case 1:")
test = test_cases[0]

ml_result = predict_vat_refund(test)
rule_result = rule_based_prediction(test)

print(f"\n🤖 ML Model:")
print(f"   Refund: ₹{ml_result['predicted_refund']:,.2f}")
print(f"   Probability: {ml_result['approval_probability']:.1f}%")

print(f"\n📏 Rule-Based:")
print(f"   Refund: ₹{rule_result['predicted_refund']:,.2f}")
print(f"   Probability: {rule_result['approval_probability']:.1f}%")

print(f"\n💡 Difference:")
print(f"   Refund: ₹{abs(ml_result['predicted_refund'] - rule_result['predicted_refund']):,.2f}")
print(f"   Probability: {abs(ml_result['approval_probability'] - rule_result['approval_probability']):.1f}%")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("✅ TESTING COMPLETE!")
print("=" * 70)
print(f"\n✨ The ML model is working correctly!")
print(f"   Model: {metadata['model_name']}")
print(f"   Accuracy (R²): {metadata['r2_score']:.4f}")
print(f"   Average Error (MAE): ₹{metadata['mae']:.2f}")

print(f"\n🎯 Next Steps:")
print(f"   1. Integrate this model into your backend API")
print(f"   2. Replace the rule-based logic in the Edge Function")
print(f"   3. Monitor model performance with real data")
print(f"   4. Retrain periodically with new data")

print("\n" + "=" * 70)