# 📧 Email Configuration Guide - Fix "Failed to register email"

## 🔴 Problem

When trying to register on the deployed site, you get:
```
"Failed to register email. Please try again later."
```

**Root Cause:** Backend is trying to send real emails but SMTP credentials are not configured on Render.

---

## ✅ QUICK FIX (2 Minutes) - Enable Testing Mode

**This allows registration to work WITHOUT sending real emails.**

### Step 1: Add Environment Variable to Render

1. Go to [Render Dashboard](https://render.com/dashboard)
2. Select your backend service (`ntu-food-backend` or similar)
3. Click **Environment** tab
4. Click **Add Environment Variable**
5. Add this:
   ```
   Name: EMAIL_TESTING_MODE
   Value: true
   ```
6. Click **Save Changes**
7. Wait for backend to redeploy (1-2 minutes)

### Step 2: Test Registration

1. Go to your deployed frontend
2. Try registering a new user
3. You should see the OTP displayed on the screen (not sent via email)
4. Registration should complete successfully ✅

---

## 🎯 How Testing Mode Works

When `EMAIL_TESTING_MODE=true`:
- ✅ OTP is generated successfully
- ✅ OTP is returned in the API response
- ✅ Frontend displays the OTP for you to copy
- ✅ Registration completes without errors
- ❌ NO actual email is sent

**Perfect for:**
- Development
- Testing
- Demo purposes
- When you don't have email credentials yet

---

## 📬 PRODUCTION FIX - Configure Real Email Sending

**For production use, configure Gmail SMTP to send real OTP emails.**

### Option A: Gmail SMTP (Recommended - Free)

#### Step 1: Get Gmail App Password

1. Go to your Google Account: https://myaccount.google.com
2. Navigate to **Security**
3. Enable **2-Step Verification** (if not already enabled)
4. Go to **App Passwords**: https://myaccount.google.com/apppasswords
5. Select app: **Mail**
6. Select device: **Other** (enter "CampusEats Backend")
7. Click **Generate**
8. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

#### Step 2: Configure Render Environment Variables

Add these to Render → Environment:

```bash
EMAIL_TESTING_MODE=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # 16-char app password (no spaces)
SMTP_FROM_NAME=CampusEats
APP_URL=https://your-frontend.vercel.app
```

**Important:**
- Use your real Gmail address for `SMTP_EMAIL`
- Use the 16-character App Password (remove spaces) for `SMTP_PASSWORD`
- Update `APP_URL` with your actual frontend URL

#### Step 3: Test Email Sending

1. Save changes and wait for redeploy
2. Try registering with a real email address
3. Check your inbox for the OTP email
4. Complete registration

---

### Option B: SendGrid (Alternative - Free Tier Available)

1. Sign up at https://sendgrid.com (free tier: 100 emails/day)
2. Create API key
3. Configure environment variables:

```bash
EMAIL_TESTING_MODE=false
EMAIL_PROVIDER=sendgrid  # Optional
SENDGRID_API_KEY=your-sendgrid-api-key
SMTP_FROM_EMAIL=noreply@your-domain.com
APP_URL=https://your-frontend.vercel.app
```

*Note: This requires code modifications to use SendGrid API instead of SMTP*

---

## 🛠️ Current Render Environment Variable Checklist

### Required for Basic Functionality:
- [x] `DATABASE_URL` - Supabase PostgreSQL connection string
- [x] `CORS_ORIGINS` - Your frontend URL(s)
- [x] `SECRET_KEY` - Random secure key
- [x] `ENVIRONMENT` - Should be `production`

### Required for Email (Choose ONE option):

**Option 1: Testing Mode (Quick Fix)**
- [ ] `EMAIL_TESTING_MODE=true`

**Option 2: Gmail SMTP (Production)**
- [ ] `EMAIL_TESTING_MODE=false`
- [ ] `SMTP_EMAIL` - Your Gmail address
- [ ] `SMTP_PASSWORD` - Gmail App Password (16 chars)
- [ ] `SMTP_HOST=smtp.gmail.com`
- [ ] `SMTP_PORT=587`
- [ ] `SMTP_FROM_NAME=CampusEats`
- [ ] `APP_URL` - Your frontend URL

### Optional:
- [ ] `ALGORITHM=HS256`
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES=30`
- [ ] `FRONTEND_URL` - Your frontend URL

---

## 🔍 Verify Configuration

### Check 1: Environment Variables Set

**Render Dashboard → Your Service → Environment**

Should see at minimum:
```
EMAIL_TESTING_MODE = true
DATABASE_URL = postgresql://...
CORS_ORIGINS = https://your-app.vercel.app
SECRET_KEY = your-secret-key
ENVIRONMENT = production
```

### Check 2: Backend Logs

**Render Dashboard → Logs**

Look for these messages on startup:
```
INFO - Email Service initialized - Testing Mode: True
INFO - CampusEats API started in production mode
```

If you see:
```
ERROR - SMTP credentials not configured...
```
Then either:
- Set `EMAIL_TESTING_MODE=true`, OR
- Configure SMTP credentials

### Check 3: Test Registration

1. Open deployed frontend
2. Navigate to `/register`
3. Fill in the form and submit
4. Check browser **Network** tab → Response:

**Success (Testing Mode):**
```json
{
  "message": "OTP generated for testing",
  "email": "test@gmail.com",
  "expires_in_minutes": 10,
  "testing_otp": "123456"
}
```

**Success (Production with SMTP):**
```json
{
  "message": "Verification code sent to your NTU email",
  "email": "test@gmail.com",
  "expires_in_minutes": 10
}
```

**Failure (No SMTP configured):**
```json
{
  "detail": "Failed to register email. Please try again later."
}
```

---

## 🐛 Troubleshooting

### Error: "Failed to register email"

**Cause:** Backend can't send emails and testing mode is disabled

**Fix:**
```bash
# On Render, set:
EMAIL_TESTING_MODE=true
```

### Error: "SMTP Authentication failed"

**Cause:** Wrong Gmail password or not using App Password

**Fix:**
1. Generate new App Password (see Option A above)
2. Use the 16-character password WITHOUT spaces
3. Make sure 2FA is enabled on your Google account

### Error: "Invalid email format" or 400 error with validation

**Cause:** Frontend sending incorrect data format

**Check:**
- Email format is valid
- Student ID matches pattern `U1234567A`
- Phone number matches pattern `+65XXXXXXXX`
- Password has uppercase, lowercase, and numbers

### OTP not displayed in testing mode

**Cause:** Frontend might not be updated to show testing OTP

**Fix:**
- Check browser console for API response
- Look for `testing_otp` field in response
- If present but not shown, frontend needs updating

### Emails go to spam

**Cause:** Gmail SMTP from new accounts often flagged as spam

**Fix:**
1. Check spam folder
2. Mark as "Not Spam"
3. Add sender to contacts
4. For production, consider using SendGrid or AWS SES

---

## 📋 Quick Reference

### Testing Mode (Development)
```bash
EMAIL_TESTING_MODE=true
```
- OTP shown in response
- No emails sent
- Perfect for testing

### Production Mode (Gmail)
```bash
EMAIL_TESTING_MODE=false
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```
- Real emails sent
- OTP delivered to inbox
- Production ready

---

## 🎓 Understanding the Flow

1. **User submits registration** → Frontend sends data to `/api/auth/otp/register`
2. **Backend validates data** → Checks email, student ID, password
3. **Backend generates OTP** → Random 6-digit code
4. **Backend stores OTP** → Saves to database (expires in 10 min)
5. **Backend sends email** → Either:
   - **Testing mode:** Returns OTP in response
   - **Production mode:** Sends email via SMTP
6. **Frontend shows OTP screen** → User enters code
7. **User verifies OTP** → Frontend sends to `/api/auth/otp/verify-otp`
8. **Backend creates account** → Marks user as verified
9. **User logged in** → Access token returned

---

## 🔒 Security Notes

- **Never commit SMTP credentials** to git
- Use environment variables for all secrets
- Gmail App Passwords are safer than account passwords
- Testing mode is fine for development, not production
- Rate limiting prevents spam (3 emails per 5 minutes)
- OTPs expire after 10 minutes
- OTPs can only be used once

---

## 📞 Still Having Issues?

1. **Check Render logs** for specific error messages
2. **Check browser console** for frontend errors
3. **Check Network tab** for API responses
4. **Verify environment variables** are saved correctly
5. **Wait for redeploy** after changing env vars

**Share these details for help:**
- Render backend logs (last 50 lines)
- Browser Network tab screenshot (API response)
- Current environment variables (hide secrets)
- Error message from frontend

---

## ✅ Success Checklist

You'll know it's working when:

- [ ] Registration form submits without errors
- [ ] You see OTP (testing mode) or receive email (production)
- [ ] OTP verification works
- [ ] User account is created
- [ ] You're redirected to /stalls page
- [ ] You're logged in automatically

---

**Last Updated:** 2025-01-14
**Status:** Ready to deploy
