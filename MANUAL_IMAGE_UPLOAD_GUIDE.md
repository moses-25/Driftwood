# Manual Image Upload Guide

## Overview
This guide shows you how to manually upload images to your products using the backend API.

## ⚠️ Important: Authentication Required
The upload endpoints require **admin authentication**. You need to:
1. Create an admin account (or use existing one)
2. Login to get an access token
3. Use the token in your upload requests

---

## Step 1: Create Admin Account (If Needed)

### Check if you have an admin account:
```bash
curl -s http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@driftwood.com","password":"admin123"}'
```

### If no admin exists, create one:
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

---

## Step 2: Login and Get Access Token

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@driftwood.com","password":"admin123"}' \
  | python3 -m json.tool
```

**Save the `access_token` from the response!**

Example response:
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

---

## Step 3: Upload Images

### Method A: Upload and Auto-Assign to Product

```bash
# Replace YOUR_TOKEN with your actual access token
# Replace PRODUCT_ID with the product ID (1-17)
# Replace /path/to/image.jpg with your image path

curl -X POST http://localhost:5000/api/upload/product-image \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "product_id=1" \
  -F "optimize=true" \
  -F "create_thumbnails=true"
```

### Method B: Upload First, Then Assign

**Step 1: Upload the image**
```bash
curl -X POST http://localhost:5000/api/upload/product-image \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg"
```

**Step 2: Update product with image URL**
```bash
# Use the URL from the upload response
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "http://localhost:5000/uploads/products/filename.jpg"}'
```

---

## Step 4: Verify Upload

```bash
# Check the product has the image
curl http://localhost:5000/api/products/1 | python3 -m json.tool
```

---

## Your Products and Existing Images

### Hot Coffee (Category ID: 1)
```
1. Espresso          → Use: client/src/assets/Hot_Cold/Hot1.jpg
2. Americano         → Use: client/src/assets/Hot_Cold/Hot2.jpg
3. Cappuccino        → Use: client/src/assets/Hot_Cold/Hot3.jpg
4. Latte             → Use: client/src/assets/Hot_Cold/Hot1.jpg (reuse)
5. Mocha             → Use: client/src/assets/Hot_Cold/Hot2.jpg (reuse)
```

### Cold Coffee (Category ID: 2)
```
6. Iced Americano    → Use: client/src/assets/Hot_Cold/Cold1.jpg
7. Iced Latte        → Use: client/src/assets/Hot_Cold/Cold2.jpg
8. Cold Brew         → Use: client/src/assets/Hot_Cold/Cold83.jpg
9. Frappuccino       → Use: client/src/assets/Hot_Cold/Cold1.jpg (reuse)
```

### Pastries (Category ID: 3)
```
10. Croissant        → Use: client/src/assets/Pastries_Specials/Almond Croissant.jpg
11. Chocolate Muffin → Use: client/src/assets/Pastries_Specials/Brown Butter Banana Bread.jpg
12. Blueberry Scone  → Use: client/src/assets/Pastries_Specials/Matcha Scone.jpg
13. Cheesecake Slice → Use: client/src/assets/Pastries_Specials/special1.jpg
```

### Specials (Category ID: 4)
```
14. Driftwood Special → Use: client/src/assets/Pastries_Specials/special2.jpg
15. Seasonal Latte    → Use: client/src/assets/Pastries_Specials/special3.jpg
```

### Merchandise (Category ID: 5)
```
16. Driftwood Mug     → Use: client/src/assets/Merch/M3.jpeg
17. Coffee Beans      → Use: client/src/assets/Merch/M1.jpeg
```

---

## Quick Upload Examples

### Example 1: Upload Espresso Image
```bash
# Set your token
TOKEN="your_access_token_here"

# Upload and assign to Espresso (product ID 1)
curl -X POST http://localhost:5000/api/upload/product-image \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@client/src/assets/Hot_Cold/Hot1.jpg" \
  -F "product_id=1"
```

### Example 2: Upload Cold Brew Image
```bash
TOKEN="your_access_token_here"

curl -X POST http://localhost:5000/api/upload/product-image \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@client/src/assets/Hot_Cold/Cold83.jpg" \
  -F "product_id=8"
```

### Example 3: Bulk Upload (Multiple Files)
```bash
TOKEN="your_access_token_here"

curl -X POST http://localhost:5000/api/upload/bulk-upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "files=@client/src/assets/Hot_Cold/Hot1.jpg" \
  -F "files=@client/src/assets/Hot_Cold/Hot2.jpg" \
  -F "files=@client/src/assets/Hot_Cold/Hot3.jpg" \
  -F "file_type=products"
```

---

## Troubleshooting

### Error: "Missing Authorization Header"
- You forgot to include the token
- Add: `-H "Authorization: Bearer YOUR_TOKEN"`

### Error: "Token has expired"
- Login again to get a new token
- Tokens expire after 1 hour

### Error: "Forbidden" or "Admin access required"
- Your account is not an admin
- Check user role in database or create admin account

### Error: "File not found"
- Check the file path is correct
- Use absolute path or relative from where you run the command

### Error: "Invalid file type"
- Only images are allowed (jpg, jpeg, png, gif, webp)
- Check file extension

---

## Tips

1. **Use absolute paths** for images to avoid confusion
2. **Test with one image first** before bulk uploading
3. **Save your token** in a variable for easier use
4. **Check the response** after each upload to verify success
5. **View uploaded images** at: http://localhost:5000/uploads/products/filename.jpg

---

## Next Steps

After uploading images:
1. Refresh your frontend (http://localhost:5173)
2. Navigate to the Menu section
3. Products should now show real images instead of placeholders
4. Check browser console for any errors

---

## Need Help?

If you encounter issues:
1. Check backend logs (terminal running `python3 run.py`)
2. Verify you're logged in as admin
3. Ensure file paths are correct
4. Check file permissions on the uploads folder
