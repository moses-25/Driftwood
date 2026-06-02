# 🚀 START HERE - Upload Product Images

## ⚡ Super Quick Start (2 Minutes)

### Step 1: Open Terminal
```bash
cd /home/moses/workspace/COFFEE/Driftwood
```

### Step 2: Run This Command
```bash
python3 upload_images.py
```

### Step 3: Press Enter 3 Times
1. Email: (press Enter for default)
2. Password: (press Enter for default)  
3. Choose option: (press Enter for option 1)

### Step 4: Wait
The script will upload all 17 images automatically.

### Step 5: Refresh Browser
Open http://localhost:5173 and check your menu!

---

## 🎬 What You'll See

```
==================================================
Driftwood Café - Image Upload Tool
==================================================

Logging in...
✅ Login successful!

Choose Upload Mode:
1) Upload all images automatically (recommended)
2) Upload images one by one (manual)
3) Exit
Choose option [1]: 

Uploading all images automatically...

Hot Coffee:
  Uploading: Espresso (ID: 1)
  ✅ Success! Image URL: http://localhost:5000/uploads/products/...
  Uploading: Americano (ID: 2)
  ✅ Success! Image URL: http://localhost:5000/uploads/products/...
  ...

==================================================
✅ Successful uploads: 17
❌ Failed uploads: 0
==================================================

Done! Check your menu at http://localhost:5173
```

---

## 🔧 If Python Script Doesn't Work

### Try the Bash Script:
```bash
./upload_images.sh
```

### Or Install requests:
```bash
pip3 install requests
python3 upload_images.py
```

---

## 📝 Manual Method (If Scripts Don't Work)

### 1. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@driftwood.com","password":"admin123"}'
```

Copy the `access_token` from the response.

### 2. Upload One Image
```bash
# Replace YOUR_TOKEN_HERE with your actual token

curl -X POST http://localhost:5000/api/upload/product-image \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@client/src/assets/Hot_Cold/Hot1.jpg" \
  -F "product_id=1"
```

### 3. Repeat for Other Products
See `MANUAL_IMAGE_UPLOAD_GUIDE.md` for all product mappings.

---

## ❓ Common Issues

### "No admin account"
Create one:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@driftwood.com","password":"admin123","full_name":"Admin","phone":"+254700000000","role":"admin"}'
```

### "requests module not found"
```bash
pip3 install requests
```

### "File not found"
Make sure you're in the project root:
```bash
cd /home/moses/workspace/COFFEE/Driftwood
pwd  # Should show: /home/moses/workspace/COFFEE/Driftwood
```

---

## 📚 More Help

- **Quick Guide:** `QUICK_START_IMAGE_UPLOAD.md`
- **Full Manual:** `MANUAL_IMAGE_UPLOAD_GUIDE.md`
- **Summary:** `IMAGE_UPLOAD_SUMMARY.md`

---

## ✅ Success Checklist

After running the script:

- [ ] Script shows "✅ Successful uploads: 17"
- [ ] No errors in the output
- [ ] Open http://localhost:5173
- [ ] Navigate to Menu section
- [ ] See real product images (not placeholders)
- [ ] All categories have images

---

## 🎯 That's It!

**Just run:**
```bash
python3 upload_images.py
```

**And press Enter 3 times!**

Your menu will have beautiful product images in 2 minutes. 🎉
