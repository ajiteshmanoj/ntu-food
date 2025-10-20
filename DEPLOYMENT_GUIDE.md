# NTU Food - Production Deployment Guide

## Quick Start: Deploy in 15 Minutes

### Prerequisites
- GitHub account (for code hosting)
- Railway account (backend hosting) - https://railway.app
- Vercel account (frontend hosting) - https://vercel.com
- Gmail account with App Password (for email OTP)

---

## Part 1: Deploy Backend to Railway (10 minutes)

### Step 1: Push Code to GitHub
```bash
# If not already a git repo, initialize
git init
git add .
git commit -m "Initial commit - ready for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/ntu-food.git
git branch -M main
git push -u origin main
```

### Step 2: Create Railway Project
1. Go to https://railway.app and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Select your `ntu-food` repository
5. Railway will detect the backend automatically

### Step 3: Add PostgreSQL Database
1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway will automatically create and link the database
4. The `DATABASE_URL` environment variable is set automatically

### Step 4: Configure Environment Variables
1. Click on your backend service
2. Go to **"Variables"** tab
3. Add these environment variables:

```
SECRET_KEY=<generate using: openssl rand -hex 32>
ENVIRONMENT=production
EMAIL_TESTING_MODE=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-gmail@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM_NAME=NTU Food
CORS_ORIGINS=http://localhost:5173
```

**Note:** You'll update `CORS_ORIGINS` with your Vercel URL after frontend deployment.

### Step 5: Generate Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select app: **"Mail"**, device: **"Other"** (enter "NTU Food")
3. Copy the 16-character password
4. Add it to Railway as `SMTP_PASSWORD`

### Step 6: Deploy
1. Railway will automatically deploy when you push to GitHub
2. Wait for deployment to complete (2-3 minutes)
3. Click **"Settings"** → Copy your **Railway URL** (e.g., `https://your-app.railway.app`)
4. Test: Visit `https://your-app.railway.app/health` - should return `{"status":"healthy"}`

---

## Part 2: Deploy Frontend to Vercel (5 minutes)

### Step 1: Disable TypeScript Strict Mode (Temporary)
Edit `frontend/tsconfig.json`:
```json
{
  "compilerOptions": {
    "skipLibCheck": true,
    "noEmit": false
  }
}
```

Or use `vercel.json` build override (already configured in your project).

### Step 2: Create Vercel Project
1. Go to https://vercel.com and sign in
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository
4. Configure build settings:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

### Step 3: Add Environment Variable
1. Before deploying, go to **"Environment Variables"**
2. Add:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://your-railway-app.railway.app` (your Railway backend URL)
   - **Environment:** Production, Preview, Development (all selected)

### Step 4: Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes for build and deployment
3. Copy your Vercel URL (e.g., `https://ntu-food.vercel.app`)

---

## Part 3: Update CORS Settings

### Update Railway Backend
1. Go to your Railway project
2. Click on backend service → **"Variables"**
3. Update `CORS_ORIGINS`:
```
CORS_ORIGINS=https://ntu-food.vercel.app,https://your-preview.vercel.app
```
4. Railway will auto-redeploy

---

## Part 4: Verify Deployment

### Test Backend
1. Visit: `https://your-railway-app.railway.app/health`
   - Should return: `{"status":"healthy"}`
2. Visit: `https://your-railway-app.railway.app/docs`
   - Should show API documentation

### Test Frontend
1. Visit your Vercel URL
2. Try to register with your NTU email
3. Check Gmail for OTP code
4. Complete registration and test ordering flow

---

## Environment Variables Cheatsheet

### Railway Backend (Required)
```bash
# Auto-provided by Railway
DATABASE_URL=<provided by Railway PostgreSQL>

# You must set these:
SECRET_KEY=<32+ character random string>
ENVIRONMENT=production
CORS_ORIGINS=<your-vercel-url>
SMTP_EMAIL=<your-gmail>
SMTP_PASSWORD=<gmail-app-password>
EMAIL_TESTING_MODE=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_FROM_NAME=NTU Food
```

### Vercel Frontend (Required)
```bash
VITE_API_URL=<your-railway-backend-url>
```

---

## Troubleshooting

### Backend won't start
- Check Railway logs: Click service → "Deployments" → Latest deployment → "View Logs"
- Verify all environment variables are set
- Ensure PostgreSQL database is connected

### Frontend build fails
- Check Vercel build logs
- Verify `VITE_API_URL` is set in environment variables
- Check that root directory is set to `frontend`

### CORS errors
- Ensure Vercel URL is added to `CORS_ORIGINS` in Railway
- Include both production and preview URLs
- Redeploy backend after CORS changes

### Email OTP not working
- Verify Gmail App Password (not regular password)
- Check `EMAIL_TESTING_MODE=false` in Railway
- Verify SMTP settings are correct
- Check Railway logs for email errors

### Database connection errors
- Ensure PostgreSQL database is linked in Railway
- Check `DATABASE_URL` is automatically set
- Verify database is running in Railway dashboard

---

## Post-Deployment Tasks

### 1. Set Up Custom Domain (Optional)
**Vercel:**
- Go to project settings → "Domains"
- Add your custom domain

**Railway:**
- Go to service settings → "Networking"
- Add custom domain

### 2. Monitor Logs
- **Railway:** Service → Deployments → View Logs
- **Vercel:** Deployments → View Function Logs

### 3. Set Up Continuous Deployment
Both platforms auto-deploy on git push to main:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### 4. Create Admin Account
After deployment, seed admin:
```bash
# Visit in browser or use curl
POST https://your-railway-app.railway.app/api/admin/seed-admin
```

Default admin credentials:
- Email: `admin@ntu.edu.sg`
- Password: `admin123`
- **⚠️ Change this immediately after first login!**

---

## Production Checklist

- [ ] Backend deployed to Railway
- [ ] PostgreSQL database connected
- [ ] All environment variables set in Railway
- [ ] Gmail App Password configured
- [ ] Backend health check returns 200
- [ ] Frontend deployed to Vercel
- [ ] `VITE_API_URL` set in Vercel
- [ ] CORS origins updated with Vercel URL
- [ ] Registration with OTP email works
- [ ] Login works
- [ ] Can browse stalls and menu
- [ ] Can place an order
- [ ] Admin panel accessible
- [ ] Stall owner dashboard works

---

## Quick Commands Reference

### Generate Secret Key
```bash
openssl rand -hex 32
```

### Test Backend Locally
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### Test Frontend Locally
```bash
cd frontend
npm run dev
```

### Build Frontend
```bash
cd frontend
npm run build
npm run preview  # Test production build locally
```

---

## Support

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Vite Docs: https://vitejs.dev

---

**You're all set! 🚀**

Your NTU Food app is now live in production. Share your Vercel URL with users to start taking orders!
