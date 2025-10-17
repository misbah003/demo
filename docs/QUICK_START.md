# ⚡ QUICK START - Fix Email Verification

## 🎯 The Problem
Clicking "Send Verification Code" doesn't send emails because the backend is not configured.

---

## ✅ The Fix (3 Steps - 10 Minutes)

### 1️⃣ Get Gmail App Password
- Go to: https://myaccount.google.com/apppasswords
- Generate a password for "Mail"
- Copy the 16-character code (looks like: `abcd efgh ijkl mnop`)

### 2️⃣ Configure Backend
- Open: `backend-example\.env`
- Replace:
  ```
  GMAIL_USER=your-email@gmail.com
  GMAIL_APP_PASSWORD=your-16-character-password
  ```
- Save the file

### 3️⃣ Start Backend
- Double-click: `start-backend.bat`
- Keep the window open

---

## 🎉 Done!
Now try sending a verification code - you should receive an email!

---

## 📖 Need More Help?
See `FIX_EMAIL_VERIFICATION.md` for detailed instructions.