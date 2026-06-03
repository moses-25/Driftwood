# 🚀 Complete Vercel Deployment Guide - Driftwood Café Frontend

## Prerequisites Checklist
- [ ] Backend deployed on Render (with URL saved)
- [ ] Code pushed to GitHub
- [ ] Vercel account created (free at [vercel.com](https://vercel.com))
- [ ] Backend URL copied from Render

---

## Part 1: Prepare for Deployment

### Verify Your Backend URL
Before deploying frontend, make sure you have:
```
Backend URL: https://driftwood-backend-XXXXX.onrender.com
```

Test it works:
```bash
curl https://your-backend-url.onrender.com/api/menu
# Should return JSON data
```

---

## Part 2: Deploy to Vercel

### Step 1: Go to Vercel
1. Open [vercel.com](https://vercel.com)
2. Click **"Sign Up"** or **"Log In"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your repositories

### Step 2: Import Project
1. You'll land on the Vercel Dashboard
2. Click **"Add New..."** button (top right)
3. Select **"Project"**

### Step 3: Import Git Repository
1. Find your repository: `driftwood-cafe`
2. Click **"Import"**

### Step 4: Configure Project

Fill in the deployment settings:

| Field | Value | Notes |
|-------|-------|-------|
| **Project Name** | `driftwood-cafe` | Can be anything, becomes your URL |
| **Framework Preset** | `Vite` | Should auto-detect |
| **Root Directory** | `client` | ⚠️ Click "Edit" and type `client` |
| **Build Command** | `npm run build` | Auto-filled |
| **Output Directory** | `dist` | Auto-filled |
| **Install Command** | `npm install` | Auto-filled |

### Step 5: Add Environment Variables

**This is critical!** Expand the **"Environment Variables"** section.

Add this variable:

```bash
Key: VITE_API_URL
Value: https://your-backend-url.onrender.com
```

**⚠️ IMPORTANT:**
- Replace `your-backend-url.onrender.com` with your **actual Render backend URL**
- Do **NOT** include a trailing slash
- Example: `https://driftwood-backend-abc123.onrender.com`

### Step 6: Deploy
1. Double-check the Root Directory is set to `client`
2. Double-check `VITE_API_URL` has your correct backend URL
3. Click **"Deploy"**

---

## Part 3: Wait for Deployment

### What Happens Now:
1. Vercel clones your GitHub repository
2. Navigates to `client/` directory
3. Runs `npm install`
4. Runs `npm run build`
5. Deploys the `dist/` folder

### Monitor the Build:
You'll see a building animation with logs. Typical messages:
```
Running "npm install"
Added 487 packages

Running "npm run build"
vite v8.0.10 building for production...
✓ 487 modules transformed
✓ built in 15.23s

Build Completed
```

### ⏰ Typical deployment time: 1-3 minutes

---

## Part 4: Get Your Frontend URL

### Step 1: Deployment Complete
Once successful, you'll see:
- 🎉 Confetti animation
- **"Visit"** button
- Your deployment URL

### Step 2: Your URLs
Vercel gives you multiple URLs:

**Production URL** (main):
```
https://driftwood-cafe.vercel.app
```

**Preview URL** (for this deployment):
```
https://driftwood-cafe-abc123.vercel.app
```

### Step 3: Test Your Frontend
1. Click **"Visit"** button
2. Your Driftwood Café website should load
3. Check browser console (F12) for errors

---

## Part 5: Update Backend CORS Settings

Now that you have your frontend URL, update your backend:

### Step 1: Go to Render Dashboard
1. Open [dashboard.render.com](https://dashboard.render.com)
2. Click on `driftwood-backend`

### Step 2: Update CLIENT_ORIGIN
1. Click **"Environment"** tab
2. Find `CLIENT_ORIGIN` variable
3. Click **edit** (pencil icon)
4. Change value to your Vercel URL:
   ```
   https://driftwood-cafe.vercel.app
   ```
5. Click **"Save Changes"**

### Step 3: Redeploy Backend
1. Scroll to top
2. Click **"Manual Deploy"** dropdown
3. Select **"Deploy latest commit"**
4. Wait 1-2 minutes for redeploy

---

## Part 6: Test Full Application

### ✅ Test Checklist:

1. **Homepage Loads**
   - [ ] Hero section displays
   - [ ] No console errors (F12)

2. **Menu Loads from Backend**
   - [ ] Navigate to menu section
   - [ ] Products display with images
   - [ ] Prices are visible
   - [ ] Check console - no CORS errors

3. **Cart Functionality**
   - [ ] Add item to cart
   - [ ] Cart count updates
   - [ ] Cart persists on page reload

4. **Checkout Process**
   - [ ] Fill out checkout form
   - [ ] Select payment method
   - [ ] Place order (test with M-Pesa sandbox)

5. **API Communication**
   - Open browser DevTools (F12)
   - Go to Network tab
   - Refresh page
   - Check API calls go to your Render backend URL
   - All should return 200 OK status

---

## Part 7: Custom Domain (Optional)

### Add Your Own Domain:

1. **In Vercel Dashboard:**
   - Click on your project
   - Go to **"Settings"** → **"Domains"**
   - Click **"Add"**
   - Enter your domain: `driftwoodcafe.com`
   - Follow DNS configuration instructions

2. **Update DNS Records** (at your domain registrar):
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```

3. **Wait for DNS Propagation** (up to 48 hours, usually faster)

4. **Update Backend CLIENT_ORIGIN**:
   - Go back to Render
   - Update `CLIENT_ORIGIN` to `https://driftwoodcafe.com`
   - Redeploy

---

## Part 8: Environment Variables for Different Environments

### Development (Local)
```bash
# client/.env
VITE_API_URL=http://localhost:5000
```

### Staging (Optional Preview Branch)
```bash
# Vercel → Project → Settings → Environment Variables
# Scope: Preview
VITE_API_URL=https://driftwood-backend-staging.onrender.com
```

### Production
```bash
# Vercel → Project → Settings → Environment Variables
# Scope: Production
VITE_API_URL=https://driftwood-backend.onrender.com
```

---

## Part 9: Automatic Deployments

### How It Works:
- **Push to `main` branch** → Automatic production deployment
- **Push to other branches** → Preview deployment
- **Pull Requests** → Preview deployment with unique URL

### Configure Deployment Settings:

1. **Go to Project Settings:**
   - Click your project
   - **"Settings"** → **"Git"**

2. **Production Branch:**
   - Set to `main` (or `master`)

3. **Deployment Protection:**
   - Can require approval before deploying
   - Useful for production

---

## Part 10: Troubleshooting

### Build Failed?

**Common Issues:**

1. **"Cannot find module 'vite'"**
   ```
   Solution: Make sure package.json is in client/ folder
   Root Directory must be set to "client"
   ```

2. **"Root Directory not found"**
   ```
   Solution: Go to Settings → General → Root Directory
   Set to exactly: client
   ```

3. **Environment variable not working**
   ```
   Solution: All Vite env vars must start with VITE_
   Redeploy after adding env vars (they're not picked up automatically)
   ```

### Frontend Loads But No Data?

**Check these:**

1. **CORS Error in Console?**
   ```
   Error: Access-Control-Allow-Origin
   
   Solution: Update CLIENT_ORIGIN on Render backend
   Must match exactly (no trailing slash)
   ```

2. **Wrong API URL?**
   ```
   Check Network tab in DevTools
   Are requests going to correct backend URL?
   
   Solution: Update VITE_API_URL in Vercel
   ```

3. **Backend Not Responding?**
   ```
   Visit backend URL directly
   Is it awake? (Render free tier sleeps after 15 min)
   
   Solution: Wait 30 seconds for backend to wake up
   ```

### Environment Variable Not Working?

1. **Redeploy Required:**
   - Changing environment variables doesn't auto-rebuild
   - Go to Deployments → Latest → Redeploy

2. **Variable Name:**
   - Must start with `VITE_`
   - Check for typos

3. **In Code:**
   ```javascript
   // Correct way to access:
   const API_URL = import.meta.env.VITE_API_URL;
   
   // NOT process.env.VITE_API_URL (that's Node.js, not Vite)
   ```

---

## Part 11: Performance Optimization

### Enable Edge Network (Automatic)
Vercel automatically serves your site from edge locations worldwide for fast loading.

### Check Performance:
1. Go to your project dashboard
2. Click **"Analytics"** tab (if available)
3. View performance metrics

### Image Optimization:
If using Vercel Image Optimization, update image imports:
```jsx
import Image from 'next/image'; // For Next.js projects
// For Vite/React, images are already optimized during build
```

---

## Part 12: Monitoring & Logs

### View Deployment Logs:
1. **In Vercel Dashboard:**
   - Click your project
   - Click **"Deployments"**
   - Click on a deployment
   - View **"Build Logs"** and **"Runtime Logs"**

### Function Logs (If using):
1. Click **"Functions"** tab
2. View invocation logs

### Real User Monitoring:
1. Click **"Analytics"** tab (paid feature)
2. View real user metrics

---

## Part 13: CI/CD Best Practices

### Branch Strategy:
```
main/master → Production (auto-deploys to driftwood-cafe.vercel.app)
staging     → Staging preview
feature/*   → Preview deployments
```

### Preview Deployments:
- Every PR gets a unique preview URL
- Test changes before merging
- Share preview links with team

### Deployment Comments:
- Vercel automatically comments on PRs with preview URLs
- Great for code reviews

---

## Quick Reference Card

| What | Where |
|------|-------|
| **Production URL** | `https://driftwood-cafe.vercel.app` |
| **Project Settings** | Dashboard → Project → Settings |
| **Environment Variables** | Settings → Environment Variables |
| **Deployment Logs** | Deployments → Select deployment → Logs |
| **Redeploy** | Deployments → ⋯ → Redeploy |
| **Custom Domain** | Settings → Domains |

---

## Environment Variables Summary

### What You Need in Vercel:
```bash
VITE_API_URL=https://your-backend-url.onrender.com
```

### What Backend Needs (Updated):
```bash
CLIENT_ORIGIN=https://driftwood-cafe.vercel.app
```

---

## 🎉 Congratulations!

Your frontend is now live at:
```
https://driftwood-cafe.vercel.app
```

### Final Checks:
- [ ] Frontend loads without errors
- [ ] Menu data loads from backend
- [ ] No CORS errors in console
- [ ] Cart works
- [ ] Checkout form works
- [ ] Images load properly
- [ ] Mobile responsive

---

## Next Steps:

1. **Test M-Pesa Integration:**
   - Place a test order
   - Use sandbox credentials
   - Verify callback is received

2. **Set Up Production M-Pesa:**
   - Get production credentials from Safaricom
   - Update Render environment variables
   - Test with real transactions

3. **Monitor Performance:**
   - Check Vercel Analytics
   - Monitor Render logs
   - Set up uptime monitoring

4. **Custom Domain (Optional):**
   - Purchase domain
   - Configure DNS
   - Update SSL certificates (automatic)

---

## Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Vercel Community**: https://github.com/vercel/vercel/discussions
- **Check Browser Console**: F12 → Console tab
- **Check Network Tab**: F12 → Network tab (see API calls)

---

**Created for Driftwood Café Frontend Deployment** ✨
