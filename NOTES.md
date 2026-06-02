<div align="center">

# 🚀 Backend Engineering Handbook

### *Your Personal Backend Development Playbook*

[![Backend](https://img.shields.io/badge/Focus-Backend-blue?style=for-the-badge)](.)
[![Flask](https://img.shields.io/badge/Flask-PostgreSQL-green?style=for-the-badge&logo=flask)](.)
[![API](https://img.shields.io/badge/API-REST-orange?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)](.)

*A practical guide for backend development across projects. Read this before starting any backend project.*

**📖 Reading Time:** 15-20 minutes | **🎯 Skill Level:** Junior to Senior

</div>

---

## 1. Backend Mindset

### How Backend Developers Think
- **Data first, UI second** - Model the business domain before anything else
- **Think in transactions** - What happens when multiple things need to succeed or fail together?
- **Assume malicious input** - Every request is potentially hostile
- **Plan for scale** - Even if you start small, design decisions matter
- **Business rules live in the backend** - Frontend validation is UX, backend validation is security

### Core Questions Before Coding
- What data needs to persist?
- Who can access what?
- What can go wrong?
- What happens when it fails?
- Can this scale?

---

## 2. Project Planning Checklist

Before writing any code, answer these:

### User & Roles
- [ ] Who are the users? (Admin, Customer, Guest, etc.)
- [ ] What permissions does each role have?
- [ ] Can roles change dynamically?

### Entities
- [ ] What are the core nouns in the business domain?
- [ ] What properties do they have?
- [ ] What can you do to them? (CRUD operations)

### Relationships
- [ ] How do entities relate to each other?
- [ ] One-to-one? One-to-many? Many-to-many?
- [ ] What happens when a parent is deleted? (Cascade? Restrict?)

### Business Rules
- [ ] What are the constraints? (e.g., "Users can't order more than 10 items")
- [ ] What are the workflows? (e.g., "Order → Payment → Fulfillment")
- [ ] What are the edge cases? (e.g., "What if payment fails after order creation?")

---

## 3. Database Design Workflow

### Step-by-Step Process

1. **Identify entities** → Convert nouns to tables
2. **Define attributes** → Properties become columns
3. **Add relationships** → Foreign keys and junction tables
4. **Apply constraints** → NOT NULL, UNIQUE, CHECK
5. **Normalize** → Eliminate redundancy (usually to 3NF)

### Relationship Patterns

| Pattern | Implementation | Example |
|---------|----------------|---------|
| **One-to-One** | Foreign key + UNIQUE constraint | User → Profile |
| **One-to-Many** | Foreign key on "many" side | Customer → Orders |
| **Many-to-Many** | Junction table with two FKs | Students ↔ Courses |

### Primary Keys
- Always use `id` as primary key
- Use `SERIAL` (PostgreSQL) or `AUTO_INCREMENT` (MySQL)
- UUIDs for distributed systems

### Foreign Keys
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Common Database Mistakes
- ❌ Storing computed values (store raw data, compute on query)
- ❌ Using strings for enums (use ENUM type or separate table)
- ❌ No indexes on foreign keys
- ❌ Weak constraints (allow NULL when it shouldn't be)
- ❌ Storing arrays in a single column (normalize instead)

### Normalization Quick Reference
- **1NF**: No repeating groups, atomic values
- **2NF**: No partial dependencies (all columns depend on full primary key)
- **3NF**: No transitive dependencies (non-key columns don't depend on other non-key columns)

---

## 4. API Design Workflow

### Design Before Implementation
1. List all resources (nouns)
2. Map CRUD operations to HTTP methods
3. Define URL structure
4. Design request/response formats
5. Document expected errors

### REST Conventions

| Action | Method | Endpoint | Request Body | Success Code |
|--------|--------|----------|--------------|--------------|
| List all | GET | `/users` | None | 200 |
| Get one | GET | `/users/:id` | None | 200 |
| Create | POST | `/users` | JSON | 201 |
| Update (full) | PUT | `/users/:id` | JSON | 200 |
| Update (partial) | PATCH | `/users/:id` | JSON | 200 |
| Delete | DELETE | `/users/:id` | None | 204 |

### URL Design Principles
- Use nouns, not verbs (`/users`, not `/getUsers`)
- Use plural nouns (`/products`, not `/product`)
- Nest resources logically (`/users/:id/orders`)
- Keep URLs shallow (max 2-3 levels)

### Status Codes Cheat Sheet
| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource (e.g., email exists) |
| 422 | Unprocessable Entity | Business rule violation |
| 500 | Internal Server Error | Unexpected server error |

### Pagination
```python
# Query parameters
GET /products?page=2&limit=20

# Response structure
{
  "data": [...],
  "pagination": {
    "total": 150,
    "page": 2,
    "limit": 20,
    "pages": 8
  }
}
```

### Filtering & Searching
```
GET /products?category=electronics&price_min=100&price_max=500
GET /products?search=laptop
GET /products?sort=price&order=desc
```

---

## 5. Authentication & Authorization

### Authentication Flow (JWT)
1. Client sends credentials (email/password)
2. Server validates credentials
3. Server generates JWT token
4. Client stores token (localStorage, httpOnly cookie)
5. Client sends token in `Authorization: Bearer <token>` header
6. Server validates token on protected routes

### JWT Token Structure
```python
# Payload example
{
  "user_id": 123,
  "email": "user@example.com",
  "role": "customer",
  "exp": 1735689600  # Expiration timestamp
}
```

### Role-Based Access Control (RBAC)
```python
# Decorator pattern
@app.route('/admin/users')
@require_auth
@require_role('admin')
def admin_users():
    pass

# Middleware checks:
# 1. Is token valid?
# 2. Does user exist?
# 3. Does user have required role?
```

### Common Security Mistakes
- ❌ Storing passwords in plain text (use bcrypt)
- ❌ No token expiration
- ❌ Returning sensitive data (passwords, tokens) in responses
- ❌ Not validating tokens on every protected route
- ❌ Using predictable token secrets

---

## 6. Validation Strategy

### Golden Rule
**Frontend validation = UX. Backend validation = Security.**

Always validate on the backend, even if frontend validates.

### Validation Layers

1. **Type Validation**
   - Is it a string/number/email?
   - Is it the right format?

2. **Required Fields**
   - Are all mandatory fields present?

3. **Business Rules**
   - Does it follow domain constraints?
   - Example: "Quantity must be > 0 and ≤ 100"

4. **Database Constraints**
   - Does it violate uniqueness?
   - Does foreign key reference exist?

### Validation Order
```python
# 1. Schema validation (type, required, format)
# 2. Business logic validation
# 3. Database constraints (let DB enforce)

# Bad
if not email:
    return error("Email required")
if not valid_email(email):
    return error("Invalid email")
if User.query.filter_by(email=email).first():
    return error("Email exists")

# Good - Use schema validation library
schema = UserSchema()
errors = schema.validate(request.json)
if errors:
    return {"errors": errors}, 400
```

### Error Response Format
```json
{
  "error": "Validation failed",
  "details": {
    "email": ["Invalid email format"],
    "password": ["Must be at least 8 characters"]
  }
}
```

---

## 7. Backend Folder Structure Principles

### Separation of Concerns
Each layer has one responsibility.

```
server/
├── app.py                 # Application entry point
├── config.py              # Configuration (dev/prod)
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (gitignored)
│
├── models/                # Database models (SQLAlchemy)
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   └── order.py
│
├── routes/                # API endpoints (Flask blueprints)
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   └── products.py
│
├── schemas/               # Validation schemas (Marshmallow)
│   ├── __init__.py
│   ├── user_schema.py
│   └── product_schema.py
│
├── services/              # Business logic
│   ├── __init__.py
│   ├── auth_service.py
│   └── order_service.py
│
├── middleware/            # Auth, logging, error handling
│   ├── __init__.py
│   ├── auth_middleware.py
│   └── error_handler.py
│
└── utils/                 # Helpers
    ├── __init__.py
    ├── validators.py
    └── email.py
```

### Layering Rules
- **Routes** → Handle HTTP, call services
- **Services** → Contain business logic, call models
- **Models** → Define schema, query database
- **Schemas** → Validate input/output

---

## 8. Development Workflow

### Recommended Order
1. ✅ Write down requirements
2. ✅ Design database schema
3. ✅ Create models
4. ✅ Design API endpoints (document them)
5. ✅ Implement routes (one resource at a time)
6. ✅ Add validation
7. ✅ Add authentication/authorization
8. ✅ Test each endpoint
9. ✅ Handle errors gracefully
10. ✅ Deploy

### Git Workflow
```bash
# Feature branch pattern
git checkout -b feature/user-authentication
# Work on feature
git add .
git commit -m "Add user authentication endpoints"
git push origin feature/user-authentication
# Create pull request
# After review and approval, merge to main
```

### Commit Message Conventions
- `feat: Add user registration endpoint`
- `fix: Resolve login token expiration bug`
- `refactor: Extract email validation to utility`
- `docs: Update API documentation`

---

## 9. Testing Checklist

### What to Test

- [ ] **Happy path** - Everything works as expected
- [ ] **Authentication** - Protected routes reject unauthenticated users
- [ ] **Authorization** - Users can only access their own resources
- [ ] **Validation** - Invalid input returns 400 with errors
- [ ] **Edge cases** - Empty strings, null values, extreme numbers
- [ ] **Error handling** - 500 errors return proper format
- [ ] **Database integrity** - Foreign keys, constraints enforced

### API Testing Pattern
```python
# Test structure
def test_create_user_success():
    """Test successful user creation"""
    response = client.post('/users', json={
        'email': 'test@example.com',
        'password': 'securepass'
    })
    assert response.status_code == 201
    assert 'id' in response.json

def test_create_user_duplicate_email():
    """Test user creation with existing email"""
    # Create first user
    client.post('/users', json={'email': 'test@example.com', 'password': 'pass'})
    # Try to create duplicate
    response = client.post('/users', json={'email': 'test@example.com', 'password': 'pass'})
    assert response.status_code == 409
```

### Testing Tools (Flask)
- `pytest` - Test framework
- `pytest-flask` - Flask testing utilities
- `coverage` - Code coverage

---

## 10. Debugging Framework

### When Something Breaks

**Step 1: Locate the Layer**
- Frontend issue? (Check browser console)
- Network issue? (Check network tab)
- Backend issue? (Check server logs)
- Database issue? (Check query logs)

**Step 2: Trace the Request**
```
1. Does request reach server? (Check logs)
2. Does authentication pass? (Check token)
3. Does validation pass? (Check input)
4. Does database query execute? (Check SQL logs)
5. Does response return correctly? (Check serialization)
```

**Step 3: Isolate the Problem**
- Comment out code sections
- Add print/logging statements
- Test with curl/Postman (eliminate frontend)
- Test queries directly in database (eliminate backend)

### Logging Strategy
```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log at appropriate levels
logger.debug("Detailed diagnostic info")
logger.info("User logged in: user_id=123")
logger.warning("Failed login attempt: email=user@example.com")
logger.error("Database connection failed")
logger.critical("System is down")
```

### Error Categories
| Type | Cause | Fix |
|------|-------|-----|
| 400-level | Client sent bad request | Validate input, return clear error |
| 500-level | Server error | Fix bug, add try/except |
| Database | Query error, connection issue | Check schema, connection string |
| Auth | Invalid token, missing permissions | Check token generation/validation |

---

## 11. Security Checklist

### Essential Security Measures

- [ ] **Password hashing** - Use bcrypt, never store plain text
  ```python
  from bcrypt import hashpw, gensalt, checkpw
  hashed = hashpw(password.encode('utf-8'), gensalt())
  ```

- [ ] **Input validation** - Validate and sanitize all input
- [ ] **SQL injection prevention** - Use parameterized queries (ORM handles this)
  ```python
  # Bad
  query = f"SELECT * FROM users WHERE email = '{email}'"
  
  # Good
  User.query.filter_by(email=email).first()
  ```

- [ ] **Environment variables** - Never commit secrets
  ```python
  # .env file (gitignored)
  DATABASE_URL=postgresql://localhost/mydb
  JWT_SECRET=your-secret-key
  
  # Load in app
  from dotenv import load_dotenv
  load_dotenv()
  ```

- [ ] **CORS configuration** - Restrict allowed origins
  ```python
  from flask_cors import CORS
  CORS(app, origins=["https://yourfrontend.com"])
  ```

- [ ] **Rate limiting** - Prevent abuse
  ```python
  from flask_limiter import Limiter
  limiter = Limiter(app, default_limits=["100 per hour"])
  ```

- [ ] **HTTPS only** - In production, enforce HTTPS

### Never Do This
- ❌ Return full error stack traces to clients (leaks implementation details)
- ❌ Log sensitive data (passwords, tokens, credit cards)
- ❌ Use default credentials
- ❌ Expose database IDs in URLs (use UUIDs if needed)
- ❌ Trust client-side data

---

## 12. Deployment Readiness Checklist

### Before Deploying

- [ ] **Environment variables configured**
  - Database URL
  - JWT secret
  - API keys
  - Frontend URL (for CORS)

- [ ] **Database migrations complete**
  ```bash
  flask db upgrade
  ```

- [ ] **Logging configured**
  - Log level set to INFO or WARNING
  - Logs captured (file or service like CloudWatch)

- [ ] **Error handling configured**
  - All routes wrapped in try/except
  - Global error handler registered
  ```python
  @app.errorhandler(Exception)
  def handle_error(e):
      logger.error(f"Unhandled error: {e}")
      return {"error": "Internal server error"}, 500
  ```

- [ ] **Security checks**
  - CORS configured
  - HTTPS enforced
  - Rate limiting enabled
  - Secrets not in code

- [ ] **Database backups enabled**

- [ ] **Health check endpoint**
  ```python
  @app.route('/health')
  def health():
      return {"status": "ok"}, 200
  ```

---

## 13. Senior Backend Developer Mental Models

### Core Principles

1. **Model the data before writing endpoints**
   - Good data model = easy APIs
   - Bad data model = constant refactoring

2. **Validate at every boundary**
   - API receives data? Validate.
   - Service receives data? Validate.
   - Never trust the previous layer.

3. **Never trust client input**
   - Every request is potentially malicious
   - Validate type, format, and business rules

4. **Keep business logic out of routes**
   - Routes handle HTTP (request/response)
   - Services handle business logic
   - Models handle data access

5. **Design for maintainability first**
   - Code is read 10x more than written
   - Explicit is better than clever
   - Consistency > perfection

6. **Fail fast, fail loudly**
   - Catch errors early
   - Log errors clearly
   - Return meaningful error messages

7. **Make the implicit explicit**
   - Don't assume, validate
   - Document assumptions
   - Use type hints

8. **One change at a time**
   - Small commits
   - One feature per branch
   - Easy to review, easy to revert

9. **Security is not optional**
   - It's not "extra work"
   - It's core functionality

10. **Test what can break**
    - Not everything needs 100% coverage
    - Focus on business logic and edge cases

11. **Logs are your time machine**
    - Log events, not just errors
    - Include context (user_id, request_id)
    - You'll thank yourself later

12. **The database is the source of truth**
    - Not the cache
    - Not the frontend
    - Enforce constraints at the database level

---

## Quick Reference Card

### Starting a New Backend Project

1. Understand requirements → Ask questions
2. Identify entities → List nouns
3. Design database → Draw relationships
4. Create models → Implement schema
5. Design API → Document endpoints
6. Implement routes → One resource at a time
7. Add validation → Schemas
8. Add auth → JWT + middleware
9. Test → Happy path + edge cases
10. Deploy → Checklist above

### When Stuck
- Break problem into smaller pieces
- Check logs first
- Test in isolation (Postman, database client)
- Draw it out (data flow diagrams help)
- Rubber duck it (explain to someone/something)

### Daily Habits
- Commit often, commit small
- Write clear commit messages
- Test before pushing
- Review your own code before PR
- Keep dependencies updated

---

**Remember:** Backend development is about modeling reality in data and logic. Take time to understand the domain before writing code. Good backends are boring – they work predictably, fail gracefully, and are easy to maintain.
