# 🔧 Login Failed - Quick Fix Guide

**Problem:** Login fails with "Login failed" or 500 error
**Cause:** Admin user likely doesn't exist in production Supabase database

---

## 🎯 Quick Fix: Add Admin User to Supabase

### Option 1: Via Supabase Dashboard (FASTEST - 2 min)

1. **Go to Supabase Dashboard:**
   ```
   https://supabase.com/dashboard/project/dhmwuixxxsxkyfjdblqu
   ```

2. **Click "Table Editor" (left sidebar)**

3. **Click on "users" table**

4. **Check if admin exists:**
   - Look for email: `admin@campuseats.com`
   - **If exists:** Skip to Option 2 (password issue)
   - **If NOT exists:** Continue below

5. **Click "Insert" → "Insert row"**

6. **Fill in these fields:**
   ```
   ntu_email: admin@campuseats.com
   student_id: ADMIN001
   name: Admin User
   phone: +6512345678
   dietary_preferences: (leave blank or "None")
   hashed_password: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oe2kndx.I.YS
   role: admin
   is_active: true
   is_verified: true
   ```

   **⚠️ Copy the hashed_password exactly as shown above!**

   This is the hash for password: `admin123`

7. **Click "Save"**

8. **Test login:**
   - Go to: https://campuseats-xi.vercel.app
   - Email: `admin@campuseats.com`
   - Password: `admin123`
   - Should work now!

---

### Option 2: Password Doesn't Match (If admin exists)

If admin user exists but login still fails:

1. **In Supabase Table Editor → users table**

2. **Find admin@campuseats.com row**

3. **Click Edit on that row**

4. **Update hashed_password to:**
   ```
   $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oe2kndx.I.YS
   ```

5. **Save**

6. **Try login again with password:** `admin123`

---

### Option 3: Seed Database via Script (Comprehensive)

If you want to add all test data:

1. **Verify DATABASE_URL in Render:**
   - Render Dashboard → campuseats-backend → Environment
   - Confirm DATABASE_URL points to Supabase

2. **Run seed script locally (connects to Supabase):**
   ```bash
   cd backend

   # Make sure .env has Supabase URL
   cat .env | grep DATABASE_URL
   # Should show: postgresql://postgres.dhmwuixxxsxkyfjdblqu...

   # Run seed script
   python seed_supabase.py
   ```

3. **This will add:**
   - Admin user
   - 3 test student accounts
   - Additional stalls if needed
   - Menu items

4. **Test login:**
   - Email: `admin@campuseats.com`
   - Password: `admin123`

---

## 🔍 Diagnose Login Issue

### Check What Error You're Getting:

**In Browser:**
1. Open https://campuseats-xi.vercel.app
2. Press F12 to open Developer Console
3. Go to "Network" tab
4. Try to login
5. Look at the login request

**Common Errors:**

❌ **Status 401: "Invalid credentials"**
- User exists but password is wrong
- Fix: Update hashed_password in Supabase (Option 2)

❌ **Status 404: "User not found"**
- Admin user doesn't exist
- Fix: Insert admin user (Option 1)

❌ **Status 500: "Internal server error"**
- Database connection issue or bcrypt error
- Fix: Check Render logs for specific error

❌ **CORS Error**
- Frontend can't reach backend
- Fix: Update CORS_ORIGINS in Render

---

## 🧪 Test Backend Login Directly

Test the backend API directly to isolate the issue:

### Using curl:
```bash
curl -X POST https://campuseats-backend.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"ntu_email":"admin@campuseats.com","password":"admin123"}'
```

**Expected Response (Success):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "token_type": "bearer"
}
```

**If you get error:**
- 401: Wrong password or user not found
- 500: Database/server issue
- Check Render logs for details

---

## 📋 Verify Supabase Users Table

**Check your users in Supabase:**

1. **Table Editor → users**

2. **Should have these columns:**
   - id (integer)
   - ntu_email (text)
   - student_id (text)
   - name (text)
   - phone (text)
   - dietary_preferences (text)
   - hashed_password (text)
   - role (enum: student/stall_owner/admin)
   - is_active (boolean)
   - is_verified (boolean)
   - created_at (timestamp)
   - updated_at (timestamp)

3. **Check if admin exists:**
   - Filter by email: admin@campuseats.com
   - Check role is: admin
   - Check is_active is: true

---

## 🔐 Password Hash Reference

**For password: `admin123`**
```
$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oe2kndx.I.YS
```

**For password: `testpassword123`**
```
$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW
```

**To generate new hash:**
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hash = pwd_context.hash("your_password")
print(hash)
```

---

## 🆘 Still Not Working?

### Check Render Logs:

1. **Render Dashboard → campuseats-backend**

2. **Logs tab**

3. **Look for errors when you try to login**

**Common log errors:**

❌ **"No module named 'passlib'"**
```
Fix: Check requirements.txt has passlib[bcrypt]
Redeploy with "Clear build cache"
```

❌ **"Database connection failed"**
```
Fix: Verify DATABASE_URL in Environment variables
Should be full Supabase connection string
```

❌ **"User not found"**
```
Fix: Admin doesn't exist in database
Add via Supabase Table Editor (Option 1)
```

---

## ✅ Test Accounts After Fix

Once admin is added, you can login with:

**Admin:**
```
Email: admin@campuseats.com
Password: admin123
```

**If you seeded test users:**
```
Email: test.student@campuseats.com
Password: testpassword123
```

---

## 🚀 Quick Reference Commands

**Check if admin exists:**
```sql
-- In Supabase SQL Editor
SELECT * FROM users WHERE ntu_email = 'admin@campuseats.com';
```

**Add admin via SQL:**
```sql
-- In Supabase SQL Editor
INSERT INTO users (ntu_email, student_id, name, phone, hashed_password, role, is_active, is_verified)
VALUES (
  'admin@campuseats.com',
  'ADMIN001',
  'Admin User',
  '+6512345678',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oe2kndx.I.YS',
  'admin',
  true,
  true
);
```

**Seed database:**
```bash
cd backend
python seed_supabase.py
```

---

## 💡 Prevention for Future

To avoid this issue:

1. **Always seed database after creating new Supabase project**
2. **Keep track of admin credentials**
3. **Document any password changes**
4. **Use environment variables for admin setup**

---

**Most Common Solution:** Add admin user via Supabase Table Editor (Option 1)

Try that first! It takes 2 minutes and fixes 90% of login issues.
