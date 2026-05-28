"""
Unit tests for NotificationPreference model

Tests cover:
- Model creation with valid data
- Required fields validation
- User relationship
- Unique constraint (one preference per user)
- Boolean preference fields
- Default values
- Serialization (to_dict)
- Email, SMS, and other notification preferences
"""

import pytest
from models.notification_preference import NotificationPreference
from tests.factories import NotificationPreferenceFactory, UserFactory


class TestNotificationPreferenceCreation:
    """Test notification preference creation and basic attributes"""
    
    def test_notification_preference_creation_with_valid_data(self, db):
        """Test creating a notification preference with all valid data"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(
            user=user,
            email_enabled=True,
            sms_enabled=False,
            order_status_updates=True,
            promotional_emails=True,
            low_stock_alerts=False
        )
        
        assert pref.id is not None
        assert pref.user_id == user.id
        assert pref.email_enabled is True
        assert pref.sms_enabled is False
        assert pref.order_status_updates is True
        assert pref.promotional_emails is True
        assert pref.low_stock_alerts is False
    
    def test_notification_preference_creation_with_minimal_data(self, db):
        """Test creating a notification preference with only required fields"""
        user = UserFactory()
        pref = NotificationPreference(user_id=user.id)
        db.session.add(pref)
        db.session.commit()
        
        assert pref.id is not None
        assert pref.user_id == user.id
    
    def test_notification_preference_default_values(self, db):
        """Test that default values are set correctly"""
        user = UserFactory()
        pref = NotificationPreference(user_id=user.id)
        db.session.add(pref)
        db.session.commit()
        
        assert pref.email_enabled is True
        assert pref.sms_enabled is False
        assert pref.order_status_updates is True
        assert pref.promotional_emails is True
        assert pref.low_stock_alerts is True


class TestNotificationPreferenceFieldValidation:
    """Test field validation and constraints"""
    
    def test_user_id_required(self, db):
        """Test that user_id is required"""
        pref = NotificationPreference()
        db.session.add(pref)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_user_id_unique_constraint(self, db):
        """Test that user_id must be unique (one preference per user)"""
        user = UserFactory()
        NotificationPreferenceFactory(user=user)
        
        # Try to create another preference for the same user
        with pytest.raises(Exception):  # IntegrityError
            NotificationPreferenceFactory(user=user)
    
    def test_different_users_can_have_preferences(self, db):
        """Test that different users can have their own preferences"""
        user1 = UserFactory()
        user2 = UserFactory()
        
        pref1 = NotificationPreferenceFactory(user=user1)
        pref2 = NotificationPreferenceFactory(user=user2)
        
        assert pref1.id != pref2.id
        assert pref1.user_id != pref2.user_id


class TestNotificationPreferenceEmailSettings:
    """Test email notification settings"""
    
    def test_email_enabled_true(self, db):
        """Test email_enabled set to True"""
        pref = NotificationPreferenceFactory(email_enabled=True)
        
        assert pref.email_enabled is True
    
    def test_email_enabled_false(self, db):
        """Test email_enabled set to False"""
        pref = NotificationPreferenceFactory(email_enabled=False)
        
        assert pref.email_enabled is False
    
    def test_email_enabled_default(self, db):
        """Test email_enabled defaults to True"""
        user = UserFactory()
        pref = NotificationPreference(user_id=user.id)
        db.session.add(pref)
        db.session.commit()
        
        assert pref.email_enabled is True
    
    def test_toggle_email_enabled(self, db):
        """Test toggling email_enabled"""
        pref = NotificationPreferenceFactory(email_enabled=True)
        
        pref.email_enabled = False
        db.session.commit()
        
        assert pref.email_enabled is False
        
        pref.email_enabled = True
        db.session.commit()
        
        assert pref.email_enabled is True


class TestNotificationPreferenceSmsSettings:
    """Test SMS notification settings"""
    
    def test_sms_enabled_true(self, db):
        """Test sms_enabled set to True"""
        pref = NotificationPreferenceFactory(sms_enabled=True)
        
        assert pref.sms_enabled is True
    
    def test_sms_enabled_false(self, db):
        """Test sms_enabled set to False"""
        pref = NotificationPreferenceFactory(sms_enabled=False)
        
        assert pref.sms_enabled is False
    
    def test_sms_enabled_default(self, db):
        """Test sms_enabled defaults to False"""
        user = UserFactory()
        pref = NotificationPreference(user_id=user.id)
        db.session.add(pref)
        db.session.commit()
        
        assert pref.sms_enabled is False
    
    def test_toggle_sms_enabled(self, db):
        """Test toggling sms_enabled"""
        pref = NotificationPreferenceFactory(sms_enabled=False)
        
        pref.sms_enabled = True
        db.session.commit()
        
        assert pref.sms_enabled is True


class TestNotificationPreferenceOrderStatusUpdates:
    """Test order status update notifications"""
    
    def test_order_status_updates_true(self, db):
        """Test order_status_updates set to True"""
        pref = NotificationPreferenceFactory(order_status_updates=True)
        
        assert pref.order_status_updates is True
    
    def test_order_status_updates_false(self, db):
        """Test order_status_updates set to False"""
        pref = NotificationPreferenceFactory(order_status_updates=False)
        
        assert pref.order_status_updates is False
    
    def test_order_status_updates_default(self, db):
        """Test order_status_updates defaults to True"""
        user = UserFactory()
        pref = NotificationPreference(user_id=user.id)
        db.session.add(pref)
        db.session.commit()
        
        assert pref.order_status_updates is True


class TestNotificationPreferencePromotionalEmails:
    """Test promotional email settings"""
    
    def test_promotional_emails_true(self, db):
        """Test promotional_emails set to True"""
        pref = NotificationPreferenceFactory(promotional_emails=True)
        
        assert pref.promotional_emails is True
    
    def test_promotional_emails_false(self, db):
        """Test promotional_emails set to False"""
        pref = NotificationPreferenceFactory(promotional_emails=False)
        
        assert pref.promotional_emails is False
    
    def test_promotional_emails_default(self, db):
        """Test promotional_emails defaults to True"""
        user = UserFactory()
        pref = NotificationPreference(user_id=user.id)
        db.session.add(pref)
        db.session.commit()
        
        assert pref.promotional_emails is True
    
    def test_opt_out_promotional_emails(self, db):
        """Test opting out of promotional emails"""
        pref = NotificationPreferenceFactory(promotional_emails=True)
        
        pref.promotional_emails = False
        db.session.commit()
        
        assert pref.promotional_emails is False


class TestNotificationPreferenceLowStockAlerts:
    """Test low stock alert settings (for staff/admin)"""
    
    def test_low_stock_alerts_true(self, db):
        """Test low_stock_alerts set to True"""
        pref = NotificationPreferenceFactory(low_stock_alerts=True)
        
        assert pref.low_stock_alerts is True
    
    def test_low_stock_alerts_false(self, db):
        """Test low_stock_alerts set to False"""
        pref = NotificationPreferenceFactory(low_stock_alerts=False)
        
        assert pref.low_stock_alerts is False
    
    def test_low_stock_alerts_default(self, db):
        """Test low_stock_alerts defaults to True"""
        user = UserFactory()
        pref = NotificationPreference(user_id=user.id)
        db.session.add(pref)
        db.session.commit()
        
        assert pref.low_stock_alerts is True
    
    def test_low_stock_alerts_for_staff(self, db):
        """Test low stock alerts for staff user"""
        staff = UserFactory(role='staff')
        pref = NotificationPreferenceFactory(
            user=staff,
            low_stock_alerts=True
        )
        
        assert pref.low_stock_alerts is True
        assert pref.user.role == 'staff'


class TestNotificationPreferenceSerialization:
    """Test notification preference serialization to dictionary"""
    
    def test_to_dict_basic(self, db):
        """Test basic to_dict conversion"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(
            user=user,
            email_enabled=True,
            sms_enabled=False,
            order_status_updates=True,
            promotional_emails=False,
            low_stock_alerts=True
        )
        
        data = pref.to_dict()
        
        assert data['id'] == pref.id
        assert data['user_id'] == user.id
        assert data['email_enabled'] is True
        assert data['sms_enabled'] is False
        assert data['order_status_updates'] is True
        assert data['promotional_emails'] is False
        assert data['low_stock_alerts'] is True
    
    def test_to_dict_all_enabled(self, db):
        """Test to_dict with all notifications enabled"""
        pref = NotificationPreferenceFactory(
            email_enabled=True,
            sms_enabled=True,
            order_status_updates=True,
            promotional_emails=True,
            low_stock_alerts=True
        )
        
        data = pref.to_dict()
        
        assert all([
            data['email_enabled'],
            data['sms_enabled'],
            data['order_status_updates'],
            data['promotional_emails'],
            data['low_stock_alerts']
        ])
    
    def test_to_dict_all_disabled(self, db):
        """Test to_dict with all notifications disabled"""
        pref = NotificationPreferenceFactory(
            email_enabled=False,
            sms_enabled=False,
            order_status_updates=False,
            promotional_emails=False,
            low_stock_alerts=False
        )
        
        data = pref.to_dict()
        
        assert not any([
            data['email_enabled'],
            data['sms_enabled'],
            data['order_status_updates'],
            data['promotional_emails'],
            data['low_stock_alerts']
        ])


class TestNotificationPreferenceRelationships:
    """Test notification preference relationships with other models"""
    
    def test_notification_preference_user_relationship(self, db):
        """Test that notification preference has user relationship"""
        user = UserFactory(username='testuser')
        pref = NotificationPreferenceFactory(user=user)
        
        assert pref.user is not None
        assert pref.user.username == 'testuser'
        assert pref.user_id == user.id
    
    def test_user_notification_preferences_backref(self, db):
        """Test that user has notification_preferences backref"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(user=user)
        db.session.commit()
        
        assert user.notification_preferences is not None
        assert user.notification_preferences.id == pref.id
        assert user.notification_preferences.user_id == user.id
    
    def test_one_to_one_relationship(self, db):
        """Test that user-preference is a one-to-one relationship"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(user=user)
        db.session.commit()
        
        # User should have exactly one preference
        assert user.notification_preferences is not None
        assert isinstance(user.notification_preferences, NotificationPreference)
        # Not a list, but a single object


class TestNotificationPreferenceRepr:
    """Test notification preference string representation"""
    
    def test_repr(self, db):
        """Test string representation of notification preference"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(user=user)
        
        assert repr(pref) == f'<NotificationPreference User#{user.id}>'
    
    def test_repr_different_users(self, db):
        """Test repr for different users"""
        user1 = UserFactory()
        user2 = UserFactory()
        
        pref1 = NotificationPreferenceFactory(user=user1)
        pref2 = NotificationPreferenceFactory(user=user2)
        
        assert f'User#{user1.id}' in repr(pref1)
        assert f'User#{user2.id}' in repr(pref2)


class TestNotificationPreferenceScenarios:
    """Test real-world notification preference scenarios"""
    
    def test_customer_default_preferences(self, db):
        """Test default preferences for a customer"""
        customer = UserFactory(role='customer')
        pref = NotificationPreference(user_id=customer.id)
        db.session.add(pref)
        db.session.commit()
        
        # Customers typically want order updates and promotional emails
        assert pref.email_enabled is True
        assert pref.order_status_updates is True
        assert pref.promotional_emails is True
        # But not SMS by default (opt-in)
        assert pref.sms_enabled is False
    
    def test_staff_preferences(self, db):
        """Test preferences for a staff member"""
        staff = UserFactory(role='staff')
        pref = NotificationPreferenceFactory(
            user=staff,
            email_enabled=True,
            low_stock_alerts=True,
            promotional_emails=False  # Staff doesn't need promotional emails
        )
        
        assert pref.email_enabled is True
        assert pref.low_stock_alerts is True
        assert pref.promotional_emails is False
    
    def test_opt_out_all_notifications(self, db):
        """Test user opting out of all notifications"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(
            user=user,
            email_enabled=False,
            sms_enabled=False,
            order_status_updates=False,
            promotional_emails=False,
            low_stock_alerts=False
        )
        
        data = pref.to_dict()
        
        # All should be False
        assert not data['email_enabled']
        assert not data['sms_enabled']
        assert not data['order_status_updates']
        assert not data['promotional_emails']
        assert not data['low_stock_alerts']
    
    def test_selective_notifications(self, db):
        """Test user with selective notification preferences"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(
            user=user,
            email_enabled=True,
            sms_enabled=True,
            order_status_updates=True,  # Want order updates
            promotional_emails=False,   # Don't want promotions
            low_stock_alerts=False      # Not relevant for customer
        )
        
        assert pref.email_enabled is True
        assert pref.sms_enabled is True
        assert pref.order_status_updates is True
        assert pref.promotional_emails is False
        assert pref.low_stock_alerts is False
    
    def test_update_preferences(self, db):
        """Test updating notification preferences"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(
            user=user,
            email_enabled=True,
            promotional_emails=True
        )
        
        # User decides to opt out of promotional emails
        pref.promotional_emails = False
        db.session.commit()
        
        assert pref.promotional_emails is False
        assert pref.email_enabled is True  # Other settings unchanged
    
    def test_enable_sms_notifications(self, db):
        """Test enabling SMS notifications (opt-in)"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(
            user=user,
            sms_enabled=False
        )
        
        # User opts in to SMS
        pref.sms_enabled = True
        db.session.commit()
        
        assert pref.sms_enabled is True


class TestNotificationPreferenceEdgeCases:
    """Test edge cases and special scenarios"""
    
    def test_preference_for_inactive_user(self, db):
        """Test notification preference for inactive user"""
        user = UserFactory(is_active=False)
        pref = NotificationPreferenceFactory(user=user)
        
        # Preference should exist even if user is inactive
        assert pref.user_id == user.id
        assert pref.user.is_active is False
    
    def test_preference_for_unverified_email(self, db):
        """Test notification preference for user with unverified email"""
        user = UserFactory(email_verified=False)
        pref = NotificationPreferenceFactory(
            user=user,
            email_enabled=True
        )
        
        # Preference can be set, but application should check email_verified
        assert pref.email_enabled is True
        assert pref.user.email_verified is False
    
    def test_all_boolean_fields_are_boolean(self, db):
        """Test that all preference fields are boolean"""
        pref = NotificationPreferenceFactory()
        
        assert isinstance(pref.email_enabled, bool)
        assert isinstance(pref.sms_enabled, bool)
        assert isinstance(pref.order_status_updates, bool)
        assert isinstance(pref.promotional_emails, bool)
        assert isinstance(pref.low_stock_alerts, bool)
    
    def test_preference_persistence(self, db):
        """Test that preferences persist across sessions"""
        user = UserFactory()
        pref = NotificationPreferenceFactory(
            user=user,
            email_enabled=False,
            sms_enabled=True
        )
        pref_id = pref.id
        db.session.commit()
        
        # Simulate new session
        db.session.expire_all()
        
        # Retrieve preference
        retrieved_pref = db.session.get(NotificationPreference, pref_id)
        
        assert retrieved_pref is not None
        assert retrieved_pref.email_enabled is False
        assert retrieved_pref.sms_enabled is True
