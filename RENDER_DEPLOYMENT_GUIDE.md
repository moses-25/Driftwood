# 🚀 Complete Render Deployment Guide - Driftwood Café Backend

## Prerequisites Checklist
- [ ] GitHub account created
- [ ] Code pushed to GitHub repository
- [ ] Render account created (free at [render.com](https://render.com))
- [ ] Gmail App Password generated (for email functionality)
- [ ] M-Pesa sandbox/production credentials ready

---

## Part 1: Push Code to GitHub

### If you haven't pushed to GitHub yet:

```bash
# Navigate to your project root
cd /home/moses/workspace/COFFEE/Driftwood

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/driftwood-cafe.git
git branch -M main
git push -u origin main
```

---

## Part 2: Create PostgreSQL Database on Render

### Step 1: Go to Render Dashboard
1. Open [dashboard.render.com](https://dashboard.render.com)
2. Sign in (or create free account)

### Step 2: Create PostgreSQL Database
1. Click the **"New +"** button (top right)
2. Select **"PostgreSQL"**

### Step 3: Configure Database
Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `driftwood-db` |
| **Database** | `driftwood_cafe` |
| **User** | `driftwood_user` (auto-filled) |
| **Region** | Choose closest to you (e.g., Oregon, Frankfurt, Singapore) |
| **PostgreSQL Version** | 15 (or latest) |
| **Plan Type** | **Free** |

4. Click **"Create Database"**

### Step 4: Wait for Database Creation
- Status will show "Creating..."
- Wait 1-2 minutes until status becomes "Available" (green checkmark)

### Step 5: Copy Database Connection String
1. Once database is ready, click on `driftwood-db` to open it
2. Scroll down to **"Connections"** section
3. Find **"Internal Database URL"** 
4. Click the **copy icon** 📋 next to it
5. **Save this somewhere** - you'll need it soon!

It looks like:
```
postgresql://driftwood_user:LONG_PASSWORD_HERE@dpg-xxxxx-a.oregon-postgres.render.com/driftwood_cafe
```

---

## Part 3: Create Web Service (Backend)

### Step 1: Create New Web Service
1. Go back to Render Dashboard
2. Click **"New +"** button again
3. Select **"Web Service"**

### Step 2: Connect GitHub Repository
1. If first time: Click **"Connect account"** → **"GitHub"**
   - Authorize Render to access your repositories
2. Find your repository: `driftwood-cafe` (or whatever you named it)
3. Click **"Connect"**

### Step 3: Configure Web Service

Fill in the form carefully:

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `driftwood-backend` | This becomes part of your URL |
| **Region** | Same as database | Important for low latency |
| **Branch** | `main` | Or `master` if that's your branch name |
| **Root Directory** | `server` | ⚠️ IMPORTANT: Type exactly `server` |
| **Runtime** | `Python 3` | Should auto-detect |
| **Build Command** | `pip install -r requirements.txt` | Should auto-fill |
| **Start Command** | `gunicorn --bind 0.0.0.0:$PORT --workers 4 wsgi:application` | Should auto-fill |

### Step 4: Choose Plan Type
- Scroll down to **"Instance Type"**
- Select **"Free"** (or paid if you prefer)

### Step 5: Add Environment Variables

**This is the most important part!** Scroll to **"Environment Variables"** section.

Click **"Add Environment Variable"** for each of these:

#### Database & Security
```bash
Key: DATABASE_URL
Value: [Paste the Internal Database URL you copied earlier]

Key: SECRET_KEY
Value: WFgX_fDNus80I-TGtAINRHedf9pcnUPPqC6ETD5oU_0

Key: JWT_SECRET_KEY
Value: L7rheGewekl__QTzbevfRk_hpyKKFcJ7mCjg5e7mYoU
```

#### Application URLs (Temporary - we'll update later)
```bash
Key: CLIENT_ORIGIN
Value: http://localhost:5173

Key: APP_URL
Value: https://driftwood-backend.onrender.com

Key: PORT
Value: 5000
```

#### Email Configuration
```bash
Key: RESEND_API_KEY
Value: your_resend_api_key_here

Key: OWNER_EMAIL
Value: mosesotieno8363@gmail.com

Key: MAIL_SERVER
Value: smtp.gmail.com

Key: MAIL_PORT
Value: 587

Key: MAIL_USE_TLS
Value: true

Key: MAIL_USERNAME
Value: mosesotieno8363@gmail.com

Key: MAIL_PASSWORD
Value: wbdonnclpnnkfsds
```

#### M-Pesa Configuration (Sandbox for now)
```bash
Key: MPESA_ENV
Value: sandbox

Key: MPESA_BASE_URL
Value: https://sandbox.safaricom.co.ke

Key: MPESA_CONSUMER_KEY
Value: BKPAAoynBEB0uXcAlNT4sjC0htO5DNA7W9kmREr3I6SGfwdn

Key: MPESA_CONSUMER_SECRET
Value: rrwUMiAqroBsozDQVIn8GfsTRQi93XP2mxu1MQLilBgMSOANYdE1l203DK1Cg1Pj

Key: MPESA_SHORTCODE
Value: 174379

Key: MPESA_PASSKEY
Value: bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919

Key: MPESA_CALLBACK_URL
Value: https://driftwood-backend.onrender.com/api/payment/mpesa/callback
```

#### File Upload
```bash
Key: UPLOAD_FOLDER
Value: uploads
```

### Step 6: Create Web Service
1. Double-check all environment variables are correct
2. Scroll to the bottom
3. Click **"Create Web Service"**

---

## Part 4: Wait for Deployment

### What Happens Now:
1. Render clones your GitHub repository
2. Installs Python dependencies from `requirements.txt`
3. Starts the application with Gunicorn
4. You'll see logs in real-time

### Monitor the Build:
Watch the **"Logs"** tab at the bottom. You should see:
```
==> Cloning from https://github.com/YOUR-USERNAME/driftwood-cafe...
==> Checking out commit abc1234 in branch main
==> Installing dependencies from requirements.txt
Successfully installed Flask-3.0.0 ...
==> Starting service with gunicorn...
[INFO] Listening at: http://0.0.0.0:5000
==> Build successful!
```

### ⏰ Typical deployment time: 3-5 minutes

---

## Part 5: Get Your Backend URL

### Step 1: Find Your URL
1. Once deployment succeeds, look at the top left
2. You'll see your service URL: `https://driftwood-backend.onrender.com`
3. **Click the URL** to verify it works

### Step 2: Test the Backend
Your URL should look like:
```
https://driftwood-backend-XXXXX.onrender.com
```

Test it by visiting:
```
https://your-backend-url.onrender.com/api/menu
```

You should see JSON response (might be empty at first).

### Step 3: Copy Your Backend URL
**Write down your full backend URL** - you'll need it for:
- Frontend deployment
- M-Pesa callback configuration

---

## Part 6: Update Environment Variables

Now that you have your real backend URL, update these variables:

### Step 1: Go to Environment Tab
1. In Render dashboard, click on `driftwood-backend`
2. Click **"Environment"** tab (left sidebar)

### Step 2: Update APP_URL
1. Find `APP_URL`
2. Click the **edit icon** (pencil)
3. Change from `https://driftwood-backend.onrender.com`
4. To your **actual URL**: `https://driftwood-backend-XXXXX.onrender.com`
5. Click **"Save Changes"**

### Step 3: Update MPESA_CALLBACK_URL
1. Find `MPESA_CALLBACK_URL`
2. Click edit
3. Update to: `https://your-actual-backend-url.onrender.com/api/payment/mpesa/callback`
4. Click **"Save Changes"**

### Step 4: Trigger Redeploy
After updating environment variables:
1. Go to **"Manual Deploy"** section at the top
2. Click **"Clear build cache & deploy"**
3. Wait for redeploy (1-2 minutes)

---

## Part 7: Initialize Database

### Option 1: Automatic (Recommended)
If your code has database initialization on startup, it should run automatically.

### Option 2: Manual via Render Shell
1. In your `driftwood-backend` service dashboard
2. Click **"Shell"** tab (left sidebar)
3. Wait for shell to connect
4. Run these commands:

```bash
# Run database migrations
flask db upgrade

# Optional: Seed initial data
python -c "from utils.database import seed_menu_data; seed_menu_data()"
```

### Option 3: Use Local Database Client
Connect to your Render database from your local machine:

```bash
# Use the External Database URL from Render dashboard
psql "postgresql://driftwood_user:PASSWORD@dpg-xxxxx-a.oregon-postgres.render.com/driftwood_cafe"

# Or use a GUI tool like pgAdmin, DBeaver, or TablePlus
```

---

## Part 8: Verify Deployment

### ✅ Checklist:
- [ ] Service status is **"Live"** (green)
- [ ] Backend URL opens without errors
- [ ] `/api/menu` endpoint returns data
- [ ] Database contains data (if seeded)
- [ ] Logs show no errors

### Test Your API Endpoints:

```bash
# Test menu endpoint
curl https://your-backend-url.onrender.com/api/menu

# Test health check (if you have one)
curl https://your-backend-url.onrender.com/health

# Test specific category
curl https://your-backend-url.onrender.com/api/menu/hot
```

---

## Part 9: Important Notes

### 🔒 Security Reminders:
- ✅ `.env` file is **NOT** pushed to GitHub (gitignored)
- ✅ Environment variables are **only** in Render dashboard
- ✅ Database password is secure (auto-generated by Render)

### ⚠️ Free Tier Limitations:
- **Spin down after 15 minutes of inactivity**
  - First request after inactivity takes ~30 seconds to wake up
  - Consider upgrading to paid tier for production
- **750 hours/month free**
  - About 31 days of uptime
  - Resets monthly

### 🔄 Auto-Deploy:
- Render automatically redeploys when you push to GitHub
- You can disable this in Settings → "Auto-Deploy"

### 📊 Monitoring:
- View logs: **"Logs"** tab
- View metrics: **"Metrics"** tab
- View events: **"Events"** tab

---

## Part 10: Troubleshooting

### Build Failed?

**Check these:**
1. **Root Directory**: Must be exactly `server`
2. **requirements.txt**: Must be in `server/` folder
3. **Python version**: Check `runtime.txt` exists with `python-3.11.0`

### Service Won't Start?

**Check logs for errors:**
```
ImportError: No module named 'something'
→ Missing dependency in requirements.txt

Cannot connect to database
→ DATABASE_URL is wrong or database not ready

ModuleNotFoundError: No module named 'app'
→ Wrong Root Directory or Start Command
```

### Database Connection Issues?

1. Make sure you're using **Internal Database URL** (not External)
2. Database and web service must be in **same region**
3. Database must be **"Available"** status (green)

### Can't Access API?

1. Check if service is **"Live"** (not "Deploying" or "Failed")
2. Verify URL doesn't have typos
3. Check CORS settings in your code match your frontend URL

---

## Next Steps: Deploy Frontend

Once backend is working:

1. **Copy your backend URL**
2. **Follow the Vercel deployment guide** (I can create this next)
3. **Update `CLIENT_ORIGIN`** in Render with your Vercel URL
4. **Test the full application**

---

## 🎉 Congratulations!

Your backend is now live at:
```
https://driftwood-backend-XXXXX.onrender.com
```

**Save this URL** - you'll need it for:
- Frontend environment variables
- M-Pesa Daraja callback configuration
- API testing

---

## Quick Reference Card

| What | Where |
|------|-------|
| **Backend URL** | `https://your-service.onrender.com` |
| **Database URL** | Found in `driftwood-db` → Connections |
| **Logs** | Service → Logs tab |
| **Environment Variables** | Service → Environment tab |
| **Shell Access** | Service → Shell tab |
| **Redeploy** | Service → Manual Deploy → Deploy latest commit |

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Check Logs First**: Most issues show up in the logs
- **GitHub Issues**: Create an issue in your repository

---

**Created for Driftwood Café Backend Deployment** 🚀
