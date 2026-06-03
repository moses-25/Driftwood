# 📋 Pre-Deployment Checklist

## Security & Configuration

### Backend (Server)
- [x] ✅ SECRET_KEY updated to secure random value
- [x] ✅ JWT_SECRET_KEY updated to secure random value
- [x] ✅ Python version pinned to 3.11.9
- [x] ✅ Pillow updated to compatible version
- [ ] 🔧 DATABASE_URL configured for production
- [ ] 🔧 CLIENT_ORIGIN updated to production frontend URL
- [ ] 🔧 APP_URL updated to production backend URL
- [ ] 🔧 M-Pesa credentials switched to production
- [ ] 🔧 MPESA_CALLBACK_URL points to production backend
- [ ] 🔧 Email credentials verified (Gmail App Password)
- [x] ✅ `.env` file in `.gitignore`
- [x] ✅ Gunicorn configured for production

### Frontend (Client)
- [ ] 🔧 VITE_API_URL updated to production backend URL
- [x] ✅ Build process tested (`npm run build`)
- [x] ✅ Deployment config created (vercel.json/netlify.toml)

---

## ✅ **FIXES APPLIED FOR YOUR ERROR:**

### Problem: Build Failed with Pillow/Python 3.14
**Root Cause:** Render was using Python 3.14.3 which is incompatible with Pillow 10.2.0

**Fixed:**
1. ✅ Updated `runtime.txt` to use Python 3.11.9 (stable version)
2. ✅ Updated Pillow from 10.2.0 to 10.3.0 (compatible with Python 3.11)
3. ✅ Pushed changes to GitHub

---

## 🚀 **Next Steps:**

### 1. Redeploy on Render
Your code has been updated and pushed to GitHub. Now:

1. **Go to Render Dashboard**
2. **Find your `driftwood-backend` service**
3. **Click "Manual Deploy"** → **"Clear build cache & deploy"**
4. **Wait for rebuild** (should succeed now!)

### 2. Monitor the Build
Watch for these success messages:
```
✓ Using Python version 3.11.9
✓ Installing dependencies...
✓ Successfully installed Flask-3.0.0 Pillow-10.3.0 ...
✓ Starting service with gunicorn...
✓ Build successful!
```

---

## Platform Setup

### Database
- [ ] PostgreSQL database created on Render
- [ ] Database connection string obtained
- [ ] Database migrations ready to run
- [ ] Seed data script prepared (if needed)

### Backend Hosting
- [ ] Render service created
- [ ] Environment variables set (see RENDER_DEPLOYMENT_GUIDE.md)
- [ ] Build succeeds without errors
- [ ] Service is "Live" (green status)

### Frontend Hosting
- [ ] Vercel project imported
- [ ] Build configured with `client` root directory
- [ ] VITE_API_URL environment variable set

---

## External Services

### M-Pesa (Safaricom Daraja)
- [ ] Sandbox credentials working
- [ ] Production app created (when ready)
- [ ] Callback URL registered in Daraja portal

### Email Service
- [ ] Gmail App Password generated
- [ ] SMTP credentials verified
- [ ] Test email sent successfully

---

## Testing

### Pre-Deployment
- [x] ✅ Client builds successfully locally
- [x] ✅ Server dependencies compatible
- [ ] Database migrations run successfully
- [ ] All API endpoints tested
- [ ] Payment flow tested in sandbox

### Post-Deployment
- [ ] Frontend loads without errors
- [ ] API endpoints respond correctly
- [ ] CORS configured properly (no console errors)
- [ ] Menu items load from database
- [ ] Cart functionality works
- [ ] Checkout process completes
- [ ] M-Pesa payment initiated successfully
- [ ] Payment callback received
- [ ] Order stored in database
- [ ] Confirmation email sent

---

## Environment Variables Summary

### Must Configure for Backend (in Render dashboard)
```bash
✅ SECRET_KEY                 # Already set in .env
✅ JWT_SECRET_KEY              # Already set in .env
🔧 DATABASE_URL                # Copy from Render PostgreSQL
🔧 CLIENT_ORIGIN               # Your Vercel frontend URL
🔧 APP_URL                     # Your Render backend URL
🔧 MPESA_CONSUMER_KEY          # From your .env
🔧 MPESA_CONSUMER_SECRET       # From your .env
🔧 MPESA_SHORTCODE             # From your .env
🔧 MPESA_PASSKEY               # From your .env
🔧 MPESA_CALLBACK_URL          # Your backend + /api/payment/mpesa/callback
🔧 RESEND_API_KEY              # From your .env
🔧 OWNER_EMAIL                 # From your .env
🔧 MAIL_USERNAME               # From your .env
🔧 MAIL_PASSWORD               # From your .env
```

### Must Configure for Frontend (in Vercel)
```bash
🔧 VITE_API_URL                # Your Render backend URL
```

---

## Troubleshooting Your Build Error

### ✅ What was fixed:
```
Error: Failed to build 'Pillow' when getting requirements to build wheel
Cause: Python 3.14.3 is too new and incompatible with Pillow 10.2.0
Fix:  Pinned Python to 3.11.9 and upgraded Pillow to 10.3.0
```

### If build still fails:
1. **Clear build cache** in Render (Manual Deploy → Clear build cache)
2. **Check logs** for specific error message
3. **Verify branch** is set to `backup` in Render settings
4. **Check root directory** is set to `server`

---

## Quick Reference

### Files Updated:
- `server/runtime.txt` → Python 3.11.9
- `server/requirements.txt` → Pillow 10.3.0
- Pushed to GitHub backup branch ✅

### Render Configuration:
- Branch: `backup`
- Root Directory: `server`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 4 wsgi:application`

---

## Legend
- ✅ = Completed / Already configured
- 🔧 = Needs configuration before/during deployment
- ❌ = Blocked / Issue

---

**Your build error is fixed! Redeploy on Render now.** 🎉
