# Payment API Reference Guide

## Quick Reference for Phase 5 Payment Integration

---

## 🔐 Authentication

Most payment endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Admin-only endpoints** require admin role.
**Staff endpoints** require staff or admin role.

---

## 📡 API Endpoints

### 1. Initiate M-Pesa Payment

**Endpoint:** `POST /api/payments/mpesa/initiate`  
**Auth:** None (public)  
**Description:** Initiates M-Pesa STK Push payment

**Request Body:**
```json
{
  "order_id": 1,
  "phone_number": "254712345678"
}
```

**Phone Number Formats Accepted:**
- `0712345678` (Kenyan format)
- `254712345678` (International format)
- `+254712345678` (With plus sign)

**Success Response (200):**
```json
{
  "success": true,
  "message": "Payment initiated successfully. Please check your phone to complete the payment.",
  "data": {
    "checkout_request_id": "ws_CO_123456789",
    "order_id": 1,
    "order_number": "ORD-20240101-001"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Invalid phone number format"
}
```

---

### 2. M-Pesa Payment Callback

**Endpoint:** `POST /api/payments/mpesa/callback`  
**Auth:** None (webhook)  
**Description:** Receives M-Pesa payment confirmation

**Note:** This endpoint is called by Safaricom, not by your frontend.

---

### 3. Query Payment Status

**Endpoint:** `GET /api/payments/query/<checkout_request_id>`  
**Auth:** JWT Required  
**Description:** Query M-Pesa payment status

**Example:**
```bash
GET /api/payments/query/ws_CO_123456789
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "result_code": "0",
    "result_desc": "The service request is processed successfully.",
    "status": "completed"
  }
}
```

---

### 4. Get Payment Details

**Endpoint:** `GET /api/payments/<payment_id>`  
**Auth:** JWT Required  
**Description:** Get payment details by ID

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "order_id": 1,
    "amount": 1500.00,
    "payment_method": "mpesa",
    "transaction_id": "ABC123XYZ",
    "status": "completed",
    "mpesa_receipt_number": "ABC123XYZ",
    "mpesa_phone_number": "254712345678",
    "currency": "KES",
    "refunded_amount": 0.00,
    "created_at": "2024-01-01T10:00:00",
    "completed_at": "2024-01-01T10:01:00"
  }
}
```

---

### 5. Get Order Payment

**Endpoint:** `GET /api/payments/order/<order_id>`  
**Auth:** None (public)  
**Description:** Get payment for a specific order

**Example:**
```bash
GET /api/payments/order/1
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "order_id": 1,
    "amount": 1500.00,
    "status": "completed",
    ...
  }
}
```

---

### 6. Process Refund

**Endpoint:** `POST /api/payments/<payment_id>/refund`  
**Auth:** Admin Only  
**Description:** Process full or partial refund

**Request Body (Full Refund):**
```json
{
  "reason": "Customer requested refund"
}
```

**Request Body (Partial Refund):**
```json
{
  "refund_amount": 500.00,
  "reason": "Partial refund for damaged item"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Refund initiated successfully",
  "data": {
    "refund_amount": 500.00,
    "refund_reference": "ws_CO_987654321"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Only completed payments can be refunded"
}
```

---

### 7. Retry Failed Payment

**Endpoint:** `POST /api/payments/<payment_id>/retry`  
**Auth:** JWT Required  
**Description:** Retry a failed payment

**Success Response (200):**
```json
{
  "success": true,
  "message": "Payment retry initiated",
  "data": {
    "payment_id": 2,
    "checkout_request_id": "ws_CO_123456790"
  }
}
```

---

### 8. Get Payment History

**Endpoint:** `GET /api/payments/history`  
**Auth:** JWT Required  
**Description:** Get current user's payment history

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `per_page` (int, optional): Items per page (default: 10)
- `status` (string, optional): Filter by status (pending, completed, failed, refunded)

**Example:**
```bash
GET /api/payments/history?page=1&per_page=10&status=completed
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "payments": [
      {
        "id": 1,
        "order_id": 1,
        "amount": 1500.00,
        "status": "completed",
        ...
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

---

### 9. Get Payment Reports

**Endpoint:** `GET /api/payments/reports`  
**Auth:** Staff/Admin Only  
**Description:** Get payment statistics and reports

**Query Parameters:**
- `start_date` (string, optional): Start date (YYYY-MM-DD)
- `end_date` (string, optional): End date (YYYY-MM-DD)
- `status` (string, optional): Filter by status

**Example:**
```bash
GET /api/payments/reports?start_date=2024-01-01&end_date=2024-12-31
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_payments": 150,
      "total_amount": 225000.00
    },
    "by_status": [
      {
        "status": "completed",
        "count": 120,
        "amount": 180000.00
      },
      {
        "status": "pending",
        "count": 20,
        "amount": 30000.00
      },
      {
        "status": "failed",
        "count": 10,
        "amount": 15000.00
      }
    ],
    "by_method": [
      {
        "method": "mpesa",
        "count": 130,
        "amount": 195000.00
      },
      {
        "method": "cash",
        "count": 20,
        "amount": 30000.00
      }
    ]
  }
}
```

---

## 🔄 Payment Flow

### Standard Payment Flow

```
1. Customer places order
   ↓
2. Frontend calls: POST /api/payments/mpesa/initiate
   ↓
3. Customer receives STK Push on phone
   ↓
4. Customer enters M-Pesa PIN
   ↓
5. M-Pesa sends callback to: POST /api/payments/mpesa/callback
   ↓
6. Payment status updated to "completed"
   ↓
7. Order status updated to "confirmed"
   ↓
8. Frontend can query: GET /api/payments/query/<checkout_request_id>
```

### Refund Flow

```
1. Admin initiates refund: POST /api/payments/<id>/refund
   ↓
2. System validates refund amount
   ↓
3. M-Pesa B2C refund initiated
   ↓
4. M-Pesa sends callback to: POST /api/payments/mpesa/refund-callback
   ↓
5. Payment status updated to "refunded"
   ↓
6. Order status updated to "cancelled"
```

---

## 💡 Payment Utilities

### Phone Number Validation

```python
from utils.payment_utils import validate_phone_number

is_valid, formatted = validate_phone_number("0712345678")
# Returns: (True, "254712345678")
```

### Amount Validation

```python
from utils.payment_utils import validate_amount

is_valid, error = validate_amount(100.0)
# Returns: (True, None)

is_valid, error = validate_amount(0.5)
# Returns: (False, "Amount must be at least 1.0 KES")
```

### Refund Validation

```python
from utils.payment_utils import validate_refund_amount

is_valid, error = validate_refund_amount(
    refund_amount=50.0,
    original_amount=100.0,
    already_refunded=0.0
)
# Returns: (True, None)
```

---

## 🚨 Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing/invalid JWT) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found (payment/order not found) |
| 500 | Internal Server Error |

---

## 🔒 Payment Status Values

| Status | Description |
|--------|-------------|
| `pending` | Payment initiated, waiting for confirmation |
| `completed` | Payment successful |
| `failed` | Payment failed |
| `refunded` | Full refund processed |
| `partially_refunded` | Partial refund processed |
| `cancelled` | Payment cancelled |

---

## 🌍 Environment Variables

Required environment variables for payment integration:

```env
# M-Pesa Configuration
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=your_shortcode
MPESA_PASSKEY=your_passkey

# M-Pesa B2C (for refunds)
MPESA_INITIATOR_NAME=your_initiator_name
MPESA_SECURITY_CREDENTIAL=your_security_credential

# Application URL (for callbacks)
APP_URL=https://yourdomain.com
```

---

## 🧪 Testing

### Test with cURL

**Initiate Payment:**
```bash
curl -X POST http://localhost:5000/api/payments/mpesa/initiate \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "phone_number": "254712345678"
  }'
```

**Get Payment History:**
```bash
curl -X GET "http://localhost:5000/api/payments/history?page=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Process Refund (Admin):**
```bash
curl -X POST http://localhost:5000/api/payments/1/refund \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "refund_amount": 500.00,
    "reason": "Customer requested refund"
  }'
```

---

## 📞 Support

For issues or questions about the payment integration:
1. Check the logs for detailed error messages
2. Verify M-Pesa credentials in `.env`
3. Ensure callback URLs are registered with Safaricom
4. Test with M-Pesa sandbox before production

---

**Last Updated:** Phase 5 Completion  
**Version:** 1.0.0
