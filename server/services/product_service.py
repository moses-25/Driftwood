"""
Product service layer
Handles business logic for product management
"""
from models.product import Product
from models.category import Category
from extensions import db
from sqlalchemy import or_


class ProductService:
    """Service class for product operations"""
    
    @staticmethod
    def get_all_products(page=1, per_page=20, category_id=None, is_available=True, search=None):
        """
        Get all products with optional filtering and pagination
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            category_id: Filter by category ID (optional)
            is_available: Filter by availability (default: True)
            search: Search query for product name/description (optional)
            
        Returns:
            tuple: (products_list, pagination_info, error_message, status_code)
        """
        try:
            query = Product.query
            
            # Filter by availability
            if is_available is not None:
                query = query.filter_by(is_available=is_available)
            
            # Filter by category
            if category_id:
                query = query.filter_by(category_id=category_id)
            
            # Search in name and description
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    or_(
                        Product.name.ilike(search_term),
                        Product.description.ilike(search_term)
                    )
                )
            
            # Order by created_at descending (newest first)
            query = query.order_by(Product.created_at.desc())
            
            # Paginate results
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            
            products_list = [product.to_dict() for product in paginated.items]
            
            pagination_info = {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev
            }
            
            return products_list, pagination_info, None, 200
            
        except Exception as e:
            return None, None, str(e), 500

    
    @staticmethod
    def get_product_by_id(product_id):
        """
        Get a single product by ID
        
        Args:
            product_id: The product's ID
            
        Returns:
            tuple: (product_dict, error_message, status_code)
        """
        try:
            product = Product.query.get(product_id)
            
            if not product:
                return None, "Product not found", 404
            
            return product.to_dict(include_reviews=True), None, 200
            
        except Exception as e:
            return None, str(e), 500
    
    @staticmethod
    def get_products_by_category(category_id, page=1, per_page=20):
        """
        Get all products in a specific category
        
        Args:
            category_id: The category's ID
            page: Page number for pagination
            per_page: Number of items per page
            
        Returns:
            tuple: (products_list, pagination_info, error_message, status_code)
        """
        try:
            # Verify category exists
            category = Category.query.get(category_id)
            if not category:
                return None, None, "Category not found", 404
            
            # Get products in category
            query = Product.query.filter_by(
                category_id=category_id,
                is_available=True
            ).order_by(Product.created_at.desc())
            
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            
            products_list = [product.to_dict() for product in paginated.items]
            
            pagination_info = {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev,
                'category': category.to_dict()
            }
            
            return products_list, pagination_info, None, 200
            
        except Exception as e:
            return None, None, str(e), 500

    
    @staticmethod
    def get_featured_products(limit=10):
        """
        Get featured products (products with 'Featured' tag)
        
        Args:
            limit: Maximum number of products to return
            
        Returns:
            tuple: (products_list, error_message, status_code)
        """
        try:
            products = Product.query.filter_by(
                is_available=True,
                tag='Featured'
            ).limit(limit).all()
            
            products_list = [product.to_dict() for product in products]
            
            return products_list, None, 200
            
        except Exception as e:
            return None, str(e), 500
    
    @staticmethod
    def create_product(data):
        """
        Create a new product (Admin only)
        
        Args:
            data: Dictionary containing product data
            
        Returns:
            tuple: (product_dict, error_message, status_code)
        """
        try:
            # Validate required fields
            required_fields = ['name', 'price', 'category_id']
            for field in required_fields:
                if field not in data or not data[field]:
                    return None, f"{field} is required", 400
            
            # Verify category exists
            category = Category.query.get(data['category_id'])
            if not category:
                return None, "Category not found", 404
            
            # Validate price
            try:
                price = float(data['price'])
                if price < 0:
                    return None, "Price must be positive", 400
            except (ValueError, TypeError):
                return None, "Invalid price format", 400
            
            # Create product
            product = Product(
                name=data['name'],
                description=data.get('description'),
                price=price,
                category_id=data['category_id'],
                image_url=data.get('image_url'),
                tag=data.get('tag'),
                stock_quantity=data.get('stock_quantity', 0),
                low_stock_threshold=data.get('low_stock_threshold', 5),
                preparation_time=data.get('preparation_time'),
                calories=data.get('calories'),
                allergens=data.get('allergens')
            )
            
            db.session.add(product)
            db.session.commit()
            
            return product.to_dict(), None, 201
            
        except Exception as e:
            db.session.rollback()
            return None, str(e), 500

    
    @staticmethod
    def update_product(product_id, data):
        """
        Update an existing product (Admin only)
        
        Args:
            product_id: The product's ID
            data: Dictionary containing updated product data
            
        Returns:
            tuple: (product_dict, error_message, status_code)
        """
        try:
            product = Product.query.get(product_id)
            
            if not product:
                return None, "Product not found", 404
            
            # Update fields if provided
            if 'name' in data:
                product.name = data['name']
            
            if 'description' in data:
                product.description = data['description']
            
            if 'price' in data:
                try:
                    price = float(data['price'])
                    if price < 0:
                        return None, "Price must be positive", 400
                    product.price = price
                except (ValueError, TypeError):
                    return None, "Invalid price format", 400
            
            if 'category_id' in data:
                category = Category.query.get(data['category_id'])
                if not category:
                    return None, "Category not found", 404
                product.category_id = data['category_id']
            
            if 'image_url' in data:
                product.image_url = data['image_url']
            
            if 'tag' in data:
                product.tag = data['tag']
            
            if 'is_available' in data:
                product.is_available = bool(data['is_available'])
            
            if 'stock_quantity' in data:
                product.stock_quantity = int(data['stock_quantity'])
            
            if 'low_stock_threshold' in data:
                product.low_stock_threshold = int(data['low_stock_threshold'])
            
            if 'preparation_time' in data:
                product.preparation_time = data['preparation_time']
            
            if 'calories' in data:
                product.calories = data['calories']
            
            if 'allergens' in data:
                product.allergens = data['allergens']
            
            db.session.commit()
            
            return product.to_dict(), None, 200
            
        except Exception as e:
            db.session.rollback()
            return None, str(e), 500
    
    @staticmethod
    def delete_product(product_id):
        """
        Soft delete a product (Admin only)
        Sets is_available to False instead of deleting from database
        
        Args:
            product_id: The product's ID
            
        Returns:
            tuple: (success, error_message, status_code)
        """
        try:
            product = Product.query.get(product_id)
            
            if not product:
                return False, "Product not found", 404
            
            # Soft delete - set is_available to False
            product.is_available = False
            db.session.commit()
            
            return True, None, 200
            
        except Exception as e:
            db.session.rollback()
            return False, str(e), 500
    
    @staticmethod
    def update_stock(product_id, quantity):
        """
        Update product stock quantity
        
        Args:
            product_id: The product's ID
            quantity: New stock quantity
            
        Returns:
            tuple: (product_dict, error_message, status_code)
        """
        try:
            product = Product.query.get(product_id)
            
            if not product:
                return None, "Product not found", 404
            
            try:
                quantity = int(quantity)
                if quantity < 0:
                    return None, "Stock quantity cannot be negative", 400
            except (ValueError, TypeError):
                return None, "Invalid quantity format", 400
            
            product.stock_quantity = quantity
            db.session.commit()
            
            return product.to_dict(), None, 200
            
        except Exception as e:
            db.session.rollback()
            return None, str(e), 500
