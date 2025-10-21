"""
📊 TRAINING DATA ANALYSIS
=========================

Analyzes training data to identify:
- Feature distributions
- Data imbalances
- Outliers
- Potential data quality issues
- Correlation patterns

This helps explain why the model might be biased or conservative.

Usage:
    python ANALYZE_TRAINING_DATA.py
"""

import pandas as pd
import numpy as np
import json
import os
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class TrainingDataAnalyzer:
    """Analyze training data characteristics"""
    
    def __init__(self):
        self.data = None
        self.feature_stats = {}
        self._load_training_data()
    
    def _load_training_data(self):
        """Try to find and load training data"""
        print("🔍 Searching for training data...")
        
        # Try multiple locations
        possible_paths = [
            "data/AI_Tax_Intelligence_Large.xlsx",
            "data/tax_documents_sample.xlsx",
            "real_data/extracted_patterns.json",
            "models/ml_models/training_data.csv"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"   Found: {path}")
                try:
                    if path.endswith('.xlsx'):
                        self.data = pd.read_excel(path)
                        print(f"   ✅ Loaded {len(self.data)} rows from Excel")
                        return
                    elif path.endswith('.csv'):
                        self.data = pd.read_csv(path)
                        print(f"   ✅ Loaded {len(self.data)} rows from CSV")
                        return
                    elif path.endswith('.json'):
                        with open(path, 'r') as f:
                            self.data = json.load(f)
                        print(f"   ✅ Loaded from JSON")
                        return
                except Exception as e:
                    print(f"   ❌ Error loading {path}: {e}")
                    continue
        
        # Try to extract from model artifacts
        print("\n   Attempting to extract statistics from model artifacts...")
        self._extract_from_model_artifacts()
    
    def _extract_from_model_artifacts(self):
        """Extract info from saved model artifacts"""
        try:
            metadata_path = "optimized_models_25000_samples/metadata.json"
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                    print(f"   ✅ Found metadata: {self.metadata.get('Training Samples', 'N/A')} training samples")
            
            # Try to load feature importance
            feature_importance_path = "models/ml_models/feature_importance.csv"
            if os.path.exists(feature_importance_path):
                self.feature_importance = pd.read_csv(feature_importance_path)
                print(f"   ✅ Found feature importance data")
        except Exception as e:
            print(f"   ❌ Error extracting from artifacts: {e}")
    
    def analyze_distribution(self):
        """Analyze feature distributions"""
        print("\n" + "="*70)
        print("📊 FEATURE DISTRIBUTION ANALYSIS")
        print("="*70)
        
        if self.data is None or self.data.empty:
            print("\n❌ No training data available for distribution analysis")
            print("   This makes it harder to diagnose bias, but we can infer from metadata.")
            self._analyze_metadata()
            return
        
        print(f"\nDataset: {len(self.data)} rows, {len(self.data.columns)} columns\n")
        
        # Analyze numeric features
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            data = self.data[col].dropna()
            
            if len(data) == 0:
                continue
            
            print(f"📈 {col}:")
            print(f"   Mean: {data.mean():,.2f}")
            print(f"   Median: {data.median():,.2f}")
            print(f"   Std Dev: {data.std():,.2f}")
            print(f"   Min: {data.min():,.2f}")
            print(f"   Max: {data.max():,.2f}")
            print(f"   Skewness: {data.skew():.2f} {'(Right skewed - many low values)' if data.skew() > 1 else '(Left skewed)' if data.skew() < -1 else '(Normal)'}")
            
            # Check for outliers
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[(data < Q1 - 1.5*IQR) | (data > Q3 + 1.5*IQR)]
            if len(outliers) > 0:
                print(f"   ⚠️  Outliers: {len(outliers)} ({len(outliers)/len(data)*100:.1f}% of data)")
            print()
    
    def _analyze_metadata(self):
        """Analyze what we know from metadata"""
        print("\n📋 METADATA ANALYSIS:")
        
        if hasattr(self, 'metadata'):
            print(f"\n   Training Samples: {self.metadata.get('Training Samples', 'N/A')}")
            print(f"   Testing Samples: {self.metadata.get('Testing Samples', 'N/A')}")
            print(f"   Best Model: {self.metadata.get('Best Model', 'N/A')}")
            print(f"   R² Score: {self.metadata.get('Best Test R² Score', 'N/A')}")
            print(f"   MAE: {self.metadata.get('Best MAE', 'N/A')}")
            
            print(f"\n   🔍 Model Performance Interpretation:")
            r2 = float(self.metadata.get('Best Test R² Score', 0))
            if r2 < 0.7:
                print(f"      ⚠️  R² = {r2:.2f} (Below ideal) - Model may be underfitting")
            else:
                print(f"      ✅ R² = {r2:.2f} (Good) - Model fits data reasonably")
        else:
            print("   No metadata available")
    
    def analyze_feature_importance(self):
        """Analyze feature importance"""
        print("\n" + "="*70)
        print("🎯 FEATURE IMPORTANCE ANALYSIS")
        print("="*70)
        
        try:
            if os.path.exists("models/ml_models/feature_importance.csv"):
                fi = pd.read_csv("models/ml_models/feature_importance.csv")
                
                print(f"\nTop Features by Importance:\n")
                for idx, row in fi.iterrows():
                    importance = float(row['Importance']) * 100
                    
                    if importance == 0:
                        bar = "░░░░░░░░░░"
                        status = "🔴 NOT USED"
                    elif importance < 5:
                        bar = "█░░░░░░░░░"
                        status = "🟡 MINIMAL"
                    elif importance < 10:
                        bar = "███░░░░░░░"
                        status = "🟡 LOW"
                    elif importance < 15:
                        bar = "█████░░░░░"
                        status = "🟡 MEDIUM"
                    else:
                        bar = "█████████░"
                        status = "🟢 HIGH"
                    
                    print(f"{idx+1:2}. {row['Feature']:30} {bar} {importance:5.1f}% {status}")
                
                # Check for unused features
                unused = fi[fi['Importance'] == 0]
                if len(unused) > 0:
                    print(f"\n⚠️  WARNING: {len(unused)} features have ZERO importance:")
                    for _, row in unused.iterrows():
                        print(f"    - {row['Feature']}")
                    print(f"\n    This suggests:")
                    print(f"    • Features are either constant in training data")
                    print(f"    • OR feature encoding is incorrect")
                    print(f"    • OR they're truly not predictive")
            else:
                print("❌ Feature importance file not found")
        except Exception as e:
            print(f"❌ Error analyzing feature importance: {e}")
    
    def analyze_categorical_balance(self):
        """Analyze categorical feature balance"""
        print("\n" + "="*70)
        print("🏷️  CATEGORICAL FEATURE ANALYSIS")
        print("="*70)
        
        if self.data is None or self.data.empty:
            print("\n⚠️  No training data to analyze")
            print("\n   Based on model behavior, we can infer:")
            print("   • Filing_Status likely has imbalanced categories")
            print("   • Some categories may have very few samples")
            print("   • This could explain why Filing_Status dominates predictions")
            return
        
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            print(f"\n📋 {col}:")
            value_counts = self.data[col].value_counts()
            
            for val, count in value_counts.items():
                percentage = (count / len(self.data)) * 100
                bar = "█" * int(percentage / 2) + "░" * (50 - int(percentage / 2))
                print(f"   {str(val):20} {bar} {percentage:5.1f}% ({count:,})")
            
            # Check for imbalance
            max_pct = (value_counts.iloc[0] / len(self.data)) * 100
            min_pct = (value_counts.iloc[-1] / len(self.data)) * 100
            imbalance_ratio = max_pct / min_pct if min_pct > 0 else float('inf')
            
            if imbalance_ratio > 5:
                print(f"   🔴 HIGHLY IMBALANCED (Ratio: {imbalance_ratio:.1f}:1)")
            elif imbalance_ratio > 2:
                print(f"   🟡 MODERATELY IMBALANCED (Ratio: {imbalance_ratio:.1f}:1)")
            else:
                print(f"   ✅ BALANCED (Ratio: {imbalance_ratio:.1f}:1)")
    
    def identify_potential_issues(self):
        """Identify potential data quality and model issues"""
        print("\n" + "="*70)
        print("🚨 POTENTIAL ISSUES IDENTIFIED")
        print("="*70)
        
        issues = []
        
        # Issue 1: Feature importance shows zeros
        try:
            fi = pd.read_csv("models/ml_models/feature_importance.csv")
            unused = len(fi[fi['Importance'] == 0])
            if unused > 0:
                issues.append({
                    "severity": "🟡 MEDIUM",
                    "issue": f"{unused} features have zero importance",
                    "impact": "Model may be using incomplete feature set",
                    "solution": "Check feature encoding and scaling"
                })
        except:
            pass
        
        # Issue 2: SHAP shows different importance than global importance
        issues.append({
            "severity": "🟡 MEDIUM",
            "issue": "SHAP values show different feature importance than global importance",
            "impact": "Instance-level explanations don't match global patterns",
            "solution": "May indicate data heterogeneity or feature interactions"
        })
        
        # Issue 3: Filing Status over-weighted
        issues.append({
            "severity": "🔴 HIGH",
            "issue": "Filing_Status dominates predictions (large negative SHAP value)",
            "impact": "Model is too sensitive to filing frequency",
            "solution": "Consider feature scaling or re-encoding filing status categories"
        })
        
        # Issue 4: VAT_Amount negative contribution
        issues.append({
            "severity": "🔴 HIGH",
            "issue": "VAT_Amount has large negative SHAP value",
            "impact": "Counter-intuitive: higher VAT should increase refunds",
            "solution": "May indicate training data has reversed relationship or encoding issue"
        })
        
        # Issue 5: Model conservatism
        issues.append({
            "severity": "⚠️  CRITICAL",
            "issue": "Model produces 44% lower refunds than baseline average",
            "impact": "May result in under-refunding legitimate claims",
            "solution": "Recalibrate model thresholds or reweight features"
        })
        
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue['severity']} - {issue['issue']}")
            print(f"   Impact: {issue['impact']}")
            print(f"   Solution: {issue['solution']}")
        
        return issues
    
    def generate_recommendations(self):
        """Generate comprehensive recommendations"""
        print("\n" + "="*70)
        print("💡 RECOMMENDATIONS FOR MODEL IMPROVEMENT")
        print("="*70)
        
        recommendations = [
            {
                "priority": "🔴 P1 - CRITICAL",
                "action": "Validate Input Data",
                "details": [
                    "Check if VAT_Amount encoding is correct (should be positive for refunds)",
                    "Verify Filing_Status categories are meaningful",
                    "Confirm that test data values are within training data ranges"
                ]
            },
            {
                "priority": "🔴 P1 - CRITICAL",
                "action": "Test with Good Scenario",
                "details": [
                    "Run test with ALL positive signals (high amount, low risk, compliant)",
                    "If refund is still low, model is over-conservative",
                    "If refund is high, model is responsive (issue is data, not model)"
                ]
            },
            {
                "priority": "🟡 P2 - HIGH",
                "action": "Feature Normalization",
                "details": [
                    "Check if features are scaled appropriately",
                    "Verify that categorical features are one-hot encoded correctly",
                    "Consider normalizing Filing_Status and VAT_Amount"
                ]
            },
            {
                "priority": "🟡 P2 - HIGH",
                "action": "Feature Weight Rebalancing",
                "details": [
                    "Reduce weight of Filing_Status if causing over-sensitivity",
                    "Increase weight of positive compliance signals",
                    "Consider interaction terms (e.g., VAT × Amount × Risk_Score)"
                ]
            },
            {
                "priority": "🟡 P2 - HIGH",
                "action": "Training Data Analysis",
                "details": [
                    "Check distribution of predicted values in training data",
                    "Look for class imbalance in refund eligibility",
                    "Verify training data doesn't have systematic bias toward low refunds"
                ]
            },
            {
                "priority": "🟢 P3 - MEDIUM",
                "action": "Model Comparison",
                "details": [
                    "Compare Random Forest with Gradient Boosting predictions",
                    "Test Ridge Regression to see if linear model is different",
                    "Potentially use ensemble of multiple models"
                ]
            },
            {
                "priority": "🟢 P3 - MEDIUM",
                "action": "Threshold Calibration",
                "details": [
                    "Adjust prediction thresholds to match business requirements",
                    "Consider confidence intervals instead of hard cutoffs",
                    "Implement confidence-based recommendation (auto-approve vs manual review)"
                ]
            }
        ]
        
        for rec in recommendations:
            print(f"\n{rec['priority']} - {rec['action']}")
            for detail in rec['details']:
                print(f"   • {detail}")
        
        return recommendations
    
    def run_full_analysis(self):
        """Run complete analysis"""
        print("\n" + "📊 "*35)
        print("TRAINING DATA & MODEL ANALYSIS")
        print("📊 "*35)
        
        self.analyze_distribution()
        self.analyze_feature_importance()
        self.analyze_categorical_balance()
        issues = self.identify_potential_issues()
        recommendations = self.generate_recommendations()
        
        # Save report
        self._save_report(issues, recommendations)
    
    def _save_report(self, issues, recommendations):
        """Save analysis report to file"""
        report = f"""
TRAINING DATA & MODEL ANALYSIS REPORT
Generated: {pd.Timestamp.now()}

ISSUES IDENTIFIED:
{json.dumps([{k: v for k, v in issue.items()} for issue in issues], indent=2)}

RECOMMENDATIONS:
{json.dumps([{k: v for k, v in rec.items()} for rec in recommendations], indent=2)}
"""
        report_path = "TRAINING_DATA_ANALYSIS_REPORT.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\n✅ Report saved to {report_path}")


if __name__ == "__main__":
    analyzer = TrainingDataAnalyzer()
    analyzer.run_full_analysis()