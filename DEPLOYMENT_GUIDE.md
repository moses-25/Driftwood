# 🚀 Deployment Guide - Driftwood Café

## Pre-Deployment Checklist

### ✅ Completed
- [x] Client builds successfully (`npm run build`)
- [x] Server has production dependencies
- [x] Secure SECRET_KEY and JWT_SECRET_KEY generated
- [x] Docker configuration ready
- [x] WSGI entry point configured
- [x] Database migrations set up

### 🔧 To Configure Before Deployment
- [ ] Update production environment variables
- [ ] Set up production database
- [ ] Configure M-Pesa for production environment
- [ ] Set up domain names (frontend + backend)
- [ ] Update CORS settings with production URLs

---

## Option 1: Quick Deploy (Recommended for Beginners)

### Frontend → Vercel
1. **Push code to GitHub** (if not already)
2. **Go to [Vercel](https://vercel.com)** and sign in
3. **Import your repository**
4. **Configure:**
   - Framework Preset: Vite
   - Root Directory: `client`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. **Add Environment Variable:**
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```
6. **Deploy** ✨

### Backend → Render
1. **Go to [Render](https://render.com)** and sign in
2. **Create New → Web Service**
3. **Connect your GitHub repository**
4. **Configure:**
   - Name: `driftwood-backend`
   - Root Directory: `server`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT wsgi:application`
5. **Add PostgreSQL Database** (from Render dashboard)
6. **Add Environment Variables** (see below)
7. **Deploy** ✨

---

## Option 2: Deploy with Railway

### Full Stack on Railway
1. **Go to [Railway](https://railway.app)** and sign in
2. **Create New Project → Deploy from GitHub**
3. **Add PostgreSQL database** from Railway dashboard
4. **Deploy Backend:**
   - Add service → Select `server` directory
   - Set start command: `gunicorn --bind 0.0.0.0:$PORT wsgi:application`
   - Add environment variables (see below)
5. **Deploy Frontend:**
   - Add service → Select `client` directory
   - Set build command: `npm run build`
   - Set start command: `npm run preview`
   - Add `VITE_API_URL` pointing to backend URL

---

## Environment Variables Setup

### Backend Environment Variables
Copy all variables from `server/.env.production.example` and update:

**Critical Variables:**
```bash
# Generate secure keys (run this locally):
python -c "import secrets; print(secrets.token_urlsafe(32))"

SECRET_KEY=<generated-secure-key>
JWT_SECRET_KEY=<generated-secure-key>
DATABASE_URL=<from-hosting-platform>
CLIENT_ORIGIN=https://your-frontend.vercel.app
APP_URL=https://your-backend.onrender.com
MPESA_CALLBACK_URL=https://your-backend.onrender.com/api/payment/mpesa/callback
```

**Email Variables:**
```bash
RESEND_API_KEY=<get-from-resend.com>
OWNER_EMAIL=mosesotieno8363@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=mosesotieno8363@gmail.com
MAIL_PASSWORD=<your-gmail-app-password>
```

**M-Pesa Production:**
```bash
MPESA_ENV=production
MPESA_BASE_URL=https://api.safaricom.co.ke
MPESA_CONSUMER_KEY=<from-safaricom-daraja>
MPESA_CONSUMER_SECRET=<from-safaricom-daraja>
MPESA_SHORTCODE=<your-production-shortcode>
MPESA_PASSKEY=<your-production-passkey>
```

### Frontend Environment Variables
```bash
VITE_API_URL=https://your-backend-domain.com
```

---

## Database Setup

### On First Deployment:
```bash
# The hosting platform will run these automatically, or you can run via SSH:
flask db upgrade
python -c "from utils.database import seed_menu_data; seed_menu_data()"
```

---

## M-Pesa Configuration for Production

### 1. Get Production Credentials
- Go to [Safaricom Daraja Portal](https://developer.safaricom.co.ke/)
- Create a production app
- Get your production `Consumer Key` and `Consumer Secret`
- Get your production `Shortcode` and `Passkey`

### 2. Update Callback URL
- In Daraja Portal, set callback URL to:
  ```
  https://your-backend-domain.com/api/payment/mpesa/callback
  ```

### 3. Test in Sandbox First
- Keep `MPESA_ENV=sandbox` initially
- Test with Safaricom test credentials
- Switch to `MPESA_ENV=production` when ready

---

## Post-Deployment Steps

### 1. Verify Backend
```bash
curl https://your-backend-domain.com/api/menu
# Should return menu items
```

### 2. Verify Frontend
- Open `https://your-frontend-domain.com`
- Check browser console for errors
- Test API calls (menu loading, cart, etc.)

### 3. Test Payment Flow
- Make a test order
- Verify M-Pesa callback is received
- Check database records

### 4. Test Email
- Submit contact form
- Verify emails are delivered

---

## CORS Troubleshooting

If you get CORS errors:

1. **Check backend logs** for exact error
2. **Verify `CLIENT_ORIGIN`** matches frontend URL exactly (no trailing slash)
3. **Restart backend** after environment variable changes
4. **Check browser network tab** for preflight OPTIONS requests

---

## Common Issues & Solutions

### Issue: "Module not found" on backend
**Solution:** Make sure all imports use relative paths and `requirements.txt` is complete

### Issue: Frontend can't reach backend
**Solution:** 
- Check `VITE_API_URL` is correct
- Verify CORS is configured properly
- Check backend is actually running

### Issue: Database connection fails
**Solution:**
- Verify `DATABASE_URL` is correct
- Check database is running and accessible
- Ensure database migrations have run

### Issue: M-Pesa callbacks not received
**Solution:**
- Verify callback URL is publicly accessible (not localhost)
- Check Daraja Portal configuration
- Review backend logs for incoming requests

---

## Security Checklist

- [x] SECRET_KEY is strong and unique
- [x] JWT_SECRET_KEY is strong and unique
- [ ] `.env` file is NOT committed to git
- [ ] Database credentials are secure
- [ ] M-Pesa credentials are production-ready
- [ ] Gmail uses App Password (not main password)
- [ ] HTTPS is enabled on production
- [ ] CORS only allows your frontend domain

---

## Monitoring

### Check Backend Health
```bash
curl https://your-backend-domain.com/health
```

### View Logs
- **Vercel:** Dashboard → Deployments → Logs
- **Render:** Dashboard → Logs tab
- **Railway:** Dashboard → Deployments → View Logs

---

## Rollback Plan

If deployment fails:
1. **Keep previous deployment running** (most platforms keep old versions)
2. **Check logs** for specific errors
3. **Revert environment variables** if needed
4. **Redeploy previous version** from platform dashboard

---

## Need Help?

1. Check logs first (most issues are visible there)
2. Verify all environment variables are set correctly
3. Test backend API endpoints directly with curl/Postman
4. Check CORS configuration if frontend can't reach backend
5. Review this guide's troubleshooting section

---

## 🎉 Deployment Complete!

Once deployed:
- Frontend URL: `https://your-app.vercel.app`
- Backend URL: `https://your-api.onrender.com`
- Admin can manage orders via API
- Customers can place orders online
- M-Pesa payments work automatically

**Remember to:**
- Monitor logs regularly
- Keep dependencies updated
- Backup database periodically
- Test M-Pesa in sandbox before going live
