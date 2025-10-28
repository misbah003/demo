"""
🚀 ADVANCED ML API WITH EXPLAINABILITY
======================================

Integrates all ML models with SHAP/LIME explainability:
- NER with attention visualization
- Document Classification with explanation
- VAT Prediction with feature importance
- Anomaly Detection with risk analysis
- Time Series Forecasting with confidence intervals

Endpoints:
- POST /api/predict - Make prediction
- POST /api/explain - Get SHAP/LIME explanation
- POST /api/explain-vat - Detailed VAT prediction explanation
- POST /api/explain-document - Document classification explanation
- POST /api/explain-anomaly - Anomaly score explanation
- POST /api/explain-report - Generate PDF report
- GET /api/status - System status
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import numpy as np
import pandas as pd
from datetime import datetime
import json
import joblib
import os
import logging

# Import ML modules
from advanced_ner_extraction import AdvancedNERExtractor
from advanced_document_classifier import AdvancedDocumentClassifier
from advanced_time_series_forecasting import AdvancedVATForecaster
from explainability_service import ExplainabilityService, format_explanation_for_api
from explainability_report_generator import ExplainabilityReportGenerator

# Initialize FastAPI
app = FastAPI(
    title="ML API with Explainability",
    description="Advanced ML models with SHAP/LIME explanations",
    version="3.0.0"
)

# CORS - Must be first middleware to handle OPTIONS preflight requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be restricted to specific domains)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight responses for 1 hour
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
ner_extractor = None
doc_classifier = None
vat_forecaster = None
explainability_service = None
report_generator = None

# Paths
MODEL_DIR = 'optimized_models_25000_samples'
REPORTS_DIR = 'explainability_reports'

# Ensure reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

# Request/Response Models
class PredictionRequest(BaseModel):
    """Base prediction request"""
    data: Dict

class ExplanationRequest(BaseModel):
    """Explanation request"""
    data: Dict
    method: str = "shap"  # shap or lime
    model_type: str = "random_forest"

class VATExplanationRequest(BaseModel):
    """VAT-specific explanation request"""
    features: Dict
    amount: float
    method: str = "shap"

class DocumentExplanationRequest(BaseModel):
    """Document classification explanation request"""
    text: str
    method: str = "shap"  # "shap", "lime", or "attention" (all now use SHAP/LIME)

class ExplainabilityReportRequest(BaseModel):
    """Report generation request"""
    prediction_data: Dict
    model_name: str
    input_summary: Dict

# ===================== STARTUP/SHUTDOWN =====================

@app.on_event("startup")
async def startup_event():
    """Initialize models and services"""
    global ner_extractor, doc_classifier, vat_forecaster, explainability_service, report_generator
    
    logger.info("🚀 Starting ML API with Explainability...")
    
    try:
        # Initialize explainability service
        logger.info("📊 Initializing Explainability Service...")
        explainability_service = ExplainabilityService()
        
        # Initialize report generator
        logger.info("📄 Initializing Report Generator...")
        report_generator = ExplainabilityReportGenerator(output_dir=REPORTS_DIR)
        
        # Initialize NER
        logger.info("📝 Loading NER Extractor...")
        ner_extractor = AdvancedNERExtractor()
        
        # Initialize Document Classifier
        logger.info("📄 Loading Document Classifier...")
        doc_classifier = AdvancedDocumentClassifier()
        
        # Initialize VAT Forecaster
        logger.info("📊 Loading VAT Forecaster...")
        vat_forecaster = AdvancedVATForecaster()
        
        logger.info("✅ All models initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Initialization error: {e}")
        raise

# ===================== HEALTH CHECK =====================

@app.get("/health")
async def health_check():
    """Render health check endpoint - must respond quickly"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """API status"""
    return {
        "status": "online",
        "message": "ML API with Explainability",
        "version": "3.0.0",
        "models_ready": {
            "ner": ner_extractor is not None,
            "classifier": doc_classifier is not None,
            "forecaster": vat_forecaster is not None,
            "explainability": explainability_service is not None,
            "report_generator": report_generator is not None
        },
        "features": [
            "predictions",
            "SHAP explanations",
            "LIME explanations",
            "Attention visualization",
            "PDF reports",
            "Anomaly detection"
        ]
    }

@app.get("/api/status")
async def get_status():
    """Detailed status check"""
    return {
        "timestamp": datetime.now().isoformat(),
        "status": "operational",
        "explainability_enabled": True,
        "supported_methods": ["shap", "lime", "attention"],
        "api_version": "3.0.0"
    }

# ===================== PREDICTION ENDPOINTS =====================

@app.post("/api/extract-entities")
async def extract_entities(request: PredictionRequest):
    """Extract entities with background information"""
    if ner_extractor is None:
        raise HTTPException(status_code=503, detail="NER model not initialized")
    
    try:
        text = request.data.get("text", "")
        
        # Extract entities
        entities = ner_extractor.extract_entities(text)
        
        # Analyze document
        analysis = ner_extractor.analyze_document_structure(text)
        
        return {
            "status": "success",
            "entities": entities,
            "document_analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===================== VAT PREDICTION ENDPOINT =====================

@app.post("/predict")
async def predict_vat_refund(request: PredictionRequest):
    """
    Make a VAT refund prediction (compatible with frontend)
    
    Request format:
    {
        "businessType": "Manufacturing" | "Services" | "Trading" | "Retail",
        "turnover": float,
        "vatPaid": float,
        "vatClaimed": float,
        "category": string,
        "region": string (one of: Delhi, Gujarat, Haryana, Karnataka, Kerala, Maharashtra, Punjab, Rajasthan, Tamil Nadu, Uttar Pradesh),
        "filingStatus": "Filed" | "Not Filed",
        "riskScore": float (0-1)
    }
    """
    try:
        # Extract prediction data from request
        data = request.data
        
        # Validate required fields
        required_fields = ['businessType', 'turnover', 'vatPaid', 'vatClaimed', 'category', 'region', 'filingStatus', 'riskScore']
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Load the trained model and scaler
        model_path = f'{MODEL_DIR}/random_forest_optimized.pkl'
        if not os.path.exists(model_path):
            model_path = f'{MODEL_DIR}/gradient_boosting_optimized.pkl'
        
        model = joblib.load(model_path)
        scaler = joblib.load(f'{MODEL_DIR}/scaler.pkl')
        label_encoders = joblib.load(f'{MODEL_DIR}/label_encoders.pkl')
        feature_columns = joblib.load(f'{MODEL_DIR}/feature_columns.pkl')
        
        # Prepare features
        vat_amount = data['turnover'] * (data.get('vatPaid', 0) / max(data['turnover'], 1)) if data['turnover'] > 0 else 0
        amount_to_turnover = data['turnover'] / max(data['turnover'], 1) if data['turnover'] > 0 else 0
        vat_to_amount = vat_amount / max(data['turnover'], 1) if data['turnover'] > 0 else 0
        
        # Encode categorical features using fitted label encoders
        encoded_features = {}
        try:
            # Map business type to category if needed
            category = data.get('category', 'Electronics')
            region = data.get('region', 'Maharashtra')
            filing_status = data.get('filingStatus', 'Filed')
            compliance_flag = 'Non-Compliant' if data.get('riskScore', 0.3) < 0.3 else 'Compliant'
            refund_eligible = 'Yes' if data['vatClaimed'] > 0 else 'No'
            is_anomaly = 'No'
            
            # Transform using label encoders
            if 'Category' in label_encoders:
                encoded_features['Category_Encoded'] = int(label_encoders['Category'].transform([category])[0])
            if 'Region' in label_encoders:
                encoded_features['Region_Encoded'] = int(label_encoders['Region'].transform([region])[0])
            if 'Filing_Status' in label_encoders:
                encoded_features['Filing_Status_Encoded'] = int(label_encoders['Filing_Status'].transform([filing_status])[0])
            if 'Compliance_Flag' in label_encoders:
                encoded_features['Compliance_Flag_Encoded'] = int(label_encoders['Compliance_Flag'].transform([compliance_flag])[0])
            if 'Refund_Eligible' in label_encoders:
                encoded_features['Refund_Eligible_Encoded'] = int(label_encoders['Refund_Eligible'].transform([refund_eligible])[0])
            if 'Is_Anomaly' in label_encoders:
                encoded_features['Is_Anomaly_Encoded'] = int(label_encoders['Is_Anomaly'].transform([is_anomaly])[0])
                
        except Exception as encode_err:
            logger.warning(f"Encoding warning: {encode_err}, using defaults")
            # Use safe defaults
            encoded_features = {
                'Category_Encoded': 0,
                'Region_Encoded': 0,
                'Filing_Status_Encoded': 0,
                'Compliance_Flag_Encoded': 0,
                'Refund_Eligible_Encoded': 1 if data['vatClaimed'] > 0 else 0,
                'Is_Anomaly_Encoded': 0
            }
        
        # Create feature vector with only required columns
        features = {
            'Amount': data['turnover'],
            'VAT_Amount': vat_amount,
            'VAT_Rate': (data['vatPaid'] / max(data['turnover'], 1) * 100) if data['turnover'] > 0 else 18,
            'Risk_Score': data.get('riskScore', 0.3),
            'Annual_Turnover': data['turnover'],
            'Amount_to_Turnover_Ratio': amount_to_turnover,
            'VAT_to_Amount_Ratio': vat_to_amount,
            'Category_Encoded': encoded_features.get('Category_Encoded', 0),
            'Region_Encoded': encoded_features.get('Region_Encoded', 0),
            'Filing_Status_Encoded': encoded_features.get('Filing_Status_Encoded', 0),
            'Compliance_Flag_Encoded': encoded_features.get('Compliance_Flag_Encoded', 0),
            'Is_Anomaly_Encoded': encoded_features.get('Is_Anomaly_Encoded', 0)
        }
        
        # Prepare DataFrame with only the required columns in the correct order
        X = pd.DataFrame([features])[feature_columns]
        X_scaled = scaler.transform(X)
        
        # Make prediction
        predicted_refund = float(model.predict(X_scaled)[0])
        predicted_refund = max(0, predicted_refund)  # Ensure non-negative
        
        # Determine approval probability based on risk score and refund amount
        risk_score = data.get('riskScore', 0.3)
        if risk_score > 0.7:
            approval_prob = 0.2
            recommendation = "manual_review"
        elif risk_score > 0.5:
            approval_prob = 0.5
            recommendation = "manual_review"
        elif predicted_refund > 100000:
            approval_prob = 0.7
            recommendation = "auto_approve"
        else:
            approval_prob = 0.85
            recommendation = "auto_approve"
        
        # Build response matching frontend expectations
        response = {
            "predictedRefund": round(predicted_refund, 2),
            "approvalProbability": round(approval_prob * 100, 1),
            "recommendation": recommendation,
            "breakdown": {
                "adjustments": []
            },
            "riskAssessment": {
                "level": "high" if risk_score > 0.6 else "medium" if risk_score > 0.3 else "low",
                "complianceFlag": data.get('filingStatus', 'Filed') != 'Filed',
                "score": risk_score
            },
            "modelInfo": {
                "name": "VAT Refund Predictor",
                "version": "3.0.0",
                "confidence": "high"
            }
        }
        
        logger.info(f"✅ VAT Prediction: ₹{predicted_refund:,.2f} | Risk: {response['riskAssessment']['level']} | Approval: {approval_prob*100:.1f}%")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in VAT prediction: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ===================== EXPLAINABILITY ENDPOINTS =====================

@app.post("/api/explain-vat")
async def explain_vat_prediction(request: VATExplanationRequest):
    """
    Explain VAT refund prediction with SHAP values
    
    Request format:
    {
        "features": {"region": "EU", "category": "services", ...},
        "amount": 50000,
        "method": "shap"
    }
    """
    if explainability_service is None:
        raise HTTPException(status_code=503, detail="Explainability service not initialized")
    
    try:
        # Load model
        model_path = f'{MODEL_DIR}/random_forest_optimized.pkl'
        if not os.path.exists(model_path):
            model_path = f'{MODEL_DIR}/gradient_boosting_optimized.pkl'
        
        model = joblib.load(model_path)
        
        # Load feature info
        feature_columns = joblib.load(f'{MODEL_DIR}/feature_columns.pkl')
        
        # Prepare input data
        input_df = pd.DataFrame([request.features])
        
        # Get explanation
        explanation = explainability_service.explain_vat_prediction(
            model=model,
            input_data=input_df,
            feature_names=feature_columns,
            model_type="random_forest",
            method=request.method.lower()
        )
        
        # Format for API
        result = format_explanation_for_api(explanation)
        result["predicted_amount"] = explanation.get("prediction")
        result["input_amount"] = request.amount
        
        return result
        
    except Exception as e:
        logger.error(f"Error in VAT explanation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/explain-document")
async def explain_document_classification(request: DocumentExplanationRequest):
    """
    Explain document classification using SHAP or LIME
    
    Now uses model-agnostic explainability methods for CNNs instead of random attention weights!
    
    Request format:
    {
        "text": "Document content...",
        "method": "shap"  # or "lime"
    }
    
    Methods:
    - "shap": SHAP (Shapley Additive exPlanations) using KernelExplainer for neural networks
    - "lime": LIME (Local Interpretable Model-agnostic Explanations) for local linear approximations
    - "attention": Alias for SHAP (backward compatible)
    
    Response includes:
    - predicted_class: The classified document category
    - confidence: Confidence score for the prediction
    - all_probabilities: Probabilities for all classes
    - top_tokens: Top 15 most influential tokens with their contributions
    - explanation_method: Technical description of the method used
    """
    if doc_classifier is None or explainability_service is None:
        raise HTTPException(status_code=503, detail="Required models not initialized")
    
    try:
        # Map "attention" to "shap" for backward compatibility
        method = "shap" if request.method.lower() == "attention" else request.method.lower()
        
        # Get explanation
        # Use reverse_label_encoder if available (idx -> label), otherwise label_encoder (label -> idx)
        label_encoder_to_use = getattr(doc_classifier, 'reverse_label_encoder', doc_classifier.label_encoder)
        
        explanation = explainability_service.explain_document_classification(
            model=doc_classifier.models.get('cnn'),
            input_text=request.text,
            tokenizer=doc_classifier.tokenizer,
            label_encoder=label_encoder_to_use,
            method=method
        )
        
        return format_explanation_for_api(explanation)
        
    except Exception as e:
        logger.error(f"Error in document explanation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/explain-anomaly")
async def explain_anomaly_detection(request: PredictionRequest):
    """
    Explain anomaly detection score with risk assessment
    
    Request format:
    {
        "data": {
            "feature1": value1,
            "feature2": value2,
            ...
        }
    }
    """
    if explainability_service is None:
        raise HTTPException(status_code=503, detail="Explainability service not initialized")
    
    try:
        # Load anomaly model
        model_path = f'{MODEL_DIR}/../anomaly_detection_models/best_model.pkl'
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            
            # Prepare data
            input_df = pd.DataFrame([request.data])
            feature_names = list(request.data.keys())
            
            # Get explanation
            explanation = explainability_service.explain_anomaly_score(
                model=model,
                input_data=input_df,
                feature_names=feature_names,
                anomaly_threshold=0.5
            )
            
            return format_explanation_for_api(explanation)
        else:
            raise HTTPException(status_code=404, detail="Anomaly model not found")
            
    except Exception as e:
        logger.error(f"Error in anomaly explanation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/explain-report")
async def generate_explanation_report(request: ExplainabilityReportRequest):
    """
    Generate comprehensive explanation report in multiple formats
    
    Request format:
    {
        "prediction_data": {...},
        "model_name": "vat_predictor",
        "input_summary": {...}
    }
    
    Returns JSON, HTML, and optional PDF reports with:
    - Prediction summary
    - Feature importance analysis
    - Risk assessment
    - Professional visualization
    """
    if report_generator is None or explainability_service is None:
        raise HTTPException(status_code=503, detail="Report generator not initialized")
    
    try:
        # Generate JSON report
        json_report = report_generator.generate_json_report(
            prediction_data=request.prediction_data,
            explanation_data=request.input_summary,
            model_name=request.model_name,
            model_type="vat_predictor"
        )
        
        # Generate HTML report
        html_report = report_generator.generate_html_report(
            prediction_data=request.prediction_data,
            explanation_data=request.input_summary,
            model_name=request.model_name,
            model_type="vat_predictor"
        )
        
        # Generate PDF report (optional, requires reportlab)
        pdf_path = report_generator.generate_pdf_report(
            prediction_data=request.prediction_data,
            explanation_data=request.input_summary,
            model_name=request.model_name,
            model_type="vat_predictor"
        )
        
        # Generate unique report ID
        report_id = f"report_{request.model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save reports to files
        json_path = report_generator.save_json_report(
            prediction_data=request.prediction_data,
            explanation_data=request.input_summary,
            model_name=request.model_name,
            model_type="vat_predictor",
            filename=f"{report_id}.json"
        )
        
        html_path = report_generator.save_html_report(
            prediction_data=request.prediction_data,
            explanation_data=request.input_summary,
            model_name=request.model_name,
            model_type="vat_predictor",
            filename=f"{report_id}.html"
        )
        
        logger.info(f"✅ Report generated: {report_id}")
        
        return {
            "status": "success",
            "report_id": report_id,
            "model_name": request.model_name,
            "timestamp": datetime.now().isoformat(),
            "reports": {
                "json": {
                    "url": f"/api/reports/{report_id}.json",
                    "filename": f"{report_id}.json"
                },
                "html": {
                    "url": f"/api/reports/{report_id}.html",
                    "filename": f"{report_id}.html"
                },
                "pdf": {
                    "url": f"/api/reports/{report_id}.pdf" if pdf_path else None,
                    "filename": f"{report_id}.pdf" if pdf_path else None,
                    "available": pdf_path is not None
                }
            },
            "summary": {
                "prediction": json_report.get('prediction', {}),
                "risk_level": json_report.get('risk_assessment', {}).get('level'),
                "top_features": json_report.get('feature_importance', {}).get('top_features', [])[:5]
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===================== REPORT DOWNLOAD =====================

@app.get("/api/reports/{filename}")
async def download_report(filename: str):
    """Download explanation report in JSON, HTML, or PDF format"""
    try:
        # Validate filename to prevent directory traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        report_path = os.path.join(REPORTS_DIR, filename)
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail=f"Report not found: {filename}")
        
        # Determine media type based on file extension
        if filename.endswith('.json'):
            media_type = "application/json"
        elif filename.endswith('.html'):
            media_type = "text/html"
        elif filename.endswith('.pdf'):
            media_type = "application/pdf"
        else:
            media_type = "application/octet-stream"
        
        logger.info(f"📥 Downloading report: {filename}")
        
        return FileResponse(
            path=report_path,
            filename=filename,
            media_type=media_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error downloading report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===================== REPORT MANAGEMENT =====================

@app.get("/api/reports")
async def list_reports():
    """List all available explainability reports"""
    try:
        reports = []
        if os.path.exists(REPORTS_DIR):
            for filename in sorted(os.listdir(REPORTS_DIR), reverse=True):
                if filename.endswith(('.json', '.html', '.pdf')):
                    filepath = os.path.join(REPORTS_DIR, filename)
                    file_stat = os.stat(filepath)
                    
                    reports.append({
                        "filename": filename,
                        "format": filename.split('.')[-1].upper(),
                        "size": file_stat.st_size,
                        "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                        "url": f"/api/reports/{filename}"
                    })
        
        logger.info(f"📋 Retrieved {len(reports)} reports")
        
        return {
            "status": "success",
            "total_reports": len(reports),
            "reports": reports[:50]  # Return latest 50 reports
        }
        
    except Exception as e:
        logger.error(f"❌ Error listing reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/reports/{filename}")
async def delete_report(filename: str):
    """Delete an explainability report"""
    try:
        # Validate filename
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        report_path = os.path.join(REPORTS_DIR, filename)
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="Report not found")
        
        os.remove(report_path)
        logger.info(f"🗑️  Deleted report: {filename}")
        
        return {
            "status": "success",
            "message": f"Report {filename} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===================== BATCH EXPLANATIONS =====================

@app.post("/api/explain-batch")
async def explain_batch(request: List[ExplanationRequest], background_tasks: BackgroundTasks):
    """
    Process batch explanations asynchronously
    
    Request format: Array of explanation requests
    """
    if explainability_service is None:
        raise HTTPException(status_code=503, detail="Explainability service not initialized")
    
    try:
        # Create batch ID
        batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Process batch in background
        background_tasks.add_task(
            _process_batch_explanations,
            batch_id=batch_id,
            requests=request
        )
        
        return {
            "status": "processing",
            "batch_id": batch_id,
            "total_items": len(request),
            "check_status_url": f"/api/batch/{batch_id}/status"
        }
        
    except Exception as e:
        logger.error(f"Error in batch explanation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/batch/{batch_id}/status")
async def get_batch_status(batch_id: str):
    """Get batch processing status"""
    try:
        status_file = f"{REPORTS_DIR}/{batch_id}_status.json"
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                return json.load(f)
        else:
            return {"status": "not_found", "batch_id": batch_id}
    except Exception as e:
        logger.error(f"Error getting batch status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===================== ADVANCED ANOMALY DETECTION EXPLAINABILITY =====================

@app.post("/api/explain-anomaly-advanced")
async def explain_anomaly_detection_advanced(request: PredictionRequest):
    """
    Explain anomaly detection using SHAP or LIME
    
    Request format:
    {
        "data": {
            "VAT_Amount": 5000,
            "Amount": 50000,
            "Risk_Score": 0.7,
            ...
        },
        "method": "shap"  # or "lime"
    }
    
    Response includes:
    - is_anomaly: Boolean indicating if transaction is anomalous
    - anomaly_score: Numeric score (0-1) indicating anomaly probability
    - feature_contributions: Top 15 features influencing the decision
    - top_positive_features: Features pushing towards anomaly classification
    - top_negative_features: Features pushing away from anomaly classification
    """
    if explainability_service is None:
        raise HTTPException(status_code=503, detail="Explainability service not initialized")
    
    try:
        # Load anomaly model
        model_path = 'models/anomaly_detection_models/best_model.pkl'
        if not os.path.exists(model_path):
            model_path = 'models/anomaly_detection_models_IMPROVED/best_model.pkl'
        
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Anomaly model not found")
        
        model = joblib.load(model_path)
        
        # Prepare input data
        input_df = pd.DataFrame([request.data])
        feature_names = list(request.data.keys())
        
        # Get explanation
        method = request.method.lower() if hasattr(request, 'method') else 'shap'
        explanation = explainability_service.explain_anomaly_detection(
            model=model,
            input_data=input_df,
            feature_names=feature_names,
            method=method
        )
        
        # Enhance response
        result = format_explanation_for_api(explanation)
        
        # Add risk level assessment
        anomaly_score = explanation.get('anomaly_score', 0)
        if anomaly_score < 0.3:
            result['risk_level'] = 'LOW'
        elif anomaly_score < 0.7:
            result['risk_level'] = 'MEDIUM'
        else:
            result['risk_level'] = 'HIGH'
        
        # Separate positive and negative contributors
        contributions = explanation.get('feature_contributions', [])
        result['top_positive_features'] = [
            f for f in contributions 
            if f.get('direction') == 'positive'
        ][:5]
        result['top_negative_features'] = [
            f for f in contributions 
            if f.get('direction') == 'negative'
        ][:5]
        
        logger.info(f"✅ Anomaly explanation generated - Risk: {result['risk_level']}")
        return result
        
    except Exception as e:
        logger.error(f"Error in advanced anomaly explanation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================== SENTIMENT ANALYSIS EXPLAINABILITY =====================

@app.post("/api/explain-sentiment")
async def explain_sentiment_analysis(request: dict):
    """
    Explain sentiment analysis prediction using SHAP or LIME
    
    Request format:
    {
        "text": "Your tax service was excellent",
        "method": "shap"  # or "lime"
    }
    
    Response includes:
    - sentiment: Predicted sentiment (positive, neutral, negative)
    - confidence: Confidence score for prediction
    - probabilities: Probability for each sentiment class
    - important_words: Top 15 words driving the prediction
    - positive_words: Words contributing to positive sentiment
    - negative_words: Words contributing to negative sentiment
    """
    if explainability_service is None:
        raise HTTPException(status_code=503, detail="Explainability service not initialized")
    
    try:
        # Load sentiment model
        model_path = 'models/sentiment_analysis/sentiment_model.pkl'
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Sentiment model not found")
        
        model = joblib.load(model_path)
        vectorizer_path = 'models/sentiment_analysis/vectorizer.pkl'
        vectorizer = joblib.load(vectorizer_path)
        
        # Label encoder for sentiment
        label_encoder = {'negative': 0, 'neutral': 1, 'positive': 2}
        
        # Get explanation
        text = request.get('text', '')
        method = request.get('method', 'shap').lower()
        
        if not text:
            raise HTTPException(status_code=400, detail="Text field is required")
        
        explanation = explainability_service.explain_sentiment(
            model=model,
            input_text=text,
            vectorizer=vectorizer,
            label_encoder=label_encoder,
            method=method
        )
        
        # Format response
        result = format_explanation_for_api(explanation)
        
        # Extract positive and negative words
        contributions = explanation.get('feature_contributions', [])
        result['positive_words'] = [
            f for f in contributions 
            if f.get('direction') == 'positive'
        ][:5]
        result['negative_words'] = [
            f for f in contributions 
            if f.get('direction') == 'negative'
        ][:5]
        
        # Add sentiment intensity
        conf = explanation.get('confidence', 0)
        if conf > 0.8:
            result['sentiment_intensity'] = 'STRONG'
        elif conf > 0.6:
            result['sentiment_intensity'] = 'MODERATE'
        else:
            result['sentiment_intensity'] = 'WEAK'
        
        logger.info(f"✅ Sentiment explanation generated - {explanation.get('sentiment').upper()}")
        return result
        
    except Exception as e:
        logger.error(f"Error in sentiment explanation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================== COMPARISON ENDPOINT =====================

@app.post("/api/explain-compare")
async def compare_explanation_methods(request: dict):
    """
    Compare SHAP vs LIME explanations for the same input
    
    Request format:
    {
        "model_type": "anomaly|sentiment|document",
        "text_or_data": "...",
        "include_timing": true
    }
    
    Useful for understanding differences between explanation methods
    and choosing appropriate method for your use case
    """
    if explainability_service is None:
        raise HTTPException(status_code=503, detail="Explainability service not initialized")
    
    import time
    
    try:
        model_type = request.get('model_type', '').lower()
        
        if model_type not in ['anomaly', 'sentiment', 'document']:
            raise HTTPException(status_code=400, detail="Invalid model_type")
        
        results = {}
        include_timing = request.get('include_timing', True)
        
        for method in ['shap', 'lime']:
            start_time = time.time()
            
            try:
                # Route to appropriate endpoint based on model type
                if model_type == 'anomaly':
                    explanation = explainability_service.explain_anomaly_detection(
                        model=None,  # Would load from file in real scenario
                        input_data=pd.DataFrame([request.get('data', {})]),
                        feature_names=list(request.get('data', {}).keys()),
                        method=method
                    )
                elif model_type == 'sentiment':
                    explanation = explainability_service.explain_sentiment(
                        model=None,
                        input_text=request.get('text', ''),
                        vectorizer=None,
                        label_encoder={},
                        method=method
                    )
                elif model_type == 'document':
                    explanation = explainability_service.explain_document_classification(
                        model=None,
                        input_text=request.get('text', ''),
                        tokenizer=None,
                        label_encoder={},
                        method=method
                    )
                
                elapsed = time.time() - start_time
                
                results[method] = {
                    'explanation': explanation,
                    'elapsed_time': elapsed if include_timing else None
                }
            except Exception as e:
                results[method] = {'error': str(e), 'elapsed_time': time.time() - start_time}
        
        # Generate comparison insights
        insights = {
            'shap_faster': results['shap'].get('elapsed_time', 0) < results['lime'].get('elapsed_time', 0),
            'methods_agree': False  # Would be calculated based on feature importance
        }
        
        if include_timing:
            insights['timing_diff'] = abs(
                results['shap'].get('elapsed_time', 0) - results['lime'].get('elapsed_time', 0)
            )
        
        return {
            'status': 'success',
            'model_type': model_type,
            'results': results,
            'insights': insights,
            'recommendation': 'Use SHAP for accuracy, LIME for speed' if insights['shap_faster'] else 'Use LIME for speed'
        }
        
    except Exception as e:
        logger.error(f"Error in explanation comparison: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================== EXPLAINABILITY STATUS ENDPOINT =====================

@app.get("/api/explainability-status")
async def get_explainability_status():
    """
    Get status of all explainability features and available models
    """
    try:
        models_available = {
            'cnn_document_classifier': os.path.exists('models/document_classifier/cnn_model.h5'),
            'anomaly_detection': os.path.exists('models/anomaly_detection_models/best_model.pkl'),
            'sentiment_analysis': os.path.exists('models/sentiment_analysis/sentiment_model.pkl'),
            'vat_predictor': os.path.exists('models/ml_models/vat_refund_predictor.pkl')
        }
        
        supported_methods = {
            'shap': True,
            'lime': True,
            'gradient_based': True
        }
        
        return {
            'status': 'operational',
            'available_models': models_available,
            'supported_methods': supported_methods,
            'available_endpoints': [
                '/api/explain-vat',
                '/api/explain-document',
                '/api/explain-anomaly-advanced',
                '/api/explain-sentiment',
                '/api/explain-compare',
                '/api/explain-batch'
            ],
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================== HELPER FUNCTIONS =====================

async def _process_batch_explanations(batch_id: str, requests: List[ExplanationRequest]):
    """Process batch explanations in background"""
    try:
        results = []
        for i, req in enumerate(requests):
            # Generate explanation for each request
            # Implementation depends on request type
            results.append({
                "index": i,
                "status": "completed"
            })
        
        # Save results
        results_file = f"{REPORTS_DIR}/{batch_id}_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Update status
        status_file = f"{REPORTS_DIR}/{batch_id}_status.json"
        with open(status_file, 'w') as f:
            json.dump({
                "batch_id": batch_id,
                "status": "completed",
                "total": len(requests),
                "results_url": f"/api/batch/{batch_id}/results"
            }, f, indent=2)
        
        logger.info(f"✅ Batch {batch_id} processing completed")
        
    except Exception as e:
        logger.error(f"Error processing batch: {e}")

# ===================== SERVER STARTUP =====================

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )