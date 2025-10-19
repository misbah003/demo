# 🎯 Quick Reference - SHAP + LIME Implementation

## 📦 What's New

### ✨ 3 Main Components

```
1. Backend Services (explainability_service.py)
   ├─ CNN Explanation (existing, enhanced)
   ├─ Anomaly Detection (NEW)
   └─ Sentiment Analysis (NEW)

2. API Endpoints (ml_api_with_explainability.py)
   ├─ /api/explain-document (enhanced)
   ├─ /api/explain-anomaly-advanced (NEW)
   ├─ /api/explain-sentiment (NEW)
   ├─ /api/explain-compare (NEW)
   └─ /api/explainability-status (NEW)

3. Frontend (EnhancedExplainabilityDashboard.tsx)
   ├─ SHAP Visualizations (NEW)
   ├─ LIME Visualizations (NEW)
   ├─ Method Comparison (NEW)
   └─ Performance Metrics (NEW)
```

---

## 🚀 Quick Start

### 1. Run Tests
```bash
cd ml
python test_comprehensive_explainability.py
```

### 2. Start Server
```bash
python ml_api_with_explainability.py
```

### 3. Test Endpoints
```bash
# Anomaly Detection
curl -X POST http://localhost:8000/api/explain-anomaly-advanced \
  -d '{"data": {...}, "method": "shap"}'

# Sentiment Analysis
curl -X POST http://localhost:8000/api/explain-sentiment \
  -d '{"text": "Good service", "method": "lime"}'

# Compare Methods
curl -X POST http://localhost:8000/api/explain-compare \
  -d '{"model_type": "sentiment", "include_timing": true}'

# Check Status
curl http://localhost:8000/api/explainability-status
```

### 4. Use in React
```tsx
import EnhancedExplainabilityDashboard from '@/components/EnhancedExplainabilityDashboard';

<EnhancedExplainabilityDashboard
  modelType="anomaly"
  modelName="tax_model_v1"
/>
```

---

## 📊 Method Comparison

| Feature | SHAP | LIME |
|---------|------|------|
| Speed | Slow (40-50s) | Fast (5-10s) |
| Accuracy | Higher | Good |
| Use Case | Critical decisions | Real-time UI |
| Best For | Production approval | Dashboard |

---

## 🔌 API Examples

### Anomaly Detection
```json
// Request
POST /api/explain-anomaly-advanced
{
  "data": {
    "VAT_Amount": 50000,
    "Amount": 300000,
    "Risk_Score": 0.95
  },
  "method": "shap"
}

// Response
{
  "is_anomaly": true,
  "anomaly_score": 0.92,
  "risk_level": "HIGH",
  "feature_contributions": [
    {"feature": "Risk_Score", "importance": 0.45}
  ]
}
```

### Sentiment Analysis
```json
// Request
POST /api/explain-sentiment
{
  "text": "Excellent tax service",
  "method": "lime"
}

// Response
{
  "sentiment": "positive",
  "confidence": 0.89,
  "sentiment_intensity": "STRONG",
  "positive_words": [
    {"feature": "excellent", "importance": 0.18}
  ]
}
```

### Compare Methods
```json
// Request
POST /api/explain-compare
{
  "model_type": "sentiment",
  "text": "Great service",
  "include_timing": true
}

// Response
{
  "results": {
    "shap": {"elapsed_time": 42500},
    "lime": {"elapsed_time": 8300}
  },
  "recommendation": "Use LIME for speed"
}
```

---

## 📁 Files to Know

### Backend
- `ml/explainability_service.py` - Core logic (NEW: +500 lines)
- `ml/ml_api_with_explainability.py` - Endpoints (NEW: +300 lines)
- `ml/test_comprehensive_explainability.py` - Tests (NEW)

### Frontend
- `web/src/components/EnhancedExplainabilityDashboard.tsx` - Component (NEW)

### Docs
- `EXPLAINABILITY_IMPLEMENTATION_GUIDE.md` - Full guide
- `IMPLEMENTATION_COMPLETE_SUMMARY.md` - Overview

---

## 🧪 Test Suite

### Run All Tests
```bash
python test_comprehensive_explainability.py
```

### Run Specific Tests
```bash
# CNN only
pytest test_comprehensive_explainability.py::TestCNNExplainability -v

# Anomaly only
pytest test_comprehensive_explainability.py::TestAnomalyExplainability -v

# Sentiment only
pytest test_comprehensive_explainability.py::TestSentimentExplainability -v
```

### Expected Results
- ✅ CNN SHAP explanation
- ✅ CNN LIME explanation
- ✅ CNN method comparison
- ✅ Anomaly detection SHAP
- ✅ Anomaly detection LIME
- ✅ Sentiment SHAP
- ✅ Sentiment LIME
- ✅ Error handling

---

## 💡 Recommendations

### For Production:
```python
# Critical decisions - use SHAP
explanation = service.explain_anomaly_detection(
    model=model,
    input_data=data,
    feature_names=features,
    method="shap"  # ← Most accurate
)
```

### For Real-time Dashboards:
```python
# Interactive UI - use LIME
explanation = service.explain_sentiment(
    model=model,
    input_text=text,
    vectorizer=vec,
    label_encoder=enc,
    method="lime"  # ← Fastest
)
```

### For Validation:
```python
# Compare both methods
comparison = call_api("/api/explain-compare")
# Use comparison.insights for method selection
```

---

## 🔧 Troubleshooting

### "Model not found"
→ Check `models/` directory has trained models

### "SHAP timeout"
→ Use LIME instead for faster response

### "API error"
→ Check `/api/explainability-status` endpoint

### "Tensor shape mismatch"
→ Fixed automatically - uses model's input shape

---

## 📈 What's Different

### Before
- ❌ CNN explanation: Random attention weights
- ❌ Anomaly detection: No explanation
- ❌ Sentiment analysis: No explanation
- ❌ No comparison capability

### After
- ✅ CNN explanation: Real SHAP + LIME
- ✅ Anomaly detection: SHAP + LIME explanations
- ✅ Sentiment analysis: SHAP + LIME explanations
- ✅ Compare methods and benchmarks
- ✅ Advanced visualization dashboard
- ✅ 15+ comprehensive tests
- ✅ 4 new API endpoints

---

## 📞 Support

**Issues?** Check:
1. `EXPLAINABILITY_IMPLEMENTATION_GUIDE.md` → Full details
2. `IMPLEMENTATION_COMPLETE_SUMMARY.md` → Overview
3. `ml/test_comprehensive_explainability.py` → Usage examples
4. `/api/explainability-status` → System status

---

**Status**: ✅ Ready to Use
**Last Updated**: 2024