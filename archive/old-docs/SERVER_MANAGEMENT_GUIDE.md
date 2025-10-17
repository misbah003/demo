# 🚀 Navi Tax Server Management Guide

## 📋 Quick Start

### ✅ **Option 1: Batch Script (Recommended for Windows)**
Double-click: **`START_BOTH_SERVERS.bat`**

### ✅ **Option 2: PowerShell Script**
Right-click **`START_SERVERS.ps1`** → Run with PowerShell

---

## 📂 Available Scripts

| Script | Purpose | How to Use |
|--------|---------|------------|
| **START_BOTH_SERVERS.bat** | Start both servers (Batch) | Double-click |
| **START_SERVERS.ps1** | Start both servers (PowerShell) | Right-click → Run with PowerShell |
| **STOP_SERVERS.bat** | Stop all servers (Batch) | Double-click |
| **STOP_SERVERS.ps1** | Stop all servers (PowerShell) | Right-click → Run with PowerShell |
| **CHECK_SERVERS.bat** | Check server status | Double-click |
| **START_BACKEND.bat** | Start only backend | Double-click |

---

## 🎯 What Each Script Does

### **START_BOTH_SERVERS.bat** / **START_SERVERS.ps1**

**Automated startup process:**

1. ✅ Checks if `.env` file exists in backend
2. ✅ Installs dependencies if missing (npm install)
3. ✅ Checks if ports 3001 and 5173 are available
4. ✅ Kills existing processes if ports are busy (with confirmation)
5. ✅ Starts backend server on port 3001
6. ✅ Starts frontend server on port 5173
7. ✅ Opens browser automatically to http://localhost:5173

**Result:**
- Two terminal windows open (Backend + Frontend)
- Browser opens to the application
- Both servers running and ready

---

### **STOP_SERVERS.bat** / **STOP_SERVERS.ps1**

**Graceful shutdown:**

1. ✅ Finds processes on port 3001 (Backend)
2. ✅ Finds processes on port 5173 (Frontend)
3. ✅ Terminates both processes
4. ✅ Confirms shutdown

**When to use:**
- When you're done working
- Before restarting servers
- To free up ports

---

### **CHECK_SERVERS.bat**

**Status monitoring:**

1. ✅ Checks if backend is running (port 3001)
2. ✅ Checks if frontend is running (port 5173)
3. ✅ Shows process IDs
4. ✅ Provides troubleshooting advice

**Output example:**
```
========================================
  NAVI TAX SERVER STATUS
========================================

[BACKEND SERVER - Port 3001]
Status: RUNNING
URL: http://localhost:3001
Process ID: 12345

========================================

[FRONTEND SERVER - Port 5173]
Status: RUNNING
URL: http://localhost:5173
Process ID: 67890

========================================

[OK] Both servers are running!

Access the application at:
http://localhost:5173
```

---

## 🔧 Troubleshooting

### ❌ **Problem: "Port 3001 is already in use"**

**Solution 1:** Let the script kill it
- The startup script will ask: "Kill existing process and restart? (Y/N)"
- Type `Y` and press Enter

**Solution 2:** Manual stop
```batch
# Run this:
STOP_SERVERS.bat

# Then start again:
START_BOTH_SERVERS.bat
```

**Solution 3:** Find and kill manually
```powershell
# Find process on port 3001
netstat -ano | findstr :3001

# Kill it (replace PID with actual process ID)
taskkill /F /PID <PID>
```

---

### ❌ **Problem: "Backend .env file not found"**

**Solution:**
1. Navigate to: `c:\Users\HomeLaptop\Downloads\navi-tax-35-main\docs\backend-example\`
2. Create file named `.env`
3. Add these lines:
```env
SUPABASE_URL=https://ikqcakganqabiscsibym.supabase.co
SUPABASE_SERVICE_KEY=your_service_key_here
PORT=3001
```

---

### ❌ **Problem: "npm install failed"**

**Solution:**
```powershell
# Clear npm cache
npm cache clean --force

# Delete node_modules
Remove-Item -Recurse -Force node_modules

# Reinstall
npm install
```

---

### ❌ **Problem: Frontend shows blank page**

**Checklist:**
1. ✅ Is backend running? → Run `CHECK_SERVERS.bat`
2. ✅ Is `.env` configured in `web` folder?
3. ✅ Clear browser cache (Ctrl + Shift + Delete)
4. ✅ Check browser console (F12) for errors

---

### ❌ **Problem: "Cannot connect to Supabase"**

**Solution:**
1. Check `docs\backend-example\.env` has correct Supabase credentials
2. Check `web\.env` has correct Supabase credentials
3. Verify Supabase project is active at https://supabase.com/dashboard
4. Test connection: Open http://localhost:3001 in browser

---

## 🎓 Understanding the Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR BROWSER                         │
│              http://localhost:5173                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP Requests
                     │
┌────────────────────▼────────────────────────────────────┐
│              FRONTEND SERVER (Vite)                     │
│                  Port: 5173                             │
│  Location: web/                                         │
│  - React + TypeScript                                   │
│  - UI Components                                        │
│  - Supabase Client                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ API Calls
                     │
┌────────────────────▼────────────────────────────────────┐
│              BACKEND SERVER (Node.js)                   │
│                  Port: 3001                             │
│  Location: docs/backend-example/                        │
│  - Document Processing (OCR + NLP)                      │
│  - Entity Extraction                                    │
│  - File Upload Handling                                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Database Queries
                     │
┌────────────────────▼────────────────────────────────────┐
│                  SUPABASE                               │
│  - PostgreSQL Database                                  │
│  - Edge Functions                                       │
│  - Authentication                                       │
│  - Storage                                              │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Server Logs

### **Backend Logs**
Located in the "Backend Server" terminal window

**What to look for:**
```
✅ Server running on port 3001
✅ Connected to Supabase
✅ Document processed successfully
❌ Error: Cannot connect to Supabase
❌ Error: Port 3001 already in use
```

### **Frontend Logs**
Located in the "Frontend Server" terminal window

**What to look for:**
```
✅ VITE v5.x.x ready in XXX ms
✅ Local: http://localhost:5173/
✅ Network: use --host to expose
❌ Error: Failed to fetch
❌ Error: EADDRINUSE (port already in use)
```

---

## 🔄 Development Workflow

### **Starting Your Day**
```batch
1. Run: START_BOTH_SERVERS.bat
2. Wait for browser to open
3. Start coding!
```

### **During Development**
- Backend auto-restarts: ❌ No (manual restart required)
- Frontend hot-reload: ✅ Yes (changes reflect automatically)

**If you modify backend code:**
```batch
1. Run: STOP_SERVERS.bat
2. Run: START_BOTH_SERVERS.bat
```

### **Ending Your Day**
```batch
1. Run: STOP_SERVERS.bat
2. Or just close both terminal windows
```

---

## 🚨 Emergency Commands

### **Kill Everything Node.js**
```powershell
# Nuclear option - kills ALL Node.js processes
taskkill /F /IM node.exe
```

### **Free Port 3001**
```powershell
# Find what's using port 3001
netstat -ano | findstr :3001

# Kill specific process (replace PID)
taskkill /F /PID <PID>
```

### **Free Port 5173**
```powershell
# Find what's using port 5173
netstat -ano | findstr :5173

# Kill specific process (replace PID)
taskkill /F /PID <PID>
```

---

## ✅ Success Checklist

After running `START_BOTH_SERVERS.bat`, verify:

- [ ] Backend terminal window is open and shows "Server running on port 3001"
- [ ] Frontend terminal window is open and shows "Local: http://localhost:5173/"
- [ ] Browser opened automatically to http://localhost:5173
- [ ] Application loads without errors
- [ ] Can navigate between pages (Dashboard, Documents, etc.)
- [ ] Can upload documents (tests backend connection)

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start everything | `START_BOTH_SERVERS.bat` |
| Stop everything | `STOP_SERVERS.bat` |
| Check status | `CHECK_SERVERS.bat` |
| Backend only | `START_BACKEND.bat` |
| Frontend only | `cd web && npm run dev` |
| View backend | http://localhost:3001 |
| View frontend | http://localhost:5173 |

---

## 🎯 Next Steps

After servers are running:

1. **Test Excel Processing Fix**
   - Delete old documents: Run `DELETE_OLD_DOCUMENTS.sql` in Supabase
   - Re-upload Excel files
   - Verify "Compliant" or "Basic Information Present" status
   - Check VAT Collection Forecast shows data

2. **Read Documentation**
   - `EXCEL_PROCESSING_FIX.md` - Technical details
   - `QUICK_EXCEL_FIX_GUIDE.md` - User guide

3. **Verify Everything Works**
   - Upload test documents
   - Check dashboard predictions
   - Test all features

---

## 💡 Pro Tips

1. **Keep terminal windows visible** - You can see errors in real-time
2. **Use CHECK_SERVERS.bat frequently** - Quick status check
3. **Bookmark http://localhost:5173** - Quick access
4. **Check browser console (F12)** - Frontend errors show here
5. **Check backend terminal** - Backend errors show here

---

## 🆘 Still Having Issues?

1. Run `CHECK_SERVERS.bat` and share the output
2. Check backend terminal for error messages
3. Check frontend terminal for error messages
4. Check browser console (F12) for errors
5. Verify `.env` files exist and have correct values

---

**Created:** 2025
**Last Updated:** After Excel Processing Fix
**Status:** ✅ Ready to Use