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
- ⚠️ Create initial data seeders (seed_data.py exists but needs review)

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

---

### **Phase 3: Authentication & Authorization System** ⚠️ (Partially Completed)
**Goal:** Implement secure user authentication and role-based access

**Features to Implement:**
1. ⚠️ **User Registration**
   - Email validation
   - ✅ Password hashing (bcrypt) - implemented in User model
   - User role assignment (customer, admin, staff)

2. ⚠️ **User Login**
   - JWT token generation
   - Token expiration handling
   - Refresh token mechanism

3. **Authorization Middleware**
   - Route protection decorators
   - Role-based access control
   - Token validation

4. **Password Management**
   - Password reset functionality
   - Email verification

**Tasks for Phase 3:**
- ⚠️ Create authentication service (`services/auth_service.py`) - needs implementation
- [ ] Implement JWT utilities (`utils/jwt_utils.py`)
- ✅ Create auth routes (`routes/auth_routes.py`) - exists but may need completion
- ✅ Add password hashing utilities - built into User model
- [ ] Create authorization decorators (`utils/decorators.py`)

**Files Status:**
- ⚠️ `services/auth_service.py` - needs creation
- ✅ `routes/auth_routes.py` - exists
- [ ] `utils/jwt_utils.py` - needs creation
- ✅ `utils/password_utils.py` - built into User model
- [ ] `utils/decorators.py` - needs creation

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
- ✅ **Phase 2:** Database Models & Schema Design (95% - all models created, migrations applied, tables in PostgreSQL)
- ⚠️ **Phase 3:** Authentication & Authorization (30% - models ready, routes exist, needs JWT implementation)
- ⚠️ **Phase 4:** Core API Endpoints (20% - routes exist but commented out, needs service layer)
- ⚠️ **Phase 5:** Payment Integration (20% - payment service exists, needs routes and webhooks)

### Next Priority Tasks:
1. **Enable existing routes** - Uncomment menu_routes, order_routes, customer_routes in routes/__init__.py
2. **Complete authentication** - Implement JWT utilities and auth service
3. **Create service layer** - Build business logic for products, orders, users
4. **Add missing routes** - Create /api/contact and /api/newsletter endpoints
5. **Test API endpoints** - Verify all routes work with PostgreSQL

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