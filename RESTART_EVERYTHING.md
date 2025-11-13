# 🔄 Complete Restart Guide

## 🛑 Step 1: Stop Everything

### Kill Local Servers:
```bash
# Kill backend (port 8000)
lsof -ti:8000 | xargs kill -9

# Kill frontend (port 5173)
lsof -ti:5173 | xargs kill -9
```

### Close All Browsers:
- Close ALL browser tabs with ntu-food-xi.vercel.app
- Close ALL browser windows
- Quit browser completely (Cmd+Q on Mac)

---

## 🧹 Step 2: Clean Everything

```bash
cd "/Users/ajitesh/Desktop/My Projects/NTU_Food/ntu-food"

# Clean frontend
cd frontend
rm -rf node_modules
rm -rf dist
npm cache clean --force

# Reinstall
npm install

# Go back to root
cd ..
```

---

## 🚀 Step 3: Test Locally First

### Terminal 1 - Backend:
```bash
cd "/Users/ajitesh/Desktop/My Projects/NTU_Food/ntu-food/backend"

# Activate virtual environment (if you have one)
# source venv/bin/activate

# Start backend
python -m uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     CampusEats API started in development mode
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Test it:**
```bash
# In another terminal
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

---

### Terminal 2 - Frontend:
```bash
cd "/Users/ajitesh/Desktop/My Projects/NTU_Food/ntu-food/frontend"

# Start frontend
npm run dev
```

**Expected output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

---

## 🧪 Step 4: Test Locally

1. Open browser: http://localhost:5173
2. Open Console (F12)
3. You should see:
   ```
   🔧 API Configuration: {
     VITE_API_URL: undefined,
     API_BASE_URL: "http://localhost:8000",
     mode: "development"
   }
   ```
   ✅ This is CORRECT for local development!

4. Go to: http://localhost:5173/register
5. Try to create an account
6. **This should work!** (connects to local backend)

---

## 🌐 Step 5: Fix Vercel Production

If local works but production doesn't, the issue is Vercel deployment.

### Option A: Use Vercel CLI (Most Reliable)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Go to frontend
cd "/Users/ajitesh/Desktop/My Projects/NTU_Food/ntu-food/frontend"

# Link to your project
vercel link

# Check environment variables
vercel env ls

# Add VITE_API_URL if missing
vercel env add VITE_API_URL production
# Enter: https://ntu-food-backend.onrender.com

# Deploy with fresh build
vercel --prod --force

# This creates a NEW deployment URL
# Use that URL for testing
```

### Option B: Manual Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Click your project
3. Settings → Environment Variables
4. Verify `VITE_API_URL = https://ntu-food-backend.onrender.com`
5. Go to Deployments tab
6. Click latest deployment → "Redeploy"
7. **UNCHECK** "Use existing Build Cache"
8. Click "Redeploy"
9. Wait 2 minutes
10. Use the new deployment preview URL

---

## 🔍 Debugging Checklist

### If Local Works But Production Doesn't:

✅ **Local works?** → Backend and frontend code is fine
❌ **Production doesn't?** → Vercel configuration issue

**Check:**
1. Vercel environment variable `VITE_API_URL` is set
2. Latest deployment succeeded (not failed)
3. Backend CORS allows Vercel domain
4. Using correct Vercel URL (not cached old one)

### Check Backend CORS:

Your Render backend needs to allow Vercel domain:

```python
# backend/app/main.py should have:
CORS_ORIGINS = "https://ntu-food-xi.vercel.app,http://localhost:5173"
```

Check in Render Dashboard → Environment → `CORS_ORIGINS`

---

## 🎯 Quick Test Commands

### Test Backend Health:
```bash
curl https://ntu-food-backend.onrender.com/health
# Should return: {"status":"healthy"}
```

### Test Backend API Root:
```bash
curl https://ntu-food-backend.onrender.com/
# Should return: {"message": "Welcome to CampusEats API", ...}
```

### Check Frontend Bundle Hash:
```bash
curl -s https://ntu-food-xi.vercel.app/ | grep -o 'index-[^"]*\.js'
# Should show current JS file hash
```

---

## 🆘 If Nothing Works

### Nuclear Option - Redeploy Everything:

```bash
# 1. Delete Vercel project
# Go to Vercel Dashboard → Settings → Delete Project

# 2. Redeploy fresh
cd frontend
vercel --prod

# 3. Add environment variable in new project
vercel env add VITE_API_URL production
# Enter: https://ntu-food-backend.onrender.com

# 4. Redeploy
vercel --prod
```

---

## 📋 Summary

**For Local Development:**
1. Kill all servers
2. Start backend: `cd backend && python -m uvicorn app.main:app --reload --port 8000`
3. Start frontend: `cd frontend && npm run dev`
4. Test: http://localhost:5173

**For Production:**
1. Verify Vercel environment variable exists
2. Force redeploy without cache
3. Use deployment preview URL
4. Check backend CORS settings

---

**Start with local testing first to verify the code works!**
