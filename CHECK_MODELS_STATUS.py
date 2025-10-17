"""
Quick Model Status Checker
Verifies all trained models are present and ready
"""

import os
import json
from pathlib import Path
from datetime import datetime

def check_models():
    """Check status of all ML models"""
    
    models_dir = Path("models")
    
    print("\n" + "="*60)
    print("  ML MODELS STATUS CHECK")
    print("="*60 + "\n")
    
    models_status = {}
    
    # 1. Document Classification
    print("[1/4] Document Classification...")
    doc_cnn = models_dir / "document_classifier" / "cnn_model.h5"
    doc_hybrid = models_dir / "document_classifier" / "hybrid_model.h5"
    doc_meta = models_dir / "document_classifier" / "metadata.json"
    
    if doc_cnn.exists() and doc_hybrid.exists() and doc_meta.exists():
        with open(doc_meta, 'r') as f:
            meta = json.load(f)
        print(f"  [OK] CNN Model: {meta['models']['cnn']['accuracy']*100:.1f}% accuracy")
        print(f"  [OK] Hybrid Model: {meta['models']['hybrid']['accuracy']*100:.1f}% accuracy")
        print(f"  [OK] Trained: {meta['training_date']}")
        print(f"  [OK] Classes: {meta['num_classes']} categories")
        models_status['document_classification'] = 'ready'
    else:
        print("  [MISSING] Models not found")
        models_status['document_classification'] = 'missing'
    
    print()
    
    # 2. Sentiment Analysis
    print("[2/4] Sentiment Analysis...")
    sent_model = models_dir / "sentiment_analysis" / "sentiment_model.pkl"
    sent_vec = models_dir / "sentiment_analysis" / "vectorizer.pkl"
    sent_meta = models_dir / "sentiment_analysis" / "metadata.json"
    
    if sent_model.exists() and sent_vec.exists() and sent_meta.exists():
        with open(sent_meta, 'r') as f:
            meta = json.load(f)
        print(f"  [OK] Model: Traditional ML")
        print(f"  [OK] Trained: {meta['training_date']}")
        print(f"  [OK] Classes: {len(meta['label_encoder'])} sentiments")
        models_status['sentiment_analysis'] = 'ready'
    else:
        print("  [MISSING] Models not found")
        models_status['sentiment_analysis'] = 'missing'
    
    print()
    
    # 3. Time Series Forecasting
    print("[3/4] Time Series Forecasting...")
    ts_meta = models_dir / "time_series_models_IMPROVED" / "metadata_improved.json"
    
    if ts_meta.exists():
        with open(ts_meta, 'r') as f:
            meta = json.load(f)
        print(f"  [OK] Best Model: {meta.get('winner', 'ARIMA')}")
        print(f"  [OK] MAPE: {meta.get('winner_mape', meta.get('walk_forward_mape', 0)):.2f}%")
        print(f"  [OK] Trained: {meta['training_date']}")
        models_status['time_series'] = 'ready'
    else:
        print("  [MISSING] Models not found")
        models_status['time_series'] = 'missing'
    
    print()
    
    # 4. Anomaly Detection
    print("[4/4] Anomaly Detection...")
    anom_model = models_dir / "anomaly_detection_models" / "best_model.pkl"
    anom_meta = models_dir / "anomaly_detection_models" / "metadata.json"
    
    if anom_model.exists() and anom_meta.exists():
        with open(anom_meta, 'r') as f:
            meta = json.load(f)
        print(f"  [OK] Best Model: {meta['best_model']}")
        print(f"  [OK] F1-Score: {meta.get('best_f1_score', meta.get('best_f1', 0)):.3f}")
        print(f"  [OK] Trained: {meta['training_date']}")
        models_status['anomaly_detection'] = 'ready'
    else:
        print("  [MISSING] Models not found")
        models_status['anomaly_detection'] = 'missing'
    
    print()
    
    # Summary
    ready_count = sum(1 for status in models_status.values() if status == 'ready')
    total_count = len(models_status)
    
    print("="*60)
    print(f"  SUMMARY: {ready_count}/{total_count} Models Ready")
    print("="*60)
    print()
    
    if ready_count == total_count:
        print("[SUCCESS] All models are trained and ready!")
        print()
        print("Next Steps:")
        print("  1. Test models: python ml/test_document_classifier.py")
        print("  2. Start servers: .\\START_ALL_SERVERS.ps1")
        print("  3. Access app: http://localhost:8080")
        print()
        return True
    else:
        print("[WARNING] Some models are missing!")
        print()
        print("To train missing models:")
        print("  .\\TRAIN_ALL_MODELS.bat")
        print()
        return False

if __name__ == "__main__":
    try:
        success = check_models()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        exit(1)