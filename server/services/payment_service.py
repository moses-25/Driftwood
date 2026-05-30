import requests
import base64
import logging
from datetime import datetime
from typing import Dict, Optional
from config import Config
from utils.payment_utils import (
    validate_phone_number,
    format_amount,
    validate_amount,
    generate_payment_reference,
    parse_mpesa_callback,
    verify_webhook_signature,
    sanitize_callback_data
)

# Set up logging
logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self):
        self.mpesa_base_url = "https://sandbox.safaricom.co.ke"  # Use production URL in production
        self.consumer_key = Config.MPESA_CONSUMER_KEY
        self.consumer_secret = Config.MPESA_CONSUMER_SECRET
        self.shortcode = Config.MPESA_SHORTCODE
        self.passkey = Config.MPESA_PASSKEY
    
    def get_mpesa_access_token(self):
        """Get M-Pesa access token"""
        try:
            api_url = f"{self.mpesa_base_url}/oauth/v1/generate?grant_type=client_credentials"
            
            # Create basic auth header
            credentials = f"{self.consumer_key}:{self.consumer_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            
            return response.json()['access_token']
        except Exception as e:
            print(f"Error getting M-Pesa token: {e}")
            return None
    
    def process_mpesa_payment(self, order, phone_number):
        """Process M-Pesa STK Push payment"""
        try:
            # Validate phone number
            is_valid, formatted_phone = validate_phone_number(phone_number)
            if not is_valid:
                return {'success': False, 'error': 'Invalid phone number format'}
            
            # Validate amount
            is_valid, error_msg = validate_amount(order.total_amount)
            if not is_valid:
                return {'success': False, 'error': error_msg}
            
            access_token = self.get_mpesa_access_token()
            if not access_token:
                logger.error("Failed to get M-Pesa access token")
                return {'success': False, 'error': 'Failed to get access token'}
            
            api_url = f"{self.mpesa_base_url}/mpesa/stkpush/v1/processrequest"
            
            # Generate timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # Generate password
            password_string = f"{self.shortcode}{self.passkey}{timestamp}"
            password = base64.b64encode(password_string.encode()).decode()
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": format_amount(order.total_amount),
                "PartyA": formatted_phone,
                "PartyB": self.shortcode,
                "PhoneNumber": formatted_phone,
                "CallBackURL": f"{Config.APP_URL}/api/payments/mpesa/callback",
                "AccountReference": order.order_number,
                "TransactionDesc": f"Payment for order {order.order_number}"
            }
            
            logger.info(f"Initiating M-Pesa payment for order {order.order_number}")
            
            response = requests.post(api_url, json=payload, headers=headers)
            
            # Log the response for debugging
            logger.info(f"M-Pesa API Response Status: {response.status_code}")
            logger.info(f"M-Pesa API Response Body: {response.text}")
            
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ResponseCode') == '0':
                logger.info(f"M-Pesa payment initiated successfully for order {order.order_number}")
                return {
                    'success': True,
                    'reference': result.get('CheckoutRequestID'),
                    'message': 'Payment initiated successfully. Please check your phone to complete the payment.'
                }
            else:
                logger.warning(f"M-Pesa payment failed for order {order.order_number}: {result.get('ResponseDescription')}")
                return {
                    'success': False,
                    'error': result.get('ResponseDescription', 'Payment failed')
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"M-Pesa API request failed: {str(e)}")
            return {'success': False, 'error': 'Payment service temporarily unavailable'}
        except Exception as e:
            logger.error(f"Unexpected error in M-Pesa payment: {str(e)}")
            return {'success': False, 'error': 'An unexpected error occurred'}
    
 
    def process_payment(self, order, payment_method, **kwargs):
        """Main payment processing method"""
        if payment_method == 'mpesa':
            phone_number = kwargs.get('phone_number', order.user.phone)
            return self.process_mpesa_payment(order, phone_number)
        elif payment_method == 'cash':
            return {
                'success': True,
                'reference': f"cash_{order.order_number}",
                'message': 'Cash payment - to be collected on pickup/delivery'
            }
        else:
            return {'success': False, 'error': 'Invalid payment method'}
    
    
    def query_payment_status(self, checkout_request_id: str) -> Dict:
        """
        Query M-Pesa payment status
        
        Args:
            checkout_request_id: CheckoutRequestID from STK Push
            
        Returns:
            Payment status information
        """
        try:
            access_token = self.get_mpesa_access_token()
            if not access_token:
                return {'success': False, 'error': 'Failed to get access token'}
            
            api_url = f"{self.mpesa_base_url}/mpesa/stkpushquery/v1/query"
            
            # Generate timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # Generate password
            password_string = f"{self.shortcode}{self.passkey}{timestamp}"
            password = base64.b64encode(password_string.encode()).decode()
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                'success': True,
                'result_code': result.get('ResultCode'),
                'result_desc': result.get('ResultDesc'),
                'status': 'completed' if result.get('ResultCode') == '0' else 'pending'
            }
            
        except Exception as e:
            logger.error(f"Error querying payment status: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    
    def process_refund(self, payment, refund_amount: Optional[float] = None, reason: str = '') -> Dict:
        """
        Process payment refund
        
        Args:
            payment: Payment object to refund
            refund_amount: Amount to refund (None for full refund)
            reason: Refund reason
            
        Returns:
            Refund result
        """
        try:
            from utils.payment_utils import validate_refund_amount
            
            # Determine refund amount
            if refund_amount is None:
                refund_amount = payment.amount
            
            # Validate refund amount
            already_refunded = getattr(payment, 'refunded_amount', 0.0) or 0.0
            is_valid, error_msg = validate_refund_amount(
                refund_amount, 
                payment.amount, 
                already_refunded
            )
            
            if not is_valid:
                return {'success': False, 'error': error_msg}
            
            # For M-Pesa, we need to use B2C API for refunds
            if payment.payment_method == 'mpesa':
                return self._process_mpesa_refund(payment, refund_amount, reason)
            elif payment.payment_method == 'cash':
                # Cash refunds are handled manually
                return {
                    'success': True,
                    'reference': f"refund_{payment.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'message': 'Cash refund approved. Please process manually.',
                    'refund_amount': refund_amount
                }
            else:
                return {'success': False, 'error': 'Refund not supported for this payment method'}
                
        except Exception as e:
            logger.error(f"Error processing refund: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    
    def _process_mpesa_refund(self, payment, refund_amount: float, reason: str) -> Dict:
        """
        Process M-Pesa B2C refund
        
        Args:
            payment: Payment object
            refund_amount: Amount to refund
            reason: Refund reason
            
        Returns:
            Refund result
        """
        try:
            access_token = self.get_mpesa_access_token()
            if not access_token:
                return {'success': False, 'error': 'Failed to get access token'}
            
            # M-Pesa B2C API endpoint
            api_url = f"{self.mpesa_base_url}/mpesa/b2c/v1/paymentrequest"
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Get initiator credentials (you need to set these in config)
            initiator_name = getattr(Config, 'MPESA_INITIATOR_NAME', 'testapi')
            security_credential = getattr(Config, 'MPESA_SECURITY_CREDENTIAL', '')
            
            payload = {
                "InitiatorName": initiator_name,
                "SecurityCredential": security_credential,
                "CommandID": "BusinessPayment",  # For refunds
                "Amount": format_amount(refund_amount),
                "PartyA": self.shortcode,
                "PartyB": payment.mpesa_phone_number,
                "Remarks": f"Refund: {reason}",
                "QueueTimeOutURL": f"{Config.APP_URL}/api/payments/mpesa/timeout",
                "ResultURL": f"{Config.APP_URL}/api/payments/mpesa/refund-callback",
                "Occasion": f"Refund for payment {payment.id}"
            }
            
            logger.info(f"Initiating M-Pesa refund for payment {payment.id}")
            
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ResponseCode') == '0':
                logger.info(f"M-Pesa refund initiated successfully for payment {payment.id}")
                return {
                    'success': True,
                    'reference': result.get('ConversationID'),
                    'message': 'Refund initiated successfully',
                    'refund_amount': refund_amount
                }
            else:
                logger.warning(f"M-Pesa refund failed for payment {payment.id}: {result.get('ResponseDescription')}")
                return {
                    'success': False,
                    'error': result.get('ResponseDescription', 'Refund failed')
                }
                
        except Exception as e:
            logger.error(f"Error processing M-Pesa refund: {str(e)}")
            return {'success': False, 'error': 'Refund service temporarily unavailable'}
    
    
    def retry_failed_payment(self, payment) -> Dict:
        """
        Retry a failed payment
        
        Args:
            payment: Payment object to retry
            
        Returns:
            Retry result
        """
        try:
            if payment.status != 'failed':
                return {'success': False, 'error': 'Only failed payments can be retried'}
            
            # Get the order
            from models.order import Order
            order = Order.query.get(payment.order_id)
            
            if not order:
                return {'success': False, 'error': 'Order not found'}
            
            # Retry the payment
            if payment.payment_method == 'mpesa':
                return self.process_mpesa_payment(order, payment.mpesa_phone_number)
            else:
                return {'success': False, 'error': 'Retry not supported for this payment method'}
                
        except Exception as e:
            logger.error(f"Error retrying payment: {str(e)}")
            return {'success': False, 'error': str(e)}
