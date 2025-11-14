# ⚡ Quick Gmail SMTP Setup (5 Minutes)

## Step 1: Get Gmail App Password (2 minutes)

1. **Go to:** https://myaccount.google.com/apppasswords
2. **Sign in** with your Gmail account (`ntufoodapp@gmail.com`)
3. **Click:** "Select app" → Choose "Mail"
4. **Click:** "Select device" → Choose "Other (Custom name)"
5. **Type:** `CampusEats Backend`
6. **Click:** "Generate"
7. **Copy the 16-character password:**
   ```
   Example shown: abcd efgh ijkl mnop
   Copy as: abcdefghijklmnop  (NO SPACES!)
   ```
8. **Save it securely** - you can't view it again!

**Can't find App Passwords?**
- Enable 2-Step Verification first: https://myaccount.google.com/security
- Then visit app passwords link again

---

## Step 2: Add to Render (2 minutes)

1. **Go to:** https://render.com/dashboard
2. **Click your backend service**
3. **Click "Environment" tab**
4. **Add these variables:**

```bash
EMAIL_TESTING_MODE = false
SMTP_HOST = smtp.gmail.com
SMTP_PORT = 587
SMTP_EMAIL = ntufoodapp@gmail.com
SMTP_PASSWORD = abcdefghijklmnop  # Your 16-char password (NO SPACES!)
SMTP_FROM_NAME = CampusEats
APP_URL = https://your-app.vercel.app  # Your frontend URL
```

5. **Click "Save Changes"**
6. **Wait 1-2 minutes** for Render to redeploy

---

## Step 3: Test (1 minute)

1. **Go to your app:** `https://your-app.vercel.app/register`
2. **Register with a REAL email** you can access
3. **Check your inbox** for OTP email (check spam too!)
4. **Enter OTP** to complete registration

---

## ✅ Success Checklist

- [ ] Got 16-character Gmail App Password
- [ ] Added all variables to Render
- [ ] `EMAIL_TESTING_MODE` is `false` (not `true`)
- [ ] No spaces in `SMTP_PASSWORD`
- [ ] Render redeployed successfully
- [ ] Test email arrived in inbox
- [ ] OTP code is visible in email
- [ ] Registration completed successfully

---

## 🐛 Troubleshooting

**Email not arriving?**
1. Check spam folder
2. Wait 1-2 minutes (Gmail can be slow)
3. Try a different email address

**"SMTP Authentication Failed"?**
1. Regenerate app password
2. Copy carefully (no spaces!)
3. Verify 2-Step Verification is enabled

**Still not working?**
- See full guide: `GMAIL_SMTP_PRODUCTION_SETUP.md`
- Test locally: `python backend/test_smtp_connection.py`

---

## 📧 What Users Will Receive

**From:** CampusEats <ntufoodapp@gmail.com>
**Subject:** CampusEats - Your Verification Code

```
🍽️ CampusEats
Verify Your Email Address

Hello [Name],

Your verification code:
┌─────────┐
│ 123456  │
└─────────┘

Expires in 10 minutes
```

---

**That's it! 🎉 Your CampusEats app will now send real OTP emails!**
