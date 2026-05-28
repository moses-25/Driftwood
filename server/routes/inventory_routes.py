"""
Inventory Routes
API endpoints for inventory management
"""

from flask import Blueprint, request, jsonify
from services.inventory_service import InventoryService
from utils.decorators import jwt_required, role_required
from utils.response_formatter import success_response, error_response
from flask_jwt_extended import get_jwt_identity
import logging

logger = logging.getLogger(__name__)

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')


@inventory_bp.route('/products', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_all_products_stock():
    """Get stock information for all products"""
    try:
        products = InventoryService.get_all_products_stock()
        
        return success_response(
            data={'products': products, 'total': len(products)},
            message=f"Retrieved stock for {len(products)} products"
        )
        
    except Exception as e:
        logger.error(f"Error getting products stock: {str(e)}")
        return error_response("Failed to get products stock", 500)


@inventory_bp.route('/product/<int:product_id>', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_product_stock(product_id):
    """Get stock information for a specific product"""
    try:
        stock_info = InventoryService.get_stock_level(product_id)
        
        return success_response(
            data=stock_info,
            message="Stock information retrieved successfully"
        )
        
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        logger.error(f"Error getting product stock: {str(e)}")
        return error_response("Failed to get product stock", 500)


@inventory_bp.route('/adjust', methods=['POST'])
@jwt_required
@role_required(['admin', 'staff'])
def adjust_stock():
    """
    Manually adjust stock level
    Body: product_id, quantity_change, reason
    """
    try:
        data = request.get_json()
        
        # Validate input
        product_id = data.get('product_id')
        quantity_change = data.get('quantity_change')
        reason = data.get('reason')
        
        if not product_id or quantity_change is None or not reason:
            return error_response("Missing required fields: product_id, quantity_change, reason", 400)
        
        # Get current user
        current_user_id = get_jwt_identity()
        
        # Adjust stock
        result = InventoryService.adjust_stock(
            product_id=product_id,
            quantity_change=quantity_change,
            reason=reason,
            user_id=current_user_id,
            adjustment_type='manual'
        )
        
        return success_response(
            data=result,
            message="Stock adjusted successfully"
        )
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error adjusting stock: {str(e)}")
        return error_response("Failed to adjust stock", 500)


@inventory_bp.route('/low-stock', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_low_stock():
    """
    Get products with low stock
    Query params: threshold (optional)
    """
    try:
        threshold = request.args.get('threshold', type=int)
        
        products = InventoryService.get_low_stock_products(threshold)
        
        return success_response(
            data={'products': products, 'count': len(products)},
            message=f"Found {len(products)} low stock products"
        )
        
    except Exception as e:
        logger.error(f"Error getting low stock products: {str(e)}")
        return error_response("Failed to get low stock products", 500)


@inventory_bp.route('/out-of-stock', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_out_of_stock():
    """Get products that are out of stock"""
    try:
        products = InventoryService.get_out_of_stock_products()
        
        return success_response(
            data={'products': products, 'count': len(products)},
            message=f"Found {len(products)} out of stock products"
        )
        
    except Exception as e:
        logger.error(f"Error getting out of stock products: {str(e)}")
        return error_response("Failed to get out of stock products", 500)


@inventory_bp.route('/history/<int:product_id>', methods=['GET'])
@jwt_required
@role_required(['admin', 'staff'])
def get_stock_history(product_id):
    """
    Get stock adjustment history for a product
    Query params: limit (default: 50)
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        
        history = InventoryService.get_stock_history(product_id, limit)
        
        return success_response(
            data={'history': history, 'count': len(history)},
            message="Stock history retrieved successfully"
        )
        
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        logger.error(f"Error getting stock history: {str(e)}")
        return error_response("Failed to get stock history", 500)


@inventory_bp.route('/bulk-update', methods=['POST'])
@jwt_required
@role_required(['admin'])
def bulk_update_stock():
    """
    Bulk update stock for multiple products
    Body: updates (array of {product_id, quantity_change, reason})
    """
    try:
        data = request.get_json()
        updates = data.get('updates', [])
        
        if not updates:
            return error_response("No updates provided", 400)
        
        # Get current user
        current_user_id = get_jwt_identity()
        
        # Perform bulk update
        results = InventoryService.bulk_update_stock(updates, current_user_id)
        
        return success_response(
            data=results,
            message=f"Bulk update completed: {len(results['success'])} succeeded, {len(results['failed'])} failed"
        )
        
    except Exception as e:
        logger.error(f"Error in bulk stock update: {str(e)}")
        return error_response("Failed to perform bulk update", 500)


@inventory_bp.route('/check-availability/<int:product_id>', methods=['GET'])
@jwt_required
def check_availability(product_id):
    """
    Check if product has sufficient stock
    Query params: quantity
    """
    try:
        quantity = request.args.get('quantity', 1, type=int)
        
        available = InventoryService.check_stock_availability(product_id, quantity)
        
        return success_response(
            data={'available': available, 'product_id': product_id, 'quantity': quantity},
            message="Stock availability checked"
        )
        
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        logger.error(f"Error checking availability: {str(e)}")
        return error_response("Failed to check availability", 500)
