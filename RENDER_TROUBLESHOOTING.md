# 🔧 Render "Not Found" - Troubleshooting Guide

**Problem:** Backend shows "Not Found" when visiting Render URL
**Common Causes:** Build command issues, start command problems, or missing environment variables

---

## 🎯 Quick Fixes (Try These First)

### Fix #1: Check Render Build & Start Commands

The issue is likely in your Render service configuration.

**Correct Configuration:**

1. **Go to Render Dashboard** → Your Service

2. **Settings → Build & Deploy:**
   ```
   Build Command:
   pip install -r backend/requirements.txt

   Start Command:
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **IMPORTANT:** Check "Root Directory" setting:
   - Should be: **BLANK** or **/** (leave empty)
   - NOT: `backend` (this causes double path issues)

---

### Fix #2: Verify Environment Variables

**Go to Environment tab and ensure these are set:**

**Critical (Must Have):**
```bash
DATABASE_URL=postgresql://postgres.dhmwuixxxsxkyfjdblqu:Ajite$h0812@aws-1-ap-south-1.pooler.supabase.com:6543/postgres

ENVIRONMENT=production

CORS_ORIGINS=http://localhost:5173,https://your-vercel-url.vercel.app
```

**Important:**
```bash
SECRET_KEY=your-super-secret-key-change-this-in-production-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Optional (for email OTP):**
```bash
EMAIL_TESTING_MODE=false
SMTP_EMAIL=ntufoodapp@gmail.com
SMTP_PASSWORD=zjrcmdheyeopdlwy
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

---

### Fix #3: Check Logs

**Render Dashboard → Your Service → Logs tab**

Look for these errors:

**Error: "No module named 'app'"**
- Fix: Root directory should be blank, not `backend`

**Error: "Database connection failed"**
- Fix: Check DATABASE_URL is set correctly

**Error: "Port already in use"**
- Fix: Make sure start command uses `$PORT` not hardcoded port

**Error: "Module not found: fastapi"**
- Fix: Check build command ran successfully

---

## 🔍 Detailed Diagnosis

### Step 1: Check Service Configuration

**Render Dashboard → Your Service → Settings**

Should look like this:

| Setting | Value |
|---------|-------|
| **Name** | campuseats-backend (or similar) |
| **Region** | Singapore / Oregon |
| **Branch** | main |
| **Root Directory** | *(leave blank)* |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free |

---

### Step 2: Review Build Logs

**Go to:** Events → Latest Deploy → View Logs

**Successful build should show:**
```
==> Cloning from https://github.com/ajiteshmanoj/campuseats...
==> Checking out commit 87d57e3...
==> Running build command 'pip install -r backend/requirements.txt'...
    Collecting fastapi
    Collecting uvicorn[standard]
    Collecting sqlalchemy
    ...
    Successfully installed ...
==> Build succeeded 🎉
==> Deploying...
```

**If build fails:**
- Error shows which package failed
- Check `backend/requirements.txt` has correct package names
- Verify Python version compatibility

---

### Step 3: Review Deploy Logs

**Go to:** Logs tab (live logs)

**Successful start should show:**
```
Starting service...
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

**Common errors:**

❌ **"FileNotFoundError: [Errno 2] No such file or directory: 'backend'"**
```
Problem: Root directory is set to "backend" already
Fix: Settings → Root Directory → Make it blank
```

❌ **"ModuleNotFoundError: No module named 'app'"**
```
Problem: Wrong directory structure or root dir issue
Fix: Ensure start command has "cd backend &&" prefix
```

❌ **"Database connection error"**
```
Problem: DATABASE_URL not set or wrong
Fix: Environment → Add DATABASE_URL with full Supabase connection string
```

---

## 🛠️ Manual Configuration Steps

If render.yaml isn't working, configure manually:

### Step-by-Step Manual Setup:

1. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect GitHub → Select `ajiteshmanoj/campuseats`

2. **Configure Basic Settings:**
   ```
   Name: campuseats-backend
   Region: Singapore (or closest)
   Branch: main
   Root Directory: (leave BLANK!)
   Runtime: Python 3
   ```

3. **Build Command:**
   ```
   pip install -r backend/requirements.txt
   ```

4. **Start Command:**
   ```
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Add Environment Variables:**
   Click "Add Environment Variable" for each:

   ```
   DATABASE_URL = postgresql://postgres.dhmwuixxxsxkyfjdblqu:Ajite$h0812@aws-1-ap-south-1.pooler.supabase.com:6543/postgres

   ENVIRONMENT = production

   CORS_ORIGINS = http://localhost:5173

   SECRET_KEY = your-super-secret-key-change-this-minimum-32-chars

   ALGORITHM = HS256

   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   ```

6. **Create Web Service**

7. **Wait for deploy** (2-3 minutes)

8. **Test:** Visit `https://your-service.onrender.com/health`

---

## 🧪 Testing Your Backend

### Test 1: Health Check
```bash
curl https://YOUR-SERVICE.onrender.com/health
```

**Expected Response:**
```json
{"status":"healthy"}
```

**If you get "Not Found":**
- Service isn't running
- URL is wrong
- Start command failed

---

### Test 2: API Root
```bash
curl https://YOUR-SERVICE.onrender.com/
```

**Expected Response:**
```json
{
  "message": "Welcome to CampusEats API",
  "version": "0.1.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

---

### Test 3: API Documentation
Visit: `https://YOUR-SERVICE.onrender.com/docs`

**Should see:**
- FastAPI Swagger UI
- List of all endpoints
- Interactive "Try it out" buttons

**If you get "Not Found":**
- Backend isn't starting properly
- Check logs for errors

---

### Test 4: Database Connection
```bash
curl https://YOUR-SERVICE.onrender.com/api/stalls
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "name": "North Spine Food Court",
    ...
  },
  ...
]
```

**If error:**
- DATABASE_URL not set
- Supabase connection issue
- Check logs for database errors

---

## 🔧 Common Issues & Solutions

### Issue 1: "Application failed to respond"

**Cause:** Start command is wrong or app crashed on startup

**Check:**
1. Logs show any Python errors?
2. Is `$PORT` being used in start command?
3. Did build command complete successfully?

**Solution:**
```bash
# Start command MUST use $PORT variable:
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT

# NOT hardcoded port:
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000  # WRONG!
```

---

### Issue 2: "This site can't be reached"

**Cause:** Service isn't deployed or URL is wrong

**Check:**
1. Render Dashboard shows "Live" with green checkmark?
2. URL is correct? (Copy from Render dashboard)
3. Service isn't still building?

**Solution:**
- Wait for deploy to complete
- Check Events tab for errors
- Try manual deploy: "Manual Deploy" → "Clear build cache & deploy"

---

### Issue 3: Works locally but not on Render

**Cause:** Environment differences or missing env vars

**Common issues:**
1. **Database URL:** Using SQLite locally but PostgreSQL on Render
   - Fix: Set DATABASE_URL in Render environment

2. **Port:** Using hardcoded port 8000 locally
   - Fix: Use `$PORT` in start command

3. **Dependencies:** Missing packages in requirements.txt
   - Fix: Add all packages to `backend/requirements.txt`

---

### Issue 4: "502 Bad Gateway"

**Cause:** App crashed or can't bind to port

**Check logs for:**
- Python exceptions
- Database connection errors
- Import errors

**Solution:**
1. Check all environment variables are set
2. Verify DATABASE_URL is correct
3. Look for specific error in logs
4. Try manual deploy with cleared cache

---

## 🎯 The Nuclear Option: Start Fresh

If nothing works, delete and recreate:

1. **Delete Existing Service:**
   - Render Dashboard → Your Service
   - Settings → Delete Service

2. **Create New Service Manually:**
   - Follow "Manual Configuration Steps" above
   - Don't use render.yaml
   - Set everything manually in UI

3. **Advantages:**
   - Fresh start, no cached issues
   - Can verify each setting
   - See errors immediately

---

## 📋 Pre-Deploy Checklist

Before deploying, verify locally:

```bash
# Test build locally
cd backend
pip install -r requirements.txt

# Test database connection
python diagnose_supabase.py
# Should show: ✅ CONNECTION TEST SUCCESSFUL!

# Test server locally
uvicorn app.main:app --reload --port 8000

# In another terminal, test:
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

curl http://localhost:8000/api/stalls
# Should return: array of stalls
```

**If ANY of these fail locally, fix before deploying!**

---

## 🆘 Still Not Working?

### Get Help from Render:

1. **Check Render Status:**
   https://status.render.com
   (Sometimes Render has outages)

2. **Render Community:**
   https://community.render.com
   Search for similar issues

3. **Contact Support:**
   - Render Dashboard → Help → Contact Support
   - Include: Service URL, logs, error messages

---

## 📸 What Success Looks Like

**Render Dashboard:**
```
✅ Live                Status: Deployed
   Last updated: Just now
   Deploy time: 2m 34s
```

**Logs:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
CampusEats API started in production mode
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

**Browser Test:**
- `https://your-service.onrender.com/health` → {"status":"healthy"}
- `https://your-service.onrender.com/docs` → FastAPI docs page
- `https://your-service.onrender.com/api/stalls` → JSON array

---

## 💡 Pro Tips

1. **Always check logs first** - They tell you exactly what's wrong

2. **Test the health endpoint** - If /health doesn't work, nothing will

3. **Verify environment variables** - 90% of issues are missing DATABASE_URL

4. **Use Manual Deploy** - After changing env vars, trigger manual deploy

5. **Clear build cache** - If stuck, "Manual Deploy" → "Clear build cache & deploy"

---

**Still stuck? Share:**
1. Your Render URL
2. Screenshot of logs
3. Build command from settings
4. Start command from settings

And I can help diagnose further!
