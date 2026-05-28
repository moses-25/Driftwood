"""
Inventory Service
Business logic for inventory management
"""

from extensions import db
from models.product import Product
from models.stock_adjustment import StockAdjustment
from sqlalchemy import and_
import logging

logger = logging.getLogger(__name__)


class InventoryService:
    """Service for inventory management operations"""
    
    @staticmethod
    def get_stock_level(product_id):
        """
        Get current stock level for a product
        
        Args:
            product_id: Product ID
        
        Returns:
            Dictionary with stock information
        """
        try:
            product = Product.query.get(product_id)
            if not product:
                raise ValueError("Product not found")
            
            return {
                'product_id': product.id,
                'name': product.name,
                'stock_quantity': product.stock_quantity,
                'low_stock_threshold': product.low_stock_threshold,
                'track_inventory': product.track_inventory,
                'is_low_stock': product.is_low_stock(),
                'status': 'out_of_stock' if product.stock_quantity == 0 else ('low_stock' if product.is_low_stock() else 'in_stock')
            }
            
        except Exception as e:
            logger.error(f"Error getting stock level: {str(e)}")
            raise
    
    @staticmethod
    def adjust_stock(product_id, quantity_change, reason, user_id=None, adjustment_type='manual', reference_id=None):
        """
        Manually adjust stock level
        
        Args:
            product_id: Product ID
            quantity_change: Amount to change (+/-)
            reason: Reason for adjustment
            user_id: User making the adjustment
            adjustment_type: Type of adjustment
            reference_id: Reference ID (e.g., order number)
        
        Returns:
            Updated stock information
        """
        try:
            product = Product.query.get(product_id)
            if not product:
                raise ValueError("Product not found")
            
            # Update stock
            new_quantity = product.stock_quantity + quantity_change
            if new_quantity < 0:
                raise ValueError("Stock cannot be negative")
            
            product.stock_quantity = new_quantity
            
            # Create adjustment record
            adjustment = StockAdjustment(
                product_id=product_id,
                quantity_change=quantity_change,
                reason=reason,
                adjustment_type=adjustment_type,
                reference_id=reference_id,
                adjusted_by=user_id
            )
            
            db.session.add(adjustment)
            db.session.commit()
            
            logger.info(f"Stock adjusted for product {product_id}: {quantity_change:+d} ({reason})")
            
            return InventoryService.get_stock_level(product_id)
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adjusting stock: {str(e)}")
            raise
    
    @staticmethod
    def deduct_stock(product_id, quantity, order_id=None):
        """
        Deduct stock for an order
        
        Args:
            product_id: Product ID
            quantity: Quantity to deduct
            order_id: Order ID reference
        
        Returns:
            Updated stock information
        """
        try:
            return InventoryService.adjust_stock(
                product_id=product_id,
                quantity_change=-quantity,
                reason=f"Order #{order_id} completed" if order_id else "Order completed",
                adjustment_type='order',
                reference_id=str(order_id) if order_id else None
            )
            
        except Exception as e:
            logger.error(f"Error deducting stock: {str(e)}")
            raise
    
    @staticmethod
    def get_low_stock_products(threshold=None):
        """
        Get products with low stock
        
        Args:
            threshold: Custom threshold (optional)
        
        Returns:
            List of low stock products
        """
        try:
            if threshold is not None:
                products = Product.query.filter(
                    and_(
                        Product.track_inventory == True,
                        Product.stock_quantity <= threshold
                    )
                ).all()
            else:
                # Use each product's own threshold
                products = Product.query.filter(
                    and_(
                        Product.track_inventory == True,
                        Product.stock_quantity <= Product.low_stock_threshold
                    )
                ).all()
            
            return [
                {
                    'id': p.id,
                    'name': p.name,
                    'stock_quantity': p.stock_quantity,
                    'low_stock_threshold': p.low_stock_threshold,
                    'category': p.category.name if p.category else None
                }
                for p in products
            ]
            
        except Exception as e:
            logger.error(f"Error getting low stock products: {str(e)}")
            raise
    
    @staticmethod
    def get_out_of_stock_products():
        """
        Get products that are out of stock
        
        Returns:
            List of out of stock products
        """
        try:
            products = Product.query.filter(
                and_(
                    Product.track_inventory == True,
                    Product.stock_quantity == 0
                )
            ).all()
            
            return [
                {
                    'id': p.id,
                    'name': p.name,
                    'category': p.category.name if p.category else None,
                    'last_updated': p.updated_at.isoformat() if p.updated_at else None
                }
                for p in products
            ]
            
        except Exception as e:
            logger.error(f"Error getting out of stock products: {str(e)}")
            raise
    
    @staticmethod
    def get_stock_history(product_id, limit=50):
        """
        Get stock adjustment history for a product
        
        Args:
            product_id: Product ID
            limit: Maximum number of records
        
        Returns:
            List of stock adjustments
        """
        try:
            product = Product.query.get(product_id)
            if not product:
                raise ValueError("Product not found")
            
            adjustments = StockAdjustment.query.filter_by(product_id=product_id)\
                                              .order_by(StockAdjustment.created_at.desc())\
                                              .limit(limit)\
                                              .all()
            
            return [adj.to_dict() for adj in adjustments]
            
        except Exception as e:
            logger.error(f"Error getting stock history: {str(e)}")
            raise
    
    @staticmethod
    def check_stock_availability(product_id, quantity):
        """
        Check if sufficient stock is available
        
        Args:
            product_id: Product ID
            quantity: Required quantity
        
        Returns:
            Boolean indicating availability
        """
        try:
            product = Product.query.get(product_id)
            if not product:
                raise ValueError("Product not found")
            
            # If inventory tracking is disabled, always available
            if not product.track_inventory:
                return True
            
            return product.stock_quantity >= quantity
            
        except Exception as e:
            logger.error(f"Error checking stock availability: {str(e)}")
            raise
    
    @staticmethod
    def bulk_update_stock(updates, user_id=None):
        """
        Update stock for multiple products
        
        Args:
            updates: List of dicts with product_id, quantity_change, reason
            user_id: User making the updates
        
        Returns:
            Summary of updates
        """
        try:
            results = {
                'success': [],
                'failed': []
            }
            
            for update in updates:
                try:
                    product_id = update.get('product_id')
                    quantity_change = update.get('quantity_change')
                    reason = update.get('reason', 'Bulk update')
                    
                    if not product_id or quantity_change is None:
                        results['failed'].append({
                            'product_id': product_id,
                            'error': 'Missing required fields'
                        })
                        continue
                    
                    result = InventoryService.adjust_stock(
                        product_id=product_id,
                        quantity_change=quantity_change,
                        reason=reason,
                        user_id=user_id,
                        adjustment_type='bulk'
                    )
                    
                    results['success'].append(result)
                    
                except Exception as e:
                    results['failed'].append({
                        'product_id': update.get('product_id'),
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in bulk stock update: {str(e)}")
            raise
    
    @staticmethod
    def get_all_products_stock():
        """
        Get stock information for all products
        
        Returns:
            List of products with stock info
        """
        try:
            products = Product.query.filter_by(track_inventory=True).all()
            
            return [
                {
                    'id': p.id,
                    'name': p.name,
                    'stock_quantity': p.stock_quantity,
                    'low_stock_threshold': p.low_stock_threshold,
                    'is_low_stock': p.is_low_stock(),
                    'status': 'out_of_stock' if p.stock_quantity == 0 else ('low_stock' if p.is_low_stock() else 'in_stock'),
                    'category': p.category.name if p.category else None
                }
                for p in products
            ]
            
        except Exception as e:
            logger.error(f"Error getting all products stock: {str(e)}")
            raise
