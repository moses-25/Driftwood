"""
Order service layer
Handles business logic for order management
"""
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.user import User
from extensions import db
from datetime import datetime, timedelta
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class OrderService:
    """Service class for order operations"""
    
    @staticmethod
    def validate_order_items(items):
        """
        Validate order items and check product availability
        
        Args:
            items: List of order items with product_id and quantity
            
        Returns:
            tuple: (is_valid, error_message, validated_items)
        """
        if not items or len(items) == 0:
            return False, "Order must contain at least one item", None
        
        validated_items = []
        
        for item in items:
            # Validate required fields
            if 'product_id' not in item or 'quantity' not in item:
                return False, "Each item must have product_id and quantity", None
            
            # Get product
            product = Product.query.get(item['product_id'])
            if not product:
                return False, f"Product with ID {item['product_id']} not found", None
            
            # Check availability
            if not product.is_available:
                return False, f"Product '{product.name}' is not available", None
            
            # Validate quantity
            try:
                quantity = int(item['quantity'])
                if quantity <= 0:
                    return False, "Quantity must be greater than 0", None
                if quantity > 100:  # Reasonable limit
                    return False, "Quantity cannot exceed 100 per item", None
            except (ValueError, TypeError):
                return False, "Invalid quantity format", None
            
            # Check stock (if stock tracking is enabled)
            if product.track_inventory:
                if product.stock_quantity <= 0:
                    return False, f"Product '{product.name}' is out of stock", None
                if quantity > product.stock_quantity:
                    return False, f"Insufficient stock for '{product.name}'. Available: {product.stock_quantity}", None
            
            validated_items.append({
                'product': product,
                'quantity': quantity,
                'unit_price': float(product.price),
                'customizations': item.get('customizations', {})
            })
        
        return True, None, validated_items

    
    @staticmethod
    def calculate_order_total(validated_items, delivery_fee=0):
        """
        Calculate order total from validated items
        
        Args:
            validated_items: List of validated order items
            delivery_fee: Delivery fee (default: 0)
            
        Returns:
            Decimal: Total order amount
        """
        subtotal = Decimal('0.00')
        
        for item in validated_items:
            item_total = Decimal(str(item['unit_price'])) * item['quantity']
            subtotal += item_total
        
        total = subtotal + Decimal(str(delivery_fee))
        return total
    
    @staticmethod
    def create_order(user_id, items, order_data):
        """
        Create a new order
        Supports both authenticated users and guest checkout
        
        Args:
            user_id: User ID (None for guest checkout)
            items: List of order items
            order_data: Dictionary containing order details
            
        Returns:
            tuple: (order_dict, error_message, status_code)
        """
        try:
            # Validate order items
            is_valid, error, validated_items = OrderService.validate_order_items(items)
            if not is_valid:
                return None, error, 400
            
            # Validate required fields
            required_fields = ['order_type', 'payment_method']
            for field in required_fields:
                if field not in order_data or not order_data[field]:
                    return None, f"{field} is required", 400
            
            # Validate order type
            if order_data['order_type'] not in ['pickup', 'delivery']:
                return None, "order_type must be 'pickup' or 'delivery'", 400
            
            # Validate payment method
            if order_data['payment_method'] not in ['mpesa', 'cash']:
                return None, "payment_method must be 'mpesa' or 'cash'", 400
            
            # For guest checkout, user_id can be None
            # For authenticated orders, verify user exists
            if user_id:
                user = User.query.get(user_id)
                if not user:
                    return None, "User not found", 404
            
            # Calculate delivery fee
            delivery_fee = Decimal('0.00')
            if order_data['order_type'] == 'delivery':
                delivery_fee = Decimal(str(order_data.get('delivery_fee', 0)))
            
            # Calculate total
            total_amount = OrderService.calculate_order_total(validated_items, delivery_fee)
            
            # Verify total matches (if provided)
            if order_data.get('total_amount') is not None:
                provided_total = Decimal(str(order_data['total_amount']))
                if abs(provided_total - total_amount) > Decimal('0.01'):
                    return None, f"Total amount mismatch. Expected: {total_amount}, Provided: {provided_total}", 400
            
            # Create order
            order = Order(
                user_id=user_id,
                total_amount=total_amount,
                order_type=order_data['order_type'],
                payment_method=order_data['payment_method'],
                delivery_address=order_data.get('delivery_address'),
                delivery_instructions=order_data.get('delivery_instructions'),
                delivery_fee=delivery_fee,
                estimated_ready_time=datetime.utcnow() + timedelta(minutes=20)  # Default 20 min
            )
            
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Create order items
            for item in validated_items:
                subtotal = Decimal(str(item['unit_price'])) * item['quantity']
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product'].id,
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    subtotal=subtotal
                )
                
                if item['customizations']:
                    order_item.set_customizations(item['customizations'])
                
                db.session.add(order_item)
            
            db.session.commit()
            
            return order.to_dict(), None, 201
            
        except Exception as e:
            db.session.rollback()
            return None, str(e), 500

    
    @staticmethod
    def get_order_by_id(order_id, user_id=None):
        """
        Get order by ID
        If user_id is provided, verify order belongs to user
        
        Args:
            order_id: The order's ID
            user_id: User ID for ownership verification (optional)
            
        Returns:
            tuple: (order_dict, error_message, status_code)
        """
        try:
            order = Order.query.get(order_id)
            
            if not order:
                return None, "Order not found", 404
            
            # Verify ownership if user_id provided
            if user_id and order.user_id != user_id:
                return None, "Access denied", 403
            
            return order.to_dict(), None, 200
            
        except Exception as e:
            return None, str(e), 500
    
    @staticmethod
    def get_order_by_number(order_number):
        """
        Get order by order number (for guest checkout tracking)
        
        Args:
            order_number: The order's unique number
            
        Returns:
            tuple: (order_dict, error_message, status_code)
        """
        try:
            order = Order.query.filter_by(order_number=order_number).first()
            
            if not order:
                return None, "Order not found", 404
            
            return order.to_dict(), None, 200
            
        except Exception as e:
            return None, str(e), 500
    
    @staticmethod
    def get_user_orders(user_id, page=1, per_page=20, status=None):
        """
        Get all orders for a specific user
        
        Args:
            user_id: The user's ID
            page: Page number for pagination
            per_page: Number of items per page
            status: Filter by order status (optional)
            
        Returns:
            tuple: (orders_list, pagination_info, error_message, status_code)
        """
        try:
            query = Order.query.filter_by(user_id=user_id)
            
            if status:
                query = query.filter_by(status=status)
            
            query = query.order_by(Order.created_at.desc())
            
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            
            orders_list = [order.to_dict() for order in paginated.items]
            
            pagination_info = {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev
            }
            
            return orders_list, pagination_info, None, 200
            
        except Exception as e:
            return None, None, str(e), 500

    
    @staticmethod
    def get_all_orders(page=1, per_page=20, status=None, order_type=None):
        """
        Get all orders (Admin/Staff only)
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            status: Filter by order status (optional)
            order_type: Filter by order type (optional)
            
        Returns:
            tuple: (orders_list, pagination_info, error_message, status_code)
        """
        try:
            query = Order.query
            
            if status:
                query = query.filter_by(status=status)
            
            if order_type:
                query = query.filter_by(order_type=order_type)
            
            query = query.order_by(Order.created_at.desc())
            
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            
            orders_list = [order.to_dict() for order in paginated.items]
            
            pagination_info = {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev
            }
            
            return orders_list, pagination_info, None, 200
            
        except Exception as e:
            return None, None, str(e), 500
    
    @staticmethod
    def update_order_status(order_id, new_status):
        """
        Update order status (Staff/Admin only)
        Automatically deducts stock when order is completed
        
        Args:
            order_id: The order's ID
            new_status: New status value
            
        Returns:
            tuple: (order_dict, error_message, status_code)
        """
        try:
            order = Order.query.get(order_id)
            
            if not order:
                return None, "Order not found", 404
            
            # Validate status
            valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']
            if new_status not in valid_statuses:
                return None, f"Invalid status. Must be one of: {', '.join(valid_statuses)}", 400
            
            old_status = order.status
            order.status = new_status
            
            # Deduct stock when order is completed
            if new_status == 'completed' and old_status != 'completed':
                from services.inventory_service import InventoryService
                
                for item in order.order_items:
                    product = item.product
                    
                    # Only deduct if inventory tracking is enabled
                    if product.track_inventory:
                        try:
                            InventoryService.deduct_stock(
                                product_id=product.id,
                                quantity=item.quantity,
                                order_id=order.id
                            )
                            logger.info(f"Stock deducted for product {product.id}: -{item.quantity}")
                        except Exception as e:
                            # Log warning but don't fail the order
                            logger.warning(f"Failed to deduct stock for product {product.id}: {str(e)}")
            
            db.session.commit()
            
            return order.to_dict(), None, 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating order status: {str(e)}")
            return None, str(e), 500
    
    @staticmethod
    def cancel_order(order_id, user_id=None):
        """
        Cancel an order
        Users can cancel their own orders, admins can cancel any order
        
        Args:
            order_id: The order's ID
            user_id: User ID for ownership verification (None for admin)
            
        Returns:
            tuple: (order_dict, error_message, status_code)
        """
        try:
            order = Order.query.get(order_id)
            
            if not order:
                return None, "Order not found", 404
            
            # Verify ownership if user_id provided
            if user_id and order.user_id != user_id:
                return None, "Access denied", 403
            
            # Check if order can be cancelled
            if order.status in ['completed', 'cancelled']:
                return None, f"Cannot cancel order with status '{order.status}'", 400
            
            order.status = 'cancelled'
            db.session.commit()
            
            return order.to_dict(), None, 200
            
        except Exception as e:
            db.session.rollback()
            return None, str(e), 500
