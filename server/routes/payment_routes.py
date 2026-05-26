"""
Payment routes
Handles all payment-related API endpoints
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.payment_service import PaymentService
from models.order import Order
from models.payment import Payment
from extensions import db

payment_bp = Blueprint('payment', __name__)


@payment_bp.route('/payments/mpesa/initiate', methods=['POST'])
def initiate_mpesa_payment():
    """
    Initiate M-Pesa STK Push payment
    
    Request Body:
        order_id (int): Order ID (required)
        phone_number (str): M-Pesa phone number (required)
        
    Returns:
        200: Payment initiated successfully
        400: Validation error
        404: Order not found
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'order_id' not in data or 'phone_number' not in data:
            return jsonify({'success': False, 'error': 'order_id and phone_number are required'}), 400
        
        # Get order
        order = Order.query.get(data['order_id'])
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        
        # Check if order already paid
        if order.payment_status == 'paid':
            return jsonify({'success': False, 'error': 'Order already paid'}), 400
        
        # Initiate M-Pesa payment
        payment_service = PaymentService()
        result = payment_service.process_mpesa_payment(order, data['phone_number'])
        
        if result['success']:
            # Create payment record
            payment = Payment(
                order_id=order.id,
                amount=order.total_amount,
                payment_method='mpesa',
                mpesa_phone_number=data['phone_number'],
                mpesa_checkout_request_id=result.get('reference'),
                status='pending'
            )
            db.session.add(payment)
            
            # Update order payment status
            order.payment_status = 'pending'
            order.payment_reference = result.get('reference')
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': result.get('message', 'Payment initiated successfully'),
                'data': {
                    'checkout_request_id': result.get('reference'),
                    'order_id': order.id,
                    'order_number': order.order_number
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Payment initiation failed')
            }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500



@payment_bp.route('/payments/mpesa/callback', methods=['POST'])
def mpesa_callback():
    """
    M-Pesa payment callback webhook
    Called by Safaricom when payment is completed
    
    Request Body:
        M-Pesa callback data
        
    Returns:
        200: Callback processed
        500: Server error
    """
    try:
        data = request.get_json()
        
        # Log callback for debugging
        print(f"M-Pesa Callback received: {data}")
        
        # Extract callback data
        # Note: Actual M-Pesa callback structure may vary
        # This is a simplified version
        if 'Body' in data and 'stkCallback' in data['Body']:
            callback_data = data['Body']['stkCallback']
            checkout_request_id = callback_data.get('CheckoutRequestID')
            result_code = callback_data.get('ResultCode')
            result_desc = callback_data.get('ResultDesc')
            
            # Find payment by checkout request ID
            payment = Payment.query.filter_by(
                mpesa_checkout_request_id=checkout_request_id
            ).first()
            
            if payment:
                order = Order.query.get(payment.order_id)
                
                if result_code == 0:  # Success
                    # Extract transaction details
                    callback_metadata = callback_data.get('CallbackMetadata', {}).get('Item', [])
                    mpesa_receipt = None
                    transaction_date = None
                    
                    for item in callback_metadata:
                        if item.get('Name') == 'MpesaReceiptNumber':
                            mpesa_receipt = item.get('Value')
                        elif item.get('Name') == 'TransactionDate':
                            transaction_date = item.get('Value')
                    
                    # Update payment
                    payment.mark_as_completed(
                        transaction_id=mpesa_receipt,
                        receipt_number=mpesa_receipt
                    )
                    
                    # Update order
                    order.payment_status = 'paid'
                    order.payment_reference = mpesa_receipt
                    
                else:  # Failed
                    payment.mark_as_failed(result_desc)
                    order.payment_status = 'failed'
                
                db.session.commit()
        
        return jsonify({'success': True, 'message': 'Callback processed'}), 200
        
    except Exception as e:
        print(f"M-Pesa Callback error: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@payment_bp.route('/payments/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment_status(payment_id):
    """
    Get payment status
    
    Path Parameters:
        payment_id (int): Payment ID
        
    Returns:
        200: Payment details
        404: Payment not found
        500: Server error
    """
    try:
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'success': False, 'error': 'Payment not found'}), 404
        
        return jsonify({
            'success': True,
            'data': payment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@payment_bp.route('/payments/order/<int:order_id>', methods=['GET'])
def get_order_payment(order_id):
    """
    Get payment for an order
    
    Path Parameters:
        order_id (int): Order ID
        
    Returns:
        200: Payment details
        404: Payment not found
        500: Server error
    """
    try:
        payment = Payment.query.filter_by(order_id=order_id).first()
        
        if not payment:
            return jsonify({'success': False, 'error': 'Payment not found'}), 404
        
        return jsonify({
            'success': True,
            'data': payment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
