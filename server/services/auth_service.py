"""
Authentication service layer
Handles business logic for user authentication and authorization
"""
from models.user import User
from extensions import db
from utils.jwt_utils import generate_tokens
from utils.validators import validate_email, validate_password, validate_username
from datetime import datetime
from flask_jwt_extended import create_access_token
from datetime import timedelta

class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    def register_user(username, email, password, first_name=None, last_name=None, phone=None, role='customer'):
        """
        Register a new user
        
        Args:
            username: User's username
            email: User's email address
            password: User's password (will be hashed)
            first_name: User's first name (optional)
            last_name: User's last name (optional)
            phone: User's phone number (optional)
            role: User's role (default: 'customer')
            
        Returns:
            tuple: (user_dict, tokens_dict, error_message, status_code)
        """
        # Validate username
        is_valid, error = validate_username(username)
        if not is_valid:
            return None, None, error, 400
        
        # Validate email
        is_valid, error = validate_email(email)
        if not is_valid:
            return None, None, error, 400
        
        # Validate password
        is_valid, error = validate_password(password)
        if not is_valid:
            return None, None, error, 400
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return None, None, "Username already exists", 409
        
        # Check if email already exists
        if User.query.filter_by(email=email.lower()).first():
            return None, None, "Email already registered", 409
        
        try:
            # Create new user
            user = User(
                username=username,
                email=email.lower(),
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role=role
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Generate tokens
            tokens = generate_tokens(user.id)
            
            return user.to_dict(), tokens, None, 201
            
        except Exception as e:
            db.session.rollback()
            return None, None, str(e), 500
    
    @staticmethod
    def login_user(email, password):
        """
        Authenticate a user and generate tokens
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            tuple: (user_dict, tokens_dict, error_message, status_code)
        """
        if not email or not password:
            return None, None, "Email and password are required", 400
        
        # Find user by email
        user = User.query.filter_by(email=email.lower()).first()
        
        if not user:
            return None, None, "Invalid credentials", 401
        
        # Verify password
        if not user.check_password(password):
            return None, None, "Invalid credentials", 401
        
        # Check if account is active
        if not user.is_active:
            return None, None, "Account is deactivated", 403
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate tokens
        tokens = generate_tokens(user.id)
        
        return user.to_dict(), tokens, None, 200
    
    @staticmethod
    def refresh_access_token(user_id):
        """
        Generate a new access token for a user
        
        Args:
            user_id: The user's ID
            
        Returns:
            tuple: (access_token, error_message, status_code)
        """
        user = User.query.get(user_id)
        
        if not user:
            return None, "User not found", 401
        
        if not user.is_active:
            return None, "Account is deactivated", 403
        
        # Generate new access token
        access_token = create_access_token(identity=str(user.id))
        
        return access_token, None, 200
    
    @staticmethod
    def verify_email(user_id):
        """
        Mark a user's email as verified
        
        Args:
            user_id: The user's ID
            
        Returns:
            tuple: (success, error_message, status_code)
        """
        user = User.query.get(user_id)
        
        if not user:
            return False, "User not found", 404
        
        if user.email_verified:
            return False, "Email already verified", 400
        
        user.email_verified = True
        db.session.commit()
        
        return True, None, 200
    
    @staticmethod
    def request_password_reset(email):
        """
        Generate a password reset token for a user
        
        Args:
            email: User's email address
            
        Returns:
            tuple: (reset_token, error_message, status_code)
        """
        user = User.query.filter_by(email=email.lower()).first()
        
        # Always return success to prevent email enumeration
        if not user:
            return None, None, 200
        
        # Generate reset token (1 hour expiration)
        reset_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=1),
            additional_claims={'type': 'password_reset'}
        )
        
        # TODO: Send email with reset token
        # For now, just return the token
        
        return reset_token, None, 200
    
    @staticmethod
    def reset_password(user_id, new_password):
        """
        Reset a user's password
        
        Args:
            user_id: The user's ID
            new_password: The new password
            
        Returns:
            tuple: (success, error_message, status_code)
        """
        # Validate new password
        is_valid, error = validate_password(new_password)
        if not is_valid:
            return False, error, 400
        
        user = User.query.get(user_id)
        
        if not user:
            return False, "User not found", 404
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return True, None, 200
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """
        Change a user's password (requires old password)
        
        Args:
            user_id: The user's ID
            old_password: The current password
            new_password: The new password
            
        Returns:
            tuple: (success, error_message, status_code)
        """
        user = User.query.get(user_id)
        
        if not user:
            return False, "User not found", 404
        
        # Verify old password
        if not user.check_password(old_password):
            return False, "Current password is incorrect", 401
        
        # Validate new password
        is_valid, error = validate_password(new_password)
        if not is_valid:
            return False, error, 400
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return True, None, 200
