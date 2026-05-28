"""
Unit tests for OrderStatusHistory model

Tests cover:
- Model creation with valid data
- Required fields validation
- Status tracking
- Order relationship
- User (changed_by) relationship
- Notes field
- Serialization (to_dict)
- Timestamp tracking
"""

import pytest
from models.order_status_history import OrderStatusHistory
from tests.factories import OrderStatusHistoryFactory, OrderFactory, UserFactory


class TestOrderStatusHistoryCreation:
    """Test order status history creation and basic attributes"""
    
    def test_order_status_history_creation_with_valid_data(self, db):
        """Test creating an order status history with all valid data"""
        order = OrderFactory()
        user = UserFactory(role='staff')
        history = OrderStatusHistoryFactory(
            order=order,
            status='confirmed',
            notes='Order confirmed by customer',
            changed_by=user
        )
        
        assert history.id is not None
        assert history.order_id == order.id
        assert history.status == 'confirmed'
        assert history.notes == 'Order confirmed by customer'
        assert history.changed_by == user.id
        assert history.created_at is not None
    
    def test_order_status_history_creation_with_minimal_data(self, db):
        """Test creating an order status history with only required fields"""
        order = OrderFactory()
        history = OrderStatusHistory(
            order_id=order.id,
            status='preparing'
        )
        db.session.add(history)
        db.session.commit()
        
        assert history.id is not None
        assert history.order_id == order.id
        assert history.status == 'preparing'
    
    def test_order_status_history_default_values(self, db):
        """Test that default values are set correctly"""
        order = OrderFactory()
        history = OrderStatusHistory(
            order_id=order.id,
            status='ready'
        )
        db.session.add(history)
        db.session.commit()
        
        assert history.created_at is not None
        assert history.notes is None
        assert history.changed_by is None


class TestOrderStatusHistoryFieldValidation:
    """Test field validation and constraints"""
    
    def test_order_id_required(self, db):
        """Test that order_id is required"""
        history = OrderStatusHistory(status='confirmed')
        db.session.add(history)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_status_required(self, db):
        """Test that status is required"""
        order = OrderFactory()
        history = OrderStatusHistory(order_id=order.id)
        db.session.add(history)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_notes_optional(self, db):
        """Test that notes is optional"""
        order = OrderFactory()
        history = OrderStatusHistoryFactory(
            order=order,
            status='confirmed',
            notes=None
        )
        
        assert history.notes is None
    
    def test_changed_by_optional(self, db):
        """Test that changed_by is optional"""
        order = OrderFactory()
        history = OrderStatusHistoryFactory(
            order=order,
            status='confirmed',
            changed_by=None
        )
        
        assert history.changed_by is None


class TestOrderStatusHistoryStatusValues:
    """Test different status values"""
    
    def test_status_values(self, db):
        """Test different status values"""
        order = OrderFactory()
        statuses = ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']
        
        for status in statuses:
            history = OrderStatusHistoryFactory(order=order, status=status)
            assert history.status == status
    
    def test_status_pending(self, db):
        """Test pending status"""
        history = OrderStatusHistoryFactory(status='pending')
        assert history.status == 'pending'
    
    def test_status_confirmed(self, db):
        """Test confirmed status"""
        history = OrderStatusHistoryFactory(status='confirmed')
        assert history.status == 'confirmed'
    
    def test_status_preparing(self, db):
        """Test preparing status"""
        history = OrderStatusHistoryFactory(status='preparing')
        assert history.status == 'preparing'
    
    def test_status_ready(self, db):
        """Test ready status"""
        history = OrderStatusHistoryFactory(status='ready')
        assert history.status == 'ready'
    
    def test_status_completed(self, db):
        """Test completed status"""
        history = OrderStatusHistoryFactory(status='completed')
        assert history.status == 'completed'
    
    def test_status_cancelled(self, db):
        """Test cancelled status"""
        history = OrderStatusHistoryFactory(status='cancelled')
        assert history.status == 'cancelled'


class TestOrderStatusHistoryNotes:
    """Test notes field"""
    
    def test_notes_with_text(self, db):
        """Test notes with text content"""
        history = OrderStatusHistoryFactory(
            notes='Customer called to confirm order'
        )
        
        assert history.notes == 'Customer called to confirm order'
    
    def test_notes_can_be_null(self, db):
        """Test that notes can be None"""
        history = OrderStatusHistoryFactory(notes=None)
        
        assert history.notes is None
    
    def test_notes_can_be_long(self, db):
        """Test that notes can be long text"""
        long_notes = 'A' * 500
        history = OrderStatusHistoryFactory(notes=long_notes)
        
        assert len(history.notes) == 500
    
    def test_notes_can_be_empty_string(self, db):
        """Test that notes can be empty string"""
        history = OrderStatusHistoryFactory(notes='')
        
        assert history.notes == ''
    
    def test_notes_with_special_characters(self, db):
        """Test notes with special characters"""
        history = OrderStatusHistoryFactory(
            notes='Order #12345 - Customer requested extra foam ☕'
        )
        
        assert '#12345' in history.notes
        assert '☕' in history.notes


class TestOrderStatusHistorySerialization:
    """Test order status history serialization to dictionary"""
    
    def test_to_dict_basic(self, db):
        """Test basic to_dict conversion"""
        order = OrderFactory()
        user = UserFactory(username='staff_member')
        history = OrderStatusHistoryFactory(
            order=order,
            status='confirmed',
            notes='Order confirmed',
            changed_by=user
        )
        
        data = history.to_dict()
        
        assert data['id'] == history.id
        assert data['order_id'] == order.id
        assert data['status'] == 'confirmed'
        assert data['notes'] == 'Order confirmed'
        assert data['changed_by'] == 'staff_member'
        assert 'created_at' in data
        assert isinstance(data['created_at'], str)
    
    def test_to_dict_with_null_user(self, db):
        """Test to_dict when changed_by is None"""
        history = OrderStatusHistoryFactory(changed_by=None)
        
        data = history.to_dict()
        
        assert data['changed_by'] == 'System'
    
    def test_to_dict_with_null_notes(self, db):
        """Test to_dict when notes is None"""
        history = OrderStatusHistoryFactory(notes=None)
        
        data = history.to_dict()
        
        assert data['notes'] is None
    
    def test_to_dict_system_change(self, db):
        """Test to_dict for system-initiated change"""
        history = OrderStatusHistoryFactory(
            status='cancelled',
            notes='Auto-cancelled due to payment timeout',
            changed_by=None
        )
        
        data = history.to_dict()
        
        assert data['status'] == 'cancelled'
        assert data['changed_by'] == 'System'
        assert 'payment timeout' in data['notes']


class TestOrderStatusHistoryRelationships:
    """Test order status history relationships with other models"""
    
    def test_order_status_history_order_relationship(self, db):
        """Test that order status history has order relationship"""
        order = OrderFactory(order_number='TEST123')
        history = OrderStatusHistoryFactory(order=order)
        
        assert history.order is not None
        assert history.order.order_number == 'TEST123'
        assert history.order_id == order.id
    
    def test_order_status_history_user_relationship(self, db):
        """Test that order status history has user relationship"""
        user = UserFactory(username='staff_user')
        history = OrderStatusHistoryFactory(changed_by=user)
        
        assert history.user is not None
        assert history.user.username == 'staff_user'
        assert history.changed_by == user.id
    
    def test_order_status_history_backref(self, db):
        """Test that order has status_history backref"""
        order = OrderFactory()
        history1 = OrderStatusHistoryFactory(order=order, status='pending')
        history2 = OrderStatusHistoryFactory(order=order, status='confirmed')
        history3 = OrderStatusHistoryFactory(order=order, status='preparing')
        db.session.commit()
        
        assert len(order.status_history) == 3
        assert history1 in order.status_history
        assert history2 in order.status_history
        assert history3 in order.status_history
    
    def test_user_order_status_changes_backref(self, db):
        """Test that user has order_status_changes backref"""
        user = UserFactory()
        history1 = OrderStatusHistoryFactory(changed_by=user)
        history2 = OrderStatusHistoryFactory(changed_by=user)
        db.session.commit()
        
        assert len(user.order_status_changes) == 2
        assert history1 in user.order_status_changes
        assert history2 in user.order_status_changes


class TestOrderStatusHistoryRepr:
    """Test order status history string representation"""
    
    def test_repr(self, db):
        """Test string representation of order status history"""
        order = OrderFactory()
        history = OrderStatusHistoryFactory(
            order=order,
            status='confirmed'
        )
        
        assert repr(history) == f'<OrderStatusHistory Order#{order.id} -> confirmed>'
    
    def test_repr_different_statuses(self, db):
        """Test repr with different statuses"""
        order = OrderFactory()
        
        for status in ['pending', 'confirmed', 'preparing', 'ready', 'completed']:
            history = OrderStatusHistoryFactory(order=order, status=status)
            assert f'-> {status}' in repr(history)


class TestOrderStatusHistoryTimestamp:
    """Test order status history timestamp"""
    
    def test_created_at_set_on_creation(self, db):
        """Test that created_at is set automatically"""
        history = OrderStatusHistoryFactory()
        
        assert history.created_at is not None
    
    def test_created_at_immutable(self, db):
        """Test that created_at doesn't change on update"""
        history = OrderStatusHistoryFactory()
        original_created_at = history.created_at
        
        import time
        time.sleep(0.01)
        
        history.notes = 'Updated notes'
        db.session.commit()
        
        # created_at should not change
        assert history.created_at == original_created_at
    
    def test_created_at_chronological_order(self, db):
        """Test that multiple history entries have chronological timestamps"""
        order = OrderFactory()
        
        history1 = OrderStatusHistoryFactory(order=order, status='pending')
        db.session.commit()
        
        import time
        time.sleep(0.01)
        
        history2 = OrderStatusHistoryFactory(order=order, status='confirmed')
        db.session.commit()
        
        time.sleep(0.01)
        
        history3 = OrderStatusHistoryFactory(order=order, status='preparing')
        db.session.commit()
        
        assert history1.created_at <= history2.created_at
        assert history2.created_at <= history3.created_at


class TestOrderStatusHistoryScenarios:
    """Test real-world order status tracking scenarios"""
    
    def test_complete_order_lifecycle(self, db):
        """Test tracking complete order lifecycle"""
        order = OrderFactory()
        staff = UserFactory(role='staff')
        
        # Order created (pending)
        h1 = OrderStatusHistoryFactory(
            order=order,
            status='pending',
            notes='Order placed',
            changed_by=None  # System
        )
        
        # Order confirmed
        h2 = OrderStatusHistoryFactory(
            order=order,
            status='confirmed',
            notes='Payment received',
            changed_by=staff
        )
        
        # Order preparing
        h3 = OrderStatusHistoryFactory(
            order=order,
            status='preparing',
            notes='Started preparation',
            changed_by=staff
        )
        
        # Order ready
        h4 = OrderStatusHistoryFactory(
            order=order,
            status='ready',
            notes='Ready for pickup',
            changed_by=staff
        )
        
        # Order completed
        h5 = OrderStatusHistoryFactory(
            order=order,
            status='completed',
            notes='Order picked up by customer',
            changed_by=staff
        )
        
        db.session.commit()
        
        assert len(order.status_history) == 5
        assert order.status_history[0].status == 'pending'
        assert order.status_history[-1].status == 'completed'
    
    def test_order_cancellation(self, db):
        """Test order cancellation scenario"""
        order = OrderFactory()
        user = UserFactory()
        
        h1 = OrderStatusHistoryFactory(
            order=order,
            status='pending',
            changed_by=None
        )
        
        h2 = OrderStatusHistoryFactory(
            order=order,
            status='cancelled',
            notes='Customer requested cancellation',
            changed_by=user
        )
        
        db.session.commit()
        
        assert len(order.status_history) == 2
        assert order.status_history[-1].status == 'cancelled'
    
    def test_system_initiated_status_change(self, db):
        """Test system-initiated status change"""
        order = OrderFactory()
        
        history = OrderStatusHistoryFactory(
            order=order,
            status='cancelled',
            notes='Auto-cancelled: Payment not received within 30 minutes',
            changed_by=None
        )
        
        assert history.changed_by is None
        
        data = history.to_dict()
        assert data['changed_by'] == 'System'
    
    def test_multiple_orders_status_tracking(self, db):
        """Test tracking status for multiple orders"""
        order1 = OrderFactory()
        order2 = OrderFactory()
        staff = UserFactory(role='staff')
        
        # Order 1 history
        OrderStatusHistoryFactory(order=order1, status='pending')
        OrderStatusHistoryFactory(order=order1, status='confirmed', changed_by=staff)
        
        # Order 2 history
        OrderStatusHistoryFactory(order=order2, status='pending')
        OrderStatusHistoryFactory(order=order2, status='confirmed', changed_by=staff)
        OrderStatusHistoryFactory(order=order2, status='preparing', changed_by=staff)
        
        db.session.commit()
        
        assert len(order1.status_history) == 2
        assert len(order2.status_history) == 3
        assert len(staff.order_status_changes) == 4


class TestOrderStatusHistoryEdgeCases:
    """Test edge cases and special scenarios"""
    
    def test_status_change_without_notes(self, db):
        """Test status change without notes"""
        history = OrderStatusHistoryFactory(
            status='confirmed',
            notes=None
        )
        
        assert history.status == 'confirmed'
        assert history.notes is None
    
    def test_same_status_multiple_times(self, db):
        """Test recording same status multiple times (edge case)"""
        order = OrderFactory()
        
        h1 = OrderStatusHistoryFactory(order=order, status='preparing')
        h2 = OrderStatusHistoryFactory(order=order, status='preparing')
        
        db.session.commit()
        
        # Both should be recorded (might happen in edge cases)
        assert len(order.status_history) == 2
        assert h1.status == h2.status == 'preparing'
    
    def test_notes_with_html_content(self, db):
        """Test notes with HTML-like content"""
        history = OrderStatusHistoryFactory(
            notes='<b>Important:</b> Customer allergic to nuts'
        )
        
        # Notes should be stored as-is (sanitization at application layer)
        assert '<b>' in history.notes
    
    def test_very_long_notes(self, db):
        """Test very long notes"""
        long_notes = 'A' * 1000
        history = OrderStatusHistoryFactory(notes=long_notes)
        
        assert len(history.notes) == 1000
