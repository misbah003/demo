# 🔐 Environment Variables Reference

Quick lookup for where each env var goes and what value it should have.

---

## 📋 Variables Needed - By Source

### From Step 1: Gmail Setup
```
GMAIL_USER = your-email@gmail.com
GMAIL_APP_PASSWORD = xxxx xxxx xxxx xxxx (16 chars)
```
**Where it goes:**
- ✅ Render Backend Dashboard (Environment section)

---

### From Step 2: Supabase
```
SUPABASE_URL = https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Location:** Supabase Dashboard → Settings → API

**Where they go:**
- `SUPABASE_URL` → Render Backend + Render ML API
- `VITE_SUPABASE_ANON_KEY` → Vercel Frontend (with VITE_ prefix)
- `SUPABASE_SERVICE_KEY` → Render Backend ONLY (secret!)

---

### From Step 4: ML API (auto-generated)
```
ML_API_URL = https://navi-tax-ml-api.onrender.com
```

**How to get:** After deploying ML API on Render, you'll see this URL

**Where it goes:**
- ✅ Render Backend Dashboard (Environment section)
- ✅ Vercel Frontend as `VITE_ML_API_URL`

---

### From Step 3: Vercel (auto-generated)
```
VERCEL_FRONTEND_URL = https://your-project.vercel.app
```

**How to get:** Vercel gives you this URL after deployment

**Where it goes:**
- ✅ Render Backend as `FRONTEND_URL` (for CORS)

---

## 📊 Variables by Platform

### 🌐 VERCEL FRONTEND

**Go to:** Vercel Dashboard → Your Project → Settings → Environment Variables

| Variable Name | Value | Source | Notes |
|---|---|---|---|
| `VITE_SUPABASE_URL` | `https://your-project.supabase.co` | Supabase | Public - safe for frontend |
| `VITE_SUPABASE_ANON_KEY` | (anon key from Supabase) | Supabase | Public - safe for frontend |
| `VITE_API_URL` | `https://navi-tax-backend.onrender.com` | Render Backend | Backend API endpoint |
| `VITE_ML_API_URL` | `https://navi-tax-ml-api.onrender.com` | Render ML API | ML predictions endpoint |

**After adding variables:**
1. Save
2. Go to Deployments tab
3. Click latest deployment's "..." menu
4. Select "Redeploy"

---

### 🤖 RENDER ML API

**Go to:** Render Dashboard → ML API Service → Environment

| Variable Name | Value | Source | Notes |
|---|---|---|---|
| `FLASK_ENV` | `production` | Static | Always this value |

**That's it!** ML API doesn't need Supabase or other variables.

---

### 🔧 RENDER BACKEND

**Go to:** Render Dashboard → Backend Service → Environment

| Variable Name | Value | Source | Notes |
|---|---|---|---|
| `GMAIL_USER` | `your-email@gmail.com` | Gmail | Your Gmail address |
| `GMAIL_APP_PASSWORD` | `xxxx xxxx xxxx xxxx` | Gmail | App-specific password |
| `SUPABASE_URL` | `https://your-project.supabase.co` | Supabase | Database URL |
| `SUPABASE_SERVICE_KEY` | (service key) | Supabase | ⚠️ KEEP SECRET |
| `ML_API_URL` | `https://navi-tax-ml-api.onrender.com` | Render | ML predictions |
| `FRONTEND_URL` | `https://your-project.vercel.app` | Vercel | For CORS |
| `PORT` | `3001` | Static | Backend port |
| `NODE_ENV` | `production` | Static | Always this value |

---

## 🔍 How to Find Each Value

### Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select: "Other (custom name)" → "Tax Intelligence Backend"
3. Click Generate
4. Copy the 16-character password (with spaces)

### Supabase URLs & Keys
1. Go to https://app.supabase.com
2. Select your project
3. Click "Settings" → "API"
4. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **Anon public key** → `VITE_SUPABASE_ANON_KEY`
   - **Service role key** → `SUPABASE_SERVICE_KEY`

### Render Service URLs
1. Go to https://dashboard.render.com
2. Click each service
3. Copy the URL from the top of the page
   - ML API → `ML_API_URL`
   - Backend → `VITE_API_URL`

### Vercel Frontend URL
1. Go to https://vercel.com/dashboard
2. Click your project
3. Copy the URL shown at the top or in Deployments tab

---

## ✅ Checklist: Did I Add Everything?

### ✅ Supabase Setup
- [ ] Project created at supabase.com
- [ ] Migrations run successfully
- [ ] Storage buckets created (documents, uploads)
- [ ] Copied SUPABASE_URL
- [ ] Copied VITE_SUPABASE_ANON_KEY (public)
- [ ] Copied SUPABASE_SERVICE_KEY (secret!)

### ✅ Gmail Setup
- [ ] 2FA enabled on Gmail
- [ ] App password generated
- [ ] Copied GMAIL_USER
- [ ] Copied GMAIL_APP_PASSWORD

### ✅ Vercel Frontend
- [ ] Project deployed
- [ ] Added VITE_SUPABASE_URL
- [ ] Added VITE_SUPABASE_ANON_KEY
- [ ] Added VITE_API_URL (backend)
- [ ] Added VITE_ML_API_URL (ML)
- [ ] Redeployed after adding vars

### ✅ Render ML API
- [ ] Service created
- [ ] Deployed successfully
- [ ] Health check responds (/health)
- [ ] Copied ML_API_URL

### ✅ Render Backend
- [ ] Service created
- [ ] Added GMAIL_USER
- [ ] Added GMAIL_APP_PASSWORD
- [ ] Added SUPABASE_URL
- [ ] Added SUPABASE_SERVICE_KEY
- [ ] Added ML_API_URL
- [ ] Added FRONTEND_URL
- [ ] Deployed successfully

---

## 🚨 Security Reminders

### ⚠️ NEVER Share or Commit
- `GMAIL_APP_PASSWORD` - Email access
- `SUPABASE_SERVICE_KEY` - Full database admin access
- `GMAIL_USER` - Email address

### ✅ Safe to Share/Commit
- `VITE_SUPABASE_ANON_KEY` - Frontend only, limited access
- `SUPABASE_URL` - Project identifier
- Application URLs (Vercel, Render)

### 🔒 Where to Store Each
- **Secrets** → Platform dashboards (Render, Vercel) only
- **Public Keys** → `.env.example` (no values, just structure)
- **URLs** → Can be in code/config files

---

## 🔄 Update Sequence

If you need to change values later:

1. **Update in Render/Vercel Dashboard**
   ```
   Render: Service → Environment → Edit → Save
   Vercel: Project → Settings → Environment Variables → Edit → Save
   ```

2. **Redeploy Services**
   ```
   Render: Auto-redeployed on env var save
   Vercel: Settings → Deployments → Redeploy latest
   ```

3. **Test Services**
   ```
   ML API:  https://navi-tax-ml-api.onrender.com/health
   Backend: https://navi-tax-backend.onrender.com/health
   Frontend: Visit your Vercel URL
   ```

---

## 📞 Quick Links

| Service | URL |
|---------|-----|
| Supabase Dashboard | https://app.supabase.com |
| Supabase Settings → API | https://app.supabase.com/project/_/settings/api |
| Gmail App Passwords | https://myaccount.google.com/apppasswords |
| Render Dashboard | https://dashboard.render.com |
| Vercel Dashboard | https://vercel.com/dashboard |

---

## 🎯 Troubleshooting

### "Environment variable not working"
- Wait 5 minutes after adding (sometimes takes time to propagate)
- Redeploy the service
- Check the variable name is exact (case-sensitive)

### "Services can't communicate"
- Check all URLs are correct (https://, not http://)
- Verify ML_API_URL doesn't have trailing slash
- Check FRONTEND_URL in backend CORS settings

### "Email not sending"
- Verify GMAIL_USER is correct
- Check app password is 16 characters (with spaces)
- Ensure 2FA is enabled on Gmail

---

**Need help?** Refer back to `DEPLOY_NOW.md` for step-by-step instructions.
