"""
Order routes
Handles all order-related API endpoints
Supports both authenticated users and guest checkout
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.order_service import OrderService
from utils.decorators import staff_required, get_current_user

order_bp = Blueprint('order', __name__)


@order_bp.route('/orders', methods=['POST'])
def create_order():
    """
    Create a new order
    Supports both authenticated users and guest checkout
    
    Request Body:
        items (list): List of order items with product_id, quantity, customizations
        order_type (str): 'pickup' or 'delivery' (required)
        payment_method (str): 'mpesa' or 'cash' (required)
        delivery_address (str): Delivery address (required for delivery orders)
        delivery_instructions (str): Special delivery instructions
        delivery_fee (float): Delivery fee (for delivery orders)
        total_amount (float): Expected total amount (for verification)
        
    Returns:
        201: Order created successfully
        400: Validation error
        404: Product not found
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Get user ID if authenticated (optional for guest checkout)
        user_id = None
        try:
            user_id = get_jwt_identity()
        except:
            pass  # Guest checkout
        
        # Extract items and order data
        items = data.get('items', [])
        order_data = {
            'order_type': data.get('order_type'),
            'payment_method': data.get('payment_method'),
            'delivery_address': data.get('delivery_address'),
            'delivery_instructions': data.get('delivery_instructions'),
            'delivery_fee': data.get('delivery_fee', 0),
            'total_amount': data.get('total_amount')
        }
        
        # Create order using service
        order, error, status_code = OrderService.create_order(user_id, items, order_data)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'data': order
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get order by ID
    Users can only view their own orders, staff/admin can view any order
    
    Path Parameters:
        order_id (int): The order's ID
        
    Returns:
        200: Order details
        403: Access denied
        404: Order not found
        500: Server error
    """
    try:
        # Get user ID if authenticated
        user_id = None
        user = get_current_user()
        if user:
            user_id = user.id
            # Staff and admin can view any order
            if user.role in ['staff', 'admin']:
                user_id = None  # Skip ownership check
        
        order, error, status_code = OrderService.get_order_by_id(order_id, user_id)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': order
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@order_bp.route('/orders/<order_number>', methods=['GET'])
def get_order_by_number(order_number):
    """
    Get order by order number (for guest checkout tracking)
    
    Path Parameters:
        order_number (str): The order's unique number
        
    Returns:
        200: Order details
        404: Order not found
        500: Server error
    """
    try:
        order, error, status_code = OrderService.get_order_by_number(order_number)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': order
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@order_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@jwt_required()
@staff_required
def update_order_status(order_id):
    """
    Update order status (Staff/Admin only)
    
    Path Parameters:
        order_id (int): The order's ID
        
    Request Body:
        status (str): New status (required)
            Valid values: pending, confirmed, preparing, ready, completed, cancelled
        
    Returns:
        200: Order status updated successfully
        400: Invalid status
        403: Forbidden (not staff/admin)
        404: Order not found
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'success': False, 'error': 'Status is required'}), 400
        
        order, error, status_code = OrderService.update_order_status(order_id, data['status'])
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Order status updated successfully',
            'data': order
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@order_bp.route('/orders', methods=['GET'])
@jwt_required()
@staff_required
def get_orders():
    """
    Get all orders with optional filtering (Staff/Admin only)
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 20)
        status (str): Filter by status
        order_type (str): Filter by order type (pickup/delivery)
        
    Returns:
        200: List of orders with pagination
        403: Forbidden (not staff/admin)
        500: Server error
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', type=str)
        order_type = request.args.get('order_type', type=str)
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        orders, pagination, error, status_code = OrderService.get_all_orders(
            page=page,
            per_page=per_page,
            status=status,
            order_type=order_type
        )
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': orders,
            'pagination': pagination
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@order_bp.route('/orders/my-orders', methods=['GET'])
@jwt_required()
def get_my_orders():
    """
    Get current user's orders
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 20)
        status (str): Filter by status
        
    Returns:
        200: List of user's orders with pagination
        401: Unauthorized
        500: Server error
    """
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', type=str)
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        orders, pagination, error, status_code = OrderService.get_user_orders(
            user_id=user_id,
            page=page,
            per_page=per_page,
            status=status
        )
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'data': orders,
            'pagination': pagination
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def cancel_order(order_id):
    """
    Cancel an order
    Users can cancel their own orders, admins can cancel any order
    
    Path Parameters:
        order_id (int): The order's ID
        
    Returns:
        200: Order cancelled successfully
        400: Cannot cancel order
        403: Access denied
        404: Order not found
        500: Server error
    """
    try:
        user = get_current_user()
        user_id = user.id if user.role == 'customer' else None  # Admin can cancel any order
        
        order, error, status_code = OrderService.cancel_order(order_id, user_id)
        
        if error:
            return jsonify({'success': False, 'error': error}), status_code
        
        return jsonify({
            'success': True,
            'message': 'Order cancelled successfully',
            'data': order
        }), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500