# Email Verification Setup Instructions

## 🎯 Quick Start Guide

Your email verification is currently not working because the backend email service is not configured. Follow these steps to fix it:

---

## Step 1: Generate Gmail App Password

A Gmail App Password is a special 16-character password that allows applications to access your Gmail account securely (without using your regular password).

### Instructions:

1. **Enable 2-Factor Authentication** (if not already enabled):
   - Go to https://myaccount.google.com/security
   - Find "2-Step Verification" and turn it ON
   - Follow the prompts to set it up

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - You might need to sign in again
   - Select "Mail" as the app
   - Select "Windows Computer" (or any device)
   - Click "Generate"
   - **IMPORTANT**: Copy the 16-character password shown (it looks like: `abcd efgh ijkl mnop`)
   - Save it somewhere safe - you won't be able to see it again!

---

## Step 2: Configure Backend

1. **Open the file**: `backend-example\.env`

2. **Replace the placeholder values**:
   ```env
   GMAIL_USER=your-actual-email@gmail.com
   GMAIL_APP_PASSWORD=your-16-character-app-password
   PORT=3001
   ```

   **Example**:
   ```env
   GMAIL_USER=john.doe@gmail.com
   GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
   PORT=3001
   ```

3. **Save the file**

---

## Step 3: Install Backend Dependencies

Open a terminal in the `backend-example` folder and run:

```bash
cd backend-example
npm install
```

This will install:
- express (web server)
- nodemailer (email sending)
- cors (cross-origin requests)
- dotenv (environment variables)

---

## Step 4: Start the Backend Server

In the same terminal (in `backend-example` folder), run:

```bash
node server.js
```

You should see:
```
🚀 Gmail OTP API server running on port 3001
📧 Gmail user: your-email@gmail.com
🔐 Gmail app password: Configured
```

**Keep this terminal window open** - the backend needs to run while you use the app.

---

## Step 5: Test the Email Verification

1. Make sure the backend is running (Step 4)
2. Start your frontend application
3. Go to the login page
4. Enter your email address
5. Click "Send Verification Code"
6. **Check your email inbox** - you should receive a 6-digit code within seconds!

---

## 🔧 Troubleshooting

### "Failed to send email" error
- Check that the backend server is running
- Verify your Gmail credentials in `.env` are correct
- Make sure you're using an App Password, not your regular Gmail password

### "Backend API error" or "Connection refused"
- The backend server is not running - start it with `node server.js`
- Check that the backend is running on port 3001

### Email not arriving
- Check your spam/junk folder
- Verify the Gmail account has 2FA enabled
- Try generating a new App Password
- Check the backend terminal for error messages

### "Email authentication failed"
- Your App Password is incorrect
- Generate a new App Password and update `.env`
- Make sure there are no extra spaces in the password

---

## 🚀 Production Deployment

For production, you should deploy the backend to a cloud service:

- **Vercel** (serverless functions)
- **Railway** (easy deployment)
- **Render** (free tier available)
- **AWS Lambda** (serverless)
- **Heroku** (simple deployment)

Then update your frontend `.env` file:
```env
VITE_BACKEND_URL=https://your-backend-url.com
```

---

## 📝 Notes

- The App Password is different from your Gmail password
- Never commit the `.env` file to Git (it's in `.gitignore`)
- The OTP codes expire after 5 minutes for security
- Rate limiting is enabled (max 3 requests per minute per IP)

---

## ✅ Success!

Once configured, your users will receive professional-looking verification emails with 6-digit codes that expire in 5 minutes.

Need help? Check the backend terminal for detailed error messages.