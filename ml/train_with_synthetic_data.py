"""
🚀 TRAIN ML MODELS WITH SYNTHETIC DATA
======================================

This script trains all 3 ML systems with synthetic data and compares
performance against the original 50-sample models.

Systems trained:
1. VAT Refund Prediction (Random Forest, XGBoost, etc.)
2. Anomaly Detection (XGBoost, Random Forest, Logistic Regression)
3. Time Series Forecasting (ARIMA, SARIMA)
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime

print("=" * 70)
print("🚀 TRAINING ML MODELS WITH SYNTHETIC DATA")
print("=" * 70)

# Find synthetic data files
print("\n📁 Looking for synthetic data files...")
synthetic_files = glob.glob('synthetic_data/synthetic_tax_data_*.xlsx')

if not synthetic_files:
    print("❌ No synthetic data found!")
    print("⚠️  Please run 'generate_synthetic_data.py' first")
    exit(1)

print(f"\n✅ Found {len(synthetic_files)} synthetic dataset(s):")
for i, file in enumerate(synthetic_files, 1):
    file_size = os.path.getsize(file) / 1024  # KB
    print(f"   {i}. {os.path.basename(file)} ({file_size:.1f} KB)")

# Select file
if len(synthetic_files) == 1:
    selected_file = synthetic_files[0]
    print(f"\n✅ Using: {os.path.basename(selected_file)}")
else:
    choice = int(input("\nSelect file number: ")) - 1
    selected_file = synthetic_files[choice]

# Load synthetic data
print(f"\n📥 Loading synthetic data...")
df = pd.read_excel(selected_file)
print(f"✅ Loaded {len(df)} transactions")

# Display data info
print("\n" + "=" * 70)
print("📊 SYNTHETIC DATA OVERVIEW")
print("=" * 70)
print(f"\nTransactions: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Date Range: {df['Invoice_Date'].min()} to {df['Invoice_Date'].max()}")
print(f"\nRefund Eligible: {(df['Refund_Eligible'] == 'Yes').sum()} ({(df['Refund_Eligible'] == 'Yes').sum() / len(df) * 100:.1f}%)")
print(f"Anomalies: {(df['Is_Anomaly'] == 'Yes').sum()} ({(df['Is_Anomaly'] == 'Yes').sum() / len(df) * 100:.1f}%)")

# Ask which models to train
print("\n" + "=" * 70)
print("🤖 WHICH MODELS TO TRAIN?")
print("=" * 70)
print("\n1. VAT Refund Prediction only")
print("2. Anomaly Detection only")
print("3. Time Series Forecasting only")
print("4. All models (recommended)")

model_choice = input("\nEnter your choice (1-4): ").strip()

train_refund = model_choice in ['1', '4']
train_anomaly = model_choice in ['2', '4']
train_timeseries = model_choice in ['3', '4']

print("\n✅ Will train:")
if train_refund:
    print("   ✓ VAT Refund Prediction")
if train_anomaly:
    print("   ✓ Anomaly Detection")
if train_timeseries:
    print("   ✓ Time Series Forecasting")

# Create output directory
output_dir = f'synthetic_models_{len(df)}_samples'
os.makedirs(output_dir, exist_ok=True)
print(f"\n📁 Models will be saved to: {output_dir}/")

# ============================================================================
# 1. TRAIN VAT REFUND PREDICTION
# ============================================================================

if train_refund:
    print("\n" + "=" * 70)
    print("🎯 TRAINING VAT REFUND PREDICTION MODELS")
    print("=" * 70)
    
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.neural_network import MLPRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    import xgboost as xgb
    import pickle
    
    # Prepare features
    print("\n📊 Preparing features...")
    df_refund = df.copy()
    
    # Encode categorical variables
    le_category = LabelEncoder()
    le_business = LabelEncoder()
    le_region = LabelEncoder()
    le_filing = LabelEncoder()
    le_compliance = LabelEncoder()
    
    df_refund['Category_Encoded'] = le_category.fit_transform(df_refund['Category'])
    df_refund['Business_Type_Encoded'] = le_business.fit_transform(df_refund['Business_Type'])
    df_refund['Region_Encoded'] = le_region.fit_transform(df_refund['Region'])
    df_refund['Filing_Status_Encoded'] = le_filing.fit_transform(df_refund['Filing_Status'])
    df_refund['Compliance_Flag_Encoded'] = le_compliance.fit_transform(df_refund['Compliance_Flag'])
    
    # Extract VAT rate numeric
    df_refund['VAT_Rate_Numeric'] = df_refund['VAT_Rate'].str.rstrip('%').astype(float) / 100
    
    # Select features
    feature_columns = [
        'Amount', 'VAT_Amount', 'VAT_Rate_Numeric', 'Risk_Score',
        'Annual_Turnover', 'Amount_to_Turnover_Ratio', 'VAT_to_Amount_Ratio',
        'Category_Encoded', 'Business_Type_Encoded', 'Region_Encoded',
        'Filing_Status_Encoded', 'Compliance_Flag_Encoded'
    ]
    
    X = df_refund[feature_columns]
    y = df_refund['Refund_Amount']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"✅ Training samples: {len(X_train)}")
    print(f"✅ Test samples: {len(X_test)}")
    
    # Train models
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
        'XGBoost': xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42),
        'Linear Regression': LinearRegression(),
        'Neural Network': MLPRegressor(hidden_layers=(64, 32), max_iter=500, random_state=42)
    }
    
    results = []
    
    for name, model in models.items():
        print(f"\n🔨 Training {name}...")
        
        if name == 'Neural Network':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            'Model': name,
            'MAE': mae,
            'RMSE': rmse,
            'R2_Score': r2
        })
        
        print(f"   MAE: ₹{mae:,.2f}")
        print(f"   RMSE: ₹{rmse:,.2f}")
        print(f"   R² Score: {r2:.4f}")
    
    # Save results
    df_results = pd.DataFrame(results).sort_values('R2_Score', ascending=False)
    df_results.to_csv(f'{output_dir}/refund_prediction_results.csv', index=False)
    
    # Save best model
    best_model_name = df_results.iloc[0]['Model']
    best_model = models[best_model_name]
    
    with open(f'{output_dir}/best_refund_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   R² Score: {df_results.iloc[0]['R2_Score']:.4f}")
    print(f"✅ Saved to: {output_dir}/best_refund_model.pkl")

# ============================================================================
# 2. TRAIN ANOMALY DETECTION
# ============================================================================

if train_anomaly:
    print("\n" + "=" * 70)
    print("🚨 TRAINING ANOMALY DETECTION MODELS")
    print("=" * 70)
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    from sklearn.model_selection import cross_val_score
    
    # Prepare features (exclude features used to create labels)
    print("\n📊 Preparing features...")
    df_anomaly = df.copy()
    
    # Encode categorical variables
    le_category = LabelEncoder()
    le_business = LabelEncoder()
    le_region = LabelEncoder()
    
    df_anomaly['Category_Encoded'] = le_category.fit_transform(df_anomaly['Category'])
    df_anomaly['Business_Type_Encoded'] = le_business.fit_transform(df_anomaly['Business_Type'])
    df_anomaly['Region_Encoded'] = le_region.fit_transform(df_anomaly['Region'])
    df_anomaly['VAT_Rate_Numeric'] = df_anomaly['VAT_Rate'].str.rstrip('%').astype(float) / 100
    
    # Select features (IMPORTANT: Don't use features that created the label!)
    feature_columns = [
        'Amount', 'VAT_Rate_Numeric', 'Annual_Turnover',
        'Business_Type_Encoded', 'Category_Encoded', 'Region_Encoded'
    ]
    
    X = df_anomaly[feature_columns]
    y = (df_anomaly['Is_Anomaly'] == 'Yes').astype(int)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"✅ Training samples: {len(X_train)}")
    print(f"✅ Test samples: {len(X_test)}")
    print(f"✅ Anomaly rate: {y.sum() / len(y) * 100:.1f}%")
    
    # Train models
    models = {
        'XGBoost': xgb.XGBClassifier(
            n_estimators=100, max_depth=4, learning_rate=0.1,
            min_child_weight=3, random_state=42
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100, max_depth=8, min_samples_split=10, random_state=42
        ),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42)
    }
    
    results = []
    
    for name, model in models.items():
        print(f"\n🔨 Training {name}...")
        
        if name == 'Logistic Regression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_train_pred = model.predict(X_train_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_train_pred = model.predict(X_train)
        
        # Calculate metrics
        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
        
        results.append({
            'Model': name,
            'Train_Accuracy': train_acc,
            'Test_Accuracy': test_acc,
            'Overfitting_Gap': train_acc - test_acc,
            'Precision': precision,
            'Recall': recall,
            'F1_Score': f1,
            'CV_F1_Mean': cv_scores.mean(),
            'CV_F1_Std': cv_scores.std()
        })
        
        print(f"   Train Accuracy: {train_acc:.2%}")
        print(f"   Test Accuracy: {test_acc:.2%}")
        print(f"   Overfitting Gap: {(train_acc - test_acc):.2%}")
        print(f"   F1-Score: {f1:.4f}")
        print(f"   CV F1: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    # Save results
    df_results = pd.DataFrame(results).sort_values('Test_Accuracy', ascending=False)
    df_results.to_csv(f'{output_dir}/anomaly_detection_results.csv', index=False)
    
    # Save best model
    best_model_name = df_results.iloc[0]['Model']
    best_model = models[best_model_name]
    
    with open(f'{output_dir}/best_anomaly_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   Test Accuracy: {df_results.iloc[0]['Test_Accuracy']:.2%}")
    print(f"   F1-Score: {df_results.iloc[0]['F1_Score']:.4f}")
    print(f"✅ Saved to: {output_dir}/best_anomaly_model.pkl")

# ============================================================================
# 3. TRAIN TIME SERIES FORECASTING
# ============================================================================

if train_timeseries:
    print("\n" + "=" * 70)
    print("📈 TRAINING TIME SERIES FORECASTING MODELS")
    print("=" * 70)
    
    from statsmodels.tsa.arima.model import ARIMA
    from sklearn.metrics import mean_absolute_percentage_error
    
    # Prepare time series data
    print("\n📊 Preparing time series data...")
    df_ts = df.copy()
    df_ts['Invoice_Date'] = pd.to_datetime(df_ts['Invoice_Date'])
    
    # Aggregate by month
    df_ts['YearMonth'] = df_ts['Invoice_Date'].dt.to_period('M')
    monthly_data = df_ts.groupby('YearMonth').agg({
        'VAT_Amount': 'sum',
        'Invoice_ID': 'count'
    }).reset_index()
    monthly_data.columns = ['YearMonth', 'Total_VAT', 'Business_Count']
    monthly_data['YearMonth'] = monthly_data['YearMonth'].dt.to_timestamp()
    
    print(f"✅ Monthly data points: {len(monthly_data)}")
    print(f"✅ Date range: {monthly_data['YearMonth'].min()} to {monthly_data['YearMonth'].max()}")
    
    # Split data (80/20)
    train_size = int(len(monthly_data) * 0.8)
    train_data = monthly_data[:train_size]
    test_data = monthly_data[train_size:]
    
    print(f"✅ Training months: {len(train_data)}")
    print(f"✅ Test months: {len(test_data)}")
    
    if len(test_data) < 2:
        print("⚠️  Not enough test data for time series forecasting")
        print("   Need at least 12 months of data")
    else:
        # Auto-tune ARIMA parameters
        print("\n🔍 Auto-tuning ARIMA parameters...")
        best_aic = np.inf
        best_order = None
        
        for p in range(3):
            for d in range(2):
                for q in range(3):
                    try:
                        model = ARIMA(train_data['Total_VAT'], order=(p, d, q))
                        fitted = model.fit()
                        if fitted.aic < best_aic:
                            best_aic = fitted.aic
                            best_order = (p, d, q)
                    except:
                        continue
        
        print(f"✅ Best ARIMA order: {best_order}")
        print(f"✅ AIC: {best_aic:.2f}")
        
        # Train final model
        print(f"\n🔨 Training ARIMA{best_order}...")
        model = ARIMA(train_data['Total_VAT'], order=best_order)
        fitted_model = model.fit()
        
        # Make predictions
        forecast = fitted_model.forecast(steps=len(test_data))
        
        # Calculate metrics
        mape = mean_absolute_percentage_error(test_data['Total_VAT'], forecast) * 100
        rmse = np.sqrt(mean_squared_error(test_data['Total_VAT'], forecast))
        
        print(f"\n📊 Results:")
        print(f"   MAPE: {mape:.2f}%")
        print(f"   RMSE: ₹{rmse:,.2f}")
        
        # Save results
        results = {
            'Model': 'ARIMA',
            'Order': str(best_order),
            'AIC': best_aic,
            'MAPE': mape,
            'RMSE': rmse,
            'Train_Months': len(train_data),
            'Test_Months': len(test_data)
        }
        
        pd.DataFrame([results]).to_csv(f'{output_dir}/timeseries_results.csv', index=False)
        
        # Save model
        with open(f'{output_dir}/best_timeseries_model.pkl', 'wb') as f:
            pickle.dump(fitted_model, f)
        
        print(f"✅ Saved to: {output_dir}/best_timeseries_model.pkl")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("🎉 TRAINING COMPLETE!")
print("=" * 70)

print(f"\n📁 All models saved to: {output_dir}/")
print("\n✅ Generated files:")
for file in os.listdir(output_dir):
    print(f"   - {file}")

print("\n" + "=" * 70)
print("📊 PERFORMANCE COMPARISON")
print("=" * 70)

# Load and display results
if train_refund and os.path.exists(f'{output_dir}/refund_prediction_results.csv'):
    print("\n🎯 VAT Refund Prediction:")
    df_refund_results = pd.read_csv(f'{output_dir}/refund_prediction_results.csv')
    print(df_refund_results.to_string(index=False))

if train_anomaly and os.path.exists(f'{output_dir}/anomaly_detection_results.csv'):
    print("\n🚨 Anomaly Detection:")
    df_anomaly_results = pd.read_csv(f'{output_dir}/anomaly_detection_results.csv')
    print(df_anomaly_results.to_string(index=False))

if train_timeseries and os.path.exists(f'{output_dir}/timeseries_results.csv'):
    print("\n📈 Time Series Forecasting:")
    df_ts_results = pd.read_csv(f'{output_dir}/timeseries_results.csv')
    print(df_ts_results.to_string(index=False))

print("\n" + "=" * 70)
print("🚀 NEXT STEPS")
print("=" * 70)
print("\n1. Compare with original 50-sample models")
print("2. Analyze performance improvements")
print("3. Test models with validation data")
print("4. Deploy best models to production")

print("\n" + "=" * 70)
print("⚠️  REMEMBER: These models trained on SYNTHETIC data!")
print("    For production, retrain on REAL data!")
print("=" * 70)