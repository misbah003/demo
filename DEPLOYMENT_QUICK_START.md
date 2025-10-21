# ⚡ Quick Start Deployment in 5 Steps

**Time to deploy:** ~30 minutes (+ 10-15 min for services to start)

---

## 1️⃣ Setup Supabase (5 min)

```
Go to: https://app.supabase.com/sign-up
1. Create project
2. Save these credentials:
   - SUPABASE_URL
   - SUPABASE_ANON_KEY
   - SUPABASE_SERVICE_KEY
```

---

## 2️⃣ Deploy Frontend to Vercel (5 min)

```
Go to: https://vercel.com/new
1. Import your GitHub repo
2. Select "web" as root directory
3. Click Deploy

Your frontend is now live at: https://[project].vercel.app ✅
```

---

## 3️⃣ Deploy ML API to Render (10 min + 10 min startup)

```
Go to: https://render.com/new
1. Create Web Service
2. Fill in:
   - Name: navi-tax-ml-api
   - Runtime: Python 3.11
   - Build: pip install --no-cache-dir -r requirements.txt
   - Start: gunicorn --workers 2 --bind 0.0.0.0:$PORT --timeout 120 'ml.ml_api_service_optimized:app'
   - Plan: Free

3. Add Environment Variables:
   - FLASK_ENV = production
   - SUPABASE_URL = [your-url]
   - SUPABASE_SERVICE_KEY = [your-key]

4. Deploy - wait 10-15 min for first startup ⏳

ML API is now live at: https://navi-tax-ml-api.onrender.com ✅
```

---

## 4️⃣ Deploy Backend to Render (5 min + 3 min startup)

```
Go to: https://render.com/new
1. Create Web Service
2. Fill in:
   - Name: navi-tax-backend
   - Runtime: Node 20
   - Build: cd docs/backend-example && npm install
   - Start: cd docs/backend-example && npm start
   - Plan: Free

3. Add Environment Variables:
   - NODE_ENV = production
   - SUPABASE_URL = [your-url]
   - SUPABASE_SERVICE_KEY = [your-key]
   - SUPABASE_ANON_KEY = [your-anon-key]
   - ML_API_URL = https://navi-tax-ml-api.onrender.com

4. Deploy - wait 3-5 min

Backend is now live at: https://navi-tax-backend.onrender.com ✅
```

---

## 5️⃣ Link Everything Together (5 min)

```
Back in Vercel Dashboard:
1. Go to Settings → Environment Variables
2. Update:
   - VITE_BACKEND_URL = https://navi-tax-backend.onrender.com
   - VITE_ML_API_URL = https://navi-tax-ml-api.onrender.com

3. Go to Deployments → Click latest → "Redeploy"
4. Wait ~3 min for redeploy

✅ DONE! All services are now connected!
```

---

## 🧪 Quick Tests

After all services are deployed, test with these commands:

```bash
# Test 1: Frontend loads
curl https://[project].vercel.app

# Test 2: ML API is healthy
curl https://navi-tax-ml-api.onrender.com/health

# Test 3: Backend is healthy
curl https://navi-tax-backend.onrender.com/health

# Test 4: Make a prediction
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

---

## 📚 Complete Guides

- **Full Guide:** See `DEPLOYMENT_GUIDE_FINAL.md`
- **Checklist:** See `DEPLOYMENT_CHECKLIST.md`
- **Environment Setup:** See `.env.example`

---

## ⚠️ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "503 Service Unavailable" | Service is starting. Wait 2 min, then retry. |
| "Cannot find module" | Check start command has correct path. |
| "Connection refused" | Verify services are running in Render dashboard. |
| "CORS error" | Check `VITE_BACKEND_URL` is set correctly in Vercel. |
| "Models not found" | Ensure `optimized_models_25000_samples/` is in GitHub root. |

---

## 💡 Pro Tips

1. **Keep services warm:** Use Uptime Robot (free) to ping services every 5 min
   - Prevents cold starts
   - Free tier: https://uptimerobot.com

2. **Monitor logs:**
   - Render: Dashboard → Your service → Logs
   - Vercel: Dashboard → Deployments → Build logs

3. **Scale up later:**
   - Render: Upgrade from free to paid tier when needed
   - Vercel: Auto-scales on paid plan

---

## 📞 Need Help?

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Supabase Docs:** https://supabase.com/docs

---

**Status:** 🟢 Ready to Deploy

Next: Follow steps 1-5 above!