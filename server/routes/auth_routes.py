from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.auth_service import AuthService
from utils.decorators import get_current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request Body:
        username (str): User's username
        email (str): User's email address
        password (str): User's password
        first_name (str, optional): User's first name
        last_name (str, optional): User's last name
        phone (str, optional): User's phone number
        
    Returns:
        201: User created successfully with tokens
        400: Validation error
        409: Username or email already exists
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        phone = data.get('phone', '').strip()

        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'Username, email, and password are required'}), 400

        # Use auth service to register user
        user_dict, tokens, error, status_code = AuthService.register_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': user_dict,
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token']
            }
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    Login a user
    
    Request Body:
        email (str): User's email address
        password (str): User's password
        
    Returns:
        200: Login successful with tokens
        400: Missing credentials
        401: Invalid credentials
        403: Account deactivated
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400

        # Use auth service to login user
        user_dict, tokens, error, status_code = AuthService.login_user(email, password)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user_dict,
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token']
            }
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token
    
    Headers:
        Authorization: Bearer <refresh_token>
        
    Returns:
        200: New access token generated
        401: Invalid or expired refresh token
        403: Account deactivated
        500: Server error
    """
    try:
        user_id = get_jwt_identity()

        # Use auth service to refresh token
        access_token, error, status_code = AuthService.refresh_access_token(user_id)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'message': 'Token refreshed successfully',
            'data': {
                'access_token': access_token
            }
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """
    Get current authenticated user's information
    
    Headers:
        Authorization: Bearer <access_token>
        
    Returns:
        200: User information
        401: Invalid or expired token
        500: Server error
    """
    try:
        user = get_current_user()

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change user's password (requires current password)
    
    Headers:
        Authorization: Bearer <access_token>
        
    Request Body:
        old_password (str): Current password
        new_password (str): New password
        
    Returns:
        200: Password changed successfully
        400: Validation error
        401: Invalid current password
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')

        if not old_password or not new_password:
            return jsonify({'success': False, 'error': 'Old password and new password are required'}), 400

        user_id = get_jwt_identity()

        # Use auth service to change password
        success, error, status_code = AuthService.change_password(user_id, old_password, new_password)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/auth/request-password-reset', methods=['POST'])
def request_password_reset():
    """
    Request a password reset token
    
    Request Body:
        email (str): User's email address
        
    Returns:
        200: Reset token generated (or generic success message)
        500: Server error
        
    Note: Always returns success to prevent email enumeration
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        email = data.get('email', '').strip()

        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400

        # Use auth service to request password reset
        reset_token, error, status_code = AuthService.request_password_reset(email)

        # Always return success message to prevent email enumeration
        return jsonify({
            'success': True,
            'message': 'If an account exists with this email, a password reset link has been sent',
            'reset_token': reset_token  # TODO: Remove this in production, send via email instead
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/auth/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    """
    Reset password using reset token
    
    Headers:
        Authorization: Bearer <reset_token>
        
    Request Body:
        new_password (str): New password
        
    Returns:
        200: Password reset successfully
        400: Validation error
        401: Invalid or expired token
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        new_password = data.get('new_password', '')

        if not new_password:
            return jsonify({'success': False, 'error': 'New password is required'}), 400

        user_id = get_jwt_identity()
        
        # Verify this is a password reset token
        claims = get_jwt()
        if claims.get('type') != 'password_reset':
            return jsonify({'success': False, 'error': 'Invalid token type'}), 401

        # Use auth service to reset password
        success, error, status_code = AuthService.reset_password(user_id, new_password)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'message': 'Password reset successfully'
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/auth/verify-email', methods=['POST'])
@jwt_required()
def verify_email():
    """
    Verify user's email address
    
    Headers:
        Authorization: Bearer <verification_token>
        
    Returns:
        200: Email verified successfully
        400: Email already verified
        401: Invalid or expired token
        404: User not found
        500: Server error
    """
    try:
        user_id = get_jwt_identity()

        # Use auth service to verify email
        success, error, status_code = AuthService.verify_email(user_id)

        if error:
            return jsonify({'success': False, 'error': error}), status_code

        return jsonify({
            'success': True,
            'message': 'Email verified successfully'
        }), status_code

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
