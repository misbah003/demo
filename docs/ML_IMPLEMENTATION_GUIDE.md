# 🤖 VAT Refund Predictor - ML Implementation Guide

## 📋 Overview

This guide explains how to train, test, and deploy the **real Machine Learning model** for VAT refund prediction. The system compares multiple ML algorithms and automatically selects the best one.

---

## 🎯 What's Included

### 1. **Training Pipeline** (`train_vat_ml_models.py`)
- Trains 5 different ML models:
  - ✅ Linear Regression (baseline)
  - ✅ Random Forest Regressor
  - ✅ Gradient Boosting Regressor
  - ✅ XGBoost Regressor
  - ✅ Neural Network (MLP)
- Compares models using MAE, RMSE, and R² Score
- Automatically saves the best model

### 2. **Testing Script** (`test_ml_prediction.py`)
- Tests the trained model with sample data
- Compares ML predictions vs rule-based approach
- Validates model accuracy

### 3. **API Service** (`ml_api_service.py`)
- Flask REST API for serving predictions
- Endpoints for single and batch predictions
- CORS-enabled for frontend integration

### 4. **Training Data** (`vat_collection.py`)
- Generates synthetic VAT transaction data
- Creates realistic business scenarios
- Outputs to Excel file

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```powershell
pip install -r requirements_ml.txt
```

**Required packages:**
- pandas
- numpy
- scikit-learn
- xgboost
- flask
- flask-cors
- openpyxl

### Step 2: Generate Training Data

```powershell
python vat_collection.py
```

**Output:** `AI_Tax_Intelligence_Expanded.xlsx`

This creates:
- 50+ transaction records
- 10 client profiles
- Monthly filing summaries
- Tax notices

### Step 3: Train Models

```powershell
python train_vat_ml_models.py
```

**What happens:**
1. Loads data from Excel
2. Engineers features (12 features total)
3. Trains 5 different models
4. Compares performance
5. Saves the best model

**Output files in `ml_models/` directory:**
- `vat_refund_predictor.pkl` - Best trained model
- `scaler.pkl` - Feature scaler
- `label_encoders.pkl` - Categorical encoders
- `feature_columns.pkl` - Feature list
- `model_metadata.json` - Model info
- `model_comparison.csv` - All results
- `feature_importance.csv` - Feature rankings

### Step 4: Test the Model

```powershell
python test_ml_prediction.py
```

**Tests 5 scenarios:**
1. Small retail business (low risk)
2. Large pharma company (medium risk)
3. IT services (high risk)
4. Construction (non-compliant)
5. FMCG (compliant)

### Step 5: Start ML API Service

```powershell
python ml_api_service.py
```

**API runs on:** `http://localhost:5001`

---

## 📡 API Endpoints

### 1. Health Check
```http
GET http://localhost:5001/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Model Info
```http
GET http://localhost:5001/model-info
```

**Response:**
```json
{
  "model_name": "Random Forest",
  "trained_date": "2024-01-15 10:00:00",
  "r2_score": 0.9234,
  "mae": 1234.56,
  "rmse": 2345.67,
  "training_samples": 40,
  "features": ["Amount", "VAT_Rate_Numeric", ...]
}
```

### 3. Make Prediction
```http
POST http://localhost:5001/predict
Content-Type: application/json

{
  "businessType": "Retail",
  "turnover": 5000000,
  "vatPaid": 50000,
  "vatClaimed": 60000,
  "category": "Electronics",
  "filingStatus": "Filed",
  "region": "Karnataka",
  "riskScore": 0.3
}
```

**Response:**
```json
{
  "predictedRefund": 8500.50,
  "approvalProbability": 85.0,
  "breakdown": {
    "inputVat": 60000,
    "outputVat": 50000,
    "netRefund": 10000,
    "adjustments": [
      "Eligible for refund based on input VAT exceeding output VAT",
      "Low risk score - favorable for approval"
    ]
  },
  "modelInfo": {
    "modelName": "Random Forest",
    "accuracy": 0.9234
  },
  "riskAssessment": {
    "score": 0.3,
    "level": "LOW",
    "complianceFlag": "Compliant"
  }
}
```

### 4. Batch Predictions
```http
POST http://localhost:5001/batch-predict
Content-Type: application/json

{
  "predictions": [
    {
      "businessType": "Retail",
      "turnover": 5000000,
      "vatPaid": 50000,
      "vatClaimed": 60000
    },
    {
      "businessType": "Pharma",
      "turnover": 15000000,
      "vatPaid": 200000,
      "vatClaimed": 250000
    }
  ]
}
```

---

## 🔧 Integration with Backend

### Option 1: Call ML API from Node.js Backend

Update `backend-example/server.js`:

```javascript
// Add this endpoint
app.post('/api/ml-predict', async (req, res) => {
  try {
    const response = await fetch('http://localhost:5001/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    
    const prediction = await response.json();
    res.json(prediction);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Option 2: Update Supabase Edge Function

Update `supabase/functions/vat-refund-predictor/index.ts`:

```typescript
// Replace the rule-based logic with ML API call
const mlResponse = await fetch('http://localhost:5001/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    businessType,
    turnover,
    vatPaid,
    vatClaimed
  })
});

const prediction = await mlResponse.json();
return new Response(JSON.stringify(prediction), {
  headers: { ...corsHeaders, 'Content-Type': 'application/json' }
});
```

### Option 3: Update Frontend Component

Update `src/components/VATRefundPredictor.tsx`:

```typescript
const handlePredict = async () => {
  setIsLoading(true);
  
  try {
    const response = await fetch('http://localhost:5001/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        businessType,
        turnover: parseFloat(turnover),
        vatPaid: parseFloat(vatPaid),
        vatClaimed: parseFloat(inputVAT)
      })
    });
    
    const prediction = await response.json();
    
    setRefundAmount(prediction.predictedRefund);
    setApprovalProbability(prediction.approvalProbability);
    setRiskFactors(prediction.breakdown.adjustments);
  } catch (error) {
    console.error('Prediction failed:', error);
  } finally {
    setIsLoading(false);
  }
};
```

---

## 📊 Model Performance

### Expected Results

| Model | MAE | RMSE | R² Score |
|-------|-----|------|----------|
| Linear Regression | ~2500 | ~3500 | ~0.75 |
| Random Forest | ~1200 | ~2000 | ~0.92 |
| Gradient Boosting | ~1300 | ~2100 | ~0.91 |
| XGBoost | ~1100 | ~1900 | ~0.93 |
| Neural Network | ~1500 | ~2300 | ~0.88 |

**Best Model:** Usually XGBoost or Random Forest

### Feature Importance (Top 5)

1. **VAT_Amount** - Most important
2. **Annual_Turnover** - Business size
3. **Risk_Score** - Compliance history
4. **Amount** - Transaction size
5. **VAT_to_Amount_Ratio** - VAT percentage

---

## 🔄 Retraining the Model

### When to Retrain

- Monthly: With new transaction data
- Quarterly: Full model comparison
- When accuracy drops below threshold
- After significant policy changes

### How to Retrain

1. **Add new data** to Excel file:
   ```python
   # Append to existing data
   new_data = pd.read_excel("AI_Tax_Intelligence_Expanded.xlsx")
   # Add new rows...
   new_data.to_excel("AI_Tax_Intelligence_Expanded.xlsx")
   ```

2. **Retrain models:**
   ```powershell
   python train_vat_ml_models.py
   ```

3. **Restart API service:**
   ```powershell
   # Stop current service (Ctrl+C)
   python ml_api_service.py
   ```

---

## 🐛 Troubleshooting

### Issue: "Model not found"
**Solution:** Run `python train_vat_ml_models.py` first

### Issue: "XGBoost not installed"
**Solution:** `pip install xgboost` (optional, will skip if not available)

### Issue: "Excel file not found"
**Solution:** Run `python vat_collection.py` to generate data

### Issue: "Port 5001 already in use"
**Solution:** Change port in `ml_api_service.py` (line: `app.run(port=5001)`)

### Issue: "CORS error in frontend"
**Solution:** Ensure `flask-cors` is installed and API is running

---

## 📈 Monitoring & Logging

### Check Model Performance

```powershell
# View comparison results
cat ml_models/model_comparison.csv

# View feature importance
cat ml_models/feature_importance.csv

# View metadata
cat ml_models/model_metadata.json
```

### API Logs

The Flask API logs all requests to console:
- Request method and endpoint
- Response status
- Prediction results
- Errors (if any)

---

## 🎯 Next Steps

1. ✅ **Train the model** - Run training script
2. ✅ **Test predictions** - Verify accuracy
3. ✅ **Start API service** - Launch Flask server
4. 🔄 **Integrate with backend** - Connect to your app
5. 📊 **Monitor performance** - Track accuracy over time
6. 🔄 **Retrain periodically** - Keep model updated

---

## 📚 Additional Resources

### Files Structure
```
navi-tax-35-main/
├── vat_collection.py              # Generate training data
├── train_vat_ml_models.py         # Train models
├── test_ml_prediction.py          # Test predictions
├── ml_api_service.py              # API service
├── requirements_ml.txt            # Dependencies
├── AI_Tax_Intelligence_Expanded.xlsx  # Training data
└── ml_models/                     # Saved models
    ├── vat_refund_predictor.pkl
    ├── scaler.pkl
    ├── label_encoders.pkl
    ├── feature_columns.pkl
    ├── model_metadata.json
    ├── model_comparison.csv
    └── feature_importance.csv
```

### Key Concepts

- **MAE (Mean Absolute Error):** Average prediction error in rupees
- **RMSE (Root Mean Squared Error):** Penalizes large errors more
- **R² Score:** How well model explains variance (0-1, higher is better)
- **Feature Engineering:** Creating useful features from raw data
- **Cross-validation:** Testing model on different data splits

---

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review console logs for errors
3. Verify all dependencies are installed
4. Ensure training data exists

---

**🎉 Congratulations! You now have a real ML-powered VAT Refund Predictor!**