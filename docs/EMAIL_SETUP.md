# Secure Gmail SMTP Setup for OTP Authentication

This guide shows how to set up secure Gmail-based OTP email delivery using a backend API.

## Architecture Overview

```
Frontend → Backend API → Gmail SMTP → User's Email
```

This approach is much more secure than client-side email services.

## Step 1: Gmail App Password Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. Go to [Google Account Settings](https://myaccount.google.com/)
3. Navigate to **Security** → **2-Step Verification**
4. Scroll down to **App passwords**
5. Generate a new app password for "Mail"
6. **Save this password securely** - you'll need it for the backend

## Step 2: Backend API Setup (Node.js/Express)

Create a backend API to handle email sending securely:

```javascript
// backend/server.js
const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Gmail SMTP configuration
const transporter = nodemailer.createTransporter({
  service: 'gmail',
  auth: {
    user: process.env.GMAIL_USER, // your-email@gmail.com
    pass: process.env.GMAIL_APP_PASSWORD // app password from Step 1
  }
});

// OTP email endpoint
app.post('/api/send-otp', async (req, res) => {
  try {
    const { to, otpCode } = req.body;
    
    const mailOptions = {
      from: `"Tax Intelligence" <${process.env.GMAIL_USER}>`,
      to: to,
      subject: 'Your Tax Intelligence Verification Code',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <div style="background: linear-gradient(135deg, #3b82f6, #1e40af); padding: 20px; text-align: center;">
            <h1 style="color: white; margin: 0;">Tax Intelligence</h1>
          </div>
          <div style="padding: 30px; background: #f8fafc;">
            <h2 style="color: #1e293b;">Your Verification Code</h2>
            <p>Your verification code is:</p>
            <div style="background: white; border: 2px solid #3b82f6; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
              <span style="font-size: 32px; font-weight: bold; color: #3b82f6; letter-spacing: 4px;">${otpCode}</span>
            </div>
            <p style="color: #475569; font-size: 14px;">
              This code will expire in <strong>5 minutes</strong>.<br>
              If you didn't request this, please ignore this email.
            </p>
          </div>
        </div>
      `
    };
    
    await transporter.sendMail(mailOptions);
    res.json({ success: true });
    
  } catch (error) {
    console.error('Email error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(3001, () => {
  console.log('Email API server running on port 3001');
});
```

## Step 3: Environment Variables

Create `.env` file in your backend:

```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
```

## Step 4: Install Dependencies

```bash
npm install express nodemailer cors dotenv
```

## Step 5: Update Frontend Configuration

Update the `callBackendEmailAPI` method in `src/lib/emailService.ts`:

```typescript
private async callBackendEmailAPI(emailData: any): Promise<{ success: boolean; error?: string }> {
  try {
    const response = await fetch('http://localhost:3001/api/send-otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        to: emailData.to,
        otpCode: emailData.html.match(/(\d{6})/)?.[1]
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result;
    
  } catch (error) {
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Backend API error'
    };
  }
}
```

## Step 6: Production Deployment

For production:

1. **Deploy backend** to services like:
   - Vercel (serverless functions)
   - Netlify Functions
   - AWS Lambda
   - Railway
   - Render

2. **Update frontend** API URL to your production backend

3. **Use environment variables** for all sensitive data

## Security Benefits

✅ **Gmail App Passwords** - More secure than regular passwords
✅ **Backend-only credentials** - Never exposed to frontend
✅ **Professional email delivery** - High deliverability rates
✅ **Rate limiting** - Can implement proper rate limiting
✅ **Audit logging** - Track all email sends
✅ **No third-party dependencies** - Direct Gmail integration

## Alternative: Serverless Functions

You can also deploy this as serverless functions on Vercel:

```javascript
// api/send-otp.js (Vercel)
const nodemailer = require('nodemailer');

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  // Same email logic as above
  // ...
}
```

This approach gives you enterprise-grade email delivery with Gmail's reliability and security.
