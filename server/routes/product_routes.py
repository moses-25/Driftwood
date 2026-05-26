"""
Product routes
Handles all product-related API endpoints
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.product_service import ProductService
from utils.decorators import admin_required

product_bp = Blueprint('product', __name__)


@product_bp.route('/products', methods=['GET'])
def get_products():
    """
    Get all products with optional filtering
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 20)
        category_id (int): Filter by category ID
        search (str): Search in product name/description
        is_available (bool): Filter by availability (default: true)
        
    Returns:
        200: List of products with pagination info
        500: Server error
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', type=str)
        is_available = request.args.get('is_available', 'true').lower() == 'true'
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        products, pagination, error, status_code = ProductService.get_all_products(
            page=page,
            per_page=per_page,
            category_id=category_id,
            is_available=is_available,
            search=search
        )
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': products,
            'pagination': pagination
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get a single product by ID
    
    Path Parameters:
        product_id (int): The product's ID
        
    Returns:
        200: Product details with reviews
        404: Product not found
        500: Server error
    """
    try:
        product, error, status_code = ProductService.get_product_by_id(product_id)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': product
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@product_bp.route('/products/category/<int:category_id>', methods=['GET'])
def get_products_by_category(category_id):
    """
    Get all products in a specific category
    
    Path Parameters:
        category_id (int): The category's ID
        
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 20)
        
    Returns:
        200: List of products in category with pagination
        404: Category not found
        500: Server error
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        products, pagination, error, status_code = ProductService.get_products_by_category(
            category_id=category_id,
            page=page,
            per_page=per_page
        )
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': products,
            'pagination': pagination
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('/products/featured', methods=['GET'])
def get_featured_products():
    """
    Get featured products
    
    Query Parameters:
        limit (int): Maximum number of products (default: 10)
        
    Returns:
        200: List of featured products
        500: Server error
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 50)  # Max 50 featured products
        
        products, error, status_code = ProductService.get_featured_products(limit=limit)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': products
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('/products', methods=['POST'])
@jwt_required()
@admin_required
def create_product():
    """
    Create a new product (Admin only)
    
    Request Body:
        name (str): Product name (required)
        description (str): Product description
        price (float): Product price (required)
        category_id (int): Category ID (required)
        image_url (str): Product image URL
        tag (str): Product tag (Featured, New, Bestseller, etc.)
        stock_quantity (int): Initial stock quantity
        low_stock_threshold (int): Low stock alert threshold
        preparation_time (int): Preparation time in minutes
        calories (int): Calorie count
        allergens (str): Allergen information
        
    Returns:
        201: Product created successfully
        400: Validation error
        403: Forbidden (not admin)
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        product, error, status_code = ProductService.create_product(data)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'data': product
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_product(product_id):
    """
    Update an existing product (Admin only)
    
    Path Parameters:
        product_id (int): The product's ID
        
    Request Body:
        Any product fields to update (same as create)
        
    Returns:
        200: Product updated successfully
        400: Validation error
        403: Forbidden (not admin)
        404: Product not found
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        product, error, status_code = ProductService.update_product(product_id, data)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Product updated successfully',
            'data': product
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_product(product_id):
    """
    Delete a product (Admin only)
    Performs soft delete by setting is_available to False
    
    Path Parameters:
        product_id (int): The product's ID
        
    Returns:
        200: Product deleted successfully
        403: Forbidden (not admin)
        404: Product not found
        500: Server error
    """
    try:
        success, error, status_code = ProductService.delete_product(product_id)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Product deleted successfully'
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('/products/<int:product_id>/stock', methods=['PUT'])
@jwt_required()
@admin_required
def update_product_stock(product_id):
    """
    Update product stock quantity (Admin only)
    
    Path Parameters:
        product_id (int): The product's ID
        
    Request Body:
        quantity (int): New stock quantity (required)
        
    Returns:
        200: Stock updated successfully
        400: Validation error
        403: Forbidden (not admin)
        404: Product not found
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data or 'quantity' not in data:
            return jsonify({'success': False, 'error': 'Quantity is required'}), 400
        
        product, error, status_code = ProductService.update_stock(
            product_id,
            data['quantity']
        )
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Stock updated successfully',
            'data': product
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
