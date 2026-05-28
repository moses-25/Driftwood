"""
Unit Tests for Product Model
Tests product creation, methods, and relationships
"""
import pytest
from models.product import Product
from models.category import Category
from decimal import Decimal


@pytest.mark.unit
class TestProductModel:
    """Test Product model"""
    
    def test_product_creation(self, db, category):
        """Test creating a product"""
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
        
        assert product.id is not None
        assert product.name == 'Espresso'
        assert product.price == Decimal('250')
        assert product.category_id == category.id
        assert product.is_available is True
        assert product.stock_quantity == 100
    
    def test_product_category_relationship(self, db, category):
        """Test product-category relationship"""
        product = Product(
            name='Latte',
            price=350,
            category_id=category.id
        )
        db.session.add(product)
        db.session.commit()
        
        assert product.category is not None
        assert product.category.name == category.name
    
    def test_product_to_dict(self, db, category):
        """Test to_dict method"""
        product = Product(
            name='Cappuccino',
            description='Creamy coffee',
            price=300,
            category_id=category.id,
            tag='Featured',
            stock_quantity=50
        )
        db.session.add(product)
        db.session.commit()
        
        product_dict = product.to_dict()
        
        assert product_dict['name'] == 'Cappuccino'
        assert product_dict['price'] == 300.0
        assert product_dict['category_name'] == category.name
        assert product_dict['tag'] == 'Featured'
        assert product_dict['stock_quantity'] == 50
    
    def test_is_low_stock(self, db, category):
        """Test is_low_stock method"""
        product = Product(
            name='Test',
            price=100,
            category_id=category.id,
            stock_quantity=3,
            low_stock_threshold=5
        )
        
        assert product.is_low_stock() is True
        
        product.stock_quantity = 10
        assert product.is_low_stock() is False
    
    def test_get_average_rating_no_reviews(self, db, category):
        """Test average rating with no reviews"""
        product = Product(
            name='Test',
            price=100,
            category_id=category.id
        )
        db.session.add(product)
        db.session.commit()
        
        assert product.get_average_rating() == 0
    
    def test_get_review_count(self, db, category):
        """Test review count"""
        product = Product(
            name='Test',
            price=100,
            category_id=category.id
        )
        db.session.add(product)
        db.session.commit()
        
        assert product.get_review_count() == 0
    
    def test_product_availability(self, db, category):
        """Test product availability"""
        product = Product(
            name='Test',
            price=100,
            category_id=category.id,
            is_available=False
        )
        
        assert product.is_available is False
        
        product.is_available = True
        assert product.is_available is True
    
    def test_product_tags(self, db, category):
        """Test product tags"""
        featured = Product(name='P1', price=100, category_id=category.id, tag='Featured')
        new = Product(name='P2', price=100, category_id=category.id, tag='New')
        bestseller = Product(name='P3', price=100, category_id=category.id, tag='Bestseller')
        
        assert featured.tag == 'Featured'
        assert new.tag == 'New'
        assert bestseller.tag == 'Bestseller'
    
    def test_product_repr(self, db, category):
        """Test product string representation"""
        product = Product(name='Espresso', price=250, category_id=category.id)
        
        assert repr(product) == '<Product Espresso>'
    
    def test_product_price_decimal(self, db, category):
        """Test price is stored as Decimal"""
        product = Product(name='Test', price=299.99, category_id=category.id)
        db.session.add(product)
        db.session.commit()
        
        assert isinstance(product.price, Decimal)
        assert product.price == Decimal('299.99')
    
    def test_product_timestamps(self, db, category):
        """Test product timestamps"""
        product = Product(name='Test', price=100, category_id=category.id)
        db.session.add(product)
        db.session.commit()
        
        assert product.created_at is not None
        assert product.updated_at is not None
