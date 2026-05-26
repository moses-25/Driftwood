# API Endpoints Reference
**Driftwood Cafe Backend - Phase 4**

Quick reference for all implemented API endpoints.

---

## 🔓 Public Endpoints (No Auth Required)

### Products
```
GET    /api/products                      List all products (with pagination, search, filters)
GET    /api/products/<id>                 Get product details with reviews
GET    /api/products/category/<id>        Get products by category
GET    /api/products/featured             Get featured products
```

### Categories
```
GET    /api/categories                    List all categories
GET    /api/categories/<id>               Get category details
GET    /api/categories/<id>/products      Get products in category
```

### Orders (Guest Checkout)
```
POST   /api/orders                        Create order (guest or authenticated)
GET    /api/orders/<order_number>         Track order by number (guest)
```

### Payments
```
POST   /api/payments/mpesa/initiate       Initiate M-Pesa payment
POST   /api/payments/mpesa/callback       M-Pesa webhook (called by Safaricom)
GET    /api/payments/order/<order_id>     Get payment status for order
```

### Health Check
```
GET    /api/health                        Server health check
GET    /                                  Welcome message
```

---

## 🔐 Authenticated Endpoints (JWT Required)

### User Orders
```
GET    /api/orders/my-orders              Get current user's orders
GET    /api/orders/<id>                   Get order details (owner only)
DELETE /api/orders/<id>                   Cancel order (owner only)
```

### Payments
```
GET    /api/payments/<id>                 Get payment details
```

---

## 👥 Staff/Admin Endpoints (JWT + Role Required)

### Order Management (Staff/Admin)
```
GET    /api/orders                        List all orders (with filters)
PUT    /api/orders/<id>/status            Update order status
```

---

## 👑 Admin Only Endpoints (JWT + Admin Role Required)

### Product Management
```
POST   /api/products                      Create new product
PUT    /api/products/<id>                 Update product
DELETE /api/products/<id>                 Delete product (soft delete)
PUT    /api/products/<id>/stock           Update product stock
```

### Category Management
```
POST   /api/categories                    Create new category
PUT    /api/categories/<id>               Update category
DELETE /api/categories/<id>               Delete category (soft delete)
PUT    /api/categories/reorder            Reorder categories
```

---

## 📝 Request/Response Examples

### Create Order (Guest Checkout)
```bash
POST /api/orders
Content-Type: application/json

{
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "customizations": {
        "size": "large",
        "milk": "oat"
      }
    }
  ],
  "order_type": "pickup",
  "payment_method": "mpesa",
  "delivery_address": "123 Main St",
  "delivery_fee": 100
}

Response (201):
{
  "success": true,
  "message": "Order created successfully",
  "data": {
    "id": 1,
    "order_number": "ABC12345",
    "total_amount": 750,
    "status": "pending",
    ...
  }
}
```

### Get Products with Filters
```bash
GET /api/products?page=1&per_page=20&category_id=1&search=coffee&is_available=true

Response (200):
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Espresso",
      "price": 250,
      "category_name": "Hot Coffee",
      ...
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 50,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

### Create Product (Admin)
```bash
POST /api/products
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Caramel Latte",
  "description": "Smooth espresso with caramel",
  "price": 350,
  "category_id": 1,
  "stock_quantity": 100,
  "tag": "Featured"
}

Response (201):
{
  "success": true,
  "message": "Product created successfully",
  "data": {
    "id": 18,
    "name": "Caramel Latte",
    ...
  }
}
```

### Initiate M-Pesa Payment
```bash
POST /api/payments/mpesa/initiate
Content-Type: application/json

{
  "order_id": 1,
  "phone_number": "254712345678"
}

Response (200):
{
  "success": true,
  "message": "Payment initiated successfully",
  "data": {
    "checkout_request_id": "ws_CO_123456789",
    "order_id": 1,
    "order_number": "ABC12345"
  }
}
```

### Update Order Status (Staff)
```bash
PUT /api/orders/1/status
Authorization: Bearer <staff_token>
Content-Type: application/json

{
  "status": "preparing"
}

Response (200):
{
  "success": true,
  "message": "Order status updated successfully",
  "data": {
    "id": 1,
    "status": "preparing",
    ...
  }
}
```

---

## 🔑 Authentication

### Get Token
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response (200):
{
  "success": true,
  "data": {
    "user": {...},
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Use Token
```bash
GET /api/orders/my-orders
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 📊 Query Parameters

### Products
- `page` (int) - Page number (default: 1)
- `per_page` (int) - Items per page (default: 20, max: 100)
- `category_id` (int) - Filter by category
- `search` (string) - Search in name/description
- `is_available` (bool) - Filter by availability (default: true)

### Categories
- `include_inactive` (bool) - Include inactive categories (default: false)

### Orders (Admin/Staff)
- `page` (int) - Page number
- `per_page` (int) - Items per page
- `status` (string) - Filter by status (pending, confirmed, preparing, ready, completed, cancelled)
- `order_type` (string) - Filter by type (pickup, delivery)

### User Orders
- `page` (int) - Page number
- `per_page` (int) - Items per page
- `status` (string) - Filter by status

---

## ⚠️ Error Responses

All endpoints return consistent error format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

### Common Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `409` - Conflict (duplicate entry)
- `500` - Internal Server Error

---

## 🧪 Testing

### Using cURL
```bash
# Get products
curl http://localhost:5000/api/products

# Create order
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"items":[{"product_id":1,"quantity":2}],"order_type":"pickup","payment_method":"cash"}'

# With authentication
curl http://localhost:5000/api/orders/my-orders \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Using Python Test Script
```bash
python test_phase4.py
```

---

## 📚 Additional Resources

- **Backend Guide:** `backend.md`
- **Auth Reference:** `AUTH_QUICK_REFERENCE.md`
- **Phase 4 Summary:** `PHASE4_COMPLETION_SUMMARY.md`
- **Audit Report:** `PHASE4_AUDIT_REPORT.md`

---

**Last Updated:** May 26, 2026  
**API Version:** 1.0  
**Base URL:** `http://localhost:5000/api` (development)
