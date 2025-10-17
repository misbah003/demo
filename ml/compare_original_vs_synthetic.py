"""
📊 COMPARE ORIGINAL VS SYNTHETIC DATA MODELS
============================================

This script compares model performance between:
- Original models (trained on 50 real transactions)
- Synthetic models (trained on synthetic data)

Shows how accuracy improves with more data!
"""

import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from datetime import datetime

print("=" * 70)
print("📊 ORIGINAL VS SYNTHETIC MODEL COMPARISON")
print("=" * 70)

# ============================================================================
# LOAD ORIGINAL MODEL RESULTS
# ============================================================================

print("\n📥 Loading original model results...")

original_results = {
    'refund': None,
    'anomaly': None,
    'timeseries': None
}

# Load refund prediction results
if os.path.exists('../models/ml_models/model_comparison.csv'):
    original_results['refund'] = pd.read_csv('../models/ml_models/model_comparison.csv')
    print("✅ Loaded original refund prediction results")
else:
    print("⚠️  Original refund prediction results not found")

# Load anomaly detection results
if os.path.exists('../models/anomaly_detection_models_IMPROVED/model_comparison_improved.csv'):
    original_results['anomaly'] = pd.read_csv('../models/anomaly_detection_models_IMPROVED/model_comparison_improved.csv')
    print("✅ Loaded original anomaly detection results")
else:
    print("⚠️  Original anomaly detection results not found")

# Load time series results
if os.path.exists('time_series_models_IMPROVED/model_comparison_improved.csv'):
    original_results['timeseries'] = pd.read_csv('time_series_models_IMPROVED/model_comparison_improved.csv')
    print("✅ Loaded original time series results")
else:
    print("⚠️  Original time series results not found")

# ============================================================================
# LOAD SYNTHETIC MODEL RESULTS
# ============================================================================

print("\n📥 Loading synthetic model results...")

# Find synthetic model directories
synthetic_dirs = glob.glob('synthetic_models_*')

if not synthetic_dirs:
    print("❌ No synthetic model results found!")
    print("⚠️  Please run 'train_with_synthetic_data.py' first")
    exit(1)

print(f"\n✅ Found {len(synthetic_dirs)} synthetic model result(s):")
for i, dir_name in enumerate(synthetic_dirs, 1):
    num_samples = dir_name.split('_')[-2]
    print(f"   {i}. {dir_name} ({num_samples} samples)")

# Select directory
if len(synthetic_dirs) == 1:
    selected_dir = synthetic_dirs[0]
else:
    choice = int(input("\nSelect directory number: ")) - 1
    selected_dir = synthetic_dirs[choice]

num_synthetic_samples = int(selected_dir.split('_')[-2])
print(f"\n✅ Using: {selected_dir}")

synthetic_results = {
    'refund': None,
    'anomaly': None,
    'timeseries': None
}

# Load synthetic results
if os.path.exists(f'{selected_dir}/refund_prediction_results.csv'):
    synthetic_results['refund'] = pd.read_csv(f'{selected_dir}/refund_prediction_results.csv')
    print("✅ Loaded synthetic refund prediction results")

if os.path.exists(f'{selected_dir}/anomaly_detection_results.csv'):
    synthetic_results['anomaly'] = pd.read_csv(f'{selected_dir}/anomaly_detection_results.csv')
    print("✅ Loaded synthetic anomaly detection results")

if os.path.exists(f'{selected_dir}/timeseries_results.csv'):
    synthetic_results['timeseries'] = pd.read_csv(f'{selected_dir}/timeseries_results.csv')
    print("✅ Loaded synthetic time series results")

# ============================================================================
# COMPARE RESULTS
# ============================================================================

print("\n" + "=" * 70)
print("📊 PERFORMANCE COMPARISON")
print("=" * 70)

comparison_data = []

# Compare Refund Prediction
if original_results['refund'] is not None and synthetic_results['refund'] is not None:
    print("\n🎯 VAT REFUND PREDICTION")
    print("-" * 70)
    
    # Get best models
    orig_best = original_results['refund'].sort_values('R2_Score', ascending=False).iloc[0]
    synth_best = synthetic_results['refund'].sort_values('R2_Score', ascending=False).iloc[0]
    
    print(f"\nOriginal (50 samples):")
    print(f"   Best Model: {orig_best['Model']}")
    print(f"   R² Score: {orig_best['R2_Score']:.4f}")
    print(f"   MAE: ₹{orig_best['MAE']:,.2f}")
    print(f"   RMSE: ₹{orig_best['RMSE']:,.2f}")
    
    print(f"\nSynthetic ({num_synthetic_samples} samples):")
    print(f"   Best Model: {synth_best['Model']}")
    print(f"   R² Score: {synth_best['R2_Score']:.4f}")
    print(f"   MAE: ₹{synth_best['MAE']:,.2f}")
    print(f"   RMSE: ₹{synth_best['RMSE']:,.2f}")
    
    # Calculate improvement
    r2_improvement = ((synth_best['R2_Score'] - orig_best['R2_Score']) / orig_best['R2_Score']) * 100
    mae_improvement = ((orig_best['MAE'] - synth_best['MAE']) / orig_best['MAE']) * 100
    
    print(f"\n📈 Improvement:")
    print(f"   R² Score: {r2_improvement:+.1f}%")
    print(f"   MAE: {mae_improvement:+.1f}%")
    
    comparison_data.append({
        'System': 'Refund Prediction',
        'Metric': 'R² Score',
        'Original_50': orig_best['R2_Score'],
        f'Synthetic_{num_synthetic_samples}': synth_best['R2_Score'],
        'Improvement_%': r2_improvement
    })
    
    comparison_data.append({
        'System': 'Refund Prediction',
        'Metric': 'MAE (₹)',
        'Original_50': orig_best['MAE'],
        f'Synthetic_{num_synthetic_samples}': synth_best['MAE'],
        'Improvement_%': mae_improvement
    })

# Compare Anomaly Detection
if original_results['anomaly'] is not None and synthetic_results['anomaly'] is not None:
    print("\n🚨 ANOMALY DETECTION")
    print("-" * 70)
    
    # Get best models
    orig_best = original_results['anomaly'].sort_values('Test_Accuracy', ascending=False).iloc[0]
    synth_best = synthetic_results['anomaly'].sort_values('Test_Accuracy', ascending=False).iloc[0]
    
    print(f"\nOriginal (50 samples):")
    print(f"   Best Model: {orig_best['Model']}")
    print(f"   Test Accuracy: {orig_best['Test_Accuracy']:.2%}")
    print(f"   F1-Score: {orig_best['F1_Score']:.4f}")
    print(f"   Overfitting Gap: {orig_best['Overfitting_Gap']:.2%}")
    
    print(f"\nSynthetic ({num_synthetic_samples} samples):")
    print(f"   Best Model: {synth_best['Model']}")
    print(f"   Test Accuracy: {synth_best['Test_Accuracy']:.2%}")
    print(f"   F1-Score: {synth_best['F1_Score']:.4f}")
    print(f"   Overfitting Gap: {synth_best['Overfitting_Gap']:.2%}")
    
    # Calculate improvement
    acc_improvement = ((synth_best['Test_Accuracy'] - orig_best['Test_Accuracy']) / orig_best['Test_Accuracy']) * 100
    f1_improvement = ((synth_best['F1_Score'] - orig_best['F1_Score']) / orig_best['F1_Score']) * 100
    
    print(f"\n📈 Improvement:")
    print(f"   Accuracy: {acc_improvement:+.1f}%")
    print(f"   F1-Score: {f1_improvement:+.1f}%")
    
    comparison_data.append({
        'System': 'Anomaly Detection',
        'Metric': 'Accuracy',
        'Original_50': orig_best['Test_Accuracy'],
        f'Synthetic_{num_synthetic_samples}': synth_best['Test_Accuracy'],
        'Improvement_%': acc_improvement
    })
    
    comparison_data.append({
        'System': 'Anomaly Detection',
        'Metric': 'F1-Score',
        'Original_50': orig_best['F1_Score'],
        f'Synthetic_{num_synthetic_samples}': synth_best['F1_Score'],
        'Improvement_%': f1_improvement
    })

# Compare Time Series
if original_results['timeseries'] is not None and synthetic_results['timeseries'] is not None:
    print("\n📈 TIME SERIES FORECASTING")
    print("-" * 70)
    
    # Get best models
    orig_best = original_results['timeseries'].sort_values('MAPE', ascending=True).iloc[0]
    synth_best = synthetic_results['timeseries'].iloc[0]
    
    print(f"\nOriginal (6 months):")
    print(f"   Model: {orig_best['Model']}")
    print(f"   MAPE: {orig_best['MAPE']:.2f}%")
    if 'RMSE' in orig_best:
        print(f"   RMSE: ₹{orig_best['RMSE']:,.2f}")
    
    print(f"\nSynthetic ({synth_best['Train_Months']} months):")
    print(f"   Model: {synth_best['Model']}")
    print(f"   MAPE: {synth_best['MAPE']:.2f}%")
    print(f"   RMSE: ₹{synth_best['RMSE']:,.2f}")
    
    # Calculate improvement (lower MAPE is better)
    mape_improvement = ((orig_best['MAPE'] - synth_best['MAPE']) / orig_best['MAPE']) * 100
    
    print(f"\n📈 Improvement:")
    print(f"   MAPE: {mape_improvement:+.1f}%")
    
    comparison_data.append({
        'System': 'Time Series',
        'Metric': 'MAPE (%)',
        'Original_50': orig_best['MAPE'],
        f'Synthetic_{num_synthetic_samples}': synth_best['MAPE'],
        'Improvement_%': mape_improvement
    })

# ============================================================================
# SAVE COMPARISON RESULTS
# ============================================================================

if comparison_data:
    df_comparison = pd.DataFrame(comparison_data)
    output_file = f'comparison_original_vs_synthetic_{num_synthetic_samples}.csv'
    df_comparison.to_csv(output_file, index=False)
    
    print("\n" + "=" * 70)
    print("💾 SAVING RESULTS")
    print("=" * 70)
    print(f"\n✅ Saved comparison to: {output_file}")
    
    # Create visualization
    print("\n📊 Creating visualization...")
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f'Original (50 samples) vs Synthetic ({num_synthetic_samples} samples)', fontsize=16, fontweight='bold')
    
    # Plot 1: Refund Prediction R²
    if any(d['System'] == 'Refund Prediction' and d['Metric'] == 'R² Score' for d in comparison_data):
        data = [d for d in comparison_data if d['System'] == 'Refund Prediction' and d['Metric'] == 'R² Score'][0]
        axes[0].bar(['Original\n(50)', f'Synthetic\n({num_synthetic_samples})'], 
                    [data['Original_50'], data[f'Synthetic_{num_synthetic_samples}']], 
                    color=['#FF6B6B', '#4ECDC4'])
        axes[0].set_title('Refund Prediction\nR² Score (Higher is Better)', fontweight='bold')
        axes[0].set_ylabel('R² Score')
        axes[0].set_ylim(0, 1)
        for i, v in enumerate([data['Original_50'], data[f'Synthetic_{num_synthetic_samples}']]):
            axes[0].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    # Plot 2: Anomaly Detection Accuracy
    if any(d['System'] == 'Anomaly Detection' and d['Metric'] == 'Accuracy' for d in comparison_data):
        data = [d for d in comparison_data if d['System'] == 'Anomaly Detection' and d['Metric'] == 'Accuracy'][0]
        axes[1].bar(['Original\n(50)', f'Synthetic\n({num_synthetic_samples})'], 
                    [data['Original_50'] * 100, data[f'Synthetic_{num_synthetic_samples}'] * 100], 
                    color=['#FF6B6B', '#4ECDC4'])
        axes[1].set_title('Anomaly Detection\nAccuracy (Higher is Better)', fontweight='bold')
        axes[1].set_ylabel('Accuracy (%)')
        axes[1].set_ylim(0, 100)
        for i, v in enumerate([data['Original_50'] * 100, data[f'Synthetic_{num_synthetic_samples}'] * 100]):
            axes[1].text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # Plot 3: Time Series MAPE
    if any(d['System'] == 'Time Series' and d['Metric'] == 'MAPE (%)' for d in comparison_data):
        data = [d for d in comparison_data if d['System'] == 'Time Series' and d['Metric'] == 'MAPE (%)'][0]
        axes[2].bar(['Original\n(6 mo)', f'Synthetic\n({synth_best["Train_Months"]} mo)'], 
                    [data['Original_50'], data[f'Synthetic_{num_synthetic_samples}']], 
                    color=['#FF6B6B', '#4ECDC4'])
        axes[2].set_title('Time Series Forecasting\nMAPE (Lower is Better)', fontweight='bold')
        axes[2].set_ylabel('MAPE (%)')
        axes[2].set_ylim(0, max(data['Original_50'], data[f'Synthetic_{num_synthetic_samples}']) * 1.2)
        for i, v in enumerate([data['Original_50'], data[f'Synthetic_{num_synthetic_samples}']]):
            axes[2].text(i, v + 0.5, f'{v:.2f}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    chart_file = f'comparison_chart_{num_synthetic_samples}_samples.png'
    plt.savefig(chart_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved chart to: {chart_file}")
    
    # Display summary table
    print("\n" + "=" * 70)
    print("📊 SUMMARY TABLE")
    print("=" * 70)
    print("\n" + df_comparison.to_string(index=False))
    
    # Overall conclusion
    print("\n" + "=" * 70)
    print("🎓 CONCLUSION")
    print("=" * 70)
    
    avg_improvement = df_comparison['Improvement_%'].mean()
    
    print(f"\n📈 Average Improvement: {avg_improvement:+.1f}%")
    
    if avg_improvement > 20:
        print("\n🎉 EXCELLENT! Synthetic data significantly improved model performance!")
        print("   More data = Better accuracy (as expected)")
    elif avg_improvement > 10:
        print("\n✅ GOOD! Synthetic data improved model performance!")
        print("   Models benefit from larger training datasets")
    elif avg_improvement > 0:
        print("\n📊 MODERATE! Synthetic data slightly improved performance")
        print("   May need more data or better feature engineering")
    else:
        print("\n⚠️  WARNING! Synthetic data didn't improve performance")
        print("   Possible reasons:")
        print("   - Synthetic data quality issues")
        print("   - Original model already optimal for this problem")
        print("   - Need different features or algorithms")
    
    print("\n💡 Key Takeaway:")
    print(f"   With {num_synthetic_samples} samples vs 50 original samples:")
    print(f"   - {num_synthetic_samples / 50:.0f}x more data")
    print(f"   - {avg_improvement:+.1f}% average improvement")
    print(f"   - Data quality matters as much as quantity!")

else:
    print("\n❌ No comparison data available")
    print("   Make sure both original and synthetic models are trained")

print("\n" + "=" * 70)
print("✅ COMPARISON COMPLETE!")
print("=" * 70)