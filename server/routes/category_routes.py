"""
Category routes
Handles all category-related API endpoints
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.category_service import CategoryService
from utils.decorators import admin_required

category_bp = Blueprint('category', __name__)


@category_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all categories
    
    Query Parameters:
        include_inactive (bool): Include inactive categories (default: false)
        
    Returns:
        200: List of categories
        500: Server error
    """
    try:
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        
        categories, error, status_code = CategoryService.get_all_categories(
            include_inactive=include_inactive
        )
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': categories
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Get a single category by ID
    
    Path Parameters:
        category_id (int): The category's ID
        
    Returns:
        200: Category details
        404: Category not found
        500: Server error
    """
    try:
        category, error, status_code = CategoryService.get_category_by_id(category_id)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': category
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@category_bp.route('/categories/<int:category_id>/products', methods=['GET'])
def get_category_products(category_id):
    """
    Get all products in a category
    
    Path Parameters:
        category_id (int): The category's ID
        
    Query Parameters:
        include_unavailable (bool): Include unavailable products (default: false)
        
    Returns:
        200: List of products in category
        404: Category not found
        500: Server error
    """
    try:
        include_unavailable = request.args.get('include_unavailable', 'false').lower() == 'true'
        
        products, error, status_code = CategoryService.get_category_products(
            category_id=category_id,
            include_unavailable=include_unavailable
        )
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': products
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@category_bp.route('/categories', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    """
    Create a new category (Admin only)
    
    Request Body:
        name (str): Category name (required)
        description (str): Category description
        is_active (bool): Category active status (default: true)
        sort_order (int): Display order (default: 0)
        
    Returns:
        201: Category created successfully
        400: Validation error
        403: Forbidden (not admin)
        409: Category name already exists
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        category, error, status_code = CategoryService.create_category(data)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Category created successfully',
            'data': category
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_category(category_id):
    """
    Update an existing category (Admin only)
    
    Path Parameters:
        category_id (int): The category's ID
        
    Request Body:
        Any category fields to update (same as create)
        
    Returns:
        200: Category updated successfully
        400: Validation error
        403: Forbidden (not admin)
        404: Category not found
        409: Category name already exists
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        category, error, status_code = CategoryService.update_category(category_id, data)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Category updated successfully',
            'data': category
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_category(category_id):
    """
    Delete a category (Admin only)
    Performs soft delete by setting is_active to False
    Cannot delete categories with products
    
    Path Parameters:
        category_id (int): The category's ID
        
    Returns:
        200: Category deleted successfully
        400: Category has products
        403: Forbidden (not admin)
        404: Category not found
        500: Server error
    """
    try:
        success, error, status_code = CategoryService.delete_category(category_id)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Category deleted successfully'
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@category_bp.route('/categories/reorder', methods=['PUT'])
@jwt_required()
@admin_required
def reorder_categories():
    """
    Reorder categories (Admin only)
    
    Request Body:
        category_ids (list): List of category IDs in desired order
        
    Returns:
        200: Categories reordered successfully
        400: Validation error
        403: Forbidden (not admin)
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data or 'category_ids' not in data:
            return jsonify({'success': False, 'error': 'category_ids is required'}), 400
        
        if not isinstance(data['category_ids'], list):
            return jsonify({'success': False, 'error': 'category_ids must be a list'}), 400
        
        success, error, status_code = CategoryService.reorder_categories(data['category_ids'])
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Categories reordered successfully'
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
