# 📧 Gmail SMTP Production Setup Guide

## 🎯 Complete Guide to Enable Real Email Sending

This guide will help you configure Gmail SMTP to send real OTP emails to users during registration.

---

## ✅ Current Email Service Features

Your backend already has a **production-ready email service** with:

- ✅ **Professional HTML email templates** with CampusEats branding
- ✅ **Automatic retry** on failure (2 attempts)
- ✅ **Rate limiting** (3 emails per 5 minutes per address)
- ✅ **Error handling** with user-friendly messages
- ✅ **TLS encryption** for secure transmission
- ✅ **Plain text fallback** for email clients that don't support HTML
- ✅ **Welcome email** after successful registration

**The email service is fully functional - you just need to configure Gmail credentials!**

---

## 📋 Step 1: Generate Gmail App Password

### Why App Password?

Gmail doesn't allow using your regular password for third-party apps. You need a special **App Password**.

### Prerequisites

1. **Gmail account** (you already have: `ntufoodapp@gmail.com`)
2. **2-Step Verification enabled** (required for App Passwords)

### Generate App Password - Detailed Steps

#### A. Enable 2-Step Verification (If Not Already Enabled)

1. Go to: https://myaccount.google.com/security
2. Scroll to **"How you sign in to Google"**
3. Click **"2-Step Verification"**
4. Follow the setup wizard:
   - Verify your phone number
   - Enter verification code sent via SMS
   - Click **"Turn on"**

#### B. Create App Password

1. **Visit App Passwords page:**
   - Direct link: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App passwords

2. **Sign in** if prompted

3. **Generate new app password:**
   - **Select app:** Choose **"Mail"** from dropdown
   - **Select device:** Choose **"Other (Custom name)"**
   - **Enter name:** Type `CampusEats Backend` or `Render Production`
   - Click **"Generate"**

4. **Copy the 16-character password:**
   ```
   Example: abcd efgh ijkl mnop
   ```
   - Gmail shows it with spaces: `abcd efgh ijkl mnop`
   - **Remove all spaces** when entering: `abcdefghijklmnop`
   - **Save it securely** - you can't view it again!

5. **Click "Done"**

### 🔒 Security Notes

- **App Passwords are account-specific**, not email-specific
- **Never share** your app password
- **Each app should have its own** app password
- **Revoke unused** app passwords periodically
- If compromised, revoke it immediately at the App Passwords page

---

## 📋 Step 2: Configure Render Environment Variables

### Required Environment Variables

Go to **Render Dashboard** → Your Backend Service → **Environment** tab

Add/Update these variables:

```bash
# ========================================
# EMAIL CONFIGURATION FOR PRODUCTION
# ========================================

# CRITICAL: Disable testing mode to send real emails
EMAIL_TESTING_MODE=false

# Gmail SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=ntufoodapp@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # Replace with your 16-char app password (NO SPACES!)

# Email Branding (Optional - has defaults)
SMTP_FROM_NAME=CampusEats

# Application URL (for links in email)
APP_URL=https://your-frontend.vercel.app  # Replace with your actual frontend URL
```

### Exact Values to Use

| Variable | Value | Notes |
|----------|-------|-------|
| `EMAIL_TESTING_MODE` | `false` | **MUST be false** for real emails |
| `SMTP_HOST` | `smtp.gmail.com` | Gmail SMTP server |
| `SMTP_PORT` | `587` | TLS port (DO NOT use 465) |
| `SMTP_EMAIL` | `ntufoodapp@gmail.com` | Your Gmail address |
| `SMTP_PASSWORD` | `[16-char app password]` | From Step 1 (NO SPACES!) |
| `SMTP_FROM_NAME` | `CampusEats` | Display name in emails |
| `APP_URL` | `https://your-app.vercel.app` | Your frontend URL |

### ⚠️ Common Mistakes to Avoid

❌ **Using regular Gmail password** → Use App Password instead
❌ **Leaving spaces in app password** → Remove all spaces: `abcdefghijklmnop`
❌ **Using port 465** → Use port 587 (STARTTLS)
❌ **Keeping EMAIL_TESTING_MODE=true** → Set to `false` for production
❌ **Wrong email format** → Must be `your-email@gmail.com`

### How to Add Variables on Render

1. **Render Dashboard** → Select your backend service
2. Click **"Environment"** tab in left sidebar
3. For each variable:
   - Click **"Add Environment Variable"**
   - Enter **Name** (e.g., `EMAIL_TESTING_MODE`)
   - Enter **Value** (e.g., `false`)
   - Click **"Save"**
4. After adding all variables, click **"Save Changes"**
5. Render will automatically redeploy (takes 1-2 minutes)

---

## 📋 Step 3: Verify Configuration

### A. Check Render Logs

After redeployment, check logs for:

```
✅ Good Signs:
INFO - Email Service initialized - Testing Mode: False
INFO - SMTP configured: ntufoodapp@gmail.com
INFO - CampusEats API started in production mode

❌ Bad Signs:
ERROR - SMTP credentials not configured
WARNING - Email testing mode enabled
```

### B. Check Environment Variables

Render → Environment tab should show:

```
EMAIL_TESTING_MODE = false  ✅
SMTP_EMAIL = ntufoodapp@gmail.com  ✅
SMTP_PASSWORD = ****************  ✅ (hidden)
SMTP_HOST = smtp.gmail.com  ✅
SMTP_PORT = 587  ✅
```

---

## 🧪 Step 4: Test Email Sending

### Test 1: Local Testing (Before Deployment)

If testing locally first:

1. **Create backend/.env.local:**
   ```bash
   EMAIL_TESTING_MODE=false
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_EMAIL=ntufoodapp@gmail.com
   SMTP_PASSWORD=abcdefghijklmnop  # Your app password
   SMTP_FROM_NAME=CampusEats
   APP_URL=http://localhost:5173
   ```

2. **Start backend:**
   ```bash
   cd backend
   source venv/bin/activate  # Windows: venv\Scripts\activate
   python -m uvicorn app.main:app --reload
   ```

3. **Check startup logs:**
   ```
   INFO - Email Service initialized - Testing Mode: False
   ```

4. **Test registration:**
   - Open frontend: http://localhost:5173
   - Register with your real email
   - Check inbox for OTP email

### Test 2: Production Testing (On Render)

1. **Go to deployed frontend:** `https://your-app.vercel.app`

2. **Navigate to** `/register`

3. **Fill in registration form:**
   - **Email:** Use a **real email you can access** (Gmail, Yahoo, etc.)
   - Student ID: `U1234567A`
   - Phone: `+65 91234567`
   - Password: `TestPass123`
   - Name: `Test User`

4. **Click "Send Verification Code"**

5. **Expected behavior:**
   - Frontend shows: "Verification code sent to your email"
   - **NO OTP displayed on screen** (testing mode disabled)
   - Check your email inbox

6. **Check your inbox:**
   - Look for email from "CampusEats <ntufoodapp@gmail.com>"
   - Subject: "CampusEats - Your Verification Code"
   - Should arrive within 10-30 seconds
   - Check spam folder if not in inbox

7. **Verify email contains:**
   - ✅ Your name
   - ✅ 6-digit OTP code (large, centered)
   - ✅ "Expires in 10 minutes" warning
   - ✅ CampusEats branding
   - ✅ Professional formatting

8. **Complete registration:**
   - Copy OTP from email
   - Enter in frontend
   - Click "Verify & Create Account"
   - Should redirect to `/stalls`

---

## 🔍 Troubleshooting

### Issue 1: Email Not Arriving

**Check these in order:**

1. **Check spam/junk folder**
   - Gmail often flags new senders as spam
   - Mark as "Not Spam" if found

2. **Verify email address is correct**
   - Check for typos
   - Use a different email provider (Yahoo, Outlook)

3. **Check Render logs:**
   ```
   Look for:
   ✅ "OTP email sent successfully to ..."
   ❌ "Failed to send email..."
   ❌ "SMTP Authentication failed"
   ```

4. **Verify app password is correct:**
   - Render → Environment → `SMTP_PASSWORD`
   - Should be 16 characters, no spaces
   - Regenerate if unsure

5. **Test SMTP connection manually:**
   ```python
   # In backend directory
   python
   >>> import smtplib
   >>> server = smtplib.SMTP('smtp.gmail.com', 587)
   >>> server.starttls()
   >>> server.login('ntufoodapp@gmail.com', 'your-app-password')
   >>> # If no error, SMTP works!
   >>> server.quit()
   ```

### Issue 2: "SMTP Authentication Failed"

**Causes:**

1. **Wrong app password**
   - Regenerate app password
   - Copy carefully (no spaces)

2. **2-Step Verification not enabled**
   - Enable at: https://myaccount.google.com/security

3. **App Password revoked**
   - Check: https://myaccount.google.com/apppasswords
   - Regenerate if deleted

4. **Wrong email address**
   - Verify `SMTP_EMAIL` matches the Google account

**Fix:**
1. Go to https://myaccount.google.com/apppasswords
2. Revoke old app password
3. Generate new one
4. Update `SMTP_PASSWORD` on Render
5. Redeploy

### Issue 3: Email Goes to Spam

**Why this happens:**
- New Gmail sender without reputation
- No SPF/DKIM records (using personal Gmail)
- Email contains OTP codes (flagged by spam filters)

**Solutions:**

**Short-term (for development/testing):**
1. Mark first email as "Not Spam"
2. Add ntufoodapp@gmail.com to contacts
3. Create filter: Never send to spam

**Long-term (for production):**
1. **Use a professional email service:**
   - SendGrid (100 emails/day free)
   - AWS SES (62,000 emails/month free)
   - Mailgun (5,000 emails/month free)
   - Postmark (100 emails/month free)

2. **Get a custom domain:**
   - `noreply@campuseats.com` instead of Gmail
   - Configure SPF, DKIM, DMARC records
   - Higher deliverability

### Issue 4: Rate Limiting

**Symptoms:**
- Error: "Too many requests. Please wait X minutes"
- Multiple registration attempts fail

**Cause:**
- Built-in rate limit: **3 emails per 5 minutes per address**

**Fix:**
- Wait 5 minutes
- Use a different email address
- This is intentional to prevent spam

### Issue 5: "Failed to send verification email"

**Check backend logs for specific error:**

```bash
# On Render
Logs tab → Look for:

ERROR - SMTP Authentication failed
→ Fix: Check app password

ERROR - Connection timeout
→ Fix: Check SMTP_HOST and SMTP_PORT

ERROR - Unexpected error sending email
→ Fix: Check full error message in logs
```

---

## 📊 Gmail SMTP Limits & Best Practices

### Gmail Sending Limits

| Limit Type | Free Gmail | Google Workspace |
|------------|------------|------------------|
| **Emails per day** | 500 | 2,000 |
| **Recipients per email** | 500 | 2,000 |
| **Rate** | ~2 emails/second | ~5 emails/second |

**For CampusEats:**
- 1 OTP email per registration
- 500 registrations/day should be enough for testing/small scale
- For larger scale, consider SendGrid/AWS SES

### Best Practices

✅ **DO:**
- Use App Passwords (never regular password)
- Enable 2-Step Verification
- Monitor sending limits
- Handle email failures gracefully
- Log all email attempts
- Test with multiple email providers

❌ **DON'T:**
- Share app passwords
- Commit passwords to git
- Use port 465 (use 587 instead)
- Send too many emails rapidly
- Ignore spam reports

### Backend Email Features Already Implemented

Your email service already has these protections:

✅ **Rate Limiting**
- 3 emails per 5 minutes per address
- Prevents spam and abuse

✅ **Retry Logic**
- Automatically retries failed sends (max 2 attempts)
- 1-second delay between retries

✅ **Error Handling**
- Catches SMTP authentication errors
- Catches connection errors
- Returns user-friendly error messages

✅ **Security**
- TLS encryption (STARTTLS)
- Secure SSL context
- 30-second timeout prevents hanging

✅ **Professional Templates**
- Beautiful HTML design
- Plain text fallback
- Mobile-responsive
- CampusEats branding

---

## 🔄 Alternative Email Services

If Gmail doesn't work or you need higher limits:

### Option 1: SendGrid (Recommended for Production)

**Pros:**
- 100 emails/day free forever
- Better deliverability
- Email analytics
- Professional sender reputation

**Setup:**
1. Sign up: https://sendgrid.com
2. Verify sender email
3. Generate API key
4. Update environment variables:
   ```bash
   EMAIL_PROVIDER=sendgrid
   SENDGRID_API_KEY=SG.xxxxx
   SENDGRID_FROM_EMAIL=noreply@yourdomain.com
   ```
5. Modify email service to use SendGrid API

### Option 2: AWS SES

**Pros:**
- 62,000 emails/month free (first 12 months)
- $0.10 per 1,000 emails after
- Highly scalable
- AWS ecosystem integration

**Setup:**
1. AWS Console → SES
2. Verify domain/email
3. Get SMTP credentials
4. Use same SMTP configuration as Gmail

### Option 3: Resend

**Pros:**
- 100 emails/day free
- Simple API
- Built for developers
- Great documentation

**Setup:**
1. Sign up: https://resend.com
2. Verify domain
3. Get API key
4. Similar to SendGrid integration

---

## 📝 Complete Render Environment Variables Checklist

Copy this checklist and fill in your values:

```bash
# ========================================
# CORE BACKEND CONFIGURATION
# ========================================
DATABASE_URL=postgresql://postgres.xxx:[password]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
SECRET_KEY=your-super-secret-key-minimum-32-characters
ENVIRONMENT=production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ========================================
# CORS & FRONTEND
# ========================================
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:5173
FRONTEND_URL=https://your-app.vercel.app
APP_URL=https://your-app.vercel.app

# ========================================
# EMAIL CONFIGURATION (GMAIL SMTP)
# ========================================
EMAIL_TESTING_MODE=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=ntufoodapp@gmail.com
SMTP_PASSWORD=[YOUR-16-CHAR-APP-PASSWORD-HERE]
SMTP_FROM_NAME=CampusEats

# ========================================
# OPTIONAL
# ========================================
USE_SUPABASE_EMAIL=false
```

### Before Deploying - Verify:

- [ ] `EMAIL_TESTING_MODE` is `false` (not `true`)
- [ ] `SMTP_EMAIL` is your Gmail address
- [ ] `SMTP_PASSWORD` is 16-character app password (NO SPACES)
- [ ] `SMTP_HOST` is `smtp.gmail.com`
- [ ] `SMTP_PORT` is `587` (not `465`)
- [ ] `APP_URL` is your actual frontend URL
- [ ] All variables saved on Render
- [ ] Backend redeployed after changes

---

## ✅ Success Checklist

You'll know email is working when:

- [ ] Render logs show: `Email Service initialized - Testing Mode: False`
- [ ] Registration doesn't show OTP on screen
- [ ] Email arrives in inbox within 30 seconds
- [ ] Email has professional CampusEats branding
- [ ] OTP code is clearly visible
- [ ] Email includes expiration warning
- [ ] Entering OTP completes registration
- [ ] User is redirected to /stalls page

---

## 📧 Email Template Preview

When configured correctly, users receive this email:

**Subject:** CampusEats - Your Verification Code

**From:** CampusEats <ntufoodapp@gmail.com>

**Content:**
```
┌─────────────────────────────────────┐
│   🍽️ CampusEats                     │
│   Smart Food Ordering for NTU      │
└─────────────────────────────────────┘

Verify Your Email Address

Hello [User Name],

Thank you for registering with CampusEats!
To complete your registration, please use
the verification code below:

┌─────────────────────┐
│  Your Verification  │
│       Code          │
│                     │
│     123456          │
│                     │
└─────────────────────┘

⏰ Important: This code expires in 10 minutes

🔒 Security Notice: Never share your OTP

Best regards,
The CampusEats Team

───────────────────────────────────────
© 2025 CampusEats - Nanyang Technological University
```

---

## 🆘 Need Help?

If you're still having issues:

1. **Check Render Logs** - Look for specific error messages
2. **Test SMTP connection** - Use Python test script above
3. **Verify app password** - Regenerate if unsure
4. **Try different email** - Test with Gmail, Yahoo, Outlook
5. **Check spam folder** - First emails often go to spam

**Share these for debugging:**
- Render backend logs (last 100 lines)
- Environment variables (hide password)
- Error message from browser console
- Email provider you're testing with

---

**🎉 Once configured, your CampusEats app will send professional OTP emails to all new users!**

**Last Updated:** 2025-01-14
