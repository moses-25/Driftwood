"""
Unit Tests for User Model
Tests user creation, password hashing, and methods
"""
import pytest
from models.user import User
from datetime import datetime


@pytest.mark.unit
class TestUserModel:
    """Test User model"""
    
    def test_user_creation(self, db):
        """Test creating a user"""
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='customer'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'customer'
        assert user.is_active is True
        assert user.email_verified is False
    
    def test_password_hashing(self, db):
        """Test password is hashed"""
        user = User(username='test', email='test@example.com')
        user.set_password('password123')
        
        assert user.password_hash is not None
        assert user.password_hash != 'password123'
        assert len(user.password_hash) > 20
    
    def test_password_verification(self, db):
        """Test password verification"""
        user = User(username='test', email='test@example.com')
        user.set_password('password123')
        
        assert user.check_password('password123') is True
        assert user.check_password('wrongpassword') is False
    
    def test_get_full_name(self, db):
        """Test get_full_name method"""
        user = User(
            username='test',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        
        assert user.get_full_name() == 'John Doe'
    
    def test_get_full_name_without_names(self, db):
        """Test get_full_name returns username if no names"""
        user = User(username='testuser', email='test@example.com')
        
        assert user.get_full_name() == 'testuser'
    
    def test_to_dict(self, db):
        """Test to_dict method"""
        user = User(
            username='test',
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            role='customer'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        user_dict = user.to_dict()
        
        assert user_dict['username'] == 'test'
        assert user_dict['email'] == 'test@example.com'
        assert user_dict['first_name'] == 'John'
        assert user_dict['role'] == 'customer'
        assert 'password_hash' not in user_dict
        assert 'password' not in user_dict
    
    def test_user_roles(self, db):
        """Test different user roles"""
        customer = User(username='customer', email='c@example.com', role='customer')
        staff = User(username='staff', email='s@example.com', role='staff')
        admin = User(username='admin', email='a@example.com', role='admin')
        
        assert customer.role == 'customer'
        assert staff.role == 'staff'
        assert admin.role == 'admin'
    
    def test_user_active_status(self, db):
        """Test user active status"""
        user = User(username='test', email='test@example.com', is_active=False)
        
        assert user.is_active is False
        
        user.is_active = True
        assert user.is_active is True
    
    def test_email_verified_status(self, db):
        """Test email verified status"""
        user = User(username='test', email='test@example.com')
        
        assert user.email_verified is False
        
        user.email_verified = True
        assert user.email_verified is True
    
    def test_user_timestamps(self, db):
        """Test user timestamps"""
        user = User(username='test', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)
        assert user.updated_at is not None
    
    def test_user_repr(self, db):
        """Test user string representation"""
        user = User(username='testuser', email='test@example.com')
        
        assert repr(user) == '<User testuser>'
    
    def test_unique_username(self, db):
        """Test username must be unique"""
        user1 = User(username='test', email='test1@example.com')
        user1.set_password('password123')
        db.session.add(user1)
        db.session.commit()
        
        user2 = User(username='test', email='test2@example.com')
        user2.set_password('password123')
        db.session.add(user2)
        
        with pytest.raises(Exception):
            db.session.commit()
    
    def test_unique_email(self, db):
        """Test email must be unique"""
        user1 = User(username='test1', email='test@example.com')
        user1.set_password('password123')
        db.session.add(user1)
        db.session.commit()
        
        user2 = User(username='test2', email='test@example.com')
        user2.set_password('password123')
        db.session.add(user2)
        
        with pytest.raises(Exception):
            db.session.commit()
