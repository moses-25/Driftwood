"""
Notification Routes
API endpoints for notification management
"""

from flask import Blueprint, request, jsonify
from services.notification_service import NotificationService
from utils.decorators import jwt_required, role_required
from utils.response_formatter import success_response, error_response
from flask_jwt_extended import get_jwt_identity
import logging

logger = logging.getLogger(__name__)

notification_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')


@notification_bp.route('/preferences', methods=['GET'])
@jwt_required
def get_preferences():
    """Get current user's notification preferences"""
    try:
        user_id = get_jwt_identity()
        
        preferences = NotificationService.get_notification_preferences(user_id)
        
        return success_response(
            data=preferences,
            message="Notification preferences retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error getting preferences: {str(e)}")
        return error_response("Failed to get notification preferences", 500)


@notification_bp.route('/preferences', methods=['PUT'])
@jwt_required
def update_preferences():
    """
    Update notification preferences
    Body: email_enabled, sms_enabled, order_status_updates, promotional_emails, low_stock_alerts
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        preferences = NotificationService.update_notification_preferences(user_id, data)
        
        return success_response(
            data=preferences,
            message="Notification preferences updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Error updating preferences: {str(e)}")
        return error_response("Failed to update notification preferences", 500)


@notification_bp.route('/test', methods=['POST'])
@jwt_required
@role_required(['admin'])
def test_notification():
    """
    Test notification system (Admin only)
    Body: order_id, status
    """
    try:
        data = request.get_json()
        
        order_id = data.get('order_id')
        status = data.get('status', 'confirmed')
        
        if not order_id:
            return error_response("order_id is required", 400)
        
        success = NotificationService.send_order_status_notification(order_id, status)
        
        if success:
            return success_response(
                data={'sent': True},
                message="Test notification sent successfully"
            )
        else:
            return error_response("Failed to send test notification", 500)
        
    except Exception as e:
        logger.error(f"Error sending test notification: {str(e)}")
        return error_response("Failed to send test notification", 500)
