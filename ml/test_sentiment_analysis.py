"""
Test Sentiment Analysis
Tests the trained sentiment model with sample texts
"""

import sys
from pathlib import Path
import pickle

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("🧪 TESTING SENTIMENT ANALYSIS")
print("=" * 60)
print()

# Load model
models_dir = Path(__file__).parent.parent / "models" / "sentiment_analysis"

if not models_dir.exists():
    print("❌ Model directory not found!")
    print(f"   Expected: {models_dir}")
    print()
    print("Please train the model first:")
    print("  python ml/sentiment_analysis.py")
    sys.exit(1)

print("📂 Loading model...")

# Load model
model_path = models_dir / "sentiment_model.pkl"
with open(model_path, 'rb') as f:
    model = pickle.load(f)
print(f"✅ Model loaded")

# Load vectorizer
vectorizer_path = models_dir / "vectorizer.pkl"
with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)
print(f"✅ Vectorizer loaded")

print()

# Test texts
test_texts = [
    {
        'text': 'Excellent service from tax department, refund processed very quickly and efficiently',
        'expected': 'positive'
    },
    {
        'text': 'Very satisfied with the GST filing process, smooth and user-friendly',
        'expected': 'positive'
    },
    {
        'text': 'Tax return filed for the current assessment year',
        'expected': 'neutral'
    },
    {
        'text': 'GST payment completed as per schedule',
        'expected': 'neutral'
    },
    {
        'text': 'Very disappointed with delayed tax refund processing, waited for 3 months',
        'expected': 'negative'
    },
    {
        'text': 'Poor customer service, no response to my queries for weeks',
        'expected': 'negative'
    },
    {
        'text': 'Great experience with tax portal, everything worked perfectly',
        'expected': 'positive'
    },
    {
        'text': 'Submitted required documents for tax assessment',
        'expected': 'neutral'
    },
    {
        'text': 'Frustrated with complicated tax filing procedures, very confusing',
        'expected': 'negative'
    },
    {
        'text': 'Tax refund received on time, thank you for prompt service',
        'expected': 'positive'
    }
]

print("=" * 60)
print("🔍 TESTING WITH SAMPLE TEXTS")
print("=" * 60)
print()

correct_predictions = 0
total_predictions = len(test_texts)

reverse_label_encoder = {0: 'negative', 1: 'neutral', 2: 'positive'}

for i, item in enumerate(test_texts, 1):
    print(f"Test {i}/{total_predictions}")
    print(f"Text: {item['text'][:80]}...")
    print(f"Expected: {item['expected']}")
    
    # Vectorize
    X_vec = vectorizer.transform([item['text']])
    
    # Predict
    prediction = model.predict(X_vec)[0]
    probabilities = model.predict_proba(X_vec)[0]
    
    predicted_label = reverse_label_encoder[prediction]
    confidence = probabilities[prediction]
    
    # Check if correct
    is_correct = predicted_label == item['expected']
    if is_correct:
        correct_predictions += 1
    
    status_icon = "✅" if is_correct else "❌"
    print(f"{status_icon} Predicted: {predicted_label} (confidence: {confidence:.2%})")
    
    # Show all probabilities
    print(f"   Probabilities:")
    print(f"      Negative: {probabilities[0]:.2%}")
    print(f"      Neutral: {probabilities[1]:.2%}")
    print(f"      Positive: {probabilities[2]:.2%}")
    
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

# Test with custom input
print("=" * 60)
print("💬 INTERACTIVE TESTING")
print("=" * 60)
print()
print("Enter your own text to analyze sentiment (or press Enter to skip):")
print()

try:
    user_text = input("Your text: ").strip()
    
    if user_text:
        X_vec = vectorizer.transform([user_text])
        prediction = model.predict(X_vec)[0]
        probabilities = model.predict_proba(X_vec)[0]
        predicted_label = reverse_label_encoder[prediction]
        confidence = probabilities[prediction]
        
        print()
        print(f"Sentiment: {predicted_label.upper()} (confidence: {confidence:.2%})")
        print()
        print("Probabilities:")
        print(f"  Negative: {probabilities[0]:.2%}")
        print(f"  Neutral: {probabilities[1]:.2%}")
        print(f"  Positive: {probabilities[2]:.2%}")
        print()
except:
    pass

print("=" * 60)
print("✅ TESTING COMPLETE")
print("=" * 60)