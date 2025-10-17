"""
Train Document Classifier (CNN) for Tax Documents
Implements CNN model for classifying tax documents into categories
"""

import numpy as np
import pandas as pd
import os
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import the advanced document classifier
from advanced_document_classifier import AdvancedDocumentClassifier

def load_training_data():
    """
    Load training data from Excel files
    """
    print("📂 Loading training data...")
    
    # Try to load from AI_Tax_Intelligence_Large.xlsx
    data_path = Path(__file__).parent.parent / "data" / "AI_Tax_Intelligence_Large.xlsx"
    
    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        return None, None
    
    try:
        df = pd.read_excel(data_path)
        print(f"✅ Loaded {len(df)} records from {data_path.name}")
        print(f"   Columns: {list(df.columns)}")
        
        # Check what columns we have
        if 'Document_Type' in df.columns or 'Category' in df.columns:
            # Use Document_Type or Category as labels
            label_col = 'Document_Type' if 'Document_Type' in df.columns else 'Category'
            
            # Create text from available columns
            text_columns = []
            for col in ['Description', 'Business_Type', 'Category', 'Filing_Status', 'Region']:
                if col in df.columns:
                    text_columns.append(col)
            
            if not text_columns:
                print("❌ No text columns found for training")
                return None, None
            
            # Combine text columns
            df['text'] = df[text_columns].fillna('').astype(str).agg(' '.join, axis=1)
            
            texts = df['text'].tolist()
            labels = df[label_col].tolist()
            
            print(f"✅ Prepared {len(texts)} text samples")
            print(f"   Label distribution:")
            label_counts = pd.Series(labels).value_counts()
            for label, count in label_counts.items():
                print(f"      {label}: {count}")
            
            return texts, labels
        else:
            print("❌ No suitable label column found (Document_Type or Category)")
            return None, None
            
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None, None


def create_synthetic_document_data():
    """
    Create synthetic tax document data for training
    """
    print("🔧 Creating synthetic document data...")
    
    # Document types
    doc_types = [
        'GST Return',
        'Invoice',
        'Purchase Order',
        'Tax Assessment',
        'VAT Return',
        'Income Tax Return',
        'TDS Certificate',
        'Balance Sheet'
    ]
    
    # Sample texts for each document type
    templates = {
        'GST Return': [
            'GST return filing for period {} with total tax amount {} and GSTIN {}',
            'Monthly GST return submission showing input tax credit {} and output tax {}',
            'GST-3B return filed with tax liability {} for the month of {}'
        ],
        'Invoice': [
            'Tax invoice number {} dated {} for amount {} with GST {}',
            'Commercial invoice for goods worth {} including GST {} issued to {}',
            'Service invoice {} with taxable value {} and GST amount {}'
        ],
        'Purchase Order': [
            'Purchase order {} for procurement of goods worth {} from supplier {}',
            'PO number {} dated {} for materials costing {} plus applicable taxes',
            'Purchase requisition {} approved for amount {} with delivery date {}'
        ],
        'Tax Assessment': [
            'Tax assessment order {} for assessment year {} with demand of {}',
            'Income tax assessment completed showing total income {} and tax payable {}',
            'Assessment notice {} issued for discrepancy in return of {}'
        ],
        'VAT Return': [
            'VAT return for period {} showing sales {} and VAT collected {}',
            'Value Added Tax filing with input VAT {} and output VAT {}',
            'Monthly VAT return submission with net tax liability of {}'
        ],
        'Income Tax Return': [
            'Income tax return filed for AY {} showing total income {} and tax paid {}',
            'ITR-{} submitted with gross total income {} and deductions {}',
            'Tax return acknowledgement {} for income {} and refund due {}'
        ],
        'TDS Certificate': [
            'TDS certificate {} for amount {} deducted at source with TAN {}',
            'Form 16A issued for TDS {} on payment {} to PAN {}',
            'Tax deduction certificate showing TDS {} deposited on {}'
        ],
        'Balance Sheet': [
            'Balance sheet as on {} showing total assets {} and liabilities {}',
            'Financial statement with equity {} debt {} and reserves {}',
            'Annual balance sheet dated {} with net worth {} and profit {}'
        ]
    }
    
    texts = []
    labels = []
    
    # Generate 1000 samples (125 per category)
    samples_per_category = 125
    
    for doc_type in doc_types:
        for i in range(samples_per_category):
            template = np.random.choice(templates[doc_type])
            
            # Fill in placeholders with random values
            text = template.format(
                np.random.randint(1000, 9999),
                np.random.randint(10000, 999999),
                f"ABC{np.random.randint(100, 999)}"
            )
            
            texts.append(text)
            labels.append(doc_type)
    
    print(f"✅ Created {len(texts)} synthetic documents")
    print(f"   Categories: {len(doc_types)}")
    print(f"   Samples per category: {samples_per_category}")
    
    return texts, labels


def main():
    """
    Main training function
    """
    print("=" * 60)
    print("🚀 DOCUMENT CLASSIFIER TRAINING")
    print("=" * 60)
    print()
    
    # Try to load real data first
    texts, labels = load_training_data()
    
    # If no real data, create synthetic data
    if texts is None or labels is None:
        print("\n⚠️ No real data available, using synthetic data")
        texts, labels = create_synthetic_document_data()
    
    if texts is None or len(texts) < 100:
        print("❌ Insufficient training data")
        return
    
    # Initialize classifier
    classifier = AdvancedDocumentClassifier(max_words=10000, max_len=200)
    
    # Prepare data
    X, y, num_classes = classifier.prepare_data(texts, labels)
    
    # Split data
    from sklearn.model_selection import train_test_split
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=np.argmax(y, axis=1)
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=np.argmax(y_temp, axis=1)
    )
    
    print(f"\n📊 Data split:")
    print(f"   Training: {len(X_train)}")
    print(f"   Validation: {len(X_val)}")
    print(f"   Test: {len(X_test)}")
    
    # Train CNN model
    print("\n" + "=" * 60)
    print("🔄 Training CNN Model")
    print("=" * 60)
    
    cnn_result = classifier.train_model(
        'cnn',
        X_train, y_train,
        X_val, y_val,
        epochs=30,
        batch_size=32
    )
    
    # Evaluate CNN
    cnn_metrics = classifier.evaluate_model('cnn', X_test, y_test)
    
    # Train Hybrid model
    print("\n" + "=" * 60)
    print("🔄 Training Hybrid CNN-LSTM Model")
    print("=" * 60)
    
    hybrid_result = classifier.train_model(
        'hybrid',
        X_train, y_train,
        X_val, y_val,
        epochs=30,
        batch_size=32
    )
    
    # Evaluate Hybrid
    hybrid_metrics = classifier.evaluate_model('hybrid', X_test, y_test)
    
    # Save models
    print("\n" + "=" * 60)
    print("💾 Saving Models")
    print("=" * 60)
    
    models_dir = Path(__file__).parent.parent / "models" / "document_classifier"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Save CNN model
    cnn_model_path = models_dir / "cnn_model.h5"
    classifier.models['cnn'].save(cnn_model_path)
    print(f"✅ CNN model saved: {cnn_model_path}")
    
    # Save Hybrid model
    hybrid_model_path = models_dir / "hybrid_model.h5"
    classifier.models['hybrid'].save(hybrid_model_path)
    print(f"✅ Hybrid model saved: {hybrid_model_path}")
    
    # Save tokenizer
    import pickle
    tokenizer_path = models_dir / "tokenizer.pkl"
    with open(tokenizer_path, 'wb') as f:
        pickle.dump(classifier.tokenizer, f)
    print(f"✅ Tokenizer saved: {tokenizer_path}")
    
    # Save label encoders
    label_encoder_path = models_dir / "label_encoder.pkl"
    with open(label_encoder_path, 'wb') as f:
        pickle.dump({
            'label_encoder': classifier.label_encoder,
            'reverse_label_encoder': classifier.reverse_label_encoder
        }, f)
    print(f"✅ Label encoders saved: {label_encoder_path}")
    
    # Save metadata
    import json
    from datetime import datetime
    
    metadata = {
        'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_samples': len(texts),
        'train_samples': len(X_train),
        'val_samples': len(X_val),
        'test_samples': len(X_test),
        'num_classes': num_classes,
        'classes': list(classifier.label_encoder.keys()),
        'max_words': classifier.max_words,
        'max_len': classifier.max_len,
        'models': {
            'cnn': {
                'accuracy': float(cnn_metrics['accuracy']),
                'model_path': str(cnn_model_path.name)
            },
            'hybrid': {
                'accuracy': float(hybrid_metrics['accuracy']),
                'model_path': str(hybrid_model_path.name)
            }
        }
    }
    
    metadata_path = models_dir / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✅ Metadata saved: {metadata_path}")
    
    # Create visualization
    classifier.plot_training_history(cnn_result['history'], 'CNN')
    classifier.plot_training_history(hybrid_result['history'], 'Hybrid')
    classifier.plot_confusion_matrices()
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Final Results:")
    print(f"   CNN Accuracy: {cnn_metrics['accuracy']:.4f}")
    print(f"   Hybrid Accuracy: {hybrid_metrics['accuracy']:.4f}")
    print(f"\n📁 Models saved in: {models_dir}")
    print("\n🎯 Next steps:")
    print("   1. Test the models with new documents")
    print("   2. Integrate into ML API service")
    print("   3. Deploy to production")


if __name__ == "__main__":
    main()