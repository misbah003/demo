"""
COMPLETE ML TRAINING PIPELINE
Trains all missing models:
1. Document Classification (CNN)
2. Sentiment Analysis
3. Improved Time Series (LSTM)
4. Enhanced Anomaly Detection
"""

import sys
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("🚀 COMPLETE ML TRAINING PIPELINE")
print("=" * 80)
print()
print("This script will train ALL missing ML models:")
print("  1. ✅ Document Classification (CNN + Hybrid)")
print("  2. ✅ Sentiment Analysis (Logistic Regression + Random Forest)")
print("  3. ✅ Time Series Forecasting (LSTM + Prophet)")
print("  4. ✅ Anomaly Detection (XGBoost + Isolation Forest)")
print()
print("=" * 80)
print()

# Track training status
training_results = {
    'document_classification': {'status': 'pending', 'accuracy': None},
    'sentiment_analysis': {'status': 'pending', 'accuracy': None},
    'time_series': {'status': 'pending', 'rmse': None},
    'anomaly_detection': {'status': 'pending', 'f1_score': None}
}


# ============================================================================
# STEP 1: Document Classification
# ============================================================================
print("\n" + "=" * 80)
print("STEP 1/4: DOCUMENT CLASSIFICATION")
print("=" * 80)
print()

try:
    print("📚 Training CNN and Hybrid models for document classification...")
    print()
    
    from train_document_classifier import main as train_doc_classifier
    train_doc_classifier()
    
    training_results['document_classification']['status'] = 'success'
    
    # Load metadata to get accuracy
    import json
    metadata_path = Path(__file__).parent.parent / "models" / "document_classifier" / "metadata.json"
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            training_results['document_classification']['accuracy'] = metadata['models']['cnn']['accuracy']
    
    print("\n✅ Document Classification: SUCCESS")
    
except Exception as e:
    print(f"\n❌ Document Classification: FAILED - {e}")
    training_results['document_classification']['status'] = 'failed'
    training_results['document_classification']['error'] = str(e)


# ============================================================================
# STEP 2: Sentiment Analysis
# ============================================================================
print("\n" + "=" * 80)
print("STEP 2/4: SENTIMENT ANALYSIS")
print("=" * 80)
print()

try:
    print("😊 Training sentiment analysis models...")
    print()
    
    from sentiment_analysis import main as train_sentiment
    train_sentiment()
    
    training_results['sentiment_analysis']['status'] = 'success'
    
    # Load metadata to get accuracy
    import json
    metadata_path = Path(__file__).parent.parent / "models" / "sentiment_analysis" / "metadata.json"
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            # Accuracy will be in the saved metrics
    
    print("\n✅ Sentiment Analysis: SUCCESS")
    
except Exception as e:
    print(f"\n❌ Sentiment Analysis: FAILED - {e}")
    training_results['sentiment_analysis']['status'] = 'failed'
    training_results['sentiment_analysis']['error'] = str(e)


# ============================================================================
# STEP 3: Time Series Forecasting (IMPROVED)
# ============================================================================
print("\n" + "=" * 80)
print("STEP 3/4: TIME SERIES FORECASTING")
print("=" * 80)
print()

try:
    print("📈 Training LSTM and Prophet models for time series...")
    print()
    
    # Check if improved time series script exists
    improved_ts_path = Path(__file__).parent / "time_series_forecasting_IMPROVED.py"
    
    if improved_ts_path.exists():
        import subprocess
        result = subprocess.run(
            [sys.executable, str(improved_ts_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            training_results['time_series']['status'] = 'success'
            print("\n✅ Time Series Forecasting: SUCCESS")
        else:
            raise Exception(result.stderr)
    else:
        print("⚠️ Improved time series script not found, using existing models")
        training_results['time_series']['status'] = 'skipped'
    
except Exception as e:
    print(f"\n❌ Time Series Forecasting: FAILED - {e}")
    training_results['time_series']['status'] = 'failed'
    training_results['time_series']['error'] = str(e)


# ============================================================================
# STEP 4: Anomaly Detection (IMPROVED)
# ============================================================================
print("\n" + "=" * 80)
print("STEP 4/4: ANOMALY DETECTION")
print("=" * 80)
print()

try:
    print("🔍 Training anomaly detection models...")
    print()
    
    # Check if improved anomaly detection script exists
    improved_ad_path = Path(__file__).parent / "anomaly_detection_classification_IMPROVED.py"
    
    if improved_ad_path.exists():
        import subprocess
        result = subprocess.run(
            [sys.executable, str(improved_ad_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            training_results['anomaly_detection']['status'] = 'success'
            print("\n✅ Anomaly Detection: SUCCESS")
        else:
            raise Exception(result.stderr)
    else:
        print("⚠️ Improved anomaly detection script not found, using existing models")
        training_results['anomaly_detection']['status'] = 'skipped'
    
except Exception as e:
    print(f"\n❌ Anomaly Detection: FAILED - {e}")
    training_results['anomaly_detection']['status'] = 'failed'
    training_results['anomaly_detection']['error'] = str(e)


# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("🎯 TRAINING SUMMARY")
print("=" * 80)
print()

success_count = sum(1 for r in training_results.values() if r['status'] == 'success')
failed_count = sum(1 for r in training_results.values() if r['status'] == 'failed')
skipped_count = sum(1 for r in training_results.values() if r['status'] == 'skipped')

print(f"✅ Successful: {success_count}/4")
print(f"❌ Failed: {failed_count}/4")
print(f"⚠️ Skipped: {skipped_count}/4")
print()

print("Detailed Results:")
print("-" * 80)

for model_name, result in training_results.items():
    status_icon = {
        'success': '✅',
        'failed': '❌',
        'skipped': '⚠️',
        'pending': '⏳'
    }[result['status']]
    
    print(f"{status_icon} {model_name.replace('_', ' ').title()}: {result['status'].upper()}")
    
    if result['status'] == 'success':
        if 'accuracy' in result and result['accuracy']:
            print(f"   Accuracy: {result['accuracy']:.4f}")
        if 'rmse' in result and result['rmse']:
            print(f"   RMSE: {result['rmse']:.2f}")
        if 'f1_score' in result and result['f1_score']:
            print(f"   F1-Score: {result['f1_score']:.4f}")
    
    if result['status'] == 'failed' and 'error' in result:
        print(f"   Error: {result['error'][:100]}")
    
    print()

# Save training summary
import json
from datetime import datetime

summary = {
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'results': training_results,
    'success_rate': f"{success_count}/4",
    'models_trained': [name for name, r in training_results.items() if r['status'] == 'success']
}

summary_path = Path(__file__).parent.parent / "models" / "training_summary.json"
summary_path.parent.mkdir(parents=True, exist_ok=True)

with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"📄 Training summary saved: {summary_path}")
print()

# ============================================================================
# NEXT STEPS
# ============================================================================
print("=" * 80)
print("🎯 NEXT STEPS")
print("=" * 80)
print()

if success_count == 4:
    print("🎉 ALL MODELS TRAINED SUCCESSFULLY!")
    print()
    print("Next steps:")
    print("  1. ✅ Test the models with real data")
    print("  2. ✅ Integrate models into ML API service")
    print("  3. ✅ Update documentation with real metrics")
    print("  4. ✅ Deploy to production")
    print()
    print("To integrate models into API:")
    print("  python ml/integrate_trained_models.py")
    
elif success_count > 0:
    print(f"✅ {success_count} models trained successfully!")
    print()
    print("Some models failed or were skipped. Review the errors above.")
    print()
    print("You can:")
    print("  1. Fix the errors and re-run this script")
    print("  2. Train individual models separately")
    print("  3. Use existing models for failed components")
    
else:
    print("❌ No models were trained successfully.")
    print()
    print("Please review the errors above and:")
    print("  1. Check if required dependencies are installed")
    print("  2. Verify data files are available")
    print("  3. Check for sufficient disk space")
    print("  4. Review error messages for specific issues")

print()
print("=" * 80)
print("Training pipeline complete!")
print("=" * 80)