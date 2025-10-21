# Split Architecture Deployment Guide 🚀

## Architecture Overview

```
Frontend (Vercel) → Backend + ML API (Render) → Supabase
```

- **Frontend**: React/TypeScript on Vercel CDN (Global, Fast)
- **Backend + ML API**: Express.js + Python FastAPI on Render (Shared dyno, 750 hrs/month free)
- **Database**: Supabase PostgreSQL (Already configured)

---

## 📋 Pre-Deployment Checklist

### 1. Accounts Setup
- ✅ **Vercel Account**: [vercel.com](https://vercel.com) - Sign up with GitHub
- ✅ **Render Account**: [render.com](https://render.com) - Sign up with GitHub
- ✅ **Supabase Already Configured** (Check `.env` for credentials)

### 2. GitHub Repository
Push your project to GitHub:
```bash
git init
git add .
git commit -m "Initial commit for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/navi-tax.git
git push -u origin main
```

---

## 🚀 Step 1: Deploy Backend + ML API on Render

### 1.1 Create Render Service

1. Go to [render.com](https://render.com) → Dashboard → New +
2. Select **"Web Service"**
3. Connect your GitHub repository
4. Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `navi-tax-api` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Runtime** | `Python 3.11` |
| **Build Command** | See below ⬇️ |
| **Start Command** | See below ⬇️ |

### 1.2 Build & Start Commands

**Build Command:**
```bash
pip install -r requirements.txt && npm install --prefix web
```

**Start Command:**
```bash
python ml/ml_api.py &
cd docs/backend-example && npm start
```

> ⚠️ Note: This starts both ML API (port 8000) and Backend (port 3001)

### 1.3 Environment Variables (Add to Render Dashboard)

Go to **"Environment"** tab and add:

```env
# Supabase
SUPABASE_URL=https://ikqcakganqabiscsibym.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrcWNha2dhbnFhYmlzY3NpYnltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNjc0NDIsImV4cCI6MjA3Mzk0MzQ0Mn0.hkfGO88f95rQO_7bwsRcxADjZRAjw5LoWFxmq5mNY90

# Backend
PORT=3001
NODE_ENV=production
BACKEND_URL=https://navi-tax-api.onrender.com

# ML API
ML_API_PORT=8000
ML_API_URL=http://localhost:8000
```

### 1.4 Click "Deploy"
- Wait 5-10 minutes for deployment
- Check logs for errors
- You'll see: `navi-tax-api.onrender.com`

---

## 🎨 Step 2: Deploy Frontend on Vercel

### 2.1 Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) → Dashboard → New Project
2. Import GitHub repository
3. Select `web` folder as root:
   - **Framework**: Vite
   - **Root Directory**: `./web`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 2.2 Environment Variables (Vercel)

Go to **"Settings"** → **"Environment Variables"** and add:

```env
VITE_SUPABASE_URL=https://ikqcakganqabiscsibym.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrcWNha2dhbnFhYmlzY3NpYnltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNjc0NDIsImV4cCI6MjA3Mzk0MzQ0Mn0.hkfGO88f95rQO_7bwsRcxADjZRAjw5LoWFxmq5mNY90
VITE_SUPABASE_PROJECT_ID=ikqcakganqabiscsibym
VITE_BACKEND_URL=https://navi-tax-api.onrender.com
```

### 2.3 Click "Deploy"
- Wait 2-3 minutes
- You'll get a Vercel URL: `navi-tax.vercel.app`

---

## 🔗 Step 3: Connect Everything

### 3.1 Update API URLs

Once you have your Render URL, update in Vercel:

1. Go to Vercel Project Settings → Environment Variables
2. Update: `VITE_BACKEND_URL=https://navi-tax-api.onrender.com`
3. Redeploy

### 3.2 Update Backend CORS (if needed)

Edit `docs/backend-example/server.js`:

```javascript
const cors = require('cors');

app.use(cors({
  origin: ['https://navi-tax.vercel.app', 'http://localhost:3000'],
  credentials: true
}));
```

---

## ✅ Testing the Deployment

### 1. Test Backend
```bash
curl https://navi-tax-api.onrender.com/health
```

### 2. Test ML API
```bash
curl https://navi-tax-api.onrender.com/ml/health
```

### 3. Test Frontend
- Open: https://navi-tax.vercel.app
- Check browser console (F12) for any errors
- Try uploading a document

---

## ⚡ Performance Optimization

### For Render (Free Tier)
- ML API takes **30-60 seconds** to load on first request (cold start)
- After that, responses are **<2 seconds**
- Service auto-spins down after 15 min inactivity
- To keep it warm, add a cron job:

Create `.github/workflows/keep-alive.yml`:
```yaml
name: Keep Render Alive
on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes
jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Ping backend
        run: curl https://navi-tax-api.onrender.com/health
```

### For Vercel
- Already optimized with automatic code splitting
- Global CDN cache
- Edge functions ready

---

## 🐛 Troubleshooting

### "ENOENT: no such file or directory"
- Check that all model files are in `models/` folder
- Verify `requirements.txt` has all Python dependencies

### "Cannot find module 'nodemailer'"
- Render didn't install dependencies
- Re-trigger deploy: `git commit --allow-empty -m "Trigger rebuild" && git push`

### "ML API timeout"
- First request takes 60 seconds
- Increase Render timeout in settings if needed

### "CORS errors in frontend"
- Update backend CORS settings
- Ensure `VITE_BACKEND_URL` matches Render URL

---

## 📊 Monitoring

### Render Logs
- Dashboard → Your Service → Logs tab
- Check for errors and performance

### Vercel Analytics
- Dashboard → Project → Analytics
- See page load times and errors

### Supabase Dashboard
- Check database queries and logs
- Monitor real-time activity

---

## 💾 Database Backups

Your Supabase database is automatically backed up. To export manually:

```bash
# In Supabase Dashboard
Settings → Database → Backups → Download
```

---

## 🔐 Security Checklist

- ✅ Environment variables not in code
- ✅ CORS properly configured
- ✅ API keys rotated monthly
- ✅ HTTPS enforced (automatic)
- ✅ Rate limiting enabled (configure on Render/Vercel)

---

## 📱 Local Testing Before Deployment

Test locally first:

```bash
# Terminal 1: ML API
cd ml
python ml_api.py

# Terminal 2: Backend
cd docs/backend-example
npm install
npm start

# Terminal 3: Frontend
cd web
npm install
npm run dev
```

Then visit: `http://localhost:5173`

---

## 🎯 Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| Vercel | ✅ Unlimited | $0 |
| Render | ✅ 750 hrs/month | $0 |
| Supabase | ✅ (Limited) | $0 |
| **Total** | | **$0/month** |

---

## 📞 Support & Docs

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Supabase Docs**: [supabase.com/docs](https://supabase.com/docs)

---

**Ready to deploy? Start with Render first, then Vercel! 🚀**