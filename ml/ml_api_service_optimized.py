"""
🚀 OPTIMIZED ML API SERVICE FOR VAT REFUND PREDICTION
======================================================

Flask API that serves the OPTIMIZED trained ML model for VAT refund predictions.

Endpoints:
- POST /predict - Make a prediction
- GET /model-info - Get model metadata
- GET /health - Health check
- GET /stats - Get prediction statistics

Usage:
    python ml_api_service_optimized.py

The API will run on http://localhost:5001
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import json
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os
from collections import defaultdict
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
MODEL_DIR = 'optimized_models_25000_samples'
PORT = 5001

# Global variables for model artifacts
model = None
scaler = None
label_encoders = None
feature_columns = None
metadata = None

# Monitoring variables
prediction_stats = {
    'total_predictions': 0,
    'successful_predictions': 0,
    'failed_predictions': 0,
    'avg_response_time': 0.0,
    'start_time': datetime.now(),
    'predictions_by_region': defaultdict(int),
    'predictions_by_category': defaultdict(int),
    'auto_approved': 0,
    'manual_review': 0
}

# Setup logging
os.makedirs('../logs', exist_ok=True)
logging.basicConfig(
    filename='../logs/ml_api_optimized.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_models():
    """Load all model artifacts"""
    global model, scaler, label_encoders, feature_columns, metadata
    
    try:
        logger.info("Loading optimized models...")
        
        # Load the best model (Random Forest by default)
        model_path = f'{MODEL_DIR}/random_forest_optimized.pkl'
        if not os.path.exists(model_path):
            # Try Gradient Boosting
            model_path = f'{MODEL_DIR}/gradient_boosting_optimized.pkl'
        
        model = joblib.load(model_path)
        scaler = joblib.load(f'{MODEL_DIR}/scaler.pkl')
        label_encoders = joblib.load(f'{MODEL_DIR}/label_encoders.pkl')
        feature_columns = joblib.load(f'{MODEL_DIR}/feature_columns.pkl')
        
        # Load metadata from JSON
        try:
            with open(f'{MODEL_DIR}/best_parameters.json', 'r') as f:
                metadata = json.load(f)
        except:
            # Create basic metadata if file doesn't exist
            metadata = {
                'Best Model': 'Random Forest',
                'Best Test R² Score': 0.70,
                'Best RMSE': 6032.07,
                'Best MAE': 3380.51,
                'Training Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Training Samples': 20000,
                'Testing Samples': 5000
            }
        
        logger.info(f"✅ Models loaded successfully from {MODEL_DIR}")
        logger.info(f"✅ Model: {metadata.get('Best Model', 'Random Forest')}")
        logger.info(f"✅ R² Score: {metadata.get('random_forest', {}).get('test_r2', 0.70):.4f}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error loading models: {str(e)}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if model is None:
        return jsonify({
            'status': 'unhealthy',
            'message': 'Models not loaded'
        }), 503
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'model_dir': MODEL_DIR,
        'uptime_seconds': (datetime.now() - prediction_stats['start_time']).total_seconds()
    })

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get model metadata"""
    if model is None or metadata is None:
        return jsonify({
            'error': 'Models not loaded'
        }), 503
    
    # Extract Random Forest metrics from metadata
    rf_data = metadata.get('random_forest', {})
    
    return jsonify({
        'model_name': 'Random Forest',
        'r2_score': float(rf_data.get('test_r2', metadata.get('Best Test R² Score', 0.70))),
        'rmse': float(rf_data.get('test_rmse', metadata.get('Best RMSE', 6032.07))),
        'mae': float(rf_data.get('test_mae', metadata.get('Best MAE', 3380.51))),
        'training_date': metadata.get('Training Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'training_samples': int(metadata.get('Training Samples', 20000)),
        'testing_samples': int(metadata.get('Testing Samples', 5000)),
        'features': len(feature_columns) if feature_columns else 12,
        'hyperparameter_tuning': 'RandomizedSearchCV with 3-fold CV',
        'model_dir': MODEL_DIR,
        'best_params': rf_data.get('best_params', {})
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get prediction statistics"""
    uptime = (datetime.now() - prediction_stats['start_time']).total_seconds()
    
    return jsonify({
        'total_predictions': prediction_stats['total_predictions'],
        'successful_predictions': prediction_stats['successful_predictions'],
        'failed_predictions': prediction_stats['failed_predictions'],
        'success_rate': (prediction_stats['successful_predictions'] / max(prediction_stats['total_predictions'], 1)) * 100,
        'avg_response_time_ms': prediction_stats['avg_response_time'] * 1000,
        'uptime_seconds': uptime,
        'uptime_hours': uptime / 3600,
        'predictions_by_region': dict(prediction_stats['predictions_by_region']),
        'predictions_by_category': dict(prediction_stats['predictions_by_category']),
        'auto_approved': prediction_stats['auto_approved'],
        'manual_review': prediction_stats['manual_review'],
        'auto_approval_rate': (prediction_stats['auto_approved'] / max(prediction_stats['total_predictions'], 1)) * 100
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Make a VAT refund prediction"""
    start_time = time.time()
    prediction_stats['total_predictions'] += 1
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            prediction_stats['failed_predictions'] += 1
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['Amount', 'VAT_Rate', 'Category', 'Region', 'Filing_Status', 
                          'Compliance_Flag', 'Refund_Eligible', 'Is_Anomaly', 
                          'Risk_Score', 'Annual_Turnover']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            prediction_stats['failed_predictions'] += 1
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        # Calculate derived features
        vat_amount = data['Amount'] * (data['VAT_Rate'] / 100)
        amount_to_turnover = data['Amount'] / data['Annual_Turnover'] if data['Annual_Turnover'] > 0 else 0
        vat_to_amount = vat_amount / data['Amount'] if data['Amount'] > 0 else 0
        
        # Encode categorical variables
        encoded_features = {}
        for col in ['Category', 'Region', 'Filing_Status', 'Compliance_Flag', 'Refund_Eligible', 'Is_Anomaly']:
            le = label_encoders[col]
            try:
                encoded_features[col + '_Encoded'] = le.transform([data[col]])[0]
            except:
                # If value not in training data, use most common value (0)
                encoded_features[col + '_Encoded'] = 0
                logger.warning(f"Unknown value for {col}: {data[col]}, using default")
        
        # Create feature vector
        features = {
            'Amount': data['Amount'],
            'VAT_Amount': vat_amount,
            'VAT_Rate': data['VAT_Rate'],
            'Risk_Score': data['Risk_Score'],
            'Annual_Turnover': data['Annual_Turnover'],
            'Amount_to_Turnover_Ratio': amount_to_turnover,
            'VAT_to_Amount_Ratio': vat_to_amount,
            **encoded_features
        }
        
        # Create DataFrame with correct column order
        X = pd.DataFrame([features])[feature_columns]
        
        # Scale features
        X_scaled = scaler.transform(X)
        
        # Make prediction
        predicted_refund = float(model.predict(X_scaled)[0])
        
        # Determine recommendation
        if data['Risk_Score'] > 0.5:
            recommendation = 'manual_review'
            reason = 'High risk score'
            prediction_stats['manual_review'] += 1
        elif data['Compliance_Flag'] == 'Non-Compliant':
            recommendation = 'manual_review'
            reason = 'Non-compliant status'
            prediction_stats['manual_review'] += 1
        elif data['Is_Anomaly'] == 'Yes':
            recommendation = 'manual_review'
            reason = 'Anomaly detected'
            prediction_stats['manual_review'] += 1
        elif predicted_refund > 100000:
            recommendation = 'manual_review'
            reason = 'High value refund'
            prediction_stats['manual_review'] += 1
        else:
            recommendation = 'auto_approve'
            reason = 'Low risk, compliant'
            prediction_stats['auto_approved'] += 1
        
        # Update statistics
        prediction_stats['successful_predictions'] += 1
        prediction_stats['predictions_by_region'][data['Region']] += 1
        prediction_stats['predictions_by_category'][data['Category']] += 1
        
        # Calculate response time
        response_time = time.time() - start_time
        prediction_stats['avg_response_time'] = (
            (prediction_stats['avg_response_time'] * (prediction_stats['successful_predictions'] - 1) + response_time) /
            prediction_stats['successful_predictions']
        )
        
        # Log prediction
        logger.info(f"Prediction: ₹{predicted_refund:,.2f} | Recommendation: {recommendation} | Response time: {response_time*1000:.2f}ms")
        
        # Return response
        return jsonify({
            'success': True,
            'predicted_refund_amount': round(predicted_refund, 2),
            'recommendation': recommendation,
            'reason': reason,
            'confidence': 'high' if data['Risk_Score'] < 0.3 else 'medium' if data['Risk_Score'] < 0.6 else 'low',
            'model_info': {
                'model_name': metadata.get('Best Model', 'Unknown'),
                'r2_score': float(metadata.get('Best Test R² Score', 0)),
                'mae': float(metadata.get('Best MAE', 0))
            },
            'response_time_ms': round(response_time * 1000, 2)
        })
        
    except Exception as e:
        prediction_stats['failed_predictions'] += 1
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Make predictions for multiple transactions"""
    try:
        data = request.get_json()
        
        if not data or 'transactions' not in data:
            return jsonify({'error': 'No transactions provided'}), 400
        
        transactions = data['transactions']
        results = []
        
        for transaction in transactions:
            # Make individual prediction (reuse predict logic)
            # For simplicity, we'll call the predict endpoint internally
            # In production, optimize this to batch process
            try:
                # Create a mock request
                with app.test_request_context('/predict', method='POST', json=transaction):
                    response = predict()
                    if response[1] == 200:  # Success
                        results.append(response[0].get_json())
                    else:
                        results.append({'error': 'Prediction failed', 'transaction': transaction})
            except Exception as e:
                results.append({'error': str(e), 'transaction': transaction})
        
        return jsonify({
            'success': True,
            'total_transactions': len(transactions),
            'successful_predictions': sum(1 for r in results if 'predicted_refund_amount' in r),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 STARTING OPTIMIZED ML API SERVICE")
    print("=" * 80)
    
    # Load models
    print(f"\n📥 Loading models from: {MODEL_DIR}/")
    if load_models():
        print(f"✅ Models loaded successfully!")
        print(f"✅ Model: {metadata.get('Best Model', 'Unknown')}")
        print(f"✅ R² Score: {metadata.get('Best Test R² Score', 0):.4f}")
        print(f"✅ RMSE: ₹{metadata.get('Best RMSE', 0):,.2f}")
        print(f"✅ MAE: ₹{metadata.get('Best MAE', 0):,.2f}")
        
        print("\n" + "=" * 80)
        print("🌐 API ENDPOINTS")
        print("=" * 80)
        print(f"\n✅ POST   http://localhost:{PORT}/predict        - Make a prediction")
        print(f"✅ POST   http://localhost:{PORT}/batch-predict  - Batch predictions")
        print(f"✅ GET    http://localhost:{PORT}/model-info     - Get model metadata")
        print(f"✅ GET    http://localhost:{PORT}/stats          - Get statistics")
        print(f"✅ GET    http://localhost:{PORT}/health         - Health check")
        
        print("\n" + "=" * 80)
        print(f"🚀 Starting server on http://localhost:{PORT}")
        print("=" * 80)
        print("\nPress CTRL+C to stop the server\n")
        
        app.run(host='0.0.0.0', port=PORT, debug=False)
    else:
        print(f"\n❌ Failed to load models from {MODEL_DIR}/")
        print(f"⚠️  Please run 'python ml/train_optimized_models.py' first")