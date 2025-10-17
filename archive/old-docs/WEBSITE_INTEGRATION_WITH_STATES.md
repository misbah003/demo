# 🌐 VAT Refund Predictor - Website Integration Guide (with Indian States)

## 📋 Overview

This guide shows you how to integrate the VAT Refund Predictor into your website with **all Indian states** in the dropdown instead of regions.

---

## 🎯 Quick Start - 3 Options

### **Option 1: Use the Complete HTML Page** ⭐ EASIEST

Simply use the ready-made page:

```html
<!-- Just open this file in your browser or embed it in your website -->
vat_refund_widget.html
```

**Features:**
- ✅ Beautiful UI with gradient design
- ✅ All 36 Indian states and UTs in dropdown
- ✅ Automatic state-to-region mapping
- ✅ Real-time API integration
- ✅ Loading animations
- ✅ Error handling
- ✅ Mobile responsive

---

### **Option 2: Use the JavaScript Module** ⭐ RECOMMENDED

Include the JavaScript module in your existing website:

```html
<!-- Include the module -->
<script src="vat_predictor.js"></script>

<!-- Use it in your code -->
<script>
async function predictRefund() {
    try {
        const result = await VATPredictor.predict({
            amount: 100000,
            vatRate: 18,
            category: 'Electronics',
            state: 'Maharashtra',  // Use state name instead of region
            annualTurnover: 5000000,
            riskScore: 0.2,
            compliance: 'Compliant'
        });
        
        console.log('Refund:', VATPredictor.formatCurrency(result.predicted_refund_amount));
        console.log('Recommendation:', result.recommendation);
    } catch (error) {
        console.error('Error:', error.message);
    }
}
</script>
```

---

### **Option 3: Copy-Paste Integration**

Copy the form HTML and JavaScript into your existing page.

---

## 📝 Complete Integration Example

### **HTML Form with All Indian States**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VAT Refund Calculator</title>
    <style>
        /* Your existing styles */
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #5568d3;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: #f0f0f0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>VAT Refund Calculator</h1>
    
    <form id="vatForm">
        <div class="form-group">
            <label for="amount">Transaction Amount (₹)</label>
            <input type="number" id="amount" required min="1">
        </div>

        <div class="form-group">
            <label for="vatRate">VAT Rate (%)</label>
            <select id="vatRate" required>
                <option value="5">5%</option>
                <option value="12">12%</option>
                <option value="18" selected>18%</option>
                <option value="28">28%</option>
            </select>
        </div>

        <div class="form-group">
            <label for="category">Business Category</label>
            <select id="category" required>
                <option value="Electronics">Electronics</option>
                <option value="Manufacturing">Manufacturing</option>
                <option value="Services">Services</option>
                <option value="Textiles">Textiles</option>
                <option value="Pharmaceuticals">Pharmaceuticals</option>
                <option value="Food & Beverages">Food & Beverages</option>
                <option value="Automotive">Automotive</option>
            </select>
        </div>

        <div class="form-group">
            <label for="state">State</label>
            <select id="state" required>
                <option value="">-- Select State --</option>
                <option value="Andhra Pradesh">Andhra Pradesh</option>
                <option value="Arunachal Pradesh">Arunachal Pradesh</option>
                <option value="Assam">Assam</option>
                <option value="Bihar">Bihar</option>
                <option value="Chhattisgarh">Chhattisgarh</option>
                <option value="Goa">Goa</option>
                <option value="Gujarat">Gujarat</option>
                <option value="Haryana">Haryana</option>
                <option value="Himachal Pradesh">Himachal Pradesh</option>
                <option value="Jharkhand">Jharkhand</option>
                <option value="Karnataka">Karnataka</option>
                <option value="Kerala">Kerala</option>
                <option value="Madhya Pradesh">Madhya Pradesh</option>
                <option value="Maharashtra">Maharashtra</option>
                <option value="Manipur">Manipur</option>
                <option value="Meghalaya">Meghalaya</option>
                <option value="Mizoram">Mizoram</option>
                <option value="Nagaland">Nagaland</option>
                <option value="Odisha">Odisha</option>
                <option value="Punjab">Punjab</option>
                <option value="Rajasthan">Rajasthan</option>
                <option value="Sikkim">Sikkim</option>
                <option value="Tamil Nadu">Tamil Nadu</option>
                <option value="Telangana">Telangana</option>
                <option value="Tripura">Tripura</option>
                <option value="Uttar Pradesh">Uttar Pradesh</option>
                <option value="Uttarakhand">Uttarakhand</option>
                <option value="West Bengal">West Bengal</option>
                <option value="Andaman and Nicobar Islands">Andaman and Nicobar Islands</option>
                <option value="Chandigarh">Chandigarh</option>
                <option value="Dadra and Nagar Haveli and Daman and Diu">Dadra and Nagar Haveli and Daman and Diu</option>
                <option value="Delhi">Delhi</option>
                <option value="Jammu and Kashmir">Jammu and Kashmir</option>
                <option value="Ladakh">Ladakh</option>
                <option value="Lakshadweep">Lakshadweep</option>
                <option value="Puducherry">Puducherry</option>
            </select>
        </div>

        <div class="form-group">
            <label for="turnover">Annual Turnover (₹)</label>
            <input type="number" id="turnover" required min="1">
        </div>

        <div class="form-group">
            <label for="riskScore">Risk Score (0.0 - 1.0)</label>
            <input type="number" id="riskScore" step="0.1" min="0" max="1" value="0.2" required>
        </div>

        <div class="form-group">
            <label for="compliance">Compliance Status</label>
            <select id="compliance" required>
                <option value="Compliant" selected>Compliant</option>
                <option value="Non-Compliant">Non-Compliant</option>
            </select>
        </div>

        <button type="submit">Calculate Refund</button>
    </form>

    <div id="result" class="result" style="display: none;">
        <h2>Prediction Result</h2>
        <p><strong>Refund Amount:</strong> <span id="refundAmount"></span></p>
        <p><strong>Recommendation:</strong> <span id="recommendation"></span></p>
        <p><strong>Reason:</strong> <span id="reason"></span></p>
    </div>

    <script>
        const API_URL = 'http://localhost:5001';

        // State to Region mapping
        const stateToRegion = {
            // North
            'Delhi': 'North', 'Haryana': 'North', 'Himachal Pradesh': 'North',
            'Jammu and Kashmir': 'North', 'Ladakh': 'North', 'Punjab': 'North',
            'Rajasthan': 'North', 'Uttar Pradesh': 'North', 'Uttarakhand': 'North',
            'Chandigarh': 'North',
            
            // South
            'Andhra Pradesh': 'South', 'Karnataka': 'South', 'Kerala': 'South',
            'Tamil Nadu': 'South', 'Telangana': 'South', 'Puducherry': 'South',
            'Lakshadweep': 'South', 'Andaman and Nicobar Islands': 'South',
            
            // East
            'Bihar': 'East', 'Jharkhand': 'East', 'Odisha': 'East',
            'West Bengal': 'East', 'Assam': 'East', 'Arunachal Pradesh': 'East',
            'Manipur': 'East', 'Meghalaya': 'East', 'Mizoram': 'East',
            'Nagaland': 'East', 'Sikkim': 'East', 'Tripura': 'East',
            
            // West
            'Goa': 'West', 'Gujarat': 'West', 'Maharashtra': 'West',
            'Chhattisgarh': 'West', 'Madhya Pradesh': 'West',
            'Dadra and Nagar Haveli and Daman and Diu': 'West'
        };

        document.getElementById('vatForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const selectedState = document.getElementById('state').value;
            const region = stateToRegion[selectedState] || 'North';
            
            const data = {
                Amount: parseFloat(document.getElementById('amount').value),
                VAT_Rate: parseFloat(document.getElementById('vatRate').value),
                Category: document.getElementById('category').value,
                Region: region,
                Filing_Status: 'Filed',
                Compliance_Flag: document.getElementById('compliance').value,
                Refund_Eligible: 'Yes',
                Is_Anomaly: 'No',
                Risk_Score: parseFloat(document.getElementById('riskScore').value),
                Annual_Turnover: parseFloat(document.getElementById('turnover').value)
            };
            
            try {
                const response = await fetch(`${API_URL}/predict`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('refundAmount').textContent = 
                        '₹' + result.predicted_refund_amount.toLocaleString('en-IN', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        });
                    document.getElementById('recommendation').textContent = 
                        result.recommendation === 'auto_approve' ? '✅ Auto-Approve' : '⚠️ Manual Review';
                    document.getElementById('reason').textContent = result.reason;
                    document.getElementById('result').style.display = 'block';
                } else {
                    alert('Error: ' + (result.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Failed to connect to API: ' + error.message);
            }
        });
    </script>
</body>
</html>
```

---

## 🗺️ State to Region Mapping

The API expects regions (North/South/East/West), but your form uses states. The mapping is automatic:

| Region | States |
|--------|--------|
| **North** | Delhi, Haryana, Himachal Pradesh, Jammu and Kashmir, Ladakh, Punjab, Rajasthan, Uttar Pradesh, Uttarakhand, Chandigarh |
| **South** | Andhra Pradesh, Karnataka, Kerala, Tamil Nadu, Telangana, Puducherry, Lakshadweep, Andaman and Nicobar Islands |
| **East** | Bihar, Jharkhand, Odisha, West Bengal, Assam, Arunachal Pradesh, Manipur, Meghalaya, Mizoram, Nagaland, Sikkim, Tripura |
| **West** | Goa, Gujarat, Maharashtra, Chhattisgarh, Madhya Pradesh, Dadra and Nagar Haveli and Daman and Diu |

---

## 🚀 Using the JavaScript Module

### **1. Include the Module**

```html
<script src="vat_predictor.js"></script>
```

### **2. Make a Prediction**

```javascript
// Simple prediction
const result = await VATPredictor.predict({
    amount: 100000,
    vatRate: 18,
    category: 'Electronics',
    state: 'Maharashtra',  // Use state name
    annualTurnover: 5000000,
    riskScore: 0.2,
    compliance: 'Compliant'
});

console.log('Refund:', result.predicted_refund_amount);
console.log('Recommendation:', result.recommendation);
```

### **3. Get All States**

```javascript
const states = VATPredictor.getStates();
console.log(states);  // Array of all 36 states/UTs
```

### **4. Convert State to Region**

```javascript
const region = VATPredictor.stateToRegion('Maharashtra');
console.log(region);  // 'West'
```

### **5. Format Currency**

```javascript
const formatted = VATPredictor.formatCurrency(8290.25);
console.log(formatted);  // '₹8,290.25'
```

### **6. Check API Health**

```javascript
const health = await VATPredictor.checkHealth();
console.log(health.status);  // 'healthy'
```

### **7. Batch Predictions**

```javascript
const results = await VATPredictor.batchPredict([
    {
        amount: 100000,
        vatRate: 18,
        category: 'Electronics',
        state: 'Maharashtra',
        annualTurnover: 5000000
    },
    {
        amount: 200000,
        vatRate: 12,
        category: 'Services',
        state: 'Karnataka',
        annualTurnover: 8000000
    }
]);

console.log(results);  // Array of predictions
```

---

## 📱 React Integration Example

```jsx
import React, { useState, useEffect } from 'react';

function VATRefundCalculator() {
    const [states, setStates] = useState([]);
    const [formData, setFormData] = useState({
        amount: '',
        vatRate: '18',
        category: 'Electronics',
        state: '',
        annualTurnover: '',
        riskScore: '0.2',
        compliance: 'Compliant'
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Load states
        setStates(VATPredictor.getStates());
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const prediction = await VATPredictor.predict({
                amount: parseFloat(formData.amount),
                vatRate: parseFloat(formData.vatRate),
                category: formData.category,
                state: formData.state,
                annualTurnover: parseFloat(formData.annualTurnover),
                riskScore: parseFloat(formData.riskScore),
                compliance: formData.compliance
            });

            setResult(prediction);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>VAT Refund Calculator</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="number"
                    placeholder="Amount"
                    value={formData.amount}
                    onChange={(e) => setFormData({...formData, amount: e.target.value})}
                    required
                />

                <select
                    value={formData.state}
                    onChange={(e) => setFormData({...formData, state: e.target.value})}
                    required
                >
                    <option value="">Select State</option>
                    {states.map(state => (
                        <option key={state} value={state}>{state}</option>
                    ))}
                </select>

                {/* Add other fields... */}

                <button type="submit" disabled={loading}>
                    {loading ? 'Calculating...' : 'Calculate Refund'}
                </button>
            </form>

            {result && (
                <div>
                    <h2>Result</h2>
                    <p>Refund: {VATPredictor.formatCurrency(result.predicted_refund_amount)}</p>
                    <p>Recommendation: {result.recommendation}</p>
                </div>
            )}
        </div>
    );
}

export default VATRefundCalculator;
```

---

## 🎨 Styling Tips

### **Beautiful State Dropdown**

```css
select#state {
    width: 100%;
    padding: 12px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 16px;
    background-color: white;
    cursor: pointer;
    transition: border-color 0.3s;
}

select#state:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

select#state option {
    padding: 10px;
}
```

---

## 🔧 Configuration

### **Change API URL for Production**

```javascript
// In vat_predictor.js
VATPredictor.setApiUrl('https://your-domain.com/api');

// Or directly in your code
const API_URL = 'https://your-domain.com/api';
```

---

## ✅ Testing Checklist

- [ ] Open `vat_refund_widget.html` in browser
- [ ] Select a state from dropdown (e.g., Maharashtra)
- [ ] Fill in all fields
- [ ] Click "Predict VAT Refund"
- [ ] Verify result shows correctly
- [ ] Test with different states
- [ ] Test error handling (disconnect API)

---

## 📊 Example Test Data

| Field | Value |
|-------|-------|
| Amount | ₹100,000 |
| VAT Rate | 18% |
| Category | Electronics |
| State | Maharashtra |
| Annual Turnover | ₹5,000,000 |
| Risk Score | 0.2 |
| Compliance | Compliant |

**Expected Result:** ~₹8,290 refund with Auto-Approve recommendation

---

## 🎯 Files Created

1. **`vat_refund_widget.html`** - Complete standalone page with all states
2. **`vat_predictor.js`** - JavaScript module for easy integration
3. **`WEBSITE_INTEGRATION_WITH_STATES.md`** - This guide

---

## 🚀 Next Steps

1. ✅ Open `vat_refund_widget.html` in your browser
2. ✅ Test with different states
3. ✅ Copy the code to your website
4. ✅ Customize the styling to match your brand
5. ✅ Deploy to production

---

## 💡 Pro Tips

1. **State Validation**: The module automatically validates state names
2. **Region Mapping**: States are automatically converted to regions for the API
3. **Error Handling**: Built-in error handling for network issues
4. **Mobile Friendly**: Responsive design works on all devices
5. **Fast Loading**: Optimized for quick page loads

---

## 🎊 You're Ready!

Your VAT Refund Predictor is now integrated with all Indian states! 🇮🇳

**Need help?** Check the example files or contact support.