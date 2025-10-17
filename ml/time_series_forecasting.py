"""
🔮 VAT Collection Time Series Forecasting
==========================================
Forecasts monthly VAT collections using:
- ARIMA (AutoRegressive Integrated Moving Average)
- SARIMA (Seasonal ARIMA)
- Prophet (Facebook's forecasting tool)
- LSTM (Long Short-Term Memory Neural Network)

Evaluation Metrics: RMSE, MAPE
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from datetime import datetime, timedelta
import json
import os

warnings.filterwarnings('ignore')

# ============================================
# 1️⃣ LOAD AND PREPARE TIME SERIES DATA
# ============================================

print("=" * 60)
print("🔮 VAT COLLECTION TIME SERIES FORECASTING")
print("=" * 60)

# Load data
excel_file = "AI_Tax_Intelligence_Expanded.xlsx"
if not os.path.exists(excel_file):
    excel_file = "../AI_Tax_Intelligence_Expanded.xlsx"

print(f"\n📂 Loading data from: {excel_file}")
monthly_summary = pd.read_excel(excel_file, sheet_name="Monthly_Filing_Summary")
transaction_data = pd.read_excel(excel_file, sheet_name="Transaction_Data")

print(f"✅ Loaded {len(monthly_summary)} monthly records")
print(f"✅ Loaded {len(transaction_data)} transactions")

# Aggregate monthly VAT collections
print("\n📊 Aggregating monthly VAT collections...")
monthly_vat = monthly_summary.groupby('Month')['Total_VAT'].sum().reset_index()
monthly_vat['Month'] = pd.to_datetime(monthly_vat['Month'])
monthly_vat = monthly_vat.sort_values('Month')
monthly_vat.set_index('Month', inplace=True)

print(f"✅ Created time series with {len(monthly_vat)} months")
print(f"   Date range: {monthly_vat.index.min()} to {monthly_vat.index.max()}")
print(f"   Total VAT collected: ₹{monthly_vat['Total_VAT'].sum():,.2f}")
print(f"   Average monthly: ₹{monthly_vat['Total_VAT'].mean():,.2f}")

# Split into train/test (80/20)
train_size = int(len(monthly_vat) * 0.8)
train_data = monthly_vat[:train_size]
test_data = monthly_vat[train_size:]

print(f"\n📊 Train/Test Split:")
print(f"   Training: {len(train_data)} months ({train_data.index.min()} to {train_data.index.max()})")
print(f"   Testing: {len(test_data)} months ({test_data.index.min()} to {test_data.index.max()})")

# ============================================
# 2️⃣ EVALUATION METRICS
# ============================================

def calculate_rmse(actual, predicted):
    """Root Mean Squared Error"""
    return np.sqrt(np.mean((actual - predicted) ** 2))

def calculate_mape(actual, predicted):
    """Mean Absolute Percentage Error"""
    # Avoid division by zero
    mask = actual != 0
    return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100

def evaluate_model(model_name, actual, predicted):
    """Calculate and display evaluation metrics"""
    rmse = calculate_rmse(actual, predicted)
    mape = calculate_mape(actual, predicted)
    
    print(f"\n{'='*60}")
    print(f"📊 {model_name} - Evaluation Metrics")
    print(f"{'='*60}")
    print(f"   RMSE: ₹{rmse:,.2f}")
    print(f"   MAPE: {mape:.2f}%")
    print(f"{'='*60}")
    
    return {'model': model_name, 'rmse': rmse, 'mape': mape}

# ============================================
# 3️⃣ MODEL 1: ARIMA
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 1: ARIMA (AutoRegressive Integrated Moving Average)")
print("="*60)

try:
    from statsmodels.tsa.arima.model import ARIMA
    
    print("📈 Training ARIMA model...")
    print("   Parameters: order=(1,1,1)")
    
    # Fit ARIMA model
    arima_model = ARIMA(train_data['Total_VAT'], order=(1, 1, 1))
    arima_fitted = arima_model.fit()
    
    # Forecast
    arima_forecast = arima_fitted.forecast(steps=len(test_data))
    arima_forecast = pd.Series(arima_forecast.values, index=test_data.index)
    
    # Evaluate
    arima_results = evaluate_model("ARIMA", test_data['Total_VAT'].values, arima_forecast.values)
    
    print("✅ ARIMA model trained successfully")
    
except ImportError:
    print("⚠️  statsmodels not installed. Installing...")
    print("   Run: pip install statsmodels")
    arima_results = {'model': 'ARIMA', 'rmse': None, 'mape': None}
    arima_forecast = None
except Exception as e:
    print(f"❌ ARIMA failed: {str(e)}")
    arima_results = {'model': 'ARIMA', 'rmse': None, 'mape': None}
    arima_forecast = None

# ============================================
# 4️⃣ MODEL 2: SARIMA
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 2: SARIMA (Seasonal ARIMA)")
print("="*60)

try:
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    
    print("📈 Training SARIMA model...")
    print("   Parameters: order=(1,1,1), seasonal_order=(1,1,1,12)")
    
    # Fit SARIMA model
    sarima_model = SARIMAX(train_data['Total_VAT'], 
                           order=(1, 1, 1), 
                           seasonal_order=(1, 1, 1, 12))
    sarima_fitted = sarima_model.fit(disp=False)
    
    # Forecast
    sarima_forecast = sarima_fitted.forecast(steps=len(test_data))
    sarima_forecast = pd.Series(sarima_forecast.values, index=test_data.index)
    
    # Evaluate
    sarima_results = evaluate_model("SARIMA", test_data['Total_VAT'].values, sarima_forecast.values)
    
    print("✅ SARIMA model trained successfully")
    
except ImportError:
    print("⚠️  statsmodels not installed")
    sarima_results = {'model': 'SARIMA', 'rmse': None, 'mape': None}
    sarima_forecast = None
except Exception as e:
    print(f"❌ SARIMA failed: {str(e)}")
    sarima_results = {'model': 'SARIMA', 'rmse': None, 'mape': None}
    sarima_forecast = None

# ============================================
# 5️⃣ MODEL 3: PROPHET
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 3: Prophet (Facebook's Forecasting Tool)")
print("="*60)

try:
    from prophet import Prophet
    
    print("📈 Training Prophet model...")
    
    # Prepare data for Prophet (requires 'ds' and 'y' columns)
    prophet_train = pd.DataFrame({
        'ds': train_data.index,
        'y': train_data['Total_VAT'].values
    })
    
    # Fit Prophet model
    prophet_model = Prophet(yearly_seasonality=True, 
                           weekly_seasonality=False,
                           daily_seasonality=False)
    prophet_model.fit(prophet_train)
    
    # Create future dataframe
    future = pd.DataFrame({'ds': test_data.index})
    
    # Forecast
    prophet_forecast_df = prophet_model.predict(future)
    prophet_forecast = pd.Series(prophet_forecast_df['yhat'].values, index=test_data.index)
    
    # Evaluate
    prophet_results = evaluate_model("Prophet", test_data['Total_VAT'].values, prophet_forecast.values)
    
    print("✅ Prophet model trained successfully")
    
except ImportError:
    print("⚠️  Prophet not installed. Installing...")
    print("   Run: pip install prophet")
    prophet_results = {'model': 'Prophet', 'rmse': None, 'mape': None}
    prophet_forecast = None
except Exception as e:
    print(f"❌ Prophet failed: {str(e)}")
    prophet_results = {'model': 'Prophet', 'rmse': None, 'mape': None}
    prophet_forecast = None

# ============================================
# 6️⃣ MODEL 4: LSTM
# ============================================

print("\n" + "="*60)
print("🤖 MODEL 4: LSTM (Long Short-Term Memory Neural Network)")
print("="*60)

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense
    from sklearn.preprocessing import MinMaxScaler
    
    print("📈 Training LSTM model...")
    print("   Architecture: LSTM(50) -> Dense(1)")
    
    # Scale data
    scaler = MinMaxScaler()
    scaled_train = scaler.fit_transform(train_data[['Total_VAT']])
    scaled_test = scaler.transform(test_data[['Total_VAT']])
    
    # Create sequences (lookback=3 months)
    lookback = 3
    
    def create_sequences(data, lookback):
        X, y = [], []
        for i in range(lookback, len(data)):
            X.append(data[i-lookback:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)
    
    X_train, y_train = create_sequences(scaled_train, lookback)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    
    # Build LSTM model
    lstm_model = Sequential([
        LSTM(50, activation='relu', input_shape=(lookback, 1)),
        Dense(1)
    ])
    lstm_model.compile(optimizer='adam', loss='mse')
    
    # Train
    lstm_model.fit(X_train, y_train, epochs=50, batch_size=1, verbose=0)
    
    # Forecast
    lstm_predictions = []
    current_sequence = scaled_train[-lookback:].flatten().tolist()
    
    for _ in range(len(test_data)):
        current_input = np.array(current_sequence[-lookback:]).reshape((1, lookback, 1))
        next_pred = lstm_model.predict(current_input, verbose=0)[0, 0]
        lstm_predictions.append(next_pred)
        current_sequence.append(next_pred)
    
    # Inverse transform
    lstm_predictions = scaler.inverse_transform(np.array(lstm_predictions).reshape(-1, 1)).flatten()
    lstm_forecast = pd.Series(lstm_predictions, index=test_data.index)
    
    # Evaluate
    lstm_results = evaluate_model("LSTM", test_data['Total_VAT'].values, lstm_forecast.values)
    
    print("✅ LSTM model trained successfully")
    
except ImportError:
    print("⚠️  TensorFlow not installed. Installing...")
    print("   Run: pip install tensorflow")
    lstm_results = {'model': 'LSTM', 'rmse': None, 'mape': None}
    lstm_forecast = None
except Exception as e:
    print(f"❌ LSTM failed: {str(e)}")
    lstm_results = {'model': 'LSTM', 'rmse': None, 'mape': None}
    lstm_forecast = None

# ============================================
# 7️⃣ COMPARE ALL MODELS
# ============================================

print("\n" + "="*60)
print("🏆 MODEL COMPARISON - TIME SERIES FORECASTING")
print("="*60)

# Collect all results
all_results = [arima_results, sarima_results, prophet_results, lstm_results]
results_df = pd.DataFrame(all_results)

# Filter out failed models
results_df = results_df[results_df['rmse'].notna()]

if len(results_df) > 0:
    # Sort by RMSE (lower is better)
    results_df = results_df.sort_values('rmse')
    
    print("\n📊 Performance Ranking (by RMSE):")
    print(f"\n{'Rank':<6} {'Model':<15} {'RMSE (₹)':<15} {'MAPE (%)':<10}")
    print("-" * 50)
    
    for idx, row in results_df.iterrows():
        rank = "🥇" if idx == results_df.index[0] else "🥈" if idx == results_df.index[1] else "🥉" if idx == results_df.index[2] else "4️⃣"
        print(f"{rank:<6} {row['model']:<15} {row['rmse']:>12,.2f}   {row['mape']:>8.2f}%")
    
    # Select best model
    best_model = results_df.iloc[0]
    print(f"\n🏆 WINNER: {best_model['model']}")
    print(f"   RMSE: ₹{best_model['rmse']:,.2f}")
    print(f"   MAPE: {best_model['mape']:.2f}%")
    
    # Save results
    os.makedirs('../models/time_series_models', exist_ok=True)
    results_df.to_csv('../models/time_series_models/model_comparison.csv', index=False)
    print(f"\n✅ Results saved to: ../models/time_series_models/model_comparison.csv")
    
    # Save metadata
    metadata = {
        'training_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'train_months': len(train_data),
        'test_months': len(test_data),
        'best_model': best_model['model'],
        'best_rmse': float(best_model['rmse']),
        'best_mape': float(best_model['mape']),
        'date_range': f"{monthly_vat.index.min()} to {monthly_vat.index.max()}"
    }
    
    with open('../models/time_series_models/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ Metadata saved to: ../models/time_series_models/metadata.json")
    
else:
    print("\n❌ No models succeeded. Please install required packages:")
    print("   pip install statsmodels prophet tensorflow scikit-learn")

# ============================================
# 8️⃣ VISUALIZATION
# ============================================

print("\n" + "="*60)
print("📊 GENERATING VISUALIZATIONS")
print("="*60)

try:
    plt.figure(figsize=(14, 8))
    
    # Plot actual data
    plt.plot(train_data.index, train_data['Total_VAT'], 
             label='Training Data', color='blue', linewidth=2)
    plt.plot(test_data.index, test_data['Total_VAT'], 
             label='Actual (Test)', color='green', linewidth=2, marker='o')
    
    # Plot forecasts
    if arima_forecast is not None:
        plt.plot(test_data.index, arima_forecast, 
                label=f"ARIMA (RMSE: ₹{arima_results['rmse']:,.0f})", 
                linestyle='--', marker='s')
    
    if sarima_forecast is not None:
        plt.plot(test_data.index, sarima_forecast, 
                label=f"SARIMA (RMSE: ₹{sarima_results['rmse']:,.0f})", 
                linestyle='--', marker='^')
    
    if prophet_forecast is not None:
        plt.plot(test_data.index, prophet_forecast, 
                label=f"Prophet (RMSE: ₹{prophet_results['rmse']:,.0f})", 
                linestyle='--', marker='d')
    
    if lstm_forecast is not None:
        plt.plot(test_data.index, lstm_forecast, 
                label=f"LSTM (RMSE: ₹{lstm_results['rmse']:,.0f})", 
                linestyle='--', marker='x')
    
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total VAT Collection (₹)', fontsize=12)
    plt.title('VAT Collection Forecasting - Model Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    plt.savefig('../models/time_series_models/forecast_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Visualization saved to: ../models/time_series_models/forecast_comparison.png")
    
except Exception as e:
    print(f"⚠️  Visualization failed: {str(e)}")

print("\n" + "="*60)
print("✅ TIME SERIES FORECASTING COMPLETE!")
print("="*60)
print("\n📁 Output Files:")
print("   1. ../models/time_series_models/model_comparison.csv")
print("   2. ../models/time_series_models/metadata.json")
print("   3. ../models/time_series_models/forecast_comparison.png")
print("\n🚀 Next: Run anomaly detection classification")
print("   python anomaly_detection_classification.py")
print("="*60)