# Phase 5 Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you quickly set up and test Phase 5 payment integration.

---

## Step 1: Database Migration (2 minutes)

```bash
# Navigate to server directory
cd /home/moses/workspace/COFFEE/Driftwood/server

# Activate virtual environment (if you have one)
source env/bin/activate

# Apply migration
flask db migrate -m "Add refund fields to payments table"
flask db upgrade
```

**Alternative (if flask command not found):**
```bash
# Use Python module
python3 -m flask db migrate -m "Add refund fields to payments table"
python3 -m flask db upgrade
```

**Alternative (manual SQL):**
```bash
# Run SQL directly
psql -U your_username -d driftwood_cafe < add_refund_fields_migration.sql
```

---

## Step 2: Update Environment Variables (1 minute)

Add these to your `.env` file:

```env
# M-Pesa B2C (for refunds)
MPESA_INITIATOR_NAME=testapi
MPESA_SECURITY_CREDENTIAL=your_security_credential

# Application URL (for callbacks)
APP_URL=http://localhost:5000
```

---

## Step 3: Run Tests (1 minute)

```bash
python3 test_phase5.py
```

Expected output:
```
✅ ALL TESTS PASSED (5/5)
Phase 5 is ready for deployment!
```

---

## Step 4: Start Server (30 seconds)

```bash
python3 run.py
```

Server should start on `http://localhost:5000`

---

## Step 5: Test Payment Endpoint (30 seconds)

```bash
# Test payment initiation
curl -X POST http://localhost:5000/api/payments/mpesa/initiate \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "phone_number": "254712345678"
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "Payment initiated successfully...",
  "data": {
    "checkout_request_id": "ws_CO_...",
    "order_id": 1,
    "order_number": "ORD-..."
  }
}
```

---

## 🎯 What's New in Phase 5?

### New Files Created
1. ✅ `utils/payment_utils.py` - 13 utility functions
2. ✅ `test_phase5.py` - Automated test suite
3. ✅ `PHASE5_COMPLETE.md` - Full documentation
4. ✅ `PAYMENT_API_REFERENCE.md` - API reference
5. ✅ `PHASE5_DEPLOYMENT_CHECKLIST.md` - Deployment guide

### Enhanced Files
1. ✅ `services/payment_service.py` - Added refunds, retry, query
2. ✅ `routes/payment_routes.py` - Added 7 new endpoints
3. ✅ `models/payment.py` - Added refund fields
4. ✅ `config.py` - Added M-Pesa B2C config

### New API Endpoints (11 total)
1. `POST /api/payments/mpesa/initiate` - Initiate payment
2. `POST /api/payments/mpesa/callback` - Payment callback
3. `POST /api/payments/mpesa/timeout` - Timeout callback
4. `POST /api/payments/mpesa/refund-callback` - Refund callback
5. `GET /api/payments/<id>` - Get payment details
6. `GET /api/payments/order/<order_id>` - Get order payment
7. `GET /api/payments/query/<checkout_request_id>` - Query status
8. `POST /api/payments/<id>/refund` - Process refund (Admin)
9. `POST /api/payments/<id>/retry` - Retry failed payment
10. `GET /api/payments/history` - Get payment history
11. `GET /api/payments/reports` - Get payment reports (Staff)

---

## 🧪 Quick Test Commands

### Test Payment History
```bash
# Get JWT token first (login)
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}' \
  | jq -r '.access_token')

# Get payment history
curl -X GET http://localhost:5000/api/payments/history \
  -H "Authorization: Bearer $TOKEN"
```

### Test Payment Reports (Admin)
```bash
# Get admin token
ADMIN_TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@driftwood.com","password":"password123"}' \
  | jq -r '.access_token')

# Get reports
curl -X GET "http://localhost:5000/api/payments/reports?start_date=2024-01-01" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### Test Refund (Admin)
```bash
curl -X POST http://localhost:5000/api/payments/1/refund \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "refund_amount": 100.00,
    "reason": "Test refund"
  }'
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `PHASE5_COMPLETE.md` | Full completion report with all details |
| `PAYMENT_API_REFERENCE.md` | API reference with examples |
| `PHASE5_DEPLOYMENT_CHECKLIST.md` | Step-by-step deployment guide |
| `PHASE5_SUMMARY.md` | Executive summary |
| `test_phase5.py` | Automated test suite |

---

## 🔍 Verify Everything Works

Run this command to verify all components:

```bash
python3 -c "
from utils.payment_utils import validate_phone_number
from services.payment_service import PaymentService
from models.payment import Payment
from config import Config

print('✓ Payment utilities imported')
print('✓ Payment service imported')
print('✓ Payment model imported')
print('✓ Configuration imported')

# Test phone validation
is_valid, formatted = validate_phone_number('0712345678')
print(f'✓ Phone validation works: {formatted}')

# Test payment service
service = PaymentService()
print(f'✓ Payment service initialized')

print('\n✅ All Phase 5 components working!')
"
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Activate virtual environment or install dependencies
```bash
pip install -r requirements.txt
```

### "flask: command not found"
**Solution:** Use `python3 -m flask` instead of `flask`

### "Migration already exists"
**Solution:** Skip migration creation, just run upgrade
```bash
flask db upgrade
```

### "Database connection error"
**Solution:** Check DATABASE_URL in .env file

---

## ✅ Success Criteria

Phase 5 is working if:
- ✅ All tests pass (`python3 test_phase5.py`)
- ✅ Server starts without errors
- ✅ Payment initiation endpoint responds
- ✅ Payment history endpoint responds
- ✅ No errors in server logs

---

## 🎉 You're Done!

Phase 5 is complete and ready to use. You now have:
- ✅ M-Pesa payment integration
- ✅ Refund processing
- ✅ Payment history and reports
- ✅ Payment retry mechanism
- ✅ Comprehensive utilities
- ✅ Full documentation

---

## 📞 Need Help?

1. Check the logs: `tail -f logs/app.log`
2. Review documentation: `PHASE5_COMPLETE.md`
3. Run tests: `python3 test_phase5.py`
4. Check API reference: `PAYMENT_API_REFERENCE.md`

---

## 🚀 Next Steps

Ready for Phase 6?
- **Phase 6: File Upload & Media Management**
- Product image uploads
- Image optimization
- File storage management

See `backend.md` for details.

---

**Quick Start Complete!** 🎊
