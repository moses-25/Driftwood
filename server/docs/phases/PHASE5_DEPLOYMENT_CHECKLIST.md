# Phase 5 Deployment Checklist

## Pre-Deployment Checklist

Use this checklist to ensure Phase 5 is properly deployed and tested.

---

## 📋 Database Migration

- [ ] **Activate virtual environment**
  ```bash
  source env/bin/activate  # Linux/Mac
  # or
  env\Scripts\activate  # Windows
  ```

- [ ] **Create migration**
  ```bash
  flask db migrate -m "Add refund fields to payments table"
  ```

- [ ] **Review migration file**
  - Check `migrations/versions/` for the new migration file
  - Verify it includes refund fields

- [ ] **Apply migration**
  ```bash
  flask db upgrade
  ```

- [ ] **Verify migration**
  ```bash
  flask db current
  ```

**Alternative: Manual SQL Migration**
- [ ] Run `add_refund_fields_migration.sql` directly on database

---

## 🔧 Configuration

- [ ] **Update .env file**
  ```env
  # M-Pesa Configuration (existing)
  MPESA_CONSUMER_KEY=your_consumer_key
  MPESA_CONSUMER_SECRET=your_consumer_secret
  MPESA_SHORTCODE=your_shortcode
  MPESA_PASSKEY=your_passkey
  
  # M-Pesa B2C (new - for refunds)
  MPESA_INITIATOR_NAME=your_initiator_name
  MPESA_SECURITY_CREDENTIAL=your_security_credential
  
  # Application URL (new - for callbacks)
  APP_URL=https://yourdomain.com
  ```

- [ ] **Verify configuration loads**
  ```bash
  python3 -c "from config import Config; print('MPESA_INITIATOR_NAME:', Config.MPESA_INITIATOR_NAME); print('APP_URL:', Config.APP_URL)"
  ```

---

## 🧪 Testing

- [ ] **Run Phase 5 test suite**
  ```bash
  python3 test_phase5.py
  ```

- [ ] **Verify all tests pass**
  - Payment Utilities: PASSED
  - Payment Service: PASSED
  - Payment Routes: PASSED
  - Payment Model: PASSED
  - Configuration: PASSED

- [ ] **Test payment initiation**
  ```bash
  curl -X POST http://localhost:5000/api/payments/mpesa/initiate \
    -H "Content-Type: application/json" \
    -d '{"order_id": 1, "phone_number": "254712345678"}'
  ```

- [ ] **Test payment query**
  ```bash
  curl -X GET http://localhost:5000/api/payments/query/ws_CO_123456789 \
    -H "Authorization: Bearer YOUR_JWT_TOKEN"
  ```

- [ ] **Test payment history**
  ```bash
  curl -X GET http://localhost:5000/api/payments/history \
    -H "Authorization: Bearer YOUR_JWT_TOKEN"
  ```

- [ ] **Test refund (admin)**
  ```bash
  curl -X POST http://localhost:5000/api/payments/1/refund \
    -H "Authorization: Bearer ADMIN_JWT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"refund_amount": 100.00, "reason": "Test refund"}'
  ```

---

## 🌐 M-Pesa Configuration

### Sandbox Testing

- [ ] **Register for M-Pesa Sandbox**
  - Visit: https://developer.safaricom.co.ke/
  - Create account
  - Get sandbox credentials

- [ ] **Configure sandbox credentials in .env**

- [ ] **Register callback URLs**
  - Payment callback: `https://yourdomain.com/api/payments/mpesa/callback`
  - Timeout callback: `https://yourdomain.com/api/payments/mpesa/timeout`
  - Refund callback: `https://yourdomain.com/api/payments/mpesa/refund-callback`

- [ ] **Test STK Push in sandbox**

- [ ] **Test callback reception**

### Production Setup

- [ ] **Get production credentials from Safaricom**

- [ ] **Update .env with production credentials**

- [ ] **Register production callback URLs**

- [ ] **Test with small amount first**

- [ ] **Monitor logs for errors**

---

## 📝 Code Review

- [ ] **Review payment_utils.py**
  - All functions documented
  - Error handling in place
  - Security measures implemented

- [ ] **Review payment_service.py**
  - Logging configured
  - Error handling comprehensive
  - Validation in place

- [ ] **Review payment_routes.py**
  - All endpoints documented
  - Authentication/authorization correct
  - Error responses standardized

- [ ] **Review payment model**
  - Refund fields added
  - to_dict() updated
  - Constraints in place

---

## 🔒 Security Checklist

- [ ] **Webhook signature verification implemented**
  - `verify_webhook_signature()` function exists
  - Used in callback handlers

- [ ] **Sensitive data sanitization**
  - `sanitize_callback_data()` used in logging
  - No passwords/secrets in logs

- [ ] **Input validation**
  - Phone numbers validated
  - Amounts validated
  - Refund amounts validated

- [ ] **Authorization checks**
  - Admin-only endpoints protected
  - User ownership verified for retry

- [ ] **HTTPS enforced**
  - Callback URLs use HTTPS
  - SSL certificate valid

---

## 📊 Monitoring

- [ ] **Set up logging**
  - Payment initiation logged
  - Callbacks logged
  - Errors logged
  - Refunds logged

- [ ] **Monitor payment success rate**
  - Track successful payments
  - Track failed payments
  - Track timeout rate

- [ ] **Set up alerts**
  - Alert on high failure rate
  - Alert on callback errors
  - Alert on refund issues

---

## 📚 Documentation

- [ ] **Review PHASE5_COMPLETE.md**
  - All features documented
  - Examples provided
  - Testing guide included

- [ ] **Review PAYMENT_API_REFERENCE.md**
  - All endpoints documented
  - Request/response examples
  - Error codes listed

- [ ] **Update backend.md**
  - Phase 5 marked complete
  - Progress summary updated

- [ ] **Share documentation with team**
  - Frontend developers
  - QA team
  - DevOps team

---

## 🚀 Deployment

### Development Environment

- [ ] **Restart development server**
  ```bash
  python3 run.py
  ```

- [ ] **Verify server starts without errors**

- [ ] **Test all endpoints**

### Staging Environment

- [ ] **Deploy to staging**

- [ ] **Run migration on staging database**

- [ ] **Update staging .env**

- [ ] **Test with M-Pesa sandbox**

- [ ] **Verify callbacks work**

- [ ] **Test refund flow**

### Production Environment

- [ ] **Deploy to production**

- [ ] **Run migration on production database**

- [ ] **Update production .env**

- [ ] **Switch to production M-Pesa credentials**

- [ ] **Test with small real payment**

- [ ] **Monitor logs for 24 hours**

- [ ] **Verify callbacks received**

---

## ✅ Post-Deployment Verification

- [ ] **Payment initiation works**
  - STK Push received on phone
  - Payment record created

- [ ] **Payment callbacks work**
  - Success callback updates payment
  - Failed callback updates payment
  - Order status updated correctly

- [ ] **Payment queries work**
  - Status query returns correct data
  - Payment history loads

- [ ] **Refunds work**
  - Admin can initiate refund
  - Refund amount validated
  - Payment status updated

- [ ] **Reports work**
  - Payment reports load
  - Statistics calculated correctly
  - Date filtering works

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Migration fails**
- Solution: Check database connection
- Solution: Review migration file for errors
- Solution: Use manual SQL migration

**Issue: M-Pesa returns "Invalid credentials"**
- Solution: Verify MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET
- Solution: Check if using correct environment (sandbox vs production)

**Issue: Callbacks not received**
- Solution: Verify callback URL is publicly accessible
- Solution: Check firewall settings
- Solution: Verify URL registered with Safaricom

**Issue: Phone number validation fails**
- Solution: Check phone number format
- Solution: Verify country code (254 for Kenya)

**Issue: Refund fails**
- Solution: Verify MPESA_INITIATOR_NAME and MPESA_SECURITY_CREDENTIAL
- Solution: Check if payment is in "completed" status
- Solution: Verify refund amount doesn't exceed original amount

---

## 📞 Support Contacts

- **M-Pesa Support:** support@safaricom.co.ke
- **Developer Portal:** https://developer.safaricom.co.ke/
- **Documentation:** See PAYMENT_API_REFERENCE.md

---

## 🎉 Completion

Once all items are checked:

- [ ] **Mark Phase 5 as deployed**
- [ ] **Update project status**
- [ ] **Notify team of completion**
- [ ] **Begin Phase 6 planning**

---

**Deployment Date:** _______________  
**Deployed By:** _______________  
**Verified By:** _______________  

---

## Next Phase

Ready to move to **Phase 6: File Upload & Media Management**?

See `backend.md` for Phase 6 details.
