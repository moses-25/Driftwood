"""
JWT utility functions for token generation and validation
"""
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from datetime import timedelta

def generate_tokens(user_id):
    """
    Generate access and refresh tokens for a user
    
    Args:
        user_id: The user's ID
        
    Returns:
        dict: Dictionary containing access_token and refresh_token
    """
    access_token = create_access_token(identity=str(user_id))
    refresh_token = create_refresh_token(identity=str(user_id))
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

def generate_access_token(user_id, expires_delta=None):
    """
    Generate an access token for a user
    
    Args:
        user_id: The user's ID
        expires_delta: Optional custom expiration time
        
    Returns:
        str: JWT access token
    """
    if expires_delta:
        return create_access_token(identity=str(user_id), expires_delta=expires_delta)
    return create_access_token(identity=str(user_id))

def generate_refresh_token(user_id, expires_delta=None):
    """
    Generate a refresh token for a user
    
    Args:
        user_id: The user's ID
        expires_delta: Optional custom expiration time
        
    Returns:
        str: JWT refresh token
    """
    if expires_delta:
        return create_refresh_token(identity=str(user_id), expires_delta=expires_delta)
    return create_refresh_token(identity=str(user_id))

def get_current_user_id():
    """
    Get the current user's ID from the JWT token
    
    Returns:
        str: User ID from the token
    """
    return get_jwt_identity()
