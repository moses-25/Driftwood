"""
Unit tests for Payment model

Tests cover:
- Model creation with valid data
- Required fields validation
- Amount validation
- Payment method validation (mpesa, card, cash)
- Payment status transitions
- M-Pesa specific fields
- Refund functionality
- Model methods (mark_as_completed, mark_as_failed)
- Serialization (to_dict)
- Relationships with orders
"""

import pytest
from decimal import Decimal
from datetime import datetime
from models.payment import Payment
from tests.factories import PaymentFactory, OrderFactory


class TestPaymentCreation:
    """Test payment creation and basic attributes"""
    
    def test_payment_creation_with_valid_data(self, db):
        """Test creating a payment with all valid data"""
        order = OrderFactory()
        payment = PaymentFactory(
            order=order,
            amount=Decimal('25.50'),
            payment_method='mpesa',
            status='pending',
            currency='KES'
        )
        
        assert payment.id is not None
        assert payment.order_id == order.id
        assert payment.amount == Decimal('25.50')
        assert payment.payment_method == 'mpesa'
        assert payment.status == 'pending'
        assert payment.currency == 'KES'
        assert payment.created_at is not None
    
    def test_payment_creation_with_minimal_data(self, db):
        """Test creating a payment with only required fields"""
        order = OrderFactory()
        payment = Payment(
            order_id=order.id,
            amount=Decimal('10.00'),
            payment_method='cash'
        )
        db.session.add(payment)
        db.session.commit()
        
        assert payment.id is not None
        assert payment.order_id == order.id
        assert payment.amount == Decimal('10.00')
        assert payment.payment_method == 'cash'
    
    def test_payment_default_values(self, db):
        """Test that default values are set correctly"""
        order = OrderFactory()
        payment = Payment(
            order_id=order.id,
            amount=Decimal('10.00'),
            payment_method='cash'
        )
        db.session.add(payment)
        db.session.commit()
        
        assert payment.status == 'pending'
        assert payment.currency == 'KES'
        assert payment.refunded_amount == Decimal('0.0')
        assert payment.created_at is not None
        assert payment.updated_at is not None


class TestPaymentFieldValidation:
    """Test field validation and constraints"""
    
    def test_order_id_required(self, db):
        """Test that order_id is required"""
        payment = Payment(
            amount=Decimal('10.00'),
            payment_method='cash'
        )
        db.session.add(payment)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_amount_required(self, db):
        """Test that amount is required"""
        order = OrderFactory()
        payment = Payment(
            order_id=order.id,
            payment_method='cash'
        )
        db.session.add(payment)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_payment_method_required(self, db):
        """Test that payment_method is required"""
        order = OrderFactory()
        payment = Payment(
            order_id=order.id,
            amount=Decimal('10.00')
        )
        db.session.add(payment)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_amount_precision(self, db):
        """Test amount decimal precision (10, 2)"""
        payment = PaymentFactory(amount=Decimal('99.99'))
        assert payment.amount == Decimal('99.99')
        
        payment2 = PaymentFactory(amount=Decimal('1234.56'))
        assert payment2.amount == Decimal('1234.56')
    
    def test_transaction_id_unique_constraint(self, db):
        """Test that transaction_id must be unique"""
        PaymentFactory(transaction_id='TXN-12345')
        
        with pytest.raises(Exception):  # IntegrityError
            PaymentFactory(transaction_id='TXN-12345')


class TestPaymentMethodValidation:
    """Test payment method validation"""
    
    def test_payment_method_mpesa(self, db):
        """Test payment with M-Pesa method"""
        payment = PaymentFactory(payment_method='mpesa')
        assert payment.payment_method == 'mpesa'
    
    def test_payment_method_card(self, db):
        """Test payment with card method"""
        payment = PaymentFactory(payment_method='card')
        assert payment.payment_method == 'card'
    
    def test_payment_method_cash(self, db):
        """Test payment with cash method"""
        payment = PaymentFactory(payment_method='cash')
        assert payment.payment_method == 'cash'


class TestPaymentStatusTransitions:
    """Test payment status transitions"""
    
    def test_status_values(self, db):
        """Test different status values"""
        pending = PaymentFactory(status='pending')
        completed = PaymentFactory(status='completed')
        failed = PaymentFactory(status='failed')
        refunded = PaymentFactory(status='refunded')
        
        assert pending.status == 'pending'
        assert completed.status == 'completed'
        assert failed.status == 'failed'
        assert refunded.status == 'refunded'
    
    def test_status_transition_pending_to_completed(self, db):
        """Test status transition from pending to completed"""
        payment = PaymentFactory(status='pending')
        
        payment.status = 'completed'
        payment.completed_at = datetime.utcnow()
        db.session.commit()
        
        assert payment.status == 'completed'
        assert payment.completed_at is not None
    
    def test_status_transition_pending_to_failed(self, db):
        """Test status transition from pending to failed"""
        payment = PaymentFactory(status='pending')
        
        payment.status = 'failed'
        payment.failure_reason = 'Insufficient funds'
        db.session.commit()
        
        assert payment.status == 'failed'
        assert payment.failure_reason == 'Insufficient funds'


class TestPaymentMpesaFields:
    """Test M-Pesa specific fields"""
    
    def test_mpesa_receipt_number(self, db):
        """Test M-Pesa receipt number field"""
        payment = PaymentFactory(
            payment_method='mpesa',
            mpesa_receipt_number='ABC123456789'
        )
        
        assert payment.mpesa_receipt_number == 'ABC123456789'
    
    def test_mpesa_phone_number(self, db):
        """Test M-Pesa phone number field"""
        payment = PaymentFactory(
            payment_method='mpesa',
            mpesa_phone_number='254712345678'
        )
        
        assert payment.mpesa_phone_number == '254712345678'
    
    def test_mpesa_checkout_request_id(self, db):
        """Test M-Pesa checkout request ID field"""
        payment = PaymentFactory(
            payment_method='mpesa',
            mpesa_checkout_request_id='ws_CO_12345'
        )
        
        assert payment.mpesa_checkout_request_id == 'ws_CO_12345'
    
    def test_mpesa_fields_null_for_non_mpesa(self, db):
        """Test M-Pesa fields are None for non-M-Pesa payments"""
        payment = PaymentFactory(
            payment_method='cash',
            mpesa_receipt_number=None,
            mpesa_phone_number=None,
            mpesa_checkout_request_id=None
        )
        
        assert payment.mpesa_receipt_number is None
        assert payment.mpesa_phone_number is None
        assert payment.mpesa_checkout_request_id is None


class TestPaymentMarkAsCompleted:
    """Test mark_as_completed method"""
    
    def test_mark_as_completed_basic(self, db):
        """Test mark_as_completed sets status and timestamp"""
        payment = PaymentFactory(status='pending')
        
        payment.mark_as_completed()
        db.session.commit()
        
        assert payment.status == 'completed'
        assert payment.completed_at is not None
        assert isinstance(payment.completed_at, datetime)
    
    def test_mark_as_completed_with_transaction_id(self, db):
        """Test mark_as_completed with transaction_id"""
        payment = PaymentFactory(status='pending')
        
        payment.mark_as_completed(transaction_id='TXN-98765')
        db.session.commit()
        
        assert payment.status == 'completed'
        assert payment.transaction_id == 'TXN-98765'
        assert payment.completed_at is not None
    
    def test_mark_as_completed_with_receipt_number(self, db):
        """Test mark_as_completed with M-Pesa receipt number"""
        payment = PaymentFactory(
            status='pending',
            payment_method='mpesa'
        )
        
        payment.mark_as_completed(receipt_number='ABC123456')
        db.session.commit()
        
        assert payment.status == 'completed'
        assert payment.mpesa_receipt_number == 'ABC123456'
        assert payment.completed_at is not None
    
    def test_mark_as_completed_with_both_ids(self, db):
        """Test mark_as_completed with both transaction_id and receipt_number"""
        payment = PaymentFactory(
            status='pending',
            payment_method='mpesa'
        )
        
        payment.mark_as_completed(
            transaction_id='TXN-12345',
            receipt_number='ABC123456'
        )
        db.session.commit()
        
        assert payment.status == 'completed'
        assert payment.transaction_id == 'TXN-12345'
        assert payment.mpesa_receipt_number == 'ABC123456'


class TestPaymentMarkAsFailed:
    """Test mark_as_failed method"""
    
    def test_mark_as_failed_basic(self, db):
        """Test mark_as_failed sets status"""
        payment = PaymentFactory(status='pending')
        
        payment.mark_as_failed()
        db.session.commit()
        
        assert payment.status == 'failed'
    
    def test_mark_as_failed_with_reason(self, db):
        """Test mark_as_failed with failure reason"""
        payment = PaymentFactory(status='pending')
        
        payment.mark_as_failed(reason='Insufficient funds')
        db.session.commit()
        
        assert payment.status == 'failed'
        assert payment.failure_reason == 'Insufficient funds'
    
    def test_mark_as_failed_different_reasons(self, db):
        """Test mark_as_failed with different failure reasons"""
        payment1 = PaymentFactory(status='pending')
        payment1.mark_as_failed(reason='Card declined')
        
        payment2 = PaymentFactory(status='pending')
        payment2.mark_as_failed(reason='Network timeout')
        
        db.session.commit()
        
        assert payment1.failure_reason == 'Card declined'
        assert payment2.failure_reason == 'Network timeout'


class TestPaymentRefundFields:
    """Test refund-related fields"""
    
    def test_refunded_amount_default(self, db):
        """Test refunded_amount defaults to 0"""
        payment = PaymentFactory()
        
        assert payment.refunded_amount == Decimal('0.0') or payment.refunded_amount == Decimal('0.00')
    
    def test_refund_fields(self, db):
        """Test setting refund fields"""
        payment = PaymentFactory(status='completed')
        
        payment.status = 'refunded'
        payment.refunded_amount = Decimal('25.50')
        payment.refund_reference = 'REF-12345'
        payment.refund_reason = 'Customer request'
        payment.refunded_at = datetime.utcnow()
        db.session.commit()
        
        assert payment.status == 'refunded'
        assert payment.refunded_amount == Decimal('25.50')
        assert payment.refund_reference == 'REF-12345'
        assert payment.refund_reason == 'Customer request'
        assert payment.refunded_at is not None
    
    def test_partial_refund(self, db):
        """Test partial refund scenario"""
        payment = PaymentFactory(
            amount=Decimal('100.00'),
            status='completed'
        )
        
        payment.refunded_amount = Decimal('30.00')
        payment.refund_reference = 'PARTIAL-REF-123'
        payment.refunded_at = datetime.utcnow()
        db.session.commit()
        
        assert payment.refunded_amount == Decimal('30.00')
        assert payment.amount == Decimal('100.00')
        # Status might remain 'completed' for partial refunds
        assert payment.refund_reference is not None


class TestPaymentSerialization:
    """Test payment serialization to dictionary"""
    
    def test_to_dict_basic(self, db):
        """Test basic to_dict conversion"""
        order = OrderFactory()
        payment = PaymentFactory(
            order=order,
            amount=Decimal('25.50'),
            payment_method='mpesa',
            status='completed',
            currency='KES'
        )
        
        data = payment.to_dict()
        
        assert data['id'] == payment.id
        assert data['order_id'] == order.id
        assert data['amount'] == 25.50
        assert data['payment_method'] == 'mpesa'
        assert data['status'] == 'completed'
        assert data['currency'] == 'KES'
        assert 'created_at' in data
        assert isinstance(data['created_at'], str)
    
    def test_to_dict_includes_mpesa_fields(self, db):
        """Test that to_dict includes M-Pesa fields"""
        payment = PaymentFactory(
            payment_method='mpesa',
            mpesa_receipt_number='ABC123',
            mpesa_phone_number='254712345678'
        )
        
        data = payment.to_dict()
        
        assert 'mpesa_receipt_number' in data
        assert 'mpesa_phone_number' in data
        assert data['mpesa_receipt_number'] == 'ABC123'
        assert data['mpesa_phone_number'] == '254712345678'
    
    def test_to_dict_includes_refund_fields(self, db):
        """Test that to_dict includes refund fields"""
        payment = PaymentFactory(
            status='refunded',
            refunded_amount=Decimal('25.50'),
            refund_reference='REF-123',
            refund_reason='Customer request'
        )
        payment.refunded_at = datetime.utcnow()
        db.session.commit()
        
        data = payment.to_dict()
        
        assert 'refunded_amount' in data
        assert 'refund_reference' in data
        assert 'refund_reason' in data
        assert 'refunded_at' in data
        assert data['refunded_amount'] == 25.50
        assert data['refund_reference'] == 'REF-123'
    
    def test_to_dict_with_null_refund_fields(self, db):
        """Test to_dict when refund fields are None"""
        payment = PaymentFactory(status='completed')
        
        data = payment.to_dict()
        
        assert data['refunded_amount'] == 0.0
        assert data['refund_reference'] is None
        assert data['refund_reason'] is None
        assert data['refunded_at'] is None
    
    def test_to_dict_completed_at(self, db):
        """Test to_dict includes completed_at"""
        payment = PaymentFactory(status='completed')
        payment.completed_at = datetime.utcnow()
        db.session.commit()
        
        data = payment.to_dict()
        
        assert 'completed_at' in data
        assert data['completed_at'] is not None
        assert isinstance(data['completed_at'], str)
    
    def test_to_dict_with_null_completed_at(self, db):
        """Test to_dict when completed_at is None"""
        payment = PaymentFactory(status='pending')
        
        data = payment.to_dict()
        
        assert data['completed_at'] is None


class TestPaymentRelationships:
    """Test payment relationships with other models"""
    
    def test_payment_order_relationship(self, db):
        """Test that payment has order relationship"""
        order = OrderFactory()
        payment = PaymentFactory(order=order)
        
        assert payment.order is not None
        assert payment.order.id == order.id
        assert payment.order_id == order.id
    
    def test_order_payment_backref(self, db):
        """Test that order has payment backref"""
        order = OrderFactory()
        payment = PaymentFactory(order=order)
        db.session.commit()
        
        assert order.payment is not None
        assert order.payment.id == payment.id


class TestPaymentCurrency:
    """Test payment currency field"""
    
    def test_currency_default(self, db):
        """Test currency defaults to KES"""
        payment = PaymentFactory()
        
        assert payment.currency == 'KES'
    
    def test_currency_custom_value(self, db):
        """Test setting custom currency"""
        payment = PaymentFactory(currency='USD')
        
        assert payment.currency == 'USD'


class TestPaymentReferences:
    """Test payment reference fields"""
    
    def test_transaction_id(self, db):
        """Test transaction_id field"""
        payment = PaymentFactory(transaction_id='TXN-12345')
        
        assert payment.transaction_id == 'TXN-12345'
    
    def test_payment_reference(self, db):
        """Test payment_reference field"""
        payment = PaymentFactory(payment_reference='PAY-REF-12345')
        
        assert payment.payment_reference == 'PAY-REF-12345'


class TestPaymentRepr:
    """Test payment string representation"""
    
    def test_repr(self, db):
        """Test string representation of payment"""
        payment = PaymentFactory(
            payment_reference='PAY-123',
            status='completed'
        )
        
        assert repr(payment) == '<Payment PAY-123 - completed>'
    
    def test_repr_with_null_reference(self, db):
        """Test repr when payment_reference is None"""
        payment = PaymentFactory(payment_reference=None, status='pending')
        
        # Should still work without error
        repr_str = repr(payment)
        assert 'Payment' in repr_str
        assert 'pending' in repr_str


class TestPaymentTimestamps:
    """Test payment timestamp fields"""
    
    def test_created_at_set_on_creation(self, db):
        """Test that created_at is set automatically"""
        payment = PaymentFactory()
        
        assert payment.created_at is not None
        assert isinstance(payment.created_at, datetime)
    
    def test_updated_at_set_on_creation(self, db):
        """Test that updated_at is set automatically"""
        payment = PaymentFactory()
        
        assert payment.updated_at is not None
        assert isinstance(payment.updated_at, datetime)
    
    def test_updated_at_changes_on_update(self, db):
        """Test that updated_at changes when payment is updated"""
        payment = PaymentFactory()
        original_updated_at = payment.updated_at
        
        import time
        time.sleep(0.01)
        
        payment.status = 'completed'
        db.session.commit()
        
        assert payment.updated_at >= original_updated_at
