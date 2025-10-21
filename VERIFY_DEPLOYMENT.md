# ✅ Post-Deployment Verification Guide

After deploying to production, verify all services are working correctly.

**Time Required:** 10-15 minutes  
**Required:** All 3 services deployed (Frontend, Backend, ML API)

---

## 🚀 Quick Test (2 minutes)

Try this first for a quick validation:

```powershell
# Set your URLs (update with your actual URLs)
$FRONTEND = "https://your-project.vercel.app"
$BACKEND = "https://navi-tax-backend.onrender.com"
$ML_API = "https://navi-tax-ml-api.onrender.com"

# Test ML API
Invoke-WebRequest "$ML_API/health" | Select-Object StatusCode, Content

# Test Backend
Invoke-WebRequest "$BACKEND/health" | Select-Object StatusCode, Content

# Test Frontend (should return HTML)
Invoke-WebRequest "$FRONTEND" | Select-Object StatusCode, StatusDescription
```

Expected output:
- ML API: `Status 200` + `{"status": "healthy"}`
- Backend: `Status 200` + `{"status": "ok"}`
- Frontend: `Status 200` + HTML content

---

## 📋 Full Verification Checklist

### 1️⃣ Frontend Verification

#### 1.1 Page Loads
- [ ] Open `https://your-vercel-url.vercel.app` in browser
- [ ] Page loads without errors
- [ ] See login/signup screen
- [ ] No console errors (F12 → Console tab)

#### 1.2 Signup Works
- [ ] Click "Sign up"
- [ ] Enter test email: `test@example.com`
- [ ] Enter password: `TestPassword123!`
- [ ] Click "Sign up"
- [ ] Should see success or check-email message

#### 1.3 Check Supabase
- [ ] Go to Supabase dashboard
- [ ] Select your project
- [ ] Go to **Authentication** → **Users**
- [ ] Should see your test user

#### 1.4 Login Works
- [ ] On frontend, go back to login
- [ ] Enter your test email
- [ ] Enter your test password
- [ ] Should log in successfully
- [ ] Should see main dashboard

#### 1.5 Navigation Works
- [ ] Can navigate between pages without errors
- [ ] Dark mode toggle works (if implemented)
- [ ] No broken images or styling issues

**Status:** ✅ / ❌ (_if all pass, frontend is working_)

---

### 2️⃣ ML API Verification

#### 2.1 Health Check
```bash
# In PowerShell or browser
curl https://navi-tax-ml-api.onrender.com/health
```

Expected:
```json
{"status": "healthy"}
```

- [ ] Status 200
- [ ] Response shows healthy

#### 2.2 Test Prediction Endpoint

Option A: Using browser
1. Open: `https://navi-tax-ml-api.onrender.com/predict`
2. Send POST request with test data
3. Should get prediction back

Option B: Using PowerShell
```powershell
$body = @{
    company_size = "medium"
    industry = "retail"
    annual_revenue = 1000000
    vat_refund_rate = 0.15
} | ConvertTo-Json

$response = Invoke-RestMethod `
  -Uri "https://navi-tax-ml-api.onrender.com/predict" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

$response
```

Expected:
```json
{
  "prediction": 0.XXX,
  "confidence": 0.XX,
  "model": "random_forest"
}
```

- [ ] Status 200
- [ ] `prediction` field present
- [ ] `confidence` field present

#### 2.3 Test SHAP Explanation

```powershell
$body = @{
    company_size = "medium"
    industry = "retail"
    annual_revenue = 1000000
    vat_refund_rate = 0.15
} | ConvertTo-Json

$response = Invoke-RestMethod `
  -Uri "https://navi-tax-ml-api.onrender.com/explain" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

$response | ConvertTo-Json -Depth 10
```

Expected: SHAP explanation with:
- `base_value`
- `shap_values`
- `feature_names`
- `prediction`

- [ ] Status 200
- [ ] SHAP values present
- [ ] Feature importance visible

#### 2.4 Check Render Logs

1. Go to Render Dashboard
2. Click ML API service
3. Go to **Logs** tab
4. Check for errors (should be mostly blank or showing requests)

- [ ] No fatal errors in logs
- [ ] Requests are being logged
- [ ] No "out of memory" errors

**Status:** ✅ / ❌ (_if all pass, ML API is working_)

---

### 3️⃣ Backend Verification

#### 3.1 Health Check
```bash
curl https://navi-tax-backend.onrender.com/health
```

Expected:
```json
{"status": "ok"}
```

- [ ] Status 200
- [ ] Response shows ok

#### 3.2 Test OTP Endpoint

```powershell
$body = @{
    email = "test@example.com"
} | ConvertTo-Json

$response = Invoke-RestMethod `
  -Uri "https://navi-tax-backend.onrender.com/send-otp" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

$response
```

Expected:
```json
{"success": true, "message": "OTP sent to email"}
```

- [ ] Status 200
- [ ] `success` is true
- [ ] Check your email for the OTP

#### 3.3 Test File Upload Endpoint

```powershell
# Create a test file
"Test document content" | Out-File -FilePath "test.txt"

# Upload it
$file = @{file = Get-Item "test.txt"}

$response = Invoke-RestMethod `
  -Uri "https://navi-tax-backend.onrender.com/upload" `
  -Method Post `
  -Form $file

$response
```

Expected:
```json
{
  "success": true,
  "filename": "...",
  "document_type": "Document",
  "text": "Test document content",
  "entities": [...]
}
```

- [ ] Status 200
- [ ] `success` is true
- [ ] Filename is present
- [ ] Text extracted successfully

#### 3.4 Test ML API Integration

Backend should be able to call ML API:

```powershell
# Upload a document and check if it gets predictions
# From frontend: upload a file
# Backend should call ML API automatically
# Check if predictions appear in response
```

- [ ] Backend successfully called ML API
- [ ] Predictions returned in response
- [ ] No timeout errors

#### 3.5 Check Render Logs

1. Go to Render Dashboard
2. Click Backend service
3. Go to **Logs** tab
4. Look for upload/OTP requests

- [ ] No fatal errors in logs
- [ ] Requests being logged
- [ ] No connection errors to ML API or Supabase

**Status:** ✅ / ❌ (_if all pass, Backend is working_)

---

### 4️⃣ Integration Tests

#### 4.1 Frontend → Backend

Test from frontend:

1. Go to `https://your-vercel-url.vercel.app`
2. Upload a test document
3. Watch for:
   - Loading spinner appears
   - Document processes
   - Results appear (predictions, entities, etc.)

- [ ] File upload works
- [ ] Backend receives file
- [ ] Predictions appear in UI
- [ ] No CORS errors (check F12 console)

#### 4.2 Backend → ML API

From backend service:

1. Check Render Backend logs
2. Look for requests to ML API
3. Should see: `GET/POST https://navi-tax-ml-api.onrender.com/predict`

- [ ] Connection successful (no 500 errors)
- [ ] Predictions returned
- [ ] Response time reasonable (< 5 seconds)

#### 4.3 Backend → Supabase

From backend service:

1. Check if data is being saved
2. Go to Supabase → Table Editor
3. Check relevant tables for new data

- [ ] Documents table has entries
- [ ] User records present
- [ ] Data looks correct (no NULL values where shouldn't be)

#### 4.4 Frontend → Supabase

Test authentication:

1. Frontend should sync user data with Supabase
2. Go to Supabase → Table Editor → `profiles` table
3. Should see user profile created

- [ ] User profile created
- [ ] Profile has correct user_id
- [ ] Profile data is complete

**Status:** ✅ / ❌ (_if all pass, integration is working_)

---

### 5️⃣ Performance Tests

#### 5.1 Response Times

With a stopwatch or browser dev tools (F12):

```
Test: Upload a document file
Expected timing:
- Frontend upload button click: < 100ms
- Backend receives: < 500ms
- ML API prediction: 1-2 seconds
- Total: 2-3 seconds
```

- [ ] Frontend responsive (buttons click immediately)
- [ ] Backend response time < 1 second (without ML)
- [ ] Predictions return within 3-5 seconds
- [ ] No timeouts

#### 5.2 Cold Start Recovery

If services were idle:

1. Trigger each service (make requests)
2. First request takes longer
3. Subsequent requests faster

```
Cold start times:
- Frontend: Instant (static)
- Backend: 30-60 seconds (first time)
- ML API: 1-2 minutes (first time, large model)
```

- [ ] Frontend loads instantly
- [ ] Backend responds after 30-60s cold start
- [ ] ML API responds after 1-2 min cold start
- [ ] Second requests are much faster

#### 5.3 Load Testing

Make multiple rapid requests:

```powershell
# Hit health endpoint 10 times rapidly
for ($i = 1; $i -le 10; $i++) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    Invoke-RestMethod "https://navi-tax-backend.onrender.com/health" | Out-Null
    $sw.Stop()
    "Request $i: $($sw.ElapsedMilliseconds)ms"
}
```

- [ ] No 503 (service unavailable) errors
- [ ] Response times consistent (not degrading)
- [ ] All requests succeed

**Status:** ✅ / ❌ (_if all pass, performance is acceptable_)

---

### 6️⃣ Error Handling Tests

#### 6.1 Invalid Input

```powershell
# Send invalid JSON to prediction endpoint
$response = Invoke-RestMethod `
  -Uri "https://navi-tax-ml-api.onrender.com/predict" `
  -Method Post `
  -ContentType "application/json" `
  -Body "invalid json" `
  -ErrorAction SilentlyContinue

$response
```

- [ ] Returns 400 (Bad Request), not 500
- [ ] Error message is helpful
- [ ] Service doesn't crash

#### 6.2 Missing Environment Variables

Check Render logs for warnings:

1. Render Dashboard → Service → Logs
2. Look for: "Missing env var", "Cannot connect", etc.

- [ ] No critical missing env var warnings
- [ ] All required variables present
- [ ] Fallbacks working where applicable

#### 6.3 Database Connection Error

Backend should handle Supabase being down:

1. Temporarily disconnect from Supabase (or it goes down)
2. Try to make request
3. Should get error, not crash

- [ ] Service doesn't crash on DB error
- [ ] User gets meaningful error message
- [ ] Service recovers when DB comes back

#### 6.4 ML API Down

Backend should handle ML API being unavailable:

1. Stop ML API (go offline temporarily)
2. Send prediction request to backend
3. Backend should fail gracefully

- [ ] No 500 Internal Server Error
- [ ] Returns 503 or helpful message
- [ ] Logs show the issue

**Status:** ✅ / ❌ (_if all pass, error handling is robust_)

---

### 7️⃣ Security Tests

#### 7.1 CORS Working Correctly

1. Open frontend
2. Open DevTools (F12)
3. Make API request to backend
4. Check Network tab

Expected: No CORS errors

- [ ] Requests go through (Status 200, not error)
- [ ] No "Access-Control-Allow-Origin" errors
- [ ] Credentials included if needed

#### 7.2 Secrets Not Exposed

Check that secrets aren't in:

```powershell
# Check frontend code doesn't have secrets
$files = Get-ChildItem "web\src" -Recurse -Include "*.js","*.tsx" | Where-Object {$_.Length -lt 1MB}

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    if ($content -match "GMAIL_APP_PASSWORD|SUPABASE_SERVICE_KEY|DATABASE_PASSWORD") {
        Write-Host "⚠️  Found secret in: $($file.Name)"
    }
}
```

- [ ] No secrets found in frontend code
- [ ] Service keys only in Render dashboard
- [ ] App passwords only in Render dashboard
- [ ] No secrets in browser DevTools

#### 7.3 HTTPS Everywhere

Check all URLs use HTTPS:

- [ ] Frontend: `https://` (✅ Vercel auto-HTTPS)
- [ ] Backend: `https://` (✅ Render auto-HTTPS)
- [ ] ML API: `https://` (✅ Render auto-HTTPS)
- [ ] Database: `https://` (✅ Supabase auto-HTTPS)

#### 7.4 User Data Isolation

1. Login as User A
2. Upload document
3. Logout
4. Login as User B
5. Should NOT see User A's document

- [ ] User B can't see User A's data
- [ ] RLS policies enforcing user isolation
- [ ] Data properly segregated

**Status:** ✅ / ❌ (_if all pass, security is solid_)

---

## 📊 Final Verification Summary

Count your ✅ marks:

| Section | Total | Passed |
|---------|-------|--------|
| Frontend | 5 | __/5 |
| ML API | 5 | __/5 |
| Backend | 5 | __/5 |
| Integration | 4 | __/4 |
| Performance | 3 | __/3 |
| Error Handling | 4 | __/4 |
| Security | 4 | __/4 |
| **TOTAL** | **34** | **__/34** |

### Results

- **32-34 ✅:** Production Ready! 🎉
- **28-31 ✅:** Minor issues to fix (see Troubleshooting)
- **< 28 ✅:** Significant issues (stop and debug)

---

## 🆘 If Something Fails

### Common Issues

**ML API Health Check Fails**
- Check Render ML API service status
- Look at Render logs
- Ensure models directory exists: `optimized_models_25000_samples/`

**Backend Can't Connect to ML API**
- Check `ML_API_URL` env var in Render backend
- Verify ML API is running (health check)
- Wait 2-3 minutes after deployment
- Check firewall isn't blocking (shouldn't be on Render)

**Frontend Can't Call Backend**
- Check CORS origins in `backend/server.js`
- Ensure `FRONTEND_URL` env var is correct
- Clear browser cache (Ctrl+Shift+Delete)
- Redeploy backend after CORS changes

**Supabase Connection Fails**
- Check `SUPABASE_URL` format
- Verify service key is correct (not anon key)
- Check project exists at supabase.com
- Verify API credentials in Render dashboard

**Email Not Sending**
- Verify 2FA enabled on Gmail
- Check app password (16 chars, not regular password)
- Verify Gmail account is correct
- Check Render logs for SMTP errors

---

## 📝 After Verification

Once all checks pass ✅:

1. **Document Results**
   - Note any warnings or slow endpoints
   - Document response times for baseline
   - Save this verification report

2. **Setup Monitoring**
   - Setup Uptime Robot (see DEPLOY_NOW.md Step 8)
   - Configure error alerts
   - Set up daily health checks

3. **Schedule Maintenance**
   - Monthly security audits
   - Review Render/Vercel logs weekly
   - Monitor database storage usage
   - Plan scaling if traffic grows

4. **Next Steps**
   - Deploy dashboard visualizations
   - Add feature importance analysis
   - Implement user analytics
   - Create admin dashboard

---

## ✅ Deployment Complete!

All systems verified and running. Your production application is live! 🎉

**Your Live URLs:**

| Service | URL |
|---------|-----|
| Frontend | `https://your-project.vercel.app` |
| Backend | `https://navi-tax-backend.onrender.com` |
| ML API | `https://navi-tax-ml-api.onrender.com` |
| Database | Supabase (managed) |

Good luck! 🚀
