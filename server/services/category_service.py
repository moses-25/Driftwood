"""
Category service layer
Handles business logic for category management
"""
from models.category import Category
from models.product import Product
from extensions import db


class CategoryService:
    """Service class for category operations"""
    
    @staticmethod
    def get_all_categories(include_inactive=False):
        """
        Get all categories
        
        Args:
            include_inactive: Include inactive categories (default: False)
            
        Returns:
            tuple: (categories_list, error_message, status_code)
        """
        try:
            query = Category.query
            
            if not include_inactive:
                query = query.filter_by(is_active=True)
            
            # Order by sort_order, then by name
            categories = query.order_by(Category.sort_order, Category.name).all()
            
            categories_list = [category.to_dict() for category in categories]
            
            return categories_list, None, 200
            
        except Exception as e:
            return None, str(e), 500
    
    @staticmethod
    def get_category_by_id(category_id):
        """
        Get a single category by ID
        
        Args:
            category_id: The category's ID
            
        Returns:
            tuple: (category_dict, error_message, status_code)
        """
        try:
            category = Category.query.get(category_id)
            
            if not category:
                return None, "Category not found", 404
            
            return category.to_dict(), None, 200
            
        except Exception as e:
            return None, str(e), 500
    
    @staticmethod
    def get_category_products(category_id, include_unavailable=False):
        """
        Get all products in a category
        
        Args:
            category_id: The category's ID
            include_unavailable: Include unavailable products (default: False)
            
        Returns:
            tuple: (products_list, error_message, status_code)
        """
        try:
            category = Category.query.get(category_id)
            
            if not category:
                return None, "Category not found", 404
            
            query = Product.query.filter_by(category_id=category_id)
            
            if not include_unavailable:
                query = query.filter_by(is_available=True)
            
            products = query.order_by(Product.created_at.desc()).all()
            products_list = [product.to_dict() for product in products]
            
            return products_list, None, 200
            
        except Exception as e:
            return None, str(e), 500

    
    @staticmethod
    def create_category(data):
        """
        Create a new category (Admin only)
        
        Args:
            data: Dictionary containing category data
            
        Returns:
            tuple: (category_dict, error_message, status_code)
        """
        try:
            # Validate required fields
            if 'name' not in data or not data['name']:
                return None, "Category name is required", 400
            
            # Check if category name already exists
            existing = Category.query.filter_by(name=data['name']).first()
            if existing:
                return None, "Category with this name already exists", 409
            
            # Create category
            category = Category(
                name=data['name'],
                description=data.get('description'),
                is_active=data.get('is_active', True),
                sort_order=data.get('sort_order', 0)
            )
            
            db.session.add(category)
            db.session.commit()
            
            return category.to_dict(), None, 201
            
        except Exception as e:
            db.session.rollback()
            return None, str(e), 500
    
    @staticmethod
    def update_category(category_id, data):
        """
        Update an existing category (Admin only)
        
        Args:
            category_id: The category's ID
            data: Dictionary containing updated category data
            
        Returns:
            tuple: (category_dict, error_message, status_code)
        """
        try:
            category = Category.query.get(category_id)
            
            if not category:
                return None, "Category not found", 404
            
            # Check if new name conflicts with existing category
            if 'name' in data and data['name'] != category.name:
                existing = Category.query.filter_by(name=data['name']).first()
                if existing:
                    return None, "Category with this name already exists", 409
                category.name = data['name']
            
            # Update fields if provided
            if 'description' in data:
                category.description = data['description']
            
            if 'is_active' in data:
                category.is_active = bool(data['is_active'])
            
            if 'sort_order' in data:
                category.sort_order = int(data['sort_order'])
            
            db.session.commit()
            
            return category.to_dict(), None, 200
            
        except Exception as e:
            db.session.rollback()
            return None, str(e), 500
    
    @staticmethod
    def delete_category(category_id):
        """
        Soft delete a category (Admin only)
        Sets is_active to False instead of deleting from database
        
        Args:
            category_id: The category's ID
            
        Returns:
            tuple: (success, error_message, status_code)
        """
        try:
            category = Category.query.get(category_id)
            
            if not category:
                return False, "Category not found", 404
            
            # Check if category has products
            product_count = Product.query.filter_by(category_id=category_id).count()
            if product_count > 0:
                return False, f"Cannot delete category with {product_count} products. Deactivate it instead.", 400
            
            # Soft delete - set is_active to False
            category.is_active = False
            db.session.commit()
            
            return True, None, 200
            
        except Exception as e:
            db.session.rollback()
            return False, str(e), 500
    
    @staticmethod
    def reorder_categories(category_ids):
        """
        Reorder categories by updating sort_order
        
        Args:
            category_ids: List of category IDs in desired order
            
        Returns:
            tuple: (success, error_message, status_code)
        """
        try:
            for index, category_id in enumerate(category_ids):
                category = Category.query.get(category_id)
                if category:
                    category.sort_order = index
            
            db.session.commit()
            
            return True, None, 200
            
        except Exception as e:
            db.session.rollback()
            return False, str(e), 500
