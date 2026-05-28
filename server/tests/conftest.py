"""
Test Configuration and Fixtures
Shared fixtures for all tests
"""
import pytest
from app import create_app
from extensions import db as _db
from models import User, Product, Category, Order, OrderItem, Payment, Review
from werkzeug.security import generate_password_hash
import os


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    # Set testing configuration
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['TESTING'] = 'True'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'JWT_SECRET_KEY': 'test-secret-key',
        'SECRET_KEY': 'test-secret-key'
    })
    
    return app


@pytest.fixture(scope='function')
def db(app):
    """Create database for testing"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app, db):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


# User Fixtures
@pytest.fixture
def admin_user(db):
    """Create admin user"""
    user = User(
        username='admin',
        email='admin@driftwood.com',
        first_name='Admin',
        last_name='User',
        role='admin',
        is_active=True,
        email_verified=True
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def staff_user(db):
    """Create staff user"""
    user = User(
        username='staff',
        email='staff@driftwood.com',
        first_name='Staff',
        last_name='User',
        role='staff',
        is_active=True,
        email_verified=True
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def customer_user(db):
    """Create customer user"""
    user = User(
        username='customer',
        email='customer@driftwood.com',
        first_name='Customer',
        last_name='User',
        role='customer',
        is_active=True,
        email_verified=True
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user



# Authentication Fixtures
@pytest.fixture
def admin_token(client, admin_user):
    """Get admin JWT token"""
    response = client.post('/api/auth/login', json={
        'email': 'admin@driftwood.com',
        'password': 'password123'
    })
    return response.json['data']['access_token']


@pytest.fixture
def staff_token(client, staff_user):
    """Get staff JWT token"""
    response = client.post('/api/auth/login', json={
        'email': 'staff@driftwood.com',
        'password': 'password123'
    })
    return response.json['data']['access_token']


@pytest.fixture
def customer_token(client, customer_user):
    """Get customer JWT token"""
    response = client.post('/api/auth/login', json={
        'email': 'customer@driftwood.com',
        'password': 'password123'
    })
    return response.json['data']['access_token']


@pytest.fixture
def admin_headers(admin_token):
    """Get admin authorization headers"""
    return {'Authorization': f'Bearer {admin_token}'}


@pytest.fixture
def staff_headers(staff_token):
    """Get staff authorization headers"""
    return {'Authorization': f'Bearer {staff_token}'}


@pytest.fixture
def customer_headers(customer_token):
    """Get customer authorization headers"""
    return {'Authorization': f'Bearer {customer_token}'}


# Category Fixtures
@pytest.fixture
def category(db):
    """Create test category"""
    category = Category(
        name='Hot Coffee',
        description='Hot coffee beverages',
        is_active=True,
        sort_order=1
    )
    db.session.add(category)
    db.session.commit()
    return category


@pytest.fixture
def categories(db):
    """Create multiple test categories"""
    cats = [
        Category(name='Hot Coffee', description='Hot beverages', is_active=True, sort_order=1),
        Category(name='Cold Coffee', description='Cold beverages', is_active=True, sort_order=2),
        Category(name='Pastries', description='Baked goods', is_active=True, sort_order=3),
    ]
    for cat in cats:
        db.session.add(cat)
    db.session.commit()
    return cats


# Product Fixtures
@pytest.fixture
def product(db, category):
    """Create test product"""
    product = Product(
        name='Espresso',
        description='Strong coffee',
        price=250,
        category_id=category.id,
        is_available=True,
        stock_quantity=100
    )
    db.session.add(product)
    db.session.commit()
    return product


@pytest.fixture
def products(db, category):
    """Create multiple test products"""
    prods = [
        Product(name='Espresso', price=250, category_id=category.id, is_available=True, stock_quantity=100),
        Product(name='Latte', price=350, category_id=category.id, is_available=True, stock_quantity=50),
        Product(name='Cappuccino', price=300, category_id=category.id, is_available=True, stock_quantity=75),
    ]
    for prod in prods:
        db.session.add(prod)
    db.session.commit()
    return prods


# Order Fixtures
@pytest.fixture
def order(db, customer_user, product):
    """Create test order"""
    order = Order(
        user_id=customer_user.id,
        total_amount=500,
        order_type='pickup',
        payment_method='cash',
        status='pending'
    )
    db.session.add(order)
    db.session.flush()
    
    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=2,
        unit_price=250,
        subtotal=500
    )
    db.session.add(order_item)
    db.session.commit()
    return order


# Payment Fixtures
@pytest.fixture
def payment(db, order):
    """Create test payment"""
    payment = Payment(
        order_id=order.id,
        amount=500,
        payment_method='mpesa',
        status='pending'
    )
    db.session.add(payment)
    db.session.commit()
    return payment


# Review Fixtures
@pytest.fixture
def review(db, customer_user, product):
    """Create test review"""
    review = Review(
        user_id=customer_user.id,
        product_id=product.id,
        rating=5,
        comment='Great coffee!',
        is_approved=True
    )
    db.session.add(review)
    db.session.commit()
    return review
