"""
Sentiment Analysis for Tax Documents and Feedback
Implements sentiment analysis using BERT/DistilBERT and traditional ML
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# Text processing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pickle

# Deep Learning
try:
    import tensorflow as tf
    from transformers import (
        AutoTokenizer, TFAutoModelForSequenceClassification,
        pipeline
    )
    TRANSFORMERS_AVAILABLE = True
except:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ Transformers not available. Install with: pip install transformers")

import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
from datetime import datetime


class TaxSentimentAnalyzer:
    """
    Sentiment Analysis for tax-related texts
    
    Supports:
    1. Traditional ML (TF-IDF + Logistic Regression/Random Forest)
    2. BERT-based models (DistilBERT, FinBERT)
    3. Pre-trained sentiment pipelines
    """
    
    def __init__(self, model_type: str = 'traditional'):
        """
        Initialize sentiment analyzer
        
        Args:
            model_type: 'traditional', 'bert', or 'finbert'
        """
        print(f"🚀 Initializing Sentiment Analyzer ({model_type})...")
        self.model_type = model_type
        self.model = None
        self.vectorizer = None
        self.label_encoder = {'negative': 0, 'neutral': 1, 'positive': 2}
        self.reverse_label_encoder = {0: 'negative', 1: 'neutral', 2: 'positive'}
        
        if model_type in ['bert', 'finbert'] and not TRANSFORMERS_AVAILABLE:
            print("⚠️ Transformers not available, falling back to traditional ML")
            self.model_type = 'traditional'
    
    def create_synthetic_sentiment_data(self, n_samples: int = 1000) -> Tuple[List[str], List[str]]:
        """
        Create synthetic sentiment data for tax-related texts
        """
        print(f"🔧 Creating {n_samples} synthetic sentiment samples...")
        
        # Positive sentiments
        positive_templates = [
            "Excellent service from tax department, refund processed quickly",
            "Very satisfied with the GST filing process, smooth and efficient",
            "Great experience with tax portal, user-friendly interface",
            "Tax refund received on time, thank you for prompt service",
            "Impressed with the quick response from tax authorities",
            "Outstanding support team, resolved my query immediately",
            "Seamless tax filing experience, highly recommend",
            "Efficient processing of documents, very professional",
            "Wonderful assistance with tax compliance, very helpful",
            "Excellent online portal, makes tax filing easy"
        ]
        
        # Neutral sentiments
        neutral_templates = [
            "Tax return filed for the current assessment year",
            "GST payment completed as per schedule",
            "Submitted required documents for tax assessment",
            "Updated business information in tax portal",
            "Received acknowledgement for tax filing",
            "Tax liability calculated based on income",
            "Compliance requirements met for this quarter",
            "Standard processing time for refund is 30 days",
            "Tax forms downloaded from official website",
            "Regular tax filing completed without issues"
        ]
        
        # Negative sentiments
        negative_templates = [
            "Very disappointed with delayed tax refund processing",
            "Poor customer service, no response to queries",
            "Frustrated with complicated tax filing procedures",
            "Unacceptable delays in processing documents",
            "Tax portal frequently crashes, very inconvenient",
            "Terrible experience with tax assessment, unfair treatment",
            "Dissatisfied with lack of communication from authorities",
            "Confusing guidelines, need better documentation",
            "Long waiting times for refund, very frustrating",
            "Unhappy with additional tax demands without proper notice"
        ]
        
        texts = []
        labels = []
        
        samples_per_class = n_samples // 3
        
        # Generate positive samples
        for i in range(samples_per_class):
            text = np.random.choice(positive_templates)
            # Add some variation
            text += f" Reference: {np.random.randint(1000, 9999)}"
            texts.append(text)
            labels.append('positive')
        
        # Generate neutral samples
        for i in range(samples_per_class):
            text = np.random.choice(neutral_templates)
            text += f" Transaction ID: {np.random.randint(10000, 99999)}"
            texts.append(text)
            labels.append('neutral')
        
        # Generate negative samples
        for i in range(samples_per_class):
            text = np.random.choice(negative_templates)
            text += f" Complaint ID: {np.random.randint(1000, 9999)}"
            texts.append(text)
            labels.append('negative')
        
        print(f"✅ Created {len(texts)} samples:")
        print(f"   Positive: {labels.count('positive')}")
        print(f"   Neutral: {labels.count('neutral')}")
        print(f"   Negative: {labels.count('negative')}")
        
        return texts, labels
    
    def train_traditional_model(
        self,
        texts: List[str],
        labels: List[str],
        model_name: str = 'logistic'
    ) -> Dict:
        """
        Train traditional ML model with TF-IDF
        """
        print(f"\n🔄 Training Traditional Model ({model_name})...")
        
        # Encode labels
        y = [self.label_encoder[label] for label in labels]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"   Training samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")
        
        # TF-IDF vectorization
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train model
        if model_name == 'logistic':
            self.model = LogisticRegression(max_iter=1000, random_state=42)
        elif model_name == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        self.model.fit(X_train_vec, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Classification report
        target_names = ['negative', 'neutral', 'positive']
        report = classification_report(y_test, y_pred, target_names=target_names, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        
        print(f"✅ Training complete!")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   Precision: {report['weighted avg']['precision']:.4f}")
        print(f"   Recall: {report['weighted avg']['recall']:.4f}")
        print(f"   F1-Score: {report['weighted avg']['f1-score']:.4f}")
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'predictions': y_pred.tolist(),
            'true_labels': y_test
        }
    
    def train_bert_model(
        self,
        texts: List[str],
        labels: List[str],
        model_name: str = 'distilbert-base-uncased',
        epochs: int = 3
    ) -> Dict:
        """
        Train BERT-based sentiment model
        """
        if not TRANSFORMERS_AVAILABLE:
            print("❌ Transformers not available")
            return None
        
        print(f"\n🔄 Training BERT Model ({model_name})...")
        
        try:
            # Encode labels
            y = [self.label_encoder[label] for label in labels]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                texts, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = TFAutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=3
            )
            
            # Tokenize
            train_encodings = tokenizer(
                X_train,
                truncation=True,
                padding=True,
                max_length=128,
                return_tensors='tf'
            )
            
            test_encodings = tokenizer(
                X_test,
                truncation=True,
                padding=True,
                max_length=128,
                return_tensors='tf'
            )
            
            # Compile
            optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
            loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
            model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
            
            # Train
            history = model.fit(
                dict(train_encodings),
                np.array(y_train),
                validation_data=(dict(test_encodings), np.array(y_test)),
                epochs=epochs,
                batch_size=16
            )
            
            # Evaluate
            results = model.evaluate(dict(test_encodings), np.array(y_test))
            accuracy = results[1]
            
            # Store model
            self.model = model
            self.tokenizer = tokenizer
            
            print(f"✅ BERT training complete!")
            print(f"   Accuracy: {accuracy:.4f}")
            
            return {
                'accuracy': accuracy,
                'history': history.history
            }
        
        except Exception as e:
            print(f"❌ BERT training failed: {e}")
            return None
    
    def predict(self, texts: List[str]) -> List[Dict]:
        """
        Predict sentiment for texts
        """
        if self.model is None:
            raise ValueError("Model not trained")
        
        if self.model_type == 'traditional':
            return self._predict_traditional(texts)
        else:
            return self._predict_bert(texts)
    
    def _predict_traditional(self, texts: List[str]) -> List[Dict]:
        """Predict using traditional ML"""
        X_vec = self.vectorizer.transform(texts)
        predictions = self.model.predict(X_vec)
        probabilities = self.model.predict_proba(X_vec)
        
        results = []
        for i, text in enumerate(texts):
            pred_label = self.reverse_label_encoder[predictions[i]]
            probs = {
                'negative': float(probabilities[i][0]),
                'neutral': float(probabilities[i][1]),
                'positive': float(probabilities[i][2])
            }
            
            results.append({
                'text': text,
                'sentiment': pred_label,
                'confidence': float(max(probabilities[i])),
                'probabilities': probs
            })
        
        return results
    
    def _predict_bert(self, texts: List[str]) -> List[Dict]:
        """Predict using BERT"""
        encodings = self.tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=128,
            return_tensors='tf'
        )
        
        outputs = self.model(dict(encodings))
        predictions = tf.nn.softmax(outputs.logits, axis=-1).numpy()
        
        results = []
        for i, text in enumerate(texts):
            pred_idx = np.argmax(predictions[i])
            pred_label = self.reverse_label_encoder[pred_idx]
            
            probs = {
                'negative': float(predictions[i][0]),
                'neutral': float(predictions[i][1]),
                'positive': float(predictions[i][2])
            }
            
            results.append({
                'text': text,
                'sentiment': pred_label,
                'confidence': float(predictions[i][pred_idx]),
                'probabilities': probs
            })
        
        return results
    
    def save_model(self, output_dir: Path):
        """Save trained model"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.model_type == 'traditional':
            # Save model
            model_path = output_dir / "sentiment_model.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            # Save vectorizer
            vectorizer_path = output_dir / "vectorizer.pkl"
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            
            print(f"✅ Model saved: {model_path}")
            print(f"✅ Vectorizer saved: {vectorizer_path}")
        
        else:
            # Save BERT model
            model_path = output_dir / "bert_sentiment_model"
            self.model.save_pretrained(model_path)
            self.tokenizer.save_pretrained(model_path)
            print(f"✅ BERT model saved: {model_path}")
        
        # Save metadata
        metadata = {
            'model_type': self.model_type,
            'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'label_encoder': self.label_encoder
        }
        
        metadata_path = output_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Metadata saved: {metadata_path}")
    
    def load_model(self, model_dir: Path):
        """Load trained model"""
        if not model_dir.exists():
            raise ValueError(f"Model directory not found: {model_dir}")
        
        # Load metadata
        metadata_path = model_dir / "metadata.json"
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        self.model_type = metadata['model_type']
        
        if self.model_type == 'traditional':
            # Load model
            model_path = model_dir / "sentiment_model.pkl"
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Load vectorizer
            vectorizer_path = model_dir / "vectorizer.pkl"
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            print(f"✅ Traditional model loaded from {model_dir}")
        
        else:
            # Load BERT model
            model_path = model_dir / "bert_sentiment_model"
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = TFAutoModelForSequenceClassification.from_pretrained(model_path)
            print(f"✅ BERT model loaded from {model_dir}")


def main():
    """
    Main training function
    """
    print("=" * 60)
    print("🚀 SENTIMENT ANALYSIS TRAINING")
    print("=" * 60)
    print()
    
    # Create synthetic data
    analyzer = TaxSentimentAnalyzer(model_type='traditional')
    texts, labels = analyzer.create_synthetic_sentiment_data(n_samples=1500)
    
    # Train traditional model
    print("\n" + "=" * 60)
    print("Training Logistic Regression Model")
    print("=" * 60)
    
    metrics_lr = analyzer.train_traditional_model(texts, labels, model_name='logistic')
    
    # Save model
    models_dir = Path(__file__).parent.parent / "models" / "sentiment_analysis"
    analyzer.save_model(models_dir)
    
    # Test predictions
    print("\n" + "=" * 60)
    print("Testing Predictions")
    print("=" * 60)
    
    test_texts = [
        "Excellent service, very satisfied with tax refund process",
        "Tax return filed successfully",
        "Very disappointed with delayed processing"
    ]
    
    predictions = analyzer.predict(test_texts)
    
    for pred in predictions:
        print(f"\nText: {pred['text']}")
        print(f"Sentiment: {pred['sentiment']} (confidence: {pred['confidence']:.4f})")
        print(f"Probabilities: {pred['probabilities']}")
    
    print("\n" + "=" * 60)
    print("✅ SENTIMENT ANALYSIS TRAINING COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Final Results:")
    print(f"   Accuracy: {metrics_lr['accuracy']:.4f}")
    print(f"\n📁 Model saved in: {models_dir}")


if __name__ == "__main__":
    main()