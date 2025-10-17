"""
🔍 MONITOR TRAINING PROGRESS IN REAL-TIME
==========================================

This script monitors the training progress by checking:
1. Files being created in the output directory
2. File sizes (models grow as they train)
3. Estimated completion time

Run this while training is in progress!
"""

import os
import time
from datetime import datetime, timedelta

output_dir = 'optimized_models_25000_samples'
expected_files = [
    'random_forest_optimized.pkl',
    'gradient_boosting_optimized.pkl',
    'ridge_optimized.pkl',
    'scaler.pkl',
    'label_encoders.pkl',
    'feature_columns.pkl',
    'best_parameters.json'
]

print("=" * 80)
print("🔍 TRAINING PROGRESS MONITOR")
print("=" * 80)
print("\nMonitoring training progress...")
print("Press Ctrl+C to stop monitoring\n")

start_time = datetime.now()
last_file_count = 0

try:
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print("🔍 TRAINING PROGRESS MONITOR")
        print("=" * 80)
        print(f"\n⏰ Monitoring started: {start_time.strftime('%H:%M:%S')}")
        print(f"⏱️  Elapsed time: {datetime.now() - start_time}")
        print(f"📅 Current time: {datetime.now().strftime('%H:%M:%S')}")
        
        # Check if output directory exists
        if not os.path.exists(output_dir):
            print(f"\n⏳ Waiting for training to start...")
            print(f"   Output directory not created yet: {output_dir}/")
        else:
            # List files in directory
            files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
            
            if not files:
                print(f"\n⏳ Training in progress...")
                print(f"   Stage: Loading data and preparing features")
                print(f"   No model files created yet")
            else:
                print(f"\n✅ Files created: {len(files)}/{len(expected_files)}")
                print(f"\n📁 Current files:")
                
                total_size = 0
                for f in sorted(files):
                    filepath = os.path.join(output_dir, f)
                    size = os.path.getsize(filepath)
                    total_size += size
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    # Determine status
                    if f in expected_files:
                        status = "✅"
                    else:
                        status = "📄"
                    
                    print(f"   {status} {f}")
                    print(f"      Size: {size:,} bytes ({size/1024/1024:.2f} MB)")
                    print(f"      Modified: {mtime.strftime('%H:%M:%S')}")
                
                print(f"\n📊 Total size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
                
                # Estimate progress
                progress = len(files) / len(expected_files) * 100
                print(f"\n📈 Progress: {progress:.1f}%")
                
                # Show progress bar
                bar_length = 50
                filled = int(bar_length * progress / 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                print(f"   [{bar}] {progress:.1f}%")
                
                # Estimate completion
                if len(files) > last_file_count:
                    last_file_count = len(files)
                
                if progress > 0 and progress < 100:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    estimated_total = elapsed / (progress / 100)
                    remaining = estimated_total - elapsed
                    eta = datetime.now() + timedelta(seconds=remaining)
                    print(f"\n⏰ Estimated completion: {eta.strftime('%H:%M:%S')}")
                    print(f"   Time remaining: ~{int(remaining/60)} minutes")
                elif progress >= 100:
                    print(f"\n🎉 TRAINING COMPLETE!")
                    print(f"   Total time: {datetime.now() - start_time}")
                    break
        
        print("\n" + "=" * 80)
        print("💡 Training takes 30-60 minutes total")
        print("   • Random Forest: ~15-25 minutes")
        print("   • Gradient Boosting: ~15-25 minutes")
        print("   • Ridge Regression: ~5-10 minutes")
        print("=" * 80)
        print("\nRefreshing in 10 seconds... (Press Ctrl+C to stop)")
        
        time.sleep(10)
        
except KeyboardInterrupt:
    print("\n\n✋ Monitoring stopped by user")
    print("   Training is still running in the background!")