# 🚨 URGENT: Security Fix - SMTP Credentials Exposed

## ⚠️ CRITICAL ISSUE

GitGuardian detected your SMTP credentials (email password) exposed on GitHub.

**Repository:** moses-25/Driftwood
**Date:** May 30th 2026, 15:30:25 UTC
**Risk:** HIGH - Anyone can access your email account

---

## 🔥 IMMEDIATE ACTIONS (Do These NOW)

### Step 1: Change Your Email Password IMMEDIATELY

**Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Delete the old app password
3. Generate a NEW app password
4. Save it securely

**Or change your Gmail password:**
1. Go to: https://myaccount.google.com/security
2. Click "Password"
3. Change to a new strong password

⚠️ **DO THIS FIRST** - Your email is currently compromised!

---

### Step 2: Update Your Local .env File

Edit `server/.env` with the NEW password:

```bash
# Open the file
nano server/.env

# Or use your editor
code server/.env
```

Update this line:
```env
MAIL_PASSWORD=YOUR_NEW_APP_PASSWORD_HERE
```

Save and close.

---

### Step 3: Remove .env from Git History

The .env file was committed to git history. We need to remove it completely.

**Option A: Using BFG Repo-Cleaner (Recommended)**

```bash
# Install BFG (if not installed)
# On Ubuntu/Debian:
sudo apt-get install bfg

# Or download from: https://rtyley.github.io/bfg-repo-cleaner/

# Clone a fresh copy
cd /tmp
git clone --mirror https://github.com/moses-25/Driftwood.git

# Remove .env from history
bfg --delete-files .env Driftwood.git

# Clean up
cd Driftwood.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (WARNING: This rewrites history)
git push --force
```

**Option B: Using git filter-branch**

```bash
cd /home/moses/workspace/COFFEE/Driftwood

# Remove .env from all commits
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch server/.env client/.env .env" \
  --prune-empty --tag-name-filter cat -- --all

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (WARNING: This rewrites history)
git push origin --force --all
git push origin --force --tags
```

**Option C: Using git-filter-repo (Modern approach)**

```bash
# Install git-filter-repo
pip3 install git-filter-repo

cd /home/moses/workspace/COFFEE/Driftwood

# Remove .env files from history
git filter-repo --path server/.env --invert-paths
git filter-repo --path client/.env --invert-paths
git filter-repo --path .env --invert-paths

# Force push
git push origin --force --all
```

---

### Step 4: Verify .env is in .gitignore

Check `.gitignore`:

```bash
cat .gitignore | grep .env
```

Should show:
```
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
```

✅ Already configured correctly!

---

### Step 5: Verify .env is NOT Tracked

```bash
git ls-files | grep .env
```

Should return NOTHING. If it shows .env files, they're still tracked!

---

### Step 6: Force Push to GitHub

⚠️ **WARNING:** This rewrites history. Coordinate with team members!

```bash
# Force push all branches
git push origin --force --all

# Force push all tags
git push origin --force --tags
```

---

### Step 7: Verify on GitHub

1. Go to: https://github.com/moses-25/Driftwood
2. Search for your email password in the code
3. Check commit history
4. Should NOT find any credentials

---

## 🔒 PREVENT FUTURE LEAKS

### 1. Use .env.example Instead

Create `server/.env.example`:

```env
# Copy this file to .env and fill in your values

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password-here

# M-Pesa Configuration
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_SHORTCODE=your-shortcode
MPESA_PASSKEY=your-passkey

# Application
OWNER_EMAIL=your-email@gmail.com
CLIENT_ORIGIN=http://localhost:5176
PORT=5000
APP_URL=http://localhost:5000
UPLOAD_FOLDER=uploads
```

Commit `.env.example` (safe - no real credentials):
```bash
git add server/.env.example
git commit -m "Add .env.example template"
git push
```

---

### 2. Add Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check for .env files
if git diff --cached --name-only | grep -E "\.env$"; then
    echo "❌ ERROR: Attempting to commit .env file!"
    echo "Please remove .env from staging:"
    echo "  git reset HEAD .env"
    exit 1
fi

# Check for potential secrets
if git diff --cached | grep -iE "(password|secret|key|token).*=.*[a-zA-Z0-9]{10,}"; then
    echo "⚠️  WARNING: Potential secret detected in commit!"
    echo "Please review your changes carefully."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

### 3. Use Environment Variables in Production

Never commit production credentials. Use:
- **Heroku:** Config Vars
- **Vercel:** Environment Variables
- **AWS:** Secrets Manager
- **Docker:** Docker secrets
- **Kubernetes:** Secrets

---

### 4. Install GitGuardian Locally

```bash
# Install ggshield
pip3 install ggshield

# Scan your repo
ggshield secret scan repo .

# Add to pre-commit
ggshield secret scan pre-commit
```

---

## 📋 Security Checklist

- [ ] Changed email password/app password
- [ ] Updated server/.env with new password
- [ ] Removed .env from git history
- [ ] Force pushed to GitHub
- [ ] Verified .env not in GitHub
- [ ] Created .env.example
- [ ] Added pre-commit hook
- [ ] Tested application still works
- [ ] Documented for team

---

## 🔍 Check for Other Exposed Secrets

Search your repo for other potential secrets:

```bash
# Search for common secret patterns
git log -p | grep -iE "(password|secret|key|token|api_key)" | head -50

# Check current files
grep -r -iE "(password|secret|key|token).*=.*[a-zA-Z0-9]{10,}" . \
  --exclude-dir=node_modules \
  --exclude-dir=.git \
  --exclude-dir=venv \
  --exclude="*.md"
```

---

## 🚨 What Could Happen if Not Fixed

If you don't fix this:
- ❌ Anyone can access your Gmail account
- ❌ Can send emails as you
- ❌ Can read your emails
- ❌ Can access other services linked to email
- ❌ Can reset passwords for other accounts
- ❌ Identity theft risk

**This is CRITICAL - fix it NOW!**

---

## ✅ After Fixing

1. **Test your application:**
   ```bash
   # Restart backend with new password
   cd server
   python3 run.py
   
   # Test contact form
   curl -X POST http://localhost:5000/api/contact \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","email":"test@example.com","message":"Test"}'
   ```

2. **Monitor for suspicious activity:**
   - Check Gmail login activity
   - Review sent emails
   - Check for unauthorized access

3. **Enable 2FA:**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification
   - Use authenticator app

---

## 📞 Need Help?

If you're unsure about any step:

1. **Priority 1:** Change your email password NOW
2. **Priority 2:** Update .env with new password
3. **Priority 3:** Remove from git history
4. **Priority 4:** Force push to GitHub

Don't wait - your email security is at risk!

---

## 🔗 Resources

- **GitHub Secret Scanning:** https://docs.github.com/en/code-security/secret-scanning
- **BFG Repo-Cleaner:** https://rtyley.github.io/bfg-repo-cleaner/
- **git-filter-repo:** https://github.com/newren/git-filter-repo
- **GitGuardian:** https://www.gitguardian.com/
- **Gmail Security:** https://myaccount.google.com/security

---

## ⏰ Timeline

**Immediate (Now):**
- Change email password
- Update .env locally

**Within 1 hour:**
- Remove from git history
- Force push to GitHub

**Within 24 hours:**
- Verify fix worked
- Add pre-commit hooks
- Enable 2FA

---

**STATUS:** 🚨 URGENT - ACT NOW
**RISK LEVEL:** HIGH
**TIME TO FIX:** 15-30 minutes

Don't delay - your email security depends on it!
