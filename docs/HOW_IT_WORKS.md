# 🔄 How Email Verification Works

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     EMAIL VERIFICATION FLOW                      │
└─────────────────────────────────────────────────────────────────┘

Step 1: User Requests Code
┌──────────┐
│  User    │  Enters email: john@example.com
│  Browser │  Clicks "Send Verification Code"
└────┬─────┘
     │
     ▼
┌──────────────────────────────────────────────────────────────┐
│  Frontend (React)                                             │
│  - Generates random 6-digit code: 123456                     │
│  - Stores code in localStorage with timestamp                │
│  - Calls emailService.sendOTP(email, code)                   │
└────┬─────────────────────────────────────────────────────────┘
     │
     │ HTTP POST Request
     │ URL: http://localhost:3001/api/send-otp
     │ Body: { to: "john@example.com", otpCode: "123456" }
     │
     ▼
┌──────────────────────────────────────────────────────────────┐
│  Backend (Node.js + Express)                                  │
│  - Receives request                                           │
│  - Validates email format                                     │
│  - Validates OTP format (6 digits)                           │
│  - Checks rate limiting                                       │
│  - Creates email with HTML template                          │
└────┬─────────────────────────────────────────────────────────┘
     │
     │ SMTP Connection
     │ Uses Gmail App Password
     │
     ▼
┌──────────────────────────────────────────────────────────────┐
│  Gmail SMTP Server                                            │
│  - Authenticates with App Password                           │
│  - Sends email to john@example.com                           │
│  - Returns success/failure                                    │
└────┬─────────────────────────────────────────────────────────┘
     │
     ▼
┌──────────┐
│  User's  │  Receives email with code: 123456
│  Inbox   │  Email expires in 5 minutes
└────┬─────┘
     │
     ▼
Step 2: User Verifies Code
┌──────────┐
│  User    │  Enters code: 123456
│  Browser │  Clicks "Verify Code"
└────┬─────┘
     │
     ▼
┌──────────────────────────────────────────────────────────────┐
│  Frontend (React)                                             │
│  - Retrieves stored code from localStorage                   │
│  - Checks if code is expired (> 5 minutes)                   │
│  - Compares entered code with stored code                    │
│  - If match: Creates Supabase session                        │
│  - If no match: Shows error                                  │
└────┬─────────────────────────────────────────────────────────┘
     │
     ▼
┌──────────┐
│  User    │  ✅ Logged in successfully!
│  Browser │  Redirected to dashboard
└──────────┘
```

---

## Component Breakdown

### 1. Frontend (`src/lib/emailService.ts`)
**Role**: Generate OTP and request email sending

```typescript
// Generates 6-digit code
const otpCode = Math.floor(100000 + Math.random() * 900000).toString();

// Stores in localStorage
localStorage.setItem(`otp_${email}`, otpCode);
localStorage.setItem(`otp_${email}_timestamp`, Date.now().toString());

// Calls backend API
await fetch('http://localhost:3001/api/send-otp', {
  method: 'POST',
  body: JSON.stringify({ to: email, otpCode: otpCode })
});
```

### 2. Backend (`backend-example/server.js`)
**Role**: Send email via Gmail SMTP

```javascript
// Configure Gmail SMTP
const transporter = nodemailer.createTransporter({
  service: 'gmail',
  auth: {
    user: process.env.GMAIL_USER,        // your-email@gmail.com
    pass: process.env.GMAIL_APP_PASSWORD // 16-char app password
  }
});

// Send email
await transporter.sendMail({
  from: 'Tax Intelligence <your-email@gmail.com>',
  to: userEmail,
  subject: 'Your Verification Code',
  html: emailTemplate
});
```

### 3. Gmail SMTP
**Role**: Deliver email to user's inbox

- Uses secure SMTP connection
- Authenticates with App Password
- Delivers email within seconds
- High deliverability rate

---

## Security Features

### 🔒 Code Storage
- Stored in browser's localStorage (client-side only)
- Includes timestamp for expiration check
- Automatically deleted after verification

### ⏱️ Expiration
- Codes expire after 5 minutes
- Checked on verification attempt
- Old codes are rejected

### 🚦 Rate Limiting
- Max 3 requests per minute per IP
- Prevents spam and abuse
- Implemented in backend

### 🔐 Credentials
- Gmail App Password (not regular password)
- Stored only in backend `.env` file
- Never exposed to frontend
- Never sent to client

### ✅ Validation
- Email format validation
- OTP format validation (6 digits)
- Input sanitization
- Error handling

---

## Data Flow

### Request Phase
```
User Input → Frontend → Backend → Gmail → User's Inbox
   ↓           ↓          ↓         ↓          ↓
  Email    Generate   Validate   Send     Receive
           6-digit    & Send     SMTP     Email
            Code      Email
```

### Verification Phase
```
User Input → Frontend → localStorage → Supabase → Success
   ↓           ↓            ↓             ↓          ↓
  Enter    Compare      Stored        Create     Login
  Code     Codes        Code          Session
```

---

## Why This Architecture?

### ✅ Advantages

1. **Security**: Credentials never exposed to frontend
2. **Reliability**: Gmail's SMTP is highly reliable
3. **Professional**: Branded emails with HTML templates
4. **Control**: Full control over email content and timing
5. **Scalability**: Easy to add features (logging, analytics)
6. **Cost**: Free for reasonable usage

### ❌ Alternative Approaches (Not Used)

1. **Client-side email services**: Less secure, credentials exposed
2. **Supabase Auth**: Requires email configuration in Supabase
3. **Third-party services**: Additional cost, external dependency

---

## Configuration Requirements

### Frontend (`.env`)
```env
VITE_BACKEND_URL=http://localhost:3001
```

### Backend (`backend-example/.env`)
```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-password
PORT=3001
```

---

## Email Template

The email sent to users includes:

- 📧 **Professional header** with Tax Intelligence branding
- 🔢 **Large, clear 6-digit code** in a highlighted box
- ⏱️ **Expiration notice** (5 minutes)
- 🔒 **Security message** (ignore if not requested)
- 📱 **Responsive design** (works on mobile)
- 🎨 **Branded colors** (blue gradient)

---

## Error Handling

### Frontend Errors
- Network errors → "Failed to connect to email service"
- Backend errors → Shows backend error message
- Timeout → "Request timed out"

### Backend Errors
- Invalid credentials → "Email authentication failed"
- Invalid email → "Invalid email format"
- Rate limit → "Too many requests"
- SMTP errors → "Failed to send email"

### Verification Errors
- Wrong code → "Invalid OTP code"
- Expired code → "OTP code has expired"
- No code found → "No OTP code found"

---

## Testing the Flow

### 1. Start Backend
```bash
cd backend-example
node server.js
```

### 2. Check Backend Logs
```
🚀 Gmail OTP API server running on port 3001
📧 Gmail user: your-email@gmail.com
🔐 Gmail app password: Configured
```

### 3. Test Email Sending
- Enter email in frontend
- Click "Send Verification Code"
- Check backend logs for: `✅ OTP email sent successfully`

### 4. Check Email
- Open your email inbox
- Look for "Tax Intelligence" email
- Should arrive within seconds

### 5. Verify Code
- Enter the 6-digit code
- Click "Verify Code"
- Should log in successfully

---

## Monitoring

### Backend Logs Show:
- ✅ Successful email sends
- ❌ Failed attempts
- 🚦 Rate limit hits
- 📧 Email addresses (for debugging)
- 🔢 OTP codes (for debugging)

### Frontend Console Shows:
- 📧 Email sending attempts
- ✅ Successful API calls
- ❌ Error messages
- 🔢 Generated OTP codes

---

## Summary

**Simple Flow**:
1. User enters email
2. Frontend generates code
3. Backend sends email via Gmail
4. User receives email
5. User enters code
6. Frontend verifies code
7. User logged in

**Time**: ~5-10 seconds from request to inbox  
**Security**: High (App Password, expiration, rate limiting)  
**Reliability**: High (Gmail SMTP)  
**Cost**: Free  

---

**Next**: See `QUICK_START.md` to set it up!