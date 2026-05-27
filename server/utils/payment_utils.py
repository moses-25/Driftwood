"""
Payment utility functions
Helper functions for payment processing, validation, and formatting
"""
import re
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


def validate_phone_number(phone: str, country_code: str = '254') -> Tuple[bool, Optional[str]]:
    """
    Validate and format phone number for M-Pesa
    
    Args:
        phone: Phone number to validate
        country_code: Country code (default: 254 for Kenya)
        
    Returns:
        Tuple of (is_valid, formatted_phone)
    """
    if not phone:
        return False, None
    
    # Remove all non-digit characters
    phone = re.sub(r'\D', '', phone)
    
    # Handle different formats
    if phone.startswith('0'):
        # Convert 0712345678 to 254712345678
        phone = country_code + phone[1:]
    elif phone.startswith('+'):
        # Remove + sign
        phone = phone[1:]
    elif not phone.startswith(country_code):
        # Add country code if missing
        phone = country_code + phone
    
    # Validate length (Kenyan numbers: 254 + 9 digits = 12 digits)
    if len(phone) != 12:
        return False, None
    
    # Validate it starts with correct country code
    if not phone.startswith(country_code):
        return False, None
    
    return True, phone


def format_amount(amount: float) -> int:
    """
    Format amount for M-Pesa (must be integer)
    
    Args:
        amount: Amount to format
        
    Returns:
        Integer amount
    """
    return int(round(amount))


def validate_amount(amount: float, min_amount: float = 1.0, max_amount: float = 150000.0) -> Tuple[bool, Optional[str]]:
    """
    Validate payment amount
    
    Args:
        amount: Amount to validate
        min_amount: Minimum allowed amount (default: 1 KES)
        max_amount: Maximum allowed amount (default: 150,000 KES)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if amount < min_amount:
        return False, f"Amount must be at least {min_amount} KES"
    
    if amount > max_amount:
        return False, f"Amount cannot exceed {max_amount} KES"
    
    return True, None


def generate_payment_reference(order_number: str, timestamp: Optional[datetime] = None) -> str:
    """
    Generate unique payment reference
    
    Args:
        order_number: Order number
        timestamp: Optional timestamp (defaults to now)
        
    Returns:
        Unique payment reference
    """
    if timestamp is None:
        timestamp = datetime.utcnow()
    
    timestamp_str = timestamp.strftime('%Y%m%d%H%M%S')
    return f"PAY-{order_number}-{timestamp_str}"


def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    """
    Verify M-Pesa webhook signature
    
    Args:
        payload: Raw webhook payload
        signature: Signature from webhook header
        secret: Webhook secret key
        
    Returns:
        True if signature is valid
    """
    try:
        expected_signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    except Exception:
        return False


def parse_mpesa_callback(callback_data: Dict) -> Dict:
    """
    Parse M-Pesa callback data into standardized format
    
    Args:
        callback_data: Raw M-Pesa callback data
        
    Returns:
        Parsed callback data
    """
    result = {
        'success': False,
        'checkout_request_id': None,
        'result_code': None,
        'result_description': None,
        'amount': None,
        'mpesa_receipt': None,
        'transaction_date': None,
        'phone_number': None
    }
    
    try:
        if 'Body' in callback_data and 'stkCallback' in callback_data['Body']:
            stk_callback = callback_data['Body']['stkCallback']
            
            result['checkout_request_id'] = stk_callback.get('CheckoutRequestID')
            result['result_code'] = stk_callback.get('ResultCode')
            result['result_description'] = stk_callback.get('ResultDesc')
            
            # Success if result code is 0
            result['success'] = result['result_code'] == 0
            
            # Parse callback metadata
            if 'CallbackMetadata' in stk_callback:
                items = stk_callback['CallbackMetadata'].get('Item', [])
                
                for item in items:
                    name = item.get('Name')
                    value = item.get('Value')
                    
                    if name == 'Amount':
                        result['amount'] = value
                    elif name == 'MpesaReceiptNumber':
                        result['mpesa_receipt'] = value
                    elif name == 'TransactionDate':
                        result['transaction_date'] = value
                    elif name == 'PhoneNumber':
                        result['phone_number'] = value
        
        return result
    except Exception as e:
        result['result_description'] = f"Error parsing callback: {str(e)}"
        return result


def calculate_transaction_fee(amount: float, fee_percentage: float = 0.0) -> float:
    """
    Calculate transaction fee
    
    Args:
        amount: Transaction amount
        fee_percentage: Fee percentage (default: 0%)
        
    Returns:
        Transaction fee
    """
    return round(amount * (fee_percentage / 100), 2)


def is_payment_expired(created_at: datetime, expiry_minutes: int = 5) -> bool:
    """
    Check if payment request has expired
    
    Args:
        created_at: Payment creation timestamp
        expiry_minutes: Expiry time in minutes (default: 5)
        
    Returns:
        True if payment has expired
    """
    expiry_time = created_at + timedelta(minutes=expiry_minutes)
    return datetime.utcnow() > expiry_time


def format_payment_status(status: str) -> str:
    """
    Format payment status for display
    
    Args:
        status: Payment status
        
    Returns:
        Formatted status
    """
    status_map = {
        'pending': 'Pending',
        'completed': 'Completed',
        'failed': 'Failed',
        'cancelled': 'Cancelled',
        'refunded': 'Refunded',
        'partially_refunded': 'Partially Refunded'
    }
    
    return status_map.get(status.lower(), status.title())


def get_payment_method_display_name(method: str) -> str:
    """
    Get display name for payment method
    
    Args:
        method: Payment method code
        
    Returns:
        Display name
    """
    method_map = {
        'mpesa': 'M-Pesa',
        'cash': 'Cash',
        'card': 'Card',
        'bank_transfer': 'Bank Transfer'
    }
    
    return method_map.get(method.lower(), method.title())


def sanitize_callback_data(data: Dict) -> Dict:
    """
    Sanitize callback data for logging (remove sensitive info)
    
    Args:
        data: Callback data
        
    Returns:
        Sanitized data
    """
    sensitive_fields = ['Password', 'password', 'secret', 'token']
    
    sanitized = data.copy()
    
    for field in sensitive_fields:
        if field in sanitized:
            sanitized[field] = '***REDACTED***'
    
    return sanitized


def validate_refund_amount(refund_amount: float, original_amount: float, already_refunded: float = 0.0) -> Tuple[bool, Optional[str]]:
    """
    Validate refund amount
    
    Args:
        refund_amount: Amount to refund
        original_amount: Original payment amount
        already_refunded: Amount already refunded
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if refund_amount <= 0:
        return False, "Refund amount must be greater than 0"
    
    remaining_amount = original_amount - already_refunded
    
    if refund_amount > remaining_amount:
        return False, f"Refund amount cannot exceed remaining amount ({remaining_amount} KES)"
    
    return True, None


def generate_transaction_id(prefix: str = 'TXN') -> str:
    """
    Generate unique transaction ID
    
    Args:
        prefix: Transaction ID prefix
        
    Returns:
        Unique transaction ID
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    return f"{prefix}-{timestamp}"
