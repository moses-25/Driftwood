from flask import Blueprint, jsonify, request
from models.customer import Customer
from extensions import db

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers', methods=['POST'])
def create_or_update_customer():
    """Create or update customer information"""
    try:
        data = request.get_json()
        
        customer = Customer.query.filter_by(email=data['email']).first()
        
        if customer:
            # Update existing customer
            customer.name = data.get('name', customer.name)
            customer.phone = data.get('phone', customer.phone)
            customer.address = data.get('address', customer.address)
        else:
            # Create new customer
            customer = Customer(
                name=data['name'],
                email=data['email'],
                phone=data.get('phone'),
                address=data.get('address')
            )
            db.session.add(customer)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': customer.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@customer_bp.route('/customers/<email>', methods=['GET'])
def get_customer_by_email(email):
    """Get customer by email"""
    try:
        customer = Customer.query.filter_by(email=email).first_or_404()
        return jsonify({
            'success': True,
            'data': customer.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@customer_bp.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    """Get all orders for a customer"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        orders = [order.to_dict() for order in customer.orders]
        
        return jsonify({
            'success': True,
            'data': {
                'customer': customer.to_dict(),
                'orders': orders
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500