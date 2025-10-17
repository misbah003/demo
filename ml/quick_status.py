"""
⚡ QUICK TRAINING STATUS CHECK
"""
import os
from datetime import datetime

output_dir = 'optimized_models_25000_samples'

print("\n" + "=" * 60)
print("⚡ QUICK TRAINING STATUS")
print("=" * 60)

if not os.path.exists(output_dir):
    print("\n🟡 Stage 1: Loading data and preparing features")
    print("   Status: In progress...")
    print("   Time: 0-5 minutes")
    print("\n💡 This is the SLOWEST part of data loading!")
    print("   Be patient - it's working!")
else:
    files = os.listdir(output_dir)
    
    if not files:
        print("\n🟡 Stage 2: Feature preparation complete")
        print("   Status: Starting Random Forest training...")
        print("   Time: ~5 minutes elapsed")
    elif 'random_forest_optimized.pkl' not in files:
        print("\n🟡 Stage 3: Training Random Forest")
        print("   Status: In progress (250 model fits)...")
        print("   Time: 5-25 minutes")
        print("\n💡 This takes 15-25 minutes - be patient!")
    elif 'gradient_boosting_optimized.pkl' not in files:
        print("\n🟡 Stage 4: Training Gradient Boosting")
        print("   Status: In progress (250 model fits)...")
        print("   Time: 25-50 minutes")
        print("\n💡 This takes 15-25 minutes - be patient!")
    elif 'ridge_optimized.pkl' not in files:
        print("\n🟡 Stage 5: Training Ridge Regression")
        print("   Status: In progress (150 model fits)...")
        print("   Time: 50-60 minutes")
        print("\n💡 Almost done! Just 5-10 more minutes!")
    else:
        print("\n🟢 Stage 6: TRAINING COMPLETE!")
        print("   Status: All models trained successfully!")
        print(f"   Files created: {len(files)}")
        print("\n✅ Next steps:")
        print("   1. Test models: python ml/test_optimized_model.py")
        print("   2. Start API: python ml/ml_api_service_optimized.py")

print("=" * 60)
print()