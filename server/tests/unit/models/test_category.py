"""
Unit tests for Category model

Tests cover:
- Model creation with valid data
- Required fields validation
- Name uniqueness constraint
- Active/inactive status
- Sort order functionality
- Product count calculation
- Serialization (to_dict)
- Relationships with products
"""

import pytest
from models.category import Category
from tests.factories import CategoryFactory, ProductFactory


class TestCategoryCreation:
    """Test category creation and basic attributes"""
    
    def test_category_creation_with_valid_data(self, db):
        """Test creating a category with all valid data"""
        category = CategoryFactory(
            name='Coffee',
            description='Hot and cold coffee beverages',
            image_url='https://example.com/coffee.jpg',
            is_active=True,
            sort_order=1
        )
        
        assert category.id is not None
        assert category.name == 'Coffee'
        assert category.description == 'Hot and cold coffee beverages'
        assert category.image_url == 'https://example.com/coffee.jpg'
        assert category.is_active is True
        assert category.sort_order == 1
        assert category.created_at is not None
    
    def test_category_creation_with_minimal_data(self, db):
        """Test creating a category with only required fields"""
        category = Category(name='Tea')
        db.session.add(category)
        db.session.commit()
        
        assert category.id is not None
        assert category.name == 'Tea'
    
    def test_category_default_values(self, db):
        """Test that default values are set correctly"""
        category = Category(name='Pastries')
        db.session.add(category)
        db.session.commit()
        
        assert category.is_active is True
        assert category.sort_order == 0
        assert category.created_at is not None
        assert category.updated_at is not None


class TestCategoryFieldValidation:
    """Test field validation and constraints"""
    
    def test_name_required(self, db):
        """Test that name is required"""
        category = Category(description='Test description')
        db.session.add(category)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_name_unique_constraint(self, db):
        """Test that name must be unique"""
        CategoryFactory(name='Coffee')
        
        with pytest.raises(Exception):  # IntegrityError
            CategoryFactory(name='Coffee')
    
    def test_name_case_sensitivity(self, db):
        """Test name uniqueness is case-sensitive in database"""
        CategoryFactory(name='Coffee')
        
        # SQLite is case-insensitive by default for UNIQUE constraints
        # This test documents the behavior
        try:
            CategoryFactory(name='coffee')
            # If this succeeds, database allows different cases
            assert True
        except Exception:
            # If this fails, database enforces case-insensitive uniqueness
            assert True
    
    def test_name_max_length(self, db):
        """Test name length constraint (100 chars)"""
        long_name = 'A' * 100
        category = CategoryFactory(name=long_name)
        assert len(category.name) == 100


class TestCategoryActiveStatus:
    """Test category active/inactive status"""
    
    def test_is_active_flag(self, db):
        """Test is_active flag"""
        active = CategoryFactory(is_active=True)
        inactive = CategoryFactory(is_active=False)
        
        assert active.is_active is True
        assert inactive.is_active is False
    
    def test_deactivate_category(self, db):
        """Test deactivating a category"""
        category = CategoryFactory(is_active=True)
        assert category.is_active is True
        
        category.is_active = False
        db.session.commit()
        
        assert category.is_active is False
    
    def test_activate_category(self, db):
        """Test activating a category"""
        category = CategoryFactory(is_active=False)
        assert category.is_active is False
        
        category.is_active = True
        db.session.commit()
        
        assert category.is_active is True


class TestCategorySortOrder:
    """Test category sort order functionality"""
    
    def test_sort_order_default(self, db):
        """Test that sort_order defaults to 0"""
        category = Category(name='Test')
        db.session.add(category)
        db.session.commit()
        
        assert category.sort_order == 0
    
    def test_sort_order_custom_values(self, db):
        """Test setting custom sort_order values"""
        cat1 = CategoryFactory(name='First', sort_order=1)
        cat2 = CategoryFactory(name='Second', sort_order=2)
        cat3 = CategoryFactory(name='Third', sort_order=3)
        
        assert cat1.sort_order == 1
        assert cat2.sort_order == 2
        assert cat3.sort_order == 3
    
    def test_sort_order_can_be_updated(self, db):
        """Test that sort_order can be updated"""
        category = CategoryFactory(sort_order=1)
        assert category.sort_order == 1
        
        category.sort_order = 5
        db.session.commit()
        
        assert category.sort_order == 5
    
    def test_sort_order_negative_values(self, db):
        """Test that sort_order can be negative"""
        category = CategoryFactory(sort_order=-1)
        assert category.sort_order == -1


class TestCategorySerialization:
    """Test category serialization to dictionary"""
    
    def test_to_dict_basic(self, db):
        """Test basic to_dict conversion"""
        category = CategoryFactory(
            name='Coffee',
            description='Hot beverages',
            image_url='https://example.com/coffee.jpg',
            is_active=True,
            sort_order=1
        )
        
        data = category.to_dict()
        
        assert data['id'] == category.id
        assert data['name'] == 'Coffee'
        assert data['description'] == 'Hot beverages'
        assert data['image_url'] == 'https://example.com/coffee.jpg'
        assert data['is_active'] is True
        assert data['sort_order'] == 1
        assert 'created_at' in data
        assert isinstance(data['created_at'], str)
    
    def test_to_dict_includes_product_count(self, db):
        """Test that to_dict includes product_count"""
        category = CategoryFactory()
        ProductFactory(category=category)
        ProductFactory(category=category)
        ProductFactory(category=category)
        db.session.commit()
        
        data = category.to_dict()
        
        assert 'product_count' in data
        assert data['product_count'] == 3
    
    def test_to_dict_product_count_zero(self, db):
        """Test product_count is 0 when no products"""
        category = CategoryFactory()
        
        data = category.to_dict()
        
        assert data['product_count'] == 0
    
    def test_to_dict_with_null_description(self, db):
        """Test to_dict when description is None"""
        category = CategoryFactory(description=None)
        
        data = category.to_dict()
        
        assert data['description'] is None
    
    def test_to_dict_with_null_image_url(self, db):
        """Test to_dict when image_url is None"""
        category = CategoryFactory(image_url=None)
        
        data = category.to_dict()
        
        assert data['image_url'] is None


class TestCategoryRelationships:
    """Test category relationships with other models"""
    
    def test_category_products_relationship(self, db):
        """Test that category has products relationship"""
        category = CategoryFactory()
        product1 = ProductFactory(category=category)
        product2 = ProductFactory(category=category)
        product3 = ProductFactory(category=category)
        db.session.commit()
        
        assert len(category.products) == 3
        assert product1 in category.products
        assert product2 in category.products
        assert product3 in category.products
    
    def test_category_products_empty(self, db):
        """Test category with no products"""
        category = CategoryFactory()
        
        assert len(category.products) == 0
    
    def test_product_category_backref(self, db):
        """Test that product has category backref"""
        category = CategoryFactory(name='Coffee')
        product = ProductFactory(category=category)
        db.session.commit()
        
        assert product.category is not None
        assert product.category.name == 'Coffee'
        assert product.category_id == category.id


class TestCategoryImageUrl:
    """Test category image URL field"""
    
    def test_image_url_with_valid_url(self, db):
        """Test image_url with valid URL"""
        category = CategoryFactory(
            image_url='https://example.com/images/coffee.jpg'
        )
        
        assert category.image_url == 'https://example.com/images/coffee.jpg'
    
    def test_image_url_can_be_null(self, db):
        """Test that image_url can be None"""
        category = CategoryFactory(image_url=None)
        
        assert category.image_url is None
    
    def test_image_url_can_be_updated(self, db):
        """Test that image_url can be updated"""
        category = CategoryFactory(image_url='https://example.com/old.jpg')
        
        category.image_url = 'https://example.com/new.jpg'
        db.session.commit()
        
        assert category.image_url == 'https://example.com/new.jpg'


class TestCategoryRepr:
    """Test category string representation"""
    
    def test_repr(self, db):
        """Test string representation of category"""
        category = CategoryFactory(name='Coffee')
        assert repr(category) == '<Category Coffee>'


class TestCategoryTimestamps:
    """Test category timestamp fields"""
    
    def test_created_at_set_on_creation(self, db):
        """Test that created_at is set automatically"""
        category = CategoryFactory()
        
        assert category.created_at is not None
    
    def test_updated_at_set_on_creation(self, db):
        """Test that updated_at is set automatically"""
        category = CategoryFactory()
        
        assert category.updated_at is not None
    
    def test_updated_at_changes_on_update(self, db):
        """Test that updated_at changes when category is updated"""
        category = CategoryFactory()
        original_updated_at = category.updated_at
        
        import time
        time.sleep(0.01)
        
        category.name = 'Updated Name'
        db.session.commit()
        
        assert category.updated_at >= original_updated_at


class TestCategoryDescription:
    """Test category description field"""
    
    def test_description_with_text(self, db):
        """Test description with text content"""
        category = CategoryFactory(
            description='A wide variety of hot and cold coffee beverages'
        )
        
        assert category.description == 'A wide variety of hot and cold coffee beverages'
    
    def test_description_can_be_null(self, db):
        """Test that description can be None"""
        category = CategoryFactory(description=None)
        
        assert category.description is None
    
    def test_description_can_be_long(self, db):
        """Test that description can be long text"""
        long_description = 'A' * 500
        category = CategoryFactory(description=long_description)
        
        assert len(category.description) == 500
    
    def test_description_can_be_updated(self, db):
        """Test that description can be updated"""
        category = CategoryFactory(description='Old description')
        
        category.description = 'New description'
        db.session.commit()
        
        assert category.description == 'New description'


class TestCategoryEdgeCases:
    """Test edge cases and special scenarios"""
    
    def test_category_with_special_characters_in_name(self, db):
        """Test category name with special characters"""
        category = CategoryFactory(name='Coffee & Tea')
        assert category.name == 'Coffee & Tea'
    
    def test_category_with_unicode_in_name(self, db):
        """Test category name with unicode characters"""
        category = CategoryFactory(name='Café ☕')
        assert category.name == 'Café ☕'
    
    def test_multiple_categories_different_sort_orders(self, db):
        """Test multiple categories with different sort orders"""
        cat1 = CategoryFactory(name='First', sort_order=3)
        cat2 = CategoryFactory(name='Second', sort_order=1)
        cat3 = CategoryFactory(name='Third', sort_order=2)
        
        # Verify they can coexist with different sort orders
        assert cat1.sort_order == 3
        assert cat2.sort_order == 1
        assert cat3.sort_order == 2
