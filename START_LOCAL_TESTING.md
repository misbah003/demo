# 🚀 Start Local Testing - Split Architecture

You now have everything set up to test the split architecture deployment locally before pushing to production.

## What's Been Created For You

### 1. **Startup Scripts**
- `START_ALL_SERVERS_SPLIT.ps1` - Main startup script (enhanced from original)
- `CHECK_LOCAL_HEALTH.ps1` - Quick health check for services
- `STOP_SERVERS.ps1` - Already exists, stops all services

### 2. **Documentation**
- `LOCAL_TESTING_GUIDE.md` - Comprehensive testing walkthrough
- `DEPLOYMENT_SPLIT_ARCHITECTURE.md` - Full production deployment guide
- `DEPLOYMENT_QUICK_START.md` - Quick reference

### 3. **Configuration Files**
- `web/vercel.json` - Frontend deployment config
- `render.yaml` - Backend deployment config  
- `Procfile` - Process file for Render
- `ml_api.py` - ML API entry point (production-ready)
- `.github/workflows/keep-render-alive.yml` - GitHub Actions for keep-alive

---

## Next 5 Minutes - Quick Start

### Step 1: Update Supabase Credentials (2 min)

You need your Supabase credentials to test locally.

**Get them from:** https://supabase.com/dashboard → Select your project → Settings → API Keys

**Update these files:**

1. **Backend** (`docs/backend-example/.env`)
   ```env
   SUPABASE_URL=<your_project_url>  
   SUPABASE_SERVICE_KEY=<your_service_role_key>
   ```

2. **Frontend** (`web/.env`)
   ```env
   VITE_SUPABASE_URL=<your_project_url>
   VITE_SUPABASE_ANON_KEY=<your_anon_key>
   ```

### Step 2: Run Local Testing (1 min)

```powershell
# Navigate to project root
cd C:\Users\HomeLaptop\Downloads\navi-tax-35-main

# Run the startup script
.\START_ALL_SERVERS_SPLIT.ps1
```

**What happens:**
- Three PowerShell windows open
- ML API loads models (30-60 seconds)
- Backend server starts on port 3001
- Frontend dev server starts on port 5173
- Browser automatically opens http://localhost:5173

### Step 3: Wait & Verify (2 min)

1. **Check ML API window** - Should show "Application startup complete"
2. **Check Backend window** - Should show "Server running on port 3001"  
3. **Check Frontend window** - Should show Vite dev server ready
4. **Browser** - Should load the app at http://localhost:5173

---

## Testing the Full Flow (5 minutes)

Once all services are running:

```
1. Sign up / Log in
2. Upload a test document
3. Make a prediction
4. View SHAP explanations
5. Check browser console (F12) - should show no errors
```

**Success = No errors in browser console + features work** ✅

---

## Quick Diagnostics

**Services not starting?** Run this anytime:

```powershell
.\CHECK_LOCAL_HEALTH.ps1
```

This will tell you exactly what's running and what's not.

---

## Common Issues & Quick Fixes

| Issue | Fix |
|-------|-----|
| "Port already in use" | `.\STOP_SERVERS.ps1` then try again |
| "ML API loading forever" | Wait full 60 seconds, check window for errors |
| "Backend can't reach ML API" | Make sure ML API window shows it's done loading |
| "CORS errors in browser" | Hard refresh: Ctrl+Shift+R |
| "Can't connect to Supabase" | Double-check `.env` credentials (copy exactly) |
| "Blank page in browser" | Check F12 console for errors, check Network tab |

---

## When Everything Works Locally ✅

1. **Run all tests** from `LOCAL_TESTING_GUIDE.md` - Phase 2 & 3
2. **Record performance metrics** to compare with production
3. **Commit to GitHub:**
   ```powershell
   git add .
   git commit -m "Ready for production deployment"
   git push origin main
   ```
4. **Deploy to production** using `DEPLOYMENT_SPLIT_ARCHITECTURE.md`

---

## Architecture You're Testing

```
┌─────────────────────────────────────────────┐
│                 LOCALHOST                   │
├─────────────────────────────────────────────┤
│                                             │
│  ⚛️  Frontend (Port 5173)                   │
│  ↓                                          │
│  🚀 Backend (Port 3001)                    │
│  ↓                                          │
│  🤖 ML API (Port 8000)                     │
│  ↓                                          │
│  🗄️  Supabase (Cloud)                      │
│                                             │
└─────────────────────────────────────────────┘
```

Each layer:
- Frontend makes requests to Backend
- Backend orchestrates ML predictions and DB queries
- ML API handles model inference and SHAP explanations
- Supabase stores data

---

## Files You Need to Touch

**Required updates:**
- [ ] `docs/backend-example/.env` - Add Supabase credentials
- [ ] `web/.env` - Add Supabase credentials

**Just run:**
- [ ] `.\START_ALL_SERVERS_SPLIT.ps1`
- [ ] Test in browser
- [ ] If issues: `.\CHECK_LOCAL_HEALTH.ps1`

---

## Performance Expectations

| Component | Local | Production |
|-----------|-------|------------|
| ML API startup | 30-60s | 30-60s (first time) |
| Prediction | <5s | <5s (after warmup) |
| SHAP explanation | <10s | <10s |
| Page load | <2s | <3s (global CDN) |

---

## Detailed Testing

For a complete walkthrough of all features:
- See `LOCAL_TESTING_GUIDE.md`

For production deployment:
- See `DEPLOYMENT_SPLIT_ARCHITECTURE.md` or `DEPLOYMENT_QUICK_START.md`

---

## Your Deployment Timeline

```
✅ Step 1: Local Testing (You are here)
   ├─ Run START_ALL_SERVERS_SPLIT.ps1
   ├─ Test all features
   └─ Verify no errors

⏳ Step 2: Prepare GitHub
   ├─ Create GitHub repos (if needed)
   └─ Push code

⏳ Step 3: Deploy Backend to Render
   ├─ Create Render account
   ├─ Deploy via render.yaml
   └─ Configure environment variables

⏳ Step 4: Deploy Frontend to Vercel
   ├─ Create Vercel account
   ├─ Deploy via vercel.json
   └─ Update backend URL

⏳ Step 5: Production Testing
   ├─ Test on Render/Vercel
   ├─ Fix any environment issues
   └─ Enable GitHub Actions keep-alive
```

---

## You're All Set! 🎉

Everything is ready to go. Here's what to do:

**Right now:**
```powershell
# 1. Update Supabase credentials in:
#    - docs/backend-example/.env
#    - web/.env

# 2. Run local testing
.\START_ALL_SERVERS_SPLIT.ps1

# 3. Test features at http://localhost:5173
```

**When local testing passes:**
```powershell
# 4. Follow DEPLOYMENT_SPLIT_ARCHITECTURE.md to go live
```

---

## Need Help?

- 📖 **Testing Help:** See `LOCAL_TESTING_GUIDE.md`
- 🚀 **Deployment Help:** See `DEPLOYMENT_SPLIT_ARCHITECTURE.md`  
- 🩺 **Diagnostics:** Run `.\CHECK_LOCAL_HEALTH.ps1`
- 🐛 **Specific Issues:** Check "Common Issues" section above

---

Good luck! You've got a professional setup ready to deploy. 🚀