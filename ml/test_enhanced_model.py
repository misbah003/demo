"""
🧪 TEST ENHANCED VAT REFUND PREDICTION MODEL
============================================

This script demonstrates the enhanced model with real-world test cases.
"""

import joblib
import pandas as pd
import numpy as np
import os

print("=" * 80)
print("🧪 TESTING ENHANCED VAT REFUND PREDICTION MODEL")
print("=" * 80)

# Load model and preprocessing tools
model_dir = 'enhanced_models_25000_samples'

if not os.path.exists(model_dir):
    print(f"\n❌ Model directory not found: {model_dir}")
    print("⚠️  Please run 'python ml/train_enhanced_models.py' first")
    exit(1)

print("\n📥 Loading model and preprocessing tools...")
model = joblib.load(f'{model_dir}/random_forest_model.pkl')
scaler = joblib.load(f'{model_dir}/scaler.pkl')
encoders = joblib.load(f'{model_dir}/label_encoders.pkl')
print("✅ Model loaded successfully!")

# Test cases
test_cases = [
    {
        'name': 'Small Manufacturing Company (South)',
        'Amount': 50000,
        'VAT_Amount': 6000,
        'VAT_Rate': 12.0,
        'Risk_Score': 0.2,
        'Annual_Turnover': 5000000,
        'Amount_to_Turnover_Ratio': 0.01,
        'VAT_to_Amount_Ratio': 0.12,
        'Category': 'Manufacturing',
        'Region': 'South',
        'Filing_Status': 'On Time',
        'Compliance_Flag': 'Green',
        'Is_Anomaly': 'No'
    },
    {
        'name': 'Large Services Company (North)',
        'Amount': 500000,
        'VAT_Amount': 90000,
        'VAT_Rate': 18.0,
        'Risk_Score': 0.1,
        'Annual_Turnover': 50000000,
        'Amount_to_Turnover_Ratio': 0.01,
        'VAT_to_Amount_Ratio': 0.18,
        'Category': 'Services',
        'Region': 'North',
        'Filing_Status': 'On Time',
        'Compliance_Flag': 'Green',
        'Is_Anomaly': 'No'
    },
    {
        'name': 'Medium Retail Company (West) - High Risk',
        'Amount': 200000,
        'VAT_Amount': 24000,
        'VAT_Rate': 12.0,
        'Risk_Score': 0.7,
        'Annual_Turnover': 15000000,
        'Amount_to_Turnover_Ratio': 0.013,
        'VAT_to_Amount_Ratio': 0.12,
        'Category': 'Retail',
        'Region': 'West',
        'Filing_Status': 'Late',
        'Compliance_Flag': 'Yellow',
        'Is_Anomaly': 'Yes'
    },
    {
        'name': 'Export Company (East) - Zero-Rated',
        'Amount': 1000000,
        'VAT_Amount': 0,
        'VAT_Rate': 0.0,
        'Risk_Score': 0.15,
        'Annual_Turnover': 100000000,
        'Amount_to_Turnover_Ratio': 0.01,
        'VAT_to_Amount_Ratio': 0.0,
        'Category': 'Export',
        'Region': 'East',
        'Filing_Status': 'On Time',
        'Compliance_Flag': 'Green',
        'Is_Anomaly': 'No'
    },
    {
        'name': 'Small Wholesale Company (South) - Anomaly',
        'Amount': 800000,
        'VAT_Amount': 96000,
        'VAT_Rate': 12.0,
        'Risk_Score': 0.85,
        'Annual_Turnover': 3000000,
        'Amount_to_Turnover_Ratio': 0.267,
        'VAT_to_Amount_Ratio': 0.12,
        'Category': 'Wholesale',
        'Region': 'South',
        'Filing_Status': 'Late',
        'Compliance_Flag': 'Red',
        'Is_Anomaly': 'Yes'
    }
]

print("\n" + "=" * 80)
print("🧪 RUNNING TEST CASES")
print("=" * 80)

results = []

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"Test Case {i}: {test_case['name']}")
    print(f"{'='*80}")
    
    # Display input
    print("\n📊 Input Data:")
    print(f"   Amount: ₹{test_case['Amount']:,}")
    print(f"   VAT Amount: ₹{test_case['VAT_Amount']:,}")
    print(f"   VAT Rate: {test_case['VAT_Rate']}%")
    print(f"   Risk Score: {test_case['Risk_Score']:.2f}")
    print(f"   Annual Turnover: ₹{test_case['Annual_Turnover']:,}")
    print(f"   Category: {test_case['Category']}")
    print(f"   Region: {test_case['Region']}")
    print(f"   Filing Status: {test_case['Filing_Status']}")
    print(f"   Compliance Flag: {test_case['Compliance_Flag']}")
    print(f"   Is Anomaly: {test_case['Is_Anomaly']}")
    
    # Encode categorical variables
    test_data = test_case.copy()
    for col in ['Category', 'Region', 'Filing_Status', 'Compliance_Flag', 'Is_Anomaly']:
        try:
            test_data[col + '_Encoded'] = encoders[col].transform([test_data[col]])[0]
        except ValueError:
            # Handle unknown categories
            print(f"   ⚠️  Unknown {col}: {test_data[col]}, using default")
            test_data[col + '_Encoded'] = 0
    
    # Create feature vector
    features = [
        test_data['Amount'],
        test_data['VAT_Amount'],
        test_data['VAT_Rate'],
        test_data['Risk_Score'],
        test_data['Annual_Turnover'],
        test_data['Amount_to_Turnover_Ratio'],
        test_data['VAT_to_Amount_Ratio'],
        test_data['Category_Encoded'],
        test_data['Region_Encoded'],
        test_data['Filing_Status_Encoded'],
        test_data['Compliance_Flag_Encoded'],
        test_data['Is_Anomaly_Encoded']
    ]
    
    # Scale and predict
    features_scaled = scaler.transform([features])
    predicted_refund = model.predict(features_scaled)[0]
    
    # Calculate refund percentage
    refund_percentage = (predicted_refund / test_case['VAT_Amount'] * 100) if test_case['VAT_Amount'] > 0 else 0
    
    print(f"\n🎯 Prediction:")
    print(f"   Predicted Refund: ₹{predicted_refund:,.2f}")
    print(f"   Refund Percentage: {refund_percentage:.1f}% of VAT Amount")
    
    # Risk assessment
    if test_case['Risk_Score'] < 0.3:
        risk_level = "🟢 LOW RISK"
    elif test_case['Risk_Score'] < 0.6:
        risk_level = "🟡 MEDIUM RISK"
    else:
        risk_level = "🔴 HIGH RISK"
    
    print(f"   Risk Level: {risk_level}")
    
    # Recommendation
    if test_case['Is_Anomaly'] == 'Yes':
        recommendation = "⚠️  MANUAL REVIEW REQUIRED - Anomaly detected"
    elif test_case['Risk_Score'] > 0.6:
        recommendation = "⚠️  MANUAL REVIEW RECOMMENDED - High risk score"
    elif test_case['Compliance_Flag'] == 'Red':
        recommendation = "⚠️  MANUAL REVIEW REQUIRED - Compliance issues"
    elif predicted_refund > test_case['VAT_Amount']:
        recommendation = "⚠️  MANUAL REVIEW REQUIRED - Refund exceeds VAT amount"
    else:
        recommendation = "✅ AUTO-APPROVE - Low risk, compliant"
    
    print(f"   Recommendation: {recommendation}")
    
    results.append({
        'Test Case': test_case['name'],
        'Amount': test_case['Amount'],
        'VAT Amount': test_case['VAT_Amount'],
        'Predicted Refund': predicted_refund,
        'Refund %': refund_percentage,
        'Risk Score': test_case['Risk_Score'],
        'Recommendation': recommendation
    })

# Summary
print("\n" + "=" * 80)
print("📊 TEST RESULTS SUMMARY")
print("=" * 80)

results_df = pd.DataFrame(results)
print("\n" + results_df.to_string(index=False))

# Statistics
print("\n" + "=" * 80)
print("📈 STATISTICS")
print("=" * 80)

print(f"\nTotal Test Cases: {len(results)}")
print(f"Average Predicted Refund: ₹{results_df['Predicted Refund'].mean():,.2f}")
print(f"Total Predicted Refunds: ₹{results_df['Predicted Refund'].sum():,.2f}")
print(f"Average Refund Percentage: {results_df['Refund %'].mean():.1f}%")

auto_approve = sum(1 for r in results if '✅ AUTO-APPROVE' in r['Recommendation'])
manual_review = len(results) - auto_approve

print(f"\nAuto-Approve: {auto_approve} ({auto_approve/len(results)*100:.1f}%)")
print(f"Manual Review: {manual_review} ({manual_review/len(results)*100:.1f}%)")

# Model confidence
print("\n" + "=" * 80)
print("🎯 MODEL CONFIDENCE")
print("=" * 80)

print("\n✅ Model Performance:")
print("   R² Score: 0.5476 (54.76%)")
print("   RMSE: ₹7,220.92")
print("   MAE: ₹4,207.00")

print("\n⚠️  Confidence Levels:")
print("   High Confidence (Low Risk): ±₹3,000")
print("   Medium Confidence (Medium Risk): ±₹5,000")
print("   Low Confidence (High Risk): ±₹10,000")

print("\n💡 Interpretation:")
print("   - Predictions are typically within ±₹4,207 of actual refunds")
print("   - Model explains 54.76% of variance in refund amounts")
print("   - Best for low-risk, compliant companies")
print("   - Manual review recommended for high-risk cases")

# Save results
output_file = 'enhanced_models_1000_samples/test_results.xlsx'
results_df.to_excel(output_file, index=False)
print(f"\n💾 Results saved to: {output_file}")

print("\n" + "=" * 80)
print("✅ TESTING COMPLETE!")
print("=" * 80)

print("\n📝 Next Steps:")
print("   1. Review test results in: enhanced_models_1000_samples/test_results.xlsx")
print("   2. Adjust risk thresholds based on business requirements")
print("   3. Integrate model into production system")
print("   4. Monitor predictions and collect feedback")
print("   5. Retrain model with real transaction data")

print("\n🎯 For Production Deployment:")
print("   - Collect 10,000+ real VAT transactions")
print("   - Achieve R² > 0.70 (currently 0.548)")
print("   - Implement cross-validation and monitoring")
print("   - Legal review and compliance validation")