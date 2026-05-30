# Quick Start: Upload Product Images

## 🚀 Easiest Way - Use the Python Script

### Step 1: Install requests library (if needed)
```bash
pip3 install requests
```

### Step 2: Run the upload script
```bash
cd /home/moses/workspace/COFFEE/Driftwood
python3 upload_images.py
```

### Step 3: Follow the prompts
1. Enter email: `admin@driftwood.com` (or press Enter for default)
2. Enter password: `admin123` (or press Enter for default)
3. Choose option 1 to upload all images automatically
4. Wait for uploads to complete
5. Refresh your browser at http://localhost:5173

**That's it!** All 17 products will have images.

---

## 🔧 Alternative: Use the Bash Script

```bash
cd /home/moses/workspace/COFFEE/Driftwood
./upload_images.sh
```

Follow the same prompts as above.

---

## 📝 Manual Upload (One Product at a Time)

### 1. Login and get token
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@driftwood.com","password":"admin123"}'
```

Save the `access_token` from the response.

### 2. Upload an image
```bash
# Replace YOUR_TOKEN with your actual token
# Replace PRODUCT_ID with the product ID (1-17)

curl -X POST http://localhost:5000/api/upload/product-image \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@client/src/assets/Hot_Cold/Hot1.jpg" \
  -F "product_id=1"
```

### 3. Verify
```bash
curl http://localhost:5000/api/products/1 | python3 -m json.tool
```

---

## ⚠️ Troubleshooting

### "No admin account exists"
Create one:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@driftwood.com",
    "password": "admin123",
    "full_name": "Admin User",
    "phone": "+254700000000",
    "role": "admin"
  }'
```

### "requests module not found"
Install it:
```bash
pip3 install requests
```

### "File not found"
Make sure you're running the script from the project root:
```bash
cd /home/moses/workspace/COFFEE/Driftwood
```

---

## 📊 What Gets Uploaded

The script will upload images for all 17 products:

✅ **Hot Coffee** (5 products) - Using Hot1.jpg, Hot2.jpg, Hot3.jpg
✅ **Cold Coffee** (4 products) - Using Cold1.jpg, Cold2.jpg, Cold83.jpg  
✅ **Pastries** (4 products) - Using Almond Croissant.jpg, Banana Bread.jpg, etc.
✅ **Specials** (2 products) - Using special1.jpg, special2.jpg, special3.jpg
✅ **Merchandise** (2 products) - Using M1.jpeg, M3.jpeg

---

## 🎯 Expected Result

After running the script:
1. All 17 products will have images
2. Menu page will show real product photos
3. No more placeholder images
4. Images are optimized and thumbnails created

---

## 📚 More Information

- Full manual guide: `MANUAL_IMAGE_UPLOAD_GUIDE.md`
- API documentation: `server/UPLOAD_API_REFERENCE.md`
- Troubleshooting: `FIXES_SUMMARY.md`

---

## ✨ Pro Tips

1. **Run the Python script** - It's the easiest and most reliable
2. **Use option 1** (automatic) to upload all images at once
3. **Check the output** - It will show success/failure for each upload
4. **Refresh your browser** after uploads complete
5. **Images are stored** in `server/uploads/products/`

---

**Ready? Let's do it!**

```bash
python3 upload_images.py
```
