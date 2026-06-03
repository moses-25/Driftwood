# 🔧 Critical Fix: Render Ignoring Python Version

## ❌ **The Problem:**
Render is **IGNORING** the `runtime.txt` file and using Python 3.14.3 by default.

```
==> Using Python version 3.14.3 (default) ← WRONG!
Should be: Using Python version 3.11.9
```

## 🎯 **The Solution: Set Environment Variable**

Render requires a **PYTHON_VERSION** environment variable when using a root directory (like `server`).

---

## ✅ **Fix This Now - In Render Dashboard:**

### Step 1: Go to Environment Variables
1. Open [dashboard.render.com](https://dashboard.render.com)
2. Click on your `driftwood-backend` service
3. Click **"Environment"** tab (left sidebar)

### Step 2: Add PYTHON_VERSION Variable
Click **"Add Environment Variable"** and add:

```
Key:   PYTHON_VERSION
Value: 3.11.9
```

### Step 3: Save Changes
1. Click **"Save Changes"**
2. This will **automatically trigger a redeploy**
3. Watch the logs

---

## 📊 **What You Should See After This:**

### ✅ SUCCESS - Logs should show:
```
==> Using Python version 3.11.9 ← CORRECT!
==> Installing Python version 3.11.9...
==> Running build command 'pip install -r requirements.txt'...
Successfully installed Flask-3.0.0 Pillow-10.3.0 ...
==> Build successful! 🎉
```

### ❌ BEFORE (Wrong):
```
==> Using Python version 3.14.3 (default) ← WRONG
```

---

## 🔍 **Why This Happens:**

### Render's Python Version Priority:
1. **Environment Variable** `PYTHON_VERSION` ← Highest priority
2. `.python-version` file in root directory
3. `runtime.txt` file in root directory
4. Default (Python 3.14.3) ← This is what it's using now

### Since you're using Root Directory = `server`:
- Render looks for `runtime.txt` in project root (not `server/`)
- Your `runtime.txt` is in `server/runtime.txt`
- Render can't find it, uses default 3.14.3
- **Solution:** Use environment variable instead

---

## 📋 **Complete Environment Variable List:**

While you're in the Environment tab, make sure you have ALL these variables:

### Critical (Must Have):
```bash
PYTHON_VERSION=3.11.9          ← ADD THIS NOW!
DATABASE_URL=postgresql://...   (from Render PostgreSQL)
SECRET_KEY=WFgX_fDNus80I-TGtAINRHedf9pcnUPPqC6ETD5oU_0
JWT_SECRET_KEY=L7rheGewekl__QTzbevfRk_hpyKKFcJ7mCjg5e7mYoU
CLIENT_ORIGIN=http://localhost:5173
APP_URL=https://your-backend.onrender.com
PORT=5000
```

### M-Pesa:
```bash
MPESA_ENV=sandbox
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
MPESA_CONSUMER_KEY=BKPAAoynBEB0uXcAlNT4sjC0htO5DNA7W9kmREr3I6SGfwdn
MPESA_CONSUMER_SECRET=rrwUMiAqroBsozDQVIn8GfsTRQi93XP2mxu1MQLilBgMSOANYdE1l203DK1Cg1Pj
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
MPESA_CALLBACK_URL=https://your-backend.onrender.com/api/payment/mpesa/callback
```

### Email:
```bash
RESEND_API_KEY=your_resend_api_key_here
OWNER_EMAIL=mosesotieno8363@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=mosesotieno8363@gmail.com
MAIL_PASSWORD=wbdonnclpnnkfsds
```

### Upload:
```bash
UPLOAD_FOLDER=uploads
```

---

## ⏰ **Timeline After Adding PYTHON_VERSION:**

Once you add the environment variable and save:
```
1. Render triggers automatic redeploy     - 5 seconds
2. Fetches latest code                    - 10 seconds
3. Installs Python 3.11.9 ← NEW!         - 30 seconds
4. Installs dependencies                  - 90 seconds
5. Starts service                         - 5 seconds
---
Total: ~2-3 minutes
✅ Build successful!
```

---

## 🎯 **Step-by-Step Visual Guide:**

### In Render Dashboard:

1. **Click on your service** → You see:
   ```
   ┌─────────────────────────────────┐
   │ driftwood-backend               │
   │                                 │
   │ [Logs] [Environment] [Settings] │
   └─────────────────────────────────┘
   ```

2. **Click "Environment"** → You see list of variables

3. **Scroll to bottom** → Click button:
   ```
   [+ Add Environment Variable]
   ```

4. **Fill in the form:**
   ```
   Key:   PYTHON_VERSION
   Value: 3.11.9
   ```

5. **Click "Save Changes"** button at bottom

6. **Banner appears:**
   ```
   ⚠️ Changes saved. Your service will redeploy automatically.
   ```

7. **Go to "Logs" tab** → Watch the build

---

## ✅ **Success Indicators:**

### You'll know it worked when you see:

```
==> Cloning from https://github.com/moses-25/Driftwood
==> Checking out commit 8ef1ee6...
==> Using Python version 3.11.9 ← THIS IS THE KEY LINE!
==> Installing Python version 3.11.9...
==> Running build command 'pip install -r requirements.txt'...
Collecting Flask==3.0.0
Collecting Pillow==10.3.0
Successfully installed Flask-3.0.0 Pillow-10.3.0 ...
==> Starting service with gunicorn...
[INFO] Listening at: http://0.0.0.0:5000
==> Build successful! 🎉
```

### And your service shows:
- 🟢 **Live** status
- No error messages
- URL is clickable and works

---

## 🆘 **If It STILL Fails:**

### Check These:

1. **Variable Name is Exact:**
   - Must be exactly: `PYTHON_VERSION` (all caps)
   - NOT: `Python_Version` or `python_version`

2. **Value is Exact:**
   - Must be: `3.11.9`
   - NOT: `python-3.11.9` or `3.11` or `3.11.9.0`

3. **Saved Changes:**
   - Click "Save Changes" button
   - Wait for redeploy banner

4. **Check Logs:**
   - Go to "Logs" tab
   - Scroll to top
   - Look for "Using Python version X.X.X"

---

## 💡 **Alternative: Move runtime.txt to Root**

If environment variable doesn't work, you could also:

1. Move `server/runtime.txt` to project root
2. But this is messier with your project structure
3. Environment variable is the cleaner solution

---

## 🎉 **TL;DR - DO THIS NOW:**

1. Go to Render dashboard
2. Click your service
3. Click **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add: `PYTHON_VERSION` = `3.11.9`
6. Click **"Save Changes"**
7. Wait 2-3 minutes
8. Check logs for "Using Python version 3.11.9"
9. Success! 🎉

---

**This is the final piece needed to make your deployment work!**
