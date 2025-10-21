# 🔍 SHAP ANALYSIS & MODEL DIAGNOSTIC ACTION PLAN

## Overview

Your SHAP endpoint is **technically working correctly**, but the **predictions are concerning**:
- Baseline refund: €3,620.87 (43% BELOW expected average)
- Model heavily penalizes Filing_Status and VAT_Amount
- Need to determine if this is data bias or model over-weighting

---

## 📋 Three-Phase Analysis Plan

### ✅ PHASE 1: Validate Model Capability (10 minutes)

**Goal:** Answer "Can the model produce HIGH refunds with all positive signals?"

**Run This Script:**
```bash
python VALIDATE_GOOD_SCENARIO.py
```

**What It Tests:**
1. ✅ Baseline test (current failing case) → Should return ~€3,620
2. ✅ Good scenario (all positive signals) → Should return €10,000+
3. ⭐ Excellent scenario (premium case) → Should return €20,000+
4. 🔴 Risky scenario (high risk) → Should return <€5,000

**Expected Results:**
- If good scenario returns €10,000+ → Model IS responsive ✅
- If good scenario still returns <€5,000 → Model has CRITICAL BIAS ❌

**Decision Point:**
- **RESPONSIVE**: Continue to Phase 2
- **NOT RESPONSIVE**: Skip to Phase 3 (Critical Issues)

---

### 🧪 PHASE 2: Sensitivity & Feature Analysis (15 minutes)

**Goal:** Identify which features are dominating predictions and by how much

**Run This Script:**
```bash
python SHAP_DIAGNOSTIC_ANALYSIS.py
```

**What It Does:**
1. Runs baseline analysis
2. Runs good scenario analysis
3. Tests sensitivity to:
   - Filing Status (monthly vs quarterly vs annual)
   - VAT Rate (5% vs 19% vs 25%)
   - Compliance flags (compliant vs partial vs non-compliant)
   - Risk Score (0.1 to 0.9)
   - Annual Turnover (€100k to €5M)

**Output Includes:**
- Variance for each feature (how much it changes predictions)
- Feature sensitivity ranking
- Bias assessment
- Recommendations

**Key Metrics to Look For:**
- Features with >€10k variance = 🔴 CRITICAL
- Features with €5-10k variance = 🟡 HIGH
- Features with <€2k variance = 🟢 LOW (acceptable)

---

### 📊 PHASE 3: Training Data Analysis (Optional, 10 minutes)

**Goal:** Check if the model's conservatism comes from biased training data

**Run This Script:**
```bash
python ANALYZE_TRAINING_DATA.py
```

**What It Analyzes:**
1. Feature distributions in training data
2. Categorical feature balance (is filing_status imbalanced?)
3. Outliers and data quality issues
4. Feature importance (which features were actually used)
5. Potential data quality problems

**Key Findings to Look For:**
- Are some categories in Filing_Status underrepresented?
- Is VAT_Amount distribution skewed?
- Are there zero-importance features?
- Is training data biased toward low refunds?

---

## 🎯 Interpretation Guide

### Scenario 1: Model IS Responsive (Good)
**Diagnosis:** The model works fine, just needs recalibration

**Actions:**
1. ✅ Run Phase 2 diagnostic
2. ✅ Identify over-weighted features
3. ✅ Recalibrate weights in `ml_api_service_optimized.py`
4. ✅ Adjust feature scaling if needed

**Fix Location:** `ml_api_service_optimized.py` lines 240-267
- Adjust feature scaling
- Consider re-encoding Filing_Status
- Normalize VAT_Amount

---

### Scenario 2: Model is NOT Responsive (Bad)
**Diagnosis:** Model has systematic bias, likely from training data

**Actions:**
1. ✅ Run Phase 3 (training data analysis)
2. ✅ Check for:
   - Data imbalance in Filing_Status
   - VAT_Amount encoding issues
   - Under-representation of high-refund cases
3. ✅ Retrain model with:
   - Balanced classes
   - Feature reweighting
   - Outlier handling

**Fix Location:** `ml/train_optimized_models.py`
- Add class balancing
- Implement SMOTE for imbalanced data
- Adjust feature importance weights

---

## 📍 Quick Reference: Where to Make Changes

### If Issue is Feature Scaling/Encoding:
**File:** `ml_api_service_optimized.py` (lines 235-267)
```python
# Feature encoding and scaling happens here
# Adjust scaler.transform() behavior
# Re-encode categorical variables
```

### If Issue is Model Weights:
**File:** `optimized_models_25000_samples/metadata.json`
- Contains best model parameters
- Adjust regularization constants
- Rebalance feature importance

### If Issue is Training Data:
**File:** `ml/train_optimized_models.py`
- Add data balancing
- Implement class weighting
- Use SMOTE for imbalanced data

### If Issue is Explainability:
**File:** `ml/explainability_service.py` (lines 72-124)
- SHAP explainer configuration
- Feature scaling for SHAP
- Base value calculation

---

## 🚨 Red Flags & What They Mean

| Red Flag | Meaning | Action |
|----------|---------|--------|
| Good scenario still returns <€5k | Model is over-conservative | Go to Phase 3, check training data |
| Filing_Status variance >€10k | Over-weighted feature | Reduce feature importance weight |
| VAT_Amount negative SHAP | Counter-intuitive | Check feature encoding/scaling |
| Risky scenario returns high refund | Model doesn't penalize risk | Adjust Risk_Score scaling |
| All features have high variance | Model is unstable | Increase regularization |
| Zero-importance features | Dead features | Check encoding or remove them |

---

## ✅ Success Criteria

### Before Recalibration:
- [ ] Baseline test returns €3-4k ✓ (currently working)
- [ ] Good scenario returns €10-20k ✓ (should increase 2-3x)
- [ ] Excellent scenario returns €20-50k ✓ (should be highest)
- [ ] Risky scenario returns <€5k ✓ (should decrease)

### After Recalibration:
- [ ] Baseline test returns €6-8k (calibrated)
- [ ] Good scenario returns €12-18k (responsive)
- [ ] Excellent scenario returns €25-40k (achievable)
- [ ] Risky scenario returns €2-4k (penalized)

---

## 🔧 Quick Fix Checklist

**Immediate Actions (No Coding):**
- [ ] Run Phase 1 validation
- [ ] Document which features have high sensitivity
- [ ] Check if baseline test matches expectations

**Short Term (Easy Fixes):**
- [ ] Adjust feature scaling in preprocessing
- [ ] Re-encode categorical features
- [ ] Normalize VAT_Amount and Filing_Status

**Medium Term (Model Tuning):**
- [ ] Rebalance feature importance
- [ ] Adjust RandomForest parameters
- [ ] Tune Ridge regularization

**Long Term (Full Recalibration):**
- [ ] Retrain model with balanced data
- [ ] Implement class weighting
- [ ] Use ensemble methods

---

## 📞 Need Help?

**Questions to Ask Yourself:**
1. Is the low refund justified by the input data?
2. Should compliant, low-risk entities always get low refunds?
3. Are there regulatory requirements for minimum refund amounts?
4. Should Filing_Status really dominate the prediction?

**Next Actions:**
1. ✅ Run VALIDATE_GOOD_SCENARIO.py first
2. 🔍 Then run SHAP_DIAGNOSTIC_ANALYSIS.py
3. 📊 Finally run ANALYZE_TRAINING_DATA.py if needed
4. 💡 Use Phase 3 results to guide recalibration

---

## 📈 Expected Outcome

After implementing these scripts and fixes:

✅ Model should produce **responsive, calibrated predictions**
✅ SHAP explanations will **clearly show WHY** predictions are made
✅ Business users can **trust and explain** the model
✅ Audit trails will show **complete feature importance breakdown**

---

**Generated:** 2025-10-20
**Status:** Ready for Analysis