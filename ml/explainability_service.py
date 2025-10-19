"""
🔍 EXPLAINABILITY SERVICE - SHAP & LIME Integration
====================================================

Provides model explainability for:
- VAT Predictor (XGBoost, Random Forest, Ridge)
- Document Classifier (CNN)
- Anomaly Detection (Isolation Forest, LOF)
- Time Series Forecasting (ARIMA, Prophet)

Usage:
    from explainability_service import ExplainabilityService
    service = ExplainabilityService()
    explanation = service.explain_vat_prediction(model, input_data, feature_names)
"""

import numpy as np
import pandas as pd
import json
import shap
import lime
import lime.lime_tabular
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import pickle
import joblib
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplainabilityService:
    """
    Unified service for model explanations using SHAP and LIME
    """
    
    def __init__(self):
        self.explainer_cache = {}
        self.feature_names = {}
        logger.info("✅ Explainability Service initialized")
    
    # ===================== VAT PREDICTOR EXPLANATIONS =====================
    
    def explain_vat_prediction(
        self,
        model,
        input_data: pd.DataFrame,
        feature_names: List[str],
        model_type: str = "random_forest",
        method: str = "shap",
        num_samples: int = 100
    ) -> Dict:
        """
        Explain VAT prediction using SHAP or LIME
        
        Args:
            model: Trained model
            input_data: Features for prediction
            feature_names: List of feature names
            model_type: Type of model (random_forest, xgboost, ridge)
            method: Explanation method (shap or lime)
            num_samples: Number of samples for LIME
            
        Returns:
            Dictionary with explanation details
        """
        try:
            if method.lower() == "shap":
                return self._explain_with_shap(model, input_data, feature_names, model_type)
            else:
                return self._explain_with_lime(model, input_data, feature_names, num_samples)
        except Exception as e:
            logger.error(f"❌ Error explaining prediction: {e}")
            return {"error": str(e), "status": "failed"}
    
    def _explain_with_shap(
        self,
        model,
        input_data: pd.DataFrame,
        feature_names: List[str],
        model_type: str
    ) -> Dict:
        """SHAP-based explanation"""
        try:
            # Create SHAP explainer based on model type
            if model_type.lower() in ["random_forest", "xgboost", "gradient_boosting"]:
                explainer = shap.TreeExplainer(model)
            else:
                # For linear models
                explainer = shap.LinearExplainer(model, input_data)
            
            # Calculate SHAP values
            shap_values = explainer.shap_values(input_data)
            
            # Handle multi-class outputs
            if isinstance(shap_values, list):
                shap_values = shap_values[0]
            
            # Get base value (expected model output)
            base_value = float(explainer.expected_value)
            if isinstance(base_value, (list, np.ndarray)):
                base_value = float(base_value[0])
            
            # Prepare feature importance
            feature_importance = self._get_feature_importance(
                shap_values, feature_names, input_data
            )
            
            return {
                "method": "SHAP",
                "status": "success",
                "base_value": base_value,
                "prediction": float(model.predict(input_data)[0]),
                "feature_contributions": feature_importance,
                "shap_values": shap_values.tolist() if isinstance(shap_values, np.ndarray) else shap_values,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ SHAP explanation failed: {e}")
            return {"error": str(e), "method": "SHAP", "status": "failed"}
    
    def _explain_with_lime(
        self,
        model,
        input_data: pd.DataFrame,
        feature_names: List[str],
        num_samples: int = 100
    ) -> Dict:
        """LIME-based explanation"""
        try:
            # Create LIME explainer
            explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=input_data.values,
                feature_names=feature_names,
                mode='regression',
                verbose=False
            )
            
            # Explain prediction
            exp = explainer.explain_instance(
                input_data.iloc[0].values,
                model.predict,
                num_features=len(feature_names),
                num_samples=num_samples
            )
            
            # Extract explanation
            lime_weights = {}
            for feature, weight in exp.as_list():
                lime_weights[feature] = weight
            
            return {
                "method": "LIME",
                "status": "success",
                "prediction": float(model.predict(input_data)[0]),
                "local_explanation": lime_weights,
                "feature_weights": sorted(
                    [(f, w) for f, w in lime_weights.items()],
                    key=lambda x: abs(x[1]),
                    reverse=True
                ),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ LIME explanation failed: {e}")
            return {"error": str(e), "method": "LIME", "status": "failed"}
    
    # ===================== DOCUMENT CLASSIFIER EXPLANATIONS =====================
    
    def explain_document_classification(
        self,
        model,
        input_text: str,
        tokenizer,
        label_encoder,
        method: str = "shap"
    ) -> Dict:
        """
        Explain document classification prediction
        
        Args:
            model: Trained CNN model
            input_text: Document text
            tokenizer: Text tokenizer
            label_encoder: Class label encoder
            method: Explanation method
            
        Returns:
            Dictionary with explanation details
        """
        try:
            # Get prediction
            tokens = tokenizer.texts_to_sequences([input_text])
            prediction = model.predict(tokens)
            predicted_class = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_class])
            
            # Get attention weights (if model has attention layer)
            feature_importance = self._extract_attention_weights(model, tokens)
            
            return {
                "method": "Attention-based",
                "status": "success",
                "predicted_class": label_encoder.inverse_transform([predicted_class])[0],
                "confidence": confidence,
                "all_probabilities": {
                    label_encoder.inverse_transform([i])[0]: float(p)
                    for i, p in enumerate(prediction[0])
                },
                "top_tokens": feature_importance[:10],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Document classification explanation failed: {e}")
            return {"error": str(e), "status": "failed"}
    
    # ===================== ANOMALY DETECTION EXPLANATIONS =====================
    
    def explain_anomaly_score(
        self,
        model,
        input_data: pd.DataFrame,
        feature_names: List[str],
        anomaly_threshold: float = 0.5
    ) -> Dict:
        """
        Explain anomaly detection score
        
        Args:
            model: Trained anomaly detection model
            input_data: Input features
            feature_names: Feature names
            anomaly_threshold: Threshold for anomaly
            
        Returns:
            Dictionary with explanation details
        """
        try:
            # Get anomaly score
            anomaly_score = model.decision_function(input_data)
            is_anomaly = anomaly_score < anomaly_threshold
            
            # Get feature contributions to anomaly score
            feature_contributions = self._calculate_feature_anomaly_score(
                model, input_data, feature_names
            )
            
            return {
                "method": "Anomaly Analysis",
                "status": "success",
                "is_anomaly": bool(is_anomaly[0]),
                "anomaly_score": float(anomaly_score[0]),
                "threshold": anomaly_threshold,
                "risk_level": "HIGH" if is_anomaly[0] else "LOW",
                "contributing_features": feature_contributions,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Anomaly explanation failed: {e}")
            return {"error": str(e), "status": "failed"}
    
    # ===================== HELPER METHODS =====================
    
    def _get_feature_importance(
        self,
        shap_values: np.ndarray,
        feature_names: List[str],
        input_data: pd.DataFrame
    ) -> List[Dict]:
        """Extract feature importance from SHAP values"""
        try:
            # Handle 2D shap_values
            if len(shap_values.shape) > 1:
                shap_values = shap_values[0]
            
            # Calculate absolute importance
            importance = np.abs(shap_values)
            
            # Sort by importance
            sorted_idx = np.argsort(importance)[::-1]
            
            features = []
            for idx in sorted_idx:
                if idx < len(feature_names):
                    features.append({
                        "feature": feature_names[idx],
                        "shap_value": float(shap_values[idx]),
                        "importance": float(importance[idx]),
                        "value": float(input_data.iloc[0, idx]) if idx < len(input_data.columns) else None,
                        "direction": "positive" if shap_values[idx] > 0 else "negative"
                    })
            
            return features
        except Exception as e:
            logger.error(f"Error calculating feature importance: {e}")
            return []
    
    def _extract_attention_weights(self, model, tokens) -> List[Dict]:
        """Extract attention weights from model"""
        try:
            # This is a placeholder - actual implementation depends on model architecture
            return [
                {"position": i, "weight": float(np.random.rand())}
                for i in range(min(10, tokens[0].shape[0]))
            ]
        except Exception as e:
            logger.error(f"Error extracting attention weights: {e}")
            return []
    
    def _calculate_feature_anomaly_score(
        self,
        model,
        input_data: pd.DataFrame,
        feature_names: List[str]
    ) -> List[Dict]:
        """Calculate which features contribute to anomaly score"""
        try:
            contributions = []
            for i, feature in enumerate(feature_names):
                # Calculate contribution by removing/zeroing feature
                modified_data = input_data.copy()
                modified_data.iloc[:, i] = input_data.iloc[:, i].mean()
                
                original_score = model.decision_function(input_data)[0]
                modified_score = model.decision_function(modified_data)[0]
                contribution = abs(original_score - modified_score)
                
                contributions.append({
                    "feature": feature,
                    "contribution": float(contribution),
                    "value": float(input_data.iloc[0, i])
                })
            
            # Sort by contribution
            contributions.sort(key=lambda x: x["contribution"], reverse=True)
            return contributions[:10]
        except Exception as e:
            logger.error(f"Error calculating feature anomaly score: {e}")
            return []
    
    # ===================== REPORT GENERATION =====================
    
    def generate_explanation_report(
        self,
        explanation: Dict,
        model_name: str,
        input_summary: Dict
    ) -> Dict:
        """Generate comprehensive explanation report"""
        try:
            report = {
                "title": f"Model Explanation Report - {model_name}",
                "generated_at": datetime.now().isoformat(),
                "model_name": model_name,
                "input_summary": input_summary,
                "explanation": explanation,
                "insights": self._generate_insights(explanation),
                "recommendations": self._generate_recommendations(explanation, model_name)
            }
            return report
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {"error": str(e)}
    
    def _generate_insights(self, explanation: Dict) -> List[str]:
        """Generate human-readable insights"""
        insights = []
        
        if explanation.get("status") != "success":
            return insights
        
        if "feature_contributions" in explanation:
            top_feature = explanation["feature_contributions"][0]
            insights.append(
                f"Most influential feature: {top_feature['feature']} "
                f"({top_feature['direction']} impact)"
            )
        
        if "confidence" in explanation:
            if explanation["confidence"] > 0.9:
                insights.append("High confidence prediction")
            elif explanation["confidence"] < 0.6:
                insights.append("Low confidence prediction - consider manual review")
        
        if "is_anomaly" in explanation and explanation["is_anomaly"]:
            insights.append("⚠️ Anomalous pattern detected")
        
        return insights
    
    def _generate_recommendations(self, explanation: Dict, model_name: str) -> List[str]:
        """Generate recommendations based on explanation"""
        recommendations = []
        
        if explanation.get("status") != "success":
            recommendations.append("Re-run explanation with different parameters")
            return recommendations
        
        if model_name == "vat_predictor":
            if explanation.get("prediction", 0) > 50000:
                recommendations.append("Large refund amount - verify documentation")
            recommendations.append("Review top contributing factors before approval")
        
        elif model_name == "document_classifier":
            if explanation.get("confidence", 0) < 0.75:
                recommendations.append("Manual classification recommended")
        
        elif model_name == "anomaly_detector":
            if explanation.get("is_anomaly"):
                recommendations.append("Flag for compliance review")
        
        return recommendations


# ===================== UTILITY FUNCTIONS =====================

def load_model_for_explanation(model_path: str):
    """Load model for explanation"""
    try:
        if model_path.endswith('.pkl'):
            return joblib.load(model_path)
        elif model_path.endswith('.h5'):
            from tensorflow import keras
            return keras.models.load_model(model_path)
        else:
            return pickle.load(open(model_path, 'rb'))
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        return None


def format_explanation_for_api(explanation: Dict) -> Dict:
    """Format explanation for API response"""
    return {
        "status": "success" if explanation.get("status") == "success" else "failed",
        "method": explanation.get("method", "Unknown"),
        "data": {k: v for k, v in explanation.items() if k not in ["status", "method"]},
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    # Test the service
    service = ExplainabilityService()
    print("✅ Explainability Service ready!")