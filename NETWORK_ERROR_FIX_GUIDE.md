# 🔧 Network Error Fix Guide

## Problem: "Network failed. Please try again"

This error occurs when the frontend cannot connect to the backend API. This guide will help you fix it.

---

## 📊 Diagnosis Complete

I've analyzed your codebase and found:

### ✅ **What's Already Working:**
- `frontend/src/services/api.ts` - Uses `VITE_API_URL` ✓
- `frontend/src/services/adminApi.ts` - Uses `VITE_API_URL` ✓

### ❌ **What Was Broken (NOW FIXED):**
- `frontend/src/components/RegisterWithOTP.tsx` - Was hardcoded to `localhost:8000` (FIXED)

### 🆕 **What I've Created:**
- `frontend/src/config/api.ts` - Centralized API configuration with debug logging

---

## 🎯 Root Cause

Your frontend is deployed on **Vercel** but the `VITE_API_URL` environment variable is either:
1. Not set in Vercel dashboard
2. Set incorrectly
3. Not applied (requires rebuild)

Meanwhile, your backend is running on **Render** at: `https://ntu-food-backend.onrender.com`

---

## 🚀 Quick Fix (3 Steps)

### Step 1: Set Environment Variable in Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project (`ntu-food` or similar)
3. Click **Settings** → **Environment Variables**
4. Add this variable:
   ```
   Name: VITE_API_URL
   Value: https://ntu-food-backend.onrender.com
   ```
5. Apply to: **Production**, **Preview**, and **Development**
6. Click **Save**

### Step 2: Update Backend CORS

1. Go to [Render Dashboard](https://render.com/dashboard)
2. Select your backend service
3. Click **Environment** tab
4. Find or add `CORS_ORIGINS` variable:
   ```
   Name: CORS_ORIGINS
   Value: https://your-frontend.vercel.app,http://localhost:5173
   ```
   ⚠️ Replace `your-frontend.vercel.app` with your actual Vercel domain
5. Click **Save Changes**
6. Wait for backend to redeploy (auto-triggers)

### Step 3: Redeploy Frontend

**Option A: Trigger Redeploy from Vercel**
1. Vercel Dashboard → Your Project → Deployments
2. Click the **...** menu on latest deployment
3. Click **Redeploy**

**Option B: Push a commit**
```bash
git commit --allow-empty -m "Trigger redeploy with VITE_API_URL"
git push origin main
```

---

## 🔍 Verify the Fix

### 1. Check Frontend Logs (Browser Console)

Open your deployed app and press **F12** to open DevTools:

```javascript
// You should see this log in the Console:
🌐 API Configuration Loaded: {
  VITE_API_URL: "https://ntu-food-backend.onrender.com",
  API_BASE_URL: "https://ntu-food-backend.onrender.com",
  API_URL: "https://ntu-food-backend.onrender.com/api",
  MODE: "production",
  DEV: false,
  PROD: true
}
```

**If you see:**
- ✅ `VITE_API_URL: "https://ntu-food-backend.onrender.com"` → Environment variable is set correctly
- ❌ `VITE_API_URL: undefined` → Environment variable NOT set, go back to Step 1

### 2. Check Backend Health

Visit this URL directly in your browser:
```
https://ntu-food-backend.onrender.com/health
```

**Expected Response:**
```json
{"status":"healthy"}
```

**If you see:**
- ✅ `{"status":"healthy"}` → Backend is running
- ❌ "Not Found" → Backend is not deployed correctly (see RENDER_TROUBLESHOOTING.md)
- ❌ Takes 30+ seconds → Render free tier is waking from sleep (normal)

### 3. Test API Documentation

Visit:
```
https://ntu-food-backend.onrender.com/docs
```

You should see FastAPI's interactive documentation (Swagger UI).

### 4. Test a Real API Call

In browser console, run:
```javascript
fetch('https://ntu-food-backend.onrender.com/api/stalls')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

**Expected:** Array of stalls
**If CORS error:** Backend CORS_ORIGINS doesn't include your frontend URL

---

## 📁 Files Changed (Summary)

### Created:
1. **`frontend/src/config/api.ts`** - Centralized API configuration
   - Reads `VITE_API_URL` from environment
   - Falls back to `localhost:8000` for development
   - Logs configuration to console for debugging

### Modified:
2. **`frontend/src/components/RegisterWithOTP.tsx`**
   - Line 4: Import `API_BASE_URL`
   - Line 150: Changed `http://localhost:8000` → `${API_BASE_URL}`
   - Line 228: Changed `http://localhost:8000` → `${API_BASE_URL}`
   - Line 263: Changed `http://localhost:8000` → `${API_BASE_URL}`

3. **`frontend/.env.example`**
   - Added comprehensive deployment instructions
   - Added troubleshooting section
   - Updated with Vercel/Netlify examples

4. **`backend/.env.example`**
   - Updated CORS_ORIGINS examples
   - Added production URL placeholders

---

## 🛠️ Local Development Testing

Before deploying, test locally:

### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

### Terminal 2 - Frontend:
```bash
cd frontend

# Create .env.local (if not exists)
echo "VITE_API_URL=http://localhost:8000" > .env.local

npm run dev
```

### Test:
1. Open http://localhost:5173
2. Press F12 → Console tab
3. Look for: `🌐 API Configuration Loaded:`
4. Verify `API_BASE_URL: "http://localhost:8000"`
5. Try registering or logging in

---

## 🚨 Common Errors & Solutions

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Cause:** Backend CORS_ORIGINS doesn't include your frontend URL

**Fix:**
1. Backend Render dashboard → Environment → CORS_ORIGINS
2. Add your Vercel URL: `https://your-app.vercel.app`
3. Format: `https://url1.com,https://url2.com` (comma-separated, no spaces)
4. Save and wait for redeploy

### Error: "Failed to fetch" or "net::ERR_CONNECTION_REFUSED"

**Cause:** Backend is not running or URL is wrong

**Fix:**
1. Check backend URL is correct (no typos)
2. Visit backend health endpoint: `https://your-backend.onrender.com/health`
3. If "Not Found", backend isn't running (check Render logs)
4. If takes 30s+ to respond, Render is waking from sleep (normal on free tier)

### Error: Backend returns 404 for all API calls

**Cause:** API paths are incorrect

**Fix:**
1. Verify API calls use `/api/` prefix
2. Check `frontend/src/config/api.ts` exports correct `API_URL`
3. Verify backend routes in `backend/app/main.py` use `/api/` prefix

### Warning: "VITE_API_URL not set in production!"

**Cause:** Environment variable not set in Vercel

**Fix:**
1. Vercel Dashboard → Settings → Environment Variables
2. Add `VITE_API_URL` with your backend URL
3. Redeploy frontend

---

## 📝 Environment Variables Checklist

### Frontend (Vercel/Netlify):
- [x] `VITE_API_URL` = `https://ntu-food-backend.onrender.com`

### Backend (Render):
- [x] `DATABASE_URL` = Your Supabase connection string
- [x] `CORS_ORIGINS` = Your frontend URL(s), comma-separated
- [x] `SECRET_KEY` = Random secure key (generate with: `openssl rand -hex 32`)
- [x] `ENVIRONMENT` = `production`
- [ ] `SMTP_EMAIL` = Your Gmail (for OTP emails)
- [ ] `SMTP_PASSWORD` = Gmail app password
- [ ] `EMAIL_TESTING_MODE` = `false` (to send real emails)

---

## 🎓 How to Find Your URLs

### Find Your Frontend URL (Vercel):
1. Vercel Dashboard → Your Project
2. Look at the top: `https://your-project-xyz.vercel.app`
3. Or go to: Deployments → Latest deployment → Visit

### Find Your Backend URL (Render):
1. Render Dashboard → Your Service
2. Look at the top: `https://your-service.onrender.com`
3. Or click the URL under service name

---

## 🧪 Debug Mode

The new `frontend/src/config/api.ts` includes debug logging. Check browser console:

```javascript
🌐 API Configuration Loaded: {
  VITE_API_URL: "...",      // Should match your backend URL
  API_BASE_URL: "...",      // Should match your backend URL
  API_URL: ".../api",       // Should be backend URL + /api
  MODE: "production",       // Should be "production" when deployed
  DEV: false,               // Should be false in production
  PROD: true                // Should be true in production
}
```

If any value is wrong, check your environment variable settings.

---

## 📞 Still Not Working?

If the error persists after following this guide:

1. **Check Render Backend Logs:**
   - Render Dashboard → Your Service → Logs
   - Look for errors or connection issues

2. **Check Vercel Build Logs:**
   - Vercel Dashboard → Deployments → Latest → View Function Logs
   - Look for build errors or warnings

3. **Check Browser Network Tab:**
   - F12 → Network tab
   - Try an action (login, register)
   - Click the failed request
   - Look at Request URL and Response

4. **Share These Details:**
   - Browser console logs (with 🌐 API Configuration)
   - Network tab screenshot
   - Render backend URL
   - Vercel frontend URL
   - Any error messages

---

## ✅ Success Checklist

You'll know it's working when:

- [ ] Browser console shows correct `VITE_API_URL`
- [ ] Backend health endpoint returns `{"status":"healthy"}`
- [ ] Backend `/docs` page loads
- [ ] No CORS errors in browser console
- [ ] Login/register works without "Network Error"
- [ ] API calls show in Network tab with 200 status

---

**Last Updated:** 2025-01-14
**Status:** Ready for deployment
