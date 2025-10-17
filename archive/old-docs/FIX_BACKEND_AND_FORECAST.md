# 🔧 Fix Backend Server & VAT Forecast

## 🔍 **Root Cause**

Your VAT Forecast is showing "Generic Forecast" because:
1. **Backend server is not running** - Documents can't be processed
2. **No documents in database** - The forecast has no data to analyze

The backend server (`http://localhost:3001`) processes uploaded documents and saves them to the `processed_documents` table. Without it running, document uploads fail silently.

---

## ✅ **Solution: Start the Backend Server**

### **Step 1: Navigate to Backend Folder**

```powershell
cd c:\Users\HomeLaptop\Downloads\navi-tax-35-main\docs\backend-example
```

### **Step 2: Install Dependencies (First Time Only)**

```powershell
npm install
```

### **Step 3: Configure Environment Variables**

Check if `.env` file exists:

```powershell
Get-Content .env
```

**If file doesn't exist**, create it:

```powershell
@"
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
PORT=3001
"@ | Out-File -FilePath .env -Encoding utf8
```

**Replace with your actual Supabase credentials:**
- Get them from: https://supabase.com/dashboard → Project Settings → API

### **Step 4: Start the Backend Server**

```powershell
node server.js
```

**You should see:**
```
Server running on port 3001
Connected to Supabase
```

**Keep this terminal window open!** The server must run while you use the app.

---

## 🧪 **Test the Fix**

### **1. Upload a Document**

1. Go to your app dashboard
2. Click "AI Document Processing"
3. Upload a VAT document (PDF, Excel, or image)
4. You should see "Documents Processed" success message

### **2. Check VAT Forecast**

1. Scroll to "VAT Refund Predictor" section
2. The forecast should now show:
   - ✅ "Personalized forecast based on your data"
   - ✅ Chart with predictions
   - ✅ "Documents Analyzed: 1" (or more)

### **3. Verify in Database**

Run this in Supabase SQL Editor:

```sql
-- Check your documents
SELECT 
  filename,
  type,
  processed_at
FROM processed_documents
WHERE user_id = auth.uid()
ORDER BY processed_at DESC;
```

---

## 🚀 **Quick Start Script**

I'll create a script to start everything automatically:

### **Option A: Start Backend Only**

```powershell
cd c:\Users\HomeLaptop\Downloads\navi-tax-35-main\docs\backend-example
node server.js
```

### **Option B: Start Everything (Backend + Frontend)**

Create a new PowerShell window and run:

```powershell
# Terminal 1: Start Backend
cd c:\Users\HomeLaptop\Downloads\navi-tax-35-main\docs\backend-example
node server.js

# Terminal 2: Start Frontend (in a new window)
cd c:\Users\HomeLaptop\Downloads\navi-tax-35-main\web
npm run dev
```

---

## 🔍 **Troubleshooting**

### **Error: "Cannot find module 'express'"**

Install dependencies:
```powershell
cd c:\Users\HomeLaptop\Downloads\navi-tax-35-main\docs\backend-example
npm install
```

### **Error: "SUPABASE_URL is not defined"**

Create/update `.env` file with your Supabase credentials.

### **Error: "Port 3001 is already in use"**

Another process is using port 3001. Either:
1. Stop the other process
2. Change port in `.env`: `PORT=3002`
3. Update frontend code to use new port

### **Documents still not showing in forecast**

1. Check backend terminal for errors
2. Open browser DevTools (F12) → Console tab
3. Look for errors when uploading documents
4. Verify backend is running on `http://localhost:3001`

---

## 📊 **Expected Results**

### **Before Fix:**
- ❌ "Generic Forecast - No VAT documents found"
- ❌ Document uploads fail silently
- ❌ Forecast shows random predictions

### **After Fix:**
- ✅ "Personalized forecast based on your data"
- ✅ Document uploads show success message
- ✅ Forecast uses your actual VAT data
- ✅ "Documents Analyzed: X" shows count

---

## 🎯 **Profile Update Issue**

For the profile not updating in the dashboard, this is a **browser cache** issue:

### **Fix:**
1. Press `Ctrl + Shift + R` (hard refresh)
2. Or press `F12` → Right-click refresh → "Empty Cache and Hard Reload"

---

## ✅ **Complete Checklist**

- [ ] Backend server is running on port 3001
- [ ] `.env` file configured with Supabase credentials
- [ ] Frontend is running on port 5173 (or your port)
- [ ] Upload a test document
- [ ] Verify document appears in "Documents" page
- [ ] Check VAT Forecast shows personalized data
- [ ] Hard refresh browser (Ctrl+Shift+R)
- [ ] Profile updates are visible

---

## 🆘 **Still Having Issues?**

Run this diagnostic query in Supabase SQL Editor:

```sql
-- Check if processed_documents table exists
SELECT 'Table exists: ' || 
  CASE WHEN EXISTS (
    SELECT FROM pg_tables 
    WHERE schemaname = 'public' 
    AND tablename = 'processed_documents'
  ) THEN 'YES' ELSE 'NO' END;

-- Check your documents
SELECT COUNT(*) as total_documents
FROM processed_documents
WHERE user_id = auth.uid();

-- Check VAT documents
SELECT COUNT(*) as vat_documents
FROM processed_documents
WHERE user_id = auth.uid()
  AND type ILIKE '%VAT%';
```

If table doesn't exist, you need to create it. Let me know and I'll provide the SQL script.

---

## 💡 **Pro Tip**

Create a startup script to launch everything at once. I can create this for you if needed!