# 🔧 Supabase Reconnection Guide - CampusEats App

**Problem:** You previously deployed to Supabase but can no longer access it.
**Solution:** This guide will help you reconnect to your existing Supabase project or set up a new one.

---

## 📊 Current Status Analysis

Based on your project files, here's what I found:

### ✅ Your Previous Supabase Configuration
- **Project ID:** `dhmwuixxxsxkyfjdblqu`
- **Region:** AWS Asia Pacific South 1 (Mumbai)
- **Database:** PostgreSQL via Supabase
- **Status:** Currently **DISCONNECTED** (using SQLite fallback)

### 📁 Files Found
- ✅ `backend/.env` - Has Supabase credentials (but commented out)
- ✅ `backend/supabase_migration.sql` - Complete database schema
- ✅ `backend/test_supabase_connection.py` - Connection testing script
- ✅ `backend/seed_supabase.py` - Data seeding script
- ✅ `SUPABASE_MIGRATION_GUIDE.md` - Original setup instructions

### 🔍 Current Database Setup
**File:** `backend/.env` (Line 8)
```env
DATABASE_URL=sqlite:///./campuseats.db  # ← Currently using local SQLite
```

**Previous Supabase URL (commented out):**
```env
# DATABASE_URL=postgresql://postgres.dhmwuixxxsxkyfjdblqu:Ajite$h0812@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
```

---

## 🎯 Reconnection Options

You have **TWO options**:

### Option A: Reconnect to Existing Supabase Project (Recommended if still active)
### Option B: Create New Supabase Project (If old project is deleted/expired)

---

## Option A: Reconnect to Existing Supabase Project

### Step 1: Check if Your Supabase Project Still Exists

1. **Go to Supabase Dashboard:**
   ```
   https://supabase.com/dashboard
   ```

2. **Sign in** with the account you used previously

3. **Look for your project:**
   - Project name might be: `campuseats` or similar
   - Project reference: `dhmwuixxxsxkyfjdblqu`

4. **Check project status:**
   - ✅ **Active:** Green indicator, can access
   - ⚠️ **Paused:** Yellow indicator (free tier pauses after 1 week inactivity)
   - ❌ **Deleted:** Project not in list

### Step 2: If Project is Paused - Restore It

Supabase free tier **pauses projects after 7 days of inactivity**.

1. **Click on your paused project**
2. Click **"Restore project"** or **"Unpause"**
3. Wait 1-2 minutes for restoration
4. Project will be active again!

### Step 3: Get Fresh Connection Credentials

Even if you have old credentials, get fresh ones to ensure they're valid:

1. **In Supabase Dashboard:**
   - Go to **Settings** (gear icon, bottom left)
   - Click **"Database"** in sidebar

2. **Get Connection String:**
   - Scroll to **"Connection string"** section
   - Select **"Connection Pooling"** tab (recommended for production)
   - Mode: **Transaction**
   - Copy the URI - looks like:
     ```
     postgresql://postgres.dhmwuixxxsxkyfjdblqu:[YOUR-PASSWORD]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
     ```

3. **Replace password:**
   - The `[YOUR-PASSWORD]` placeholder needs your actual password
   - **Don't remember password?** Click **"Reset database password"**
   - After reset, copy new password and update connection string

4. **Get Supabase API Keys:**
   - Go to **Settings** → **API**
   - Copy:
     - **Project URL:** `https://dhmwuixxxsxkyfjdblqu.supabase.co`
     - **anon public key:** Long JWT token (starts with `eyJ...`)

### Step 4: Update Backend .env File

1. **Open:** `backend/.env`

2. **Update these lines:**
   ```env
   # Change from SQLite to Supabase PostgreSQL
   DATABASE_URL=postgresql://postgres.dhmwuixxxsxkyfjdblqu:YOUR_ACTUAL_PASSWORD@aws-1-ap-south-1.pooler.supabase.com:6543/postgres

   # Verify these are correct
   SUPABASE_URL=https://dhmwuixxxsxkyfjdblqu.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...your-full-key...
   ```

3. **Important:**
   - Replace `YOUR_ACTUAL_PASSWORD` with your database password
   - If password has special characters ($, @, #), you may need to URL-encode them
   - Example: `Ajite$h0812` might need to be `Ajite%24h0812` ($ = %24)

### Step 5: Test Connection

```bash
cd backend
python test_supabase_connection.py
```

**Expected output if successful:**
```
============================================================
TESTING SUPABASE CONNECTION
============================================================

📋 Configuration:
   Database URL: postgresql://postgres.dhmwuixxxsxkyfjdblqu...
   Supabase URL: https://dhmwuixxxsxkyfjdblqu.supabase.co

🔌 Creating database engine...
🔗 Testing connection...
   ✓ Connected to PostgreSQL
   Version: PostgreSQL 15.x on x86_64-pc-linux-gnu...

📊 Checking tables...
   ✓ Found 7 tables:
      • menu_items
      • order_items
      • orders
      • otp_verifications
      • queue_entries
      • stalls
      • users

✅ CONNECTION TEST SUCCESSFUL!
```

**If connection fails:**
- ❌ Check password is correct (no typos, special chars encoded)
- ❌ Verify project is not paused
- ❌ Confirm DATABASE_URL format is exact
- ❌ Check internet connection

### Step 6: Verify Data Still Exists

1. **Check Supabase Dashboard:**
   - Go to **Table Editor**
   - Click on each table (users, stalls, menu_items, orders)
   - Verify your data is still there

2. **If tables are empty or missing:**
   - You'll need to re-run the migration and seeding (see below)

### Step 7: Start Backend with Supabase

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload --port 8000
```

**Check it works:**
- Visit: http://localhost:8000/docs
- Try: `GET /api/stalls` endpoint
- Should return data from Supabase

---

## Option B: Create New Supabase Project

If your old project is deleted or you want a fresh start:

### Step 1: Create New Supabase Project

1. **Go to:** https://supabase.com
2. **Sign in** or create account (100% free, no credit card)
3. Click **"New Project"**
4. Fill in:
   - **Name:** `campuseats-production` (or any name)
   - **Database Password:** Choose strong password (SAVE IT!)
   - **Region:** Singapore / Southeast Asia (closest to you)
5. Click **"Create new project"**
6. **Wait 2-3 minutes** for provisioning

### Step 2: Run Migration Script

1. **In Supabase Dashboard:**
   - Go to **SQL Editor** (left sidebar)
   - Click **"New Query"**

2. **Open migration file:**
   - On your computer: `backend/supabase_migration.sql`
   - Copy **entire contents** (423 lines)

3. **Paste and run:**
   - Paste into SQL Editor
   - Click **"RUN"** or press `Ctrl+Enter`
   - Should see: `Success. No rows returned`

4. **Verify tables created:**
   - Go to **Table Editor**
   - Should see 7 tables:
     - users
     - stalls
     - menu_items
     - orders
     - order_items
     - queue_entries
     - otp_verifications

### Step 3: Get New Connection Details

1. **Go to Settings → Database:**
   - Copy **Connection Pooling** URI:
     ```
     postgresql://postgres.NEW_PROJECT_REF:[PASSWORD]@aws-X-region.pooler.supabase.com:6543/postgres
     ```
   - Replace `[PASSWORD]` with your database password

2. **Go to Settings → API:**
   - Copy **Project URL**
   - Copy **anon public** key

### Step 4: Update .env File

```env
# backend/.env
DATABASE_URL=postgresql://postgres.NEW_PROJECT_REF:YOUR_PASSWORD@aws-X-region.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://NEW_PROJECT_REF.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...new-key...
```

### Step 5: Test Connection

```bash
cd backend
python test_supabase_connection.py
```

Should show successful connection with 7 tables (but 0 records).

### Step 6: Seed Database with Initial Data

```bash
python seed_supabase.py
```

**Expected output:**
```
============================================================
SEEDING SUPABASE DATABASE
============================================================

📝 Creating admin user...
   ✓ Admin user created

📝 Creating test student accounts...
   ✓ Created: Test Student (test.student@campuseats.com)
   ✓ Created: John Doe (john.doe@campuseats.com)
   ✓ Created: Jane Smith (jane.smith@campuseats.com)

📝 Creating food stalls...
   ✓ Created: Western Food Paradise
   ✓ Created: Hainanese Chicken Rice
   ✓ Created: Mala Xiang Guo

📝 Creating menu items...
   ✓ Created 15 menu items total

✅ DATABASE SEEDED SUCCESSFULLY!
```

### Step 7: Verify in Supabase Dashboard

- **Table Editor → users:** Should have 4 users
- **Table Editor → stalls:** Should have 3 stalls
- **Table Editor → menu_items:** Should have 15 items

### Step 8: Start Backend

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Test: http://localhost:8000/api/stalls (should return 3 stalls)

---

## 🐛 Troubleshooting Common Issues

### Issue 1: "Connection refused" or "Could not connect to database"

**Possible Causes:**
1. Project is paused (free tier pauses after 7 days inactivity)
2. Wrong password in DATABASE_URL
3. Network/firewall blocking connection
4. Supabase is down (rare)

**Solutions:**
```bash
# 1. Check Supabase status
https://status.supabase.com/

# 2. Verify project is active in dashboard
https://supabase.com/dashboard

# 3. Check DATABASE_URL format
# Should be: postgresql://postgres.PROJECT_REF:PASSWORD@...pooler.supabase.com:6543/postgres

# 4. Test with psql directly (if installed)
psql "postgresql://postgres.PROJECT_REF:PASSWORD@aws-X-region.pooler.supabase.com:6543/postgres"
```

### Issue 2: "psycopg2 not installed"

```bash
cd backend
pip install psycopg2-binary
```

### Issue 3: "Table does not exist"

**Solution:** Run migration script in Supabase SQL Editor
- File: `backend/supabase_migration.sql`
- Copy all → Paste in SQL Editor → Run

### Issue 4: "Authentication failed for user postgres"

**Causes:**
- Wrong password in DATABASE_URL
- Password contains special characters not URL-encoded

**Solution:**
```bash
# Reset password in Supabase Dashboard:
# Settings → Database → "Reset database password"

# Special character encoding:
# $ → %24
# @ → %40
# # → %23
# Example: "MyPass$123" becomes "MyPass%24123"
```

### Issue 5: Backend shows "Connection error" on startup

**Check .env file:**
```bash
cd backend
cat .env | grep DATABASE_URL
```

**Should see:**
```
DATABASE_URL=postgresql://postgres...
```

**NOT:**
```
DATABASE_URL=sqlite:///./campuseats.db  # ← Wrong!
```

### Issue 6: Supabase project deleted/can't find it

**Options:**
1. Check if you used a different email account
2. Check organization projects (if you were in a team)
3. Contact Supabase support (support@supabase.io)
4. **Best:** Just create a new project (takes 3 minutes)

---

## 🔒 Security Best Practices

### 1. Never Commit Database Password
```bash
# Make sure .env is in .gitignore
echo "backend/.env" >> .gitignore
git add .gitignore
git commit -m "Ensure .env is ignored"
```

### 2. Use Strong Database Password
- Minimum 16 characters
- Mix of letters, numbers, symbols
- Don't use personal info

### 3. Rotate Credentials Periodically
- Change database password every 90 days
- Regenerate API keys if exposed

### 4. Enable Row Level Security (RLS)
In Supabase Dashboard:
1. Go to **Table Editor**
2. For each table, click **"..." → Enable RLS**
3. Add policies for data access control

---

## 📊 Verify Everything Works

### Backend Connection Test
```bash
cd backend
python test_supabase_connection.py
```
✅ Should show: "CONNECTION TEST SUCCESSFUL"

### API Test
```bash
# Start backend
python -m uvicorn app.main:app --reload --port 8000

# Test in another terminal
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

curl http://localhost:8000/api/stalls
# Should return: array of stalls
```

### Frontend Test
```bash
# In another terminal
cd frontend
npm run dev

# Visit: http://localhost:5173
# Login with: admin@campuseats.com / admin123
```

---

## 📚 Quick Reference

### Your Supabase URLs
```
Dashboard:  https://supabase.com/dashboard/project/dhmwuixxxsxkyfjdblqu
Table Editor: https://supabase.com/dashboard/project/dhmwuixxxsxkyfjdblqu/editor
SQL Editor: https://supabase.com/dashboard/project/dhmwuixxxsxkyfjdblqu/sql
Settings:  https://supabase.com/dashboard/project/dhmwuixxxsxkyfjdblqu/settings/database
```

### Connection String Format
```
# Session mode (direct connection)
postgresql://postgres:[PASSWORD]@db.PROJECT_REF.supabase.co:5432/postgres

# Transaction mode (connection pooling - RECOMMENDED)
postgresql://postgres.PROJECT_REF:[PASSWORD]@aws-X-region.pooler.supabase.com:6543/postgres
```

### Test Accounts (after seeding)
```
Admin:
  Email: admin@campuseats.com
  Password: admin123

Student:
  Email: test.student@campuseats.com
  Password: testpassword123
```

### Important Files
```
backend/.env                      → Database credentials
backend/supabase_migration.sql    → Create tables
backend/seed_supabase.py          → Add initial data
backend/test_supabase_connection.py → Test connection
SUPABASE_MIGRATION_GUIDE.md       → Original setup guide
```

---

## 🚀 Next Steps After Reconnection

1. **Test All Features:**
   - [ ] Admin login works
   - [ ] Students can register with OTP
   - [ ] Browse stalls and menu
   - [ ] Place orders
   - [ ] Queue system works
   - [ ] Order tracking updates

2. **Enable Production Features:**
   - [ ] Set `EMAIL_TESTING_MODE=false` for real OTP emails
   - [ ] Configure SMTP or Supabase Auth for emails
   - [ ] Add Row Level Security policies
   - [ ] Set up database backups (automatic in Supabase)

3. **Deploy to Production:**
   - [ ] Deploy backend to Render.com (see DEPLOYMENT_GUIDE.md)
   - [ ] Deploy frontend to Vercel
   - [ ] Update CORS_ORIGINS with production URLs
   - [ ] Change SECRET_KEY to secure random string

4. **Monitor Performance:**
   - Check Supabase Dashboard → Reports
   - Monitor API response times
   - Review database query performance

---

## 💡 Tips for Avoiding Future Issues

### Keep Project Active
Supabase free tier pauses after **7 days of no activity**. To prevent:
- Visit dashboard weekly
- Set up cron job to ping database
- Upgrade to Pro tier ($25/month for always-on)

### Backup Regularly
```bash
# Export data
pg_dump "postgresql://postgres:PASSWORD@..." > backup.sql

# Or use Supabase Dashboard → Database → Backups
```

### Document Changes
Keep notes in `DEPLOYMENT_LOG.md`:
```
2025-11-13: Reconnected to Supabase project dhmwuixxxsxkyfjdblqu
2025-11-13: Updated DATABASE_URL in .env
2025-11-13: Tested connection - all tables present
```

---

## 🆘 Still Having Issues?

### 1. Check Logs
```bash
# Backend logs
python -m uvicorn app.main:app --reload --log-level debug

# Supabase logs
Dashboard → Logs → Postgres Logs
```

### 2. Verify Environment
```bash
cd backend
python -c "from app.config import settings; print(settings.DATABASE_URL)"
# Should show: postgresql://postgres...
# NOT: sqlite:///...
```

### 3. Test Minimal Connection
```python
# test_minimal.py
from sqlalchemy import create_engine, text

DB_URL = "postgresql://postgres.PROJECT_REF:PASSWORD@..."
engine = create_engine(DB_URL)
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("✅ Connected!", result.fetchone())
```

### 4. Contact Support
- **Supabase Support:** support@supabase.io
- **Supabase Discord:** https://discord.supabase.com
- **GitHub Issues:** Check if it's a known issue

---

## ✅ Success Checklist

Before considering reconnection complete, verify:

- [ ] Can access Supabase dashboard
- [ ] Project is active (not paused)
- [ ] All 7 tables exist in database
- [ ] `test_supabase_connection.py` passes
- [ ] Backend starts without errors
- [ ] Can fetch stalls via API
- [ ] Frontend can login
- [ ] Can create orders successfully
- [ ] Data persists in Supabase (check Table Editor)

---

**Last Updated:** 2025-11-13
**Your Supabase Project ID:** dhmwuixxxsxkyfjdblqu
**Status:** Ready to reconnect!

---

Good luck! Once you're reconnected, your app will be back on cloud infrastructure with automatic backups and scalability! 🎉
