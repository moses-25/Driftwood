"""
Test to verify the test infrastructure is working correctly.

This test validates that all fixtures and factories are properly configured
and can be used to create test data.
"""

import pytest
from models import User, Product, Category, Order, Payment, Review
from tests.factories import (
    UserFactory, ProductFactory, CategoryFactory,
    OrderFactory, PaymentFactory, ReviewFactory
)


class TestInfrastructure:
    """Test suite to verify test infrastructure components."""
    
    def test_app_fixture(self, app):
        """Test that the app fixture creates a Flask application."""
        assert app is not None
        assert app.config['TESTING'] is True
        assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
    
    def test_db_fixture(self, db):
        """Test that the db fixture creates a database."""
        assert db is not None
        # Verify we can create tables
        db.create_all()
        assert True
    
    def test_client_fixture(self, client):
        """Test that the client fixture creates a test client."""
        assert client is not None
        # Make a simple request
        response = client.get('/')
        assert response is not None
    
    def test_auth_headers_fixture(self, auth_headers):
        """Test that auth_headers fixture provides valid headers."""
        assert auth_headers is not None
        assert 'Authorization' in auth_headers
        assert auth_headers['Authorization'].startswith('Bearer ')
        assert 'Content-Type' in auth_headers
    
    def test_admin_headers_fixture(self, admin_headers):
        """Test that admin_headers fixture provides valid headers."""
        assert admin_headers is not None
        assert 'Authorization' in admin_headers
        assert admin_headers['Authorization'].startswith('Bearer ')
    
    def test_sample_user_fixture(self, sample_user):
        """Test that sample_user fixture creates a user."""
        assert sample_user is not None
        assert sample_user.username == 'testuser'
        assert sample_user.email == 'testuser@example.com'
        assert sample_user.role == 'customer'
        assert sample_user.check_password('password123')
    
    def test_sample_admin_fixture(self, sample_admin):
        """Test that sample_admin fixture creates an admin user."""
        assert sample_admin is not None
        assert sample_admin.username == 'admin'
        assert sample_admin.role == 'admin'
    
    def test_sample_category_fixture(self, sample_category):
        """Test that sample_category fixture creates a category."""
        assert sample_category is not None
        assert sample_category.name == 'Coffee'
        assert sample_category.is_active is True
    
    def test_sample_product_fixture(self, sample_product):
        """Test that sample_product fixture creates a product."""
        assert sample_product is not None
        assert sample_product.name == 'Cappuccino'
        assert sample_product.price == 4.50
        assert sample_product.is_available is True
    
    def test_sample_order_fixture(self, sample_order):
        """Test that sample_order fixture creates an order."""
        assert sample_order is not None
        assert sample_order.user is not None
        assert sample_order.total_amount == 4.50
        assert len(sample_order.order_items) == 1
    
    def test_sample_payment_fixture(self, sample_payment):
        """Test that sample_payment fixture creates a payment."""
        assert sample_payment is not None
        assert sample_payment.order is not None
        assert sample_payment.payment_method == 'mpesa'
    
    def test_sample_review_fixture(self, sample_review):
        """Test that sample_review fixture creates a review."""
        assert sample_review is not None
        assert sample_review.rating == 5
        assert sample_review.comment == 'Excellent coffee!'


class TestFactories:
    """Test suite to verify factory_boy factories."""
    
    def test_user_factory(self, db):
        """Test that UserFactory creates valid users."""
        user = UserFactory()
        assert user.id is not None
        assert user.username is not None
        assert user.email is not None
        assert user.role in ['customer', 'staff', 'admin']
    
    def test_category_factory(self, db):
        """Test that CategoryFactory creates valid categories."""
        category = CategoryFactory()
        assert category.id is not None
        assert category.name is not None
        assert category.is_active is True
    
    def test_product_factory(self, db):
        """Test that ProductFactory creates valid products."""
        product = ProductFactory()
        assert product.id is not None
        assert product.name is not None
        assert product.price > 0
        assert product.category is not None
    
    def test_order_factory(self, db):
        """Test that OrderFactory creates valid orders."""
        order = OrderFactory()
        assert order.id is not None
        assert order.order_number is not None
        assert order.user is not None
        assert order.total_amount > 0
    
    def test_payment_factory(self, db):
        """Test that PaymentFactory creates valid payments."""
        payment = PaymentFactory()
        assert payment.id is not None
        assert payment.order is not None
        assert payment.amount > 0
        assert payment.payment_method in ['mpesa', 'card', 'cash']
    
    def test_review_factory(self, db):
        """Test that ReviewFactory creates valid reviews."""
        review = ReviewFactory()
        assert review.id is not None
        assert review.user is not None
        assert review.product is not None
        assert 1 <= review.rating <= 5
    
    def test_factory_batch_creation(self, db):
        """Test that factories can create multiple instances."""
        users = UserFactory.create_batch(5)
        assert len(users) == 5
        assert all(user.id is not None for user in users)
    
    def test_factory_custom_attributes(self, db):
        """Test that factories accept custom attributes."""
        user = UserFactory(username='custom_user', role='admin')
        assert user.username == 'custom_user'
        assert user.role == 'admin'


class TestDatabaseOperations:
    """Test suite to verify database operations work correctly."""
    
    def test_create_and_query_user(self, db):
        """Test creating and querying a user."""
        user = User(
            username='testuser',
            email='test@example.com',
            role='customer'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Query the user
        queried_user = User.query.filter_by(username='testuser').first()
        assert queried_user is not None
        assert queried_user.email == 'test@example.com'
        assert queried_user.check_password('password123')
    
    def test_create_product_with_category(self, db):
        """Test creating a product with a category relationship."""
        category = CategoryFactory()
        product = ProductFactory(category=category)
        
        assert product.category_id == category.id
        assert product.category.name == category.name
    
    def test_create_order_with_items(self, db, sample_user, sample_product):
        """Test creating an order with order items."""
        from models.order_item import OrderItem
        
        order = Order(
            user_id=sample_user.id,
            total_amount=sample_product.price,
            order_type='pickup',
            status='pending'
        )
        db.session.add(order)
        db.session.flush()
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=sample_product.id,
            quantity=1,
            unit_price=sample_product.price,
            subtotal=sample_product.price
        )
        db.session.add(order_item)
        db.session.commit()
        
        assert len(order.order_items) == 1
        assert order.order_items[0].product_id == sample_product.id
    
    def test_database_rollback(self, db):
        """Test that database rollback works correctly."""
        user = UserFactory()
        user_id = user.id
        
        # Start a new transaction and rollback
        db.session.rollback()
        
        # User should still exist from the factory commit
        queried_user = User.query.get(user_id)
        assert queried_user is not None


class TestAuthenticationFlow:
    """Test suite to verify authentication fixtures work correctly."""
    
    def test_generate_and_use_auth_token(self, client, auth_headers):
        """Test that auth headers can be used for authenticated requests."""
        # This tests that the token is properly formatted
        assert 'Bearer ' in auth_headers['Authorization']
        token = auth_headers['Authorization'].replace('Bearer ', '')
        assert len(token) > 0
    
    def test_different_user_roles(self, auth_headers, admin_headers, staff_headers):
        """Test that different role fixtures generate different tokens."""
        # Extract tokens
        auth_token = auth_headers['Authorization']
        admin_token = admin_headers['Authorization']
        staff_token = staff_headers['Authorization']
        
        # Tokens should be different
        assert auth_token != admin_token
        assert auth_token != staff_token
        assert admin_token != staff_token


class TestModelMethods:
    """Test suite to verify model methods work correctly."""
    
    def test_user_password_methods(self, db):
        """Test user password hashing and checking."""
        user = UserFactory()
        user.set_password('newpassword')
        db.session.commit()
        
        assert user.check_password('newpassword')
        assert not user.check_password('wrongpassword')
    
    def test_user_to_dict(self, sample_user):
        """Test user to_dict method."""
        user_dict = sample_user.to_dict()
        assert 'id' in user_dict
        assert 'username' in user_dict
        assert 'email' in user_dict
        assert 'password_hash' not in user_dict  # Should not expose password
    
    def test_product_to_dict(self, sample_product):
        """Test product to_dict method."""
        product_dict = sample_product.to_dict()
        assert 'id' in product_dict
        assert 'name' in product_dict
        assert 'price' in product_dict
        assert 'category_name' in product_dict
    
    def test_category_to_dict(self, sample_category):
        """Test category to_dict method."""
        category_dict = sample_category.to_dict()
        assert 'id' in category_dict
        assert 'name' in category_dict
        assert 'product_count' in category_dict
    
    def test_order_to_dict(self, sample_order):
        """Test order to_dict method."""
        order_dict = sample_order.to_dict()
        assert 'id' in order_dict
        assert 'order_number' in order_dict
        assert 'total_amount' in order_dict
        assert 'items' in order_dict
    
    def test_payment_to_dict(self, sample_payment):
        """Test payment to_dict method."""
        payment_dict = sample_payment.to_dict()
        assert 'id' in payment_dict
        assert 'amount' in payment_dict
        assert 'payment_method' in payment_dict
        assert 'status' in payment_dict
    
    def test_review_to_dict(self, sample_review):
        """Test review to_dict method."""
        review_dict = sample_review.to_dict()
        assert 'id' in review_dict
        assert 'rating' in review_dict
        assert 'comment' in review_dict
        assert 'user' in review_dict


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
