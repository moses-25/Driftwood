"""
Payment routes
Handles all payment-related API endpoints
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.payment_service import PaymentService
from models.order import Order
from models.payment import Payment
from models.user import User
from extensions import db
from utils.decorators import admin_required, staff_required
from utils.payment_utils import parse_mpesa_callback, sanitize_callback_data
import logging

payment_bp = Blueprint('payment', __name__)
logger = logging.getLogger(__name__)


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
        
        # Log sanitized callback for debugging
        sanitized = sanitize_callback_data(data)
        logger.info(f"M-Pesa Callback received: {sanitized}")
        
        # Parse callback data
        parsed = parse_mpesa_callback(data)
        
        if not parsed['checkout_request_id']:
            logger.warning("Callback missing checkout_request_id")
            return jsonify({'success': True, 'message': 'Callback received'}), 200
        
        # Find payment by checkout request ID
        payment = Payment.query.filter_by(
            mpesa_checkout_request_id=parsed['checkout_request_id']
        ).first()
        
        if not payment:
            logger.warning(f"Payment not found for checkout_request_id: {parsed['checkout_request_id']}")
            return jsonify({'success': True, 'message': 'Payment not found'}), 200
        
        order = Order.query.get(payment.order_id)
        
        if parsed['success']:
            # Payment successful
            logger.info(f"Payment successful for order {order.order_number}")
            
            payment.mark_as_completed(
                transaction_id=parsed['mpesa_receipt'],
                receipt_number=parsed['mpesa_receipt']
            )
            
            order.payment_status = 'paid'
            order.payment_reference = parsed['mpesa_receipt']
            order.status = 'confirmed'  # Auto-confirm order on successful payment
            
        else:
            # Payment failed
            logger.warning(f"Payment failed for order {order.order_number}: {parsed['result_description']}")
            
            payment.mark_as_failed(parsed['result_description'])
            order.payment_status = 'failed'
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Callback processed'}), 200
        
    except Exception as e:
        logger.error(f"M-Pesa Callback error: {str(e)}")
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


@payment_bp.route('/payments/query/<checkout_request_id>', methods=['GET'])
@jwt_required()
def query_payment_status(checkout_request_id):
    """
    Query M-Pesa payment status
    
    Path Parameters:
        checkout_request_id (str): CheckoutRequestID from STK Push
        
    Returns:
        200: Payment status
        404: Payment not found
        500: Server error
    """
    try:
        payment_service = PaymentService()
        result = payment_service.query_payment_status(checkout_request_id)
        
        if result['success']:
            # Update payment status if needed
            payment = Payment.query.filter_by(
                mpesa_checkout_request_id=checkout_request_id
            ).first()
            
            if payment and result.get('status') == 'completed' and payment.status == 'pending':
                payment.mark_as_completed()
                db.session.commit()
            
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error querying payment status: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@payment_bp.route('/payments/<int:payment_id>/refund', methods=['POST'])
@jwt_required()
@admin_required
def refund_payment(payment_id):
    """
    Process payment refund (Admin only)
    
    Path Parameters:
        payment_id (int): Payment ID
        
    Request Body:
        refund_amount (float): Amount to refund (optional, defaults to full refund)
        reason (str): Refund reason (optional)
        
    Returns:
        200: Refund processed
        400: Validation error
        404: Payment not found
        500: Server error
    """
    try:
        data = request.get_json() or {}
        
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'success': False, 'error': 'Payment not found'}), 404
        
        if payment.status != 'completed':
            return jsonify({'success': False, 'error': 'Only completed payments can be refunded'}), 400
        
        refund_amount = data.get('refund_amount')
        reason = data.get('reason', 'Refund requested by admin')
        
        payment_service = PaymentService()
        result = payment_service.process_refund(payment, refund_amount, reason)
        
        if result['success']:
            # Update payment status
            if refund_amount and refund_amount < payment.amount:
                payment.status = 'partially_refunded'
                payment.refunded_amount = (payment.refunded_amount or 0) + refund_amount
            else:
                payment.status = 'refunded'
                payment.refunded_amount = payment.amount
            
            payment.refund_reference = result.get('reference')
            payment.refund_reason = reason
            
            # Update order status
            order = Order.query.get(payment.order_id)
            order.payment_status = 'refunded'
            order.status = 'cancelled'
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': result.get('message', 'Refund processed successfully'),
                'data': {
                    'refund_amount': result.get('refund_amount'),
                    'refund_reference': result.get('reference')
                }
            }), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error processing refund: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@payment_bp.route('/payments/<int:payment_id>/retry', methods=['POST'])
@jwt_required()
def retry_payment(payment_id):
    """
    Retry a failed payment
    
    Path Parameters:
        payment_id (int): Payment ID
        
    Returns:
        200: Payment retry initiated
        400: Validation error
        404: Payment not found
        500: Server error
    """
    try:
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'success': False, 'error': 'Payment not found'}), 404
        
        # Verify user owns this payment
        current_user_id = get_jwt_identity()
        order = Order.query.get(payment.order_id)
        
        if order.user_id != current_user_id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        payment_service = PaymentService()
        result = payment_service.retry_failed_payment(payment)
        
        if result['success']:
            # Create new payment record for retry
            new_payment = Payment(
                order_id=payment.order_id,
                amount=payment.amount,
                payment_method=payment.payment_method,
                mpesa_phone_number=payment.mpesa_phone_number,
                mpesa_checkout_request_id=result.get('reference'),
                status='pending'
            )
            db.session.add(new_payment)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': result.get('message', 'Payment retry initiated'),
                'data': {
                    'payment_id': new_payment.id,
                    'checkout_request_id': result.get('reference')
                }
            }), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error retrying payment: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@payment_bp.route('/payments/history', methods=['GET'])
@jwt_required()
def get_payment_history():
    """
    Get payment history for current user
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10)
        status (str): Filter by status (optional)
        
    Returns:
        200: Payment history
        500: Server error
    """
    try:
        current_user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        # Get user's orders
        query = Payment.query.join(Order).filter(Order.user_id == current_user_id)
        
        if status:
            query = query.filter(Payment.status == status)
        
        query = query.order_by(Payment.created_at.desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'payments': [payment.to_dict() for payment in pagination.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'pages': pagination.pages
                }
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting payment history: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@payment_bp.route('/payments/reports', methods=['GET'])
@jwt_required()
@staff_required
def get_payment_reports():
    """
    Get payment reports (Staff/Admin only)
    
    Query Parameters:
        start_date (str): Start date (YYYY-MM-DD)
        end_date (str): End date (YYYY-MM-DD)
        status (str): Filter by status (optional)
        
    Returns:
        200: Payment reports
        500: Server error
    """
    try:
        from datetime import datetime
        from sqlalchemy import func
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')
        
        query = Payment.query
        
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Payment.created_at >= start)
        
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Payment.created_at <= end)
        
        if status:
            query = query.filter(Payment.status == status)
        
        # Get statistics
        total_payments = query.count()
        total_amount = db.session.query(func.sum(Payment.amount)).filter(
            Payment.id.in_([p.id for p in query.all()])
        ).scalar() or 0
        
        # Group by status
        status_breakdown = db.session.query(
            Payment.status,
            func.count(Payment.id),
            func.sum(Payment.amount)
        ).filter(
            Payment.id.in_([p.id for p in query.all()])
        ).group_by(Payment.status).all()
        
        # Group by payment method
        method_breakdown = db.session.query(
            Payment.payment_method,
            func.count(Payment.id),
            func.sum(Payment.amount)
        ).filter(
            Payment.id.in_([p.id for p in query.all()])
        ).group_by(Payment.payment_method).all()
        
        return jsonify({
            'success': True,
            'data': {
                'summary': {
                    'total_payments': total_payments,
                    'total_amount': float(total_amount)
                },
                'by_status': [
                    {
                        'status': status,
                        'count': count,
                        'amount': float(amount or 0)
                    }
                    for status, count, amount in status_breakdown
                ],
                'by_method': [
                    {
                        'method': method,
                        'count': count,
                        'amount': float(amount or 0)
                    }
                    for method, count, amount in method_breakdown
                ]
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating payment reports: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@payment_bp.route('/payments/mpesa/timeout', methods=['POST'])
def mpesa_timeout():
    """
    M-Pesa timeout callback
    Called when payment request times out
    """
    try:
        data = request.get_json()
        logger.warning(f"M-Pesa timeout received: {sanitize_callback_data(data)}")
        
        return jsonify({'success': True, 'message': 'Timeout received'}), 200
        
    except Exception as e:
        logger.error(f"M-Pesa timeout error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@payment_bp.route('/payments/mpesa/refund-callback', methods=['POST'])
def mpesa_refund_callback():
    """
    M-Pesa refund callback
    Called when refund is completed
    """
    try:
        data = request.get_json()
        logger.info(f"M-Pesa refund callback received: {sanitize_callback_data(data)}")
        
        # Process refund callback
        # Implementation depends on M-Pesa B2C callback structure
        
        return jsonify({'success': True, 'message': 'Refund callback processed'}), 200
        
    except Exception as e:
        logger.error(f"M-Pesa refund callback error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
