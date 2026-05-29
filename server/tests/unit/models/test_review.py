"""
Unit tests for Review model

Tests cover:
- Model creation with valid data
- Required fields validation
- Rating validation (1-5 stars)
- User and product relationships
- Verified purchase flag
- Approval status
- Helpful count tracking
- Unique constraint (one review per user per product)
- Model methods (validate_rating)
- Serialization (to_dict)
"""

import pytest
from models.review import Review
from tests.factories import ReviewFactory, UserFactory, ProductFactory


class TestReviewCreation:
    """Test review creation and basic attributes"""
    
    def test_review_creation_with_valid_data(self, db):
        """Test creating a review with all valid data"""
        user = UserFactory()
        product = ProductFactory()
        review = ReviewFactory(
            user=user,
            product=product,
            rating=5,
            comment='Excellent coffee!',
            is_verified_purchase=True,
            is_approved=True
        )
        
        assert review.id is not None
        assert review.user_id == user.id
        assert review.product_id == product.id
        assert review.rating == 5
        assert review.comment == 'Excellent coffee!'
        assert review.is_verified_purchase is True
        assert review.is_approved is True
        assert review.created_at is not None
    
    def test_review_creation_with_minimal_data(self, db):
        """Test creating a review with only required fields"""
        user = UserFactory()
        product = ProductFactory()
        review = Review(
            user_id=user.id,
            product_id=product.id,
            rating=4
        )
        db.session.add(review)
        db.session.commit()
        
        assert review.id is not None
        assert review.user_id == user.id
        assert review.product_id == product.id
        assert review.rating == 4
    
    def test_review_default_values(self, db):
        """Test that default values are set correctly"""
        user = UserFactory()
        product = ProductFactory()
        review = Review(
            user_id=user.id,
            product_id=product.id,
            rating=5
        )
        db.session.add(review)
        db.session.commit()
        
        assert review.is_verified_purchase is False
        assert review.is_approved is True
        assert review.helpful_count == 0
        assert review.created_at is not None
        assert review.updated_at is not None


class TestReviewFieldValidation:
    """Test field validation and constraints"""
    
    def test_user_id_required(self, db):
        """Test that user_id is required"""
        product = ProductFactory()
        review = Review(
            product_id=product.id,
            rating=5
        )
        db.session.add(review)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_product_id_required(self, db):
        """Test that product_id is required"""
        user = UserFactory()
        review = Review(
            user_id=user.id,
            rating=5
        )
        db.session.add(review)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_rating_required(self, db):
        """Test that rating is required"""
        user = UserFactory()
        product = ProductFactory()
        review = Review(
            user_id=user.id,
            product_id=product.id
        )
        db.session.add(review)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_unique_user_product_constraint(self, db):
        """Test that a user can only review a product once"""
        user = UserFactory()
        product = ProductFactory()
        
        # Create first review
        ReviewFactory(user=user, product=product, rating=5)
        
        # Try to create second review for same user and product
        with pytest.raises(Exception):  # IntegrityError
            ReviewFactory(user=user, product=product, rating=4)
    
    def test_different_users_can_review_same_product(self, db):
        """Test that different users can review the same product"""
        user1 = UserFactory()
        user2 = UserFactory()
        product = ProductFactory()
        
        review1 = ReviewFactory(user=user1, product=product, rating=5)
        review2 = ReviewFactory(user=user2, product=product, rating=4)
        
        assert review1.id != review2.id
        assert review1.product_id == review2.product_id
        assert review1.user_id != review2.user_id
    
    def test_same_user_can_review_different_products(self, db):
        """Test that same user can review different products"""
        user = UserFactory()
        product1 = ProductFactory()
        product2 = ProductFactory()
        
        review1 = ReviewFactory(user=user, product=product1, rating=5)
        review2 = ReviewFactory(user=user, product=product2, rating=4)
        
        assert review1.id != review2.id
        assert review1.user_id == review2.user_id
        assert review1.product_id != review2.product_id


class TestReviewRatingValidation:
    """Test rating validation"""
    
    def test_rating_values_1_to_5(self, db):
        """Test all valid rating values (1-5)"""
        user = UserFactory()
        
        for rating in [1, 2, 3, 4, 5]:
            product = ProductFactory()
            review = ReviewFactory(user=user, product=product, rating=rating)
            assert review.rating == rating
    
    def test_validate_rating_static_method_valid(self):
        """Test validate_rating static method with valid ratings"""
        assert Review.validate_rating(1) is True
        assert Review.validate_rating(2) is True
        assert Review.validate_rating(3) is True
        assert Review.validate_rating(4) is True
        assert Review.validate_rating(5) is True
    
    def test_validate_rating_static_method_invalid(self):
        """Test validate_rating static method with invalid ratings"""
        assert Review.validate_rating(0) is False
        assert Review.validate_rating(6) is False
        assert Review.validate_rating(-1) is False
        assert Review.validate_rating(10) is False
    
    def test_rating_boundary_values(self, db):
        """Test rating boundary values"""
        user = UserFactory()
        
        # Minimum valid rating
        product1 = ProductFactory()
        review1 = ReviewFactory(user=user, product=product1, rating=1)
        assert review1.rating == 1
        
        # Maximum valid rating
        product2 = ProductFactory()
        review2 = ReviewFactory(user=user, product=product2, rating=5)
        assert review2.rating == 5


class TestReviewComment:
    """Test review comment field"""
    
    def test_comment_with_text(self, db):
        """Test comment with text content"""
        review = ReviewFactory(comment='Great product, highly recommend!')
        
        assert review.comment == 'Great product, highly recommend!'
    
    def test_comment_can_be_null(self, db):
        """Test that comment can be None"""
        review = ReviewFactory(comment=None)
        
        assert review.comment is None
    
    def test_comment_can_be_long(self, db):
        """Test that comment can be long text"""
        long_comment = 'A' * 500
        review = ReviewFactory(comment=long_comment)
        
        assert len(review.comment) == 500
    
    def test_comment_can_be_empty_string(self, db):
        """Test that comment can be empty string"""
        review = ReviewFactory(comment='')
        
        assert review.comment == ''


class TestReviewVerifiedPurchase:
    """Test verified purchase flag"""
    
    def test_is_verified_purchase_true(self, db):
        """Test is_verified_purchase flag set to True"""
        review = ReviewFactory(is_verified_purchase=True)
        
        assert review.is_verified_purchase is True
    
    def test_is_verified_purchase_false(self, db):
        """Test is_verified_purchase flag set to False"""
        review = ReviewFactory(is_verified_purchase=False)
        
        assert review.is_verified_purchase is False
    
    def test_is_verified_purchase_default(self, db):
        """Test is_verified_purchase defaults to False"""
        user = UserFactory()
        product = ProductFactory()
        review = Review(
            user_id=user.id,
            product_id=product.id,
            rating=5
        )
        db.session.add(review)
        db.session.commit()
        
        assert review.is_verified_purchase is False


class TestReviewApprovalStatus:
    """Test review approval/moderation"""
    
    def test_is_approved_true(self, db):
        """Test is_approved flag set to True"""
        review = ReviewFactory(is_approved=True)
        
        assert review.is_approved is True
    
    def test_is_approved_false(self, db):
        """Test is_approved flag set to False"""
        review = ReviewFactory(is_approved=False)
        
        assert review.is_approved is False
    
    def test_is_approved_default(self, db):
        """Test is_approved defaults to True"""
        user = UserFactory()
        product = ProductFactory()
        review = Review(
            user_id=user.id,
            product_id=product.id,
            rating=5
        )
        db.session.add(review)
        db.session.commit()
        
        assert review.is_approved is True
    
    def test_approve_review(self, db):
        """Test approving a review"""
        review = ReviewFactory(is_approved=False)
        
        review.is_approved = True
        db.session.commit()
        
        assert review.is_approved is True
    
    def test_unapprove_review(self, db):
        """Test unapproving a review"""
        review = ReviewFactory(is_approved=True)
        
        review.is_approved = False
        db.session.commit()
        
        assert review.is_approved is False


class TestReviewHelpfulCount:
    """Test helpful count tracking"""
    
    def test_helpful_count_default(self, db):
        """Test helpful_count defaults to 0"""
        review = ReviewFactory()
        
        assert review.helpful_count == 0
    
    def test_helpful_count_can_be_incremented(self, db):
        """Test that helpful_count can be incremented"""
        review = ReviewFactory(helpful_count=0)
        
        review.helpful_count += 1
        db.session.commit()
        
        assert review.helpful_count == 1
    
    def test_helpful_count_multiple_increments(self, db):
        """Test multiple increments of helpful_count"""
        review = ReviewFactory(helpful_count=0)
        
        for i in range(5):
            review.helpful_count += 1
        db.session.commit()
        
        assert review.helpful_count == 5
    
    def test_helpful_count_custom_value(self, db):
        """Test setting custom helpful_count value"""
        review = ReviewFactory(helpful_count=42)
        
        assert review.helpful_count == 42


class TestReviewSerialization:
    """Test review serialization to dictionary"""
    
    def test_to_dict_basic(self, db):
        """Test basic to_dict conversion"""
        user = UserFactory(username='reviewer', first_name='John')
        product = ProductFactory()
        review = ReviewFactory(
            user=user,
            product=product,
            rating=5,
            comment='Excellent!',
            is_verified_purchase=True,
            helpful_count=10
        )
        
        data = review.to_dict()
        
        assert data['id'] == review.id
        assert data['product_id'] == product.id
        assert data['rating'] == 5
        assert data['comment'] == 'Excellent!'
        assert data['is_verified_purchase'] is True
        assert data['is_approved'] is True
        assert data['helpful_count'] == 10
        assert 'created_at' in data
        assert isinstance(data['created_at'], str)
    
    def test_to_dict_includes_user_by_default(self, db):
        """Test that to_dict includes user information by default"""
        user = UserFactory(
            username='reviewer',
            first_name='John'
        )
        review = ReviewFactory(user=user)
        
        data = review.to_dict()
        
        assert 'user' in data
        assert data['user'] is not None
        assert data['user']['username'] == 'reviewer'
        assert data['user']['first_name'] == 'John'
    
    def test_to_dict_without_user(self, db):
        """Test to_dict with include_user=False"""
        user = UserFactory()
        review = ReviewFactory(user=user)
        
        data = review.to_dict(include_user=False)
        
        assert 'user' not in data
    
    def test_to_dict_with_null_comment(self, db):
        """Test to_dict when comment is None"""
        review = ReviewFactory(comment=None)
        
        data = review.to_dict()
        
        assert data['comment'] is None
    
    def test_to_dict_user_info_structure(self, db):
        """Test that user info in to_dict has correct structure"""
        user = UserFactory(
            id=123,
            username='testuser',
            first_name='Test'
        )
        review = ReviewFactory(user=user)
        
        data = review.to_dict()
        
        assert 'user' in data
        assert 'id' in data['user']
        assert 'username' in data['user']
        assert 'first_name' in data['user']
        assert data['user']['id'] == 123
        assert data['user']['username'] == 'testuser'
        assert data['user']['first_name'] == 'Test'


class TestReviewRelationships:
    """Test review relationships with other models"""
    
    def test_review_user_relationship(self, db):
        """Test that review has user relationship"""
        user = UserFactory(username='reviewer')
        review = ReviewFactory(user=user)
        
        assert review.user is not None
        assert review.user.username == 'reviewer'
        assert review.user_id == user.id
    
    def test_review_product_relationship(self, db):
        """Test that review has product relationship"""
        product = ProductFactory(name='Cappuccino')
        review = ReviewFactory(product=product)
        
        assert review.product is not None
        assert review.product.name == 'Cappuccino'
        assert review.product_id == product.id
    
    def test_user_reviews_backref(self, db):
        """Test that user has reviews backref"""
        user = UserFactory()
        review1 = ReviewFactory(user=user)
        review2 = ReviewFactory(user=user)
        db.session.commit()
        
        assert len(user.reviews) == 2
        assert review1 in user.reviews
        assert review2 in user.reviews
    
    def test_product_reviews_backref(self, db):
        """Test that product has reviews backref"""
        product = ProductFactory()
        review1 = ReviewFactory(product=product)
        review2 = ReviewFactory(product=product)
        db.session.commit()
        
        assert len(product.reviews) == 2
        assert review1 in product.reviews
        assert review2 in product.reviews


class TestReviewRepr:
    """Test review string representation"""
    
    def test_repr(self, db):
        """Test string representation of review"""
        user = UserFactory(username='reviewer')
        review = ReviewFactory(user=user, rating=5)
        
        assert repr(review) == '<Review 5★ by reviewer>'
    
    def test_repr_different_ratings(self, db):
        """Test repr with different ratings"""
        user = UserFactory(username='testuser')
        
        for rating in [1, 2, 3, 4, 5]:
            product = ProductFactory()
            review = ReviewFactory(user=user, product=product, rating=rating)
            assert repr(review) == f'<Review {rating}★ by testuser>'


class TestReviewTimestamps:
    """Test review timestamp fields"""
    
    def test_created_at_set_on_creation(self, db):
        """Test that created_at is set automatically"""
        review = ReviewFactory()
        
        assert review.created_at is not None
    
    def test_updated_at_set_on_creation(self, db):
        """Test that updated_at is set automatically"""
        review = ReviewFactory()
        
        assert review.updated_at is not None
    
    def test_updated_at_changes_on_update(self, db):
        """Test that updated_at changes when review is updated"""
        review = ReviewFactory()
        original_updated_at = review.updated_at
        
        import time
        time.sleep(0.01)
        
        review.comment = 'Updated comment'
        db.session.commit()
        
        assert review.updated_at >= original_updated_at


class TestReviewEdgeCases:
    """Test edge cases and special scenarios"""
    
    def test_review_with_special_characters_in_comment(self, db):
        """Test review comment with special characters"""
        review = ReviewFactory(comment='Great coffee! ☕ 100% recommended 👍')
        
        assert '☕' in review.comment
        assert '👍' in review.comment
    
    def test_review_with_html_in_comment(self, db):
        """Test review comment with HTML-like content"""
        review = ReviewFactory(comment='<script>alert("test")</script>')
        
        # Comment should be stored as-is (sanitization happens at application layer)
        assert '<script>' in review.comment
    
    def test_multiple_reviews_same_rating(self, db):
        """Test multiple reviews with same rating"""
        product = ProductFactory()
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        
        review1 = ReviewFactory(user=user1, product=product, rating=5)
        review2 = ReviewFactory(user=user2, product=product, rating=5)
        review3 = ReviewFactory(user=user3, product=product, rating=5)
        
        assert review1.rating == review2.rating == review3.rating == 5
