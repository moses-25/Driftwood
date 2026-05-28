# Upload API Reference Guide

## Quick Reference for Phase 6 File Upload & Media Management

---

## 🔐 Authentication

Most upload endpoints require JWT authentication with specific roles:
- **Admin Only:** Upload, delete, cleanup endpoints
- **Staff/Admin:** List files endpoint
- **JWT Required:** File info endpoint
- **Public:** Serve files endpoint

Include the token in the Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 📡 API Endpoints

### 1. Serve Uploaded File

**Endpoint:** `GET /api/uploads/<path:filename>`  
**Auth:** None (public)  
**Description:** Serve uploaded files directly

**Example:**
```
GET /api/uploads/products/image.jpg
GET /api/uploads/products/thumbnails/small/small_image.jpg
GET /api/uploads/categories/category.jpg
```

**Response:** Image file (binary)

---

### 2. Upload Product Image

**Endpoint:** `POST /api/upload/product-image`  
**Auth:** Admin Only  
**Description:** Upload and process product image

**Form Data:**
```
file (file): Image file (required)
product_id (int): Product ID to update (optional)
optimize (bool): Optimize image (default: true)
create_thumbnails (bool): Create thumbnails (default: true)
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/upload/product-image \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -F "file=@product.jpg" \
  -F "product_id=1" \
  -F "optimize=true" \
  -F "create_thumbnails=true"
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Image uploaded successfully",
  "data": {
    "filename": "4c25ab55-d576-4884-a49a-1e041c090179.jpg",
    "url": "http://localhost:5000/uploads/products/4c25ab55-d576-4884-a49a-1e041c090179.jpg",
    "path": "/path/to/uploads/products/4c25ab55-d576-4884-a49a-1e041c090179.jpg",
    "size": 1824,
    "width": 500,
    "height": 500,
    "thumbnails": {
      "small": {
        "filename": "small_4c25ab55-d576-4884-a49a-1e041c090179.jpg",
        "url": "http://localhost:5000/uploads/products/thumbnails/small/small_4c25ab55-d576-4884-a49a-1e041c090179.jpg",
        "path": "/path/to/uploads/products/thumbnails/small/small_4c25ab55-d576-4884-a49a-1e041c090179.jpg"
      },
      "medium": { ... },
      "large": { ... }
    },
    "product_id": 1,
    "product_name": "Espresso"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "File type not allowed. Allowed types: png, jpg, jpeg, gif, webp"
}
```

---

### 3. Upload Category Image

**Endpoint:** `POST /api/upload/category-image`  
**Auth:** Admin Only  
**Description:** Upload and process category image

**Form Data:**
```
file (file): Image file (required)
category_id (int): Category ID to update (optional)
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/upload/category-image \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -F "file=@category.jpg" \
  -F "category_id=1"
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Image uploaded successfully",
  "data": {
    "filename": "7d3e9f12-a456-4b89-c123-d456e789f012.jpg",
    "url": "http://localhost:5000/uploads/categories/7d3e9f12-a456-4b89-c123-d456e789f012.jpg",
    "size": 1234,
    "width": 400,
    "height": 300,
    "category_id": 1,
    "category_name": "Hot Coffee"
  }
}
```

---

### 4. Delete File

**Endpoint:** `DELETE /api/upload/delete/<file_type>/<filename>`  
**Auth:** Admin Only  
**Description:** Delete file and all its thumbnails

**Path Parameters:**
- `file_type` (string): Type of file (products, categories)
- `filename` (string): Filename to delete

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/upload/delete/products/image.jpg \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "File deleted successfully"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Invalid file type"
}
```

---

### 5. List Files

**Endpoint:** `GET /api/upload/files/<file_type>`  
**Auth:** Staff/Admin Only  
**Description:** List uploaded files

**Path Parameters:**
- `file_type` (string): Type of file (products, categories)

**Query Parameters:**
- `limit` (int, optional): Maximum number of files (default: 100)

**Example:**
```bash
curl -X GET "http://localhost:5000/api/upload/files/products?limit=10" \
  -H "Authorization: Bearer STAFF_TOKEN"
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "files": [
      {
        "filename": "image1.jpg",
        "url": "http://localhost:5000/uploads/products/image1.jpg",
        "size": 1824,
        "created": 1779914274.123,
        "modified": 1779914274.123
      },
      {
        "filename": "image2.jpg",
        "url": "http://localhost:5000/uploads/products/image2.jpg",
        "size": 2048,
        "created": 1779914280.456,
        "modified": 1779914280.456
      }
    ],
    "count": 2
  }
}
```

---

### 6. Get File Info

**Endpoint:** `GET /api/upload/file-info/<file_type>/<filename>`  
**Auth:** JWT Required  
**Description:** Get detailed file information

**Path Parameters:**
- `file_type` (string): Type of file (products, categories)
- `filename` (string): Filename

**Example:**
```bash
curl -X GET http://localhost:5000/api/upload/file-info/products/image.jpg \
  -H "Authorization: Bearer JWT_TOKEN"
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "filename": "image.jpg",
    "path": "/path/to/uploads/products/image.jpg",
    "url": "http://localhost:5000/uploads/products/image.jpg",
    "size": 1824,
    "created": 1779914274.123,
    "modified": 1779914274.123,
    "width": 500,
    "height": 500,
    "format": "JPEG"
  }
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "File not found"
}
```

---

### 7. Cleanup Orphaned Files

**Endpoint:** `POST /api/upload/cleanup/<file_type>`  
**Auth:** Admin Only  
**Description:** Remove files not referenced in database

**Path Parameters:**
- `file_type` (string): Type of file (products, categories)

**Example:**
```bash
curl -X POST http://localhost:5000/api/upload/cleanup/products \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**Success Response (200):**
```json
{
  "success": true,
  "deleted": 5,
  "message": "Deleted 5 orphaned files"
}
```

---

### 8. Bulk Upload

**Endpoint:** `POST /api/upload/bulk-upload`  
**Auth:** Admin Only  
**Description:** Upload multiple images at once

**Form Data:**
```
files (files): Multiple image files (required)
file_type (string): Type of files (products, categories)
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/upload/bulk-upload \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@image3.jpg" \
  -F "file_type=products"
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Uploaded 3 files, 0 failed",
  "data": {
    "results": [
      {
        "filename": "image1.jpg",
        "success": true,
        "url": "http://localhost:5000/uploads/products/abc123.jpg",
        "error": null
      },
      {
        "filename": "image2.jpg",
        "success": true,
        "url": "http://localhost:5000/uploads/products/def456.jpg",
        "error": null
      },
      {
        "filename": "image3.jpg",
        "success": true,
        "url": "http://localhost:5000/uploads/products/ghi789.jpg",
        "error": null
      }
    ],
    "successful": 3,
    "failed": 0
  }
}
```

---

## 🔄 Upload Flow

### Standard Upload Flow

```
1. Admin selects image file
   ↓
2. Frontend calls: POST /api/upload/product-image
   ↓
3. Backend validates image (type, size, dimensions)
   ↓
4. Backend generates unique filename (UUID)
   ↓
5. Backend optimizes image (quality 85%, max 1200px)
   ↓
6. Backend creates thumbnails (small, medium, large)
   ↓
7. Backend saves files to uploads folder
   ↓
8. Backend updates product record (if product_id provided)
   ↓
9. Backend returns URLs for image and thumbnails
```

### Update Product Image Flow

```
1. Admin uploads new image with product_id
   ↓
2. Backend retrieves existing product
   ↓
3. Backend deletes old image and thumbnails
   ↓
4. Backend uploads new image
   ↓
5. Backend updates product.image_url
   ↓
6. Frontend displays new image
```

---

## 💡 Image Utilities

### Validation Rules

**Allowed File Types:**
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

**Size Limits:**
- Maximum file size: 5MB
- Minimum dimensions: 100x100px
- Maximum dimensions: 2000x2000px

**Validation Checks:**
1. File extension validation
2. File size validation
3. Image type verification (using imghdr)
4. Dimension validation
5. Corruption detection

### Image Processing

**Optimization:**
- Quality: 85% (JPEG)
- Max width: 1200px (maintains aspect ratio)
- RGBA to RGB conversion (for JPEG compatibility)

**Thumbnails:**
- Small: 150x150px
- Medium: 300x300px
- Large: 600x600px
- Maintains aspect ratio
- Quality: 85%

---

## 🚨 Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing/invalid JWT) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found (file/product/category not found) |
| 500 | Internal Server Error |

---

## 🔒 File Types

| Type | Description | Thumbnails |
|------|-------------|------------|
| `products` | Product images | Yes (3 sizes) |
| `categories` | Category images | No |

---

## 📁 Directory Structure

```
uploads/
├── products/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── thumbnails/
│       ├── small/
│       │   ├── small_image1.jpg
│       │   └── small_image2.jpg
│       ├── medium/
│       │   ├── medium_image1.jpg
│       │   └── medium_image2.jpg
│       └── large/
│           ├── large_image1.jpg
│           └── large_image2.jpg
├── categories/
│   ├── category1.jpg
│   └── category2.jpg
└── temp/
```

---

## 🧪 Testing

### Test with cURL

**Upload Product Image:**
```bash
curl -X POST http://localhost:5000/api/upload/product-image \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -F "file=@test.jpg" \
  -F "optimize=true"
```

**List Files:**
```bash
curl -X GET http://localhost:5000/api/upload/files/products \
  -H "Authorization: Bearer STAFF_TOKEN"
```

**Delete File:**
```bash
curl -X DELETE http://localhost:5000/api/upload/delete/products/image.jpg \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## 📞 Support

For issues or questions about file uploads:
1. Check the logs for detailed error messages
2. Verify file meets validation requirements
3. Ensure proper authentication and authorization
4. Check uploads directory permissions

---

**Last Updated:** Phase 6 Completion  
**Version:** 1.0.0
