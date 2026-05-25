"""
Input validation utilities
"""
import re

def validate_email(email):
    """
    Validate email format using RFC 5322 regex
    
    Args:
        email: Email string to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    # RFC 5322 simplified regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    
    return True, None

def validate_password(password):
    """
    Validate password strength
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        return False, "Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)"
    
    return True, None

def validate_username(username):
    """
    Validate username format
    
    Requirements:
    - Between 3 and 80 characters
    - Only alphanumeric characters, underscores, and hyphens
    
    Args:
        username: Username string to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 80:
        return False, "Username must be at most 80 characters long"
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    
    return True, None

def validate_phone(phone):
    """
    Validate phone number format (Kenyan format)
    
    Args:
        phone: Phone number string to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not phone:
        return True, None  # Phone is optional
    
    # Remove spaces and common separators
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Kenyan phone format: +254XXXXXXXXX or 07XXXXXXXX or 01XXXXXXXX
    kenyan_pattern = r'^(\+254|254|0)[17]\d{8}$'
    
    if not re.match(kenyan_pattern, cleaned_phone):
        return False, "Invalid phone number format. Use format: +254XXXXXXXXX or 07XXXXXXXX"
    
    return True, None
