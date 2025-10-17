"""
Advanced ML API Service
Integrates all ML models: NER, Document Classification, Time Series Forecasting
"""

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import numpy as np
import pandas as pd
from datetime import datetime
import json

# Import our advanced ML modules
from advanced_ner_extraction import AdvancedNERExtractor
from advanced_document_classifier import AdvancedDocumentClassifier
from advanced_time_series_forecasting import AdvancedVATForecaster

# Initialize FastAPI
app = FastAPI(
    title="Advanced ML API for VAT Processing",
    description="Real ML/AI system with NER, Classification, and Forecasting",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global ML models
ner_extractor = None
doc_classifier = None
vat_forecaster = None

# Request/Response Models
class TextInput(BaseModel):
    text: str

class EntityExtractionResponse(BaseModel):
    entities: Dict[str, List[Dict]]
    document_analysis: Dict
    document_type: str

class DocumentClassificationRequest(BaseModel):
    text: str

class DocumentClassificationResponse(BaseModel):
    predicted_class: str
    confidence: float
    all_probabilities: Dict[str, float]

class VATForecastRequest(BaseModel):
    amounts: List[float]
    dates: Optional[List[str]] = None
    forecast_months: int = 6

class VATForecastResponse(BaseModel):
    forecast: Dict
    metrics: Dict
    best_model: str
    confidence: float


@app.on_event("startup")
async def startup_event():
    """Initialize ML models on startup"""
    global ner_extractor, doc_classifier, vat_forecaster
    
    print("🚀 Initializing Advanced ML Models...")
    
    try:
        # Initialize NER Extractor
        print("📝 Loading NER Extractor...")
        ner_extractor = AdvancedNERExtractor()
        
        # Initialize Document Classifier
        print("📄 Loading Document Classifier...")
        doc_classifier = AdvancedDocumentClassifier()
        
        # Try to load pre-trained classifier
        try:
            import os
            if os.path.exists('models/document_classifier/cnn_model.h5'):
                from tensorflow import keras
                doc_classifier.models['cnn'] = keras.models.load_model('models/document_classifier/cnn_model.h5')
                
                # Load tokenizer and label encoders
                import pickle
                with open('models/document_classifier/tokenizer.pkl', 'rb') as f:
                    doc_classifier.tokenizer = pickle.load(f)
                
                with open('models/document_classifier/label_encoders.json', 'r') as f:
                    encoders = json.load(f)
                    doc_classifier.label_encoder = encoders['label_encoder']
                    doc_classifier.reverse_label_encoder = {
                        int(k): v for k, v in encoders['reverse_label_encoder'].items()
                    }
                
                print("✅ Pre-trained classifier loaded")
        except Exception as e:
            print(f"⚠️ No pre-trained classifier found: {e}")
        
        # Initialize VAT Forecaster
        print("📊 Loading VAT Forecaster...")
        vat_forecaster = AdvancedVATForecaster()
        
        print("✅ All ML models initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing models: {e}")
        raise


@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "message": "Advanced ML API for VAT Processing",
        "version": "2.0.0",
        "models": {
            "ner": ner_extractor is not None,
            "classifier": doc_classifier is not None,
            "forecaster": vat_forecaster is not None
        }
    }


@app.post("/api/extract-entities", response_model=EntityExtractionResponse)
async def extract_entities(input_data: TextInput):
    """
    Extract entities from document text using advanced NER
    """
    if ner_extractor is None:
        raise HTTPException(status_code=503, detail="NER model not initialized")
    
    try:
        # Extract entities
        entities = ner_extractor.extract_entities(input_data.text)
        
        # Analyze document structure
        analysis = ner_extractor.analyze_document_structure(input_data.text)
        
        # Get document type
        doc_type = analysis.get('document_type', 'Document')
        
        return EntityExtractionResponse(
            entities=entities,
            document_analysis=analysis,
            document_type=doc_type
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity extraction failed: {str(e)}")


@app.post("/api/classify-document", response_model=DocumentClassificationResponse)
async def classify_document(request: DocumentClassificationRequest):
    """
    Classify document type using deep learning
    """
    if doc_classifier is None or 'cnn' not in doc_classifier.models:
        raise HTTPException(status_code=503, detail="Classifier model not initialized")
    
    try:
        # Predict
        predictions = doc_classifier.predict([request.text], model_name='cnn')
        result = predictions[0]
        
        return DocumentClassificationResponse(
            predicted_class=result['class'],
            confidence=result['confidence'],
            all_probabilities=result['all_probabilities']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


@app.post("/api/forecast-vat", response_model=VATForecastResponse)
async def forecast_vat(request: VATForecastRequest):
    """
    Generate VAT forecast using advanced time series models (ARIMA, Prophet, LSTM)
    """
    if vat_forecaster is None:
        raise HTTPException(status_code=503, detail="Forecaster model not initialized")
    
    try:
        # Prepare data
        df = vat_forecaster.prepare_data(request.amounts, request.dates)
        
        # Check if we have enough data
        if len(df) < 6:
            raise HTTPException(
                status_code=400,
                detail="Need at least 6 data points for reliable forecasting"
            )
        
        # Split data
        train_df, test_df = vat_forecaster.train_test_split(df, test_size=0.2)
        
        # Train ensemble
        ensemble_results = vat_forecaster.train_ensemble(train_df, test_df)
        
        # Generate future forecast
        future_forecast = vat_forecaster.forecast_future(num_months=request.forecast_months)
        
        # Get best model metrics
        best_model = ensemble_results['best_model']
        best_metrics = vat_forecaster.metrics[best_model]
        
        return VATForecastResponse(
            forecast=future_forecast,
            metrics={
                'r2_score': best_metrics['r2_score'],
                'mae': best_metrics['mae'],
                'rmse': best_metrics['rmse'],
                'mape': best_metrics['mape']
            },
            best_model=best_model,
            confidence=best_metrics['r2_score']
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecasting failed: {str(e)}")


@app.post("/api/process-document")
async def process_document(text: str):
    """
    Complete document processing pipeline:
    1. Extract entities (NER)
    2. Classify document type
    3. Return structured data
    """
    try:
        # Extract entities
        entities_result = await extract_entities(TextInput(text=text))
        
        # Classify document
        classification_result = await classify_document(
            DocumentClassificationRequest(text=text)
        )
        
        return {
            "entities": entities_result.entities,
            "document_analysis": entities_result.document_analysis,
            "classification": {
                "predicted_class": classification_result.predicted_class,
                "confidence": classification_result.confidence
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")


@app.get("/api/model-info")
async def get_model_info():
    """
    Get information about loaded models
    """
    info = {
        "ner_extractor": {
            "loaded": ner_extractor is not None,
            "models": ["spaCy", "FinBERT", "Regex"] if ner_extractor else []
        },
        "document_classifier": {
            "loaded": doc_classifier is not None,
            "models": list(doc_classifier.models.keys()) if doc_classifier else [],
            "metrics": doc_classifier.metrics if doc_classifier else {}
        },
        "vat_forecaster": {
            "loaded": vat_forecaster is not None,
            "models": ["ARIMA", "Prophet", "LSTM"] if vat_forecaster else []
        }
    }
    
    return info


@app.post("/api/train-classifier")
async def train_classifier(texts: List[str], labels: List[str]):
    """
    Train document classifier with new data
    """
    if doc_classifier is None:
        raise HTTPException(status_code=503, detail="Classifier not initialized")
    
    try:
        # Prepare data
        X, y, num_classes = doc_classifier.prepare_data(texts, labels)
        
        # Split data
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=0.2, random_state=42
        )
        
        # Train CNN
        doc_classifier.train_model('cnn', X_train, y_train, X_val, y_val, epochs=20)
        
        # Evaluate
        metrics = doc_classifier.evaluate_model('cnn', X_test, y_test)
        
        # Save model
        doc_classifier.save_models()
        
        return {
            "status": "success",
            "accuracy": metrics['accuracy'],
            "message": "Classifier trained and saved successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


if __name__ == "__main__":
    print("="*60)
    print("🚀 STARTING ADVANCED ML API SERVICE")
    print("="*60)
    print("\n📡 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n" + "="*60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )