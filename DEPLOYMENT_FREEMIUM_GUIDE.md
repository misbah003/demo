# 🚀 Complete Deployment Guide: Vercel → Render → Supabase (FREE TIER)

**Status**: Production Ready ✅  
**Timeline**: 45-60 minutes  
**Cost**: €0/month (free tier)  
**Architecture**: Frontend on Vercel | Backend + ML on Render | Database on Supabase

---

## 📋 Pre-Deployment Checklist

Before you start, ensure:

- [ ] GitHub account with this repository pushed
- [ ] Vercel account (connect GitHub during setup)
- [ ] Render account (render.com, free tier)
- [ ] Supabase project active with credentials
- [ ] All environment variables collected
- [ ] ML models present in `optimized_models_25000_samples/`

---

## 🎯 STEP 1: Prepare Your Repository

### 1.1 Update Frontend Environment Variables

Frontend needs to point to **your Render backend URL** (you'll create this in Step 2).

**File: `web/.env.production`**

Create or update with:

```env
# These will be injected by Vercel automatically from environment variables
# But you can also hardcode them if needed

# Supabase (public keys - safe to expose)
VITE_SUPABASE_PROJECT_ID=ikqcakganqabiscsibyim
VITE_SUPABASE_PUBLISHABLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrcWNha2dhbnFhYmlzY3NpYnltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNjc0NDIsImV4cCI6MjA3Mzk0MzQ0Mn0.hkfGO88f95rQO_7bwsRcxADjZRAjw5LoWFxmq5mNY90
VITE_SUPABASE_URL=https://ikqcakganqabiscsibyim.supabase.co

# Backend URL - REPLACE with your Render service URL
# Format: https://your-service-name.onrender.com
VITE_BACKEND_URL=https://your-backend-service.onrender.com
```

### 1.2 Verify ML Models Are Present

```bash
# Check models directory exists and has required files
ls -la optimized_models_25000_samples/

# Should contain:
# - random_forest_optimized.pkl
# - gradient_boosting_optimized.pkl
# - ridge_optimized.pkl
# - scaler.pkl
# - label_encoders.pkl
# - feature_columns.pkl
```

### 1.3 Commit Changes

```bash
git add web/.env.production
git commit -m "Add production environment configuration"
git push origin main
```

---

## 🎯 STEP 2: Deploy Backend + ML API on Render (First!)

**IMPORTANT**: Deploy backend FIRST, get the URL, then update frontend `.env.production`.

### 2.1 Create Render Account & Connect GitHub

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize GitHub access
4. Create new Web Service

### 2.2 Create New Web Service on Render

1. Dashboard → **New +** → **Web Service**
2. **Connect Repository**:
   - Select your GitHub repo
   - Branch: `main`
   - Root Directory: `.` (or leave blank)

3. **Basic Settings**:
   - **Name**: `navi-tax-ml-api`
   - **Environment**: `Python 3.9`
   - **Plan**: `Free` ✅
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     gunicorn -w 2 -b 0.0.0.0:$PORT ml.ml_api_service_optimized:app
     ```

4. **Environment Variables** → Add these:

   | Key | Value |
   |-----|-------|
   | `PYTHON_VERSION` | `3.9.18` |
   | `PORT` | `10000` |

   > **Note**: Render automatically sets `$PORT`. Don't override it.

5. **Advanced Settings**:
   - ✅ Enable "Auto-Deploy" on push
   - ⏱️ Set max build time to 20 minutes (models are heavy)

6. Click **Create Web Service**

### 2.3 Wait for First Deploy

- ⏱️ **First deploy: 10-15 minutes** (installs all dependencies, downloads models)
- 📊 Watch the build log in Render dashboard
- ✅ When complete, you'll get a URL like: `https://navi-tax-ml-api.onrender.com`

### 2.4 Test Render Backend is Live

Once deployed, test your API:

```bash
# Test health endpoint
curl https://navi-tax-ml-api.onrender.com/health

# Expected response:
# {"status": "healthy", "models_loaded": true, "timestamp": "..."}

# Test validation reference
curl https://navi-tax-ml-api.onrender.com/validation-reference

# Should return valid categories, regions, etc.
```

### 2.5 Get Your Render Service URL

Copy the URL: `https://navi-tax-ml-api.onrender.com`

---

## 🎯 STEP 3: Update Frontend with Backend URL

Now that you have your Render URL, update the frontend:

### 3.1 Update `.env.production`

**File: `web/.env.production`**

```env
VITE_SUPABASE_PROJECT_ID=ikqcakganqabiscsibyim
VITE_SUPABASE_PUBLISHABLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrcWNha2dhbnFhYmlzY3NpYnltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNjc0NDIsImV4cCI6MjA3Mzk0MzQ0Mn0.hkfGO88f95rQO_7bwsRcxADjZRAjw5LoWFxmq5mNY90
VITE_SUPABASE_URL=https://ikqcakganqabiscsibyim.supabase.co

# UPDATE THIS with your actual Render URL
VITE_BACKEND_URL=https://navi-tax-ml-api.onrender.com
```

### 3.2 Commit & Push

```bash
git add web/.env.production
git commit -m "Update backend URL to production Render service"
git push origin main
```

---

## 🎯 STEP 4: Deploy Frontend on Vercel

### 4.1 Create Vercel Account & Connect GitHub

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Authorize GitHub
4. Import project

### 4.2 Import Project

1. **New Project** → Select your GitHub repo
2. **Framework Preset**: `Vite`
3. **Project Settings**:
   - **Root Directory**: `web`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Environment Variables**:
   
   | Key | Value |
   |-----|-------|
   | `VITE_SUPABASE_PROJECT_ID` | `ikqcakganqabiscsibyim` |
   | `VITE_SUPABASE_PUBLISHABLE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrcWNha2dhbnFhYmlzY3NpYnltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNjc0NDIsImV4cCI6MjA3Mzk0MzQ0Mn0.hkfGO88f95rQO_7bwsRcxADjZRAjw5LoWFxmq5mNY90` |
   | `VITE_SUPABASE_URL` | `https://ikqcakganqabiscsibyim.supabase.co` |
   | `VITE_BACKEND_URL` | `https://navi-tax-ml-api.onrender.com` |

5. Click **Deploy**

### 4.3 Wait for Vercel Build

- ⏱️ **Frontend deploy: 2-5 minutes**
- ✅ You'll get a URL like: `https://navi-tax-35-main.vercel.app`

---

## 🎯 STEP 5: Verify Supabase Configuration

### 5.1 Ensure Database Tables Exist

1. Go to [supabase.co](https://supabase.co)
2. Dashboard → Your Project
3. SQL Editor → Run migration scripts if needed

### 5.2 Check Row Level Security (RLS)

1. **Authentication** tab → Ensure JWT is configured
2. **Database** → Tables → Check RLS policies

---

## ✅ STEP 6: Full System Test

### 6.1 Test Frontend

```
https://navi-tax-35-main.vercel.app
```

- ✅ Page loads
- ✅ Auth page accessible
- ✅ Can sign up
- ✅ Dashboard loads after login
- ✅ ML prediction form visible

### 6.2 Test API Connection

Once logged in, try VAT refund prediction:

1. Fill in prediction form
2. Click "Predict"
3. Should see prediction result + SHAP explanation

### 6.3 Check Network Requests

**Browser DevTools** → Network tab:

- `POST /predict` → Status `200` → Render
- `POST /explain` → Status `200` → Render
- Auth requests → Status `200` → Supabase

---

## 🔧 TROUBLESHOOTING

### Issue: "Backend not responding"

**Solution**: 
1. Check Render service is running: https://navi-tax-ml-api.onrender.com/health
2. Verify `VITE_BACKEND_URL` in Vercel matches your Render URL
3. Wait 30 seconds (cold start)

### Issue: "Models not loaded"

**Solution**:
1. Check Render build logs for download errors
2. Verify `optimized_models_25000_samples/` exists in repo
3. Check file paths are correct

### Issue: CORS errors

**Solution**:
- CORS is already enabled in ML API
- If still failing, check that Vercel domain is not blocked
- ML API has: `CORS(app)` enabled for all origins

### Issue: "Build failed on Vercel"

**Solution**:
1. Check Node version: should be `18.x` or `20.x`
2. Run locally: `npm install && npm run build` in `web/` directory
3. Check for TypeScript errors: `npm run lint`

### Issue: "Free tier sleep after 15 minutes"

**Solution** (for Render):
- Free tier services pause after 15 mins inactivity
- On next request, they spin up (5-10 second delay)
- **Recommended**: Add uptime monitoring via [uptimerobot.com](https://uptimerobot.com) (free)

---

## 📊 Monitoring & Maintenance

### Free Tier Limits:

| Service | Free Limit | Cost if Exceeded |
|---------|-----------|-----------------|
| Vercel | 100 GB bandwidth/month | $0.50/GB overage |
| Render | 750 hours/month | Auto-paused after |
| Supabase | 500 MB storage | $5/month |

### Monitor Render Service

1. Render Dashboard → Your service
2. Watch "Logs" for errors
3. Check "Metrics" for CPU/memory

### Monitor Vercel Deployment

1. Vercel Dashboard → Your project
2. Check "Analytics" tab
3. Monitor "Failed Requests"

---

## 🚀 Next Steps: Scaling Beyond Free Tier

When you're ready to scale:

### Option 1: Render Paid
- Upgrade to **$7/month** (keeps service always on)
- Better CPU/memory for ML predictions

### Option 2: AWS Lambda + API Gateway
- Pay-per-use for predictions
- ~$0.02 per prediction (very cheap)

### Option 3: DigitalOcean App Platform
- $12/month for reliable backend
- Better than Render for production

---

## 📋 Deployment Checklist

Before going live, verify:

- [ ] Git repository pushed with all code
- [ ] Render service deployed and health check passing
- [ ] Vercel frontend deployed without errors
- [ ] Backend URL correctly set in frontend `.env`
- [ ] Supabase database initialized
- [ ] Full end-to-end test completed
- [ ] CORS working (no cross-origin errors)
- [ ] Authentication redirects working
- [ ] Predictions returning correct results
- [ ] Error handling working (invalid inputs rejected)

---

## 🎯 Quick Reference URLs

Once deployed, save these:

```
Frontend: https://navi-tax-35-main.vercel.app
Backend:  https://navi-tax-ml-api.onrender.com
Database: https://ikqcakganqabiscsibyim.supabase.co
```

---

**Questions?** Check logs:
- Render: Dashboard → Logs
- Vercel: Dashboard → Deployments → Logs
- Supabase: Dashboard → Logs

**Estimated time to production: 1 hour** ⏱️