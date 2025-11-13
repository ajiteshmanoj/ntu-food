# 🔧 "Network Error" During Registration - Fix Guide

## 🎯 Problem
When trying to create a new account, you get: **"Network error. Please try again"**

## 🔍 Root Cause
Your Vercel frontend app doesn't know the URL of your Render backend API. By default, it tries to connect to `http://localhost:8000`, which doesn't exist in production.

---

## ✅ SOLUTION: Configure Vercel Environment Variable

### Step-by-Step Fix (2 minutes):

1. **Go to Vercel Dashboard:**
   ```
   https://vercel.com/dashboard
   ```

2. **Select Your Project:**
   - Click on your project (likely named "ntu-food" or similar)

3. **Open Settings:**
   - Click "Settings" tab at the top

4. **Add Environment Variable:**
   - Click "Environment Variables" in the left sidebar
   - Click "Add New"

5. **Configure the Variable:**
   ```
   Name:  VITE_API_URL
   Value: https://ntu-food-backend.onrender.com
   ```

   **Important**: No trailing slash!

6. **Select Environment:**
   - Check all three: ☑️ Production ☑️ Preview ☑️ Development

7. **Save:**
   - Click "Save"

8. **Redeploy:**
   - Go to "Deployments" tab
   - Click "..." on the latest deployment
   - Click "Redeploy"
   - Wait 2 minutes for redeployment

---

## 🧪 Verify the Fix

### After Redeployment (2 minutes):

1. **Visit Your Frontend:**
   ```
   https://ntu-food-xi.vercel.app
   ```

2. **Open Browser Console:**
   - Press F12 (Windows) or Cmd+Option+I (Mac)
   - Go to "Console" tab

3. **Try to Register:**
   - Fill out registration form
   - Click "Send OTP"

4. **Check Console:**
   - Should see API request to: `https://ntu-food-backend.onrender.com/api/auth/otp/register`
   - Should NOT see errors about "localhost:8000"

---

## 🔍 How to Check Current Configuration

### Check if VITE_API_URL is Set:

1. **In Browser Console (on your live site):**
   ```javascript
   console.log(import.meta.env.VITE_API_URL)
   ```

   **Expected**: `https://ntu-food-backend.onrender.com`
   **Problem**: `undefined` or `http://localhost:8000`

2. **In Network Tab:**
   - Open DevTools (F12)
   - Go to "Network" tab
   - Try to register
   - Look at the request URL

   **Expected**: Request goes to `https://ntu-food-backend.onrender.com/api/auth/otp/register`
   **Problem**: Request goes to `http://localhost:8000/...` or fails immediately

---

## 📋 Alternative Method: Using Vercel CLI

If you prefer command line:

```bash
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Login
vercel login

# Link to your project
cd frontend
vercel link

# Add environment variable
vercel env add VITE_API_URL production
# When prompted, enter: https://ntu-food-backend.onrender.com

# Redeploy
vercel --prod
```

---

## 🚨 Common Mistakes to Avoid

### ❌ Wrong Variable Name:
```
API_URL  ❌ (won't work - Vite requires VITE_ prefix)
REACT_APP_API_URL  ❌ (that's for Create React App, not Vite)
VITE_API_URL  ✅ (correct!)
```

### ❌ Trailing Slash:
```
https://ntu-food-backend.onrender.com/  ❌ (extra slash causes issues)
https://ntu-food-backend.onrender.com   ✅ (no trailing slash)
```

### ❌ HTTP instead of HTTPS:
```
http://ntu-food-backend.onrender.com  ❌ (Render uses HTTPS)
https://ntu-food-backend.onrender.com ✅ (always HTTPS)
```

---

## 🔍 Additional Debugging

### If Still Getting Network Error:

1. **Check Backend is Running:**
   ```bash
   curl https://ntu-food-backend.onrender.com/health
   ```

   **Expected**: `{"status":"healthy"}`
   **If fails**: Backend is down or sleeping (Render free tier)

2. **Check CORS Configuration:**
   - Backend must allow requests from Vercel domain
   - Check Render environment variable: `CORS_ORIGINS`
   - Should include: `https://ntu-food-xi.vercel.app`

3. **Wake Up Render Backend:**
   - First request after 15min of inactivity takes ~30 seconds
   - Visit: https://ntu-food-backend.onrender.com/health
   - Wait 30 seconds, then try registration again

---

## 📊 Current Configuration Check

### Vercel Environment Variables (Should Have):
```
VITE_API_URL = https://ntu-food-backend.onrender.com
```

### Render Environment Variables (Should Have):
```
CORS_ORIGINS = https://ntu-food-xi.vercel.app,http://localhost:5173
FRONTEND_URL = https://ntu-food-xi.vercel.app
```

---

## 🎯 Quick Test After Fix

### Test Registration Flow:

1. **Go to**: https://ntu-food-xi.vercel.app/register

2. **Fill Form:**
   ```
   Email: test@example.com
   Student ID: U1234567A
   Name: Test User
   Phone: +65 9123 4567
   Password: TestPass123
   ```

3. **Click "Send OTP"**

4. **Expected Result:**
   - ✅ Loading spinner appears
   - ✅ OTP verification step shows
   - ✅ Email sent (or console log shows OTP in testing mode)
   - ✅ No "Network error" message

5. **If Error:**
   - Check browser console for actual error
   - Check Network tab for failed request
   - Share the error message for further debugging

---

## 🆘 Still Not Working?

### Get More Details:

1. **Open Browser Console (F12)**

2. **Go to Network Tab**

3. **Try to register**

4. **Look for the API request:**
   - Click on the failed request
   - Check "Headers" tab
   - Check "Response" tab
   - Share the error details

### Common Errors:

**"Failed to fetch"**
- Frontend can't reach backend URL
- Check VITE_API_URL is set correctly in Vercel

**"CORS policy error"**
- Backend not allowing Vercel domain
- Update CORS_ORIGINS in Render

**"404 Not Found"**
- Endpoint doesn't exist
- Check backend is deployed and running

**"500 Internal Server Error"**
- Backend error
- Check Render logs for Python errors

---

## 📝 Summary

**The Fix:**
1. Add `VITE_API_URL=https://ntu-food-backend.onrender.com` to Vercel Environment Variables
2. Redeploy the frontend
3. Test registration

**Time to Fix**: ~3 minutes
**Why This Happened**: Environment variable not configured during initial deployment

---

**Need More Help?**
Share the exact error message from browser console and I can provide more specific guidance.
