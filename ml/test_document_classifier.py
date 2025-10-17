"""
Test Document Classifier
Tests the trained CNN model with sample documents
"""

import sys
from pathlib import Path
import pickle
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences

print("=" * 60)
print("🧪 TESTING DOCUMENT CLASSIFIER")
print("=" * 60)
print()

# Load model
models_dir = Path(__file__).parent.parent / "models" / "document_classifier"

if not models_dir.exists():
    print("❌ Model directory not found!")
    print(f"   Expected: {models_dir}")
    print()
    print("Please train the model first:")
    print("  python ml/train_document_classifier.py")
    sys.exit(1)

print("📂 Loading models...")

# Load CNN model
cnn_model_path = models_dir / "cnn_model.h5"
if cnn_model_path.exists():
    cnn_model = keras.models.load_model(cnn_model_path)
    print(f"✅ CNN model loaded: {cnn_model_path.name}")
else:
    print(f"❌ CNN model not found: {cnn_model_path}")
    cnn_model = None

# Load tokenizer
tokenizer_path = models_dir / "tokenizer.pkl"
with open(tokenizer_path, 'rb') as f:
    tokenizer = pickle.load(f)
print(f"✅ Tokenizer loaded")

# Load label encoders
label_encoder_path = models_dir / "label_encoder.pkl"
with open(label_encoder_path, 'rb') as f:
    encoders = pickle.load(f)
    label_encoder = encoders['label_encoder']
    reverse_label_encoder = encoders['reverse_label_encoder']
print(f"✅ Label encoders loaded")

print()

# Test documents
test_documents = [
    {
        'text': 'GST return filing for period Q1-2024 with total tax amount 125000 and GSTIN 29ABCDE1234F1Z5',
        'expected': 'GST Return'
    },
    {
        'text': 'Tax invoice number INV-2024-001 dated 15-Jan-2024 for amount 50000 with GST 9000',
        'expected': 'Invoice'
    },
    {
        'text': 'Purchase order PO-12345 for procurement of goods worth 75000 from supplier ABC Corp',
        'expected': 'Purchase Order'
    },
    {
        'text': 'Tax assessment order AO-2024-567 for assessment year 2023-24 with demand of 25000',
        'expected': 'Tax Assessment'
    },
    {
        'text': 'VAT return for period Jan-2024 showing sales 500000 and VAT collected 90000',
        'expected': 'VAT Return'
    },
    {
        'text': 'Income tax return filed for AY 2023-24 showing total income 800000 and tax paid 120000',
        'expected': 'Income Tax Return'
    },
    {
        'text': 'TDS certificate 16A for amount 15000 deducted at source with TAN ABCD12345E',
        'expected': 'TDS Certificate'
    },
    {
        'text': 'Balance sheet as on 31-Mar-2024 showing total assets 5000000 and liabilities 3000000',
        'expected': 'Balance Sheet'
    }
]

print("=" * 60)
print("🔍 TESTING WITH SAMPLE DOCUMENTS")
print("=" * 60)
print()

if cnn_model:
    correct_predictions = 0
    total_predictions = len(test_documents)
    
    for i, doc in enumerate(test_documents, 1):
        print(f"Test {i}/{total_predictions}")
        print(f"Text: {doc['text'][:80]}...")
        print(f"Expected: {doc['expected']}")
        
        # Tokenize and pad
        sequence = tokenizer.texts_to_sequences([doc['text']])
        padded = pad_sequences(sequence, maxlen=200, padding='post', truncating='post')
        
        # Predict
        prediction = cnn_model.predict(padded, verbose=0)
        predicted_idx = np.argmax(prediction[0])
        predicted_label = reverse_label_encoder[predicted_idx]
        confidence = prediction[0][predicted_idx]
        
        # Check if correct
        is_correct = predicted_label == doc['expected']
        if is_correct:
            correct_predictions += 1
        
        status_icon = "✅" if is_correct else "❌"
        print(f"{status_icon} Predicted: {predicted_label} (confidence: {confidence:.2%})")
        
        # Show top 3 predictions
        top_3_idx = np.argsort(prediction[0])[-3:][::-1]
        print(f"   Top 3 predictions:")
        for idx in top_3_idx:
            label = reverse_label_encoder[idx]
            conf = prediction[0][idx]
            print(f"      {label}: {conf:.2%}")
        
        print()
    
    # Summary
    accuracy = correct_predictions / total_predictions
    print("=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print()
    print(f"Total tests: {total_predictions}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.2%}")
    print()
    
    if accuracy >= 0.8:
        print("✅ Model performance: EXCELLENT")
    elif accuracy >= 0.6:
        print("⚠️ Model performance: GOOD (may need more training)")
    else:
        print("❌ Model performance: NEEDS IMPROVEMENT")
    
    print()

print("=" * 60)
print("✅ TESTING COMPLETE")
print("=" * 60)