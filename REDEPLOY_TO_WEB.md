# 🚀 Redeploy CampusEats to Web (Vercel + Render)

**Quick Guide:** Get your app back online in ~15 minutes

**Your Setup:**
- 🎨 Frontend → Vercel (Free)
- 🔧 Backend → Render.com (Free)
- 💾 Database → Supabase (Already connected! ✅)

---

## 📋 Prerequisites Check

✅ **Already Complete:**
- GitHub repo: https://github.com/ajiteshmanoj/campuseats
- Supabase connected and working
- Vercel config file exists
- Render config file exists

⚠️ **Need to Setup:**
- Push latest code to GitHub
- Deploy backend to Render
- Deploy frontend to Vercel
- Update environment variables

---

## 🎯 Deployment Plan

```
Step 1: Push Code to GitHub          (2 min)
Step 2: Deploy Backend to Render     (8 min)
Step 3: Deploy Frontend to Vercel    (5 min)
Total Time: ~15 minutes
```

---

## Step 1: Push Latest Code to GitHub (2 minutes)

You have new changes that need to be pushed:

### What's New:
- ✅ Review system (backend complete)
- ✅ Redux store implementation
- ✅ Supabase reconnection (DATABASE_URL updated)
- ✅ Various documentation files

### Push Commands:

```bash
cd /Users/ajitesh/Desktop/My\ Projects/NTU_Food/campuseats

# Add all changes
git add .

# Commit with message
git commit -m "Add review system, Redux store, and reconnect to Supabase

- Backend: Complete review API with ratings and comments
- Frontend: Redux Toolkit store with auth/stalls/orders/cart slices
- Database: Reconnected to Supabase PostgreSQL
- Docs: Comprehensive deployment and reconnection guides

🤖 Generated with Claude Code"

# Push to GitHub
git push origin main
```

**Verify Push:**
Visit https://github.com/ajiteshmanoj/campuseats and confirm latest commit shows up.

---

## Step 2: Deploy Backend to Render.com (8 minutes)

### A. Check if You Already Have a Render Project

1. **Go to Render Dashboard:**
   ```
   https://render.com/dashboard
   ```

2. **Look for existing service:**
   - Service name might be: `campuseats-backend` or similar
   - If exists: Skip to "Update Existing Service" below
   - If not exists: Continue to "Create New Service"

---

### B. Create New Service (If Needed)

1. **Click "New +" → "Web Service"**

2. **Connect GitHub:**
   - Click "Connect account" if needed
   - Select repository: `ajiteshmanoj/campuseats`
   - Click "Connect"

3. **Configure Service:**
   ```
   Name: campuseats-backend
   Region: Singapore (or closest to you)
   Branch: main
   Runtime: Python 3

   Build Command:
   pip install -r backend/requirements.txt

   Start Command:
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT

   Plan: Free ($0/month)
   ```

4. **Click "Create Web Service"**

5. **IMPORTANT: Wait for first deploy to complete** (this will fail, that's ok)
   - Takes ~2-3 minutes
   - Will show "Deploy failed" (expected - missing env vars)

---

### C. Set Environment Variables

1. **In Render Dashboard, go to your service**

2. **Click "Environment" tab**

3. **Add these variables** (click "Add Environment Variable" for each):

```bash
# DATABASE (Supabase)
DATABASE_URL=postgresql://postgres.dhmwuixxxsxkyfjdblqu:Ajite$h0812@aws-1-ap-south-1.pooler.supabase.com:6543/postgres

# Supabase Config
SUPABASE_URL=https://dhmwuixxxsxkyfjdblqu.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRobXd1aXh4eHN4a3lmamRibHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwMjY3NTAsImV4cCI6MjA3NTYwMjc1MH0.Yov5NZhvE70BNlEZYlCTET2MEFHYnTFhTHe3regE9-o

# Security (IMPORTANT: Generate new SECRET_KEY for production!)
SECRET_KEY=your-super-secret-key-change-this-in-production-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=production

# CORS (we'll update this after Vercel deployment)
CORS_ORIGINS=http://localhost:5173,https://campuseats.vercel.app
FRONTEND_URL=https://campuseats.vercel.app

# Email
EMAIL_TESTING_MODE=false
USE_SUPABASE_EMAIL=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=ntufoodapp@gmail.com
SMTP_PASSWORD=zjrcmdheyeopdlwy
SMTP_FROM_NAME=CampusEats
APP_URL=https://campuseats.vercel.app
```

**⚠️ SECURITY NOTE:**
Generate a secure SECRET_KEY:
```bash
# On Mac/Linux:
openssl rand -hex 32

# Copy output and use as SECRET_KEY
```

4. **Click "Save Changes"**

5. **Trigger Manual Deploy:**
   - Click "Manual Deploy" → "Deploy latest commit"
   - Wait ~2 minutes
   - Should see "Live ✅" with green indicator

6. **Copy your Render URL:**
   - Looks like: `https://campuseats-backend.onrender.com`
   - **Save this URL** - you'll need it for Vercel!

7. **Test Backend:**
   - Visit: `https://YOUR-RENDER-URL.onrender.com/health`
   - Should return: `{"status":"healthy"}`
   - Visit: `https://YOUR-RENDER-URL.onrender.com/docs`
   - Should show FastAPI documentation

---

### D. Update Existing Service (If Already Exists)

1. **Go to your existing service in Render**

2. **Check Environment Variables:**
   - Verify DATABASE_URL points to Supabase (not old database)
   - Update if needed (see variables list above)

3. **Trigger Manual Deploy:**
   - Click "Manual Deploy" → "Deploy latest commit"
   - This will pull latest code from GitHub

---

## Step 3: Deploy Frontend to Vercel (5 minutes)

### A. Check if You Already Have a Vercel Project

1. **Go to Vercel Dashboard:**
   ```
   https://vercel.com/dashboard
   ```

2. **Look for existing project:**
   - Project name might be: `campuseats` or `campuseats-frontend`
   - If exists: Skip to "Update Existing Project" below
   - If not exists: Continue to "Create New Project"

---

### B. Create New Project (If Needed)

1. **Click "Add New..." → "Project"**

2. **Import Git Repository:**
   - Select `ajiteshmanoj/campuseats`
   - Click "Import"

3. **Configure Project:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Environment Variables:**
   Click "Environment Variables" and add:

   ```
   Key: VITE_API_URL
   Value: https://YOUR-RENDER-URL.onrender.com
   ```

   **Replace `YOUR-RENDER-URL` with your actual Render URL from Step 2!**

5. **Click "Deploy"**

6. **Wait for deployment** (~2 minutes)
   - Should see "Congratulations!" when done
   - Copy your Vercel URL (looks like: `https://campuseats-xxxx.vercel.app`)

---

### C. Update Existing Project (If Already Exists)

1. **Go to your project in Vercel**

2. **Settings → Environment Variables:**
   - Update `VITE_API_URL` with your current Render URL
   - Value: `https://YOUR-RENDER-URL.onrender.com`

3. **Deployments → Three dots → Redeploy:**
   - This pulls latest code from GitHub

---

## Step 4: Update CORS (CRITICAL!)

After Vercel deployment, you need to update backend CORS:

1. **Go back to Render Dashboard → Your Backend Service**

2. **Environment → Edit CORS_ORIGINS:**
   ```
   CORS_ORIGINS=https://YOUR-VERCEL-URL.vercel.app,http://localhost:5173
   ```

   **Replace `YOUR-VERCEL-URL` with your actual Vercel URL!**

3. **Also update:**
   ```
   FRONTEND_URL=https://YOUR-VERCEL-URL.vercel.app
   APP_URL=https://YOUR-VERCEL-URL.vercel.app
   ```

4. **Save Changes**

5. **Manual Deploy** (to apply CORS changes)

---

## Step 5: Test Your Live App! 🎉

### Frontend Test:
1. **Visit your Vercel URL:**
   ```
   https://YOUR-VERCEL-URL.vercel.app
   ```

2. **Should see:** CampusEats login page

3. **Try logging in:**
   - Email: `admin@campuseats.com`
   - Password: `admin123`

4. **Should work:** Redirects to stalls page with 17 stalls

### Backend Test:
1. **Visit API docs:**
   ```
   https://YOUR-RENDER-URL.onrender.com/docs
   ```

2. **Try endpoint:** `GET /api/stalls`
   - Click "Try it out" → "Execute"
   - Should return 17 stalls

### Full Flow Test:
1. Login as student
2. Browse stalls (should load)
3. Click on a stall (should show menu)
4. Add item to cart (should work)
5. Try placing order (should work if everything connected)

---

## 🐛 Troubleshooting

### Issue: Frontend can't connect to backend

**Check:**
1. VITE_API_URL in Vercel is correct
2. CORS_ORIGINS in Render includes your Vercel URL
3. Backend is deployed and showing "Live ✅"

**Fix:**
```bash
# Verify backend is accessible
curl https://YOUR-RENDER-URL.onrender.com/health

# Should return: {"status":"healthy"}
```

### Issue: "Database connection error"

**Check:**
1. DATABASE_URL in Render matches your Supabase connection string
2. Supabase project is not paused (visit Supabase dashboard)
3. Password is correct in DATABASE_URL

**Fix:**
- Copy DATABASE_URL from local `backend/.env` (where it works)
- Paste exact same value in Render environment variables

### Issue: "CORS policy: No 'Access-Control-Allow-Origin'"

**Fix:**
```bash
# In Render, update CORS_ORIGINS to include your Vercel URL:
CORS_ORIGINS=https://YOUR-VERCEL-URL.vercel.app,http://localhost:5173
```

### Issue: Render "Deploy Failed"

**Check build logs:**
1. Render Dashboard → Your Service → "Logs" tab
2. Look for error messages
3. Common issues:
   - Missing dependencies (check requirements.txt)
   - Python version mismatch
   - Missing environment variables

### Issue: Vercel "Build Failed"

**Check build logs:**
1. Vercel Dashboard → Your Project → Failed deployment
2. Common issues:
   - Missing VITE_API_URL
   - npm install failed (check package.json)
   - TypeScript errors (run `npm run build` locally first)

---

## 📊 Your Live URLs

Once deployed, bookmark these:

```
🌐 Frontend:     https://YOUR-VERCEL-URL.vercel.app
🔧 Backend API:  https://YOUR-RENDER-URL.onrender.com
📚 API Docs:     https://YOUR-RENDER-URL.onrender.com/docs
👤 Admin Login:  https://YOUR-VERCEL-URL.vercel.app/admin/login
💾 Database:     https://supabase.com/dashboard/project/dhmwuixxxsxkyfjdblqu
📂 GitHub:       https://github.com/ajiteshmanoj/campuseats
```

---

## 🔐 Post-Deployment Security

### 1. Change Admin Password
```bash
# Via Supabase Dashboard:
# Table Editor → users → Find admin user → Edit password field
# Or do it via your app's admin panel
```

### 2. Generate Strong SECRET_KEY
```bash
# Generate:
openssl rand -hex 32

# Update in Render environment variables
```

### 3. Protect .env Files
```bash
# Make sure these are in .gitignore:
backend/.env
frontend/.env

# Verify:
cat .gitignore | grep .env
```

---

## 💰 Cost Breakdown

**Total Monthly Cost: $0** 🎉

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| Vercel | Free | $0 | 100GB bandwidth, unlimited deployments |
| Render | Free | $0 | 750 hours/month, sleeps after 15min inactivity |
| Supabase | Free | $0 | 500MB database, 2GB file storage, auto-pauses after 7 days |

**Limitations:**
- Render free tier: First request after sleep takes ~30 seconds (cold start)
- Supabase free tier: Pauses after 7 days inactivity (restore with one click)

**To Upgrade (Optional):**
- Render Pro: $7/month (no sleeping)
- Supabase Pro: $25/month (no pausing)
- Vercel Pro: $20/month (more features, not needed)

---

## 🚦 Keeping Your App Alive

### Prevent Render from Sleeping
Render free tier sleeps after 15 minutes of inactivity.

**Option 1: Cron Job (Free)**
Use cron-job.org to ping your backend every 14 minutes:
```
URL: https://YOUR-RENDER-URL.onrender.com/health
Interval: Every 14 minutes
```

**Option 2: Uptime Monitor (Free)**
- UptimeRobot: https://uptimerobot.com
- Pingdom: Free tier
- Freshping: Free tier

**Option 3: Upgrade to Render Pro ($7/month)**
No sleeping, always instant response.

### Keep Supabase Active
Visit dashboard weekly or upgrade to Pro.

---

## 🔄 Future Updates

When you make code changes:

### Update Backend:
```bash
# Commit and push
git add .
git commit -m "Your update message"
git push origin main

# Render auto-deploys (if enabled) or Manual Deploy
```

### Update Frontend:
```bash
# Same - commit and push
git add .
git commit -m "Your update message"
git push origin main

# Vercel auto-deploys from main branch
```

**Auto-Deploy Setup:**
- Vercel: Already auto-deploys on push to main ✅
- Render: Enable in Settings → "Auto-Deploy: Yes"

---

## 📝 Quick Commands Cheat Sheet

```bash
# Push code to GitHub
git add .
git commit -m "Update"
git push origin main

# Test local backend
cd backend
python -m uvicorn app.main:app --reload

# Test local frontend
cd frontend
npm run dev

# Build frontend locally (test before deploy)
cd frontend
npm run build

# Test Supabase connection
cd backend
python diagnose_supabase.py

# Generate secure SECRET_KEY
openssl rand -hex 32
```

---

## ✅ Deployment Checklist

Before considering deployment complete:

- [ ] Code pushed to GitHub
- [ ] Backend deployed on Render
- [ ] Backend shows "Live ✅" status
- [ ] Backend /health endpoint returns 200
- [ ] Frontend deployed on Vercel
- [ ] Frontend loads without errors
- [ ] VITE_API_URL set in Vercel
- [ ] CORS_ORIGINS updated in Render
- [ ] Can login to app
- [ ] Can browse stalls
- [ ] Can view menu items
- [ ] Database connected (Supabase)
- [ ] SECRET_KEY changed from default
- [ ] .env files not in git

---

## 🆘 Need Help?

**Vercel Support:**
- Docs: https://vercel.com/docs
- Discord: https://vercel.com/discord

**Render Support:**
- Docs: https://render.com/docs
- Community: https://community.render.com

**Supabase Support:**
- Docs: https://supabase.com/docs
- Discord: https://discord.supabase.com
- Email: support@supabase.io

---

**Ready to deploy? Start with Step 1!** 🚀

After deployment, share your Vercel URL and your CampusEats app will be live on the web!
