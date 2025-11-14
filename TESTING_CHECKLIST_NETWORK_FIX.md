# ✅ Testing Checklist - Network Error Fix

## 🎯 What Was Fixed

**Problem:** "Network failed. Please try again" error in production
**Root Cause:** `RegisterWithOTP.tsx` had 3 hardcoded `localhost:8000` URLs
**Solution:** Replaced with `API_BASE_URL` from environment variables

---

## 📋 Quick Verification (5 minutes)

### Before Testing - Verify Environment

**1. Check Vercel Environment Variable:**
- ✅ Vercel already updated with `VITE_API_URL=https://ntu-food-backend.onrender.com`

**2. Verify Backend is Running:**
Visit: https://ntu-food-backend.onrender.com/health
```json
Expected: {"status":"healthy"}
```

---

## 🧪 Test Cases

### Test 1: Browser Console Check (Critical)

**Steps:**
1. Open your deployed app: `https://your-app.vercel.app`
2. Press `F12` to open DevTools
3. Go to **Console** tab
4. Look for the log: `🌐 API Configuration Loaded:`

**Expected Output:**
```javascript
🌐 API Configuration Loaded: {
  VITE_API_URL: "https://ntu-food-backend.onrender.com",
  API_BASE_URL: "https://ntu-food-backend.onrender.com",
  API_URL: "https://ntu-food-backend.onrender.com/api",
  MODE: "production",
  DEV: false,
  PROD: true
}
```

**Result:**
- ✅ PASS if `VITE_API_URL` shows backend URL
- ❌ FAIL if `VITE_API_URL: undefined` → Redeploy needed

---

### Test 2: User Registration with OTP (Primary Fix)

**This specifically tests the fixed code in RegisterWithOTP.tsx**

**Steps:**
1. Navigate to `/register` page
2. Fill in all registration fields:
   - Full Name: `Test User`
   - Email: `test@gmail.com` (any email)
   - Student ID: `U1234567A`
   - Phone: `91234567`
   - Password: `TestPass123`
   - Confirm Password: `TestPass123`
3. Click **"Send Verification Code"**
4. Check browser **Console** and **Network** tab

**Expected:**
- ✅ Network request goes to `https://ntu-food-backend.onrender.com/api/auth/otp/register`
- ✅ Response: 200 OK with `{"testing_otp": "123456", ...}`
- ✅ Page advances to OTP verification step
- ✅ Testing OTP is displayed (if EMAIL_TESTING_MODE=true)

**Common Issues:**
- ❌ Request goes to `http://localhost:8000` → Code not updated, check git status
- ❌ CORS error → Backend CORS_ORIGINS needs your Vercel URL (but you said it's already set)
- ❌ 404 Not Found → Backend route issue
- ❌ Network failed → Backend is down or sleeping (Render free tier)

---

### Test 3: OTP Verification

**Steps:**
1. After Step 2, on OTP screen
2. Enter the 6-digit OTP (displayed in testing mode)
3. Click **"Verify & Create Account"**

**Expected:**
- ✅ Request goes to `https://ntu-food-backend.onrender.com/api/auth/otp/verify-otp`
- ✅ Response: 200 OK with access token
- ✅ Redirects to `/stalls` page
- ✅ User is logged in

---

### Test 4: OTP Resend

**Steps:**
1. On OTP verification screen
2. Click **"Resend Code"** button

**Expected:**
- ✅ Request goes to `https://ntu-food-backend.onrender.com/api/auth/otp/resend-otp`
- ✅ New OTP generated
- ✅ Success message shown

---

### Test 5: Other API Calls (Already Working)

**These were already using environment variables, but test to be sure:**

**Login Test:**
1. Go to `/login`
2. Enter credentials
3. Click Login

**Expected:**
- ✅ Request goes to `https://ntu-food-backend.onrender.com/api/auth/login`

**Browse Stalls Test:**
1. Go to `/stalls`
2. Check if stalls load

**Expected:**
- ✅ Request goes to `https://ntu-food-backend.onrender.com/api/stalls`

**Admin Login Test:**
1. Go to `/admin/login`
2. Login with admin credentials

**Expected:**
- ✅ Request goes to `https://ntu-food-backend.onrender.com/api/auth/login`

---

## 🔍 How to Debug Issues

### Check Browser Network Tab

1. Open DevTools (`F12`)
2. Go to **Network** tab
3. Try the action that's failing
4. Look at the request:
   - **Request URL:** Should be `https://ntu-food-backend.onrender.com/api/...`
   - **Status:** Should be 200 (or 201 for POST)
   - **Response:** Check the response body

### Common Network Tab Issues:

**Request URL shows `http://localhost:8000`**
```
Problem: Code changes not deployed
Fix: Check git status, commit and push changes
```

**Status: (failed) net::ERR_FAILED**
```
Problem: Backend not responding
Fix: Check if backend is sleeping (Render free tier wakes in 30s)
     Visit /health endpoint to wake it up
```

**Status: 0 with CORS error in console**
```
Problem: CORS not configured
Fix: Add your Vercel URL to backend CORS_ORIGINS
     (But you said this is already done)
```

**Status: 404 Not Found**
```
Problem: Wrong API endpoint
Fix: Check the API path in the request
```

---

## 📊 Test Results Template

Copy and fill this out:

```
✅/❌ Test 1 - Console Check
  - VITE_API_URL: _________________
  - Mode: _________________

✅/❌ Test 2 - Registration
  - Request URL: _________________
  - Status: _________________
  - Error (if any): _________________

✅/❌ Test 3 - OTP Verification
  - Status: _________________
  - Redirected: Yes/No

✅/❌ Test 4 - OTP Resend
  - Status: _________________

✅/❌ Test 5 - Other API Calls
  - Login: _________________
  - Stalls: _________________
  - Admin: _________________
```

---

## 🚀 If All Tests Pass

Congratulations! The network error is fixed. You should now be able to:
- ✅ Register new users with OTP verification
- ✅ Login existing users
- ✅ Browse stalls
- ✅ Access admin panel
- ✅ All API calls work in production

---

## 🆘 If Tests Fail

**1. Check if changes are deployed:**
```bash
git status
# Should show no changes if committed and pushed
```

**2. Verify Vercel deployment:**
- Go to Vercel Dashboard → Deployments
- Check latest deployment status
- Click to see build logs

**3. Check backend is awake:**
- Visit: https://ntu-food-backend.onrender.com/health
- If slow (30s+), Render is waking from sleep (normal)

**4. Share debug info:**
- Browser console screenshot (showing API Configuration log)
- Network tab screenshot (showing failed request)
- Error message

---

## 📝 Files Changed

```
frontend/src/config/api.ts                   [NEW] - Centralized config
frontend/src/components/RegisterWithOTP.tsx  [MODIFIED] - 3 URL fixes
frontend/.env.example                        [MODIFIED] - Documentation
backend/.env.example                         [MODIFIED] - Documentation
NETWORK_ERROR_FIX_GUIDE.md                   [NEW] - Full guide
TESTING_CHECKLIST_NETWORK_FIX.md            [NEW] - This file
```

---

## ✨ Success Indicators

You'll know everything is working when:
- ✅ No "Network failed" errors
- ✅ All API requests show backend URL (not localhost)
- ✅ CORS errors are gone
- ✅ Users can register, login, and use the app
- ✅ Console shows correct API configuration

---

**Happy Testing! 🎉**

If you see all green checkmarks, the fix is complete!
