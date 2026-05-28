"""
Analytics Service
Business logic for analytics and reporting
"""

from extensions import db
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.category import Category
from models.user import User
from models.payment import Payment
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from utils.report_utils import calculate_growth_rate, safe_divide, calculate_percentage
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for analytics and reporting operations"""
    
    @staticmethod
    def get_sales_report(start_date=None, end_date=None):
        """
        Get sales report for date range
        
        Args:
            start_date: Start date (default: 30 days ago)
            end_date: End date (default: today)
        
        Returns:
            Dictionary with sales data
        """
        try:
            # Default date range: last 30 days
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)
            
            # Query orders in date range
            orders = Order.query.filter(
                and_(
                    Order.created_at >= start_date,
                    Order.created_at <= end_date,
                    Order.status.in_(['completed', 'confirmed', 'preparing', 'ready'])
                )
            ).all()
            
            # Calculate metrics
            total_orders = len(orders)
            total_revenue = sum(float(order.total_amount) for order in orders)
            completed_orders = len([o for o in orders if o.status == 'completed'])
            cancelled_orders = Order.query.filter(
                and_(
                    Order.created_at >= start_date,
                    Order.created_at <= end_date,
                    Order.status == 'cancelled'
                )
            ).count()
            
            average_order_value = safe_divide(total_revenue, total_orders)
            
            # Previous period comparison
            period_days = (end_date - start_date).days
            prev_start = start_date - timedelta(days=period_days)
            prev_end = start_date
            
            prev_orders = Order.query.filter(
                and_(
                    Order.created_at >= prev_start,
                    Order.created_at <= prev_end,
                    Order.status.in_(['completed', 'confirmed', 'preparing', 'ready'])
                )
            ).all()
            
            prev_revenue = sum(float(order.total_amount) for order in prev_orders)
            revenue_growth = calculate_growth_rate(total_revenue, prev_revenue)
            
            return {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'revenue': {
                    'total': round(total_revenue, 2),
                    'average_order_value': average_order_value,
                    'growth_rate': revenue_growth,
                    'previous_period': round(prev_revenue, 2)
                },
                'orders': {
                    'total': total_orders,
                    'completed': completed_orders,
                    'cancelled': cancelled_orders,
                    'completion_rate': calculate_percentage(completed_orders, total_orders)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating sales report: {str(e)}")
            raise
    
    @staticmethod
    def get_popular_products(limit=10, start_date=None, end_date=None):
        """
        Get popular products by sales
        
        Args:
            limit: Number of products to return
            start_date: Start date filter
            end_date: End date filter
        
        Returns:
            List of popular products
        """
        try:
            # Build query
            query = db.session.query(
                Product.id,
                Product.name,
                Product.price,
                func.sum(OrderItem.quantity).label('sales_count'),
                func.sum(OrderItem.subtotal).label('revenue')
            ).join(OrderItem).join(Order)
            
            # Apply date filters
            if start_date:
                query = query.filter(Order.created_at >= start_date)
            if end_date:
                query = query.filter(Order.created_at <= end_date)
            
            # Filter completed orders
            query = query.filter(Order.status.in_(['completed', 'confirmed', 'preparing', 'ready']))
            
            # Group and order
            products = query.group_by(Product.id, Product.name, Product.price)\
                           .order_by(func.sum(OrderItem.quantity).desc())\
                           .limit(limit)\
                           .all()
            
            return [
                {
                    'id': p.id,
                    'name': p.name,
                    'price': float(p.price),
                    'sales_count': int(p.sales_count),
                    'revenue': float(p.revenue)
                }
                for p in products
            ]
            
        except Exception as e:
            logger.error(f"Error getting popular products: {str(e)}")
            raise
    
    @staticmethod
    def get_customer_analytics(start_date=None, end_date=None):
        """
        Get customer analytics
        
        Args:
            start_date: Start date filter
            end_date: End date filter
        
        Returns:
            Dictionary with customer insights
        """
        try:
            # Total customers
            total_customers = User.query.filter_by(role='customer').count()
            
            # New customers in period
            query = User.query.filter_by(role='customer')
            if start_date:
                query = query.filter(User.created_at >= start_date)
            if end_date:
                query = query.filter(User.created_at <= end_date)
            new_customers = query.count()
            
            # Customers with orders
            customers_with_orders = db.session.query(func.count(func.distinct(Order.user_id)))\
                .filter(Order.user_id.isnot(None))
            
            if start_date:
                customers_with_orders = customers_with_orders.filter(Order.created_at >= start_date)
            if end_date:
                customers_with_orders = customers_with_orders.filter(Order.created_at <= end_date)
            
            active_customers = customers_with_orders.scalar() or 0
            
            # Top customers by revenue
            top_customers = db.session.query(
                User.id,
                User.username,
                User.email,
                func.count(Order.id).label('order_count'),
                func.sum(Order.total_amount).label('total_spent')
            ).join(Order).filter(User.role == 'customer')
            
            if start_date:
                top_customers = top_customers.filter(Order.created_at >= start_date)
            if end_date:
                top_customers = top_customers.filter(Order.created_at <= end_date)
            
            top_customers = top_customers.group_by(User.id, User.username, User.email)\
                                       .order_by(func.sum(Order.total_amount).desc())\
                                       .limit(10)\
                                       .all()
            
            return {
                'total_customers': total_customers,
                'new_customers': new_customers,
                'active_customers': active_customers,
                'engagement_rate': calculate_percentage(active_customers, total_customers),
                'top_customers': [
                    {
                        'id': c.id,
                        'username': c.username,
                        'email': c.email,
                        'order_count': int(c.order_count),
                        'total_spent': float(c.total_spent)
                    }
                    for c in top_customers
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting customer analytics: {str(e)}")
            raise
    
    @staticmethod
    def get_order_statistics(start_date=None, end_date=None):
        """
        Get order statistics
        
        Args:
            start_date: Start date filter
            end_date: End date filter
        
        Returns:
            Dictionary with order metrics
        """
        try:
            # Build query
            query = Order.query
            
            if start_date:
                query = query.filter(Order.created_at >= start_date)
            if end_date:
                query = query.filter(Order.created_at <= end_date)
            
            # Status breakdown
            status_counts = {}
            for status in ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']:
                count = query.filter_by(status=status).count()
                status_counts[status] = count
            
            # Order type breakdown
            pickup_orders = query.filter_by(order_type='pickup').count()
            delivery_orders = query.filter_by(order_type='delivery').count()
            
            # Payment method breakdown
            mpesa_orders = query.filter_by(payment_method='mpesa').count()
            cash_orders = query.filter_by(payment_method='cash').count()
            
            # Average order value
            completed_orders = query.filter(Order.status.in_(['completed', 'confirmed', 'preparing', 'ready'])).all()
            total_revenue = sum(float(o.total_amount) for o in completed_orders)
            avg_order_value = safe_divide(total_revenue, len(completed_orders))
            
            return {
                'status_breakdown': status_counts,
                'order_type': {
                    'pickup': pickup_orders,
                    'delivery': delivery_orders
                },
                'payment_method': {
                    'mpesa': mpesa_orders,
                    'cash': cash_orders
                },
                'metrics': {
                    'total_orders': query.count(),
                    'average_order_value': avg_order_value,
                    'total_revenue': round(total_revenue, 2)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting order statistics: {str(e)}")
            raise
    
    @staticmethod
    def get_category_performance(start_date=None, end_date=None):
        """
        Get category performance analysis
        
        Args:
            start_date: Start date filter
            end_date: End date filter
        
        Returns:
            List of category performance data
        """
        try:
            # Query category sales
            query = db.session.query(
                Category.id,
                Category.name,
                func.count(OrderItem.id).label('items_sold'),
                func.sum(OrderItem.subtotal).label('revenue')
            ).join(Product).join(OrderItem).join(Order)
            
            # Apply filters
            if start_date:
                query = query.filter(Order.created_at >= start_date)
            if end_date:
                query = query.filter(Order.created_at <= end_date)
            
            query = query.filter(Order.status.in_(['completed', 'confirmed', 'preparing', 'ready']))
            
            categories = query.group_by(Category.id, Category.name)\
                            .order_by(func.sum(OrderItem.subtotal).desc())\
                            .all()
            
            total_revenue = sum(float(c.revenue) for c in categories)
            
            return [
                {
                    'id': c.id,
                    'name': c.name,
                    'items_sold': int(c.items_sold),
                    'revenue': float(c.revenue),
                    'revenue_percentage': calculate_percentage(float(c.revenue), total_revenue)
                }
                for c in categories
            ]
            
        except Exception as e:
            logger.error(f"Error getting category performance: {str(e)}")
            raise
    
    @staticmethod
    def get_revenue_trends(period='day', start_date=None, end_date=None):
        """
        Get revenue trends over time
        
        Args:
            period: Period type ('day', 'week', 'month')
            start_date: Start date
            end_date: End date
        
        Returns:
            List of revenue data points
        """
        try:
            # Default date range
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                if period == 'day':
                    start_date = end_date - timedelta(days=30)
                elif period == 'week':
                    start_date = end_date - timedelta(weeks=12)
                else:  # month
                    start_date = end_date - timedelta(days=365)
            
            # Query orders
            orders = Order.query.filter(
                and_(
                    Order.created_at >= start_date,
                    Order.created_at <= end_date,
                    Order.status.in_(['completed', 'confirmed', 'preparing', 'ready'])
                )
            ).all()
            
            # Group by period
            trends = {}
            for order in orders:
                if period == 'day':
                    key = order.created_at.strftime('%Y-%m-%d')
                elif period == 'week':
                    key = order.created_at.strftime('%Y-W%W')
                else:  # month
                    key = order.created_at.strftime('%Y-%m')
                
                if key not in trends:
                    trends[key] = {'revenue': 0, 'orders': 0}
                
                trends[key]['revenue'] += float(order.total_amount)
                trends[key]['orders'] += 1
            
            # Convert to list
            result = [
                {
                    'period': key,
                    'revenue': round(data['revenue'], 2),
                    'orders': data['orders'],
                    'average_order_value': safe_divide(data['revenue'], data['orders'])
                }
                for key, data in sorted(trends.items())
            ]
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting revenue trends: {str(e)}")
            raise
    
    @staticmethod
    def get_dashboard_summary(start_date=None, end_date=None):
        """
        Get dashboard summary with key metrics
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            Dictionary with dashboard data
        """
        try:
            sales_report = AnalyticsService.get_sales_report(start_date, end_date)
            popular_products = AnalyticsService.get_popular_products(5, start_date, end_date)
            customer_analytics = AnalyticsService.get_customer_analytics(start_date, end_date)
            order_stats = AnalyticsService.get_order_statistics(start_date, end_date)
            
            return {
                'sales': sales_report,
                'popular_products': popular_products,
                'customers': customer_analytics,
                'orders': order_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard summary: {str(e)}")
            raise
