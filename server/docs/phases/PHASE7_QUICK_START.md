# Phase 7: Quick Start Guide

## 🚀 Getting Started with Phase 7 Features

This guide will help you quickly set up and use the Phase 7 advanced features: Analytics, Inventory Management, and Order Tracking & Notifications.

---

## 📋 Prerequisites

- Phase 1-6 completed and working
- PostgreSQL database running
- Python environment activated
- `.env` file configured

---

## ⚡ Quick Setup (5 minutes)

### Step 1: Create Database Migration

```bash
# Create migration for new tables
python create_phase7_migration.py

# Apply migration
flask db upgrade
```

### Step 2: Configure Email (Optional)

Add to your `.env` file:

```env
# Email Configuration (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**Note:** Notifications will work without email config, but emails won't be sent.

### Step 3: Restart Application

```bash
python run.py
```

### Step 4: Run Tests

```bash
python test_phase7_complete.py
```

---

## 🎯 Feature Overview

### 1. Analytics & Reporting

**What it does:** Provides business insights, sales reports, and performance metrics.

**Who can use it:** Admin and Staff

**Key endpoints:**
- `GET /api/analytics/dashboard` - Complete dashboard
- `GET /api/analytics/sales` - Sales report
- `GET /api/analytics/popular-products` - Top products

**Quick test:**
```bash
# Get dashboard (requires admin/staff token)
curl -X GET http://localhost:5000/api/analytics/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 2. Inventory Management

**What it does:** Tracks stock levels, manages inventory, and alerts on low stock.

**Who can use it:** Admin and Staff

**Key endpoints:**
- `GET /api/inventory/products` - View all stock
- `POST /api/inventory/adjust` - Adjust stock
- `GET /api/inventory/low-stock` - Low stock alerts

**Quick test:**
```bash
# View all product stock
curl -X GET http://localhost:5000/api/inventory/products \
  -H "Authorization: Bearer YOUR_TOKEN"

# Adjust stock
curl -X POST http://localhost:5000/api/inventory/adjust \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity_change": 50,
    "reason": "New stock delivery"
  }'
```

**Automatic Features:**
- ✅ Stock automatically decreases when orders are completed
- ✅ Low stock alerts generated automatically
- ✅ All changes logged in audit trail

---

### 3. Order Tracking & Notifications

**What it does:** Tracks order status changes and sends email notifications.

**Who can use it:** Everyone (public tracking available)

**Key endpoints:**
- `GET /api/orders/<id>/timeline` - Order history
- `GET /api/orders/<order_number>/track` - Public tracking
- `PUT /api/orders/<id>/status-with-tracking` - Update status (staff)

**Quick test:**
```bash
# Track order (public - no auth needed)
curl -X GET http://localhost:5000/api/orders/A1B2C3D4/track

# Get order timeline
curl -X GET http://localhost:5000/api/orders/1/timeline

# Update order status (staff/admin)
curl -X PUT http://localhost:5000/api/orders/1/status-with-tracking \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "preparing",
    "notes": "Order is being prepared"
  }'
```

**Automatic Features:**
- ✅ Email sent when order status changes
- ✅ Status history automatically tracked
- ✅ Estimated completion time calculated

---

## 📊 Common Use Cases

### Use Case 1: View Today's Sales

```bash
curl -X GET "http://localhost:5000/api/analytics/sales?start_date=2026-05-28&end_date=2026-05-28" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### Use Case 2: Check Low Stock Products

```bash
curl -X GET http://localhost:5000/api/inventory/low-stock \
  -H "Authorization: Bearer STAFF_TOKEN"
```

### Use Case 3: Update Order Status and Notify Customer

```bash
curl -X PUT http://localhost:5000/api/orders/123/status-with-tracking \
  -H "Authorization: Bearer STAFF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "ready",
    "notes": "Your order is ready for pickup!"
  }'
```

### Use Case 4: Customer Tracks Their Order

```bash
# Customer uses their order number (no login required)
curl -X GET http://localhost:5000/api/orders/A1B2C3D4/track
```

### Use Case 5: Bulk Stock Update

```bash
curl -X POST http://localhost:5000/api/inventory/bulk-update \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "updates": [
      {"product_id": 1, "quantity_change": 50, "reason": "Restock"},
      {"product_id": 2, "quantity_change": 30, "reason": "Restock"},
      {"product_id": 3, "quantity_change": 40, "reason": "Restock"}
    ]
  }'
```

---

## 🔧 Configuration Options

### Email Templates

Email templates are in `utils/email_utils.py`. You can customize:
- Order confirmed email
- Order preparing email
- Order ready email
- Order completed email
- Order cancelled email

### Notification Preferences

Users can configure their preferences:

```bash
curl -X PUT http://localhost:5000/api/notifications/preferences \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email_enabled": true,
    "order_status_updates": true,
    "promotional_emails": false
  }'
```

### Stock Thresholds

Each product has a `low_stock_threshold` field. Adjust it:

```bash
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "low_stock_threshold": 15
  }'
```

---

## 🐛 Troubleshooting

### Issue: Migration fails

**Solution:**
```bash
# Check current migration status
flask db current

# If needed, reset and reapply
flask db downgrade
flask db upgrade
```

### Issue: Emails not sending

**Check:**
1. Email configuration in `.env`
2. MAIL_USERNAME and MAIL_PASSWORD are correct
3. For Gmail, use an "App Password" not your regular password
4. Check logs for email errors

**Test email config:**
```bash
curl -X POST http://localhost:5000/api/notifications/test \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "status": "confirmed"
  }'
```

### Issue: Stock not deducting

**Check:**
1. Product has `track_inventory` set to `true`
2. Order status is being changed to `completed`
3. Check logs for stock deduction errors

**Verify:**
```bash
# Check product inventory settings
curl -X GET http://localhost:5000/api/products/1

# Check stock history
curl -X GET http://localhost:5000/api/inventory/history/1 \
  -H "Authorization: Bearer STAFF_TOKEN"
```

---

## 📚 API Documentation

### Analytics Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/analytics/sales` | GET | Admin/Staff | Sales report |
| `/api/analytics/popular-products` | GET | Admin/Staff | Top products |
| `/api/analytics/customers` | GET | Admin | Customer insights |
| `/api/analytics/orders` | GET | Admin/Staff | Order statistics |
| `/api/analytics/categories` | GET | Admin/Staff | Category performance |
| `/api/analytics/revenue-trends` | GET | Admin/Staff | Revenue trends |
| `/api/analytics/dashboard` | GET | Admin/Staff | Dashboard summary |

### Inventory Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/inventory/products` | GET | Admin/Staff | All products stock |
| `/api/inventory/product/<id>` | GET | Admin/Staff | Product stock details |
| `/api/inventory/adjust` | POST | Admin/Staff | Adjust stock |
| `/api/inventory/low-stock` | GET | Admin/Staff | Low stock products |
| `/api/inventory/out-of-stock` | GET | Admin/Staff | Out of stock products |
| `/api/inventory/history/<id>` | GET | Admin/Staff | Stock history |
| `/api/inventory/bulk-update` | POST | Admin | Bulk stock update |
| `/api/inventory/check-availability/<id>` | GET | Any | Check availability |

### Notification Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/notifications/preferences` | GET | User | Get preferences |
| `/api/notifications/preferences` | PUT | User | Update preferences |
| `/api/notifications/test` | POST | Admin | Test notification |

### Order Tracking Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/orders/<id>/timeline` | GET | Public | Order timeline |
| `/api/orders/<number>/track` | GET | Public | Track order |
| `/api/orders/<id>/status-with-tracking` | PUT | Staff/Admin | Update status |

---

## 🎓 Best Practices

### For Analytics
- Use date filters to limit data range
- Cache dashboard data for better performance
- Export reports to CSV for offline analysis

### For Inventory
- Set appropriate low stock thresholds
- Review stock history regularly
- Use bulk updates for efficiency
- Enable inventory tracking only for physical products

### For Notifications
- Test email configuration before going live
- Respect user notification preferences
- Keep email templates concise and clear
- Monitor email delivery rates

---

## 🔗 Related Documentation

- [PHASE7_COMPLETE.md](./PHASE7_COMPLETE.md) - Complete Phase 7 documentation
- [API_ENDPOINTS_REFERENCE.md](./API_ENDPOINTS_REFERENCE.md) - All API endpoints
- [backend.md](./backend.md) - Complete backend guide

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Migration applied successfully
- [ ] All 3 new tables created (stock_adjustments, order_status_history, notification_preferences)
- [ ] Analytics endpoints return data
- [ ] Inventory endpoints work
- [ ] Stock deducts when order completed
- [ ] Order timeline shows status changes
- [ ] Email configuration tested (if configured)
- [ ] Test suite passes

---

## 🎉 You're Ready!

Phase 7 is now set up and ready to use. Start exploring the new features:

1. **Check the dashboard** - See your business metrics
2. **Monitor inventory** - Keep track of stock levels
3. **Track orders** - Follow order progress in real-time

Need help? Check the [complete documentation](./PHASE7_COMPLETE.md) or run the test suite for examples.

**Happy coding!** 🚀
