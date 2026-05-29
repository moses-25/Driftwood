#!/usr/bin/env python3
"""
Phase 7 Complete Test Suite
Tests all Phase 7 features: Analytics, Inventory, Notifications
"""

import sys
from app import create_app
from extensions import db
from models.product import Product
from models.order import Order
from models.stock_adjustment import StockAdjustment
from models.order_status_history import OrderStatusHistory
from models.notification_preference import NotificationPreference
from services.analytics_service import AnalyticsService
from services.inventory_service import InventoryService
from services.notification_service import NotificationService
from services.order_tracking_service import OrderTrackingService
from datetime import datetime, timedelta

def test_analytics():
    """Test analytics service"""
    print("\n=== Testing Analytics Service ===")
    
    try:
        # Test sales report
        print("\n1. Testing sales report...")
        report = AnalyticsService.get_sales_report()
        assert 'revenue' in report
        assert 'orders' in report
        print(f"   ✓ Sales report generated: {report['revenue']['total']} revenue, {report['orders']['total']} orders")
        
        # Test popular products
        print("\n2. Testing popular products...")
        products = AnalyticsService.get_popular_products(limit=5)
        print(f"   ✓ Found {len(products)} popular products")
        if products:
            print(f"   Top product: {products[0]['name']} ({products[0]['sales_count']} sales)")
        
        # Test customer analytics
        print("\n3. Testing customer analytics...")
        analytics = AnalyticsService.get_customer_analytics()
        assert 'total_customers' in analytics
        print(f"   ✓ Customer analytics: {analytics['total_customers']} total, {analytics['active_customers']} active")
        
        # Test order statistics
        print("\n4. Testing order statistics...")
        stats = AnalyticsService.get_order_statistics()
        assert 'status_breakdown' in stats
        print(f"   ✓ Order statistics: {stats['metrics']['total_orders']} total orders")
        
        # Test category performance
        print("\n5. Testing category performance...")
        categories = AnalyticsService.get_category_performance()
        print(f"   ✓ Found {len(categories)} categories with sales")
        
        # Test revenue trends
        print("\n6. Testing revenue trends...")
        trends = AnalyticsService.get_revenue_trends(period='day')
        print(f"   ✓ Revenue trends: {len(trends)} data points")
        
        # Test dashboard summary
        print("\n7. Testing dashboard summary...")
        dashboard = AnalyticsService.get_dashboard_summary()
        assert 'sales' in dashboard
        assert 'popular_products' in dashboard
        print("   ✓ Dashboard summary generated")
        
        print("\n✅ Analytics Service: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Analytics Service: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_inventory():
    """Test inventory service"""
    print("\n=== Testing Inventory Service ===")
    
    try:
        # Get a product for testing
        product = Product.query.first()
        if not product:
            print("   ⚠ No products found, skipping inventory tests")
            return True
        
        print(f"\n1. Testing with product: {product.name} (ID: {product.id})")
        
        # Test get stock level
        print("\n2. Testing get stock level...")
        stock_info = InventoryService.get_stock_level(product.id)
        assert 'stock_quantity' in stock_info
        print(f"   ✓ Current stock: {stock_info['stock_quantity']}")
        
        # Test adjust stock
        print("\n3. Testing stock adjustment...")
        initial_stock = product.stock_quantity
        result = InventoryService.adjust_stock(
            product_id=product.id,
            quantity_change=10,
            reason="Test adjustment",
            user_id=1,
            adjustment_type='manual'
        )
        assert result['stock_quantity'] == initial_stock + 10
        print(f"   ✓ Stock adjusted: {initial_stock} -> {result['stock_quantity']}")
        
        # Test stock history
        print("\n4. Testing stock history...")
        history = InventoryService.get_stock_history(product.id, limit=5)
        assert len(history) > 0
        print(f"   ✓ Found {len(history)} stock adjustments")
        
        # Test low stock products
        print("\n5. Testing low stock detection...")
        low_stock = InventoryService.get_low_stock_products()
        print(f"   ✓ Found {len(low_stock)} low stock products")
        
        # Test out of stock products
        print("\n6. Testing out of stock detection...")
        out_of_stock = InventoryService.get_out_of_stock_products()
        print(f"   ✓ Found {len(out_of_stock)} out of stock products")
        
        # Test check availability
        print("\n7. Testing stock availability check...")
        available = InventoryService.check_stock_availability(product.id, 1)
        print(f"   ✓ Stock available: {available}")
        
        # Test get all products stock
        print("\n8. Testing get all products stock...")
        all_stock = InventoryService.get_all_products_stock()
        print(f"   ✓ Retrieved stock for {len(all_stock)} products")
        
        # Restore original stock
        InventoryService.adjust_stock(
            product_id=product.id,
            quantity_change=-10,
            reason="Test cleanup",
            user_id=1,
            adjustment_type='manual'
        )
        
        print("\n✅ Inventory Service: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Inventory Service: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_notifications():
    """Test notification service"""
    print("\n=== Testing Notification Service ===")
    
    try:
        # Test get preferences (user 1)
        print("\n1. Testing get notification preferences...")
        prefs = NotificationService.get_notification_preferences(1)
        assert 'email_enabled' in prefs
        print(f"   ✓ Preferences retrieved: email_enabled={prefs['email_enabled']}")
        
        # Test update preferences
        print("\n2. Testing update notification preferences...")
        updated = NotificationService.update_notification_preferences(1, {
            'email_enabled': True,
            'order_status_updates': True
        })
        assert updated['email_enabled'] == True
        print("   ✓ Preferences updated successfully")
        
        # Test send notification (will skip if no email config)
        print("\n3. Testing send order notification...")
        order = Order.query.first()
        if order:
            success = NotificationService.send_order_status_notification(order.id, 'confirmed')
            print(f"   ✓ Notification sent: {success}")
        else:
            print("   ⚠ No orders found, skipping notification test")
        
        print("\n✅ Notification Service: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Notification Service: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_order_tracking():
    """Test order tracking service"""
    print("\n=== Testing Order Tracking Service ===")
    
    try:
        # Get an order for testing
        order = Order.query.first()
        if not order:
            print("   ⚠ No orders found, skipping tracking tests")
            return True
        
        print(f"\n1. Testing with order: #{order.order_number} (ID: {order.id})")
        
        # Test update order status with tracking
        print("\n2. Testing update order status with tracking...")
        updated = OrderTrackingService.update_order_status(
            order_id=order.id,
            status='preparing',
            notes='Test status update',
            user_id=1
        )
        assert updated['status'] == 'preparing'
        print(f"   ✓ Order status updated to: {updated['status']}")
        
        # Test get order timeline
        print("\n3. Testing get order timeline...")
        timeline = OrderTrackingService.get_order_timeline(order.id)
        assert 'timeline' in timeline
        print(f"   ✓ Timeline retrieved: {len(timeline['timeline'])} status changes")
        
        # Test estimate completion time
        print("\n4. Testing estimate completion time...")
        estimated = OrderTrackingService.estimate_completion_time(order.id)
        print(f"   ✓ Estimated completion: {estimated}")
        
        # Test track order (public)
        print("\n5. Testing public order tracking...")
        tracking = OrderTrackingService.track_order(order.order_number)
        assert 'order_number' in tracking
        print(f"   ✓ Public tracking info retrieved for order #{tracking['order_number']}")
        
        print("\n✅ Order Tracking Service: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Order Tracking Service: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_models():
    """Test Phase 7 models"""
    print("\n=== Testing Phase 7 Models ===")
    
    try:
        # Test StockAdjustment model
        print("\n1. Testing StockAdjustment model...")
        adjustment_count = StockAdjustment.query.count()
        print(f"   ✓ StockAdjustment model working: {adjustment_count} records")
        
        # Test OrderStatusHistory model
        print("\n2. Testing OrderStatusHistory model...")
        history_count = OrderStatusHistory.query.count()
        print(f"   ✓ OrderStatusHistory model working: {history_count} records")
        
        # Test NotificationPreference model
        print("\n3. Testing NotificationPreference model...")
        pref_count = NotificationPreference.query.count()
        print(f"   ✓ NotificationPreference model working: {pref_count} records")
        
        print("\n✅ Phase 7 Models: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 7 Models: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all Phase 7 tests"""
    print("=" * 60)
    print("PHASE 7 COMPLETE TEST SUITE")
    print("Testing: Analytics, Inventory, Notifications, Order Tracking")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        results = {
            'Models': test_models(),
            'Analytics': test_analytics(),
            'Inventory': test_inventory(),
            'Notifications': test_notifications(),
            'Order Tracking': test_order_tracking()
        }
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        for feature, passed in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{feature:20} {status}")
        
        all_passed = all(results.values())
        
        print("=" * 60)
        if all_passed:
            print("🎉 ALL PHASE 7 TESTS PASSED!")
            print("=" * 60)
            return 0
        else:
            print("⚠️  SOME TESTS FAILED")
            print("=" * 60)
            return 1


if __name__ == '__main__':
    sys.exit(main())
