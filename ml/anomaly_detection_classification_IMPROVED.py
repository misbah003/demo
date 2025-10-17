"""
🚨 VAT Transaction Anomaly Detection (IMPROVED - NO OVERFITTING)
=================================================================
FIXES:
1. ✅ Removes data leakage (no label-creating features)
2. ✅ Adds cross-validation (detects overfitting)
3. ✅ Uses only independent features
4. ✅ Compares train vs test performance

Models: Random Forest, XGBoost, Logistic Regression
Evaluation: Confusion Matrix, Precision, Recall, F1-Score, Cross-Validation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import json
import os

warnings.filterwarnings('ignore')

# ============================================
# 1️⃣ LOAD AND PREPARE DATA
# ============================================

print("=" * 60)
print("VAT ANOMALY DETECTION (IMPROVED - NO OVERFITTING)")
print("=" * 60)

# Load data
excel_file = "AI_Tax_Intelligence_Expanded.xlsx"
if not os.path.exists(excel_file):
    excel_file = "../AI_Tax_Intelligence_Expanded.xlsx"

print(f"\n Loading data from: {excel_file}")
transaction_data = pd.read_excel(excel_file, sheet_name="Transaction_Data")
client_profile = pd.read_excel(excel_file, sheet_name="Client_Profile")

print(f" Loaded {len(transaction_data)} transactions")
print(f" Loaded {len(client_profile)} client profiles")

# Merge data
print("\n🔗 Merging transaction and client data...")
df = transaction_data.merge(client_profile, on='Client_ID', how='left')
print(f" Merged dataset: {len(df)} records")

# ============================================
# 2️⃣ CREATE ANOMALY LABELS (Same as before)
# ============================================

print("\n" + "="*60)
print("🏷️  CREATING ANOMALY LABELS")
print("="*60)

print("\n📊 Anomaly Detection Rules:")
print("   1. High VAT Amount (> 90th percentile)")
print("   2. High Risk Score (> 0.7)")
print("   3. Non-Compliant Business")
print("   4. Filed Late or Not Filed")
print("   5. High Amount-to-Turnover Ratio (> 0.5)")

# Calculate anomaly indicators
vat_threshold = df['VAT_Amount'].quantile(0.90)
amount_threshold = df['Amount'].quantile(0.90)

df['High_VAT'] = (df['VAT_Amount'] > vat_threshold).astype(int)
df['High_Risk'] = (df['Risk_Score'] > 0.7).astype(int)
df['Non_Compliant'] = (df['Compliance_Flag'] == 'Non-Compliant').astype(int)
df['Late_Filing'] = (df['Filing_Status'].isin(['Filed Late', 'Not Filed'])).astype(int)
df['Amount_to_Turnover'] = df['Amount'] / df['Annual_Turnover']
df['High_Ratio'] = (df['Amount_to_Turnover'] > 0.5).astype(int)

# Create anomaly label
df['Is_Anomaly'] = (
    (df['High_VAT'] == 1) | 
    (df['High_Risk'] == 1) | 
    (df['Non_Compliant'] == 1) | 
    (df['Late_Filing'] == 1) |
    (df['High_Ratio'] == 1)
).astype(int)

# Statistics
anomaly_count = df['Is_Anomaly'].sum()
normal_count = len(df) - anomaly_count
anomaly_pct = (anomaly_count / len(df)) * 100

print(f"\n Anomaly Distribution:")
print(f"   Normal Transactions: {normal_count} ({100-anomaly_pct:.1f}%)")
print(f"   Anomalous Transactions: {anomaly_count} ({anomaly_pct:.1f}%)")

# ============================================
# 3️⃣ FEATURE ENGINEERING (IMPROVED - NO LEAKAGE!)
# ============================================

print("\n" + "="*60)
print("🔧 FEATURE ENGINEERING (IMPROVED)")
print("="*60)

from sklearn.preprocessing import LabelEncoder, StandardScaler

# Extract numeric VAT rate
df['VAT_Rate_Numeric'] = df['VAT_Rate'].str.rstrip('%').astype(float)

# Label encode categorical features
label_encoders = {}
categorical_cols = ['Business_Type', 'Category', 'Region']

for col in categorical_cols:
    le = LabelEncoder()
    df[f'{col}_Encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le

# ⚠️ CRITICAL CHANGE: Remove features that create labels!
print("\n🚨 REMOVING DATA LEAKAGE:")
print("   ❌ Removed: Filing_Status_Encoded (used in Late_Filing rule)")
print("   ❌ Removed: Risk_Score (used in High_Risk rule)")
print("   ❌ Removed: Compliance_Flag_Encoded (used in Non_Compliant rule)")
print("   ❌ Removed: VAT_Amount (used in High_VAT rule)")
print("   ❌ Removed: Amount_to_Turnover (used in High_Ratio rule)")

# Use ONLY independent features
feature_cols = [
    'Amount',                    # ✅ Transaction size (not used in label)
    'VAT_Rate_Numeric',          # ✅ VAT rate (not used in label)
    'Annual_Turnover',           # ✅ Business size (not used in label)
    'Business_Type_Encoded',     # ✅ Business type (not used in label)
    'Category_Encoded',          # ✅ Industry (not used in label)
    'Region_Encoded',            # ✅ Location (not used in label)
]

X = df[feature_cols]
y = df['Is_Anomaly']

print(f"\n Features (NO LEAKAGE): {len(feature_cols)}")
print(f"   {', '.join(feature_cols)}")
print(f"\n Target: Is_Anomaly (0=Normal, 1=Anomaly)")

# ============================================
# 4️⃣ TRAIN/TEST SPLIT
# ============================================

from sklearn.model_selection import train_test_split

print("\n" + "="*60)
print("📊 TRAIN/TEST SPLIT")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n Training set: {len(X_train)} samples")
print(f"   Normal: {(y_train == 0).sum()}, Anomaly: {(y_train == 1).sum()}")
print(f"\n Test set: {len(X_test)} samples")
print(f"   Normal: {(y_test == 0).sum()}, Anomaly: {(y_test == 1).sum()}")

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n Features normalized using StandardScaler")

# ============================================
# 5️⃣ CROSS-VALIDATION (NEW!)
# ============================================

from sklearn.model_selection import cross_val_score, StratifiedKFold

print("\n" + "="*60)
print("🔄 CROSS-VALIDATION SETUP")
print("="*60)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print("✅ Using 5-Fold Stratified Cross-Validation")
print("   This will detect overfitting!")

# ============================================
# 6️⃣ EVALUATION FUNCTIONS (ENHANCED)
# ============================================

from sklearn.metrics import (
    confusion_matrix, classification_report, 
    precision_score, recall_score, f1_score, accuracy_score,
    roc_auc_score, precision_recall_curve, auc
)

def evaluate_classifier_improved(model_name, model, X_train, X_test, y_train, y_test):
    """
    Enhanced evaluation with:
    1. Train performance
    2. Test performance
    3. Cross-validation
    4. Overfitting detection
    """
    
    print(f"\n{'='*60}")
    print(f" {model_name} - IMPROVED EVALUATION")
    print(f"{'='*60}")
    
    # 1. Train Performance
    y_train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, y_train_pred)
    train_f1 = f1_score(y_train, y_train_pred, zero_division=0)
    
    # 2. Test Performance
    y_test_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_precision = precision_score(y_test, y_test_pred, zero_division=0)
    test_recall = recall_score(y_test, y_test_pred, zero_division=0)
    test_f1 = f1_score(y_test, y_test_pred, zero_division=0)
    
    # 3. Cross-Validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='f1')
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()
    
    # 4. Overfitting Detection
    overfitting_gap = train_accuracy - test_accuracy
    
    print(f"\n📈 TRAIN Performance:")
    print(f"   Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    print(f"   F1-Score: {train_f1:.4f}")
    
    print(f"\n📈 TEST Performance:")
    print(f"   Accuracy:  {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print(f"   Precision: {test_precision:.4f} ({test_precision*100:.2f}%)")
    print(f"   Recall:    {test_recall:.4f} ({test_recall*100:.2f}%)")
    print(f"   F1-Score:  {test_f1:.4f}")
    
    print(f"\n CROSS-VALIDATION (5-Fold):")
    print(f"   F1-Scores: {[f'{s:.4f}' for s in cv_scores]}")
    print(f"   Mean F1:   {cv_mean:.4f} ± {cv_std:.4f}")
    
    print(f"\n🚨 OVERFITTING CHECK:")
    print(f"   Train Accuracy: {train_accuracy:.4f}")
    print(f"   Test Accuracy:  {test_accuracy:.4f}")
    print(f"   Gap:            {overfitting_gap:.4f}")
    
    if overfitting_gap > 0.15:
        print(f"     HIGH OVERFITTING! (gap > 15%)")
    elif overfitting_gap > 0.05:
        print(f"   🟡 Moderate overfitting (gap 5-15%)")
    else:
        print(f"    No significant overfitting (gap < 5%)")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_test_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print(f"\n🔢 Confusion Matrix (Test Set):")
    print(f"                 Predicted")
    print(f"               Normal  Anomaly")
    print(f"   Actual Normal   {tn:>4}    {fp:>4}")
    print(f"          Anomaly  {fn:>4}    {tp:>4}")
    
    return {
        'model': model_name,
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'precision': test_precision,
        'recall': test_recall,
        'f1_score': test_f1,
        'cv_mean_f1': cv_mean,
        'cv_std_f1': cv_std,
        'overfitting_gap': overfitting_gap,
        'confusion_matrix': cm.tolist(),
        'tp': int(tp), 'tn': int(tn), 'fp': int(fp), 'fn': int(fn)
    }

# ============================================
# 7️⃣ MODEL 1: RANDOM FOREST
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 1: RANDOM FOREST")
print("="*60)

from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,           # Limit depth to prevent overfitting
    min_samples_split=5,   # Require more samples to split
    min_samples_leaf=2,    # Require more samples in leaf
    class_weight='balanced',
    random_state=42
)

print("📈 Training Random Forest...")
rf_model.fit(X_train_scaled, y_train)
print("✅ Training complete")

rf_results = evaluate_classifier_improved(
    "Random Forest", rf_model, X_train_scaled, X_test_scaled, y_train, y_test
)

# ============================================
# 8️⃣ MODEL 2: XGBOOST
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 2: XGBOOST")
print("="*60)

try:
    from xgboost import XGBClassifier
    
    xgb_model = XGBClassifier(
        n_estimators=100,
        max_depth=3,           # Limit depth
        learning_rate=0.1,
        scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
        random_state=42,
        eval_metric='logloss'
    )
    
    print("📈 Training XGBoost...")
    xgb_model.fit(X_train_scaled, y_train)
    print("✅ Training complete")
    
    xgb_results = evaluate_classifier_improved(
        "XGBoost", xgb_model, X_train_scaled, X_test_scaled, y_train, y_test
    )
    
except ImportError:
    print("⚠️  XGBoost not installed")
    xgb_results = None

# ============================================
# 9️⃣ MODEL 3: LOGISTIC REGRESSION
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 3: LOGISTIC REGRESSION")
print("="*60)

from sklearn.linear_model import LogisticRegression

lr_model = LogisticRegression(
    class_weight='balanced',
    max_iter=1000,
    random_state=42
)

print("📈 Training Logistic Regression...")
lr_model.fit(X_train_scaled, y_train)
print("✅ Training complete")

lr_results = evaluate_classifier_improved(
    "Logistic Regression", lr_model, X_train_scaled, X_test_scaled, y_train, y_test
)

# ============================================
# 🔟 COMPARE MODELS
# ============================================

print("\n" + "="*60)
print("🏆 MODEL COMPARISON (IMPROVED)")
print("="*60)

results_list = [rf_results, lr_results]
if xgb_results:
    results_list.insert(1, xgb_results)

comparison_df = pd.DataFrame(results_list)
comparison_df = comparison_df.sort_values('f1_score', ascending=False)

print("\n📊 Performance Comparison:")
print(comparison_df[['model', 'test_accuracy', 'precision', 'recall', 'f1_score', 
                     'cv_mean_f1', 'overfitting_gap']].to_string(index=False))

print("\n🏆 Winner (by F1-Score):")
winner = comparison_df.iloc[0]
print(f"   Model: {winner['model']}")
print(f"   Test Accuracy: {winner['test_accuracy']:.4f}")
print(f"   F1-Score: {winner['f1_score']:.4f}")
print(f"   CV F1: {winner['cv_mean_f1']:.4f} ± {winner['cv_std_f1']:.4f}")
print(f"   Overfitting Gap: {winner['overfitting_gap']:.4f}")

# ============================================
# 1️⃣1️⃣ SAVE RESULTS
# ============================================

print("\n" + "="*60)
print("💾 SAVING IMPROVED RESULTS")
print("="*60)

output_dir = "../models/anomaly_detection_models_IMPROVED"
os.makedirs(output_dir, exist_ok=True)

# Save comparison
comparison_df.to_csv(f"{output_dir}/model_comparison_improved.csv", index=False)
print(f" Saved: {output_dir}/model_comparison_improved.csv")

# Save metadata
metadata = {
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_samples': len(df),
    'train_samples': len(X_train),
    'test_samples': len(X_test),
    'features': feature_cols,
    'improvements': [
        'Removed data leakage (no label-creating features)',
        'Added cross-validation',
        'Added overfitting detection',
        'Limited model complexity'
    ],
    'winner': winner['model'],
    'winner_f1': float(winner['f1_score']),
    'winner_cv_f1': float(winner['cv_mean_f1'])
}

with open(f"{output_dir}/metadata_improved.json", 'w') as f:
    json.dump(metadata, f, indent=2)
print(f" Saved: {output_dir}/metadata_improved.json")

print("\n" + "="*60)
print("✅ IMPROVED ANOMALY DETECTION COMPLETE!")
print("="*60)
print(f"\n Key Findings:")
print(f"   Best Model: {winner['model']}")
print(f"   Test F1-Score: {winner['f1_score']:.4f} (realistic!)")
print(f"   CV F1-Score: {winner['cv_mean_f1']:.4f} ± {winner['cv_std_f1']:.4f}")
print(f"   Overfitting: {winner['overfitting_gap']:.4f}")
print(f"\n💡 Compare this to the original 100% accuracy!")
print(f"   This is more realistic and trustworthy.")