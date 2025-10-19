# 🔍 Model Explainability Guide

## Overview

This guide explains the **Explainable AI (XAI)** features added to the Navi Tax system. These features provide transparency into ML model predictions using **SHAP** and **LIME** methodologies.

---

## 📊 What is Model Explainability?

Model explainability helps answer the question: **"Why did the model make this prediction?"**

### Key Concepts

| Concept | Description |
|---------|-------------|
| **SHAP Values** | Shows how much each feature contributes to pushing the prediction from base value to actual prediction |
| **LIME** | Local Interpretable Model-agnostic Explanations - creates local interpretable models around a prediction |
| **Feature Importance** | Ranks features by their impact on predictions |
| **Base Value** | The expected model output (average of all predictions) |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ml
pip install -r requirements_advanced_ml.txt
```

New packages added:
- `shap>=0.42.0` - SHAP value calculations
- `lime>=0.2.0` - LIME explanations
- `reportlab>=4.0.0` - PDF report generation

### 2. Start the ML API with Explainability

```bash
python ml_api_with_explainability.py
```

The API will be available at `http://localhost:8000`

### 3. API Endpoints

#### Explain VAT Prediction
```bash
curl -X POST http://localhost:8000/api/explain-vat \
  -H "Content-Type: application/json" \
  -d '{
    "features": {"region": "EU", "category": "services", "amount": 50000},
    "amount": 50000,
    "method": "shap"
  }'
```

**Response:**
```json
{
  "status": "success",
  "method": "SHAP",
  "data": {
    "base_value": 30000,
    "prediction": 50000,
    "feature_contributions": [
      {
        "feature": "amount",
        "shap_value": 15000,
        "importance": 0.5,
        "direction": "positive"
      }
    ]
  }
}
```

#### Explain Document Classification
```bash
curl -X POST http://localhost:8000/api/explain-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Invoice for services rendered...",
    "method": "attention"
  }'
```

#### Explain Anomaly Detection
```bash
curl -X POST http://localhost:8000/api/explain-anomaly \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"feature1": 100, "feature2": 200}
  }'
```

#### Generate Explanation Report
```bash
curl -X POST http://localhost:8000/api/explain-report \
  -H "Content-Type: application/json" \
  -d '{
    "prediction_data": {...},
    "model_name": "vat_predictor",
    "input_summary": {"region": "EU"}
  }'
```

---

## 📈 Features by Model

### VAT Refund Predictor

**What it explains:**
- Why a refund amount was predicted
- Which input features had the most impact
- Whether the prediction is within normal range

**SHAP Visualization:**
```
Base Value: €30,000 (average prediction)
Actual Prediction: €50,000

Feature Contributions:
├─ amount: +€15,000 (positive impact) ✅
├─ region: +€5,000 (EU region bonus) ✅
├─ category: -€2,000 (service deduction) ❌
└─ Other factors: +€2,000
```

**Use Case:**
```
Auditor says: "Why was this refund approved for €50,000?"

Explanation:
1. Base expectation: €30,000
2. Large transaction amount: +€15,000
3. EU region classification: +€5,000
4. Service category adjustment: -€2,000
5. **Final prediction: €50,000** ✅
```

---

### Document Classifier

**What it explains:**
- Which parts of document text influenced the classification
- Attention weights for important tokens
- Confidence in the classification

**Example Output:**
```
Document Type: Invoice (89% confidence)

Top Tokens (by attention weight):
1. "invoice" (0.95) 🎯
2. "payment" (0.87)
3. "services" (0.81)
4. "total" (0.76)
5. "amount" (0.72)

Alternative Classifications:
- Receipt: 8%
- Contract: 2%
- Other: 1%
```

---

### Anomaly Detection

**What it explains:**
- Which features make the transaction anomalous
- Risk score breakdown
- Contributing factors to anomaly

**Risk Assessment:**
```
Anomaly Score: 0.75 (HIGH RISK) ⚠️

Contributing Factors:
├─ Unusual amount: €500,000 (5x average) 📈
├─ New supplier: First transaction
├─ Multiple invoices in 1 hour: 15 items
└─ Total pattern score: 0.75 / 1.0
```

---

## 🎨 React Dashboard Component

### Using ExplainabilityDashboard

```typescript
import ExplainabilityDashboard from '@/components/ExplainabilityDashboard';

export default function PredictionPage() {
  return (
    <ExplainabilityDashboard
      predictionData={{
        features: { region: "EU", category: "services" },
        amount: 50000
      }}
      modelName="vat_predictor"
      onGenerateReport={() => console.log('Generating...')}
    />
  );
}
```

### Features:
- 📊 Interactive charts with Recharts
- 🔄 Switch between SHAP and LIME methods
- 📥 Download PDF reports
- 📋 Detailed feature tables
- ⚠️ Anomaly alerts

---

## 📄 PDF Report Generation

### Generate Reports Programmatically

```python
from pdf_report_generator import PDFReportGenerator

generator = PDFReportGenerator()

explanation = {
    "method": "SHAP",
    "status": "success",
    "prediction": 50000,
    "base_value": 30000,
    "feature_contributions": [...]
}

pdf_path = generator.generate_report(
    explanation_data=explanation,
    model_name="vat_predictor",
    input_summary={"region": "EU", "amount": 50000}
)

print(f"Report saved to: {pdf_path}")
```

### Report Contents:
- ✅ Title and metadata
- 📊 Feature importance charts
- 📈 Prediction breakdown
- 💡 Key insights
- 🎯 Recommendations
- 📋 Full feature table

---

## 🔧 ExplainabilityService API

### Basic Usage

```python
from explainability_service import ExplainabilityService
import pandas as pd

service = ExplainabilityService()

# Prepare data
input_data = pd.DataFrame({
    'amount': [50000],
    'region': [1],  # encoded
    'category': [0]  # encoded
})

# Get SHAP explanation
explanation = service.explain_vat_prediction(
    model=model,
    input_data=input_data,
    feature_names=['amount', 'region', 'category'],
    model_type='random_forest',
    method='shap'
)

# Get LIME explanation
explanation = service.explain_vat_prediction(
    model=model,
    input_data=input_data,
    feature_names=['amount', 'region', 'category'],
    method='lime'
)
```

### Available Methods

| Method | Best For | Speed | Accuracy |
|--------|----------|-------|----------|
| SHAP | Global + Local | Medium | High |
| LIME | Local explanations | Fast | Medium |
| Attention | Deep learning | Fast | Medium |

---

## 📊 Performance Metrics

| Operation | Time | Memory |
|-----------|------|--------|
| Single SHAP explanation | 200-500ms | 100MB |
| Single LIME explanation | 100-300ms | 50MB |
| PDF report generation | 1-2s | 20MB |
| Batch (100 items) SHAP | 20-50s | 200MB |

---

## 🎓 Examples

### Example 1: Audit Trail

```python
# Create audit trail for compliance
explanation = service.explain_vat_prediction(model, data, features)
report = service.generate_explanation_report(
    explanation=explanation,
    model_name="vat_predictor",
    input_summary={"invoice_id": "INV-2024-001"}
)

# Save for audit
with open(f"audit_{invoice_id}.json", "w") as f:
    json.dump(report, f)
```

### Example 2: Model Debugging

```python
# Debug why model made unexpected prediction
if prediction > 100000:
    explanation = service.explain_vat_prediction(model, data, features)
    
    # Check which features caused high prediction
    top_features = explanation['feature_contributions'][:5]
    
    # If caused by data quality issue:
    if 'corrupt_field' in [f['feature'] for f in top_features]:
        print("⚠️ Data quality issue detected")
```

### Example 3: User Explanation

```python
# Generate user-friendly explanation
explanation = service.explain_vat_prediction(model, data, features)
insights = service._generate_insights(explanation)

for insight in insights:
    print(f"💡 {insight}")
# Output:
# 💡 Most influential feature: amount (positive impact)
# 💡 High confidence prediction
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in `ml/` directory:

```env
# Explainability Settings
SHAP_NUM_SAMPLES=100  # Increase for more accurate but slower SHAP
LIME_NUM_SAMPLES=1000  # Samples for LIME explanations
PDF_INCLUDE_CHARTS=true  # Include visualizations in PDF

# Report Settings
REPORTS_DIR=explainability_reports
BATCH_SIZE=10  # Batch processing size
ENABLE_CACHING=true  # Cache explanations
```

---

## 🐛 Troubleshooting

### Issue: "SHAP explainer not initialized"

**Solution:**
```python
# Ensure model is tree-based or linear
if isinstance(model, (RandomForestRegressor, GradientBoostingRegressor)):
    explainer = shap.TreeExplainer(model)
elif isinstance(model, LinearRegression):
    explainer = shap.LinearExplainer(model, training_data)
else:
    # Use KernelExplainer for black-box models
    explainer = shap.KernelExplainer(model.predict, training_data)
```

### Issue: "LIME explanation is inconsistent"

**Solution:**
Increase `num_samples`:
```python
explanation = service.explain_vat_prediction(
    model=model,
    input_data=data,
    features=features,
    method='lime',
    num_samples=5000  # Increase from default 100
)
```

### Issue: "PDF report fails to generate"

**Solution:**
Ensure matplotlib backend is set:
```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
```

---

## 📚 Further Reading

- [SHAP Documentation](https://shap.readthedocs.io/)
- [LIME Paper](https://arxiv.org/abs/1602.04938)
- [Model Interpretability Best Practices](https://christophm.github.io/interpretable-ml-book/)

---

## ✅ Implementation Checklist

- [x] SHAP value calculations
- [x] LIME explanations
- [x] Feature importance visualization
- [x] PDF report generation
- [x] API endpoints for all explanation types
- [x] React dashboard component
- [x] Batch processing support
- [x] Anomaly detection explanation
- [x] Document classification explanation
- [x] VAT prediction explanation

---

## 🎯 Next Steps

1. **Deploy to Production:**
   ```bash
   docker build -f ml/Dockerfile -t ml-api-xai .
   docker run -p 8000:8000 ml-api-xai
   ```

2. **Monitor Explanations:**
   - Track most important features over time
   - Detect model drift
   - Identify data quality issues

3. **Audit Trail:**
   - Store all explanations for compliance
   - Generate monthly reports
   - Review decisions with high uncertainty

4. **User Training:**
   - Train auditors to interpret SHAP values
   - Create decision support guidelines
   - Document model behavior

---

**Made with ❤️ for transparent AI**