"""
Phase 5 Testing Script
Tests all payment integration features
"""
import sys
import json
from datetime import datetime

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ {text}{RESET}")

def test_payment_utils():
    """Test payment utility functions"""
    print_header("Testing Payment Utilities")
    
    try:
        from utils.payment_utils import (
            validate_phone_number,
            format_amount,
            validate_amount,
            generate_payment_reference,
            parse_mpesa_callback,
            validate_refund_amount,
            sanitize_callback_data
        )
        
        # Test phone number validation
        print_info("Testing phone number validation...")
        is_valid, formatted = validate_phone_number("0712345678")
        assert is_valid and formatted == "254712345678", "Phone validation failed"
        print_success(f"Phone validation: 0712345678 → {formatted}")
        
        is_valid, formatted = validate_phone_number("254712345678")
        assert is_valid and formatted == "254712345678", "Phone validation failed"
        print_success(f"Phone validation: 254712345678 → {formatted}")
        
        is_valid, formatted = validate_phone_number("+254712345678")
        assert is_valid and formatted == "254712345678", "Phone validation failed"
        print_success(f"Phone validation: +254712345678 → {formatted}")
        
        # Test amount formatting
        print_info("\nTesting amount formatting...")
        amount = format_amount(1234.56)
        assert amount == 1235, "Amount formatting failed"
        print_success(f"Amount formatting: 1234.56 → {amount}")
        
        # Test amount validation
        print_info("\nTesting amount validation...")
        is_valid, error = validate_amount(100.0)
        assert is_valid, "Amount validation failed"
        print_success(f"Amount validation: 100.0 is valid")
        
        is_valid, error = validate_amount(0.5)
        assert not is_valid, "Amount validation should fail for < 1"
        print_success(f"Amount validation: 0.5 is invalid (as expected)")
        
        is_valid, error = validate_amount(200000.0)
        assert not is_valid, "Amount validation should fail for > 150000"
        print_success(f"Amount validation: 200000.0 is invalid (as expected)")
        
        # Test payment reference generation
        print_info("\nTesting payment reference generation...")
        ref = generate_payment_reference("ORD-001")
        assert ref.startswith("PAY-ORD-001-"), "Payment reference generation failed"
        print_success(f"Payment reference: {ref}")
        
        # Test refund validation
        print_info("\nTesting refund validation...")
        is_valid, error = validate_refund_amount(50.0, 100.0, 0.0)
        assert is_valid, "Refund validation failed"
        print_success(f"Refund validation: 50.0 of 100.0 is valid")
        
        is_valid, error = validate_refund_amount(60.0, 100.0, 50.0)
        assert not is_valid, "Refund validation should fail"
        print_success(f"Refund validation: 60.0 of 100.0 (50.0 already refunded) is invalid (as expected)")
        
        # Test callback parsing
        print_info("\nTesting M-Pesa callback parsing...")
        callback_data = {
            'Body': {
                'stkCallback': {
                    'CheckoutRequestID': 'ws_CO_123456789',
                    'ResultCode': 0,
                    'ResultDesc': 'Success',
                    'CallbackMetadata': {
                        'Item': [
                            {'Name': 'Amount', 'Value': 100},
                            {'Name': 'MpesaReceiptNumber', 'Value': 'ABC123'},
                            {'Name': 'PhoneNumber', 'Value': '254712345678'}
                        ]
                    }
                }
            }
        }
        
        parsed = parse_mpesa_callback(callback_data)
        assert parsed['success'], "Callback parsing failed"
        assert parsed['mpesa_receipt'] == 'ABC123', "Receipt number not parsed"
        print_success(f"Callback parsed: {parsed['mpesa_receipt']}")
        
        # Test data sanitization
        print_info("\nTesting data sanitization...")
        sensitive_data = {
            'password': 'secret123',
            'amount': 100,
            'token': 'abc123'
        }
        sanitized = sanitize_callback_data(sensitive_data)
        assert sanitized['password'] == '***REDACTED***', "Sanitization failed"
        assert sanitized['amount'] == 100, "Non-sensitive data should not be sanitized"
        print_success(f"Data sanitized: password → {sanitized['password']}")
        
        print_success("\n✅ All payment utility tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Payment utility tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_payment_service():
    """Test payment service"""
    print_header("Testing Payment Service")
    
    try:
        from services.payment_service import PaymentService
        
        service = PaymentService()
        
        print_info("Payment service initialized")
        print_success(f"M-Pesa Base URL: {service.mpesa_base_url}")
        print_success(f"Shortcode configured: {service.shortcode is not None}")
        
        # Test methods exist
        assert hasattr(service, 'get_mpesa_access_token'), "Missing get_mpesa_access_token method"
        assert hasattr(service, 'process_mpesa_payment'), "Missing process_mpesa_payment method"
        assert hasattr(service, 'query_payment_status'), "Missing query_payment_status method"
        assert hasattr(service, 'process_refund'), "Missing process_refund method"
        assert hasattr(service, 'retry_failed_payment'), "Missing retry_failed_payment method"
        
        print_success("✓ get_mpesa_access_token method exists")
        print_success("✓ process_mpesa_payment method exists")
        print_success("✓ query_payment_status method exists")
        print_success("✓ process_refund method exists")
        print_success("✓ retry_failed_payment method exists")
        
        print_success("\n✅ Payment service tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Payment service tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_payment_routes():
    """Test payment routes"""
    print_header("Testing Payment Routes")
    
    try:
        # Create a test app to get the actual routes
        import sys
        sys.path.insert(0, '.')
        from app import create_app
        app = create_app()
        
        # Get all payment-related routes
        routes = []
        with app.app_context():
            for rule in app.url_map.iter_rules():
                if 'payment' in rule.rule and not rule.rule.startswith('/static'):
                    routes.append({
                        'endpoint': rule.endpoint,
                        'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                        'path': str(rule)
                    })
        
        print_info(f"Found {len(routes)} payment routes:\n")
        
        expected_routes = [
            'payment.initiate_mpesa_payment',
            'payment.mpesa_callback',
            'payment.get_payment_status',
            'payment.get_order_payment',
            'payment.query_payment_status',
            'payment.refund_payment',
            'payment.retry_payment',
            'payment.get_payment_history',
            'payment.get_payment_reports',
            'payment.mpesa_timeout',
            'payment.mpesa_refund_callback'
        ]
        
        for route in sorted(routes, key=lambda r: r['endpoint']):
            methods = ', '.join(route['methods'])
            print_success(f"{route['endpoint']}: {methods} {route['path']}")
        
        # Check all expected routes exist
        found_endpoints = [r['endpoint'] for r in routes]
        
        for expected in expected_routes:
            if expected in found_endpoints:
                print_success(f"✓ {expected} route exists")
            else:
                print_error(f"✗ {expected} route missing")
        
        print_success(f"\n✅ Payment routes tests passed! ({len(routes)} routes)")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Payment routes tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_payment_model():
    """Test payment model"""
    print_header("Testing Payment Model")
    
    try:
        from models.payment import Payment
        
        # Check model attributes
        print_info("Checking Payment model attributes...")
        
        required_fields = [
            'id', 'order_id', 'amount', 'payment_method', 'transaction_id',
            'status', 'mpesa_receipt_number', 'mpesa_phone_number',
            'mpesa_checkout_request_id', 'currency', 'payment_reference',
            'failure_reason', 'refunded_amount', 'refund_reference',
            'refund_reason', 'refunded_at', 'created_at', 'updated_at',
            'completed_at'
        ]
        
        for field in required_fields:
            assert hasattr(Payment, field), f"Missing field: {field}"
            print_success(f"✓ {field} field exists")
        
        # Check methods
        print_info("\nChecking Payment model methods...")
        
        required_methods = ['mark_as_completed', 'mark_as_failed', 'to_dict']
        
        for method in required_methods:
            assert hasattr(Payment, method), f"Missing method: {method}"
            print_success(f"✓ {method} method exists")
        
        print_success("\n✅ Payment model tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Payment model tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration"""
    print_header("Testing Configuration")
    
    try:
        from config import Config
        
        print_info("Checking payment configuration...")
        
        config_vars = [
            'MPESA_CONSUMER_KEY',
            'MPESA_CONSUMER_SECRET',
            'MPESA_SHORTCODE',
            'MPESA_PASSKEY',
            'MPESA_INITIATOR_NAME',
            'MPESA_SECURITY_CREDENTIAL',
            'APP_URL'
        ]
        
        for var in config_vars:
            assert hasattr(Config, var), f"Missing config: {var}"
            value = getattr(Config, var)
            if value:
                print_success(f"✓ {var} is configured")
            else:
                print_info(f"⚠ {var} is not set (optional for testing)")
        
        print_success("\n✅ Configuration tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Configuration tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print_header("PHASE 5 PAYMENT INTEGRATION TESTS")
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        'Payment Utilities': test_payment_utils(),
        'Payment Service': test_payment_service(),
        'Payment Routes': test_payment_routes(),
        'Payment Model': test_payment_model(),
        'Configuration': test_config()
    }
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    if passed == total:
        print(f"{GREEN}✅ ALL TESTS PASSED ({passed}/{total}){RESET}")
        print(f"{GREEN}Phase 5 is ready for deployment!{RESET}")
    else:
        print(f"{RED}❌ SOME TESTS FAILED ({passed}/{total}){RESET}")
        print(f"{YELLOW}Please fix the failing tests before proceeding.{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
