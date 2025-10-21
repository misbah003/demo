# Local Testing Guide - Split Architecture

This guide walks you through testing the split architecture deployment locally before deploying to Render/Vercel.

## Quick Start

```powershell
# Run the split architecture startup script
.\START_ALL_SERVERS_SPLIT.ps1
```

This will start all three services in separate windows:
- **ML API** (Port 8000) - Python/Flask
- **Backend** (Port 3001) - Node.js/Express  
- **Frontend** (Port 5173) - Vite/React

---

## Prerequisites

Before testing, ensure you have:

```
✓ Python 3.8+ installed
✓ Node.js 16+ installed  
✓ Supabase account with credentials
✓ All dependencies installed
```

### Check Prerequisites

```powershell
python --version    # Should be 3.8+
node --version      # Should be 16+
npm --version       # Should work
```

---

## Environment Setup

The startup script automatically creates `.env` files if they don't exist.

### Backend Environment (`docs/backend-example/.env`)

```env
NODE_ENV=development
PORT=3001
SUPABASE_URL=your_actual_supabase_url
SUPABASE_SERVICE_KEY=your_actual_service_key
ML_API_URL=http://localhost:8000
CORS_ORIGIN=http://localhost:5173
```

**⚠️ ACTION REQUIRED:** Update `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` with your actual credentials.

### Frontend Environment (`web/.env`)

```env
VITE_API_URL=http://localhost:3001
VITE_SUPABASE_URL=your_actual_supabase_url
VITE_SUPABASE_ANON_KEY=your_actual_anon_key
```

**⚠️ ACTION REQUIRED:** Update Supabase credentials.

---

## Testing Sequence

### Phase 1: Service Startup (5 minutes)

#### Step 1: Run Startup Script
```powershell
cd C:\Users\HomeLaptop\Downloads\navi-tax-35-main
.\START_ALL_SERVERS_SPLIT.ps1
```

**Expected Output:**
- Three new PowerShell windows open
- ML API window shows loading messages
- Backend window shows "Server running on port 3001"
- Frontend window shows Vite dev server ready

**Troubleshooting:**
- If a window closes immediately: Check for errors in window or run manually
- Port already in use: Close existing services with `STOP_SERVERS.ps1`

#### Step 2: Wait for ML API Initialization
- **Timeline:** 30-60 seconds from startup
- **Look for:** "Application startup complete" in ML API window
- **Status check:** 
  ```powershell
  curl http://localhost:8000/ml/health
  # Should return 200 OK with model status
  ```

**Troubleshooting:**
- Models not loading: Check `ml_api.py` console for errors
- Still loading after 2 minutes: Try restarting ML API window
- Memory issues: Ensure system has 4GB+ free RAM

#### Step 3: Verify Backend Connection to ML API
- ML API should be ready before proceeding
- Backend should show connection success messages
- **Status check:**
  ```powershell
  curl http://localhost:3001/health
  # Should return JSON with status info
  ```

**Troubleshooting:**
- Backend connection timeout: Check ML API started first
- CORS errors: Verify `CORS_ORIGIN=http://localhost:5173` in backend .env

#### Step 4: Frontend Ready
- Navigate to http://localhost:5173 in browser
- Should display login/dashboard
- Check browser console for errors: Press F12

**Troubleshooting:**
- Blank page: Check browser console for API connection errors
- CORS errors: Backend .env CORS_ORIGIN might be wrong
- API URL wrong: Check frontend .env `VITE_API_URL`

---

### Phase 2: Connectivity Testing (5 minutes)

#### Test 1: Frontend ↔ Backend Connection

**In browser console:**
```javascript
fetch('http://localhost:3001/health')
  .then(r => r.json())
  .then(d => console.log('✓ Backend connected:', d))
  .catch(e => console.error('✗ Backend error:', e))
```

**Expected:** See `✓ Backend connected:` with status info

#### Test 2: Backend ↔ ML API Connection

**In backend terminal:**
```bash
# If you have curl installed
curl -X GET http://localhost:8000/ml/health -H "Content-Type: application/json"
```

**Expected:** Returns JSON with model status

#### Test 3: Database Connection

**In backend terminal, check logs for:**
```
✓ Database connected
✓ Supabase initialized
```

**Troubleshooting:**
- Database connection failed: Check `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`
- Wrong credentials format: Verify copied exactly without spaces

---

### Phase 3: Feature Testing (10 minutes)

#### Test 1: User Authentication
- [ ] Sign up works
- [ ] Login works
- [ ] Session persists
- [ ] Logout works

**If authentication fails:**
- Check backend logs for Supabase errors
- Verify `SUPABASE_SERVICE_KEY` in `.env`
- Check Supabase project has users table

#### Test 2: Data Upload & Processing
- [ ] Upload sample tax document
- [ ] Backend processes file
- [ ] Upload shows in history
- [ ] No errors in browser console

**If upload fails:**
- Check file size (< 10MB recommended)
- Verify CORS headers in backend
- Check server logs for processing errors

#### Test 3: ML Predictions
- [ ] Make prediction on data
- [ ] Response returns within 10 seconds
- [ ] Predictions display in UI
- [ ] No console errors

**If prediction fails:**
- ML API may still be loading (30-60 seconds total)
- Check ML API window for model load status
- Verify backend can reach ML API

#### Test 4: SHAP Explanations
- [ ] SHAP dashboard loads after prediction
- [ ] Feature importance displays
- [ ] Force plot renders
- [ ] Dependence plots interactive

**If SHAP fails:**
- Check ML API has loaded explainability models
- Verify browser console for JavaScript errors
- Check SHAP response in Network tab (F12)

---

## Performance Baseline

Record these metrics to compare with production:

```
Metric                          | Target    | Local    | Render
-----------------------------------------------------------
ML API Startup Time             | 30-60s    | ___      | ___
First Prediction Response       | < 5s      | ___      | ___
SHAP Explanation Response       | < 10s     | ___      | ___
Frontend Page Load              | < 2s      | ___      | ___
Database Query (health check)   | < 500ms   | ___      | ___
```

---

## Common Issues & Solutions

### Issue: "Port Already in Use"

**Problem:** Service fails to start because port is occupied

**Solution:**
```powershell
# Stop all services
.\STOP_SERVERS.ps1

# Or manually kill processes
Get-Process python | Stop-Process -Force
Get-Process node | Stop-Process -Force

# Restart
.\START_ALL_SERVERS_SPLIT.ps1
```

---

### Issue: "ML API Not Responding"

**Problem:** Backend can't connect to ML API

**Checklist:**
- [ ] ML API window shows "Application startup complete"
- [ ] ML API took full 30-60 seconds to load
- [ ] Firewall isn't blocking localhost:8000
- [ ] Check `ml_api.py` console for errors

**Solution:**
```powershell
# Manually test ML API
curl http://localhost:8000/ml/health

# If timeout: restart ML API window
# If error response: check console for specific error
```

---

### Issue: "CORS Errors in Browser"

**Problem:** Browser blocks requests between services

**Solution:**
1. Backend `.env` has correct `CORS_ORIGIN=http://localhost:5173`
2. Restart backend after changing `.env`
3. Clear browser cache (Ctrl+Shift+Delete)
4. Hard refresh browser (Ctrl+Shift+R)

---

### Issue: "Database Connection Failed"

**Problem:** Backend can't reach Supabase

**Checklist:**
- [ ] `SUPABASE_URL` is correct (check Supabase dashboard)
- [ ] `SUPABASE_SERVICE_KEY` is correct (not anon key)
- [ ] No extra spaces in credentials
- [ ] Supabase project is active
- [ ] Network connection working

**Solution:**
```powershell
# Test Supabase connection manually from Node.js
node
> const fetch = require('node-fetch');
> fetch('https://your-supabase-url/rest/v1/')
>   .then(r => r.json())
>   .then(d => console.log(d))
```

---

### Issue: "SHAP Dashboard Empty"

**Problem:** No explanations display

**Checklist:**
- [ ] ML API fully loaded (check window)
- [ ] Prediction completed successfully
- [ ] Browser console has no errors
- [ ] SHAP models exist in `models/` directory

**Solution:**
```powershell
# Check SHAP models exist
ls models/document_classifier/
ls models/ml_models/

# If missing: Train models first
python scripts/train_models.py
```

---

## Validation Checklist

Before proceeding to production deployment, verify:

### Backend & ML API
- [ ] `.\START_ALL_SERVERS_SPLIT.ps1` runs without errors
- [ ] ML API reaches "Application startup complete"
- [ ] Backend log shows "Server running on port 3001"
- [ ] Backend shows "Connected to ML API"
- [ ] Database connection successful
- [ ] All three windows stay open (no crashes)

### Frontend
- [ ] Frontend loads at http://localhost:5173
- [ ] No CORS errors in browser console
- [ ] Navigation works
- [ ] API calls show in Network tab

### Features
- [ ] Authentication works (signup/login)
- [ ] File upload works
- [ ] Predictions return correctly
- [ ] SHAP explanations display
- [ ] No unhandled errors in console

### Performance
- [ ] ML API startup: 30-60 seconds
- [ ] First prediction: < 10 seconds
- [ ] SHAP explanation: < 15 seconds
- [ ] Frontend interactive: < 3 seconds

---

## Ready for Production?

If all checks pass ✓, you're ready to:

1. **Commit to GitHub**
   ```powershell
   git add .
   git commit -m "Ready for production deployment"
   git push origin main
   ```

2. **Deploy to Render**
   - See `DEPLOYMENT_SPLIT_ARCHITECTURE.md`

3. **Deploy to Vercel**
   - See `DEPLOYMENT_SPLIT_ARCHITECTURE.md`

---

## Need Help?

**Check These Files:**
- Backend errors: `docs/backend-example/.env` and server logs
- ML API errors: `ml_api.py` console output
- Frontend errors: Browser console (F12)
- Database errors: Supabase dashboard > Logs

**Debug Commands:**

```powershell
# Check all ports
netstat -ano | findstr "8000\|3001\|5173"

# Kill process by PID
taskkill /PID <pid> /F

# Test connectivity
Test-NetConnection localhost -Port 8000
Test-NetConnection localhost -Port 3001
Test-NetConnection localhost -Port 5173
```

---

## Next Steps

Once local testing is complete and successful:

1. ✅ Push code to GitHub repository
2. ✅ Follow `DEPLOYMENT_SPLIT_ARCHITECTURE.md`
3. ✅ Deploy backend to Render
4. ✅ Deploy frontend to Vercel
5. ✅ Configure GitHub Actions for keep-alive
6. ✅ Monitor first week in production

Good luck! 🚀