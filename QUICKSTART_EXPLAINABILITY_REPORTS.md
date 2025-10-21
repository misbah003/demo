# 🚀 Quick Start: Explainability Reports

## 5-Minute Setup Guide

### 1️⃣ Start the API

```bash
cd c:\Users\HomeLaptop\Downloads\navi-tax-35-main
python -m uvicorn ml.ml_api_with_explainability:app --host 0.0.0.0 --port 8000
```

### 2️⃣ Generate a Prediction with Explanation

```bash
curl -X POST http://localhost:8000/api/explain-vat \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "amount": 5000,
      "frequency": 12,
      "region": "EU",
      "category": "goods"
    },
    "amount": 5000,
    "method": "shap"
  }'
```

### 3️⃣ Generate Report

```bash
curl -X POST http://localhost:8000/api/explain-report \
  -H "Content-Type: application/json" \
  -d '{
    "prediction_data": {
      "amount": 5000,
      "frequency": 12,
      "region": "EU"
    },
    "model_name": "vat_predictor",
    "input_summary": {
      "prediction": 450.50,
      "confidence": 0.85,
      "method": "SHAP",
      "feature_contributions": [
        {
          "feature": "amount",
          "importance": 0.60,
          "shap_value": 0.45,
          "value": 5000,
          "direction": "positive"
        }
      ]
    }
  }'
```

**Response:**
```json
{
  "status": "success",
  "report_id": "report_vat_predictor_20240115_143022",
  "reports": {
    "json": {
      "url": "/api/reports/report_vat_predictor_20240115_143022.json"
    },
    "html": {
      "url": "/api/reports/report_vat_predictor_20240115_143022.html"
    }
  }
}
```

### 4️⃣ Download Report

```bash
# Download HTML (open in browser)
curl http://localhost:8000/api/reports/report_vat_predictor_20240115_143022.html \
  -o report.html

# Download JSON
curl http://localhost:8000/api/reports/report_vat_predictor_20240115_143022.json \
  -o report.json
```

### 5️⃣ View in Frontend

```bash
# In your React app, use:
import ExplainabilityReportViewer from '@/components/ExplainabilityReportViewer';

export default function ReportsPage() {
  return <ExplainabilityReportViewer apiEndpoint="http://localhost:8000" />;
}
```

---

## 📊 What You Get

### JSON Report
```json
{
  "metadata": {
    "timestamp": "2024-01-15T14:30:22",
    "model_name": "vat_predictor"
  },
  "prediction": {
    "value": 450.50,
    "confidence": 0.85
  },
  "feature_importance": {
    "top_features": [
      {
        "feature": "amount",
        "importance": 0.60,
        "shap_value": 0.45
      }
    ]
  },
  "risk_assessment": {
    "level": "LOW",
    "score": 25.5
  }
}
```

### HTML Report
- Professional formatting
- Printable layout
- Visual charts
- Feature importance display
- Risk assessment badges
- Browser-ready (no rendering needed)

### Key Information
- 📊 **Prediction Value & Confidence**
- 🎯 **Top Contributing Features**
- ⚠️ **Risk Level Assessment**
- 📈 **Feature Importance Charts**
- 💡 **AI Interpretation**

---

## 🎯 Common Tasks

### List All Reports
```bash
curl http://localhost:8000/api/reports
```

### Download Any Report
```bash
curl http://localhost:8000/api/reports/report_name.html -o report.html
curl http://localhost:8000/api/reports/report_name.json -o report.json
curl http://localhost:8000/api/reports/report_name.pdf -o report.pdf
```

### Delete Report
```bash
curl -X DELETE http://localhost:8000/api/reports/report_name.html
```

### Generate PDF (Optional)
Install reportlab:
```bash
pip install reportlab
```

Then PDF reports will be generated automatically.

---

## 🌐 Frontend Integration

### Step 1: Import Component
```tsx
import ExplainabilityReportViewer from '@/components/ExplainabilityReportViewer';
```

### Step 2: Add to Your Page
```tsx
export function ReportsPage() {
  return (
    <div>
      <h1>Explainability Reports</h1>
      <ExplainabilityReportViewer 
        apiEndpoint="http://localhost:8000"
        autoRefresh={true}
      />
    </div>
  );
}
```

### Step 3: Features Available
- ✅ View all reports
- ✅ Download in any format
- ✅ Preview report details
- ✅ Delete reports
- ✅ Auto-refresh
- ✅ File info display

---

## ✅ Verify Installation

```bash
# 1. Check API is running
curl http://localhost:8000/

# 2. Check report generator is loaded
curl http://localhost:8000/ | grep report_generator

# 3. Generate a test report
curl -X POST http://localhost:8000/api/explain-report ...

# 4. Check reports directory
ls -la explainability_reports/

# 5. Verify reports exist
curl http://localhost:8000/api/reports
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| API not responding | Check if running: `python -m uvicorn ...` |
| Reports not saving | Check `explainability_reports/` directory exists |
| PDF not generating | Install reportlab: `pip install reportlab` |
| Frontend shows no reports | Ensure API CORS is enabled |
| 404 errors | Verify report filename in URL |

---

## 📚 Next Steps

1. ✅ Start generating predictions
2. ✅ Create explainability reports
3. ✅ View reports in frontend
4. ✅ Download and share reports
5. ✅ Integrate into your workflow

---

**Status**: ✅ Ready to Use  
**Version**: 1.0  
**Last Updated**: January 15, 2024