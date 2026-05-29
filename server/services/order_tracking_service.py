"""
Order Tracking Service
Business logic for order tracking and status management
"""

from models.order import Order
from models.order_status_history import OrderStatusHistory
from extensions import db
from services.notification_service import NotificationService
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class OrderTrackingService:
    """Service for order tracking operations"""
    
    @staticmethod
    def update_order_status(order_id, status, notes=None, user_id=None):
        """
        Update order status with history tracking and notifications
        
        Args:
            order_id: Order ID
            status: New status
            notes: Optional notes
            user_id: User making the change
        
        Returns:
            Updated order dictionary
        """
        try:
            order = Order.query.get(order_id)
            if not order:
                raise ValueError("Order not found")
            
            # Validate status
            valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            
            old_status = order.status
            
            # Update order status
            order.status = status
            
            # Set completed_at timestamp
            if status == 'completed' and not order.completed_at:
                order.completed_at = datetime.utcnow()
            
            # Create status history record
            history = OrderStatusHistory(
                order_id=order_id,
                status=status,
                notes=notes,
                changed_by=user_id
            )
            
            db.session.add(history)
            db.session.commit()
            
            logger.info(f"Order {order_id} status updated: {old_status} -> {status}")
            
            # Send notification (async in production)
            try:
                NotificationService.send_order_status_notification(order_id, status)
            except Exception as e:
                logger.warning(f"Failed to send notification: {str(e)}")
            
            return order.to_dict()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating order status: {str(e)}")
            raise
    
    @staticmethod
    def get_order_timeline(order_id):
        """
        Get order status history timeline
        
        Args:
            order_id: Order ID
        
        Returns:
            Dictionary with order and timeline
        """
        try:
            order = Order.query.get(order_id)
            if not order:
                raise ValueError("Order not found")
            
            # Get status history
            history = OrderStatusHistory.query.filter_by(order_id=order_id)\
                                             .order_by(OrderStatusHistory.created_at.asc())\
                                             .all()
            
            return {
                'order_id': order.id,
                'order_number': order.order_number,
                'current_status': order.status,
                'estimated_completion': order.estimated_completion.isoformat() if order.estimated_completion else None,
                'completed_at': order.completed_at.isoformat() if order.completed_at else None,
                'timeline': [h.to_dict() for h in history]
            }
            
        except Exception as e:
            logger.error(f"Error getting order timeline: {str(e)}")
            raise
    
    @staticmethod
    def estimate_completion_time(order_id):
        """
        Estimate order completion time
        
        Args:
            order_id: Order ID
        
        Returns:
            Estimated completion datetime
        """
        try:
            order = Order.query.get(order_id)
            if not order:
                raise ValueError("Order not found")
            
            # If already set, return it
            if order.estimated_completion:
                return order.estimated_completion
            
            # Calculate based on order items
            total_prep_time = 0
            for item in order.order_items:
                if item.product.preparation_time:
                    total_prep_time += item.product.preparation_time * item.quantity
            
            # Default to 20 minutes if no prep time data
            if total_prep_time == 0:
                total_prep_time = 20
            
            # Add buffer time
            buffer = 10  # minutes
            estimated = order.created_at + timedelta(minutes=total_prep_time + buffer)
            
            # Update order
            order.estimated_completion = estimated
            db.session.commit()
            
            return estimated
            
        except Exception as e:
            logger.error(f"Error estimating completion time: {str(e)}")
            raise
    
    @staticmethod
    def get_orders_by_status(status):
        """
        Get all orders with specific status
        
        Args:
            status: Order status
        
        Returns:
            List of orders
        """
        try:
            orders = Order.query.filter_by(status=status)\
                               .order_by(Order.created_at.desc())\
                               .all()
            
            return [order.to_dict() for order in orders]
            
        except Exception as e:
            logger.error(f"Error getting orders by status: {str(e)}")
            raise
    
    @staticmethod
    def track_order(order_number):
        """
        Public order tracking (for guest orders)
        
        Args:
            order_number: Order number
        
        Returns:
            Order tracking information
        """
        try:
            order = Order.query.filter_by(order_number=order_number).first()
            if not order:
                raise ValueError("Order not found")
            
            # Get latest status update
            latest_history = OrderStatusHistory.query.filter_by(order_id=order.id)\
                                                    .order_by(OrderStatusHistory.created_at.desc())\
                                                    .first()
            
            return {
                'order_number': order.order_number,
                'status': order.status,
                'order_type': order.order_type,
                'total_amount': float(order.total_amount),
                'created_at': order.created_at.isoformat(),
                'estimated_completion': order.estimated_completion.isoformat() if order.estimated_completion else None,
                'last_update': latest_history.to_dict() if latest_history else None
            }
            
        except Exception as e:
            logger.error(f"Error tracking order: {str(e)}")
            raise
