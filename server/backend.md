# Backend Development Guide - Driftwood Cafe
## Complete Flask + PostgreSQL Backend Implementation

This guide will walk you through building a complete backend system for Driftwood Cafe using Python, Flask, and PostgreSQL. Each phase builds upon the previous one, making it easy to follow and implement step by step.

---

## 🎯 Project Overview

**Tech Stack:**
- **Backend Framework:** Flask (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migration Tool:** Flask-Migrate
- **API Style:** RESTful APIs
- **Authentication:** JWT (JSON Web Tokens)
- **Payment Integration:** M-Pesa (Kenya)
- **File Handling:** Local storage with upload capabilities

**Project Structure:**
```
server/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions initialization
├── requirements.txt    # Python dependencies
├── models/            # Database models
├── routes/            # API route handlers
├── services/          # Business logic layer
├── utils/             # Helper functions
├── migrations/        # Database migration files
└── tests/             # Unit and integration tests
```

---

##  Development Phases

### **Phase 1: Foundation Setup** ✅ (Already Done)
**Goal:** Set up the basic Flask application structure

**What's Already Implemented:**
- ✅ Flask app initialization (`app.py`)
- ✅ Configuration management (`config.py`)
- ✅ Extensions setup (`extensions.py`)
- ✅ Basic dependencies (`requirements.txt`)
- ✅ CORS configuration
- ✅ Database connection setup

**Files to Review:**
- `app.py` - Main application factory
- `config.py` - Environment variables and settings
- `extensions.py` - Flask extensions
- `requirements.txt` - Dependencies

---

### **Phase 2: Database Models & Schema Design** ✅ (Completed)
**Goal:** Create all database models and relationships

**Models to Create:**
1. ✅ **User Model** (`models/user.py`)
   - Fields: id, username, email, password_hash, role, created_at, updated_at
   - Relationships: orders, reviews

2. ✅ **Category Model** (`models/category.py`)
   - Fields: id, name, description, is_active, created_at
   - Relationships: products

3. ✅ **Product Model** (`models/product.py`)
   - Fields: id, name, description, price, category_id, image_url, is_available, created_at
   - Relationships: category, order_items, reviews

4. ✅ **Order Model** (`models/order.py`)
   - Fields: id, user_id, total_amount, status, payment_status, created_at, updated_at
   - Relationships: user, order_items, payment

5. ✅ **OrderItem Model** (`models/order_item.py`)
   - Fields: id, order_id, product_id, quantity, unit_price, subtotal
   - Relationships: order, product

6. ✅ **Payment Model** (`models/payment.py`)
   - Fields: id, order_id, amount, payment_method, transaction_id, status, created_at
   - Relationships: order

7. ✅ **Review Model** (`models/review.py`)
   - Fields: id, user_id, product_id, rating, comment, created_at
   - Relationships: user, product

**Tasks for Phase 2:**
- ✅ Create each model file with proper fields and relationships
- ✅ Set up database migrations
- ✅ Test model relationships (all foreign keys verified)
- ✅ Create initial data seeders (seed_data.py tested and working)

**Seed Data Summary:**
- ✅ 5 Categories (Hot Coffee, Cold Coffee, Pastries, Specials, Merchandise)
- ✅ 17 Products (various coffee drinks, pastries, and merchandise)
- ✅ 5 Users (1 admin, 1 staff, 3 customers)
- ✅ 10 Sample Orders with 25 order items
- ✅ 5 Payment records
- ✅ 2 Sample reviews

**Test Credentials:**
- Admin: `admin@driftwood.com` / `password123`
- Staff: `staff@driftwood.com` / `password123`
- Customer: `john@example.com` / `password123`

**Files Created:**
- ✅ `models/__init__.py`
- ✅ `models/user.py`
- ✅ `models/category.py`
- ✅ `models/product.py`
- ✅ `models/order.py`
- ✅ `models/order_item.py`
- ✅ `models/payment.py`
- ✅ `models/review.py`
- ✅ `models/menu_item.py` (bonus legacy model)
- ✅ `seed_data.py` (fully functional)

---

### **Phase 3: Authentication & Authorization System** ✅ (100% Completed)
**Goal:** Implement secure user authentication and role-based access

**Features Implemented:**
1. ✅ **User Registration** (COMPLETED)
   - ✅ Email validation - implemented with RFC 5322 regex
   - ✅ Password hashing (bcrypt) - implemented in User model
   - ✅ User role assignment (customer, admin, staff) - default role set to 'customer'
   - ✅ JWT token generation on registration - returns access & refresh tokens
   - ✅ Strong password validation (8+ chars, uppercase, lowercase, digit, special char)

2. ✅ **User Login** (COMPLETED)
   - ✅ Login endpoint implemented (`POST /api/auth/login`)
   - ✅ JWT token generation (access & refresh tokens)
   - ✅ Token expiration configured (1 hour access, 30 days refresh)
   - ✅ Last login timestamp tracking
   - ✅ Account status validation (is_active check)

3. ✅ **Authorization Middleware** (COMPLETED)
   - ✅ Route protection decorators (@jwt_required)
   - ✅ Role-based access control decorators (@role_required, @admin_required, @staff_required)
   - ✅ Token validation middleware
   - ✅ Role hierarchy (admin > staff > customer)

4. ✅ **Password Management** (COMPLETED)
   - ✅ Password change functionality (requires old password)
   - ✅ Password reset request endpoint
   - ✅ Password reset with token
   - ✅ Email verification endpoint

**Implemented Endpoints:**
- ✅ `POST /api/auth/register` - Register new user
- ✅ `POST /api/auth/login` - Login user
- ✅ `POST /api/auth/refresh` - Refresh access token
- ✅ `GET /api/auth/me` - Get current user info
- ✅ `POST /api/auth/change-password` - Change password
- ✅ `POST /api/auth/request-password-reset` - Request password reset
- ✅ `POST /api/auth/reset-password` - Reset password with token
- ✅ `POST /api/auth/verify-email` - Verify email address

**Files Created:**
- ✅ `services/auth_service.py` - Authentication business logic
- ✅ `routes/auth_routes.py` - All auth endpoints implemented
- ✅ `utils/jwt_utils.py` - JWT token generation and validation
- ✅ `utils/decorators.py` - @jwt_required, @role_required, @admin_required, @staff_required
- ✅ `utils/validators.py` - Email, password, username, phone validation
- ✅ `routes/protected_example.py` - Example protected routes demonstrating decorator usage
- ✅ `test_auth.py` - Comprehensive authentication test script

**What's Working:**
- ✅ JWT configured in extensions.py and app.py
- ✅ JWT secret key and expiration times set in config.py
- ✅ User registration with validation
- ✅ User login with credential verification
- ✅ Token refresh mechanism
- ✅ Password hashing with bcrypt
- ✅ Access & refresh token generation
- ✅ Protected routes with @jwt_required
- ✅ Role-based access control with role hierarchy
- ✅ Password change and reset
- ✅ Email verification
- ✅ Input validation (email, password, username)

**Testing:**
All authentication features have been tested and verified:
- ✅ User registration works
- ✅ User login works
- ✅ Token refresh works
- ✅ Protected routes work
- ✅ Role-based access control works (admin can access all, staff can access staff+customer, customer can access customer only)
- ✅ Password change works
- ✅ Password validation works (rejects weak passwords)
- ✅ Last login timestamp updates correctly

---

### **Phase 4: Core API Endpoints** ⚠️ (Partially Completed)
**Goal:** Build all CRUD operations for main entities

**API Endpoints to Create:**

**1. User Management APIs**
- `GET /api/users` - List users (admin only)
- `GET /api/users/{id}` - Get user profile
- `PUT /api/users/{id}` - Update user profile
- `DELETE /api/users/{id}` - Delete user (admin only)

**2. Category Management APIs**
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create category (admin only)
- `PUT /api/categories/{id}` - Update category (admin only)
- `DELETE /api/categories/{id}` - Delete category (admin only)

**3. Product Management APIs**
- `GET /api/products` - List products with filtering
- `GET /api/products/{id}` - Get product details
- `POST /api/products` - Create product (admin only)
- `PUT /api/products/{id}` - Update product (admin only)
- `DELETE /api/products/{id}` - Delete product (admin only)

**4. Order Management APIs**
- `GET /api/orders` - List user orders
- `GET /api/orders/{id}` - Get order details
- `POST /api/orders` - Create new order
- `PUT /api/orders/{id}` - Update order status (staff/admin)
- `DELETE /api/orders/{id}` - Cancel order

**Tasks for Phase 4:**
- [ ] Create service layer for each entity
- ⚠️ Implement route handlers (some exist but commented out)
- [ ] Add input validation
- [ ] Create response serializers
- [ ] Add error handling

**Files Status:**
- [ ] `routes/user_routes.py` - needs creation
- [ ] `routes/category_routes.py` - needs creation
- [ ] `routes/product_routes.py` - needs creation
- ✅ `routes/order_routes.py` - exists (but commented out in __init__.py)
- ✅ `routes/menu_routes.py` - exists (but commented out in __init__.py)
- ✅ `routes/customer_routes.py` - exists (but commented out in __init__.py)
- [ ] `services/user_service.py` - needs creation
- [ ] `services/product_service.py` - needs creation
- [ ] `services/order_service.py` - needs creation
- [ ] `utils/validators.py` - needs creation
- [ ] `utils/serializers.py` - needs creation

---

### **Phase 5: Payment Integration** ⚠️ (Partially Completed)
**Goal:** Integrate M-Pesa payment system

**Features to Implement:**
1. **M-Pesa STK Push**
   - Initiate payment requests
   - Handle payment callbacks
   - Payment status tracking

2. **Payment Processing**
   - Order payment workflow
   - Payment confirmation
   - Failed payment handling

3. **Payment History**
   - Transaction logging
   - Payment reports
   - Refund processing

**Tasks for Phase 5:**
- ✅ Create M-Pesa service (`services/mpesa_service.py`) - exists as payment_service.py
- [ ] Implement payment routes (`routes/payment_routes.py`)
- [ ] Add webhook handlers for callbacks
- [ ] Create payment utilities (`utils/payment_utils.py`)

**Files Status:**
- ✅ `services/payment_service.py` - exists (check if M-Pesa is implemented)
- [ ] `routes/payment_routes.py` - needs creation
- [ ] `utils/payment_utils.py` - needs creation

---

### **Phase 6: File Upload & Media Management**
**Goal:** Handle product images and file uploads

**Features to Implement:**
1. **Image Upload**
   - Product image upload
   - Image validation and processing
   - File size and type restrictions

2. **File Management**
   - Secure file storage
   - File URL generation
   - Image optimization

**Tasks for Phase 6:**
- [ ] Create file upload service (`services/file_service.py`)
- [ ] Implement upload routes (`routes/upload_routes.py`)
- [ ] Add image processing utilities (`utils/image_utils.py`)

**Files to Create:**
- `services/file_service.py`
- `routes/upload_routes.py`
- `utils/image_utils.py`

---

### **Phase 7: Advanced Features**
**Goal:** Add sophisticated business features

**Features to Implement:**
1. **Product Reviews & Ratings**
   - Customer reviews
   - Rating calculations
   - Review moderation

2. **Order Tracking**
   - Real-time order status
   - Notification system
   - Delivery tracking

3. **Inventory Management**
   - Stock tracking
   - Low stock alerts
   - Automatic stock updates

4. **Analytics & Reporting**
   - Sales reports
   - Popular products
   - Customer analytics

**Tasks for Phase 7:**
- [ ] Create review system (`services/review_service.py`)
- [ ] Implement notification service (`services/notification_service.py`)
- [ ] Add analytics endpoints (`routes/analytics_routes.py`)
- [ ] Create reporting utilities (`utils/report_utils.py`)

**Files to Create:**
- `services/review_service.py`
- `services/notification_service.py`
- `routes/analytics_routes.py`
- `utils/report_utils.py`

---

### **Phase 8: Testing & Quality Assurance**
**Goal:** Ensure code quality and reliability

**Testing Strategy:**
1. **Unit Tests**
   - Model tests
   - Service layer tests
   - Utility function tests

2. **Integration Tests**
   - API endpoint tests
   - Database integration tests
   - Payment integration tests

3. **Performance Tests**
   - Load testing
   - Database query optimization
   - API response time testing

**Tasks for Phase 8:**
- [ ] Set up testing framework (pytest)
- [ ] Create test fixtures and factories
- [ ] Write comprehensive test suites
- [ ] Set up continuous integration

**Files to Create:**
- `tests/conftest.py`
- `tests/test_models.py`
- `tests/test_services.py`
- `tests/test_routes.py`
- `tests/factories.py`

---

### **Phase 9: Deployment & Production Setup**
**Goal:** Deploy the application to production

**Deployment Tasks:**
1. **Environment Configuration**
   - Production environment variables
   - Database setup on production
   - SSL certificate configuration

2. **Docker Containerization**
   - Dockerfile optimization
   - Docker Compose for production
   - Container orchestration

3. **Monitoring & Logging**
   - Application logging
   - Error tracking
   - Performance monitoring

**Tasks for Phase 9:**
- [ ] Configure production settings
- [ ] Set up database migrations for production
- [ ] Implement logging and monitoring
- [ ] Create deployment scripts

**Files to Create/Update:**
- `Dockerfile` (optimize existing)
- `docker-compose.prod.yml`
- `utils/logging_config.py`
- `deploy.sh`

---

## 🚀 Getting Started

### Prerequisites
- ✅ Python 3.8+
- ✅ PostgreSQL 12+
- ✅ Git

### Quick Start Commands
```bash
# Navigate to server directory
cd server

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Initialize database (COMPLETED ✅)
flask db init  # Already done
flask db migrate -m "Initial migration"  # Already done
flask db upgrade  # Already done

# Run the development server
python run.py
```

---

## ✅ Current Progress Summary

### Completed:
- ✅ **Phase 1:** Foundation Setup (100%)
- ✅ **Phase 2:** Database Models & Schema Design (100% - all models created, migrations applied, seed data working)
- ✅ **Phase 3:** Authentication & Authorization (100% - complete auth system with JWT, role-based access, password management)
- ⚠️ **Phase 4:** Core API Endpoints (20% - routes exist but commented out, needs service layer)
- ⚠️ **Phase 5:** Payment Integration (20% - payment service exists, needs routes and webhooks)

### Next Priority Tasks:
1. **Phase 4: Core API Endpoints** - Build guest checkout APIs (products, orders, cart)
2. **Enable existing routes** - Uncomment menu_routes, order_routes, customer_routes in routes/__init__.py
3. **Create service layer** - Build business logic for products, orders, categories
4. **Add missing routes** - Create /api/contact and /api/newsletter endpoints
5. **Phase 5: Payment Integration** - Implement M-Pesa STK Push for guest checkout

---

## 📚 Phase Implementation Guide

**How to Use This Guide:**
1. **Start with Phase 2** (Phase 1 is already complete)
2. **Complete each phase fully** before moving to the next
3. **Test each phase** before proceeding
4. **Ask for help** when implementing each phase
5. **Review and refactor** code as you progress

**For Each Phase:**
1. Read the phase description carefully
2. Understand the goals and requirements
3. Create the files listed in the "Files to Create" section
4. Implement the features step by step
5. Test the implementation
6. Move to the next phase

---

## 🔧 Development Tips

**Best Practices:**
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Write docstrings for all functions and classes
- Handle errors gracefully with proper HTTP status codes
- Use environment variables for sensitive data
- Implement proper logging throughout the application

**Common Patterns:**
- Use service layer for business logic
- Keep routes thin (delegate to services)
- Use decorators for common functionality (auth, validation)
- Implement proper error handling middleware
- Use database transactions for data consistency

---

Ready to start with Phase 2? Let me know which phase you'd like to begin with, and I'll guide you through the implementation step by step!