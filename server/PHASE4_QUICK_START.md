# Phase 4 Quick Start Guide
**Start Here:** Your roadmap to completing Phase 4

---

## 📋 What You Need to Know

**Phase 4 Status:** 35% Complete  
**Main Blocker:** Missing service layer for core entities  
**Critical Path:** Guest checkout (Products → Orders → Payments)

---

## 🚀 Quick Action Plan

### This Week: Enable Guest Checkout

**Day 1-2: Products & Categories**
```bash
# Create these files:
touch services/product_service.py
touch services/category_service.py
touch routes/product_routes.py
touch routes/category_routes.py
```

**Day 3-4: Orders**
```bash
# Create and refactor:
touch services/order_service.py
# Edit routes/order_routes.py (already exists, needs refactoring)
```

**Day 5: Payments**
```bash
# Create:
touch routes/payment_routes.py
# Enhance services/payment_service.py (already exists)
```

---

## 📁 Files You'll Create (Priority Order)

### Week 1 (Critical)
1. `services/product_service.py` - Product business logic
2. `routes/product_routes.py` - Product API endpoints
3. `services/category_service.py` - Category business logic
4. `routes/category_routes.py` - Category API endpoints
5. `services/order_service.py` - Order business logic
6. `routes/payment_routes.py` - Payment API endpoints

### Week 2 (High Priority)
7. `services/user_service.py` - User management logic
8. `routes/user_routes.py` - User API endpoints
9. `utils/response_formatter.py` - Standardized responses

### Week 3-4 (Medium/Low Priority)
10. Admin features (enhance existing services)
11. `services/review_service.py` - Review system
12. `routes/review_routes.py` - Review endpoints
13. `utils/error_handlers.py` - Global error handling

---

## 🔧 Files You'll Refactor

1. **`routes/order_routes.py`** (EXISTS - needs fixing)
   - Replace `Customer` → `User`
   - Replace `MenuItem` → `Product`
   - Move logic to OrderService
   - Add authentication decorators

2. **`routes/__init__.py`** (EXISTS - needs updating)
   - Uncomment product/order/category routes
   - Register new route blueprints

3. **`services/payment_service.py`** (EXISTS - needs enhancement)
   - Add callback handler
   - Add payment verification
   - Add transaction logging

---

## ❌ Files You'll Delete (After Migration)

1. `routes/menu_routes.py` - Replaced by product_routes.py
2. `routes/customer_routes.py` - Replaced by user_routes.py

---

## 🎯 Your First Task: Product Service

Create `services/product_service.py` with these methods:

```python
class ProductService:
    @staticmethod
    def get_all_products(filters=None, page=1, per_page=20):
        """List all products with optional filtering"""
        pass
    
    @staticmethod
    def get_product_by_id(product_id):
        """Get single product by ID"""
        pass
    
    @staticmethod
    def get_products_by_category(category_id):
        """Get products in a category"""
        pass
```

**Reference:** Look at `services/auth_service.py` for the pattern to follow.

---

## 📚 Key Resources

- **Full Audit Report:** `PHASE4_AUDIT_REPORT.md` (detailed analysis)
- **Implementation Checklist:** `PHASE4_IMPLEMENTATION_CHECKLIST.md` (track progress)
- **Backend Guide:** `backend.md` (overall project guide)
- **Auth Reference:** `AUTH_QUICK_REFERENCE.md` (decorator usage)

---

## 🔍 What's Already Done (Don't Rebuild)

✅ **Models** - All database models complete  
✅ **Auth System** - Registration, login, JWT, decorators  
✅ **Validators** - Email, password, username, phone  
✅ **Decorators** - @jwt_required, @admin_required, @staff_required  
✅ **Payment Service** - M-Pesa integration (partial)

---

## ⚠️ Common Pitfalls to Avoid

1. **Don't use legacy models** - Use `Product` not `MenuItem`, `User` not `Customer`
2. **Don't put logic in routes** - Move business logic to services
3. **Don't forget auth decorators** - Add @admin_required, @jwt_required, etc.
4. **Don't skip validation** - Validate all inputs
5. **Don't hardcode responses** - Use consistent response format

---

## 🎓 Pattern to Follow

**Every endpoint should follow this pattern:**

```python
# 1. Route handler (thin)
@product_bp.route('/products', methods=['GET'])
def get_products():
    # Get request params
    page = request.args.get('page', 1, type=int)
    
    # Call service
    products, error, status = ProductService.get_all_products(page=page)
    
    # Return response
    if error:
        return jsonify({'success': False, 'error': error}), status
    return jsonify({'success': True, 'data': products}), status

# 2. Service layer (business logic)
class ProductService:
    @staticmethod
    def get_all_products(page=1):
        try:
            products = Product.query.paginate(page=page, per_page=20)
            return [p.to_dict() for p in products.items], None, 200
        except Exception as e:
            return None, str(e), 500
```

---

## 🚦 How to Know You're Done

Phase 4 is complete when you can:
- [ ] Browse products as a guest
- [ ] Add products to cart and checkout as a guest
- [ ] Pay with M-Pesa
- [ ] Track order status
- [ ] Login and view order history
- [ ] Admin can manage products and categories

---

## 💡 Pro Tips

1. **Start with GET endpoints** - Easier to test, no auth needed
2. **Test as you go** - Don't wait until the end
3. **Copy auth_service.py pattern** - It's well-structured
4. **Use existing decorators** - Don't reinvent authorization
5. **Keep routes thin** - All logic goes in services

---

## 🆘 Need Help?

1. Check `PHASE4_AUDIT_REPORT.md` for detailed analysis
2. Look at `services/auth_service.py` for service pattern
3. Look at `routes/auth_routes.py` for route pattern
4. Check `utils/decorators.py` for authorization examples

---

**Ready to start?** Begin with creating `services/product_service.py`!
