#!/usr/bin/env python3
"""
Database utility functions for Driftwood Cafe
Provides common database operations and maintenance tasks
"""

from app import create_app
from extensions import db
from models import User, Category, Product, Order, OrderItem, Payment, Review
from datetime import datetime, timedelta
import json

def get_database_stats():
    """Get comprehensive database statistics"""
    app = create_app()
    
    with app.app_context():
        stats = {
            'tables': {},
            'relationships': {},
            'business_metrics': {}
        }
        
        # Table counts
        stats['tables'] = {
            'users': User.query.count(),
            'categories': Category.query.count(),
            'products': Product.query.count(),
            'orders': Order.query.count(),
            'order_items': OrderItem.query.count(),
            'payments': Payment.query.count(),
            'reviews': Review.query.count()
        }
        
        # Relationship integrity
        stats['relationships'] = {
            'users_with_orders': User.query.join(Order).count(),
            'products_with_orders': Product.query.join(OrderItem).count(),
            'orders_with_payments': Order.query.join(Payment).count(),
            'products_with_reviews': Product.query.join(Review).count()
        }
        
        # Business metrics
        total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
        avg_order_value = db.session.query(db.func.avg(Order.total_amount)).scalar() or 0
        total_orders = Order.query.count()
        completed_orders = Order.query.filter_by(status='completed').count()
        
        stats['business_metrics'] = {
            'total_revenue': float(total_revenue),
            'average_order_value': float(avg_order_value),
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'completion_rate': (completed_orders / total_orders * 100) if total_orders > 0 else 0
        }
        
        return stats

def backup_database_data():
    """Create a JSON backup of all database data"""
    app = create_app()
    
    with app.app_context():
        backup_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'users': [],
            'categories': [],
            'products': [],
            'orders': [],
            'order_items': [],
            'payments': [],
            'reviews': []
        }
        
        # Backup users (without passwords)
        for user in User.query.all():
            user_data = user.to_dict()
            backup_data['users'].append(user_data)
        
        # Backup categories
        for category in Category.query.all():
            backup_data['categories'].append(category.to_dict())
        
        # Backup products
        for product in Product.query.all():
            backup_data['products'].append(product.to_dict())
        
        # Backup orders
        for order in Order.query.all():
            backup_data['orders'].append(order.to_dict())
        
        # Backup order items
        for item in OrderItem.query.all():
            backup_data['order_items'].append(item.to_dict())
        
        # Backup payments
        for payment in Payment.query.all():
            backup_data['payments'].append(payment.to_dict())
        
        # Backup reviews
        for review in Review.query.all():
            backup_data['reviews'].append(review.to_dict())
        
        # Save to file
        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        return filename

def clean_test_data():
    """Remove test data from database"""
    app = create_app()
    
    with app.app_context():
        print("🧹 Cleaning test data...")
        
        # Remove test users
        test_users = User.query.filter(User.email.like('%example.com')).all()
        for user in test_users:
            # Remove associated reviews
            Review.query.filter_by(user_id=user.id).delete()
            
            # Remove associated orders and their items/payments
            for order in user.orders:
                OrderItem.query.filter_by(order_id=order.id).delete()
                Payment.query.filter_by(order_id=order.id).delete()
                db.session.delete(order)
            
            db.session.delete(user)
        
        # Remove test categories
        test_categories = Category.query.filter(Category.name.like('Test%')).all()
        for category in test_categories:
            # Remove associated products first
            for product in category.products:
                # Remove associated order items and reviews
                OrderItem.query.filter_by(product_id=product.id).delete()
                Review.query.filter_by(product_id=product.id).delete()
                db.session.delete(product)
            db.session.delete(category)
        
        db.session.commit()
        print("✅ Test data cleaned successfully")

def reset_database():
    """Reset database to initial state"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Resetting database...")
        
        # Drop all tables
        db.drop_all()
        
        # Recreate all tables
        db.create_all()
        
        print("✅ Database reset successfully")

def validate_data_integrity():
    """Validate database integrity and relationships"""
    app = create_app()
    
    with app.app_context():
        issues = []
        
        print("🔍 Validating data integrity...")
        
        # Check for orphaned records
        
        # Orders without users
        orphaned_orders = Order.query.filter(~Order.user_id.in_(
            db.session.query(User.id)
        )).count()
        if orphaned_orders > 0:
            issues.append(f"Found {orphaned_orders} orders without valid users")
        
        # Order items without orders
        orphaned_items = OrderItem.query.filter(~OrderItem.order_id.in_(
            db.session.query(Order.id)
        )).count()
        if orphaned_items > 0:
            issues.append(f"Found {orphaned_items} order items without valid orders")
        
        # Order items without products
        orphaned_product_items = OrderItem.query.filter(~OrderItem.product_id.in_(
            db.session.query(Product.id)
        )).count()
        if orphaned_product_items > 0:
            issues.append(f"Found {orphaned_product_items} order items without valid products")
        
        # Products without categories
        orphaned_products = Product.query.filter(~Product.category_id.in_(
            db.session.query(Category.id)
        )).count()
        if orphaned_products > 0:
            issues.append(f"Found {orphaned_products} products without valid categories")
        
        # Payments without orders
        orphaned_payments = Payment.query.filter(~Payment.order_id.in_(
            db.session.query(Order.id)
        )).count()
        if orphaned_payments > 0:
            issues.append(f"Found {orphaned_payments} payments without valid orders")
        
        # Reviews without users or products
        orphaned_user_reviews = Review.query.filter(~Review.user_id.in_(
            db.session.query(User.id)
        )).count()
        if orphaned_user_reviews > 0:
            issues.append(f"Found {orphaned_user_reviews} reviews without valid users")
        
        orphaned_product_reviews = Review.query.filter(~Review.product_id.in_(
            db.session.query(Product.id)
        )).count()
        if orphaned_product_reviews > 0:
            issues.append(f"Found {orphaned_product_reviews} reviews without valid products")
        
        # Check business logic constraints
        
        # Orders with mismatched totals
        orders_with_wrong_totals = []
        for order in Order.query.all():
            calculated_total = sum(float(item.subtotal) for item in order.order_items)
            calculated_total += float(order.delivery_fee or 0)
            if abs(float(order.total_amount) - calculated_total) > 0.01:
                orders_with_wrong_totals.append(order.order_number)
        
        if orders_with_wrong_totals:
            issues.append(f"Found {len(orders_with_wrong_totals)} orders with incorrect totals: {orders_with_wrong_totals}")
        
        # Reviews with invalid ratings
        invalid_reviews = Review.query.filter(
            (Review.rating < 1) | (Review.rating > 5)
        ).count()
        if invalid_reviews > 0:
            issues.append(f"Found {invalid_reviews} reviews with invalid ratings (not 1-5)")
        
        if issues:
            print("❌ Data integrity issues found:")
            for issue in issues:
                print(f"   • {issue}")
        else:
            print("✅ No data integrity issues found")
        
        return issues

def print_database_summary():
    """Print a comprehensive database summary"""
    stats = get_database_stats()
    
    print("\n📊 DATABASE SUMMARY")
    print("=" * 50)
    
    print("\n📋 Table Counts:")
    for table, count in stats['tables'].items():
        print(f"   • {table.capitalize()}: {count}")
    
    print("\n🔗 Relationship Integrity:")
    for relationship, count in stats['relationships'].items():
        print(f"   • {relationship.replace('_', ' ').title()}: {count}")
    
    print("\n💼 Business Metrics:")
    metrics = stats['business_metrics']
    print(f"   • Total Revenue: KES {metrics['total_revenue']:,.2f}")
    print(f"   • Average Order Value: KES {metrics['average_order_value']:,.2f}")
    print(f"   • Total Orders: {metrics['total_orders']}")
    print(f"   • Completed Orders: {metrics['completed_orders']}")
    print(f"   • Completion Rate: {metrics['completion_rate']:.1f}%")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python db_utils.py <command>")
        print("Commands:")
        print("  stats     - Show database statistics")
        print("  backup    - Create data backup")
        print("  clean     - Clean test data")
        print("  reset     - Reset database")
        print("  validate  - Validate data integrity")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "stats":
        print_database_summary()
    elif command == "backup":
        filename = backup_database_data()
        print(f"✅ Database backed up to {filename}")
    elif command == "clean":
        clean_test_data()
    elif command == "reset":
        reset_database()
    elif command == "validate":
        validate_data_integrity()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)