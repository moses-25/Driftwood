"""
Test Data Factories
Using factory_boy for generating test data
"""
import factory
from factory import fuzzy
from faker import Faker
from models import User, Product, Category, Order, OrderItem, Payment, Review
from extensions import db
from datetime import datetime, timedelta
import random

fake = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating User instances"""
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone = factory.Faker('phone_number')
    role = 'customer'
    is_active = True
    email_verified = True
    created_at = factory.LazyFunction(datetime.utcnow)
    
    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if create:
            obj.set_password(extracted or 'password123')


class AdminUserFactory(UserFactory):
    """Factory for creating Admin users"""
    role = 'admin'
    username = factory.Sequence(lambda n: f'admin{n}')


class StaffUserFactory(UserFactory):
    """Factory for creating Staff users"""
    role = 'staff'
    username = factory.Sequence(lambda n: f'staff{n}')


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Category instances"""
    class Meta:
        model = Category
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
    
    name = factory.Sequence(lambda n: f'Category {n}')
    description = factory.Faker('sentence')
    is_active = True
    sort_order = factory.Sequence(lambda n: n)
    created_at = factory.LazyFunction(datetime.utcnow)


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Product instances"""
    class Meta:
        model = Product
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
    
    name = factory.Sequence(lambda n: f'Product {n}')
    description = factory.Faker('sentence')
    price = fuzzy.FuzzyDecimal(100, 1000, 2)
    category = factory.SubFactory(CategoryFactory)
    image_url = factory.Faker('image_url')
    tag = factory.Iterator(['Featured', 'New', 'Bestseller', None])
    is_available = True
    stock_quantity = fuzzy.FuzzyInteger(0, 200)
    low_stock_threshold = 5
    preparation_time = fuzzy.FuzzyInteger(5, 30)
    calories = fuzzy.FuzzyInteger(50, 500)
    created_at = factory.LazyFunction(datetime.utcnow)


class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Order instances"""
    class Meta:
        model = Order
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
    
    user = factory.SubFactory(UserFactory)
    total_amount = fuzzy.FuzzyDecimal(100, 5000, 2)
    order_type = factory.Iterator(['pickup', 'delivery'])
    status = 'pending'
    payment_method = factory.Iterator(['mpesa', 'cash'])
    payment_status = 'pending'
    delivery_fee = fuzzy.FuzzyDecimal(0, 200, 2)
    created_at = factory.LazyFunction(datetime.utcnow)
    estimated_ready_time = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(minutes=20))


class OrderItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating OrderItem instances"""
    class Meta:
        model = OrderItem
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
    
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = fuzzy.FuzzyInteger(1, 5)
    unit_price = factory.LazyAttribute(lambda obj: obj.product.price)
    subtotal = factory.LazyAttribute(lambda obj: obj.unit_price * obj.quantity)


class PaymentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Payment instances"""
    class Meta:
        model = Payment
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
    
    order = factory.SubFactory(OrderFactory)
    amount = factory.LazyAttribute(lambda obj: obj.order.total_amount)
    payment_method = factory.Iterator(['mpesa', 'cash', 'card'])
    transaction_id = factory.Sequence(lambda n: f'TXN{n:08d}')
    status = 'pending'
    currency = 'KES'
    created_at = factory.LazyFunction(datetime.utcnow)


class ReviewFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Review instances"""
    class Meta:
        model = Review
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
    
    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    rating = fuzzy.FuzzyInteger(1, 5)
    comment = factory.Faker('paragraph')
    is_verified_purchase = True
    is_approved = True
    helpful_count = fuzzy.FuzzyInteger(0, 50)
    created_at = factory.LazyFunction(datetime.utcnow)


# Helper functions for batch creation
def create_users(count=10, **kwargs):
    """Create multiple users"""
    return [UserFactory(**kwargs) for _ in range(count)]


def create_products(count=10, **kwargs):
    """Create multiple products"""
    return [ProductFactory(**kwargs) for _ in range(count)]


def create_orders(count=10, **kwargs):
    """Create multiple orders"""
    return [OrderFactory(**kwargs) for _ in range(count)]


def create_reviews(count=10, **kwargs):
    """Create multiple reviews"""
    return [ReviewFactory(**kwargs) for _ in range(count)]
