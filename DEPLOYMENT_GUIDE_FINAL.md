# 🚀 Complete Deployment Guide: Vercel + Render + Supabase

This guide walks you through deploying the Navi Tax system to production using the free tiers of Vercel, Render, and Supabase.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│  User Browser                                       │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  FRONTEND (Vercel Free)                            │
│  - React + Vite + TailwindCSS                       │
│  - Hosted at: https://navi-tax.vercel.app          │
│  - Environment: /web                               │
└────────────┬─────────────────────────────────────┬──┘
             │                                     │
             ▼                                     ▼
┌─────────────────────────────┐  ┌────────────────────────────┐
│ BACKEND (Render Free)       │  │ ML API (Render Free)       │
│ https://navi-tax-...        │  │ https://navi-tax-...       │
│ onrender.com:3001           │  │ onrender.com:8000          │
│ - Node.js Express           │  │ - Python Flask             │
│ - /docs/backend-example     │  │ - /ml                      │
│ - Handles uploads, emails   │  │ - SHAP predictions         │
└────────┬────────────────────┘  └──────────┬─────────────────┘
         │                                  │
         └──────────────┬───────────────────┘
                        ▼
         ┌──────────────────────────────┐
         │  SUPABASE (PostgreSQL)       │
         │  - Database                  │
         │  - Authentication            │
         │  - Edge Functions (optional) │
         └──────────────────────────────┘
```

---

## 📋 Prerequisites

- [ ] GitHub account
- [ ] Vercel account (free tier)
- [ ] Render account (free tier)
- [ ] Supabase account (free tier)
- [ ] Repository forked/cloned on GitHub

---

## ✅ Step 1: Setup Supabase Database

### 1.1 Create Supabase Project

1. Go to https://app.supabase.com/sign-up
2. Create new project:
   - **Project Name:** `navi-tax`
   - **Database Password:** Save this securely! ⚠️
   - **Region:** Choose closest to your users

### 1.2 Get Credentials

After project is created, go to **Settings → API**:

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_KEY=eyJhbGc... (Keep SECRET!)
```

Save these values - you'll need them for both Render and Vercel.

### 1.3 Setup Database Schema

Run migrations:
```bash
cd web/supabase
supabase db pull  # If you have migrations
# OR manually import SQL from /web/supabase/migrations/
```

---

## 🌐 Step 2: Deploy Frontend to Vercel

### 2.1 Push Code to GitHub

```bash
git add .
git commit -m "Ready for production deployment"
git push origin main
```

### 2.2 Deploy to Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Select `web` folder as root:
   - **Framework:** Vite
   - **Root Directory:** `./web`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

### 2.3 Configure Environment Variables

In Vercel dashboard, go to **Settings → Environment Variables** and add:

```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=eyJhbGc...
VITE_BACKEND_URL=https://navi-tax-backend.onrender.com
VITE_ML_API_URL=https://navi-tax-ml-api.onrender.com
```

**Note:** Replace `navi-tax-backend` and `navi-tax-ml-api` with YOUR actual Render service names.

### 2.4 Deploy

Click "Deploy" - Vercel will handle everything. Your frontend will be live in ~3-5 minutes.

✅ Frontend URL: `https://your-project-name.vercel.app`

---

## ⚙️ Step 3: Deploy ML API to Render

### 3.1 Create Render Account

Go to https://render.com/signup

### 3.2 Create ML API Service

1. Dashboard → **New** → **Web Service**
2. Connect your GitHub repository
3. Configure:

   | Setting | Value |
   |---------|-------|
   | **Name** | `navi-tax-ml-api` |
   | **Root Directory** | `.` (empty) |
   | **Runtime** | Python 3.11 |
   | **Build Command** | `pip install --no-cache-dir -r requirements.txt` |
   | **Start Command** | `gunicorn --workers 2 --bind 0.0.0.0:$PORT --timeout 120 'ml.ml_api_service_optimized:app'` |
   | **Plan** | Free |

### 3.3 Add Environment Variables

In Render dashboard, go to your service **Environment**:

```env
FLASK_ENV=production
ML_API_PORT=$PORT
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGc...
```

### 3.4 Deploy

Click "Create Web Service" - Render will start deployment.

⏳ **First deployment takes 5-10 minutes** (installing TensorFlow, scikit-learn, etc.)

✅ ML API URL: `https://navi-tax-ml-api.onrender.com`

---

## 🔙 Step 4: Deploy Backend to Render

### 4.1 Create Backend Service

1. Dashboard → **New** → **Web Service**
2. Connect your GitHub repository
3. Configure:

   | Setting | Value |
   |---------|-------|
   | **Name** | `navi-tax-backend` |
   | **Root Directory** | `.` |
   | **Runtime** | Node 20 |
   | **Build Command** | `cd docs/backend-example && npm install` |
   | **Start Command** | `cd docs/backend-example && npm start` |
   | **Plan** | Free |

### 4.2 Add Environment Variables

```env
NODE_ENV=production
PORT=3001
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGc...
SUPABASE_ANON_KEY=eyJhbGc...
ML_API_URL=https://navi-tax-ml-api.onrender.com
```

### 4.3 Deploy

Click "Create Web Service"

✅ Backend URL: `https://navi-tax-backend.onrender.com`

---

## 🔗 Step 5: Update Frontend Environment Variables

Now that you have the actual URLs, update Vercel environment variables:

1. Go to Vercel dashboard → Your project → **Settings → Environment Variables**
2. Update these with ACTUAL URLs:

```env
VITE_BACKEND_URL=https://navi-tax-backend.onrender.com
VITE_ML_API_URL=https://navi-tax-ml-api.onrender.com
```

3. Redeploy frontend: **Deployments → Select latest → Click "Redeploy"**

---

## 🧪 Step 6: Test the Deployment

### Test 1: Frontend Loading
```
https://your-project.vercel.app
```
✅ Should load without errors

### Test 2: API Health Check
```bash
curl https://navi-tax-ml-api.onrender.com/health
```
✅ Should return: `{"status":"healthy"}`

### Test 3: Backend Health
```bash
curl https://navi-tax-backend.onrender.com/health
```
✅ Should respond

### Test 4: Make a Prediction
```bash
curl -X POST https://navi-tax-ml-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Amount": 10000,
    "VAT_Rate": 0.19,
    "Risk_Score": 0.3,
    "Annual_Turnover": 100000,
    "Category": "Product Sales",
    "Region": "EU",
    "Filing_Status": "Quarterly",
    "Compliance_Flag": 1,
    "Refund_Eligible": 1,
    "Is_Anomaly": 0
  }'
```
✅ Should return a prediction

---

## ⚠️ Important Notes for Free Tier

### Render Free Tier Limitations:
- **Automatic shutdown:** Services will spin down after 15 minutes of inactivity
- **Slow first request:** Cold starts take ~1-2 minutes
- **No persistence:** Uploads are temporary (upload to Supabase Storage instead)
- **Limited resources:** 512MB RAM, shared CPU

### Solutions:
1. **Keep services warm:** Use monitoring tools (e.g., Uptime Robot)
2. **Increase timeouts:** Already set to 120 seconds in gunicorn
3. **Optimize code:** Use optimized ML models
4. **Use Supabase Storage:** For file uploads instead of local disk

### Vercel Free Tier:
- ✅ No automatic shutdown
- ✅ Fast edge network
- ✅ Unlimited deployments
- ⚠️ 12 MB total function size

---

## 📊 Monitoring Deployment

### Check Service Status

**Render Dashboard:**
- Services → Your service → Logs
- Check for errors during startup

**Vercel Dashboard:**
- Deployments → Click deployment
- View build logs

### Monitor Uptime (Free)
Use Uptime Robot to keep services warm:
https://uptimerobot.com/
- Ping ML API every 5 minutes: `https://navi-tax-ml-api.onrender.com/health`
- Ping Backend every 5 minutes: `https://navi-tax-backend.onrender.com/health`

---

## 🔐 Security Checklist

- [ ] Use environment variables (never hardcode secrets)
- [ ] Keep `SUPABASE_SERVICE_KEY` secret (only in backend/Render)
- [ ] Frontend gets only `SUPABASE_ANON_KEY`
- [ ] Enable CORS properly (whitelist your Vercel domain)
- [ ] Use HTTPS everywhere (automatic on Vercel/Render)
- [ ] Rotate secrets regularly

---

## 🐛 Troubleshooting

### ML API returns 503 Service Unavailable
→ Service is starting up (cold start). Wait 1-2 minutes and retry.

### Frontend shows "Cannot connect to backend"
→ Check Render service is running. Go to Render dashboard and manually restart if needed.

### Models not found error
→ Verify `optimized_models_25000_samples/` folder is in repository root.

### Supabase connection fails
→ Double-check environment variables on Render and Vercel.

---

## 📞 Support Resources

- **Vercel Docs:** https://vercel.com/docs
- **Render Docs:** https://render.com/docs
- **Supabase Docs:** https://supabase.com/docs
- **Flask Guide:** https://flask.palletsprojects.com/

---

## ✨ Next Steps

After deployment:
1. ✅ Test all features in production
2. ✅ Monitor error logs
3. ✅ Set up automated backups
4. ✅ Plan scaling strategy
5. ✅ Consider upgrading to paid tiers if needed

---

**Deployment Date:** [Enter date]  
**Deployed By:** [Your name]  
**Status:** ✅ Live