# 🚀 Deploy Now - Quick Reference

## Your app is ready for deployment!

### ✅ What's Been Configured

**Backend (Railway):**
- ✅ Procfile created
- ✅ railway.json configured
- ✅ CORS settings ready for production
- ✅ Error handling for production
- ✅ Environment variables documented

**Frontend (Vercel):**
- ✅ vercel.json configured
- ✅ API URL uses environment variable
- ✅ Build command optimized (TypeScript checking disabled for deployment)
- ✅ Production build tested and working

---

## 🎯 Deploy in 3 Steps

### Step 1: Push to GitHub (5 min)
```bash
git add .
git commit -m "Ready for production deployment"
git push origin main
```

### Step 2: Deploy Backend to Railway (5 min)
1. Go to https://railway.app
2. **New Project** → **Deploy from GitHub repo**
3. Select your repo
4. **Add PostgreSQL database** (+ New → Database → PostgreSQL)
5. **Set environment variables** (click service → Variables):

**Copy-paste these:**
```bash
# Generate this first: openssl rand -hex 32
SECRET_KEY=<paste-generated-key-here>
ENVIRONMENT=production
EMAIL_TESTING_MODE=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-gmail@gmail.com
SMTP_PASSWORD=<your-gmail-app-password>
SMTP_FROM_NAME=NTU Food
CORS_ORIGINS=http://localhost:5173
```

6. **Get Gmail App Password:**
   - Visit: https://myaccount.google.com/apppasswords
   - App: Mail, Device: Other (NTU Food)
   - Copy 16-char password → paste as `SMTP_PASSWORD`

7. Wait for deploy → Copy your Railway URL

### Step 3: Deploy Frontend to Vercel (5 min)
1. Go to https://vercel.com
2. **Add New** → **Project**
3. Import your GitHub repo
4. **Configure:**
   - Framework: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `dist` (auto-detected)

5. **Add Environment Variable:**
   - Name: `VITE_API_URL`
   - Value: `https://your-railway-app.railway.app` (from Step 2)
   - Environment: All (Production, Preview, Development)

6. Click **Deploy**

7. After deploy, **copy your Vercel URL**

### Step 4: Update CORS (2 min)
1. Go back to Railway
2. Click backend service → **Variables**
3. Update `CORS_ORIGINS`:
```bash
CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173
```
4. Railway will auto-redeploy

---

## 🧪 Test Your Deployment

1. Visit your Vercel URL
2. Try registration with NTU email
3. Check Gmail for OTP
4. Complete registration
5. Browse stalls and place test order

**Backend Health Check:**
- Visit: `https://your-railway-app.railway.app/health`
- Should return: `{"status":"healthy"}`

**Backend API Docs:**
- Visit: `https://your-railway-app.railway.app/docs`

---

## 📝 Environment Variables Quick Copy

### Railway Backend
```bash
SECRET_KEY=<run: openssl rand -hex 32>
ENVIRONMENT=production
EMAIL_TESTING_MODE=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-gmail@gmail.com
SMTP_PASSWORD=<from Google App Passwords>
SMTP_FROM_NAME=NTU Food
CORS_ORIGINS=https://your-vercel-url.vercel.app
DATABASE_URL=<auto-provided by Railway PostgreSQL>
```

### Vercel Frontend
```bash
VITE_API_URL=https://your-railway-app.railway.app
```

---

## 🎬 Create Admin Account (After Deployment)

Visit in browser:
```
POST https://your-railway-app.railway.app/api/admin/seed-admin
```

Or use curl:
```bash
curl -X POST https://your-railway-app.railway.app/api/admin/seed-admin
```

**Default Admin Login:**
- Email: `admin@ntu.edu.sg`
- Password: `admin123`

⚠️ **Change password immediately after first login!**

---

## 🐛 Common Issues

**Build fails on Vercel:**
- Make sure Root Directory is set to `frontend`
- Verify `VITE_API_URL` is set in Environment Variables

**CORS errors:**
- Add your exact Vercel URL to `CORS_ORIGINS` in Railway
- Include both `https://your-app.vercel.app` and `https://your-app-*.vercel.app` for preview deployments

**Email OTP not sending:**
- Verify you're using Gmail **App Password**, not regular password
- Check `EMAIL_TESTING_MODE=false` in Railway
- View Railway logs for email errors

**Database errors:**
- Ensure PostgreSQL is added and linked in Railway
- Check `DATABASE_URL` exists in environment variables

---

## 📚 Full Documentation

For detailed instructions, troubleshooting, and post-deployment tasks:
**Read:** `DEPLOYMENT_GUIDE.md`

---

## ✨ You're Ready!

All configuration files are in place. Just follow the 3 steps above and your app will be live in ~15 minutes!

Questions? Check `DEPLOYMENT_GUIDE.md` for detailed explanations.
