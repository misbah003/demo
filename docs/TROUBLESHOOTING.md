# 🔧 Troubleshooting Guide - Site Not Working

## Quick Diagnosis

### Problem: "Site doesn't seem to work"

This usually means one or both servers aren't running. The application needs **TWO** servers:

1. **Backend Server** (Node.js) - Port 3001
2. **Frontend Server** (Vite/React) - Port 5173

---

## ✅ Quick Fix - Use the Startup Script

**Double-click:** `START_SITE.bat`

This will:
- ✓ Check if Node.js is installed
- ✓ Install dependencies if needed
- ✓ Start both servers automatically
- ✓ Open two terminal windows (keep them open!)

Then open your browser to: **http://localhost:8080**

---

## 🔍 Manual Troubleshooting

### Step 1: Check if Node.js is Installed

Open PowerShell and run:
```powershell
node --version
```

**Expected:** `v16.0.0` or higher

**If not installed:**
- Download from: https://nodejs.org/
- Install the LTS version
- Restart your terminal

---

### Step 2: Install Dependencies

#### Backend Dependencies:
```powershell
cd backend-example
npm install
cd ..
```

#### Frontend Dependencies:
```powershell
npm install
```

---

### Step 3: Start Backend Server

**Terminal 1:**
```powershell
cd backend-example
node server.js
```

**Expected output:**
```
🚀 Server running on http://localhost:3001
📧 Email service configured
📄 Document processing ready
```

**If you see errors:**
- Check if port 3001 is already in use
- Make sure `.env` file exists in `backend-example/`
- Check for missing dependencies

---

### Step 4: Start Frontend Server

**Terminal 2 (new window):**
```powershell
npm run dev
```

**Expected output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**If you see errors:**
- Check if port 5173 is already in use
- Make sure dependencies are installed
- Check for TypeScript errors

---

### Step 5: Open Browser

Navigate to: **http://localhost:8080**

You should see the Tax Intelligence Platform login page.

---

## 🚨 Common Issues

### Issue 1: "Port 3001 already in use"

**Solution:**
```powershell
# Find process using port 3001
netstat -ano | findstr :3001

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

---

### Issue 2: "Port 5173 already in use"

**Solution:**
```powershell
# Find process using port 5173
netstat -ano | findstr :5173

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

---

### Issue 3: "Cannot find module 'express'"

**Solution:**
```powershell
cd backend-example
npm install
```

---

### Issue 4: "Cannot find module 'react'"

**Solution:**
```powershell
npm install
```

---

### Issue 5: Backend starts but frontend shows "Network Error"

**Cause:** Backend not running or wrong URL

**Solution:**
1. Check backend is running on port 3001
2. Check browser console for errors
3. Verify API URL in frontend code

---

### Issue 6: "ENOENT: no such file or directory"

**Cause:** Running commands from wrong directory

**Solution:**
Make sure you're in the project root:
```powershell
cd C:\Users\HomeLaptop\Downloads\navi-tax-35-main\navi-tax-35-main
```

---

### Issue 7: White screen or blank page

**Possible causes:**
1. Frontend server not started
2. JavaScript errors in browser console
3. Build issues

**Solution:**
1. Check browser console (F12) for errors
2. Restart frontend server
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try incognito mode

---

### Issue 8: "Email verification not working"

**Cause:** Backend email not configured

**Solution:**
See `QUICK_START.md` for email setup instructions.

---

## 📊 Verify Everything is Working

### Check Backend:
```powershell
curl http://localhost:3001/api/health
```

**Expected:** `{"status":"ok"}`

### Check Frontend:
Open browser to: http://localhost:8080

**Expected:** Login page loads

---

## 🔄 Complete Reset

If nothing works, try a complete reset:

```powershell
# Stop all servers (close terminal windows)

# Delete dependencies
Remove-Item -Recurse -Force node_modules
Remove-Item -Recurse -Force backend-example\node_modules

# Reinstall everything
npm install
cd backend-example
npm install
cd ..

# Start servers
START_SITE.bat
```

---

## 📞 Still Having Issues?

### Check these files:
1. `backend-example\.env` - Backend configuration
2. `package.json` - Dependencies list
3. `vite.config.ts` - Frontend configuration

### Collect this information:
- Node.js version: `node --version`
- npm version: `npm --version`
- Operating System: Windows 11
- Error messages from terminal
- Browser console errors (F12)

---

## 🎯 Expected Behavior

When everything is working:

✅ **Backend Terminal:**
```
🚀 Server running on http://localhost:3001
📧 Email service configured
📄 Document processing ready
```

✅ **Frontend Terminal:**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:8080/
```

✅ **Browser:**
- Login page loads at http://localhost:8080
- No console errors
- Can interact with the page

---

## 📚 Related Documentation

- `QUICK_START.md` - Email setup
- `README_FIXES.md` - Document processing fixes
- `RUN_TESTS.md` - Testing guide
- `START_HERE.md` - General setup

---

**Last Updated:** January 2025