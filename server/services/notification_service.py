"""
Notification Service
Business logic for sending notifications
"""

from models.notification_preference import NotificationPreference
from models.user import User
from models.order import Order
from extensions import db
from utils.email_utils import send_email, render_email_template
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for notification operations"""
    
    @staticmethod
    def get_notification_preferences(user_id):
        """
        Get user notification preferences
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with preferences
        """
        try:
            prefs = NotificationPreference.query.filter_by(user_id=user_id).first()
            
            # Create default preferences if not exist
            if not prefs:
                prefs = NotificationPreference(user_id=user_id)
                db.session.add(prefs)
                db.session.commit()
            
            return prefs.to_dict()
            
        except Exception as e:
            logger.error(f"Error getting notification preferences: {str(e)}")
            raise
    
    @staticmethod
    def update_notification_preferences(user_id, preferences):
        """
        Update user notification preferences
        
        Args:
            user_id: User ID
            preferences: Dictionary with preference updates
        
        Returns:
            Updated preferences dictionary
        """
        try:
            prefs = NotificationPreference.query.filter_by(user_id=user_id).first()
            
            if not prefs:
                prefs = NotificationPreference(user_id=user_id)
                db.session.add(prefs)
            
            # Update fields
            if 'email_enabled' in preferences:
                prefs.email_enabled = preferences['email_enabled']
            if 'sms_enabled' in preferences:
                prefs.sms_enabled = preferences['sms_enabled']
            if 'order_status_updates' in preferences:
                prefs.order_status_updates = preferences['order_status_updates']
            if 'promotional_emails' in preferences:
                prefs.promotional_emails = preferences['promotional_emails']
            if 'low_stock_alerts' in preferences:
                prefs.low_stock_alerts = preferences['low_stock_alerts']
            
            db.session.commit()
            
            return prefs.to_dict()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating notification preferences: {str(e)}")
            raise
    
    @staticmethod
    def send_order_status_notification(order_id, status):
        """
        Send notification for order status change
        
        Args:
            order_id: Order ID
            status: New order status
        
        Returns:
            Boolean indicating success
        """
        try:
            order = Order.query.get(order_id)
            if not order:
                logger.warning(f"Order {order_id} not found")
                return False
            
            # Get user (skip for guest orders)
            if not order.user_id:
                logger.info(f"Skipping notification for guest order {order_id}")
                return True
            
            user = User.query.get(order.user_id)
            if not user or not user.email:
                logger.warning(f"User {order.user_id} not found or has no email")
                return False
            
            # Check notification preferences
            prefs = NotificationPreference.query.filter_by(user_id=user.id).first()
            if prefs and not prefs.email_enabled:
                logger.info(f"Email notifications disabled for user {user.id}")
                return True
            if prefs and not prefs.order_status_updates:
                logger.info(f"Order status notifications disabled for user {user.id}")
                return True
            
            # Prepare email content
            subject, template_name = NotificationService._get_email_template_for_status(status)
            
            context = {
                'customer_name': user.first_name or user.username,
                'order_number': order.order_number,
                'total_amount': f"{float(order.total_amount):,.2f}",
                'estimated_time': order.estimated_ready_time.strftime('%I:%M %p') if order.estimated_ready_time else 'Soon',
                'order_type': order.order_type
            }
            
            html_body = render_email_template(template_name, context)
            plain_body = f"Order #{order.order_number} status: {status}"
            
            # Send email
            success = send_email(
                to=user.email,
                subject=subject,
                body=plain_body,
                html=html_body
            )
            
            if success:
                logger.info(f"Notification sent for order {order_id}, status: {status}")
            else:
                logger.warning(f"Failed to send notification for order {order_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending order notification: {str(e)}")
            return False
    
    @staticmethod
    def _get_email_template_for_status(status):
        """
        Get email subject and template name for order status
        
        Args:
            status: Order status
        
        Returns:
            Tuple of (subject, template_name)
        """
        templates = {
            'confirmed': ('Order Confirmed - Driftwood Cafe', 'order_confirmed'),
            'preparing': ('Your Order is Being Prepared - Driftwood Cafe', 'order_preparing'),
            'ready': ('Your Order is Ready! - Driftwood Cafe', 'order_ready'),
            'completed': ('Order Completed - Driftwood Cafe', 'order_completed'),
            'cancelled': ('Order Cancelled - Driftwood Cafe', 'order_cancelled')
        }
        
        return templates.get(status, ('Order Update - Driftwood Cafe', 'order_confirmed'))
    
    @staticmethod
    def send_low_stock_alert(product_id, product_name, stock_quantity):
        """
        Send low stock alert to staff/admin
        
        Args:
            product_id: Product ID
            product_name: Product name
            stock_quantity: Current stock quantity
        
        Returns:
            Boolean indicating success
        """
        try:
            # Get staff and admin users with low stock alerts enabled
            staff_users = User.query.filter(User.role.in_(['staff', 'admin'])).all()
            
            for user in staff_users:
                if not user.email:
                    continue
                
                # Check preferences
                prefs = NotificationPreference.query.filter_by(user_id=user.id).first()
                if prefs and not prefs.low_stock_alerts:
                    continue
                
                subject = f"Low Stock Alert: {product_name}"
                body = f"Product '{product_name}' (ID: {product_id}) is low on stock. Current quantity: {stock_quantity}"
                
                send_email(
                    to=user.email,
                    subject=subject,
                    body=body
                )
            
            logger.info(f"Low stock alerts sent for product {product_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending low stock alert: {str(e)}")
            return False
