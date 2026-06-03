# 🚨 URGENT: Force Render to Redeploy Latest Code

## ❌ Problem:
Render is still using the OLD commit without the fixes:
```
Checking out commit 5267546... ← OLD (has Python 3.14 bug)
```

It should be using:
```
Checking out commit f09a8f3... ← NEW (has Python 3.11.9 fix)
```

---

## ✅ Solution: Force Manual Redeploy

### Step 1: Go to Render Dashboard
1. Open [dashboard.render.com](https://dashboard.render.com)
2. Click on your `driftwood-backend` service

### Step 2: Manual Deploy
Look at the top right corner, you'll see a **"Manual Deploy"** button.

1. Click **"Manual Deploy"** dropdown
2. Select **"Clear build cache & deploy"**
3. Click to confirm

### Step 3: Verify Correct Commit
Watch the logs. You should now see:
```
==> Checking out commit f09a8f3... ← This is correct!
==> Using Python version 3.11.9 ← This is correct!
```

NOT:
```
==> Checking out commit 5267546... ← This is wrong!
==> Using Python version 3.14.3 ← This is wrong!
```

---

## 🔍 Why This Happened:

### Render Didn't Auto-Deploy Because:
1. **Auto-deploy might be disabled** in your service settings
2. **Or webhook not triggered** from GitHub push
3. **Or still caching** the old commit

### The Manual Deploy Fixes This:
- Forces Render to fetch latest code from GitHub
- Clears build cache (removes old Python/dependencies)
- Starts fresh build with correct commit

---

## 📋 **Checklist After Manual Deploy:**

Watch the logs for these SUCCESS indicators:

```
✅ Checking out commit f09a8f3 (or aac72e3)
✅ Using Python version 3.11.9
✅ Successfully installed Flask-3.0.0
✅ Successfully installed Pillow-10.3.0
✅ [INFO] Listening at: http://0.0.0.0:5000
✅ Build successful!
```

---

## 🎯 **Exact Steps (Screenshot Guide):**

### What You'll See in Render:

1. **Top of your service page:**
   ```
   [Service Name: driftwood-backend]
   
   [Manual Deploy ▼]  [Settings]  [Logs]
   ```

2. **Click "Manual Deploy" dropdown, you'll see:**
   ```
   ○ Deploy latest commit
   ○ Clear build cache & deploy  ← CLICK THIS ONE
   ○ Deploy a specific commit
   ```

3. **Select "Clear build cache & deploy"**

4. **You'll see confirmation:**
   ```
   This will rebuild your service from scratch
   
   [Cancel]  [Deploy]  ← CLICK Deploy
   ```

5. **Build starts immediately**

---

## ⚙️ **Alternative: Check Auto-Deploy Settings**

While you're there, enable auto-deploy for future:

1. In your service, click **"Settings"** (left sidebar)
2. Scroll to **"Build & Deploy"** section
3. Find **"Auto-Deploy"**
4. Make sure it's set to **"Yes"**
5. Save if you changed it

This way, future pushes to GitHub will auto-deploy.

---

## 🔄 **If Manual Deploy Still Uses Old Commit:**

### Check Branch Setting:
1. Go to **"Settings"** → **"Build & Deploy"**
2. Verify **"Branch"** is set to: `backup`
3. If it says `main` or `master`, change it to `backup`
4. Click **"Save Changes"**
5. Then do manual deploy again

---

## 📊 **Expected Timeline:**

Once you click "Clear build cache & deploy":
```
1. Fetching latest code from GitHub  - 10 sec
2. Installing Python 3.11.9          - 30 sec
3. Installing dependencies           - 90 sec
4. Starting service                  - 5 sec
---
Total: ~2-3 minutes
```

---

## ✅ **Success Confirmation:**

You'll know it worked when:

### In Logs:
```
==> Checking out commit f09a8f3 ✓
==> Using Python version 3.11.9 ✓
Successfully installed Pillow-10.3.0 ✓
Build successful! ✓
```

### In Dashboard:
- 🟢 Green "Live" badge
- No error messages
- URL is clickable

### Test It:
```bash
curl https://your-backend-url.onrender.com/api/menu
# Should return JSON (not error)
```

---

## 🆘 **If It STILL Fails After Manual Deploy:**

### 1. Verify GitHub Has Latest Code:
Go to: https://github.com/moses-25/Driftwood
- Click on `backup` branch
- Click `server/runtime.txt`
- Should show: `python-3.11.9`

If it doesn't, the push didn't work. Let me know.

### 2. Try Deploy Specific Commit:
In Render:
1. **"Manual Deploy"** → **"Deploy a specific commit"**
2. Enter commit hash: `f09a8f3`
3. Click Deploy

### 3. Check Render Branch:
Settings → Build & Deploy → Branch should be `backup`

---

## 💡 **Pro Tip:**

After successful deploy, visit:
```
Settings → Build & Deploy → Deploy Hook
```

Copy the webhook URL and add it to GitHub:
```
GitHub Repo → Settings → Webhooks → Add webhook
Paste the Deploy Hook URL
```

This ensures future pushes trigger automatic deploys.

---

## ⚡ **TL;DR - Do This Now:**

1. Go to Render dashboard
2. Click your service
3. **"Manual Deploy"** → **"Clear build cache & deploy"**
4. Wait 2-3 minutes
5. Check logs for `commit f09a8f3` and `Python 3.11.9`
6. Should succeed! 🎉

---

**The fix is in your code, Render just needs to deploy the latest version!**
