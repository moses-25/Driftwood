"""
User routes
Handles all user-related API endpoints
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import UserService
from utils.decorators import admin_required, get_current_user

user_bp = Blueprint('user', __name__)


@user_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    """
    Get current user's profile

    Returns:
        200: User profile data
        401: Unauthorized
        404: User not found
        500: Server error
    """
    try:
        user_id = get_jwt_identity()
        user, error, status_code = UserService.get_user_by_id(user_id)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'data': user
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@user_bp.route('/users/me', methods=['PUT'])
@jwt_required()
def update_my_profile():
    """
    Update current user's profile

    Request Body:
        first_name (str): User's first name
        last_name (str): User's last name
        phone (str): Phone number
        address (str): Physical address
        username (str): New username

    Returns:
        200: Profile updated successfully
        400: Validation error
        401: Unauthorized
        409: Username already taken
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        user_id = get_jwt_identity()
        user, error, status_code = UserService.update_user_profile(user_id, data)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'data': user
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@user_bp.route('/users/me/orders', methods=['GET'])
@jwt_required()
def get_my_orders():
    """
    Get current user's order history

    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 20)
        status (str): Filter by order status

    Returns:
        200: List of orders with pagination
        401: Unauthorized
        500: Server error
    """
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', type=str)

        per_page = min(per_page, 100)

        orders, pagination, error, status_code = UserService.get_user_orders(
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


@user_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """
    List all users (Admin only)

    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 20)
        role (str): Filter by role (customer, staff, admin)
        is_active (bool): Filter by active status
        search (str): Search by username, email, or name

    Returns:
        200: List of users with pagination
        403: Forbidden (not admin)
        500: Server error
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role = request.args.get('role', type=str)
        search = request.args.get('search', type=str)
        is_active = request.args.get('is_active', type=str)

        if is_active is not None:
            is_active = is_active.lower() == 'true'

        per_page = min(per_page, 100)

        users, pagination, error, status_code = UserService.list_users(
            page=page,
            per_page=per_page,
            role=role,
            is_active=is_active,
            search=search
        )

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'data': users,
            'pagination': pagination
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    """
    Get user by ID (Admin only)

    Path Parameters:
        user_id (int): The user's ID

    Returns:
        200: User details
        403: Forbidden (not admin)
        404: User not found
        500: Server error
    """
    try:
        user, error, status_code = UserService.get_user_by_id(user_id)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'data': user
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    """
    Update user profile (Admin only)

    Path Parameters:
        user_id (int): The user's ID

    Request Body:
        first_name (str): User's first name
        last_name (str): User's last name
        phone (str): Phone number
        address (str): Physical address
        is_active (bool): Account active status
        role (str): User role

    Returns:
        200: User updated successfully
        403: Forbidden (not admin)
        404: User not found
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        user, error, status_code = UserService.update_user_profile(user_id, data)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'data': user
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """
    Delete a user (Admin only)

    Path Parameters:
        user_id (int): The user's ID

    Returns:
        200: User deleted successfully
        400: Cannot delete admin users
        403: Forbidden (not admin)
        404: User not found
        500: Server error
    """
    try:
        success, error, status_code = UserService.delete_user(user_id)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
