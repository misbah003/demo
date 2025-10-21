# 🛡️ ML API INPUT VALIDATION GUIDE

## Overview

The ML API now includes **strict input validation** using Pydantic schemas. This ensures:
- ✅ Only valid categorical values are accepted
- ✅ Clear, actionable error messages for invalid inputs
- ✅ No silent failures or defaults to wrong categories
- ✅ Early detection of data issues

---

## Quick Start

### Before: Silent Failure ❌
```json
{
  "Filing_Status": "quarterly"  // Not in training data!
}
```
**Result**: API silently defaults to "Late", reducing refund prediction by €1,757

### After: Clear Error ✅
```json
{
  "Filing_Status": "quarterly"
}
```
**Result**: 
```json
{
  "error": "Invalid input data",
  "details": "Invalid Filing_Status: 'quarterly'. Must be one of: Late, On Time, Very Late",
  "status": "validation_error",
  "valid_categories": {...}
}
```

---

## Valid Input Values

### 📋 Filing Status
- `"On Time"` - ✅ Good (no penalty)
- `"Late"` - ⚠️ Penalty applied
- `"Very Late"` - 🔴 Heavy penalty

### 🏛️ Compliance Flag
- `"Compliant"` - ✅ Good
- `"Non-Compliant"` - 🔴 Bad (manual review)
- `"Under Review"` - 🟡 Neutral

### 💰 Refund Eligible
- `"Yes"` - ✅ Eligible
- `"No"` - 🔴 Not eligible

### 🚨 Anomaly Detection
- `"No"` - ✅ Normal
- `"Yes"` - 🔴 Anomaly detected (triggers manual review)

### 🌍 Region
- `"East"` - 
- `"North"` - 
- `"South"` - 
- `"West"` - 

### 🏪 Category (Product/Service Type)
- `"Retail"` - Retail businesses
- `"Manufacturing"` - Manufacturing sector
- `"Hospitality"` - Hotels, restaurants
- `"IT Services"` - IT/Software services
- `"Pharmaceuticals"` - Pharma sector
- `"Healthcare"` - Hospitals, clinics
- `"Education"` - Schools, universities
- `"FMCG"` - Fast-moving consumer goods
- `"Real Estate"` - Real estate sector
- `"Others"` - Other sectors

---

## Numeric Field Constraints

| Field | Type | Min | Max | Description |
|-------|------|-----|-----|-------------|
| Amount | float | > 0 | unlimited | Refund amount in EUR |
| VAT_Rate | float | 0 | 100 | VAT rate as percentage |
| Risk_Score | float | 0 | 1 | Risk assessment score |
| Annual_Turnover | float | 0 | unlimited | Annual business turnover in EUR |

---

## API Endpoints

### 1️⃣ GET `/validation-reference`
Get complete reference of valid values for all fields.

**Response:**
```json
{
  "valid_categories": {
    "Category": ["Education", "FMCG", "Healthcare", ...],
    "Compliance_Flag": ["Compliant", "Non-Compliant", "Under Review"],
    "Filing_Status": ["Late", "On Time", "Very Late"],
    "Is_Anomaly": ["No", "Yes"],
    "Refund_Eligible": ["No", "Yes"],
    "Region": ["East", "North", "South", "West"]
  },
  "field_descriptions": {...},
  "example_request": {...}
}
```

**Use Case**: Auto-complete, dropdown population, client-side validation

---

### 2️⃣ POST `/predict`
Make a VAT refund prediction with validation.

**Request:**
```json
{
  "Amount": 50000,
  "VAT_Rate": 19,
  "Risk_Score": 0.3,
  "Annual_Turnover": 500000,
  "Category": "Retail",
  "Region": "East",
  "Filing_Status": "On Time",
  "Compliance_Flag": "Compliant",
  "Refund_Eligible": "Yes",
  "Is_Anomaly": "No"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "predicted_refund_amount": 4751.76,
  "recommendation": "auto_approve",
  "reason": "Low risk, compliant",
  "confidence": "high",
  "model_info": {
    "model_name": "Random Forest",
    "r2_score": 0.70,
    "mae": 3380.51
  },
  "response_time_ms": 45.23
}
```

**Validation Error (400):**
```json
{
  "error": "Invalid input data",
  "details": "Invalid Filing_Status: 'quarterly'. Must be one of: Late, On Time, Very Late",
  "status": "validation_error",
  "valid_categories": {...}
}
```

**Numeric Error (400):**
```json
{
  "error": "Invalid input data",
  "details": "ensure this value is greater than 0 (type=value_error.number.not_gt; limit_value=0)",
  "status": "validation_error",
  "valid_categories": {...}
}
```

---

### 3️⃣ POST `/explain`
Get SHAP explanation with validation.

**Request:** (Same schema as `/predict`)

**Success Response (200):**
```json
{
  "success": true,
  "prediction": 4751.76,
  "base_value": 6409.26,
  "method": "SHAP",
  "top_features": [
    {
      "feature": "Annual_Turnover",
      "value": -0.245,
      "shap_value": 1245.32,
      "contribution": 305.10
    },
    ...
  ],
  "all_features": [...],
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Validation Error:** Same as `/predict`

---

### 4️⃣ POST `/batch-predict`
Predict for multiple transactions with validation.

**Request:**
```json
{
  "transactions": [
    { /* valid prediction request */ },
    { /* valid prediction request */ }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "total_transactions": 2,
  "successful_predictions": 2,
  "results": [
    { /* prediction 1 */ },
    { /* prediction 2 */ }
  ]
}
```

---

## Error Handling Guide

### Invalid Category Value
```json
{
  "error": "Invalid input data",
  "details": "Invalid Category: 'goods'. Must be one of: Education, FMCG, Healthcare, Hospitality, IT Services, Manufacturing, Others, Pharmaceuticals, Real Estate, Retail",
  "status": "validation_error"
}
```

**Fix**: Use one of the valid categories listed in the error message.

---

### Invalid Region
```json
{
  "error": "Invalid input data",
  "details": "Invalid Region: 'EU'. Must be one of: East, North, South, West",
  "status": "validation_error"
}
```

**Fix**: Use one of: East, North, South, West

---

### Invalid Filing Status
```json
{
  "error": "Invalid input data",
  "details": "Invalid Filing_Status: 'quarterly'. Must be one of: Late, On Time, Very Late",
  "status": "validation_error"
}
```

**Fix**: Use one of: On Time, Late, Very Late

---

### Missing Required Field
```json
{
  "error": "Invalid input data",
  "details": "field required",
  "status": "validation_error"
}
```

**Fix**: Ensure all 10 required fields are present

---

### Numeric Value Out of Range
```json
{
  "error": "Invalid input data",
  "details": "ensure this value is less than or equal to 100 (type=value_error.number.not_le; limit_value=100)",
  "status": "validation_error"
}
```

**Fix**: For VAT_Rate, use 0-100. For Risk_Score, use 0-1.

---

### Invalid Amount
```json
{
  "error": "Invalid input data",
  "details": "ensure this value is greater than 0 (type=value_error.number.not_gt; limit_value=0)",
  "status": "validation_error"
}
```

**Fix**: Amount must be positive (> 0)

---

## Integration Examples

### Python (requests)
```python
import requests

# Get validation reference
ref = requests.get('http://localhost:8000/validation-reference').json()
print(ref['valid_categories'])

# Make prediction with validation
data = {
    "Amount": 50000,
    "VAT_Rate": 19,
    "Risk_Score": 0.3,
    "Annual_Turnover": 500000,
    "Category": "Retail",  # Use valid value from reference
    "Region": "East",
    "Filing_Status": "On Time",
    "Compliance_Flag": "Compliant",
    "Refund_Eligible": "Yes",
    "Is_Anomaly": "No"
}

response = requests.post('http://localhost:8000/predict', json=data)
if response.status_code == 200:
    print(f"Prediction: €{response.json()['predicted_refund_amount']:,.2f}")
else:
    print(f"Error: {response.json()['details']}")
    # Use response.json()['valid_categories'] to show user valid values
```

### JavaScript (fetch)
```javascript
// Get validation reference
const ref = await fetch('http://localhost:8000/validation-reference')
  .then(r => r.json());

// Build dropdown from valid categories
const categorySelect = document.getElementById('category');
ref.valid_categories.Category.forEach(cat => {
  const option = document.createElement('option');
  option.value = cat;
  option.text = cat;
  categorySelect.appendChild(option);
});

// Make prediction
const data = {
  Amount: 50000,
  VAT_Rate: 19,
  Risk_Score: 0.3,
  Annual_Turnover: 500000,
  Category: categorySelect.value,
  Region: "East",
  Filing_Status: "On Time",
  Compliance_Flag: "Compliant",
  Refund_Eligible: "Yes",
  Is_Anomaly: "No"
};

const response = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
});

const result = await response.json();
if (response.ok) {
  console.log(`Prediction: €${result.predicted_refund_amount.toFixed(2)}`);
} else {
  console.error(result.details);
}
```

### cURL
```bash
# Get validation reference
curl http://localhost:8000/validation-reference

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Amount": 50000,
    "VAT_Rate": 19,
    "Risk_Score": 0.3,
    "Annual_Turnover": 500000,
    "Category": "Retail",
    "Region": "East",
    "Filing_Status": "On Time",
    "Compliance_Flag": "Compliant",
    "Refund_Eligible": "Yes",
    "Is_Anomaly": "No"
  }'
```

---

## Testing with test_shap.http

The `test_shap.http` file has been updated to use valid categories:

```http
POST http://localhost:8000/explain
Content-Type: application/json

{
  "Amount": 50000,
  "VAT_Rate": 19,
  "Risk_Score": 0.3,
  "Annual_Turnover": 500000,
  "Category": "Retail",
  "Region": "East",
  "Filing_Status": "On Time",
  "Compliance_Flag": "Compliant",
  "Refund_Eligible": "Yes",
  "Is_Anomaly": "No"
}
```

Use in VS Code REST Client:
1. Install REST Client extension
2. Open `test_shap.http`
3. Click "Send Request"
4. See validated response

---

## Migration Checklist

If updating existing integrations:

- [ ] Update all Category values to valid options
- [ ] Update all Region values to valid options
- [ ] Update all Filing_Status values to valid options
- [ ] Update all Compliance_Flag values to valid options
- [ ] Add error handling for validation_error status
- [ ] Display valid_categories to user when validation fails
- [ ] Test with `/validation-reference` endpoint
- [ ] Update client-side dropdowns/selects with valid values
- [ ] Test batch operations with mixed valid/invalid data
- [ ] Monitor logs for validation errors

---

## Benefits Summary

| Before | After |
|--------|-------|
| Silent defaults to wrong values | Clear validation errors |
| Mysterious low predictions | Obvious cause (invalid input) |
| No guidance on valid values | Reference endpoint provided |
| Difficult debugging | Actionable error messages |
| Missing fields ignored | All required fields checked |
| No numeric constraints | Range validation on all numbers |

---

## Support

If you encounter validation errors:

1. Call `/validation-reference` to see all valid values
2. Check error message for list of valid options
3. Update your input data
4. Retry the request

For example, if you see:
```
"Invalid Region: 'EU'. Must be one of: East, North, South, West"
```

Change your Region value from "EU" to one of: "East", "North", "South", or "West"

---

## File Changes Summary

| File | Changes |
|------|---------|
| `ml/validation.py` | ✅ New validation module |
| `ml/ml_api_service_optimized.py` | ✅ Updated with validation |
| `test_shap.http` | ✅ Updated to use valid categories |
| `VALIDATE_GOOD_SCENARIO.py` | ✅ Updated test data |

---

**Last Updated**: 2024  
**Validation Framework**: Pydantic v2  
**API Version**: v1.0