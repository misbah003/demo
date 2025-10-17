"""
🚨 VAT Transaction Anomaly Detection (Classification)
======================================================
Detects anomalous transactions using:
- Random Forest Classifier
- XGBoost Classifier
- Logistic Regression

Evaluation Metrics: Confusion Matrix, Precision, Recall, F1-Score
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
print("🚨 VAT TRANSACTION ANOMALY DETECTION")
print("=" * 60)

# Load data
excel_file = "AI_Tax_Intelligence_Expanded.xlsx"
if not os.path.exists(excel_file):
    excel_file = "../AI_Tax_Intelligence_Expanded.xlsx"

print(f"\n📂 Loading data from: {excel_file}")
transaction_data = pd.read_excel(excel_file, sheet_name="Transaction_Data")
client_profile = pd.read_excel(excel_file, sheet_name="Client_Profile")

print(f"✅ Loaded {len(transaction_data)} transactions")
print(f"✅ Loaded {len(client_profile)} client profiles")

# Merge data
print("\n🔗 Merging transaction and client data...")
df = transaction_data.merge(client_profile, on='Client_ID', how='left')
print(f"✅ Merged dataset: {len(df)} records")

# ============================================
# 2️⃣ CREATE ANOMALY LABELS
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

# Create anomaly label (if ANY condition is met)
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

print(f"\n📊 Anomaly Distribution:")
print(f"   Normal Transactions: {normal_count} ({100-anomaly_pct:.1f}%)")
print(f"   Anomalous Transactions: {anomaly_count} ({anomaly_pct:.1f}%)")

print(f"\n📊 Anomaly Breakdown:")
print(f"   High VAT Amount: {df['High_VAT'].sum()}")
print(f"   High Risk Score: {df['High_Risk'].sum()}")
print(f"   Non-Compliant: {df['Non_Compliant'].sum()}")
print(f"   Late/Not Filed: {df['Late_Filing'].sum()}")
print(f"   High Amount Ratio: {df['High_Ratio'].sum()}")

# ============================================
# 3️⃣ FEATURE ENGINEERING
# ============================================

print("\n" + "="*60)
print("🔧 FEATURE ENGINEERING")
print("="*60)

from sklearn.preprocessing import LabelEncoder, StandardScaler

# Extract numeric VAT rate
df['VAT_Rate_Numeric'] = df['VAT_Rate'].str.rstrip('%').astype(float)

# Label encode categorical features
label_encoders = {}
categorical_cols = ['Business_Type', 'Category', 'Filing_Status', 'Region', 'Compliance_Flag']

for col in categorical_cols:
    le = LabelEncoder()
    df[f'{col}_Encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le

# Select features for modeling
feature_cols = [
    'Amount', 'VAT_Rate_Numeric', 'VAT_Amount', 'Annual_Turnover', 'Risk_Score',
    'Business_Type_Encoded', 'Category_Encoded', 'Filing_Status_Encoded', 
    'Region_Encoded', 'Compliance_Flag_Encoded', 'Amount_to_Turnover'
]

X = df[feature_cols]
y = df['Is_Anomaly']

print(f"\n✅ Features: {len(feature_cols)}")
print(f"   {', '.join(feature_cols)}")
print(f"\n✅ Target: Is_Anomaly (0=Normal, 1=Anomaly)")

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

print(f"\n✅ Training set: {len(X_train)} samples")
print(f"   Normal: {(y_train == 0).sum()}, Anomaly: {(y_train == 1).sum()}")
print(f"\n✅ Test set: {len(X_test)} samples")
print(f"   Normal: {(y_test == 0).sum()}, Anomaly: {(y_test == 1).sum()}")

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n✅ Features normalized using StandardScaler")

# ============================================
# 5️⃣ EVALUATION FUNCTIONS
# ============================================

from sklearn.metrics import (
    confusion_matrix, classification_report, 
    precision_score, recall_score, f1_score, accuracy_score,
    roc_auc_score, precision_recall_curve, auc
)

def evaluate_classifier(model_name, y_true, y_pred, y_pred_proba=None):
    """Comprehensive evaluation with confusion matrix and metrics"""
    
    print(f"\n{'='*60}")
    print(f"📊 {model_name} - Evaluation Results")
    print(f"{'='*60}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print(f"\n🔢 Confusion Matrix:")
    print(f"                 Predicted")
    print(f"               Normal  Anomaly")
    print(f"   Actual Normal   {tn:>4}    {fp:>4}")
    print(f"          Anomaly  {fn:>4}    {tp:>4}")
    
    # Metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    print(f"\n📈 Classification Metrics:")
    print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"   Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"   F1-Score:  {f1:.4f}")
    
    # ROC-AUC if probabilities available
    if y_pred_proba is not None:
        try:
            roc_auc = roc_auc_score(y_true, y_pred_proba)
            print(f"   ROC-AUC:   {roc_auc:.4f}")
        except:
            roc_auc = None
    else:
        roc_auc = None
    
    # Precision-Recall AUC
    if y_pred_proba is not None:
        try:
            precision_curve, recall_curve, _ = precision_recall_curve(y_true, y_pred_proba)
            pr_auc = auc(recall_curve, precision_curve)
            print(f"   PR-AUC:    {pr_auc:.4f}")
        except:
            pr_auc = None
    else:
        pr_auc = None
    
    print(f"\n📊 Detailed Classification Report:")
    print(classification_report(y_true, y_pred, 
                                target_names=['Normal', 'Anomaly'],
                                zero_division=0))
    
    print(f"{'='*60}")
    
    return {
        'model': model_name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'pr_auc': pr_auc,
        'confusion_matrix': cm.tolist(),
        'tp': int(tp), 'tn': int(tn), 'fp': int(fp), 'fn': int(fn)
    }

# ============================================
# 6️⃣ MODEL 1: RANDOM FOREST CLASSIFIER
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 1: Random Forest Classifier")
print("="*60)

from sklearn.ensemble import RandomForestClassifier

print("📈 Training Random Forest...")
print("   Parameters: n_estimators=100, max_depth=10, random_state=42")

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'  # Handle class imbalance
)

rf_model.fit(X_train_scaled, y_train)
rf_pred = rf_model.predict(X_test_scaled)
rf_pred_proba = rf_model.predict_proba(X_test_scaled)[:, 1]

rf_results = evaluate_classifier("Random Forest", y_test, rf_pred, rf_pred_proba)

print("✅ Random Forest trained successfully")

# Feature importance
rf_feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\n🔍 Top 5 Important Features:")
for idx, row in rf_feature_importance.head(5).iterrows():
    print(f"   {row['Feature']:<30} {row['Importance']:.4f}")

# ============================================
# 7️⃣ MODEL 2: XGBOOST CLASSIFIER
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 2: XGBoost Classifier")
print("="*60)

try:
    import xgboost as xgb
    
    print("📈 Training XGBoost...")
    print("   Parameters: n_estimators=100, max_depth=6, learning_rate=0.1")
    
    # Calculate scale_pos_weight for imbalanced data
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        scale_pos_weight=scale_pos_weight,
        eval_metric='logloss'
    )
    
    xgb_model.fit(X_train_scaled, y_train)
    xgb_pred = xgb_model.predict(X_test_scaled)
    xgb_pred_proba = xgb_model.predict_proba(X_test_scaled)[:, 1]
    
    xgb_results = evaluate_classifier("XGBoost", y_test, xgb_pred, xgb_pred_proba)
    
    print("✅ XGBoost trained successfully")
    
except ImportError:
    print("⚠️  XGBoost not installed. Installing...")
    print("   Run: pip install xgboost")
    xgb_results = None
except Exception as e:
    print(f"❌ XGBoost failed: {str(e)}")
    xgb_results = None

# ============================================
# 8️⃣ MODEL 3: LOGISTIC REGRESSION
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 3: Logistic Regression")
print("="*60)

from sklearn.linear_model import LogisticRegression

print("📈 Training Logistic Regression...")
print("   Parameters: max_iter=1000, class_weight='balanced'")

lr_model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight='balanced'
)

lr_model.fit(X_train_scaled, y_train)
lr_pred = lr_model.predict(X_test_scaled)
lr_pred_proba = lr_model.predict_proba(X_test_scaled)[:, 1]

lr_results = evaluate_classifier("Logistic Regression", y_test, lr_pred, lr_pred_proba)

print("✅ Logistic Regression trained successfully")

# ============================================
# 9️⃣ COMPARE ALL MODELS
# ============================================

print("\n" + "="*60)
print("🏆 MODEL COMPARISON - ANOMALY DETECTION")
print("="*60)

# Collect all results
all_results = [rf_results]
if xgb_results:
    all_results.append(xgb_results)
all_results.append(lr_results)

results_df = pd.DataFrame(all_results)

# Sort by F1-Score (best metric for imbalanced data)
results_df = results_df.sort_values('f1_score', ascending=False)

print("\n📊 Performance Ranking (by F1-Score):")
print(f"\n{'Rank':<6} {'Model':<20} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10}")
print("-" * 70)

for idx, row in results_df.iterrows():
    rank = "🥇" if idx == results_df.index[0] else "🥈" if idx == results_df.index[1] else "🥉"
    print(f"{rank:<6} {row['model']:<20} {row['accuracy']:>8.4f}  {row['precision']:>8.4f}  {row['recall']:>8.4f}  {row['f1_score']:>8.4f}")

# Select best model
best_model = results_df.iloc[0]
print(f"\n🏆 WINNER: {best_model['model']}")
print(f"   Accuracy:  {best_model['accuracy']:.4f}")
print(f"   Precision: {best_model['precision']:.4f}")
print(f"   Recall:    {best_model['recall']:.4f}")
print(f"   F1-Score:  {best_model['f1_score']:.4f}")

# ============================================
# 🔟 SAVE RESULTS
# ============================================

print("\n" + "="*60)
print("💾 SAVING RESULTS")
print("="*60)

os.makedirs('../models/anomaly_detection_models', exist_ok=True)

# Save comparison
results_df.to_csv('../models/anomaly_detection_models/model_comparison.csv', index=False)
print("✅ Model comparison saved to: ../models/anomaly_detection_models/model_comparison.csv")

# Save feature importance
rf_feature_importance.to_csv('../models/anomaly_detection_models/feature_importance.csv', index=False)
print("✅ Feature importance saved to: ../models/anomaly_detection_models/feature_importance.csv")

# Save metadata
metadata = {
    'training_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'total_samples': len(df),
    'train_samples': len(X_train),
    'test_samples': len(X_test),
    'anomaly_rate': float(anomaly_pct),
    'features': feature_cols,
    'best_model': best_model['model'],
    'best_f1_score': float(best_model['f1_score']),
    'best_precision': float(best_model['precision']),
    'best_recall': float(best_model['recall'])
}

with open('../models/anomaly_detection_models/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)

print("✅ Metadata saved to: ../models/anomaly_detection_models/metadata.json")

# Save best model
import pickle

if best_model['model'] == 'Random Forest':
    best_model_obj = rf_model
elif best_model['model'] == 'XGBoost':
    best_model_obj = xgb_model
else:
    best_model_obj = lr_model

with open('../models/anomaly_detection_models/best_model.pkl', 'wb') as f:
    pickle.dump(best_model_obj, f)

with open('../models/anomaly_detection_models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('../models/anomaly_detection_models/label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

print("✅ Best model saved to: ../models/anomaly_detection_models/best_model.pkl")

# ============================================
# 1️⃣1️⃣ VISUALIZATIONS
# ============================================

print("\n" + "="*60)
print("📊 GENERATING VISUALIZATIONS")
print("="*60)

# 1. Confusion Matrix Heatmap
fig, axes = plt.subplots(1, len(all_results), figsize=(6*len(all_results), 5))

if len(all_results) == 1:
    axes = [axes]

for idx, result in enumerate(all_results):
    cm = np.array(result['confusion_matrix'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Normal', 'Anomaly'],
                yticklabels=['Normal', 'Anomaly'],
                ax=axes[idx])
    axes[idx].set_title(f"{result['model']}\nF1-Score: {result['f1_score']:.4f}", 
                       fontweight='bold')
    axes[idx].set_ylabel('Actual')
    axes[idx].set_xlabel('Predicted')

plt.tight_layout()
plt.savefig('../models/anomaly_detection_models/confusion_matrices.png', dpi=300, bbox_inches='tight')
print("✅ Confusion matrices saved to: ../models/anomaly_detection_models/confusion_matrices.png")

# 2. Metrics Comparison
fig, ax = plt.subplots(figsize=(12, 6))

metrics = ['accuracy', 'precision', 'recall', 'f1_score']
x = np.arange(len(results_df))
width = 0.2

for i, metric in enumerate(metrics):
    values = results_df[metric].values
    ax.bar(x + i*width, values, width, label=metric.capitalize())

ax.set_xlabel('Model', fontsize=12)
ax.set_ylabel('Score', fontsize=12)
ax.set_title('Anomaly Detection - Model Performance Comparison', fontsize=14, fontweight='bold')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(results_df['model'].values)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 1.1)

plt.tight_layout()
plt.savefig('../models/anomaly_detection_models/metrics_comparison.png', dpi=300, bbox_inches='tight')
print("✅ Metrics comparison saved to: ../models/anomaly_detection_models/metrics_comparison.png")

# 3. Feature Importance
fig, ax = plt.subplots(figsize=(10, 6))

top_features = rf_feature_importance.head(10)
ax.barh(range(len(top_features)), top_features['Importance'].values)
ax.set_yticks(range(len(top_features)))
ax.set_yticklabels(top_features['Feature'].values)
ax.set_xlabel('Importance', fontsize=12)
ax.set_title('Top 10 Features for Anomaly Detection (Random Forest)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('../models/anomaly_detection_models/feature_importance.png', dpi=300, bbox_inches='tight')
print("✅ Feature importance saved to: ../models/anomaly_detection_models/feature_importance.png")

print("\n" + "="*60)
print("✅ ANOMALY DETECTION CLASSIFICATION COMPLETE!")
print("="*60)
print("\n📁 Output Files:")
print("   1. ../models/anomaly_detection_models/model_comparison.csv")
print("   2. ../models/anomaly_detection_models/feature_importance.csv")
print("   3. ../models/anomaly_detection_models/metadata.json")
print("   4. ../models/anomaly_detection_models/best_model.pkl")
print("   5. ../models/anomaly_detection_models/confusion_matrices.png")
print("   6. ../models/anomaly_detection_models/metrics_comparison.png")
print("   7. ../models/anomaly_detection_models/feature_importance.png")
print("\n🎉 Both ML systems complete!")
print("="*60)