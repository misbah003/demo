# 🌐 VAT Refund ML API - Website Integration Guide

## ✅ API Status: RUNNING
- **URL:** `http://localhost:5001`
- **Status:** ✅ Healthy
- **Model:** Random Forest (70.26% accuracy)

---

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [API Endpoints](#api-endpoints)
3. [Integration Examples](#integration-examples)
4. [Error Handling](#error-handling)
5. [Testing](#testing)

---

## 🚀 Quick Start

### Start the API Server
```bash
python c:\Users\HomeLaptop\Downloads\navi-tax-35-main\ml\ml_api_service_optimized.py
```

The API will be available at: **http://localhost:5001**

---

## 📡 API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running and models are loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_dir": "optimized_models_25000_samples",
  "uptime_seconds": 123.45
}
```

---

### 2. Model Information
**GET** `/model-info`

Get details about the trained model.

**Response:**
```json
{
  "model_name": "Random Forest",
  "r2_score": 0.7026,
  "rmse": 6032.07,
  "mae": 3380.51,
  "training_samples": 20000,
  "testing_samples": 5000,
  "features": 12,
  "hyperparameter_tuning": "RandomizedSearchCV with 3-fold CV"
}
```

---

### 3. Predict VAT Refund
**POST** `/predict`

Get VAT refund prediction for a single transaction.

**Request Body:**
```json
{
  "Amount": 100000,
  "VAT_Rate": 18.0,
  "Category": "Electronics",
  "Region": "South",
  "Filing_Status": "Filed",
  "Compliance_Flag": "Compliant",
  "Refund_Eligible": "Yes",
  "Is_Anomaly": "No",
  "Risk_Score": 0.2,
  "Annual_Turnover": 5000000
}
```

**Response:**
```json
{
  "success": true,
  "predicted_refund_amount": 8290.25,
  "recommendation": "auto_approve",
  "reason": "Low risk, compliant",
  "confidence": "high",
  "response_time_ms": 68.19,
  "model_info": {
    "model_name": "Random Forest",
    "r2_score": 0.7026,
    "mae": 3380.51
  }
}
```

---

### 4. Batch Predictions
**POST** `/batch-predict`

Get predictions for multiple transactions at once.

**Request Body:**
```json
{
  "transactions": [
    {
      "Amount": 100000,
      "VAT_Rate": 18.0,
      "Category": "Electronics",
      "Region": "South",
      "Filing_Status": "Filed",
      "Compliance_Flag": "Compliant",
      "Refund_Eligible": "Yes",
      "Is_Anomaly": "No",
      "Risk_Score": 0.2,
      "Annual_Turnover": 5000000
    },
    {
      "Amount": 200000,
      "VAT_Rate": 18.0,
      "Category": "Manufacturing",
      "Region": "West",
      "Filing_Status": "Filed",
      "Compliance_Flag": "Compliant",
      "Refund_Eligible": "Yes",
      "Is_Anomaly": "No",
      "Risk_Score": 0.3,
      "Annual_Turnover": 10000000
    }
  ]
}
```

---

### 5. Statistics
**GET** `/stats`

Get API usage statistics.

**Response:**
```json
{
  "total_predictions": 150,
  "successful_predictions": 145,
  "failed_predictions": 5,
  "avg_response_time_ms": 65.3,
  "auto_approved": 120,
  "manual_review": 25,
  "uptime_hours": 2.5
}
```

---

## 💻 Integration Examples

### JavaScript (Fetch API)

```javascript
// Predict VAT Refund
async function predictVATRefund(transactionData) {
  try {
    const response = await fetch('http://localhost:5001/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        Amount: transactionData.amount,
        VAT_Rate: transactionData.vatRate,
        Category: transactionData.category,
        Region: transactionData.region,
        Filing_Status: transactionData.filingStatus || 'Filed',
        Compliance_Flag: transactionData.complianceFlag || 'Compliant',
        Refund_Eligible: transactionData.refundEligible || 'Yes',
        Is_Anomaly: transactionData.isAnomaly || 'No',
        Risk_Score: transactionData.riskScore || 0.2,
        Annual_Turnover: transactionData.annualTurnover
      })
    });

    const result = await response.json();
    
    if (result.success) {
      console.log('Predicted Refund:', result.predicted_refund_amount);
      console.log('Recommendation:', result.recommendation);
      return result;
    } else {
      console.error('Prediction failed:', result.error);
      return null;
    }
  } catch (error) {
    console.error('API Error:', error);
    return null;
  }
}

// Example usage
const transaction = {
  amount: 100000,
  vatRate: 18.0,
  category: 'Electronics',
  region: 'South',
  filingStatus: 'Filed',
  complianceFlag: 'Compliant',
  refundEligible: 'Yes',
  isAnomaly: 'No',
  riskScore: 0.2,
  annualTurnover: 5000000
};

predictVATRefund(transaction).then(result => {
  if (result) {
    document.getElementById('refund-amount').textContent = 
      `₹${result.predicted_refund_amount.toFixed(2)}`;
    document.getElementById('recommendation').textContent = 
      result.recommendation === 'auto_approve' ? '✅ Auto-Approve' : '⚠️ Manual Review';
  }
});
```

---

### jQuery (AJAX)

```javascript
function predictVATRefund(transactionData) {
  $.ajax({
    url: 'http://localhost:5001/predict',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
      Amount: transactionData.amount,
      VAT_Rate: transactionData.vatRate,
      Category: transactionData.category,
      Region: transactionData.region,
      Filing_Status: 'Filed',
      Compliance_Flag: 'Compliant',
      Refund_Eligible: 'Yes',
      Is_Anomaly: 'No',
      Risk_Score: transactionData.riskScore || 0.2,
      Annual_Turnover: transactionData.annualTurnover
    }),
    success: function(result) {
      if (result.success) {
        $('#refund-amount').text('₹' + result.predicted_refund_amount.toFixed(2));
        $('#recommendation').text(
          result.recommendation === 'auto_approve' ? '✅ Auto-Approve' : '⚠️ Manual Review'
        );
      }
    },
    error: function(xhr, status, error) {
      console.error('API Error:', error);
      alert('Failed to get prediction. Please try again.');
    }
  });
}
```

---

### PHP (cURL)

```php
<?php
function predictVATRefund($transactionData) {
    $url = 'http://localhost:5001/predict';
    
    $data = array(
        'Amount' => $transactionData['amount'],
        'VAT_Rate' => $transactionData['vat_rate'],
        'Category' => $transactionData['category'],
        'Region' => $transactionData['region'],
        'Filing_Status' => 'Filed',
        'Compliance_Flag' => 'Compliant',
        'Refund_Eligible' => 'Yes',
        'Is_Anomaly' => 'No',
        'Risk_Score' => $transactionData['risk_score'] ?? 0.2,
        'Annual_Turnover' => $transactionData['annual_turnover']
    );
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($response, true);
}

// Example usage
$transaction = array(
    'amount' => 100000,
    'vat_rate' => 18.0,
    'category' => 'Electronics',
    'region' => 'South',
    'risk_score' => 0.2,
    'annual_turnover' => 5000000
);

$result = predictVATRefund($transaction);

if ($result['success']) {
    echo "Predicted Refund: ₹" . number_format($result['predicted_refund_amount'], 2);
    echo "\nRecommendation: " . $result['recommendation'];
}
?>
```

---

### Python (Requests)

```python
import requests

def predict_vat_refund(transaction_data):
    url = 'http://localhost:5001/predict'
    
    payload = {
        'Amount': transaction_data['amount'],
        'VAT_Rate': transaction_data['vat_rate'],
        'Category': transaction_data['category'],
        'Region': transaction_data['region'],
        'Filing_Status': 'Filed',
        'Compliance_Flag': 'Compliant',
        'Refund_Eligible': 'Yes',
        'Is_Anomaly': 'No',
        'Risk_Score': transaction_data.get('risk_score', 0.2),
        'Annual_Turnover': transaction_data['annual_turnover']
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# Example usage
transaction = {
    'amount': 100000,
    'vat_rate': 18.0,
    'category': 'Electronics',
    'region': 'South',
    'risk_score': 0.2,
    'annual_turnover': 5000000
}

result = predict_vat_refund(transaction)

if result['success']:
    print(f"Predicted Refund: ₹{result['predicted_refund_amount']:,.2f}")
    print(f"Recommendation: {result['recommendation']}")
```

---

## 🎨 HTML Form Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>VAT Refund Predictor</title>
    <style>
        .container { max-width: 600px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px; }
        .success { color: #28a745; }
        .warning { color: #ffc107; }
    </style>
</head>
<body>
    <div class="container">
        <h1>VAT Refund Predictor</h1>
        
        <form id="vatForm">
            <div class="form-group">
                <label>Transaction Amount (₹)</label>
                <input type="number" id="amount" required>
            </div>
            
            <div class="form-group">
                <label>VAT Rate (%)</label>
                <select id="vatRate" required>
                    <option value="5">5%</option>
                    <option value="12">12%</option>
                    <option value="18" selected>18%</option>
                    <option value="28">28%</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Business Category</label>
                <select id="category" required>
                    <option value="Electronics">Electronics</option>
                    <option value="Manufacturing">Manufacturing</option>
                    <option value="Services">Services</option>
                    <option value="Textiles">Textiles</option>
                    <option value="Pharmaceuticals">Pharmaceuticals</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Region</label>
                <select id="region" required>
                    <option value="North">North</option>
                    <option value="South">South</option>
                    <option value="East">East</option>
                    <option value="West">West</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Annual Turnover (₹)</label>
                <input type="number" id="turnover" required>
            </div>
            
            <button type="submit">Predict Refund</button>
        </form>
        
        <div id="result" class="result" style="display:none;">
            <h3>Prediction Result</h3>
            <p><strong>Predicted Refund:</strong> <span id="refundAmount"></span></p>
            <p><strong>Recommendation:</strong> <span id="recommendation"></span></p>
            <p><strong>Reason:</strong> <span id="reason"></span></p>
        </div>
    </div>
    
    <script>
        document.getElementById('vatForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const data = {
                Amount: parseFloat(document.getElementById('amount').value),
                VAT_Rate: parseFloat(document.getElementById('vatRate').value),
                Category: document.getElementById('category').value,
                Region: document.getElementById('region').value,
                Filing_Status: 'Filed',
                Compliance_Flag: 'Compliant',
                Refund_Eligible: 'Yes',
                Is_Anomaly: 'No',
                Risk_Score: 0.2,
                Annual_Turnover: parseFloat(document.getElementById('turnover').value)
            };
            
            try {
                const response = await fetch('http://localhost:5001/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('refundAmount').textContent = 
                        '₹' + result.predicted_refund_amount.toFixed(2);
                    
                    const recElement = document.getElementById('recommendation');
                    recElement.textContent = result.recommendation === 'auto_approve' 
                        ? '✅ Auto-Approve' : '⚠️ Manual Review';
                    recElement.className = result.recommendation === 'auto_approve' 
                        ? 'success' : 'warning';
                    
                    document.getElementById('reason').textContent = result.reason;
                    document.getElementById('result').style.display = 'block';
                } else {
                    alert('Prediction failed: ' + result.error);
                }
            } catch (error) {
                alert('Error connecting to API: ' + error.message);
            }
        });
    </script>
</body>
</html>
```

---

## 🔧 Field Descriptions

| Field | Type | Required | Description | Example Values |
|-------|------|----------|-------------|----------------|
| `Amount` | Number | Yes | Transaction amount in ₹ | 100000 |
| `VAT_Rate` | Number | Yes | VAT rate percentage | 5, 12, 18, 28 |
| `Category` | String | Yes | Business category | Electronics, Manufacturing, Services, Textiles, Pharmaceuticals |
| `Region` | String | Yes | Geographic region | North, South, East, West |
| `Filing_Status` | String | Yes | Tax filing status | Filed, Not Filed, Pending |
| `Compliance_Flag` | String | Yes | Compliance status | Compliant, Non-Compliant |
| `Refund_Eligible` | String | Yes | Refund eligibility | Yes, No |
| `Is_Anomaly` | String | Yes | Anomaly detection flag | Yes, No |
| `Risk_Score` | Number | Yes | Risk score (0.0 to 1.0) | 0.2 |
| `Annual_Turnover` | Number | Yes | Annual business turnover in ₹ | 5000000 |

---

## ⚠️ Error Handling

### Common Errors

**1. Missing Fields**
```json
{
  "error": "Missing required fields",
  "missing_fields": ["Amount", "VAT_Rate"]
}
```

**2. Invalid Data**
```json
{
  "error": "Invalid data type",
  "field": "Amount",
  "expected": "number"
}
```

**3. Model Not Loaded**
```json
{
  "error": "Models not loaded",
  "status": 503
}
```

### Error Handling Example

```javascript
async function predictWithErrorHandling(data) {
  try {
    const response = await fetch('http://localhost:5001/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Prediction failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Prediction error:', error);
    
    // Show user-friendly message
    if (error.message.includes('Missing required fields')) {
      alert('Please fill in all required fields');
    } else if (error.message.includes('Models not loaded')) {
      alert('Service is starting up. Please try again in a moment.');
    } else {
      alert('An error occurred. Please try again.');
    }
    
    return null;
  }
}
```

---

## 🧪 Testing

### Test with cURL (PowerShell)

```powershell
# Test prediction
$body = @{
    Amount = 100000
    VAT_Rate = 18.0
    Category = "Electronics"
    Region = "South"
    Filing_Status = "Filed"
    Compliance_Flag = "Compliant"
    Refund_Eligible = "Yes"
    Is_Anomaly = "No"
    Risk_Score = 0.2
    Annual_Turnover = 5000000
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri "http://localhost:5001/predict" -Body $body -ContentType "application/json"
```

### Test with cURL (Linux/Mac)

```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Amount": 100000,
    "VAT_Rate": 18.0,
    "Category": "Electronics",
    "Region": "South",
    "Filing_Status": "Filed",
    "Compliance_Flag": "Compliant",
    "Refund_Eligible": "Yes",
    "Is_Anomaly": "No",
    "Risk_Score": 0.2,
    "Annual_Turnover": 5000000
  }'
```

---

## 📊 Response Interpretation

### Recommendation Types

| Recommendation | Meaning | Action |
|---------------|---------|--------|
| `auto_approve` | Low risk, compliant transaction | Automatically approve refund |
| `manual_review` | High risk or non-compliant | Requires manual review |

### Confidence Levels

| Confidence | Meaning |
|-----------|---------|
| `high` | Model is confident in prediction (R² > 0.7) |
| `medium` | Moderate confidence (R² 0.5-0.7) |
| `low` | Low confidence (R² < 0.5) |

---

## 🚀 Production Deployment

### For Production Use:

1. **Change localhost to your server IP/domain**
   ```javascript
   const API_URL = 'https://your-domain.com/api/predict';
   ```

2. **Add authentication** (if needed)
   ```javascript
   headers: {
     'Content-Type': 'application/json',
     'Authorization': 'Bearer YOUR_API_KEY'
   }
   ```

3. **Use HTTPS** for secure communication

4. **Add rate limiting** to prevent abuse

5. **Monitor API performance** using the `/stats` endpoint

---

## 📞 Support

For issues or questions:
- Check API health: `GET http://localhost:5001/health`
- View logs: `c:\Users\HomeLaptop\Downloads\navi-tax-35-main\logs\ml_api_optimized.log`
- Test models: `python ml/test_optimized_model.py`

---

## ✅ Quick Checklist

- [ ] API server is running (`python ml/ml_api_service_optimized.py`)
- [ ] Health check passes (`GET /health`)
- [ ] Test prediction works (`POST /predict`)
- [ ] Website can connect to API
- [ ] Error handling is implemented
- [ ] Results are displayed correctly

---

**🎉 Your ML API is ready for integration!**