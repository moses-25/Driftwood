from flask import Blueprint, jsonify, request
from models.order import Order
from models.order_item import OrderItem
from models.customer import Customer
from models.menu_item import MenuItem
from extensions import db
from datetime import datetime, timedelta
from services.payment_service import PaymentService

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        
        # Get or create customer
        customer_data = data['customerInfo']
        customer = Customer.query.filter_by(email=customer_data['email']).first()
        
        if not customer:
            customer = Customer(
                name=customer_data['name'],
                email=customer_data['email'],
                phone=customer_data.get('phone'),
                address=data.get('deliveryInfo', {}).get('address')
            )
            db.session.add(customer)
            db.session.flush()  # Get customer ID
        
        # Create order
        order = Order(
            customer_id=customer.id,
            total_amount=data['totalAmount'],
            order_type=data['orderType'],
            payment_method=data['paymentMethod'],
            delivery_address=data.get('deliveryInfo', {}).get('address'),
            delivery_instructions=data.get('deliveryInfo', {}).get('instructions'),
            estimated_ready_time=datetime.utcnow() + timedelta(minutes=20)  # Default 20 min
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add order items
        total_calculated = 0
        for item_data in data['items']:
            menu_item = MenuItem.query.get(item_data['id'])
            if not menu_item:
                raise ValueError(f"Menu item {item_data['id']} not found")
            
            unit_price = float(menu_item.price)
            total_price = unit_price * item_data['quantity']
            total_calculated += total_price
            
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=item_data['quantity'],
                unit_price=unit_price,
                total_price=total_price
            )
            
            if 'customizations' in item_data:
                order_item.set_customizations(item_data['customizations'])
            
            db.session.add(order_item)
        
        # Verify total amount
        if abs(total_calculated - float(data['totalAmount'])) > 0.01:
            raise ValueError("Total amount mismatch")
        
        db.session.commit()
        
        # Process payment if needed
        if data['paymentMethod'] in ['card', 'mpesa']:
            payment_service = PaymentService()
            payment_result = payment_service.process_payment(order, data['paymentMethod'])
            
            if payment_result['success']:
                order.payment_status = 'paid'
                order.payment_reference = payment_result['reference']
            else:
                order.payment_status = 'failed'
            
            db.session.commit()
        
        return jsonify({
            'success': True,
            'data': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order by ID"""
    try:
        order = Order.query.get_or_404(order_id)
        return jsonify({
            'success': True,
            'data': order.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@order_bp.route('/orders/<order_number>', methods=['GET'])
def get_order_by_number(order_number):
    """Get order by order number"""
    try:
        order = Order.query.filter_by(order_number=order_number).first_or_404()
        return jsonify({
            'success': True,
            'data': order.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@order_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        
        valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']
        new_status = data.get('status')
        
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'error': 'Invalid status'
            }), 400
        
        order.status = new_status
        
        # Update estimated ready time if provided
        if 'estimated_ready_time' in data:
            order.estimated_ready_time = datetime.fromisoformat(data['estimated_ready_time'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': order.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@order_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get orders with optional filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        customer_email = request.args.get('customer_email')
        
        query = Order.query
        
        if status:
            query = query.filter_by(status=status)
        
        if customer_email:
            customer = Customer.query.filter_by(email=customer_email).first()
            if customer:
                query = query.filter_by(customer_id=customer.id)
        
        orders = query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [order.to_dict() for order in orders.items],
            'pagination': {
                'page': page,
                'pages': orders.pages,
                'per_page': per_page,
                'total': orders.total
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500