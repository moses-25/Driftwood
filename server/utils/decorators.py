"""
Authorization decorators for route protection
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def jwt_required(fn):
    """
    Decorator to require a valid JWT token for a route
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper

ROLE_HIERARCHY = {
    'customer': 1,
    'staff': 2,
    'admin': 3,
}

def role_required(*allowed_roles):
    """
    Decorator to require specific user roles for a route
    
    Uses role hierarchy: admin > staff > customer
    A user with a higher role can access routes requiring lower roles.
    
    Args:
        *allowed_roles: Variable number of role strings (e.g., 'admin', 'staff', 'customer')
        
    Usage:
        @role_required('admin')
        @role_required('admin', 'staff')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            user = User.query.get(user_id)
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 401
            
            if not user.is_active:
                return jsonify({'success': False, 'error': 'Account is deactivated'}), 403
            
            user_level = ROLE_HIERARCHY.get(user.role, 0)
            min_level = min(ROLE_HIERARCHY.get(role, 0) for role in allowed_roles)
            
            if user_level < min_level:
                return jsonify({
                    'success': False, 
                    'error': 'Insufficient permissions',
                    'required_roles': list(allowed_roles),
                    'user_role': user.role
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn):
    """
    Decorator to require admin role for a route
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 401
        
        if not user.is_active:
            return jsonify({'success': False, 'error': 'Account is deactivated'}), 403
        
        if user.role != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def staff_required(fn):
    """
    Decorator to require staff or admin role for a route
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 401
        
        if not user.is_active:
            return jsonify({'success': False, 'error': 'Account is deactivated'}), 403
        
        if user.role not in ['admin', 'staff']:
            return jsonify({'success': False, 'error': 'Staff access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def get_current_user():
    """
    Get the current authenticated user from the JWT token
    
    Returns:
        User: The authenticated user object or None
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except:
        return None

def verified_email_required(fn):
    """
    Decorator to require email verification for a route
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 401
        
        if not user.email_verified:
            return jsonify({'success': False, 'error': 'Email verification required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper
