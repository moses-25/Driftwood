# Backend Development Notes - Flask + Database Architecture

## Phase 1: Foundation & Project Setup

### 1. Project Structure Strategy

**Why Structure Matters:**
- Separates concerns for maintainability
- Makes code easier to navigate and debug
- Enables team collaboration
- Supports testing and deployment

**Standard Flask Project Structure:**
```
project/
├── app.py              # Application entry point & factory
├── config.py           # Environment configurations
├── extensions.py       # Flask extensions initialization
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (never commit)
├── models/            # Database models (one per file)
├── routes/            # API endpoints (organized by feature)
├── services/          # Business logic layer
├── utils/             # Helper functions & utilities
├── migrations/        # Database version control
├── tests/             # Test suite
└── uploads/           # File storage (if needed)
```

**Key Principles:**
- **Separation of Concerns:** Each directory has a specific purpose
- **Scalability:** Structure grows with your application
- **Modularity:** Easy to add/remove features
- **Testability:** Clear boundaries for unit testing

### 2. Configuration Management

**Environment-Based Configuration Pattern:**
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Always use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Feature flags
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    # Production should always use environment variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

**Best Practices:**
- **Never hardcode secrets** - Use environment variables
- **Provide development defaults** - Makes setup easier
- **Use different configs per environment** - dev/staging/production
- **Validate required variables** - Fail fast if missing critical config

### 3. Flask Extensions Pattern

**Extensions Setup Strategy:**
```python
# extensions.py - Initialize without app instance
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# app.py - Application factory pattern
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    return app
```

**Why This Pattern Works:**
- **Avoids circular imports** - Extensions don't depend on app instance
- **Enables testing** - Can create multiple app instances
- **Supports blueprints** - Extensions available across modules
- **Configuration flexibility** - Different setups per environment

### 4. Dependency Management

**Essential Flask Dependencies:**
```txt
# Core Framework
Flask==3.0.0
Flask-SQLAlchemy==3.1.1      # Database ORM
Flask-Migrate==4.0.5         # Database migrations
Flask-CORS==4.0.0            # Cross-origin requests

# Authentication & Security
Flask-JWT-Extended==4.6.0    # JWT tokens
Werkzeug==3.0.1              # Password hashing
bcrypt==4.1.2                # Additional hashing

# Database Drivers
psycopg2-binary==2.9.9       # PostgreSQL
# OR sqlite3 (built-in)       # SQLite for development

# Utilities
python-dotenv==1.0.0         # Environment variables
requests==2.31.0             # HTTP client
gunicorn==21.2.0             # Production server
```

**Dependency Strategy:**
- **Pin versions** - Ensures consistent deployments
- **Separate dev/prod dependencies** - Use requirements-dev.txt for development tools
- **Regular updates** - Keep dependencies current for security
- **Minimal dependencies** - Only add what you actually need

---

## Phase 2: Database Models & Architecture

### 1. Model Design Philosophy

**Core Principles:**
- **One model per file** - Easier to maintain and find
- **Consistent patterns** - Same structure across all models
- **Rich domain models** - Include business logic in models
- **Clear relationships** - Explicit foreign keys and constraints

**Standard Model Template:**
```python
from extensions import db
from datetime import datetime

class ModelName(db.Model):
    __tablename__ = 'table_name'  # Explicit table naming
    
    # Primary Key (always first)
    id = db.Column(db.Integer, primary_key=True)
    
    # Business Fields
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Status & Flags
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps (always include these)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    
    # Relationships
    children = db.relationship('Child', backref='parent', lazy=True)
    
    def to_dict(self):
        """Always include serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'
```

### 2. Database Relationships Mastery

**One-to-Many Relationship:**
```python
# Parent Model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Relationship (no foreign key here)
    products = db.relationship('Product', backref='category', lazy=True)

# Child Model  
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Foreign key (always on the "many" side)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
```

**One-to-One Relationship:**
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    
    # One-to-one (uselist=False)
    profile = db.relationship('UserProfile', backref='user', uselist=False)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
```

**Many-to-Many Relationship:**
```python
# Association table (no model class needed)
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roles = db.relationship('Role', secondary=user_roles, backref='users')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
```

### 3. Essential Model Types for Any Application

**User/Authentication Model:**
```python
class User(db.Model):
    # Identity
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    
    # Access Control
    role = db.Column(db.String(20), default='user')  # user, admin, moderator
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Security Methods
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
```

**Content/Item Model Pattern:**
```python
class Product(db.Model):  # Could be Post, Article, Item, etc.
    # Basic Info
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Categorization
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    tags = db.Column(db.Text)  # JSON string or separate table
    
    # Status
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Metrics (if applicable)
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    
    # SEO
    slug = db.Column(db.String(100), unique=True)  # URL-friendly version
```

### 4. Field Types & When to Use Them

**Text Fields:**
```python
# Short text (indexed, searchable)
name = db.Column(db.String(100), nullable=False)
email = db.Column(db.String(120), unique=True)

# Long text (not indexed)
description = db.Column(db.Text)
content = db.Column(db.Text)

# Fixed length (codes, hashes)
code = db.Column(db.CHAR(10))
```

**Numeric Fields:**
```python
# Integers
quantity = db.Column(db.Integer, default=0)
user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Decimals (for money, precise calculations)
price = db.Column(db.Numeric(10, 2))  # 10 digits, 2 decimal places
tax_rate = db.Column(db.Numeric(5, 4))  # 0.1234

# Floats (for measurements, less precision needed)
rating = db.Column(db.Float)
```

**Boolean & Status Fields:**
```python
# Simple flags
is_active = db.Column(db.Boolean, default=True)
is_deleted = db.Column(db.Boolean, default=False)

# Status enums (as strings)
status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
```

**Date & Time Fields:**
```python
# Timestamps
created_at = db.Column(db.DateTime, default=datetime.utcnow)
updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Dates only
birth_date = db.Column(db.Date)
event_date = db.Column(db.Date)

# Time only
opening_time = db.Column(db.Time)
```

### 5. Database Migration Strategy

**Migration Workflow:**
```bash
# 1. Initialize migrations (once per project)
flask db init

# 2. Create migration after model changes
flask db migrate -m "Add user table"

# 3. Review generated migration file
# Edit if needed for data migrations or custom logic

# 4. Apply migration
flask db upgrade

# 5. Rollback if needed
flask db downgrade
```

**Migration Best Practices:**
- **Small, focused migrations** - One logical change per migration
- **Descriptive messages** - Clear description of what changed
- **Review before applying** - Check generated SQL
- **Backup before major changes** - Especially in production
- **Test rollbacks** - Ensure downgrade works

### 6. Data Seeding Strategy

**Seeder Script Pattern:**
```python
def seed_database():
    # Clear existing data (development only)
    if app.config['ENV'] == 'development':
        db.drop_all()
        db.create_all()
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        role='admin'
    )
    admin.set_password('secure_password')
    db.session.add(admin)
    
    # Create categories
    categories = [
        Category(name='Electronics', description='Electronic devices'),
        Category(name='Books', description='Books and literature')
    ]
    for category in categories:
        db.session.add(category)
    
    db.session.commit()
    
    # Create products (after categories are committed)
    products = [
        Product(name='Laptop', category_id=1, price=999.99),
        Product(name='Python Book', category_id=2, price=29.99)
    ]
    for product in products:
        db.session.add(product)
    
    db.session.commit()
```

---

## Universal Best Practices

### 1. Error Handling Patterns

**Database Operations:**
```python
def create_user(username, email, password):
    try:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user, None
    except IntegrityError as e:
        db.session.rollback()
        return None, "Username or email already exists"
    except Exception as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}"
```

### 2. Query Optimization

**Efficient Queries:**
```python
# Bad: N+1 query problem
users = User.query.all()
for user in users:
    print(user.orders)  # Separate query for each user

# Good: Eager loading
users = User.query.options(db.joinedload(User.orders)).all()
for user in users:
    print(user.orders)  # No additional queries

# Pagination for large datasets
users = User.query.paginate(page=1, per_page=20, error_out=False)
```

### 3. Security Considerations

**Input Validation:**
```python
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    # At least 8 characters, one uppercase, one lowercase, one digit
    return (len(password) >= 8 and 
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password))
```

### 4. Testing Strategy

**Model Testing:**
```python
def test_user_creation():
    user = User(username='test', email='test@example.com')
    user.set_password('password123')
    
    assert user.username == 'test'
    assert user.check_password('password123')
    assert not user.check_password('wrong_password')

def test_relationships():
    category = Category(name='Test Category')
    product = Product(name='Test Product', category=category)
    
    db.session.add_all([category, product])
    db.session.commit()
    
    assert product.category == category
    assert product in category.products
```

---

## Development Workflow

### 1. Model-First Development Process

1. **Design Schema** - Plan your data relationships
2. **Create Models** - Implement one model at a time
3. **Add Relationships** - Connect models with foreign keys
4. **Create Migration** - Version control your schema
5. **Seed Data** - Create realistic test data
6. **Test Models** - Verify relationships and methods
7. **Build APIs** - Create endpoints that use your models

### 2. Common Pitfalls & Solutions

**Pitfall: Circular Imports**
```python
# Problem: models importing from each other
# Solution: Use string references in relationships
user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
orders = db.relationship('Order', backref='user')  # String reference
```

**Pitfall: Missing Migrations**
```python
# Always create migrations for schema changes
# Never modify database directly in production
flask db migrate -m "Add new column"
flask db upgrade
```

**Pitfall: Hardcoded Values**
```python
# Bad
DATABASE_URL = "postgresql://user:pass@localhost/db"

# Good
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### 3. Production Readiness Checklist

- [ ] Environment variables for all secrets
- [ ] Database migrations tested
- [ ] Proper error handling
- [ ] Input validation
- [ ] Logging configured
- [ ] Backup strategy in place
- [ ] Performance testing done
- [ ] Security review completed

---

## Quick Reference

### Essential Commands
```bash
# Project Setup
pip install -r requirements.txt
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Development
python seed_data.py          # Populate database
python -m pytest tests/      # Run tests
flask run                    # Start development server

# Database Management
flask db migrate -m "message"  # Create migration
flask db upgrade               # Apply migrations
flask db downgrade            # Rollback migration
```

### Common Patterns
```python
# Model with timestamps
created_at = db.Column(db.DateTime, default=datetime.utcnow)
updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Soft delete pattern
is_deleted = db.Column(db.Boolean, default=False)

# Status enum pattern
STATUS_CHOICES = ['pending', 'approved', 'rejected']
status = db.Column(db.String(20), default='pending')

# JSON storage pattern
metadata = db.Column(db.Text)  # Store JSON.dumps() result
```

This foundation provides a robust, scalable backend architecture that works for any Flask application, from simple blogs to complex e-commerce systems.