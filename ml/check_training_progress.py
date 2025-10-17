"""
Quick script to check if training is running and show progress
"""
import os
import time
from datetime import datetime

output_dir = 'optimized_models_25000_samples'

print("=" * 80)
print("🔍 CHECKING TRAINING PROGRESS")
print("=" * 80)

# Check if output directory exists
if os.path.exists(output_dir):
    print(f"\n✅ Output directory exists: {output_dir}/")
    
    # List files in directory
    files = os.listdir(output_dir)
    if files:
        print(f"\n📁 Files created so far ({len(files)}):")
        for f in files:
            filepath = os.path.join(output_dir, f)
            size = os.path.getsize(filepath)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            print(f"   {f}")
            print(f"      Size: {size:,} bytes")
            print(f"      Modified: {mtime}")
    else:
        print("\n⏳ No files created yet - training is still in progress...")
else:
    print(f"\n⏳ Output directory not created yet - training is starting...")

# Check if training data exists
enhanced_file = 'enhanced_synthetic_data/enhanced_synthetic_25000_with_real_patterns.xlsx'
if os.path.exists(enhanced_file):
    print(f"\n✅ Training data exists: {enhanced_file}")
    size = os.path.getsize(enhanced_file)
    print(f"   Size: {size:,} bytes")
else:
    print(f"\n❌ Training data not found: {enhanced_file}")

print("\n" + "=" * 80)
print("💡 TIP: Training takes 30-60 minutes. Check back later!")
print("=" * 80)