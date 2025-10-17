"""
Convert Excel to CSV for faster loading
"""
import pandas as pd
import time

print("Converting Excel to CSV for faster training...")
start = time.time()

# Load Excel
df = pd.read_excel('enhanced_synthetic_data/enhanced_synthetic_25000_with_real_patterns.xlsx')
print(f"✅ Loaded Excel in {time.time()-start:.2f} seconds")

# Save as CSV
df.to_csv('enhanced_synthetic_data/enhanced_synthetic_25000_with_real_patterns.csv', index=False)
print(f"✅ Saved CSV in {time.time()-start:.2f} seconds")
print(f"\n💡 CSV is 10-20x faster to load than Excel!")