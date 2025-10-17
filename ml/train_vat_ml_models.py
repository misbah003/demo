"""
VAT Refund Predictor - ML Model Training & Comparison
======================================================
This script trains multiple ML models and selects the best one for VAT refund prediction.

Models tested:
1. Linear Regression (baseline)
2. Random Forest Regressor
3. XGBoost Regressor
4. Neural Network (MLPRegressor)
5. Gradient Boosting Regressor

Metrics: MAE, RMSE, R² Score
"""

import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Try to import XGBoost (optional)
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️  XGBoost not installed. Will skip XGBoost model.")
    print("   Install with: pip install xgboost")

print("=" * 70)
print("🤖 VAT REFUND PREDICTOR - ML MODEL TRAINING")
print("=" * 70)

# ============================================================================
# 1️⃣ LOAD AND PREPARE DATA
# ============================================================================
print("\n📊 Step 1: Loading data from Excel...")

# Try to load large dataset first, fall back to small dataset
data_files = ["../data/AI_Tax_Intelligence_Large.xlsx", "../data/AI_Tax_Intelligence_Expanded.xlsx", "AI_Tax_Intelligence_Expanded.xlsx"]

data_loaded = False
for data_file in data_files:
    try:
        # Load all sheets
        transaction_data = pd.read_excel(data_file, sheet_name="Transaction_Data")
        client_profile = pd.read_excel(data_file, sheet_name="Client_Profile")
        monthly_summary = pd.read_excel(data_file, sheet_name="Monthly_Filing_Summary")

        print(f"✅ Loaded data from {data_file}")
        print(f"   📊 {len(client_profile)} client profiles")
        print(f"   💰 {len(transaction_data)} transactions")
        print(f"   📈 {len(monthly_summary)} monthly summaries")
        data_loaded = True
        break
    except FileNotFoundError:
        continue

if not data_loaded:
    print("❌ Error: No data file found!")
    print("   Please run vat_collection.py first to generate the data.")
    print("   Options:")
    print("   - python vat_collection.py (small dataset)")
    print("   - python vat_collection.py --clients 2000 --transactions 25000 --years 5 (large dataset)")
    exit(1)

# Memory optimization for large datasets
if len(transaction_data) > 10000:
    print("🧠 Large dataset detected - optimizing memory usage...")
    # Convert data types to reduce memory
    transaction_data['Amount'] = transaction_data['Amount'].astype('float32')
    transaction_data['VAT_Amount'] = transaction_data['VAT_Amount'].astype('float32')
    client_profile['Annual_Turnover'] = client_profile['Annual_Turnover'].astype('float32')
    client_profile['Risk_Score'] = client_profile['Risk_Score'].astype('float32')

    # Use categorical data types where appropriate
    categorical_cols = ['Business_Type', 'Filing_Status', 'Refund_Eligible', 'Region', 'Category']
    for col in categorical_cols:
        if col in transaction_data.columns:
            transaction_data[col] = transaction_data[col].astype('category')

    print(f"✅ Memory optimized - using {transaction_data.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB for transactions")

# ============================================================================
# 2️⃣ FEATURE ENGINEERING
# ============================================================================
print("\n🔧 Step 2: Feature Engineering...")

# Merge transaction data with client profile
df = transaction_data.merge(client_profile, on='Client_ID', how='left')

# Extract VAT rate as numeric
df['VAT_Rate_Numeric'] = df['VAT_Rate'].str.rstrip('%').astype(float)

# Encode categorical variables
label_encoders = {}
categorical_cols = ['Business_Type', 'Category', 'Filing_Status', 'Region', 'Compliance_Flag']

for col in categorical_cols:
    le = LabelEncoder()
    df[col + '_Encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le

# Binary encoding
df['Refund_Eligible_Binary'] = (df['Refund_Eligible'] == 'Yes').astype(int)

# Calculate refund amount (target variable)
# Refund = VAT_Amount if eligible, else 0
df['Refund_Amount'] = df['VAT_Amount'] * df['Refund_Eligible_Binary']

# Additional features
df['Amount_to_Turnover_Ratio'] = df['Amount'] / df['Annual_Turnover']
df['VAT_to_Amount_Ratio'] = df['VAT_Amount'] / df['Amount']

print(f"✅ Created {len(df.columns)} features")

# ============================================================================
# 3️⃣ PREPARE TRAINING DATA
# ============================================================================
print("\n📋 Step 3: Preparing training data...")

# Select features for training
feature_columns = [
    'Amount',
    'VAT_Rate_Numeric',
    'VAT_Amount',
    'Annual_Turnover',
    'Risk_Score',
    'Business_Type_Encoded',
    'Category_Encoded',
    'Filing_Status_Encoded',
    'Region_Encoded',
    'Compliance_Flag_Encoded',
    'Amount_to_Turnover_Ratio',
    'VAT_to_Amount_Ratio'
]

X = df[feature_columns]
y = df['Refund_Amount']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"✅ Training set: {len(X_train)} samples")
print(f"✅ Test set: {len(X_test)} samples")
print(f"✅ Features: {len(feature_columns)}")

# ============================================================================
# 4️⃣ TRAIN MULTIPLE MODELS
# ============================================================================
print("\n🚀 Step 4: Training multiple models...")
print("-" * 70)

# Determine if we need batch processing for large datasets
use_batch_training = len(X_train) > 50000
if use_batch_training:
    print("📊 Large dataset detected - using batch training for memory efficiency")
    batch_size = 10000
    print(f"   Batch size: {batch_size} samples")
else:
    print("📊 Using standard training (dataset fits in memory)")

models = {}
results = []

# Model 1: Linear Regression (Baseline)
print("\n1️⃣  Training Linear Regression...")
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)
lr_pred = lr_model.predict(X_test_scaled)
lr_mae = mean_absolute_error(y_test, lr_pred)
lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
lr_r2 = r2_score(y_test, lr_pred)
models['Linear_Regression'] = lr_model
results.append({
    'Model': 'Linear Regression',
    'MAE': lr_mae,
    'RMSE': lr_rmse,
    'R2_Score': lr_r2
})
print(f"   MAE: {lr_mae:.2f} | RMSE: {lr_rmse:.2f} | R²: {lr_r2:.4f}")

# Model 2: Random Forest
print("\n2️⃣  Training Random Forest...")
if use_batch_training:
    # For large datasets, use fewer estimators and shallower trees
    rf_model = RandomForestRegressor(
        n_estimators=50,  # Reduced for speed
        max_depth=8,      # Shallower trees
        random_state=42,
        n_jobs=-1,
        warm_start=False
    )
    print("   Using optimized settings for large dataset")
else:
    rf_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

rf_model.fit(X_train_scaled, y_train)
rf_pred = rf_model.predict(X_test_scaled)
rf_mae = mean_absolute_error(y_test, rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_r2 = r2_score(y_test, rf_pred)
models['Random_Forest'] = rf_model
results.append({
    'Model': 'Random Forest',
    'MAE': rf_mae,
    'RMSE': rf_rmse,
    'R2_Score': rf_r2
})
print(f"   MAE: {rf_mae:.2f} | RMSE: {rf_rmse:.2f} | R²: {rf_r2:.4f}")

# Model 3: Gradient Boosting
print("\n3️⃣  Training Gradient Boosting...")
if use_batch_training:
    # For large datasets, use fewer estimators and subsample
    gb_model = GradientBoostingRegressor(
        n_estimators=50,      # Reduced for speed
        learning_rate=0.1,
        max_depth=4,          # Shallower trees
        subsample=0.8,        # Use subsample for memory efficiency
        random_state=42
    )
    print("   Using optimized settings for large dataset")
else:
    gb_model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

gb_model.fit(X_train_scaled, y_train)
gb_pred = gb_model.predict(X_test_scaled)
gb_mae = mean_absolute_error(y_test, gb_pred)
gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
gb_r2 = r2_score(y_test, gb_pred)
models['Gradient_Boosting'] = gb_model
results.append({
    'Model': 'Gradient Boosting',
    'MAE': gb_mae,
    'RMSE': gb_rmse,
    'R2_Score': gb_r2
})
print(f"   MAE: {gb_mae:.2f} | RMSE: {gb_rmse:.2f} | R²: {gb_r2:.4f}")

# Model 4: XGBoost (if available)
if XGBOOST_AVAILABLE:
    print("\n4️⃣  Training XGBoost...")
    if use_batch_training:
        # For large datasets, optimize XGBoost settings
        xgb_model = xgb.XGBRegressor(
            n_estimators=50,      # Reduced for speed
            learning_rate=0.1,
            max_depth=4,          # Shallower trees
            subsample=0.8,        # Subsample for memory
            colsample_bytree=0.8, # Feature subsampling
            random_state=42,
            n_jobs=-1
        )
        print("   Using optimized settings for large dataset")
    else:
        xgb_model = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )

    xgb_model.fit(X_train_scaled, y_train)
    xgb_pred = xgb_model.predict(X_test_scaled)
    xgb_mae = mean_absolute_error(y_test, xgb_pred)
    xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
    xgb_r2 = r2_score(y_test, xgb_pred)
    models['XGBoost'] = xgb_model
    results.append({
        'Model': 'XGBoost',
        'MAE': xgb_mae,
        'RMSE': xgb_rmse,
        'R2_Score': xgb_r2
    })
    print(f"   MAE: {xgb_mae:.2f} | RMSE: {xgb_rmse:.2f} | R²: {xgb_r2:.4f}")

# Model 5: Neural Network
print("\n5️⃣  Training Neural Network...")
if use_batch_training:
    # For large datasets, use smaller network and batch training
    nn_model = MLPRegressor(
        hidden_layer_sizes=(50, 25),  # Smaller network
        activation='relu',
        solver='adam',
        max_iter=200,                 # Fewer iterations
        batch_size=1000,              # Explicit batch size
        random_state=42,
        early_stopping=True,          # Enable early stopping
        validation_fraction=0.1
    )
    print("   Using optimized settings for large dataset")
else:
    nn_model = MLPRegressor(
        hidden_layer_sizes=(100, 50),
        activation='relu',
        solver='adam',
        max_iter=500,
        random_state=42
    )

nn_model.fit(X_train_scaled, y_train)
nn_pred = nn_model.predict(X_test_scaled)
nn_mae = mean_absolute_error(y_test, nn_pred)
nn_rmse = np.sqrt(mean_squared_error(y_test, nn_pred))
nn_r2 = r2_score(y_test, nn_pred)
models['Neural_Network'] = nn_model
results.append({
    'Model': 'Neural Network',
    'MAE': nn_mae,
    'RMSE': nn_rmse,
    'R2_Score': nn_r2
})
print(f"   MAE: {nn_mae:.2f} | RMSE: {nn_rmse:.2f} | R²: {nn_r2:.4f}")

# ============================================================================
# 5️⃣ COMPARE MODELS AND SELECT BEST
# ============================================================================
print("\n" + "=" * 70)
print("📊 MODEL COMPARISON RESULTS")
print("=" * 70)

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('R2_Score', ascending=False)

print("\n" + results_df.to_string(index=False))

# Select best model (highest R² score)
best_model_name = results_df.iloc[0]['Model']
best_model = models[best_model_name.replace(' ', '_')]
best_r2 = results_df.iloc[0]['R2_Score']
best_mae = results_df.iloc[0]['MAE']
best_rmse = results_df.iloc[0]['RMSE']

print("\n" + "=" * 70)
print(f"🏆 BEST MODEL: {best_model_name}")
print("=" * 70)
print(f"   R² Score: {best_r2:.4f}")
print(f"   MAE: {best_mae:.2f}")
print(f"   RMSE: {best_rmse:.2f}")

# ============================================================================
# 6️⃣ SAVE BEST MODEL AND ARTIFACTS
# ============================================================================
print("\n💾 Step 5: Saving model and artifacts...")

# Create models directory
import os
os.makedirs('../models/ml_models', exist_ok=True)

# Save the best model
model_path = '../models/ml_models/vat_refund_predictor.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(best_model, f)
print(f"✅ Saved best model: {model_path}")

# Save scaler
scaler_path = '../models/ml_models/scaler.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)
print(f"✅ Saved scaler: {scaler_path}")

# Save label encoders
encoders_path = '../models/ml_models/label_encoders.pkl'
with open(encoders_path, 'wb') as f:
    pickle.dump(label_encoders, f)
print(f"✅ Saved label encoders: {encoders_path}")

# Save feature columns
features_path = '../models/ml_models/feature_columns.pkl'
with open(features_path, 'wb') as f:
    pickle.dump(feature_columns, f)
print(f"✅ Saved feature columns: {features_path}")

# Save model metadata
metadata = {
    'model_name': best_model_name,
    'trained_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'r2_score': float(best_r2),
    'mae': float(best_mae),
    'rmse': float(best_rmse),
    'training_samples': len(X_train),
    'test_samples': len(X_test),
    'features': feature_columns,
    'all_results': results
}

metadata_path = '../models/ml_models/model_metadata.json'
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✅ Saved metadata: {metadata_path}")

# Save comparison results
results_df.to_csv('../models/ml_models/model_comparison.csv', index=False)
print(f"✅ Saved comparison: ../models/ml_models/model_comparison.csv")

# ============================================================================
# 7️⃣ FEATURE IMPORTANCE (if available)
# ============================================================================
if hasattr(best_model, 'feature_importances_'):
    print("\n📊 Feature Importance (Top 5):")
    print("-" * 70)
    feature_importance = pd.DataFrame({
        'Feature': feature_columns,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print(feature_importance.head(5).to_string(index=False))
    
    # Save feature importance
    feature_importance.to_csv('../models/ml_models/feature_importance.csv', index=False)
    print(f"\n✅ Saved feature importance: ../models/ml_models/feature_importance.csv")

# ============================================================================
# 8️⃣ TEST PREDICTION
# ============================================================================
print("\n" + "=" * 70)
print("🧪 TESTING PREDICTION")
print("=" * 70)

# Create a sample prediction
sample_data = {
    'Amount': 100000,
    'VAT_Rate_Numeric': 18.0,
    'VAT_Amount': 18000,
    'Annual_Turnover': 5000000,
    'Risk_Score': 0.3,
    'Business_Type_Encoded': label_encoders['Business_Type'].transform(['Retail'])[0],
    'Category_Encoded': label_encoders['Category'].transform(['Electronics'])[0],
    'Filing_Status_Encoded': label_encoders['Filing_Status'].transform(['Filed'])[0],
    'Region_Encoded': label_encoders['Region'].transform(['Karnataka'])[0],
    'Compliance_Flag_Encoded': label_encoders['Compliance_Flag'].transform(['Compliant'])[0],
    'Amount_to_Turnover_Ratio': 100000 / 5000000,
    'VAT_to_Amount_Ratio': 18000 / 100000
}

sample_df = pd.DataFrame([sample_data])
sample_scaled = scaler.transform(sample_df)
prediction = best_model.predict(sample_scaled)[0]

print("\n📝 Sample Input:")
print(f"   Business Type: Retail")
print(f"   Amount: ₹100,000")
print(f"   VAT Rate: 18%")
print(f"   VAT Amount: ₹18,000")
print(f"   Annual Turnover: ₹5,000,000")
print(f"   Risk Score: 0.3")
print(f"   Compliance: Compliant")

print(f"\n🎯 Predicted Refund: ₹{prediction:,.2f}")

# ============================================================================
# 9️⃣ SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("✅ TRAINING COMPLETE!")
print("=" * 70)
print(f"\n📦 Saved artifacts in '../models/ml_models/' directory:")
print(f"   • vat_refund_predictor.pkl - Best model ({best_model_name})")
print(f"   • scaler.pkl - Feature scaler")
print(f"   • label_encoders.pkl - Categorical encoders")
print(f"   • feature_columns.pkl - Feature list")
print(f"   • model_metadata.json - Model information")
print(f"   • model_comparison.csv - All model results")
if hasattr(best_model, 'feature_importances_'):
    print(f"   • feature_importance.csv - Feature rankings")

print(f"\n🎯 Next Steps:")
print(f"   1. Review model_comparison.csv to see all model performances")
print(f"   2. Run 'python test_ml_prediction.py' to test the model")
print(f"   3. Integrate the model into your backend API")

print("\n" + "=" * 70)