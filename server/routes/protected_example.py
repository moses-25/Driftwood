"""
Example routes showing how to use authentication decorators
This file demonstrates the usage of @jwt_required, @role_required, @admin_required, etc.
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import role_required, admin_required, staff_required, get_current_user

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected/public', methods=['GET'])
def public_route():
    """
    Public route - no authentication required
    """
    return jsonify({
        'success': True,
        'message': 'This is a public route, anyone can access it'
    }), 200

@protected_bp.route('/protected/authenticated', methods=['GET'])
@jwt_required()
def authenticated_route():
    """
    Protected route - requires valid JWT token
    Any authenticated user can access this
    """
    user_id = get_jwt_identity()
    user = get_current_user()
    
    return jsonify({
        'success': True,
        'message': 'This route requires authentication',
        'user_id': user_id,
        'username': user.username if user else None
    }), 200

@protected_bp.route('/protected/customer', methods=['GET'])
@jwt_required()
@role_required('customer')
def customer_route():
    """
    Customer route - requires customer role (or higher)
    """
    user = get_current_user()
    
    return jsonify({
        'success': True,
        'message': 'This route is for customers',
        'user': user.to_dict() if user else None
    }), 200

@protected_bp.route('/protected/staff', methods=['GET'])
@jwt_required()
@staff_required
def staff_route():
    """
    Staff route - requires staff or admin role
    """
    user = get_current_user()
    
    return jsonify({
        'success': True,
        'message': 'This route is for staff and admins',
        'user': user.to_dict() if user else None
    }), 200

@protected_bp.route('/protected/admin', methods=['GET'])
@jwt_required()
@admin_required
def admin_route():
    """
    Admin route - requires admin role only
    """
    user = get_current_user()
    
    return jsonify({
        'success': True,
        'message': 'This route is for admins only',
        'user': user.to_dict() if user else None
    }), 200

@protected_bp.route('/protected/multi-role', methods=['GET'])
@jwt_required()
@role_required('staff', 'admin')
def multi_role_route():
    """
    Multi-role route - requires either staff or admin role
    """
    user = get_current_user()
    
    return jsonify({
        'success': True,
        'message': 'This route allows staff and admin roles',
        'user_role': user.role if user else None
    }), 200
