# 🚀 Deployment Checklist: Vercel + Render + Supabase

Follow these steps in order to deploy your application to production.

---

## 📋 Pre-Deployment (LOCAL)

### Code Preparation
- [ ] All code is committed and pushed to GitHub main branch
- [ ] No hardcoded API keys or secrets in code
- [ ] Environment variables are documented in `.env.example`
- [ ] All tests pass locally
- [ ] Build completes successfully: `npm run build` in `/web`

### Verify File Structure
- [ ] `optimized_models_25000_samples/` folder exists in root
- [ ] `ml/ml_api_service_optimized.py` exists and runs locally
- [ ] `docs/backend-example/server.js` exists and has start script
- [ ] `web/dist/` or `/web` folder exists with frontend code

### Run Local Tests
```bash
# Test ML API locally
python ml_api.py

# In another terminal, test ML endpoint
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"Amount": 10000, ...}'

# Test Backend locally
cd docs/backend-example && npm start

# Test Frontend build
cd web && npm run build
```

---

## ☁️ Phase 1: SUPABASE Setup

- [ ] Created Supabase project at https://app.supabase.com
- [ ] Database created successfully
- [ ] Retrieved credentials:
  - [ ] `SUPABASE_URL` = `https://xxxxx.supabase.co`
  - [ ] `SUPABASE_ANON_KEY` = `eyJ...`
  - [ ] `SUPABASE_SERVICE_KEY` = `eyJ...` (keep SECRET!)
  - [ ] `SUPABASE_PUBLISHABLE_KEY` (if different)
  - [ ] `SUPABASE_PROJECT_ID` = `xxxxx`

- [ ] Database migrations applied (if needed)
- [ ] Tables created and tested
- [ ] Users can authenticate locally with Supabase

---

## ☁️ Phase 2: FRONTEND Deployment (Vercel)

### Create & Connect
- [ ] Vercel account created: https://vercel.com
- [ ] Authorized GitHub integration
- [ ] Repository imported to Vercel

### Configure in Vercel Dashboard
- [ ] **Settings → General**
  - [ ] Project Name: `navi-tax`
  - [ ] Framework: `Vite`
  - [ ] Root Directory: `./web`
  - [ ] Build Command: `npm run build`
  - [ ] Output Directory: `dist`

- [ ] **Settings → Environment Variables**
  ```env
  VITE_SUPABASE_URL=https://xxxxx.supabase.co
  VITE_SUPABASE_PUBLISHABLE_KEY=eyJ...
  VITE_SUPABASE_PROJECT_ID=xxxxx
  VITE_BACKEND_URL=https://navi-tax-backend.onrender.com
  VITE_ML_API_URL=https://navi-tax-ml-api.onrender.com
  ```
  ⚠️ **Wait for Render URLs before setting BACKEND & ML_API URLs!**

### Deploy
- [ ] Click "Deploy" button
- [ ] Monitor build progress in Vercel dashboard
- [ ] Build completes successfully (~3-5 minutes)
- [ ] Frontend live at: `https://[project-name].vercel.app`

### Post-Deploy Test
- [ ] Open `https://[project-name].vercel.app` in browser
- [ ] No console errors in DevTools
- [ ] Page loads without errors (may show backend/ML errors which is OK)

---

## ☁️ Phase 3: ML API Deployment (Render)

### Create Service in Render
- [ ] Render account created: https://render.com
- [ ] GitHub integration authorized
- [ ] New Web Service created
- [ ] GitHub repository connected

### Configure Service
- [ ] **Service Name:** `navi-tax-ml-api`
- [ ] **Environment:** Python 3.11
- [ ] **Root Directory:** `.` (leave empty)
- [ ] **Build Command:** `pip install --no-cache-dir -r requirements.txt`
- [ ] **Start Command:** `gunicorn --workers 2 --bind 0.0.0.0:$PORT --timeout 120 'ml.ml_api_service_optimized:app'`
- [ ] **Plan:** Free

### Add Environment Variables
- [ ] `FLASK_ENV` = `production`
- [ ] `SUPABASE_URL` = (from Supabase)
- [ ] `SUPABASE_SERVICE_KEY` = (from Supabase - KEEP SECRET!)

### Deploy
- [ ] Click "Create Web Service"
- [ ] Monitor deployment in Render dashboard
- [ ] Deployment takes 5-15 minutes (first time is slow)
- [ ] Check for errors in deployment logs
- [ ] Look for message: "✅ Models loaded successfully"

### Get URL
- [ ] Copy service URL: `https://navi-tax-ml-api.onrender.com`
- [ ] Note this for Vercel/Backend configuration

### Test ML API
```bash
# Wait 2-3 minutes for cold start, then test
curl https://navi-tax-ml-api.onrender.com/health
# Should return: {"status":"healthy",...}

# Make a prediction
curl -X POST https://navi-tax-ml-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"Amount": 10000, "VAT_Rate": 0.19, ...}'
```

---

## ☁️ Phase 4: BACKEND Deployment (Render)

### Create Service in Render
- [ ] New Web Service created
- [ ] GitHub repository connected

### Configure Service
- [ ] **Service Name:** `navi-tax-backend`
- [ ] **Environment:** Node 20
- [ ] **Root Directory:** `.`
- [ ] **Build Command:** `cd docs/backend-example && npm install`
- [ ] **Start Command:** `cd docs/backend-example && npm start`
- [ ] **Plan:** Free

### Add Environment Variables
- [ ] `NODE_ENV` = `production`
- [ ] `PORT` = `3001`
- [ ] `SUPABASE_URL` = (from Supabase)
- [ ] `SUPABASE_SERVICE_KEY` = (from Supabase - KEEP SECRET!)
- [ ] `SUPABASE_ANON_KEY` = (from Supabase)
- [ ] `ML_API_URL` = `https://navi-tax-ml-api.onrender.com`

### Deploy
- [ ] Click "Create Web Service"
- [ ] Monitor deployment in Render dashboard
- [ ] Deployment takes 3-5 minutes
- [ ] Check logs for errors

### Get URL
- [ ] Copy service URL: `https://navi-tax-backend.onrender.com`

### Test Backend
```bash
curl https://navi-tax-backend.onrender.com/health
# Should return: {"status":"OK"} or similar
```

---

## 🔗 Phase 5: LINK SERVICES TOGETHER

### Update Vercel Environment Variables
- [ ] Go back to Vercel dashboard
- [ ] **Settings → Environment Variables**
- [ ] Update these with ACTUAL URLs:
  ```env
  VITE_BACKEND_URL=https://navi-tax-backend.onrender.com
  VITE_ML_API_URL=https://navi-tax-ml-api.onrender.com
  ```
- [ ] Save changes

### Redeploy Frontend
- [ ] Go to **Deployments** tab
- [ ] Select latest deployment
- [ ] Click "Redeploy"
- [ ] Wait for build to complete

---

## ✅ Phase 6: FINAL TESTING

### Test 1: Frontend Access
- [ ] Open `https://[project-name].vercel.app`
- [ ] [ ] Page loads without errors
- [ ] [ ] Navigation works
- [ ] [ ] No console errors in DevTools

### Test 2: API Connectivity
- [ ] Frontend can reach backend (check Network tab)
- [ ] Frontend can reach ML API (check Network tab)
- [ ] No CORS errors in console

### Test 3: Make a Prediction
- [ ] Submit a prediction in the app
- [ ] See prediction result
- [ ] See SHAP explanation (if available)
- [ ] No errors in browser console

### Test 4: Data Persistence
- [ ] Upload a file to test backend
- [ ] Data persists in Supabase
- [ ] Can retrieve data on page reload

### Test 5: Authentication (if applicable)
- [ ] Sign up works
- [ ] Login works
- [ ] Session persists
- [ ] User data saves to Supabase

---

## ⚠️ Important Notes

### Render Free Tier Behavior
- ✅ Services stay up 24/7 (unlike some other free tiers)
- ❌ Services spin down after 15 minutes of inactivity
- ❌ First request after idle is slow (~1-2 minutes)
- ✅ Unlimited inactivity restarts

### Cold Start Solutions
Use Uptime Robot (free) to keep services warm:
1. Go to https://uptimerobot.com
2. Create two monitors:
   - **Monitor 1:** `https://navi-tax-ml-api.onrender.com/health` (every 5 min)
   - **Monitor 2:** `https://navi-tax-backend.onrender.com/health` (every 5 min)

This prevents cold starts during business hours.

### Secrets Management
- ✅ `SUPABASE_SERVICE_KEY` - Backend/Render only (NEVER in frontend)
- ✅ `SUPABASE_ANON_KEY` - OK in frontend (public)
- ✅ `SUPABASE_PUBLISHABLE_KEY` - OK in frontend (public)
- ❌ NEVER hardcode secrets in code

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **503 Service Unavailable** | Service is starting (cold start). Wait 2 min and retry. |
| **Cannot connect to backend** | Check Render service is running. Restart in Render dashboard. |
| **Models not found error** | Verify `optimized_models_25000_samples/` folder is in GitHub root. |
| **CORS errors** | Check `VITE_BACKEND_URL` and `VITE_ML_API_URL` are set correctly in Vercel. |
| **Supabase connection fails** | Verify env vars on Render match Supabase project. |
| **Frontend shows 404** | Wait for Vercel redeploy to complete (check Deployments tab). |

---

## 📊 Monitor & Maintain

### Weekly
- [ ] Check Render logs for errors
- [ ] Verify Vercel builds are successful
- [ ] Test predictions still working

### Monthly
- [ ] Review error logs
- [ ] Check Supabase quota usage
- [ ] Monitor response times

### As Needed
- [ ] Update dependencies
- [ ] Deploy new model versions
- [ ] Scale resources if needed

---

## ✨ Deployment Complete!

When all items are checked off:

```
✅ Frontend: https://[your-project].vercel.app
✅ Backend: https://navi-tax-backend.onrender.com
✅ ML API: https://navi-tax-ml-api.onrender.com
✅ Database: Supabase project
✅ All services connected and working
```

🎉 **Your application is now live in production!**

---

**Deployment Date:** _______________
**Deployed By:** _______________
**Notes:** _______________________________________________