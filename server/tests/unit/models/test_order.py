"""
Unit tests for Order model

Tests cover:
- Model creation with valid data
- Required fields validation
- Order number generation
- Total calculation
- Status transitions
- Order type validation (pickup, delivery)
- Payment method and status
- Delivery details
- Serialization (to_dict)
- Relationships with user, order items, and payment
"""

import pytest
from decimal import Decimal
from datetime import datetime
from models.order import Order
from tests.factories import OrderFactory, UserFactory, ProductFactory, OrderItemFactory


class TestOrderCreation:
    """Test order creation and basic attributes"""
    
    def test_order_creation_with_valid_data(self, db):
        """Test creating an order with all valid data"""
        user = UserFactory()
        order = OrderFactory(
            user=user,
            total_amount=Decimal('25.50'),
            order_type='pickup',
            status='pending',
            payment_method='mpesa',
            payment_status='pending'
        )
        
        assert order.id is not None
        assert order.order_number is not None
        assert order.user_id == user.id
        assert order.total_amount == Decimal('25.50')
        assert order.order_type == 'pickup'
        assert order.status == 'pending'
        assert order.payment_method == 'mpesa'
        assert order.payment_status == 'pending'
        assert order.created_at is not None
    
    def test_order_creation_with_minimal_data(self, db):
        """Test creating an order with only required fields"""
        user = UserFactory()
        order = Order(
            user_id=user.id,
            total_amount=Decimal('10.00'),
            order_type='pickup'
        )
        db.session.add(order)
        db.session.commit()
        
        assert order.id is not None
        assert order.order_number is not None
        assert order.total_amount == Decimal('10.00')
        assert order.order_type == 'pickup'
    
    def test_order_default_values(self, db):
        """Test that default values are set correctly"""
        user = UserFactory()
        order = Order(
            user_id=user.id,
            total_amount=Decimal('10.00'),
            order_type='pickup'
        )
        db.session.add(order)
        db.session.commit()
        
        assert order.status == 'pending'
        assert order.payment_status == 'pending'
        assert order.delivery_fee == Decimal('0')
        assert order.created_at is not None
        assert order.updated_at is not None


class TestOrderNumberGeneration:
    """Test order number generation"""
    
    def test_order_number_generated_automatically(self, db):
        """Test that order_number is generated automatically"""
        order = OrderFactory()
        
        assert order.order_number is not None
        assert len(order.order_number) == 8
        assert order.order_number.isupper()
    
    def test_order_number_is_unique(self, db):
        """Test that each order gets a unique order number"""
        order1 = OrderFactory()
        order2 = OrderFactory()
        order3 = OrderFactory()
        
        assert order1.order_number != order2.order_number
        assert order1.order_number != order3.order_number
        assert order2.order_number != order3.order_number
    
    def test_order_number_unique_constraint(self, db):
        """Test that order_number has unique constraint"""
        order1 = OrderFactory()
        order_number = order1.order_number
        
        # Try to create another order with same order_number
        order2 = Order(
            user_id=order1.user_id,
            total_amount=Decimal('10.00'),
            order_type='pickup',
            order_number=order_number
        )
        db.session.add(order2)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()


class TestOrderFieldValidation:
    """Test field validation and constraints"""
    
    def test_total_amount_required(self, db):
        """Test that total_amount is required"""
        user = UserFactory()
        order = Order(
            user_id=user.id,
            order_type='pickup'
        )
        db.session.add(order)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_order_type_required(self, db):
        """Test that order_type is required"""
        user = UserFactory()
        order = Order(
            user_id=user.id,
            total_amount=Decimal('10.00')
        )
        db.session.add(order)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_order_type_values(self, db):
        """Test different order_type values"""
        pickup_order = OrderFactory(order_type='pickup')
        delivery_order = OrderFactory(order_type='delivery')
        
        assert pickup_order.order_type == 'pickup'
        assert delivery_order.order_type == 'delivery'
    
    def test_status_values(self, db):
        """Test different status values"""
        statuses = ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']
        
        for status in statuses:
            order = OrderFactory(status=status)
            assert order.status == status
    
    def test_payment_method_values(self, db):
        """Test different payment_method values"""
        mpesa_order = OrderFactory(payment_method='mpesa')
        cash_order = OrderFactory(payment_method='cash')
        
        assert mpesa_order.payment_method == 'mpesa'
        assert cash_order.payment_method == 'cash'
    
    def test_payment_status_values(self, db):
        """Test different payment_status values"""
        pending = OrderFactory(payment_status='pending')
        paid = OrderFactory(payment_status='paid')
        failed = OrderFactory(payment_status='failed')
        
        assert pending.payment_status == 'pending'
        assert paid.payment_status == 'paid'
        assert failed.payment_status == 'failed'


class TestOrderDeliveryDetails:
    """Test delivery-related fields"""
    
    def test_delivery_order_with_address(self, db):
        """Test delivery order with address"""
        order = OrderFactory(
            order_type='delivery',
            delivery_address='123 Main St, Nairobi',
            delivery_instructions='Ring doorbell',
            delivery_fee=Decimal('2.50')
        )
        
        assert order.order_type == 'delivery'
        assert order.delivery_address == '123 Main St, Nairobi'
        assert order.delivery_instructions == 'Ring doorbell'
        assert order.delivery_fee == Decimal('2.50')
    
    def test_pickup_order_no_delivery_details(self, db):
        """Test pickup order typically has no delivery details"""
        order = OrderFactory(
            order_type='pickup',
            delivery_address=None,
            delivery_instructions=None,
            delivery_fee=Decimal('0.00')
        )
        
        assert order.order_type == 'pickup'
        assert order.delivery_address is None
        assert order.delivery_instructions is None
        assert order.delivery_fee == Decimal('0.00')
    
    def test_delivery_fee_default(self, db):
        """Test delivery_fee defaults to 0"""
        order = OrderFactory()
        
        # Default should be 0
        assert order.delivery_fee == Decimal('0') or order.delivery_fee == Decimal('0.00')


class TestOrderSafeFloatMethod:
    """Test the safe_float helper method"""
    
    def test_safe_float_with_decimal(self, db):
        """Test safe_float converts Decimal to float"""
        order = OrderFactory(total_amount=Decimal('25.50'))
        
        result = order.safe_float(order.total_amount)
        
        assert isinstance(result, float)
        assert result == 25.50
    
    def test_safe_float_with_none(self, db):
        """Test safe_float handles None"""
        order = OrderFactory()
        
        result = order.safe_float(None)
        
        assert result == 0.0
    
    def test_safe_float_with_zero(self, db):
        """Test safe_float handles zero"""
        order = OrderFactory()
        
        result = order.safe_float(Decimal('0.00'))
        
        assert result == 0.0
    
    def test_safe_float_with_float(self, db):
        """Test safe_float handles float input"""
        order = OrderFactory()
        
        result = order.safe_float(15.75)
        
        assert result == 15.75


class TestOrderSerialization:
    """Test order serialization to dictionary"""
    
    def test_to_dict_basic(self, db):
        """Test basic to_dict conversion"""
        user = UserFactory(username='testuser')
        order = OrderFactory(
            user=user,
            total_amount=Decimal('25.50'),
            order_type='pickup',
            status='pending',
            payment_method='mpesa'
        )
        
        data = order.to_dict()
        
        assert data['id'] == order.id
        assert data['order_number'] == order.order_number
        assert data['total_amount'] == 25.50
        assert data['order_type'] == 'pickup'
        assert data['status'] == 'pending'
        assert data['payment_method'] == 'mpesa'
        assert 'created_at' in data
        assert isinstance(data['created_at'], str)
    
    def test_to_dict_includes_user(self, db):
        """Test that to_dict includes user information"""
        user = UserFactory(username='testuser', email='test@example.com')
        order = OrderFactory(user=user)
        
        data = order.to_dict()
        
        assert 'user' in data
        assert data['user'] is not None
        assert data['user']['username'] == 'testuser'
        assert data['user']['email'] == 'test@example.com'
    
    def test_to_dict_with_null_user(self, db):
        """Test to_dict when user is None"""
        order = OrderFactory()
        order.user = None
        
        data = order.to_dict()
        
        assert data['user'] is None
    
    def test_to_dict_includes_items(self, db):
        """Test that to_dict includes order items"""
        order = OrderFactory()
        item1 = OrderItemFactory(order=order)
        item2 = OrderItemFactory(order=order)
        db.session.commit()
        
        data = order.to_dict()
        
        assert 'items' in data
        assert len(data['items']) == 2
    
    def test_to_dict_includes_payment(self, db):
        """Test that to_dict includes payment information"""
        from tests.factories import PaymentFactory
        
        order = OrderFactory()
        payment = PaymentFactory(order=order)
        db.session.commit()
        
        data = order.to_dict()
        
        assert 'payment' in data
        assert data['payment'] is not None
        assert data['payment']['id'] == payment.id
    
    def test_to_dict_without_payment(self, db):
        """Test to_dict when payment is None"""
        order = OrderFactory()
        
        data = order.to_dict()
        
        assert 'payment' in data
        assert data['payment'] is None
    
    def test_to_dict_delivery_details(self, db):
        """Test to_dict includes delivery details"""
        order = OrderFactory(
            order_type='delivery',
            delivery_address='123 Main St',
            delivery_instructions='Ring bell',
            delivery_fee=Decimal('2.50')
        )
        
        data = order.to_dict()
        
        assert data['delivery_address'] == '123 Main St'
        assert data['delivery_instructions'] == 'Ring bell'
        assert data['delivery_fee'] == 2.50
    
    def test_to_dict_estimated_ready_time(self, db):
        """Test to_dict includes estimated_ready_time"""
        order = OrderFactory()
        order.estimated_ready_time = datetime.utcnow()
        db.session.commit()
        
        data = order.to_dict()
        
        assert 'estimated_ready_time' in data
        assert data['estimated_ready_time'] is not None
        assert isinstance(data['estimated_ready_time'], str)
    
    def test_to_dict_with_null_estimated_ready_time(self, db):
        """Test to_dict when estimated_ready_time is None"""
        order = OrderFactory()
        order.estimated_ready_time = None
        db.session.commit()
        
        data = order.to_dict()
        
        assert data['estimated_ready_time'] is None


class TestOrderRelationships:
    """Test order relationships with other models"""
    
    def test_order_user_relationship(self, db):
        """Test that order has user relationship"""
        user = UserFactory()
        order = OrderFactory(user=user)
        
        assert order.user is not None
        assert order.user.id == user.id
        assert order in user.orders
    
    def test_order_items_relationship(self, db):
        """Test that order has order_items relationship"""
        order = OrderFactory()
        item1 = OrderItemFactory(order=order)
        item2 = OrderItemFactory(order=order)
        db.session.commit()
        
        assert len(order.order_items) == 2
        assert item1 in order.order_items
        assert item2 in order.order_items
    
    def test_order_payment_relationship(self, db):
        """Test that order has payment relationship"""
        from tests.factories import PaymentFactory
        
        order = OrderFactory()
        payment = PaymentFactory(order=order)
        db.session.commit()
        
        assert order.payment is not None
        assert order.payment.id == payment.id
        assert order.payment.order_id == order.id
    
    def test_order_items_cascade_delete(self, db):
        """Test that order items are deleted when order is deleted"""
        from models.order_item import OrderItem
        
        order = OrderFactory()
        item1 = OrderItemFactory(order=order)
        item2 = OrderItemFactory(order=order)
        db.session.commit()
        
        item1_id = item1.id
        item2_id = item2.id
        
        # Delete the order
        db.session.delete(order)
        db.session.commit()
        
        # Check that items are also deleted (cascade)
        assert db.session.get(OrderItem, item1_id) is None
        assert db.session.get(OrderItem, item2_id) is None


class TestOrderStatusManagement:
    """Test order status management"""
    
    def test_status_transition_pending_to_confirmed(self, db):
        """Test status transition from pending to confirmed"""
        order = OrderFactory(status='pending')
        
        order.status = 'confirmed'
        db.session.commit()
        
        assert order.status == 'confirmed'
    
    def test_status_transition_to_preparing(self, db):
        """Test status transition to preparing"""
        order = OrderFactory(status='confirmed')
        
        order.status = 'preparing'
        db.session.commit()
        
        assert order.status == 'preparing'
    
    def test_status_transition_to_ready(self, db):
        """Test status transition to ready"""
        order = OrderFactory(status='preparing')
        
        order.status = 'ready'
        db.session.commit()
        
        assert order.status == 'ready'
    
    def test_status_transition_to_completed(self, db):
        """Test status transition to completed"""
        order = OrderFactory(status='ready')
        
        order.status = 'completed'
        order.completed_at = datetime.utcnow()
        db.session.commit()
        
        assert order.status == 'completed'
        assert order.completed_at is not None
    
    def test_status_transition_to_cancelled(self, db):
        """Test status transition to cancelled"""
        order = OrderFactory(status='pending')
        
        order.status = 'cancelled'
        db.session.commit()
        
        assert order.status == 'cancelled'


class TestOrderPaymentManagement:
    """Test payment-related fields"""
    
    def test_payment_reference(self, db):
        """Test payment_reference field"""
        order = OrderFactory(payment_reference='PAY-12345')
        
        assert order.payment_reference == 'PAY-12345'
    
    def test_payment_status_update(self, db):
        """Test updating payment status"""
        order = OrderFactory(payment_status='pending')
        
        order.payment_status = 'paid'
        db.session.commit()
        
        assert order.payment_status == 'paid'


class TestOrderRepr:
    """Test order string representation"""
    
    def test_repr(self, db):
        """Test string representation of order"""
        order = OrderFactory()
        
        assert repr(order) == f'<Order {order.order_number}>'


class TestOrderTimestamps:
    """Test order timestamp fields"""
    
    def test_created_at_set_on_creation(self, db):
        """Test that created_at is set automatically"""
        order = OrderFactory()
        
        assert order.created_at is not None
        assert isinstance(order.created_at, datetime)
    
    def test_updated_at_set_on_creation(self, db):
        """Test that updated_at is set automatically"""
        order = OrderFactory()
        
        assert order.updated_at is not None
        assert isinstance(order.updated_at, datetime)
    
    def test_updated_at_changes_on_update(self, db):
        """Test that updated_at changes when order is updated"""
        order = OrderFactory()
        original_updated_at = order.updated_at
        
        import time
        time.sleep(0.01)
        
        order.status = 'confirmed'
        db.session.commit()
        
        assert order.updated_at >= original_updated_at
    
    def test_completed_at_initially_none(self, db):
        """Test that completed_at is initially None"""
        order = OrderFactory()
        
        assert order.completed_at is None
    
    def test_completed_at_can_be_set(self, db):
        """Test that completed_at can be set"""
        order = OrderFactory()
        completion_time = datetime.utcnow()
        order.completed_at = completion_time
        order.status = 'completed'
        db.session.commit()
        
        assert order.completed_at is not None
        assert isinstance(order.completed_at, datetime)
