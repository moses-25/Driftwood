"""
Review routes
Handles all review-related API endpoints
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.review_service import ReviewService
from utils.decorators import admin_required
from models.user import User
import logging

review_bp = Blueprint('review', __name__)
logger = logging.getLogger(__name__)


@review_bp.route('/reviews/product/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    """
    Get reviews for a product
    
    Path Parameters:
        product_id (int): Product ID
        
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10)
        
    Returns:
        200: Reviews list with pagination and stats
        500: Server error
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = ReviewService.get_product_reviews(product_id, page, per_page)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error getting product reviews: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@review_bp.route('/reviews/user/<int:user_id>', methods=['GET'])
def get_user_reviews(user_id):
    """
    Get reviews by a user
    
    Path Parameters:
        user_id (int): User ID
        
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10)
        
    Returns:
        200: Reviews list with pagination
        500: Server error
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = ReviewService.get_user_reviews(user_id, page, per_page)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error getting user reviews: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@review_bp.route('/reviews/my-reviews', methods=['GET'])
@jwt_required()
def get_my_reviews():
    """
    Get current user's reviews
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10)
        
    Returns:
        200: Reviews list with pagination
        500: Server error
    """
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = ReviewService.get_user_reviews(current_user_id, page, per_page)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error getting my reviews: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@review_bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    """
    Create a new review
    
    Request Body:
        product_id (int): Product ID (required)
        rating (int): Rating 1-5 (required)
        comment (str): Review comment (optional)
        
    Returns:
        201: Review created
        400: Validation error
        500: Server error
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'product_id' not in data or 'rating' not in data:
            return jsonify({'success': False, 'error': 'product_id and rating are required'}), 400
        
        result = ReviewService.create_review(
            user_id=current_user_id,
            product_id=data['product_id'],
            rating=data['rating'],
            comment=data.get('comment')
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error creating review: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@review_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """
    Update a review
    
    Path Parameters:
        review_id (int): Review ID
        
    Request Body:
        rating (int): New rating (optional)
        comment (str): New comment (optional)
        
    Returns:
        200: Review updated
        400: Validation error
        403: Unauthorized
        404: Review not found
        500: Server error
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        result = ReviewService.update_review(
            review_id=review_id,
            user_id=current_user_id,
            rating=data.get('rating'),
            comment=data.get('comment')
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            status_code = 403 if 'Unauthorized' in result.get('error', '') else 400
            return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error updating review: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """
    Delete a review
    
    Path Parameters:
        review_id (int): Review ID
        
    Returns:
        200: Review deleted
        403: Unauthorized
        404: Review not found
        500: Server error
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is admin
        user = User.query.get(current_user_id)
        is_admin = user and user.role == 'admin'
        
        result = ReviewService.delete_review(
            review_id=review_id,
            user_id=current_user_id,
            is_admin=is_admin
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            status_code = 403 if 'Unauthorized' in result.get('error', '') else 400
            return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error deleting review: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@review_bp.route('/reviews/<int:review_id>/helpful', methods=['POST'])
def mark_review_helpful(review_id):
    """
    Mark a review as helpful
    
    Path Parameters:
        review_id (int): Review ID
        
    Returns:
        200: Review marked as helpful
        404: Review not found
        500: Server error
    """
    try:
        result = ReviewService.mark_helpful(review_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
        
    except Exception as e:
        logger.error(f"Error marking review as helpful: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@review_bp.route('/reviews/<int:review_id>/moderate', methods=['POST'])
@jwt_required()
@admin_required
def moderate_review(review_id):
    """
    Moderate a review (Admin only)
    
    Path Parameters:
        review_id (int): Review ID
        
    Request Body:
        is_approved (bool): Whether to approve the review (required)
        
    Returns:
        200: Review moderated
        400: Validation error
        404: Review not found
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data or 'is_approved' not in data:
            return jsonify({'success': False, 'error': 'is_approved is required'}), 400
        
        result = ReviewService.moderate_review(
            review_id=review_id,
            is_approved=data['is_approved']
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
        
    except Exception as e:
        logger.error(f"Error moderating review: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@review_bp.route('/reviews/product/<int:product_id>/stats', methods=['GET'])
def get_product_rating_stats(product_id):
    """
    Get rating statistics for a product
    
    Path Parameters:
        product_id (int): Product ID
        
    Returns:
        200: Rating statistics
        500: Server error
    """
    try:
        stats = ReviewService.get_product_rating_stats(product_id)
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting rating stats: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
