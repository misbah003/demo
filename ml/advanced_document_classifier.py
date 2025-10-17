"""
Advanced Document Classification using Deep Learning
Implements: CNN, BERT/Transformers with real training and evaluation
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

# Deep Learning
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    Dense, Dropout, Conv1D, MaxPooling1D, GlobalMaxPooling1D,
    Embedding, LSTM, Bidirectional, Input, Concatenate
)
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Transformers
try:
    from transformers import (
        AutoTokenizer, AutoModelForSequenceClassification,
        TFAutoModelForSequenceClassification, TrainingArguments, Trainer
    )
    TRANSFORMERS_AVAILABLE = True
except:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ Transformers not available. Install with: pip install transformers")

import matplotlib.pyplot as plt
import seaborn as sns
import json
import pickle


class AdvancedDocumentClassifier:
    """
    Advanced document classification system using:
    1. CNN - Convolutional Neural Network for text
    2. BERT - Transformer-based model
    3. Hybrid - CNN + LSTM combination
    """
    
    def __init__(self, max_words: int = 10000, max_len: int = 500):
        print("🚀 Initializing Advanced Document Classifier...")
        self.max_words = max_words
        self.max_len = max_len
        self.tokenizer = None
        self.models = {}
        self.metrics = {}
        self.label_encoder = {}
        self.reverse_label_encoder = {}
        
    def prepare_data(self, texts: List[str], labels: List[str]) -> Tuple:
        """
        Prepare text data for classification
        """
        print("\n📊 Preparing data...")
        
        # Encode labels
        unique_labels = sorted(list(set(labels)))
        self.label_encoder = {label: idx for idx, label in enumerate(unique_labels)}
        self.reverse_label_encoder = {idx: label for label, idx in self.label_encoder.items()}
        
        encoded_labels = [self.label_encoder[label] for label in labels]
        
        # Tokenize texts
        self.tokenizer = Tokenizer(num_words=self.max_words, oov_token='<OOV>')
        self.tokenizer.fit_on_texts(texts)
        
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=self.max_len, padding='post', truncating='post')
        
        # Convert labels to categorical
        num_classes = len(unique_labels)
        categorical_labels = keras.utils.to_categorical(encoded_labels, num_classes)
        
        print(f"✅ Data prepared:")
        print(f"   Samples: {len(texts)}")
        print(f"   Classes: {num_classes} - {unique_labels}")
        print(f"   Vocabulary size: {min(self.max_words, len(self.tokenizer.word_index))}")
        
        return padded_sequences, categorical_labels, num_classes
    
    def build_cnn_model(self, num_classes: int) -> Model:
        """
        Build CNN model for text classification
        
        CNN Architecture:
        - Embedding layer
        - Multiple Conv1D layers with different filter sizes
        - MaxPooling
        - Dense layers
        """
        print("\n🏗️ Building CNN Model...")
        
        # Input
        input_layer = Input(shape=(self.max_len,))
        
        # Embedding
        embedding = Embedding(
            input_dim=self.max_words,
            output_dim=128,
            input_length=self.max_len
        )(input_layer)
        
        # Multiple parallel Conv1D layers with different kernel sizes
        conv_blocks = []
        for kernel_size in [3, 4, 5]:
            conv = Conv1D(filters=128, kernel_size=kernel_size, activation='relu')(embedding)
            conv = MaxPooling1D(pool_size=2)(conv)
            conv = GlobalMaxPooling1D()(conv)
            conv_blocks.append(conv)
        
        # Concatenate all conv blocks
        concatenated = Concatenate()(conv_blocks)
        
        # Dense layers
        dense = Dense(128, activation='relu')(concatenated)
        dense = Dropout(0.5)(dense)
        dense = Dense(64, activation='relu')(dense)
        dense = Dropout(0.3)(dense)
        
        # Output
        output = Dense(num_classes, activation='softmax')(dense)
        
        # Create model
        model = Model(inputs=input_layer, outputs=output)
        
        # Build the model first
        model.build(input_shape=(None, self.max_len))
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ CNN Model built")
        print(f"   Total parameters: {model.count_params():,}")
        
        return model
    
    def build_hybrid_model(self, num_classes: int) -> Model:
        """
        Build Hybrid CNN-LSTM model
        
        Combines:
        - CNN for local feature extraction
        - LSTM for sequential patterns
        """
        print("\n🏗️ Building Hybrid CNN-LSTM Model...")
        
        model = Sequential([
            Embedding(self.max_words, 128, input_length=self.max_len),
            
            # CNN layers
            Conv1D(128, 5, activation='relu'),
            MaxPooling1D(pool_size=2),
            
            # LSTM layers
            Bidirectional(LSTM(64, return_sequences=True)),
            Dropout(0.3),
            Bidirectional(LSTM(32)),
            Dropout(0.3),
            
            # Dense layers
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(num_classes, activation='softmax')
        ])
        
        # Build the model first
        model.build(input_shape=(None, self.max_len))
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Hybrid Model built")
        print(f"   Total parameters: {model.count_params():,}")
        
        return model
    
    def train_model(
        self,
        model_name: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 50,
        batch_size: int = 32
    ) -> Dict:
        """
        Train a model with early stopping and checkpointing
        """
        print(f"\n🔄 Training {model_name.upper()} Model...")
        
        # Get model
        num_classes = y_train.shape[1]
        if model_name == 'cnn':
            model = self.build_cnn_model(num_classes)
        elif model_name == 'hybrid':
            model = self.build_hybrid_model(num_classes)
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Callbacks
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        )
        
        # Train
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop],
            verbose=1
        )
        
        # Store model
        self.models[model_name] = model
        
        print(f"✅ {model_name.upper()} training complete")
        
        return {
            'model': model,
            'history': history.history
        }
    
    def evaluate_model(
        self,
        model_name: str,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict:
        """
        Evaluate model with comprehensive metrics
        """
        print(f"\n📊 Evaluating {model_name.upper()} Model...")
        
        model = self.models[model_name]
        
        # Predictions
        y_pred_proba = model.predict(X_test)
        y_pred = np.argmax(y_pred_proba, axis=1)
        y_true = np.argmax(y_test, axis=1)
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, y_pred)
        
        # Classification report
        class_names = [self.reverse_label_encoder[i] for i in range(len(self.reverse_label_encoder))]
        report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        metrics = {
            'model': model_name,
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'predictions': y_pred.tolist(),
            'true_labels': y_true.tolist()
        }
        
        self.metrics[model_name] = metrics
        
        print(f"✅ {model_name.upper()} Evaluation:")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"\n   Per-class metrics:")
        for class_name in class_names:
            if class_name in report:
                print(f"   {class_name}:")
                print(f"      Precision: {report[class_name]['precision']:.4f}")
                print(f"      Recall: {report[class_name]['recall']:.4f}")
                print(f"      F1-Score: {report[class_name]['f1-score']:.4f}")
        
        return metrics
    
    def train_bert_classifier(
        self,
        texts: List[str],
        labels: List[str],
        model_name: str = "bert-base-uncased",
        epochs: int = 3
    ) -> Dict:
        """
        Train BERT-based classifier using Hugging Face Transformers
        """
        if not TRANSFORMERS_AVAILABLE:
            print("❌ Transformers library not available")
            return None
        
        print(f"\n🔄 Training BERT Classifier ({model_name})...")
        
        try:
            # Prepare labels
            unique_labels = sorted(list(set(labels)))
            label2id = {label: idx for idx, label in enumerate(unique_labels)}
            id2label = {idx: label for label, idx in label2id.items()}
            
            encoded_labels = [label2id[label] for label in labels]
            
            # Split data
            X_train, X_val, y_train, y_val = train_test_split(
                texts, encoded_labels, test_size=0.2, random_state=42
            )
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = TFAutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=len(unique_labels),
                id2label=id2label,
                label2id=label2id
            )
            
            # Tokenize
            train_encodings = tokenizer(X_train, truncation=True, padding=True, max_length=512)
            val_encodings = tokenizer(X_val, truncation=True, padding=True, max_length=512)
            
            # Create TF datasets
            train_dataset = tf.data.Dataset.from_tensor_slices((
                dict(train_encodings),
                y_train
            )).batch(8)
            
            val_dataset = tf.data.Dataset.from_tensor_slices((
                dict(val_encodings),
                y_val
            )).batch(8)
            
            # Compile
            optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
            loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
            model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
            
            # Train
            history = model.fit(
                train_dataset,
                validation_data=val_dataset,
                epochs=epochs
            )
            
            # Store
            self.models['bert'] = {
                'model': model,
                'tokenizer': tokenizer,
                'label2id': label2id,
                'id2label': id2label
            }
            
            print("✅ BERT training complete")
            
            return {
                'model': model,
                'tokenizer': tokenizer,
                'history': history.history
            }
        
        except Exception as e:
            print(f"❌ BERT training failed: {e}")
            return None
    
    def predict(self, texts: List[str], model_name: str = 'cnn') -> List[Dict]:
        """
        Predict document classes for new texts
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained")
        
        if model_name == 'bert':
            return self._predict_bert(texts)
        else:
            return self._predict_keras(texts, model_name)
    
    def _predict_keras(self, texts: List[str], model_name: str) -> List[Dict]:
        """Predict using Keras models (CNN, Hybrid)"""
        model = self.models[model_name]
        
        # Tokenize
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded = pad_sequences(sequences, maxlen=self.max_len, padding='post', truncating='post')
        
        # Predict
        predictions = model.predict(padded)
        
        results = []
        for pred in predictions:
            class_idx = np.argmax(pred)
            class_name = self.reverse_label_encoder[class_idx]
            confidence = float(pred[class_idx])
            
            results.append({
                'class': class_name,
                'confidence': confidence,
                'all_probabilities': {
                    self.reverse_label_encoder[i]: float(pred[i])
                    for i in range(len(pred))
                }
            })
        
        return results
    
    def _predict_bert(self, texts: List[str]) -> List[Dict]:
        """Predict using BERT model"""
        bert_info = self.models['bert']
        model = bert_info['model']
        tokenizer = bert_info['tokenizer']
        id2label = bert_info['id2label']
        
        # Tokenize
        encodings = tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors='tf')
        
        # Predict
        outputs = model(encodings)
        predictions = tf.nn.softmax(outputs.logits, axis=-1).numpy()
        
        results = []
        for pred in predictions:
            class_idx = np.argmax(pred)
            class_name = id2label[class_idx]
            confidence = float(pred[class_idx])
            
            results.append({
                'class': class_name,
                'confidence': confidence,
                'all_probabilities': {
                    id2label[i]: float(pred[i])
                    for i in range(len(pred))
                }
            })
        
        return results
    
    def plot_confusion_matrix(self, model_name: str, save_path: str = None):
        """Plot confusion matrix"""
        if model_name not in self.metrics:
            print(f"❌ No metrics for {model_name}")
            return
        
        cm = np.array(self.metrics[model_name]['confusion_matrix'])
        class_names = [self.reverse_label_encoder[i] for i in range(len(self.reverse_label_encoder))]
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=class_names, yticklabels=class_names)
        plt.title(f'Confusion Matrix - {model_name.upper()}', fontsize=14, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Confusion matrix saved to: {save_path}")
        
        plt.show()
    
    def save_models(self, output_dir: str = 'models/document_classifier'):
        """Save trained models"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save Keras models
        for model_name in ['cnn', 'hybrid']:
            if model_name in self.models:
                self.models[model_name].save(f'{output_dir}/{model_name}_model.h5')
        
        # Save tokenizer
        if self.tokenizer:
            with open(f'{output_dir}/tokenizer.pkl', 'wb') as f:
                pickle.dump(self.tokenizer, f)
        
        # Save label encoders
        with open(f'{output_dir}/label_encoders.json', 'w') as f:
            json.dump({
                'label_encoder': self.label_encoder,
                'reverse_label_encoder': {str(k): v for k, v in self.reverse_label_encoder.items()}
            }, f, indent=2)
        
        # Save metrics
        metrics_to_save = {}
        for model_name, metrics in self.metrics.items():
            metrics_to_save[model_name] = {
                'accuracy': metrics['accuracy'],
                'classification_report': metrics['classification_report']
            }
        
        with open(f'{output_dir}/metrics.json', 'w') as f:
            json.dump(metrics_to_save, f, indent=2)
        
        print(f"✅ Models saved to: {output_dir}")


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("ADVANCED DOCUMENT CLASSIFICATION TEST")
    print("="*60)
    
    # Generate sample data
    sample_texts = [
        "VAT Invoice INV-001 Total Amount ₹50,000 GST 18%",
        "Tax Return Form for FY 2023-24 Total Tax ₹100,000",
        "Purchase Receipt REC-123 Amount ₹25,000",
        "VAT Return GSTIN 29ABCDE1234F1Z5 Refund ₹15,000",
        "Bank Statement Account Balance ₹500,000",
        "Financial Statement Profit ₹200,000 Loss ₹50,000",
    ] * 20  # Repeat to have more samples
    
    sample_labels = [
        "VAT Invoice",
        "Tax Return",
        "Purchase Receipt",
        "VAT Return",
        "Bank Statement",
        "Financial Statement",
    ] * 20
    
    print(f"\n📊 Sample Data: {len(sample_texts)} documents")
    
    # Initialize classifier
    classifier = AdvancedDocumentClassifier()
    
    # Prepare data
    X, y, num_classes = classifier.prepare_data(sample_texts, sample_labels)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42
    )
    
    # Train CNN
    classifier.train_model('cnn', X_train, y_train, X_val, y_val, epochs=10)
    classifier.evaluate_model('cnn', X_test, y_test)
    
    # Train Hybrid
    classifier.train_model('hybrid', X_train, y_train, X_val, y_val, epochs=10)
    classifier.evaluate_model('hybrid', X_test, y_test)
    
    # Test prediction
    test_texts = [
        "VAT Invoice Total ₹75,000",
        "Tax Return Refund ₹20,000"
    ]
    
    print("\n🔮 Testing Predictions:")
    predictions = classifier.predict(test_texts, model_name='cnn')
    for text, pred in zip(test_texts, predictions):
        print(f"\nText: {text}")
        print(f"Predicted: {pred['class']} (confidence: {pred['confidence']:.4f})")
    
    # Plot confusion matrix
    classifier.plot_confusion_matrix('cnn', save_path='confusion_matrix_cnn.png')
    
    # Save models
    classifier.save_models()
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETE!")
    print("="*60)