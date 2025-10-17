# 🚀 How to Start the Tax Intelligence Platform

## ✅ I Just Started the Servers For You!

Two PowerShell windows should have opened:
1. **Backend Server** (Blue header) - Port 3001
2. **Frontend Server** (Green header) - Port 5173

---

## 🌐 Access the Site

**Wait 10-15 seconds** for the frontend to fully start, then open your browser to:

### **http://localhost:8080**

---

## 🔍 Check Server Status

**Double-click:** `CHECK_STATUS.bat`

This will show you if both servers are running.

---

## 📋 What You Should See

### Backend Terminal (Port 3001):
```
========================================
   BACKEND SERVER (Port 3001)
========================================

🚀 Server running on http://localhost:3001
📧 Email service configured
📄 Document processing ready
```

### Frontend Terminal (Port 5173):
```
========================================
   FRONTEND SERVER (Port 5173)
========================================

VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:8080/
➜  Network: use --host to expose
```

### Browser (http://localhost:8080):
- Tax Intelligence Platform login page
- Clean interface with login/signup options
- No console errors (press F12 to check)

---

## 🛑 How to Stop the Servers

Simply **close both PowerShell windows** that opened.

---

## 🔄 How to Restart

### Option 1: Use the Startup Script
**Double-click:** `START_SITE.bat`

### Option 2: Manual Start

**Terminal 1 (Backend):**
```powershell
cd C:\Users\HomeLaptop\Downloads\navi-tax-35-main\navi-tax-35-main\backend-example
node server.js
```

**Terminal 2 (Frontend):**
```powershell
cd C:\Users\HomeLaptop\Downloads\navi-tax-35-main\navi-tax-35-main
npm run dev
```

---

## ⚠️ Troubleshooting

### Problem: "Site doesn't load"

1. **Check if servers are running:**
   - Double-click `CHECK_STATUS.bat`
   - Both should show ✓

2. **If backend not running:**
   ```powershell
   cd backend-example
   node server.js
   ```

3. **If frontend not running:**
   ```powershell
   npm run dev
   ```

4. **If ports are in use:**
   - Close the PowerShell windows
   - Wait 5 seconds
   - Run `START_SITE.bat` again

### Problem: "Cannot connect to backend"

1. Verify backend is running on port 3001
2. Check browser console (F12) for errors
3. Try accessing: http://localhost:3001/api/health

### Problem: "White screen"

1. Check frontend terminal for errors
2. Clear browser cache (Ctrl+Shift+Delete)
3. Try incognito mode
4. Check browser console (F12)

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `START_SITE.bat` | Start both servers automatically |
| `CHECK_STATUS.bat` | Check if servers are running |
| `TROUBLESHOOTING.md` | Detailed troubleshooting guide |
| `backend-example/server.js` | Backend server code |
| `package.json` | Frontend dependencies |

---

## 🎯 Next Steps

Once the site loads:

1. **Create an account** or **login**
2. **Upload documents** using the Document Processor
3. **View results** in the dashboard
4. **Test the fixes** using `test_processing.py`

---

## 📚 Related Documentation

- `TROUBLESHOOTING.md` - Detailed troubleshooting
- `README_FIXES.md` - Document processing fixes
- `QUICK_START.md` - Email setup
- `RUN_TESTS.md` - Testing guide

---

## 🆘 Still Having Issues?

See `TROUBLESHOOTING.md` for detailed solutions to common problems.

---

**Last Updated:** January 2025