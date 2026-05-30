# 🚨 SECURITY QUICK FIX - Do This NOW!

## ⚡ 3-Step Emergency Fix (15 minutes)

### Step 1: Change Your Gmail App Password (5 min)

1. **Go to:** https://myaccount.google.com/apppasswords
2. **Delete** the old app password
3. **Generate** a NEW app password
4. **Copy** the new password (16 characters)

### Step 2: Update Your .env File (2 min)

```bash
# Open the file
nano server/.env

# Find this line:
MAIL_PASSWORD=wbdonnclpnnkfsds

# Replace with your NEW app password:
MAIL_PASSWORD=your_new_16_char_password

# Save: Ctrl+O, Enter, Ctrl+X
```

### Step 3: Remove from Git History (8 min)

```bash
cd /home/moses/workspace/COFFEE/Driftwood

# Run the fix script
./fix_security_leak.sh

# Follow the prompts:
# 1. Confirm you changed password: y
# 2. Confirm you updated .env: y
# 3. Choose method: 1 (press Enter)

# Wait for it to complete...

# Force push to GitHub
git push origin --force --all
git push origin --force --tags
```

---

## ✅ Verify It Worked

### Check GitHub:
1. Go to: https://github.com/moses-25/Driftwood
2. Press `/` to search
3. Search for: `wbdonnclpnnkfsds`
4. Should find: **0 results** ✅

### Check Locally:
```bash
git ls-files | grep .env
# Should return nothing
```

---

## 🔒 What Was Exposed

These credentials were in your GitHub repo:

```
Email: mosesotieno8363@gmail.com
Password: wbdonnclpnnkfsds (Gmail app password)
Database Password: ochiengmose
M-Pesa Consumer Key: BKPAAoynBEB0uXcAlNT4sjC0htO5DNA7W9kmREr3I6SGfwdn
M-Pesa Consumer Secret: rrwUMiAqroBsozDQVIn8GfsTRQi93XP2mxu1MQLilBgMSOANYdE1l203DK1Cg1Pj
M-Pesa Passkey: bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
```

**All of these need to be changed!**

---

## 🔐 Change All Credentials

### 1. Gmail App Password ✅ (Already done in Step 1)

### 2. Database Password
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Change password
ALTER USER postgres WITH PASSWORD 'new_secure_password_here';

# Exit
\q

# Update server/.env
DATABASE_URL=postgresql://postgres:new_secure_password_here@localhost:5432/driftwood_cafe
```

### 3. M-Pesa Credentials
1. Go to: https://developer.safaricom.co.ke/
2. Login to your account
3. Regenerate your Consumer Key and Secret
4. Update `server/.env` with new values

### 4. Secret Keys
```bash
# Generate new secret keys
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Update server/.env
SECRET_KEY=<first_generated_key>
JWT_SECRET_KEY=<second_generated_key>
```

---

## 🛡️ Prevent Future Leaks

### Add Pre-commit Hook

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
if git diff --cached --name-only | grep -E "\.env$"; then
    echo "❌ ERROR: Attempting to commit .env file!"
    exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

### Always Use .env.example

✅ Already created: `server/.env.example`

Commit this (safe - no real credentials):
```bash
git add server/.env.example
git commit -m "Add .env.example template"
git push
```

---

## ⏰ Timeline

- **Now:** Change Gmail app password
- **+2 min:** Update .env
- **+10 min:** Run fix script
- **+15 min:** Force push to GitHub
- **+20 min:** Verify on GitHub
- **+30 min:** Change other credentials
- **+40 min:** Add pre-commit hook

---

## 🆘 If Something Goes Wrong

### Backup Created
The script creates a backup at:
```
../Driftwood_backup_YYYYMMDD_HHMMSS/
```

### Restore from Backup
```bash
cd /home/moses/workspace/COFFEE
rm -rf Driftwood
cp -r Driftwood_backup_* Driftwood
cd Driftwood
```

---

## 📞 Need Help?

Read the full guide: `SECURITY_FIX_URGENT.md`

---

## ✅ Checklist

- [ ] Changed Gmail app password
- [ ] Updated server/.env with new password
- [ ] Ran ./fix_security_leak.sh
- [ ] Force pushed to GitHub
- [ ] Verified password not on GitHub
- [ ] Changed database password
- [ ] Regenerated M-Pesa credentials
- [ ] Generated new secret keys
- [ ] Added pre-commit hook
- [ ] Committed .env.example

---

**STATUS:** 🚨 URGENT
**TIME:** 15-30 minutes
**PRIORITY:** CRITICAL

**DO THIS NOW!** Your email and payment credentials are exposed!
