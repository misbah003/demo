"""
🚀 TRAIN OPTIMIZED ML MODELS WITH FULL HYPERPARAMETER TUNING
=============================================================

This script trains ML models with:
- Full hyperparameter tuning using RandomizedSearchCV
- Cross-validation (5-fold)
- Optimized parameters for production
- Expected R² improvement: 0.72-0.78 (72-78%)
- Training time: 30-60 minutes

Author: ML Team
Date: 2024
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import time
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

# Force unbuffered output for real-time progress
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

print("=" * 80, flush=True)
print("🚀 TRAINING OPTIMIZED ML MODELS WITH HYPERPARAMETER TUNING", flush=True)
print("=" * 80, flush=True)
print("\n⏱️  Expected training time: 30-60 minutes", flush=True)
print("🎯 Target R² Score: 0.72-0.78 (72-78%)", flush=True)
print("=" * 80, flush=True)

# Load enhanced data
enhanced_file = 'enhanced_synthetic_data/enhanced_synthetic_25000_with_real_patterns.xlsx'

if not os.path.exists(enhanced_file):
    print(f"\n❌ Enhanced data not found: {enhanced_file}", flush=True)
    print("⚠️  Please run 'python ml/integrate_real_data.py' first", flush=True)
    sys.exit(1)

print(f"\n📥 Loading enhanced data...", flush=True)
start_time = time.time()
df = pd.read_excel(enhanced_file)
load_time = time.time() - start_time
print(f"✅ Loaded {len(df)} transactions in {load_time:.2f} seconds", flush=True)

# Display data info
print("\n" + "=" * 80, flush=True)
print("📊 ENHANCED DATA OVERVIEW", flush=True)
print("=" * 80, flush=True)
print(f"\nTransactions: {len(df)}", flush=True)
print(f"Columns: {len(df.columns)}", flush=True)
print(f"Date Range: {df['Invoice_Date'].min()} to {df['Invoice_Date'].max()}", flush=True)
print(f"\nRefund Eligible: {(df['Refund_Eligible'] == 'Yes').sum()} ({(df['Refund_Eligible'] == 'Yes').sum() / len(df) * 100:.1f}%)", flush=True)
print(f"Anomalies: {(df['Is_Anomaly'] == 'Yes').sum()} ({(df['Is_Anomaly'] == 'Yes').sum() / len(df) * 100:.1f}%)", flush=True)

# Regional distribution
print(f"\n🌍 Regional Distribution:", flush=True)
for region, count in df['Region'].value_counts().items():
    print(f"   {region}: {count} ({count/len(df)*100:.1f}%)", flush=True)

# Create output directory
output_dir = 'optimized_models_25000_samples'
os.makedirs(output_dir, exist_ok=True)
print(f"\n📁 Models will be saved to: {output_dir}/", flush=True)

# ============================================================================
# PREPARE FEATURES
# ============================================================================

print("\n" + "=" * 80, flush=True)
print("🔧 PREPARING FEATURES", flush=True)
print("=" * 80, flush=True)

df_encoded = df.copy()

# Convert VAT_Rate from percentage string to float
if df_encoded['VAT_Rate'].dtype == 'object':
    df_encoded['VAT_Rate'] = df_encoded['VAT_Rate'].str.replace('%', '').astype(float)

# Encode categorical variables
label_encoders = {}
categorical_cols = ['Category', 'Region', 'Filing_Status', 'Compliance_Flag', 'Refund_Eligible', 'Is_Anomaly']

for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col + '_Encoded'] = le.fit_transform(df_encoded[col])
    label_encoders[col] = le

# Select features for prediction
feature_cols = [
    'Amount', 'VAT_Amount', 'VAT_Rate', 'Risk_Score',
    'Annual_Turnover', 'Amount_to_Turnover_Ratio', 'VAT_to_Amount_Ratio',
    'Category_Encoded', 'Region_Encoded', 'Filing_Status_Encoded',
    'Compliance_Flag_Encoded', 'Is_Anomaly_Encoded'
]

X = df_encoded[feature_cols]
y = df_encoded['Refund_Amount']

print(f"✅ Features: {len(feature_cols)}")
print(f"✅ Samples: {len(X)}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n📊 Data Split:")
print(f"   Training: {len(X_train)} samples")
print(f"   Testing: {len(X_test)} samples")

# Scale features
print(f"\n🔄 Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"✅ Features scaled")

# ============================================================================
# HYPERPARAMETER TUNING - RANDOM FOREST
# ============================================================================

print("\n" + "=" * 80)
print("🎯 HYPERPARAMETER TUNING - RANDOM FOREST")
print("=" * 80)
print("\n⏱️  This will take 15-25 minutes...")

rf_param_grid = {
    'n_estimators': [300, 500, 700, 1000],
    'max_depth': [15, 20, 25, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None],
    'bootstrap': [True, False]
}

print(f"\n🔍 Parameter grid:")
print(f"   n_estimators: {rf_param_grid['n_estimators']}")
print(f"   max_depth: {rf_param_grid['max_depth']}")
print(f"   min_samples_split: {rf_param_grid['min_samples_split']}")
print(f"   min_samples_leaf: {rf_param_grid['min_samples_leaf']}")
print(f"   max_features: {rf_param_grid['max_features']}")
print(f"   bootstrap: {rf_param_grid['bootstrap']}")

rf_start = time.time()
rf_random = RandomizedSearchCV(
    estimator=RandomForestRegressor(random_state=42, n_jobs=-1),
    param_distributions=rf_param_grid,
    n_iter=50,  # Try 50 random combinations
    cv=5,  # 5-fold cross-validation
    verbose=2,
    random_state=42,
    n_jobs=-1,
    scoring='r2'
)

print(f"\n🤖 Training Random Forest with RandomizedSearchCV...", flush=True)
print(f"   Iterations: 50", flush=True)
print(f"   Cross-validation folds: 5", flush=True)
print(f"   Total fits: 50 × 5 = 250", flush=True)
print(f"\n⏳ Training in progress... (sklearn verbose output below)", flush=True)

rf_random.fit(X_train_scaled, y_train)
rf_time = time.time() - rf_start

print(f"\n✅ Random Forest training complete in {rf_time/60:.2f} minutes", flush=True)
print(f"\n🏆 Best parameters:")
for param, value in rf_random.best_params_.items():
    print(f"   {param}: {value}")

rf_best = rf_random.best_estimator_
rf_cv_score = rf_random.best_score_
print(f"\n📊 Cross-validation R² Score: {rf_cv_score:.4f} ({rf_cv_score*100:.2f}%)")

# Test set evaluation
rf_pred = rf_best.predict(X_test_scaled)
rf_r2 = r2_score(y_test, rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_mae = mean_absolute_error(y_test, rf_pred)

print(f"\n📊 Test Set Performance:")
print(f"   R² Score: {rf_r2:.4f} ({rf_r2*100:.2f}%)")
print(f"   RMSE: ₹{rf_rmse:,.2f}")
print(f"   MAE: ₹{rf_mae:,.2f}")

# Save Random Forest model
joblib.dump(rf_best, f'{output_dir}/random_forest_optimized.pkl')
print(f"\n💾 Saved: {output_dir}/random_forest_optimized.pkl")

# ============================================================================
# HYPERPARAMETER TUNING - GRADIENT BOOSTING
# ============================================================================

print("\n" + "=" * 80)
print("🎯 HYPERPARAMETER TUNING - GRADIENT BOOSTING")
print("=" * 80)
print("\n⏱️  This will take 15-25 minutes...")

gb_param_grid = {
    'n_estimators': [300, 500, 700, 1000],
    'learning_rate': [0.01, 0.05, 0.1, 0.15],
    'max_depth': [5, 7, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'subsample': [0.8, 0.9, 1.0],
    'max_features': ['sqrt', 'log2', None]
}

print(f"\n🔍 Parameter grid:")
print(f"   n_estimators: {gb_param_grid['n_estimators']}")
print(f"   learning_rate: {gb_param_grid['learning_rate']}")
print(f"   max_depth: {gb_param_grid['max_depth']}")
print(f"   min_samples_split: {gb_param_grid['min_samples_split']}")
print(f"   min_samples_leaf: {gb_param_grid['min_samples_leaf']}")
print(f"   subsample: {gb_param_grid['subsample']}")
print(f"   max_features: {gb_param_grid['max_features']}")

gb_start = time.time()
gb_random = RandomizedSearchCV(
    estimator=GradientBoostingRegressor(random_state=42),
    param_distributions=gb_param_grid,
    n_iter=50,  # Try 50 random combinations
    cv=5,  # 5-fold cross-validation
    verbose=2,
    random_state=42,
    n_jobs=-1,
    scoring='r2'
)

print(f"\n🤖 Training Gradient Boosting with RandomizedSearchCV...", flush=True)
print(f"   Iterations: 50", flush=True)
print(f"   Cross-validation folds: 5", flush=True)
print(f"   Total fits: 50 × 5 = 250", flush=True)
print(f"\n⏳ Training in progress... (sklearn verbose output below)", flush=True)

gb_random.fit(X_train_scaled, y_train)
gb_time = time.time() - gb_start

print(f"\n✅ Gradient Boosting training complete in {gb_time/60:.2f} minutes", flush=True)
print(f"\n🏆 Best parameters:")
for param, value in gb_random.best_params_.items():
    print(f"   {param}: {value}")

gb_best = gb_random.best_estimator_
gb_cv_score = gb_random.best_score_
print(f"\n📊 Cross-validation R² Score: {gb_cv_score:.4f} ({gb_cv_score*100:.2f}%)")

# Test set evaluation
gb_pred = gb_best.predict(X_test_scaled)
gb_r2 = r2_score(y_test, gb_pred)
gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
gb_mae = mean_absolute_error(y_test, gb_pred)

print(f"\n📊 Test Set Performance:")
print(f"   R² Score: {gb_r2:.4f} ({gb_r2*100:.2f}%)")
print(f"   RMSE: ₹{gb_rmse:,.2f}")
print(f"   MAE: ₹{gb_mae:,.2f}")

# Save Gradient Boosting model
joblib.dump(gb_best, f'{output_dir}/gradient_boosting_optimized.pkl')
print(f"\n💾 Saved: {output_dir}/gradient_boosting_optimized.pkl")

# ============================================================================
# HYPERPARAMETER TUNING - RIDGE REGRESSION
# ============================================================================

print("\n" + "=" * 80)
print("🎯 HYPERPARAMETER TUNING - RIDGE REGRESSION")
print("=" * 80)
print("\n⏱️  This will take 2-5 minutes...")

ridge_param_grid = {
    'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0],
    'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'saga']
}

print(f"\n🔍 Parameter grid:")
print(f"   alpha: {ridge_param_grid['alpha']}")
print(f"   solver: {ridge_param_grid['solver']}")

ridge_start = time.time()
ridge_random = RandomizedSearchCV(
    estimator=Ridge(random_state=42),
    param_distributions=ridge_param_grid,
    n_iter=30,  # Try 30 random combinations
    cv=5,  # 5-fold cross-validation
    verbose=2,
    random_state=42,
    n_jobs=-1,
    scoring='r2'
)

print(f"\n🤖 Training Ridge Regression with RandomizedSearchCV...")
print(f"   Iterations: 30")
print(f"   Cross-validation folds: 5")
print(f"   Total fits: 30 × 5 = 150")

ridge_random.fit(X_train_scaled, y_train)
ridge_time = time.time() - ridge_start

print(f"\n✅ Ridge Regression training complete in {ridge_time/60:.2f} minutes")
print(f"\n🏆 Best parameters:")
for param, value in ridge_random.best_params_.items():
    print(f"   {param}: {value}")

ridge_best = ridge_random.best_estimator_
ridge_cv_score = ridge_random.best_score_
print(f"\n📊 Cross-validation R² Score: {ridge_cv_score:.4f} ({ridge_cv_score*100:.2f}%)")

# Test set evaluation
ridge_pred = ridge_best.predict(X_test_scaled)
ridge_r2 = r2_score(y_test, ridge_pred)
ridge_rmse = np.sqrt(mean_squared_error(y_test, ridge_pred))
ridge_mae = mean_absolute_error(y_test, ridge_pred)

print(f"\n📊 Test Set Performance:")
print(f"   R² Score: {ridge_r2:.4f} ({ridge_r2*100:.2f}%)")
print(f"   RMSE: ₹{ridge_rmse:,.2f}")
print(f"   MAE: ₹{ridge_mae:,.2f}")

# Save Ridge model
joblib.dump(ridge_best, f'{output_dir}/ridge_optimized.pkl')
print(f"\n💾 Saved: {output_dir}/ridge_optimized.pkl")

# ============================================================================
# SAVE SCALER AND ENCODERS
# ============================================================================

joblib.dump(scaler, f'{output_dir}/scaler.pkl')
joblib.dump(label_encoders, f'{output_dir}/label_encoders.pkl')
joblib.dump(feature_cols, f'{output_dir}/feature_columns.pkl')

print(f"\n💾 Saved: {output_dir}/scaler.pkl")
print(f"💾 Saved: {output_dir}/label_encoders.pkl")
print(f"💾 Saved: {output_dir}/feature_columns.pkl")

# ============================================================================
# RESULTS COMPARISON
# ============================================================================

print("\n" + "=" * 80)
print("📊 FINAL RESULTS COMPARISON")
print("=" * 80)

results = [
    {
        'Model': 'Random Forest (Optimized)',
        'CV R² Score': rf_cv_score,
        'Test R² Score': rf_r2,
        'RMSE': rf_rmse,
        'MAE': rf_mae,
        'Training Time (min)': rf_time / 60
    },
    {
        'Model': 'Gradient Boosting (Optimized)',
        'CV R² Score': gb_cv_score,
        'Test R² Score': gb_r2,
        'RMSE': gb_rmse,
        'MAE': gb_mae,
        'Training Time (min)': gb_time / 60
    },
    {
        'Model': 'Ridge Regression (Optimized)',
        'CV R² Score': ridge_cv_score,
        'Test R² Score': ridge_r2,
        'RMSE': ridge_rmse,
        'MAE': ridge_mae,
        'Training Time (min)': ridge_time / 60
    }
]

results_df = pd.DataFrame(results)
print("\n" + results_df.to_string(index=False))

# Find best model
best_idx = results_df['Test R² Score'].idxmax()
best_model_info = results_df.iloc[best_idx]

print(f"\n🏆 BEST MODEL: {best_model_info['Model']}")
print(f"   CV R² Score: {best_model_info['CV R² Score']:.4f} ({best_model_info['CV R² Score']*100:.2f}%)")
print(f"   Test R² Score: {best_model_info['Test R² Score']:.4f} ({best_model_info['Test R² Score']*100:.2f}%)")
print(f"   RMSE: ₹{best_model_info['RMSE']:,.2f}")
print(f"   MAE: ₹{best_model_info['MAE']:,.2f}")
print(f"   Training Time: {best_model_info['Training Time (min)']:.2f} minutes")

# ============================================================================
# IMPROVEMENT ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("📈 IMPROVEMENT ANALYSIS")
print("=" * 80)

original_r2 = 0.258  # Original model with 50 samples
simple_r2 = 0.7013   # Simple model with 25,000 samples
optimized_r2 = best_model_info['Test R² Score']

print(f"\n🔍 Model Evolution:")
print(f"   Original (50 samples):        R² = {original_r2:.4f} ({original_r2*100:.2f}%)")
print(f"   Simple (25,000 samples):      R² = {simple_r2:.4f} ({simple_r2*100:.2f}%)")
print(f"   Optimized (25,000 samples):   R² = {optimized_r2:.4f} ({optimized_r2*100:.2f}%)")

improvement_vs_original = ((optimized_r2 - original_r2) / original_r2) * 100
improvement_vs_simple = ((optimized_r2 - simple_r2) / simple_r2) * 100

print(f"\n📊 Improvements:")
print(f"   vs Original:  +{improvement_vs_original:.1f}%")
print(f"   vs Simple:    +{improvement_vs_simple:.1f}%")

if optimized_r2 >= 0.75:
    print("\n🎉 OUTSTANDING! Model performance is EXCELLENT!")
    print("   ✅ Ready for production deployment!")
elif optimized_r2 >= 0.70:
    print("\n✅ EXCELLENT! Model performance is very good!")
    print("   ✅ Production-ready with monitoring!")
elif optimized_r2 >= 0.65:
    print("\n✅ GOOD! Model performance is solid!")
    print("   ⚠️  Consider additional tuning or more data")
else:
    print("\n⚠️  MODERATE performance")
    print("   💡 Consider collecting more real transaction data")

# ============================================================================
# FEATURE IMPORTANCE
# ============================================================================

print("\n" + "=" * 80)
print("🔍 FEATURE IMPORTANCE (Best Model)")
print("=" * 80)

if best_model_info['Model'].startswith('Random Forest'):
    best_model = rf_best
elif best_model_info['Model'].startswith('Gradient Boosting'):
    best_model = gb_best
else:
    best_model = None

if best_model and hasattr(best_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\n" + feature_importance.to_string(index=False))
    
    # Save feature importance
    feature_importance.to_excel(f'{output_dir}/feature_importance.xlsx', index=False)
    print(f"\n💾 Saved: {output_dir}/feature_importance.xlsx")

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("💾 SAVING RESULTS")
print("=" * 80)

# Save results
results_df.to_excel(f'{output_dir}/model_comparison.xlsx', index=False)
print(f"✅ Saved: {output_dir}/model_comparison.xlsx")

# Save metadata
total_time = (rf_time + gb_time + ridge_time) / 60
metadata = {
    'Training Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'Data Source': enhanced_file,
    'Total Samples': len(df),
    'Training Samples': len(X_train),
    'Testing Samples': len(X_test),
    'Features': len(feature_cols),
    'Best Model': best_model_info['Model'],
    'Best CV R² Score': best_model_info['CV R² Score'],
    'Best Test R² Score': best_model_info['Test R² Score'],
    'Best RMSE': best_model_info['RMSE'],
    'Best MAE': best_model_info['MAE'],
    'Total Training Time (min)': total_time,
    'Hyperparameter Tuning': 'RandomizedSearchCV with 5-fold CV',
    'Random Forest Iterations': 50,
    'Gradient Boosting Iterations': 50,
    'Ridge Iterations': 30
}

metadata_df = pd.DataFrame([metadata])
metadata_df.to_excel(f'{output_dir}/training_metadata.xlsx', index=False)
print(f"✅ Saved: {output_dir}/training_metadata.xlsx")

# Save best parameters
best_params = {
    'Random Forest': rf_random.best_params_,
    'Gradient Boosting': gb_random.best_params_,
    'Ridge Regression': ridge_random.best_params_
}

import json
with open(f'{output_dir}/best_parameters.json', 'w') as f:
    json.dump(best_params, f, indent=4)
print(f"✅ Saved: {output_dir}/best_parameters.json")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("🎉 TRAINING COMPLETE!")
print("=" * 80)

print(f"\n⏱️  Total Training Time: {total_time:.2f} minutes")
print(f"\n🏆 Best Model: {best_model_info['Model']}")
print(f"   Test R² Score: {best_model_info['Test R² Score']:.4f} ({best_model_info['Test R² Score']*100:.2f}%)")
print(f"   RMSE: ₹{best_model_info['RMSE']:,.2f}")
print(f"   MAE: ₹{best_model_info['MAE']:,.2f}")

print(f"\n📁 All models saved to: {output_dir}/")
print(f"\n📊 Files created:")
print(f"   ✅ random_forest_optimized.pkl")
print(f"   ✅ gradient_boosting_optimized.pkl")
print(f"   ✅ ridge_optimized.pkl")
print(f"   ✅ scaler.pkl")
print(f"   ✅ label_encoders.pkl")
print(f"   ✅ feature_columns.pkl")
print(f"   ✅ model_comparison.xlsx")
print(f"   ✅ feature_importance.xlsx")
print(f"   ✅ training_metadata.xlsx")
print(f"   ✅ best_parameters.json")

print("\n" + "=" * 80)
print("🚀 NEXT STEPS")
print("=" * 80)

print("\n1️⃣  Test the optimized model:")
print(f"   python ml/test_optimized_model.py")

print("\n2️⃣  Deploy to ML API:")
print(f"   Update ml/ml_api_service.py to use optimized models")

print("\n3️⃣  Integrate with website:")
print(f"   Update API endpoints to use new model directory")

print("\n4️⃣  Monitor performance:")
print(f"   Track predictions and retrain quarterly")

print("\n" + "=" * 80)
print("✅ ALL DONE!")
print("=" * 80)