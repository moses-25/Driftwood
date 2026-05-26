# Phase 4 Implementation Checklist
**Status:** 35% Complete | **Target:** 100% Complete

Use this checklist to track Phase 4 implementation progress. Check off items as you complete them.

---

## 🚨 PRIORITY 1: Guest Checkout (CRITICAL - Week 1) ✅ COMPLETE

### Product Management (Public Endpoints) ✅
- ✅ Create `services/product_service.py`
  - ✅ `get_all_products(filters, page, per_page)`
  - ✅ `get_product_by_id(product_id)`
  - ✅ `get_products_by_category(category_id)`
  - ✅ `get_featured_products()`
  - ✅ `create_product()` - Admin
  - ✅ `update_product()` - Admin
  - ✅ `delete_product()` - Admin
  - ✅ `update_stock()` - Admin
  
- ✅ Create `routes/product_routes.py`
  - ✅ `GET /api/products` - List all products (public)
  - ✅ `GET /api/products/<int:product_id>` - Get product details (public)
  - ✅ `GET /api/products/category/<int:category_id>` - Filter by category (public)
  - ✅ `GET /api/products/featured` - Featured products (public)
  - ✅ `POST /api/products` - Create product (admin)
  - ✅ `PUT /api/products/<int:product_id>` - Update product (admin)
  - ✅ `DELETE /api/products/<int:product_id>` - Delete product (admin)
  - ✅ `PUT /api/products/<int:product_id>/stock` - Update stock (admin)
  
- ✅ Register product routes in `routes/__init__.py`
- ✅ Test product endpoints

### Category Management (Public Endpoints) ✅
- ✅ Create `services/category_service.py`
  - ✅ `get_all_categories(include_inactive=False)`
  - ✅ `get_category_by_id(category_id)`
  - ✅ `get_category_products(category_id)`
  - ✅ `create_category()` - Admin
  - ✅ `update_category()` - Admin
  - ✅ `delete_category()` - Admin
  - ✅ `reorder_categories()` - Admin
  
- ✅ Create `routes/category_routes.py`
  - ✅ `GET /api/categories` - List all categories (public)
  - ✅ `GET /api/categories/<int:category_id>` - Get category details (public)
  - ✅ `GET /api/categories/<int:category_id>/products` - Category products (public)
  - ✅ `POST /api/categories` - Create category (admin)
  - ✅ `PUT /api/categories/<int:category_id>` - Update category (admin)
  - ✅ `DELETE /api/categories/<int:category_id>` - Delete category (admin)
  - ✅ `PUT /api/categories/reorder` - Reorder categories (admin)
  
- ✅ Register category routes in `routes/__init__.py`
- ✅ Test category endpoints

### Order Management (Guest + Authenticated) ✅
- ✅ Create `services/order_service.py`
  - ✅ `create_order(user_id, items, order_data)` - Support guest (user_id=None)
  - ✅ `get_order_by_id(order_id)`
  - ✅ `get_order_by_number(order_number)`
  - ✅ `validate_order_items(items)`
  - ✅ `calculate_order_total(items)`
  - ✅ `get_user_orders()` - User order history
  - ✅ `get_all_orders()` - Admin/staff
  - ✅ `update_order_status()` - Staff/admin
  - ✅ `cancel_order()` - User/admin
  
- ✅ Refactor `routes/order_routes.py`
  - ✅ Replace `Customer` model with `User` model
  - ✅ Replace `MenuItem` model with `Product` model
  - ✅ Move business logic to OrderService
  - ✅ Support guest checkout (optional authentication)
  - ✅ `POST /api/orders` - Create order
  - ✅ `GET /api/orders/<order_number>` - Get order status
  - ✅ `GET /api/orders/<int:order_id>` - Get order details
  - ✅ `GET /api/orders` - List all orders (staff/admin)
  - ✅ `GET /api/orders/my-orders` - User's orders
  - ✅ `PUT /api/orders/<int:order_id>/status` - Update status (staff/admin)
  - ✅ `DELETE /api/orders/<int:order_id>` - Cancel order
  
- ✅ Uncomment order routes in `routes/__init__.py`
- ✅ Test order creation flow (guest and authenticated)

### Payment Integration ✅
- ✅ Create `routes/payment_routes.py`
  - ✅ `POST /api/payments/mpesa/initiate` - Initiate M-Pesa payment
  - ✅ `POST /api/payments/mpesa/callback` - M-Pesa webhook handler
  - ✅ `GET /api/payments/<int:payment_id>` - Get payment status
  - ✅ `GET /api/payments/order/<int:order_id>` - Get order payment
  
- ✅ Enhance `services/payment_service.py`
  - ✅ Add callback handler logic
  - ✅ Add payment verification
  - ✅ Add transaction logging
  
- ✅ Register payment routes in `routes/__init__.py`
- ✅ Test M-Pesa integration (sandbox)

### Validation & Utilities ✅
- ✅ Create enhanced validators in `utils/validators.py`
  - ✅ `validate_order_data(data)` - In OrderService
  - ✅ `validate_order_items(items)` - In OrderService
  - ✅ `validate_product_data(data)` - In ProductService
  - ✅ `validate_price(price)` - In ProductService
  
- ⚠️ Create `utils/response_formatter.py` (Optional - using inline responses)
  - ⚠️ `success_response(data, message, status_code)` - Not critical
  - ⚠️ `error_response(error, status_code)` - Not critical
  - ⚠️ `paginated_response(items, page, per_page, total)` - Not critical

### Testing ✅
- ✅ Test complete guest checkout flow
- ✅ Test product listing and filtering
- ✅ Test order creation
- ✅ Test M-Pesa payment initiation
- ✅ Test order status retrieval
- ✅ Created `test_phase4.py` test script

---

## 📋 PRIORITY 2: User Management (HIGH - Week 2)

### User Service & Routes
- [ ] Create `services/user_service.py`
  - [ ] `get_user_by_id(user_id)`
  - [ ] `get_user_by_email(email)`
  - [ ] `update_user_profile(user_id, data)`
  - [ ] `get_user_orders(user_id, filters)`
  - [ ] `list_users(page, per_page, filters)` - Admin only
  - [ ] `deactivate_user(user_id)` - Admin only
  
- [ ] Create `routes/user_routes.py`
  - [ ] `GET /api/users/me` - Get current user profile
  - [ ] `PUT /api/users/me` - Update current user profile
  - [ ] `GET /api/users/me/orders` - Get user's order history
  - [ ] `GET /api/users` - List all users (admin)
  - [ ] `GET /api/users/<int:user_id>` - Get user by ID (admin)
  - [ ] `PUT /api/users/<int:user_id>` - Update user (admin)
  - [ ] `DELETE /api/users/<int:user_id>` - Delete user (admin)
  
- [ ] Register user routes in `routes/__init__.py`
- [ ] Add proper authorization decorators
- [ ] Test user management endpoints

---

## 🔧 PRIORITY 3: Admin Product Management (MEDIUM - Week 3)

### Admin Product Features
- [ ] Enhance `services/product_service.py`
  - [ ] `create_product(data)`
  - [ ] `update_product(product_id, data)`
  - [ ] `delete_product(product_id)` - Soft delete
  - [ ] `update_stock(product_id, quantity)`
  - [ ] `search_products(query)`
  
- [ ] Add admin routes to `routes/product_routes.py`
  - [ ] `POST /api/products` - Create product (admin)
  - [ ] `PUT /api/products/<int:product_id>` - Update product (admin)
  - [ ] `DELETE /api/products/<int:product_id>` - Delete product (admin)
  - [ ] `GET /api/products/search?q=<query>` - Search products
  
- [ ] Add `@admin_required` decorators
- [ ] Test admin product management

### Admin Category Features
- [ ] Enhance `services/category_service.py`
  - [ ] `create_category(data)`
  - [ ] `update_category(category_id, data)`
  - [ ] `delete_category(category_id)` - Soft delete
  - [ ] `reorder_categories(category_ids)`
  
- [ ] Add admin routes to `routes/category_routes.py`
  - [ ] `POST /api/categories` - Create category (admin)
  - [ ] `PUT /api/categories/<int:category_id>` - Update category (admin)
  - [ ] `DELETE /api/categories/<int:category_id>` - Delete category (admin)
  
- [ ] Add `@admin_required` decorators
- [ ] Test admin category management

---

## 📦 PRIORITY 4: Order Management (MEDIUM - Week 3)

### Staff/Admin Order Features
- [ ] Enhance `services/order_service.py`
  - [ ] `get_all_orders(filters, page, per_page)` - Staff/Admin
  - [ ] `get_user_orders(user_id, filters)` - User's own orders
  - [ ] `update_order_status(order_id, status)` - Staff/Admin
  - [ ] `cancel_order(order_id)` - User or Admin
  
- [ ] Add order management routes to `routes/order_routes.py`
  - [ ] `GET /api/orders` - List all orders (staff/admin)
  - [ ] `GET /api/orders/<int:order_id>` - Get order details (owner/staff/admin)
  - [ ] `PUT /api/orders/<int:order_id>/status` - Update status (staff/admin)
  - [ ] `DELETE /api/orders/<int:order_id>` - Cancel order (owner/admin)
  
- [ ] Add proper authorization (owner, staff, admin)
- [ ] Test order management features

---

## ⭐ PRIORITY 5: Reviews (LOW - Week 4)

### Review System
- [ ] Create `services/review_service.py`
  - [ ] `create_review(user_id, product_id, rating, comment)`
  - [ ] `get_product_reviews(product_id, page, per_page)`
  - [ ] `get_user_reviews(user_id)`
  - [ ] `update_review(review_id, data)`
  - [ ] `delete_review(review_id)`
  - [ ] `moderate_review(review_id, is_approved)` - Admin
  
- [ ] Create `routes/review_routes.py`
  - [ ] `GET /api/products/<int:product_id>/reviews` - List reviews (public)
  - [ ] `POST /api/products/<int:product_id>/reviews` - Create review (authenticated)
  - [ ] `PUT /api/reviews/<int:review_id>` - Update review (owner)
  - [ ] `DELETE /api/reviews/<int:review_id>` - Delete review (owner/admin)
  
- [ ] Register review routes in `routes/__init__.py`
- [ ] Add authorization (owner can edit, admin can moderate)
- [ ] Test review system

---

## 🧹 CLEANUP & REFACTORING

### Legacy Code Removal
- [ ] Delete `routes/menu_routes.py` (replaced by product_routes.py)
- [ ] Delete `routes/customer_routes.py` (replaced by user_routes.py)
- [ ] Consider deprecating `MenuItem` model (keep for backward compatibility)
- [ ] Remove `Customer` model references completely

### Code Quality Improvements
- [ ] Create `utils/error_handlers.py`
  - [ ] Global 404 handler
  - [ ] Global 500 handler
  - [ ] Validation error handler
  - [ ] Authorization error handler
  
- [ ] Create request schemas (optional - using marshmallow/pydantic)
  - [ ] `schemas/product_schema.py`
  - [ ] `schemas/order_schema.py`
  - [ ] `schemas/category_schema.py`
  - [ ] `schemas/review_schema.py`
  
- [ ] Standardize response formats across all endpoints
- [ ] Add comprehensive docstrings to all services
- [ ] Add type hints to service methods

---

## 🧪 TESTING

### Unit Tests
- [ ] `tests/test_product_service.py`
- [ ] `tests/test_category_service.py`
- [ ] `tests/test_order_service.py`
- [ ] `tests/test_user_service.py`
- [ ] `tests/test_review_service.py`
- [ ] `tests/test_validators.py`

### Integration Tests
- [ ] `tests/test_product_routes.py`
- [ ] `tests/test_category_routes.py`
- [ ] `tests/test_order_routes.py`
- [ ] `tests/test_user_routes.py`
- [ ] `tests/test_payment_routes.py`
- [ ] `tests/test_review_routes.py`

### End-to-End Tests
- [ ] Guest checkout flow
- [ ] Authenticated user order flow
- [ ] M-Pesa payment flow
- [ ] Admin product management flow
- [ ] Order status update flow

---

## 📊 Progress Tracking

**Overall Phase 4 Progress:** 35% → **85%** ✅ (MVP COMPLETE)

| Component | Before | Current | Target | Status |
|-----------|--------|---------|--------|--------|
| Models | 100% | 100% | 100% | ✅ Complete |
| Auth System | 100% | 100% | 100% | ✅ Complete |
| Service Layer | 20% | 85% | 100% | ✅ MVP Complete |
| Routes | 35% | 90% | 100% | ✅ MVP Complete |
| Validators | 40% | 70% | 100% | ✅ Sufficient |
| Serializers | 0% | 0% | 100% | ⚠️ Using to_dict() |
| Tests | 30% | 40% | 100% | ⚠️ Manual tests ready |

**Priority 1 (Guest Checkout): 100% COMPLETE** ✅

---

## 🎯 Success Criteria

Phase 4 is complete when:
- [ ] All CRUD endpoints are implemented and working
- [ ] Guest checkout flow works end-to-end
- [ ] M-Pesa payment integration works
- [ ] Admin can manage products, categories, and orders
- [ ] Users can view their order history
- [ ] All endpoints have proper authentication/authorization
- [ ] All endpoints have input validation
- [ ] All endpoints return consistent response formats
- [ ] Service layer handles all business logic
- [ ] Comprehensive tests cover all features
- [ ] No legacy code remains (MenuItem, Customer models)

---

**Last Updated:** May 26, 2026  
**Next Review:** After Priority 1 completion
