"""
Review service
Handles product reviews and ratings
"""
import logging
from typing import Optional, Dict, List
from sqlalchemy import func, and_
from models.review import Review
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.user import User
from extensions import db

logger = logging.getLogger(__name__)


class ReviewService:
    """Service for handling product reviews"""
    
    @staticmethod
    def create_review(user_id: int, product_id: int, rating: int, 
                     comment: Optional[str] = None) -> Dict:
        """
        Create a new review
        
        Args:
            user_id: User ID
            product_id: Product ID
            rating: Rating (1-5)
            comment: Review comment (optional)
            
        Returns:
            Dictionary with result
        """
        try:
            # Validate rating
            if not Review.validate_rating(rating):
                return {'success': False, 'error': 'Rating must be between 1 and 5'}
            
            # Check if product exists
            product = Product.query.get(product_id)
            if not product:
                return {'success': False, 'error': 'Product not found'}
            
            # Check if user already reviewed this product
            existing_review = Review.query.filter_by(
                user_id=user_id,
                product_id=product_id
            ).first()
            
            if existing_review:
                return {'success': False, 'error': 'You have already reviewed this product'}
            
            # Check if user purchased this product (for verified purchase badge)
            is_verified = ReviewService._check_verified_purchase(user_id, product_id)
            
            # Create review
            review = Review(
                user_id=user_id,
                product_id=product_id,
                rating=rating,
                comment=comment,
                is_verified_purchase=is_verified,
                is_approved=True  # Auto-approve for now, can add moderation later
            )
            
            db.session.add(review)
            db.session.commit()
            
            # Update product average rating
            ReviewService._update_product_rating(product_id)
            
            logger.info(f"Review created: User {user_id} reviewed Product {product_id} with {rating} stars")
            
            return {
                'success': True,
                'message': 'Review created successfully',
                'data': review.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating review: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_review(review_id: int, user_id: int, rating: Optional[int] = None,
                     comment: Optional[str] = None) -> Dict:
        """
        Update an existing review
        
        Args:
            review_id: Review ID
            user_id: User ID (for authorization)
            rating: New rating (optional)
            comment: New comment (optional)
            
        Returns:
            Dictionary with result
        """
        try:
            review = Review.query.get(review_id)
            
            if not review:
                return {'success': False, 'error': 'Review not found'}
            
            # Check authorization
            if review.user_id != user_id:
                return {'success': False, 'error': 'Unauthorized to update this review'}
            
            # Update fields
            if rating is not None:
                if not Review.validate_rating(rating):
                    return {'success': False, 'error': 'Rating must be between 1 and 5'}
                review.rating = rating
            
            if comment is not None:
                review.comment = comment
            
            db.session.commit()
            
            # Update product average rating
            ReviewService._update_product_rating(review.product_id)
            
            logger.info(f"Review updated: Review {review_id}")
            
            return {
                'success': True,
                'message': 'Review updated successfully',
                'data': review.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating review: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_review(review_id: int, user_id: int, is_admin: bool = False) -> Dict:
        """
        Delete a review
        
        Args:
            review_id: Review ID
            user_id: User ID (for authorization)
            is_admin: Whether user is admin
            
        Returns:
            Dictionary with result
        """
        try:
            review = Review.query.get(review_id)
            
            if not review:
                return {'success': False, 'error': 'Review not found'}
            
            # Check authorization (user can delete own review, admin can delete any)
            if not is_admin and review.user_id != user_id:
                return {'success': False, 'error': 'Unauthorized to delete this review'}
            
            product_id = review.product_id
            
            db.session.delete(review)
            db.session.commit()
            
            # Update product average rating
            ReviewService._update_product_rating(product_id)
            
            logger.info(f"Review deleted: Review {review_id}")
            
            return {
                'success': True,
                'message': 'Review deleted successfully'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting review: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_product_reviews(product_id: int, page: int = 1, per_page: int = 10,
                           approved_only: bool = True) -> Dict:
        """
        Get reviews for a product
        
        Args:
            product_id: Product ID
            page: Page number
            per_page: Items per page
            approved_only: Only show approved reviews
            
        Returns:
            Dictionary with reviews and pagination
        """
        try:
            query = Review.query.filter_by(product_id=product_id)
            
            if approved_only:
                query = query.filter_by(is_approved=True)
            
            query = query.order_by(Review.created_at.desc())
            
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            reviews = [review.to_dict() for review in pagination.items]
            
            # Get rating statistics
            stats = ReviewService.get_product_rating_stats(product_id)
            
            return {
                'success': True,
                'data': {
                    'reviews': reviews,
                    'pagination': {
                        'page': page,
                        'per_page': per_page,
                        'total': pagination.total,
                        'pages': pagination.pages
                    },
                    'stats': stats
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting product reviews: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_user_reviews(user_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """
        Get reviews by a user
        
        Args:
            user_id: User ID
            page: Page number
            per_page: Items per page
            
        Returns:
            Dictionary with reviews and pagination
        """
        try:
            query = Review.query.filter_by(user_id=user_id).order_by(Review.created_at.desc())
            
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            reviews = [review.to_dict() for review in pagination.items]
            
            return {
                'success': True,
                'data': {
                    'reviews': reviews,
                    'pagination': {
                        'page': page,
                        'per_page': per_page,
                        'total': pagination.total,
                        'pages': pagination.pages
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting user reviews: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def mark_helpful(review_id: int) -> Dict:
        """
        Mark a review as helpful
        
        Args:
            review_id: Review ID
            
        Returns:
            Dictionary with result
        """
        try:
            review = Review.query.get(review_id)
            
            if not review:
                return {'success': False, 'error': 'Review not found'}
            
            review.helpful_count += 1
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Review marked as helpful',
                'helpful_count': review.helpful_count
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error marking review as helpful: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def moderate_review(review_id: int, is_approved: bool) -> Dict:
        """
        Moderate a review (approve/reject)
        
        Args:
            review_id: Review ID
            is_approved: Whether to approve the review
            
        Returns:
            Dictionary with result
        """
        try:
            review = Review.query.get(review_id)
            
            if not review:
                return {'success': False, 'error': 'Review not found'}
            
            review.is_approved = is_approved
            db.session.commit()
            
            # Update product rating if approval status changed
            ReviewService._update_product_rating(review.product_id)
            
            status = 'approved' if is_approved else 'rejected'
            logger.info(f"Review {review_id} {status}")
            
            return {
                'success': True,
                'message': f'Review {status} successfully'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error moderating review: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_product_rating_stats(product_id: int) -> Dict:
        """
        Get rating statistics for a product
        
        Args:
            product_id: Product ID
            
        Returns:
            Dictionary with rating statistics
        """
        try:
            # Get approved reviews only
            reviews = Review.query.filter_by(
                product_id=product_id,
                is_approved=True
            ).all()
            
            if not reviews:
                return {
                    'average_rating': 0,
                    'total_reviews': 0,
                    'rating_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                    'verified_purchases': 0
                }
            
            # Calculate statistics
            total_reviews = len(reviews)
            average_rating = sum(r.rating for r in reviews) / total_reviews
            verified_purchases = sum(1 for r in reviews if r.is_verified_purchase)
            
            # Rating distribution
            rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for review in reviews:
                rating_distribution[review.rating] += 1
            
            return {
                'average_rating': round(average_rating, 2),
                'total_reviews': total_reviews,
                'rating_distribution': rating_distribution,
                'verified_purchases': verified_purchases
            }
            
        except Exception as e:
            logger.error(f"Error getting rating stats: {str(e)}")
            return {
                'average_rating': 0,
                'total_reviews': 0,
                'rating_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                'verified_purchases': 0
            }
    
    @staticmethod
    def _check_verified_purchase(user_id: int, product_id: int) -> bool:
        """
        Check if user has purchased this product
        
        Args:
            user_id: User ID
            product_id: Product ID
            
        Returns:
            True if user purchased this product
        """
        try:
            # Check if user has a completed order with this product
            purchase = db.session.query(OrderItem).join(Order).filter(
                and_(
                    Order.user_id == user_id,
                    OrderItem.product_id == product_id,
                    Order.status.in_(['completed', 'delivered'])
                )
            ).first()
            
            return purchase is not None
            
        except Exception as e:
            logger.error(f"Error checking verified purchase: {str(e)}")
            return False
    
    @staticmethod
    def _update_product_rating(product_id: int):
        """
        Update product's average rating
        
        Args:
            product_id: Product ID
        """
        try:
            stats = ReviewService.get_product_rating_stats(product_id)
            
            product = Product.query.get(product_id)
            if product and hasattr(product, 'average_rating'):
                product.average_rating = stats['average_rating']
                product.review_count = stats['total_reviews']
                db.session.commit()
                
        except Exception as e:
            logger.error(f"Error updating product rating: {str(e)}")
            db.session.rollback()
