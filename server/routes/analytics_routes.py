"""
Analytics Routes
API endpoints for analytics and reporting
"""

from flask import Blueprint, request, jsonify
from services.analytics_service import AnalyticsService
from utils.decorators import jwt_required, role_required
from utils.response_formatter import success_response, error_response
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/sales', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_sales_report():
    """
    Get sales report
    Query params: start_date, end_date (ISO format)
    """
    try:
        # Parse date parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get report
        report = AnalyticsService.get_sales_report(start_date, end_date)
        
        return success_response(
            data=report,
            message="Sales report generated successfully"
        )
        
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error getting sales report: {str(e)}")
        return error_response("Failed to generate sales report", 500)


@analytics_bp.route('/popular-products', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_popular_products():
    """
    Get popular products
    Query params: limit, start_date, end_date
    """
    try:
        # Parse parameters
        limit = request.args.get('limit', 10, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get products
        products = AnalyticsService.get_popular_products(limit, start_date, end_date)
        
        return success_response(
            data={'products': products},
            message=f"Top {len(products)} popular products retrieved"
        )
        
    except ValueError as e:
        return error_response(f"Invalid parameter: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error getting popular products: {str(e)}")
        return error_response("Failed to get popular products", 500)


@analytics_bp.route('/customers', methods=['GET'])
@jwt_required
@role_required(['admin'])
def get_customer_analytics():
    """
    Get customer analytics
    Query params: start_date, end_date
    """
    try:
        # Parse date parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get analytics
        analytics = AnalyticsService.get_customer_analytics(start_date, end_date)
        
        return success_response(
            data=analytics,
            message="Customer analytics retrieved successfully"
        )
        
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error getting customer analytics: {str(e)}")
        return error_response("Failed to get customer analytics", 500)


@analytics_bp.route('/orders', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_order_statistics():
    """
    Get order statistics
    Query params: start_date, end_date
    """
    try:
        # Parse date parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get statistics
        stats = AnalyticsService.get_order_statistics(start_date, end_date)
        
        return success_response(
            data=stats,
            message="Order statistics retrieved successfully"
        )
        
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error getting order statistics: {str(e)}")
        return error_response("Failed to get order statistics", 500)


@analytics_bp.route('/categories', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_category_performance():
    """
    Get category performance
    Query params: start_date, end_date
    """
    try:
        # Parse date parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get performance
        performance = AnalyticsService.get_category_performance(start_date, end_date)
        
        return success_response(
            data={'categories': performance},
            message="Category performance retrieved successfully"
        )
        
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error getting category performance: {str(e)}")
        return error_response("Failed to get category performance", 500)


@analytics_bp.route('/revenue-trends', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_revenue_trends():
    """
    Get revenue trends
    Query params: period (day/week/month), start_date, end_date
    """
    try:
        # Parse parameters
        period = request.args.get('period', 'day')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if period not in ['day', 'week', 'month']:
            return error_response("Invalid period. Must be 'day', 'week', or 'month'", 400)
        
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get trends
        trends = AnalyticsService.get_revenue_trends(period, start_date, end_date)
        
        return success_response(
            data={'trends': trends, 'period': period},
            message="Revenue trends retrieved successfully"
        )
        
    except ValueError as e:
        return error_response(f"Invalid parameter: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error getting revenue trends: {str(e)}")
        return error_response("Failed to get revenue trends", 500)


@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_dashboard():
    """
    Get dashboard summary
    Query params: start_date, end_date
    """
    try:
        # Parse date parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get dashboard data
        dashboard = AnalyticsService.get_dashboard_summary(start_date, end_date)
        
        return success_response(
            data=dashboard,
            message="Dashboard data retrieved successfully"
        )
        
    except ValueError as e:
        return error_response(f"Invalid date format: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error getting dashboard: {str(e)}")
        return error_response("Failed to get dashboard data", 500)
