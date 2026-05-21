import requests
import base64
from datetime import datetime
from config import Config

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
            access_token = self.get_mpesa_access_token()
            if not access_token:
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
                "Amount": int(order.total_amount),
                "PartyA": phone_number,
                "PartyB": self.shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": "https://yourdomain.com/api/mpesa/callback",
                "AccountReference": order.order_number,
                "TransactionDesc": f"Payment for order {order.order_number}"
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ResponseCode') == '0':
                return {
                    'success': True,
                    'reference': result.get('CheckoutRequestID'),
                    'message': 'Payment initiated successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.get('ResponseDescription', 'Payment failed')
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
 
    def process_payment(self, order, payment_method, **kwargs):
        """Main payment processing method"""
        if payment_method == 'mpesa':
            phone_number = kwargs.get('phone_number', order.customer.phone)
            return self.process_mpesa_payment(order, phone_number)
        elif payment_method == 'cash':
            return {
                'success': True,
                'reference': f"cash_{order.order_number}",
                'message': 'Cash payment - to be collected on pickup/delivery'
            }
        else:
            return {'success': False, 'error': 'Invalid payment method'}