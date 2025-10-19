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
import lime.lime_text
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
        Explain document classification prediction using SHAP or LIME
        
        Args:
            model: Trained CNN model
            input_text: Document text
            tokenizer: Text tokenizer
            label_encoder: Class label encoder (dict or sklearn LabelEncoder)
            method: Explanation method ("shap" or "lime")
            
        Returns:
            Dictionary with explanation details
        """
        try:
            # Get prediction
            from tensorflow.keras.preprocessing.sequence import pad_sequences
            tokens = tokenizer.texts_to_sequences([input_text])
            # Use 200 as default, but try to infer from model if possible
            max_len = 200
            try:
                # Try to get from model input shape
                model_input_shape = model.input_shape
                if model_input_shape and len(model_input_shape) > 1:
                    max_len = model_input_shape[1]
            except:
                pass
            padded_tokens = pad_sequences(tokens, maxlen=max_len, padding='post', truncating='post')
            prediction = model.predict(padded_tokens, verbose=0)
            predicted_class = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_class])
            
            # Helper function to decode labels (handles both dict and sklearn encoder)
            def decode_label(class_idx):
                try:
                    if isinstance(label_encoder, dict):
                        # Try as reverse mapping dict {idx: label}
                        if class_idx in label_encoder:
                            return label_encoder[class_idx]
                        # If not found, try to find reverse mapping
                        for key, val in label_encoder.items():
                            if val == class_idx:
                                return key
                        return f"class_{class_idx}"
                    else:
                        # It's sklearn LabelEncoder
                        return label_encoder.inverse_transform([class_idx])[0]
                except Exception as e:
                    logger.debug(f"Error decoding label {class_idx}: {e}")
                    return f"class_{class_idx}"
            
            # Get explanation using selected method
            if method.lower() == "lime":
                feature_importance = self._explain_cnn_with_lime(
                    model, padded_tokens, tokenizer, input_text
                )
            else:  # Default to SHAP
                feature_importance = self._explain_cnn_with_shap(
                    model, padded_tokens, tokenizer, input_text
                )
            
            # Build all probabilities dict
            all_probabilities = {}
            for i, prob in enumerate(prediction[0]):
                class_label = decode_label(i)
                all_probabilities[class_label] = float(prob)
            
            return {
                "method": method.upper(),
                "status": "success",
                "predicted_class": decode_label(predicted_class),
                "confidence": confidence,
                "all_probabilities": all_probabilities,
                "top_tokens": feature_importance[:15],
                "explanation_method": f"Model-agnostic {method.upper()} explainability for neural networks",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Document classification explanation failed: {e}")
            import traceback
            traceback.print_exc()
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
    
    def _explain_cnn_with_lime(
        self,
        model,
        padded_tokens: np.ndarray,
        tokenizer,
        input_text: str,
        num_samples: int = 50
    ) -> List[Dict]:
        """
        Explain CNN predictions using LIME (Local Interpretable Model-agnostic Explanations)
        
        LIME creates a local linear approximation around the prediction to identify
        which tokens/features contribute most to the classification decision.
        """
        try:
            logger.info("🔍 Generating LIME explanation for CNN document classification...")
            
            # Extract unique tokens from the input text
            words = input_text.lower().split()
            word_indices = tokenizer.texts_to_sequences([input_text])[0]
            reverse_word_index = {v: k for k, v in tokenizer.word_index.items()}
            
            # Create prediction function for LIME
            def predict_fn(token_matrix):
                """Prediction function for LIME - handles perturbed token matrices"""
                predictions = []
                for sample in token_matrix:
                    # Convert binary mask back to token sequence
                    masked_tokens = padded_tokens[0] * sample[:len(padded_tokens[0])]
                    masked_tokens = masked_tokens.astype(np.int32)
                    pred = model.predict(masked_tokens.reshape(1, -1), verbose=0)[0]
                    predictions.append(pred)
                return np.array(predictions)
            
            # Create LIME explainer for tabular data (treating token positions as features)
            feature_names = [
                reverse_word_index.get(int(token), f"token_{token}")
                for token in padded_tokens[0][:len(word_indices)]
            ]
            
            explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=padded_tokens.copy(),
                feature_names=feature_names[:len(padded_tokens[0])],
                mode='classification',
                verbose=False
            )
            
            # Explain the prediction
            exp = explainer.explain_instance(
                padded_tokens[0].astype(np.float32),
                predict_fn,
                num_features=min(15, len(feature_names)),
                num_samples=num_samples
            )
            
            # Extract explanation as list of (feature, weight) pairs
            lime_features = []
            explanation_list = exp.as_list()
            
            for list_idx, (feature_name, weight) in enumerate(explanation_list):
                # Clean up feature name
                token_text = feature_name.replace(" <= ", "").replace(" > ", "").strip()
                
                # Try to extract token index from feature name
                try:
                    # Feature name format is usually "token_value"
                    token_idx = int(token_text) if token_text.isdigit() else list_idx
                except (ValueError, AttributeError):
                    token_idx = list_idx
                
                # Get actual token word if available
                if token_idx < len(padded_tokens[0]):
                    token_id = int(padded_tokens[0][token_idx])
                    if token_id > 0:
                        actual_word = reverse_word_index.get(token_id, token_text)
                    else:
                        actual_word = "[PAD]"
                else:
                    actual_word = token_text
                
                lime_features.append({
                    "token": actual_word,
                    "position": token_idx,
                    "weight": float(weight),
                    "importance": float(abs(weight)),
                    "contribution": "positive" if weight > 0 else "negative"
                })
            
            # Sort by importance
            lime_features.sort(key=lambda x: x["importance"], reverse=True)
            
            logger.info(f"✅ LIME explanation generated with {len(lime_features)} important tokens")
            return lime_features
            
        except Exception as e:
            logger.error(f"❌ LIME explanation failed: {e}")
            return self._get_gradient_based_importance(model, padded_tokens, tokenizer)
    
    def _explain_cnn_with_shap(
        self,
        model,
        padded_tokens: np.ndarray,
        tokenizer,
        input_text: str,
        num_samples: int = 50
    ) -> List[Dict]:
        """
        Explain CNN predictions using SHAP (Shapley Additive exPlanations)
        
        SHAP uses Shapley values from game theory to provide a unified measure of feature
        importance that fairly distributes the prediction among all input tokens.
        Uses KernelExplainer for model-agnostic neural network explanations.
        """
        try:
            logger.info("🔍 Generating SHAP explanation for CNN document classification...")
            
            # Extract token words
            word_indices = tokenizer.texts_to_sequences([input_text])[0]
            reverse_word_index = {v: k for k, v in tokenizer.word_index.items()}
            
            # Create background data (reference dataset)
            background_data = np.zeros((min(50, num_samples), padded_tokens.shape[1]))
            
            # Create prediction function that returns probabilities
            def model_predict(x):
                """Wrapper for model predictions"""
                preds = model.predict(x.astype(np.int32), verbose=0)
                return preds
            
            # Initialize KernelExplainer (model-agnostic)
            explainer = shap.KernelExplainer(
                model=model_predict,
                data=background_data,
                link="logit"
            )
            
            # Calculate SHAP values
            shap_values = explainer.shap_values(padded_tokens.astype(np.float32))
            
            # Handle multi-class output - use the predicted class
            if isinstance(shap_values, list):
                predicted_class = np.argmax(model.predict(padded_tokens, verbose=0)[0])
                shap_values = shap_values[predicted_class]
            
            # Ensure shap_values is 1D
            if isinstance(shap_values, np.ndarray):
                if len(shap_values.shape) > 1:
                    shap_values = shap_values[0]
                shap_values = shap_values.flatten()
            
            # Extract feature importance
            shap_features = []
            shap_values_len = len(shap_values) if hasattr(shap_values, '__len__') else 1
            
            for token_idx in range(min(len(padded_tokens[0]), shap_values_len)):
                token_id = int(padded_tokens[0][token_idx])
                if token_id > 0:  # Skip padding (0 values)
                    actual_word = reverse_word_index.get(token_id, f"token_{token_id}")
                    try:
                        shap_value = float(shap_values[token_idx])
                    except (IndexError, TypeError):
                        shap_value = 0.0
                    
                    shap_features.append({
                        "token": actual_word,
                        "position": token_idx,
                        "shap_value": shap_value,
                        "importance": float(abs(shap_value)),
                        "contribution": "positive" if shap_value > 0 else "negative"
                    })
            
            # Sort by importance
            shap_features.sort(key=lambda x: x["importance"], reverse=True)
            
            logger.info(f"✅ SHAP explanation generated with {len(shap_features)} important tokens")
            return shap_features
            
        except Exception as e:
            logger.error(f"❌ SHAP explanation failed: {e}")
            return self._get_gradient_based_importance(model, padded_tokens, tokenizer)
    
    def _get_gradient_based_importance(
        self,
        model,
        padded_tokens: np.ndarray,
        tokenizer
    ) -> List[Dict]:
        """
        Fallback: Use gradient-based attribution to identify important tokens
        
        This method computes the gradient of the model output with respect to the
        embedding layer to identify which tokens have the strongest influence on
        the prediction.
        """
        try:
            logger.info("🔍 Using gradient-based importance extraction (fallback)...")
            
            import tensorflow as tf
            
            # Convert to TensorFlow tensor
            input_tensor = tf.convert_to_tensor(padded_tokens, dtype=tf.int32)
            
            # Watch the input for gradient computation
            with tf.GradientTape() as tape:
                # Convert input to float for embedding
                input_float = tf.cast(input_tensor, tf.float32)
                tape.watch(input_float)
                
                # Get model output
                output = model(input_tensor)
            
            # Compute gradients (simplified - uses input directly)
            gradients = tape.gradient(output, input_float)
            
            if gradients is not None:
                # Sum across all output dimensions and get absolute values
                importance_scores = np.abs(np.mean(gradients.numpy()[0], axis=1))
            else:
                # Fallback to simple frequency-based importance
                importance_scores = np.bincount(
                    padded_tokens[0],
                    minlength=len(padded_tokens[0])
                )
            
            reverse_word_index = {v: k for k, v in tokenizer.word_index.items()}
            
            # Create feature list
            gradient_features = []
            for token_idx in range(len(padded_tokens[0])):
                token_id = int(padded_tokens[0][token_idx])
                if token_id > 0:  # Skip padding
                    actual_word = reverse_word_index.get(token_id, f"token_{token_id}")
                    importance = float(importance_scores[token_idx])
                    
                    gradient_features.append({
                        "token": actual_word,
                        "position": token_idx,
                        "importance": importance,
                        "contribution": "influential"
                    })
            
            # Sort by importance
            gradient_features.sort(key=lambda x: x["importance"], reverse=True)
            
            logger.info(f"✅ Gradient-based importance extracted for {len(gradient_features)} tokens")
            return gradient_features
            
        except Exception as e:
            logger.error(f"❌ Gradient-based explanation failed: {e}")
            return []
    
    # ===================== ANOMALY DETECTION EXPLANATIONS =====================
    
    def explain_anomaly_detection(
        self,
        model,
        input_data: pd.DataFrame,
        feature_names: List[str],
        method: str = "shap"
    ) -> Dict:
        """
        Explain anomaly detection predictions using SHAP or LIME
        
        Args:
            model: Trained Random Forest or Isolation Forest model
            input_data: Single row DataFrame with features
            feature_names: List of feature names
            method: "shap" or "lime"
            
        Returns:
            Dictionary with explanation details
        """
        try:
            if method.lower() == "lime":
                return self._explain_anomaly_with_lime(model, input_data, feature_names)
            else:
                return self._explain_anomaly_with_shap(model, input_data, feature_names)
        except Exception as e:
            logger.error(f"❌ Anomaly explanation failed: {e}")
            return {"error": str(e), "method": method, "status": "failed"}
    
    def _explain_anomaly_with_shap(
        self,
        model,
        input_data: pd.DataFrame,
        feature_names: List[str]
    ) -> Dict:
        """SHAP explanation for anomaly detection"""
        try:
            logger.info("🔍 Generating SHAP explanation for anomaly detection...")
            
            # Create SHAP explainer
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(input_data)
            
            # Handle array structure
            if isinstance(shap_values, list):
                shap_values = shap_values[0]
            if isinstance(shap_values, np.ndarray) and len(shap_values.shape) > 1:
                shap_values = shap_values[0]
            
            # Get prediction
            prediction = model.predict(input_data)[0]
            anomaly_score = float(model.predict_proba(input_data)[0, 1]) if hasattr(model, 'predict_proba') else float(prediction)
            
            # Feature contributions
            feature_contributions = []
            for i, feature_name in enumerate(feature_names):
                if i < len(shap_values):
                    shap_val = float(shap_values[i])
                    feature_contributions.append({
                        "feature": feature_name,
                        "shap_value": shap_val,
                        "importance": float(abs(shap_val)),
                        "value": float(input_data.iloc[0, i]),
                        "direction": "positive" if shap_val > 0 else "negative"
                    })
            
            # Sort by importance
            feature_contributions.sort(key=lambda x: x["importance"], reverse=True)
            
            # Identify if anomalous
            is_anomaly = prediction == 1 if isinstance(prediction, (int, np.integer)) else prediction > 0.5
            
            logger.info(f"✅ SHAP anomaly explanation with {len(feature_contributions)} features")
            return {
                "method": "SHAP",
                "status": "success",
                "prediction": int(prediction),
                "anomaly_score": anomaly_score,
                "is_anomaly": bool(is_anomaly),
                "feature_contributions": feature_contributions[:15],  # Top 15 features
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ SHAP anomaly explanation failed: {e}")
            raise
    
    def _explain_anomaly_with_lime(
        self,
        model,
        input_data: pd.DataFrame,
        feature_names: List[str],
        num_samples: int = 100
    ) -> Dict:
        """LIME explanation for anomaly detection"""
        try:
            logger.info("🔍 Generating LIME explanation for anomaly detection...")
            
            # Create LIME explainer
            explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=input_data.values,
                feature_names=feature_names,
                mode='classification',
                class_names=['Normal', 'Anomaly'],
                verbose=False
            )
            
            # Predict function wrapper
            def predict_proba(x):
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(x)
                else:
                    pred = model.predict(x)
                    proba = np.column_stack([1 - pred, pred])
                return proba
            
            # Explain
            exp = explainer.explain_instance(
                input_data.iloc[0].values,
                predict_proba,
                num_features=len(feature_names),
                num_samples=num_samples
            )
            
            # Extract features
            feature_weights = {}
            for feature_name, weight in exp.as_list():
                feature_weights[feature_name] = weight
            
            # Get prediction
            prediction = model.predict(input_data)[0]
            anomaly_score = float(model.predict_proba(input_data)[0, 1]) if hasattr(model, 'predict_proba') else float(prediction)
            is_anomaly = prediction == 1 if isinstance(prediction, (int, np.integer)) else prediction > 0.5
            
            # Prepare feature contributions
            feature_contributions = []
            for i, feature_name in enumerate(feature_names):
                weight = feature_weights.get(f"{feature_name} <= {input_data.iloc[0, i]:.2f}", 
                                            feature_weights.get(feature_name, 0.0))
                feature_contributions.append({
                    "feature": feature_name,
                    "lime_weight": float(weight),
                    "importance": float(abs(weight)),
                    "value": float(input_data.iloc[0, i]),
                    "direction": "positive" if weight > 0 else "negative"
                })
            
            feature_contributions.sort(key=lambda x: x["importance"], reverse=True)
            
            logger.info(f"✅ LIME anomaly explanation with {len(feature_contributions)} features")
            return {
                "method": "LIME",
                "status": "success",
                "prediction": int(prediction),
                "anomaly_score": anomaly_score,
                "is_anomaly": bool(is_anomaly),
                "feature_contributions": feature_contributions[:15],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ LIME anomaly explanation failed: {e}")
            raise
    
    # ===================== SENTIMENT ANALYSIS EXPLANATIONS =====================
    
    def explain_sentiment(
        self,
        model,
        input_text: str,
        vectorizer,
        label_encoder: Dict,
        method: str = "shap"
    ) -> Dict:
        """
        Explain sentiment analysis prediction using SHAP or LIME
        
        Args:
            model: Trained sentiment classifier
            input_text: Text to analyze
            vectorizer: TF-IDF or similar vectorizer
            label_encoder: Dict mapping labels to indices
            method: "shap" or "lime"
            
        Returns:
            Dictionary with explanation details
        """
        try:
            if method.lower() == "lime":
                return self._explain_sentiment_with_lime(model, input_text, vectorizer, label_encoder)
            else:
                return self._explain_sentiment_with_shap(model, input_text, vectorizer, label_encoder)
        except Exception as e:
            logger.error(f"❌ Sentiment explanation failed: {e}")
            return {"error": str(e), "method": method, "status": "failed"}
    
    def _explain_sentiment_with_shap(
        self,
        model,
        input_text: str,
        vectorizer,
        label_encoder: Dict
    ) -> Dict:
        """SHAP explanation for sentiment analysis"""
        try:
            logger.info("🔍 Generating SHAP explanation for sentiment...")
            
            # Vectorize text
            text_vec = vectorizer.transform([input_text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Create SHAP explainer
            explainer = shap.TreeExplainer(model) if hasattr(model, 'tree_') else shap.KernelExplainer(
                lambda x: model.predict_proba(x),
                vectorizer.transform([" ".join([w for _ in range(5)]) for w in feature_names[:100]])
            )
            
            shap_values = explainer.shap_values(text_vec)
            
            # Handle structure
            if isinstance(shap_values, list):
                shap_values = shap_values[0] if len(shap_values) > 0 else shap_values
            if isinstance(shap_values, np.ndarray) and len(shap_values.shape) > 1:
                shap_values = shap_values[0]
            
            # Prediction
            prediction = model.predict(text_vec)[0]
            prediction_proba = model.predict_proba(text_vec)[0]
            
            # Reverse label encoder
            reverse_labels = {v: k for k, v in label_encoder.items()}
            sentiment = reverse_labels.get(prediction, 'unknown')
            confidence = float(max(prediction_proba))
            
            # Feature contributions
            feature_contributions = []
            for i, feature_name in enumerate(feature_names):
                if i < len(shap_values):
                    shap_val = float(shap_values[i])
                    if text_vec[0, i] > 0:  # Only include features present in text
                        feature_contributions.append({
                            "feature": feature_name,
                            "shap_value": shap_val,
                            "importance": float(abs(shap_val)),
                            "value": float(text_vec[0, i]),
                            "direction": "positive" if shap_val > 0 else "negative"
                        })
            
            feature_contributions.sort(key=lambda x: x["importance"], reverse=True)
            
            logger.info(f"✅ SHAP sentiment explanation with {len(feature_contributions)} words")
            return {
                "method": "SHAP",
                "status": "success",
                "sentiment": sentiment,
                "confidence": confidence,
                "probabilities": {
                    reverse_labels.get(i, f"class_{i}"): float(p)
                    for i, p in enumerate(prediction_proba)
                },
                "feature_contributions": feature_contributions[:15],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ SHAP sentiment explanation failed: {e}")
            raise
    
    def _explain_sentiment_with_lime(
        self,
        model,
        input_text: str,
        vectorizer,
        label_encoder: Dict,
        num_samples: int = 100
    ) -> Dict:
        """LIME explanation for sentiment analysis"""
        try:
            logger.info("🔍 Generating LIME explanation for sentiment...")
            
            # Vectorize text
            text_vec = vectorizer.transform([input_text])
            feature_names = list(vectorizer.get_feature_names_out())
            
            # Reverse label encoder
            reverse_labels = {v: k for k, v in label_encoder.items()}
            
            # Create LIME explainer
            explainer = lime.lime_text.LimeTextExplainer(
                class_names=list(reverse_labels.values()),
                verbose=False
            )
            
            # Prediction wrapper
            def predict_proba(texts):
                vectorized = vectorizer.transform(texts)
                return model.predict_proba(vectorized)
            
            # Explain
            exp = explainer.explain_instance(
                input_text,
                predict_proba,
                num_features=20,
                num_samples=num_samples
            )
            
            # Extract features
            feature_weights = dict(exp.as_list())
            
            # Prediction
            prediction = model.predict(text_vec)[0]
            prediction_proba = model.predict_proba(text_vec)[0]
            sentiment = reverse_labels.get(prediction, 'unknown')
            confidence = float(max(prediction_proba))
            
            # Feature contributions
            feature_contributions = []
            for word, weight in exp.as_list():
                feature_contributions.append({
                    "feature": word,
                    "lime_weight": float(weight),
                    "importance": float(abs(weight)),
                    "direction": "positive" if weight > 0 else "negative"
                })
            
            feature_contributions.sort(key=lambda x: x["importance"], reverse=True)
            
            logger.info(f"✅ LIME sentiment explanation with {len(feature_contributions)} words")
            return {
                "method": "LIME",
                "status": "success",
                "sentiment": sentiment,
                "confidence": confidence,
                "probabilities": {
                    reverse_labels.get(i, f"class_{i}"): float(p)
                    for i, p in enumerate(prediction_proba)
                },
                "feature_contributions": feature_contributions[:15],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ LIME sentiment explanation failed: {e}")
            raise
    
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