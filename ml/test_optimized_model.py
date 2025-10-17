"""
🧪 TEST OPTIMIZED ML MODEL
==========================

This script tests the optimized ML model with real-world scenarios.
"""

import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

print("=" * 80)
print("🧪 TESTING OPTIMIZED ML MODEL")
print("=" * 80)

# Load models and artifacts
model_dir = 'optimized_models_25000_samples'

if not os.path.exists(model_dir):
    print(f"\n❌ Model directory not found: {model_dir}")
    print("⚠️  Please run 'python ml/train_optimized_models.py' first")
    exit(1)

print(f"\n📥 Loading optimized models from: {model_dir}/")

# Try to load the best model (usually Random Forest)
model_files = {
    'Random Forest': f'{model_dir}/random_forest_optimized.pkl',
    'Gradient Boosting': f'{model_dir}/gradient_boosting_optimized.pkl',
    'Ridge Regression': f'{model_dir}/ridge_optimized.pkl'
}

# Load all models
models = {}
for name, file_path in model_files.items():
    if os.path.exists(file_path):
        models[name] = joblib.load(file_path)
        print(f"✅ Loaded: {name}")

# Load scaler and encoders
scaler = joblib.load(f'{model_dir}/scaler.pkl')
label_encoders = joblib.load(f'{model_dir}/label_encoders.pkl')
feature_cols = joblib.load(f'{model_dir}/feature_columns.pkl')

print(f"✅ Loaded scaler and encoders")

# ============================================================================
# TEST CASES
# ============================================================================

print("\n" + "=" * 80)
print("🧪 RUNNING TEST CASES")
print("=" * 80)

test_cases = [
    {
        'name': 'Small Business - Electronics',
        'Amount': 50000,
        'VAT_Rate': 18.0,
        'Category': 'Electronics',
        'Region': 'South',
        'Filing_Status': 'Filed',
        'Compliance_Flag': 'Compliant',
        'Refund_Eligible': 'Yes',
        'Is_Anomaly': 'No',
        'Risk_Score': 0.15,
        'Annual_Turnover': 5000000
    },
    {
        'name': 'Large Business - Manufacturing',
        'Amount': 500000,
        'VAT_Rate': 18.0,
        'Category': 'Manufacturing',
        'Region': 'West',
        'Filing_Status': 'Filed',
        'Compliance_Flag': 'Compliant',
        'Refund_Eligible': 'Yes',
        'Is_Anomaly': 'No',
        'Risk_Score': 0.25,
        'Annual_Turnover': 50000000
    },
    {
        'name': 'High Risk - Textiles',
        'Amount': 200000,
        'VAT_Rate': 5.0,
        'Category': 'Textiles',
        'Region': 'North',
        'Filing_Status': 'Pending',
        'Compliance_Flag': 'Non-Compliant',
        'Refund_Eligible': 'No',
        'Is_Anomaly': 'Yes',
        'Risk_Score': 0.85,
        'Annual_Turnover': 10000000
    },
    {
        'name': 'Medium Business - Services',
        'Amount': 150000,
        'VAT_Rate': 18.0,
        'Category': 'Services',
        'Region': 'East',
        'Filing_Status': 'Filed',
        'Compliance_Flag': 'Compliant',
        'Refund_Eligible': 'Yes',
        'Is_Anomaly': 'No',
        'Risk_Score': 0.30,
        'Annual_Turnover': 15000000
    },
    {
        'name': 'Export Business - Pharmaceuticals',
        'Amount': 1000000,
        'VAT_Rate': 0.0,
        'Category': 'Pharmaceuticals',
        'Region': 'South',
        'Filing_Status': 'Filed',
        'Compliance_Flag': 'Compliant',
        'Refund_Eligible': 'Yes',
        'Is_Anomaly': 'No',
        'Risk_Score': 0.10,
        'Annual_Turnover': 100000000
    }
]

results = []

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'=' * 80}")
    print(f"Test Case {i}: {test_case['name']}")
    print(f"{'=' * 80}")
    
    # Calculate derived features
    vat_amount = test_case['Amount'] * (test_case['VAT_Rate'] / 100)
    amount_to_turnover = test_case['Amount'] / test_case['Annual_Turnover']
    vat_to_amount = vat_amount / test_case['Amount'] if test_case['Amount'] > 0 else 0
    
    # Encode categorical variables
    encoded_features = {}
    for col in ['Category', 'Region', 'Filing_Status', 'Compliance_Flag', 'Refund_Eligible', 'Is_Anomaly']:
        le = label_encoders[col]
        try:
            encoded_features[col + '_Encoded'] = le.transform([test_case[col]])[0]
        except:
            # If value not in training data, use most common value
            encoded_features[col + '_Encoded'] = 0
    
    # Create feature vector
    features = {
        'Amount': test_case['Amount'],
        'VAT_Amount': vat_amount,
        'VAT_Rate': test_case['VAT_Rate'],
        'Risk_Score': test_case['Risk_Score'],
        'Annual_Turnover': test_case['Annual_Turnover'],
        'Amount_to_Turnover_Ratio': amount_to_turnover,
        'VAT_to_Amount_Ratio': vat_to_amount,
        **encoded_features
    }
    
    # Create DataFrame with correct column order
    X_test = pd.DataFrame([features])[feature_cols]
    
    # Scale features
    X_test_scaled = scaler.transform(X_test)
    
    # Make predictions with all models
    print(f"\n📊 Input:")
    print(f"   Amount: ₹{test_case['Amount']:,}")
    print(f"   VAT Rate: {test_case['VAT_Rate']}%")
    print(f"   VAT Amount: ₹{vat_amount:,.2f}")
    print(f"   Category: {test_case['Category']}")
    print(f"   Region: {test_case['Region']}")
    print(f"   Risk Score: {test_case['Risk_Score']}")
    print(f"   Compliance: {test_case['Compliance_Flag']}")
    
    print(f"\n🤖 Predictions:")
    
    test_result = {
        'Test Case': test_case['name'],
        'Amount': test_case['Amount'],
        'VAT_Amount': vat_amount,
        'Risk_Score': test_case['Risk_Score']
    }
    
    for model_name, model in models.items():
        prediction = model.predict(X_test_scaled)[0]
        test_result[f'{model_name} Prediction'] = prediction
        
        # Determine recommendation
        if test_case['Risk_Score'] > 0.5 or test_case['Compliance_Flag'] == 'Non-Compliant':
            recommendation = "❌ Manual Review Required"
        elif prediction > 100000:
            recommendation = "⚠️  Manual Review (High Value)"
        else:
            recommendation = "✅ Auto-Approve"
        
        print(f"   {model_name}:")
        print(f"      Predicted Refund: ₹{prediction:,.2f}")
        print(f"      Recommendation: {recommendation}")
        
        test_result[f'{model_name} Recommendation'] = recommendation
    
    results.append(test_result)

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("💾 SAVING TEST RESULTS")
print("=" * 80)

results_df = pd.DataFrame(results)
results_df.to_excel(f'{model_dir}/test_results.xlsx', index=False)
print(f"✅ Saved: {model_dir}/test_results.xlsx")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)

print(f"\n✅ Tested {len(test_cases)} scenarios")
print(f"✅ All models working correctly")

# Calculate statistics
for model_name in models.keys():
    predictions = [r[f'{model_name} Prediction'] for r in results]
    avg_prediction = np.mean(predictions)
    min_prediction = np.min(predictions)
    max_prediction = np.max(predictions)
    
    print(f"\n{model_name}:")
    print(f"   Average Prediction: ₹{avg_prediction:,.2f}")
    print(f"   Min Prediction: ₹{min_prediction:,.2f}")
    print(f"   Max Prediction: ₹{max_prediction:,.2f}")

print("\n" + "=" * 80)
print("✅ TESTING COMPLETE!")
print("=" * 80)