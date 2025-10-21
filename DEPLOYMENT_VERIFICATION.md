# 🔍 Deployment Verification Checklist

After deploying to Vercel → Render → Supabase, use this checklist to verify everything works.

---

## ✅ STEP 1: Backend (Render) Verification

### 1.1 Service Status

```bash
# Check Render service is running
curl https://navi-tax-ml-api.onrender.com/health

# Expected response:
# {"status": "healthy", "models_loaded": true, ...}
```

**Result**: ✅ Pass / ❌ Fail

### 1.2 Validation Endpoint

```bash
curl https://navi-tax-ml-api.onrender.com/validation-reference

# Should return valid categories, regions, filing statuses
```

**Result**: ✅ Pass / ❌ Fail

### 1.3 Prediction Test

```bash
curl -X POST https://navi-tax-ml-api.onrender.com/predict \
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

# Expected: {"refund_amount": ~4751.76, "confidence": ~0.87}
```

**Result**: ✅ Pass / ❌ Fail

### 1.4 SHAP Explanation

```bash
curl -X POST https://navi-tax-ml-api.onrender.com/explain \
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

# Expected: SHAP values showing feature contributions
```

**Result**: ✅ Pass / ❌ Fail

### 1.5 Render Logs Check

1. Go to Render dashboard
2. Select `navi-tax-ml-api` service
3. Check **Logs** tab for errors
4. Expected: No ERROR or CRITICAL messages

**Result**: ✅ Pass / ❌ Fail

---

## ✅ STEP 2: Frontend (Vercel) Verification

### 2.1 Page Load

```
https://navi-tax-35-main.vercel.app
```

- [ ] Page loads without 404
- [ ] No console errors (F12 → Console tab)
- [ ] All UI components render

**Result**: ✅ Pass / ❌ Fail

### 2.2 Authentication

- [ ] Can see login/signup page
- [ ] Can click "Sign Up"
- [ ] Form validates correctly

**Result**: ✅ Pass / ❌ Fail

### 2.3 Network Requests (DevTools)

1. Press **F12** → Network tab
2. Try to make a prediction
3. Watch for requests:
   - Should see requests to `navi-tax-ml-api.onrender.com`
   - Status should be **200** (not 403, 404, 500)

**Result**: ✅ Pass / ❌ Fail

### 2.4 Vercel Logs

1. Go to Vercel dashboard
2. Select your project
3. Check **Deployments** → most recent
4. Click to expand and check **Build Logs**
5. Expected: No errors, build successful

**Result**: ✅ Pass / ❌ Fail

---

## ✅ STEP 3: Database (Supabase) Verification

### 3.1 Authentication Status

1. Go to [supabase.co](https://supabase.co)
2. Select your project
3. Check **Authentication** → Users section
4. You should see at least 1 user (yourself)

**Result**: ✅ Pass / ❌ Fail

### 3.2 Realtime Enabled

1. **Database** → **Tables**
2. Check tables have realtime enabled (blue status)
3. Expected tables:
   - `users` or `auth.users`
   - Any custom tables for predictions/documents

**Result**: ✅ Pass / ❌ Fail

### 3.3 RLS Policies

1. Select any table
2. **RLS** tab → Verify policies exist
3. Expected: Policies should restrict data to authenticated users

**Result**: ✅ Pass / ❌ Fail

---

## ✅ STEP 4: End-to-End Integration Test

### 4.1 Sign Up & Login

1. Go to `https://navi-tax-35-main.vercel.app`
2. Click **Sign Up**
3. Enter email & password
4. Should see confirmation message or redirect to dashboard

**Result**: ✅ Pass / ❌ Fail

### 4.2 Make a Prediction

1. Once logged in, go to **VAT Refund Predictor**
2. Fill in form:
   - Amount: €50,000
   - VAT Rate: 19%
   - Risk Score: 0.3
   - Category: Retail
   - etc.
3. Click **Predict**

**Expected Results**:
- ✅ See prediction: ~€4,751.76
- ✅ See SHAP explanation with feature contributions
- ✅ No error messages

**Result**: ✅ Pass / ❌ Fail

### 4.3 Test Invalid Input

1. Try invalid Filing_Status: "Quarterly"
2. Should see error: "Invalid Filing_Status..."

**Result**: ✅ Pass / ❌ Fail

### 4.4 Test Batch Prediction

1. Go to **Bulk Prediction** (if available)
2. Upload CSV with multiple rows
3. Should process and return results

**Result**: ✅ Pass / ❌ Fail

---

## ✅ STEP 5: Performance Check

### 5.1 API Response Time

Using DevTools Network tab:

- Single prediction: **< 500ms** ✅
- SHAP explanation: **< 1000ms** ✅
- Batch prediction: **< 2 seconds for 10 rows** ✅

**Result**: ✅ Pass / ❌ Fail

### 5.2 Cold Start

After 15+ minutes of inactivity:
- First request should take **5-10 seconds** (acceptable for free tier)
- Subsequent requests: **< 500ms**

**Result**: ✅ Pass / ❌ Fail

---

## ✅ STEP 6: Error Handling

### 6.1 Invalid Category

```bash
curl -X POST https://navi-tax-ml-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Amount": 50000,
    "VAT_Rate": 19,
    "Risk_Score": 0.3,
    "Annual_Turnover": 500000,
    "Category": "InvalidCategory",
    "Region": "East",
    "Filing_Status": "On Time",
    "Compliance_Flag": "Compliant",
    "Refund_Eligible": "Yes",
    "Is_Anomaly": "No"
  }'

# Expected error with list of valid categories
```

**Result**: ✅ Pass / ❌ Fail

### 6.2 Missing Required Field

```bash
curl -X POST https://navi-tax-ml-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Amount": 50000
  }'

# Expected: 400 Bad Request with helpful error message
```

**Result**: ✅ Pass / ❌ Fail

### 6.3 Invalid Number Range

```bash
curl -X POST https://navi-tax-ml-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Amount": -100,
    "VAT_Rate": 19,
    ...
  }'

# Expected: Validation error about negative amount
```

**Result**: ✅ Pass / ❌ Fail

---

## 📊 Final Verification Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Backend Health | ✅ / ❌ | |
| Predictions | ✅ / ❌ | |
| SHAP Explanations | ✅ / ❌ | |
| Frontend Load | ✅ / ❌ | |
| Authentication | ✅ / ❌ | |
| Database | ✅ / ❌ | |
| End-to-End Flow | ✅ / ❌ | |
| Error Handling | ✅ / ❌ | |
| Performance | ✅ / ❌ | |

---

## 🚀 If ALL ✅: Ready for Production!

If all checks pass, your system is production-ready.

## 🔧 If ANY ❌: Troubleshooting

Check `DEPLOYMENT_FREEMIUM_GUIDE.md` → **TROUBLESHOOTING** section.

---

## 📞 Quick Debug Commands

```bash
# Check Render backend
curl -v https://navi-tax-ml-api.onrender.com/health

# Check CORS headers
curl -I -X OPTIONS https://navi-tax-ml-api.onrender.com/predict

# Test with sample data
curl -X POST https://navi-tax-ml-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"Amount":50000,"VAT_Rate":19,"Risk_Score":0.3,"Annual_Turnover":500000,"Category":"Retail","Region":"East","Filing_Status":"On Time","Compliance_Flag":"Compliant","Refund_Eligible":"Yes","Is_Anomaly":"No"}'
```

---

**Last Verified**: [Add date]  
**Verified By**: [Your name]  
**Environment**: Production