"""
OPTIMIZED ML API SERVICE FOR VAT REFUND PREDICTION WITH EXPLAINABILITY
=======================================================================

Flask API that serves the OPTIMIZED trained ML model for VAT refund predictions.

Endpoints:
- POST /predict - Make a prediction
- POST /explain - Get SHAP explanation for prediction
- POST /batch-predict - Batch predictions
- GET /model-info - Get model metadata
- GET /health - Health check
- GET /stats - Get prediction statistics
- GET /feature-importance - Get global feature importance
- POST /compare-predictions - Compare multiple predictions

Usage:
    python ml_api_service_optimized.py

The API will run on http://localhost:8000
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
import shap
import warnings
warnings.filterwarnings('ignore')

# Import validation module
from .validation import (
    PredictionRequest, ExplainRequest, BatchPredictionRequest, ComparisonRequest,
    validate_request, get_validation_reference
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
# Use absolute path for models, or relative to parent directory if running from ml/
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
MODEL_DIR = os.path.join(_project_root, 'optimized_models_25000_samples')
PORT = int(os.getenv('ML_API_PORT', '8000'))  # Support ML_API_PORT env var, default to 8000

# Initialize models on app startup
_models_initialized = False

# Global variables for model artifacts
model = None
scaler = None
label_encoders = None
feature_columns = None
metadata = None
shap_explainer = None
background_data = None  # For SHAP

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

# Setup logging (with fallback for Render free tier)
log_file = None
try:
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'ml_api_optimized.log')
except Exception as e:
    # Fallback: Log to stdout only on Render
    log_file = None

if log_file:
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
else:
    # Log to console on Render free tier
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

@app.before_request
def initialize_models():
    """Initialize models on first request"""
    global _models_initialized
    if not _models_initialized:
        _models_initialized = load_models()
        if _models_initialized:
            logger.info("✅ Models initialized on first request")

def load_models():
    """Load all model artifacts and initialize SHAP explainer"""
    global model, scaler, label_encoders, feature_columns, metadata, shap_explainer, background_data
    
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
            with open(f'{MODEL_DIR}/metadata.json', 'r') as f:
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
                'Testing Samples': 5000,
                'random_forest': {
                    'test_r2': 0.70,
                    'test_rmse': 6032.07,
                    'test_mae': 3380.51
                }
            }
        
        # Initialize SHAP explainer
        try:
            shap_explainer = shap.TreeExplainer(model)
            logger.info("✅ SHAP TreeExplainer initialized")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize SHAP explainer: {e}")
            shap_explainer = None
        
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

@app.route('/validation-reference', methods=['GET'])
def validation_reference():
    """
    Get reference of valid input values for API calls.
    Useful for client-side validation and auto-complete.
    """
    return jsonify({
        'valid_categories': get_validation_reference(),
        'field_descriptions': {
            'Amount': 'Refund amount in EUR (required, > 0)',
            'VAT_Rate': 'VAT rate as percentage (required, 0-100)',
            'Risk_Score': 'Risk score from 0 to 1 (required)',
            'Annual_Turnover': 'Annual turnover in EUR (required, >= 0)',
            'Category': 'Product/Service category (required, see valid_categories)',
            'Region': 'Geographic region (required, see valid_categories)',
            'Filing_Status': 'Filing status (required, see valid_categories)',
            'Compliance_Flag': 'Compliance status (required, see valid_categories)',
            'Refund_Eligible': 'Refund eligibility (required, see valid_categories)',
            'Is_Anomaly': 'Anomaly flag (required, see valid_categories)'
        },
        'example_request': {
            'Amount': 50000,
            'VAT_Rate': 19,
            'Risk_Score': 0.3,
            'Annual_Turnover': 500000,
            'Category': 'Retail',
            'Region': 'East',
            'Filing_Status': 'On Time',
            'Compliance_Flag': 'Compliant',
            'Refund_Eligible': 'Yes',
            'Is_Anomaly': 'No'
        }
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
            return jsonify({
                'error': 'No data provided',
                'status': 'error'
            }), 400
        
        # Validate request using Pydantic schema
        try:
            validated_data = PredictionRequest(**data)
        except ValueError as e:
            prediction_stats['failed_predictions'] += 1
            error_msg = str(e)
            logger.warning(f"Validation error: {error_msg}")
            return jsonify({
                'error': 'Invalid input data',
                'details': error_msg,
                'status': 'validation_error',
                'valid_categories': get_validation_reference()
            }), 400
        
        # Calculate derived features
        vat_amount = validated_data.Amount * (validated_data.VAT_Rate / 100)
        amount_to_turnover = validated_data.Amount / validated_data.Annual_Turnover if validated_data.Annual_Turnover > 0 else 0
        vat_to_amount = vat_amount / validated_data.Amount if validated_data.Amount > 0 else 0
        
        # Encode categorical variables (now guaranteed valid)
        encoded_features = {}
        for col in ['Category', 'Region', 'Filing_Status', 'Compliance_Flag', 'Refund_Eligible', 'Is_Anomaly']:
            le = label_encoders[col]
            # No try/except needed - validation ensures values exist
            encoded_features[col + '_Encoded'] = le.transform([getattr(validated_data, col)])[0]
        
        # Create feature vector
        features = {
            'Amount': validated_data.Amount,
            'VAT_Amount': vat_amount,
            'VAT_Rate': validated_data.VAT_Rate,
            'Risk_Score': validated_data.Risk_Score,
            'Annual_Turnover': validated_data.Annual_Turnover,
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
        if validated_data.Risk_Score > 0.5:
            recommendation = 'manual_review'
            reason = 'High risk score'
            prediction_stats['manual_review'] += 1
        elif validated_data.Compliance_Flag == 'Non-Compliant':
            recommendation = 'manual_review'
            reason = 'Non-compliant status'
            prediction_stats['manual_review'] += 1
        elif validated_data.Is_Anomaly == 'Yes':
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
        prediction_stats['predictions_by_region'][validated_data.Region] += 1
        prediction_stats['predictions_by_category'][validated_data.Category] += 1
        
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

@app.route('/explain', methods=['POST'])
def explain_prediction():
    """
    Get SHAP explanation for a VAT prediction
    
    Request format:
    {
        "Amount": 50000,
        "VAT_Rate": 19,
        "Risk_Score": 0.3,
        "Annual_Turnover": 500000,
        "Category": "goods",
        "Region": "EU",
        "Filing_Status": "quarterly",
        "Compliance_Flag": "Compliant",
        "Refund_Eligible": "Yes",
        "Is_Anomaly": "No"
    }
    """
    if not shap_explainer:
        return jsonify({
            'success': False,
            'error': 'SHAP explainer not available'
        }), 503
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate request using Pydantic schema
        try:
            validated_data = ExplainRequest(**data)
        except ValueError as e:
            error_msg = str(e)
            logger.warning(f"Validation error in /explain: {error_msg}")
            return jsonify({
                'success': False,
                'error': 'Invalid input data',
                'details': error_msg,
                'status': 'validation_error',
                'valid_categories': get_validation_reference()
            }), 400
        
        # Calculate derived features
        vat_amount = validated_data.Amount * (validated_data.VAT_Rate / 100)
        amount_to_turnover = validated_data.Amount / validated_data.Annual_Turnover if validated_data.Annual_Turnover > 0 else 0
        vat_to_amount = vat_amount / validated_data.Amount if validated_data.Amount > 0 else 0
        
        # Encode categorical variables (now guaranteed valid)
        encoded_features = {}
        for col in ['Category', 'Region', 'Filing_Status', 'Compliance_Flag', 'Refund_Eligible', 'Is_Anomaly']:
            le = label_encoders[col]
            encoded_features[col + '_Encoded'] = le.transform([getattr(validated_data, col)])[0]
        
        # Create feature vector
        features = {
            'Amount': validated_data.Amount,
            'VAT_Amount': vat_amount,
            'VAT_Rate': validated_data.VAT_Rate,
            'Risk_Score': validated_data.Risk_Score,
            'Annual_Turnover': validated_data.Annual_Turnover,
            'Amount_to_Turnover_Ratio': amount_to_turnover,
            'VAT_to_Amount_Ratio': vat_to_amount,
            **encoded_features
        }
        
        # Create DataFrame with correct column order
        X = pd.DataFrame([features])[feature_columns]
        X_scaled = scaler.transform(X)
        
        # Make prediction
        prediction = float(model.predict(X_scaled)[0])
        
        # Get SHAP values
        shap_values = shap_explainer.shap_values(X_scaled)
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
        
        # Calculate base value
        base_value = float(shap_explainer.expected_value)
        if isinstance(base_value, (list, np.ndarray)):
            base_value = float(base_value[0])
        
        # Prepare feature importance with detailed explanations
        feature_impact = []
        for i, col in enumerate(feature_columns):
            feature_impact.append({
                'feature': col,
                'value': float(X_scaled[0, i]),
                'shap_value': float(shap_values[0, i]),
                'contribution': float(shap_values[0, i] * X_scaled[0, i]) if X_scaled[0, i] != 0 else 0
            })
        
        # Sort by absolute SHAP value
        feature_impact = sorted(feature_impact, key=lambda x: abs(x['shap_value']), reverse=True)
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'base_value': base_value,
            'method': 'SHAP',
            'top_features': feature_impact[:10],
            'all_features': feature_impact,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Explanation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/feature-importance', methods=['GET'])
def get_feature_importance():
    """
    Get global feature importance from the model
    """
    try:
        # Get feature importances from the model
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        else:
            return jsonify({
                'success': False,
                'error': 'Model does not support feature importance'
            }), 400
        
        # Create sorted list
        feature_importance = []
        for i, col in enumerate(feature_columns):
            feature_importance.append({
                'feature': col,
                'importance': float(importances[i])
            })
        
        # Sort by importance
        feature_importance = sorted(feature_importance, key=lambda x: x['importance'], reverse=True)
        
        return jsonify({
            'success': True,
            'feature_importance': feature_importance,
            'top_features': feature_importance[:10],
            'model_type': metadata.get('Best Model', 'Random Forest'),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Feature importance error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 80)
    print("[*] STARTING OPTIMIZED ML API SERVICE")
    print("=" * 80)
    
    # Load models
    print(f"\n[>>] Loading models from: {MODEL_DIR}/")
    if load_models():
        print(f"[OK] Models loaded successfully!")
        print(f"[OK] Model: {metadata.get('Best Model', 'Unknown')}")
        print(f"[OK] R² Score: {metadata.get('Best Test R² Score', 0):.4f}")
        print(f"[OK] RMSE: {metadata.get('Best RMSE', 0):,.2f}")
        print(f"[OK] MAE: {metadata.get('Best MAE', 0):,.2f}")
        
        print("\n" + "=" * 80)
        print("[WEB] API ENDPOINTS")
        print("=" * 80)
        print(f"\n[OK] POST   http://localhost:{PORT}/predict              - Make a prediction")
        print(f"[OK] POST   http://localhost:{PORT}/batch-predict       - Batch predictions")
        print(f"[OK] POST   http://localhost:{PORT}/explain             - SHAP explanation")
        print(f"[OK] GET    http://localhost:{PORT}/feature-importance  - Feature importance")
        print(f"[OK] GET    http://localhost:{PORT}/model-info         - Model metadata")
        print(f"[OK] GET    http://localhost:{PORT}/stats              - Statistics")
        print(f"[OK] GET    http://localhost:{PORT}/health             - Health check")
        
        print("\n" + "=" * 80)
        print(f"[*] Starting server on http://localhost:{PORT}")
        print("=" * 80)
        print("\nPress CTRL+C to stop the server\n")
        
        app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False, threaded=True)
    else:
        print(f"\n[XX] Failed to load models from {MODEL_DIR}/")
        print(f"[!] Please run 'python ml/train_optimized_models.py' first")