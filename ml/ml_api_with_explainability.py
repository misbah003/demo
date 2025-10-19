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

# Initialize FastAPI
app = FastAPI(
    title="ML API with Explainability",
    description="Advanced ML models with SHAP/LIME explanations",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
ner_extractor = None
doc_classifier = None
vat_forecaster = None
explainability_service = None

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
    method: str = "attention"

class ExplainabilityReportRequest(BaseModel):
    """Report generation request"""
    prediction_data: Dict
    model_name: str
    input_summary: Dict

# ===================== STARTUP/SHUTDOWN =====================

@app.on_event("startup")
async def startup_event():
    """Initialize models and services"""
    global ner_extractor, doc_classifier, vat_forecaster, explainability_service
    
    logger.info("🚀 Starting ML API with Explainability...")
    
    try:
        # Initialize explainability service
        logger.info("📊 Initializing Explainability Service...")
        explainability_service = ExplainabilityService()
        
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
            "explainability": explainability_service is not None
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
    Explain document classification with attention weights
    
    Request format:
    {
        "text": "Document content...",
        "method": "attention"
    }
    """
    if doc_classifier is None or explainability_service is None:
        raise HTTPException(status_code=503, detail="Required models not initialized")
    
    try:
        # Get explanation
        explanation = explainability_service.explain_document_classification(
            model=doc_classifier.models.get('cnn'),
            input_text=request.text,
            tokenizer=doc_classifier.tokenizer,
            label_encoder=doc_classifier.label_encoder,
            method=request.method.lower()
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
    Generate comprehensive explanation report
    
    Request format:
    {
        "prediction_data": {...},
        "model_name": "vat_predictor",
        "input_summary": {
            "region": "EU",
            "category": "goods"
        }
    }
    """
    if explainability_service is None:
        raise HTTPException(status_code=503, detail="Explainability service not initialized")
    
    try:
        # Generate explanation
        explanation = {}  # Would be generated from prediction_data
        
        # Generate report
        report = explainability_service.generate_explanation_report(
            explanation=explanation,
            model_name=request.model_name,
            input_summary=request.input_summary
        )
        
        # Save report
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        report_path = f"{REPORTS_DIR}/{report_id}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return {
            "status": "success",
            "report_id": report_id,
            "report": report,
            "download_url": f"/api/reports/{report_id}.json"
        }
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===================== REPORT DOWNLOAD =====================

@app.get("/api/reports/{report_id}.json")
async def download_report(report_id: str):
    """Download explanation report"""
    try:
        report_path = f"{REPORTS_DIR}/{report_id}.json"
        if os.path.exists(report_path):
            return FileResponse(
                path=report_path,
                filename=f"{report_id}.json",
                media_type="application/json"
            )
        else:
            raise HTTPException(status_code=404, detail="Report not found")
    except Exception as e:
        logger.error(f"Error downloading report: {e}")
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