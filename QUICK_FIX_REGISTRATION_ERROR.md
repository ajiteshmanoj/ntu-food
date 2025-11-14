# ⚡ QUICK FIX - "Failed to register email" Error

## 🎯 Problem
Registration returns **400 error**: "Failed to register email. Please try again later."

## ✅ Solution (2 Minutes)

### Go to Render Dashboard

1. Visit: https://render.com/dashboard
2. Click your backend service
3. Click **Environment** tab
4. Click **Add Environment Variable**
5. Add:
   ```
   Name: EMAIL_TESTING_MODE
   Value: true
   ```
6. Click **Save Changes**
7. Wait 1-2 minutes for auto-redeploy

### Test

1. Go to your app → Register
2. Fill form and click "Send Verification Code"
3. OTP should appear on screen ✅
4. Enter OTP to complete registration ✅

---

## 🔍 What This Does

**Before:**
- Backend tries to send real emails
- No SMTP credentials configured
- Returns 400 error ❌

**After:**
- Backend generates OTP
- Returns OTP in API response
- Frontend displays OTP
- No email sent (testing mode)
- Registration works ✅

---

## 📧 For Production (Send Real Emails)

See `EMAIL_CONFIGURATION_GUIDE.md` for:
- Gmail SMTP setup
- SendGrid integration
- Full production configuration

---

**That's it! Registration should work now.**

See detailed guide: `EMAIL_CONFIGURATION_GUIDE.md`
