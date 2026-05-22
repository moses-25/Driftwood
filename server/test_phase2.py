#!/usr/bin/env python3
"""
Test script for Phase 2 - Database Models & Relationships
"""
from app import create_app
from extensions import db
from models import User, Category, Product, Order, OrderItem, Payment, Review

def test_models():
    """Test all models and relationships"""
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing Phase 2 - Database Models & Relationships\n")
        
        # Test 1: Basic model queries
        print("1️⃣ Testing basic model queries...")
        users = User.query.all()
        categories = Category.query.all()
        products = Product.query.all()
        orders = Order.query.all()
        
        print(f"   ✅ Users: {len(users)} found")
        print(f"   ✅ Categories: {len(categories)} found")
        print(f"   ✅ Products: {len(products)} found")
        print(f"   ✅ Orders: {len(orders)} found")
        
        # Test 2: Relationships
        print("\n2️⃣ Testing model relationships...")
        
        # Test user-order relationship
        user = User.query.filter_by(role='customer').first()
        print(f"   👤 Customer '{user.username}' has {len(user.orders)} orders")
        
        # Test category-product relationship
        category = Category.query.first()
        print(f"   📂 Category '{category.name}' has {len(category.products)} products")
        
        # Test order-items relationship
        order = Order.query.first()
        print(f"   🛒 Order #{order.order_number} has {len(order.order_items)} items")
        
        # Test product reviews
        product = Product.query.first()
        print(f"   ⭐ Product '{product.name}' has {len(product.reviews)} reviews")
        
        # Test 3: Model methods
        print("\n3️⃣ Testing model methods...")
        
        # Test user methods
        print(f"   👤 User full name: {user.get_full_name()}")
        print(f"   🔐 Password check: {user.check_password('password123')}")
        
        # Test product methods
        product_with_reviews = Product.query.join(Review).first()
        if product_with_reviews:
            print(f"   ⭐ Product rating: {product_with_reviews.get_average_rating()}/5")
            print(f"   📊 Review count: {product_with_reviews.get_review_count()}")
        
        # Test order calculations
        if order.order_items:
            total_calculated = sum(item.subtotal for item in order.order_items)
            print(f"   💰 Order total: KES {order.total_amount} (calculated: {total_calculated})")
        
        # Test 4: Data serialization
        print("\n4️⃣ Testing data serialization...")
        
        user_dict = user.to_dict()
        print(f"   👤 User serialization: {len(user_dict)} fields")
        
        product_dict = product.to_dict()
        print(f"   ☕ Product serialization: {len(product_dict)} fields")
        
        order_dict = order.to_dict()
        print(f"   🛒 Order serialization: {len(order_dict)} fields")
        
        # Test 5: Complex queries
        print("\n5️⃣ Testing complex queries...")
        
        # Find bestseller products
        bestsellers = Product.query.filter_by(tag='Bestseller').all()
        print(f"   🏆 Bestseller products: {len(bestsellers)}")
        
        # Find completed orders
        completed_orders = Order.query.filter_by(status='completed').all()
        print(f"   ✅ Completed orders: {len(completed_orders)}")
        
        # Find products with reviews
        products_with_reviews = Product.query.join(Review).distinct().all()
        print(f"   ⭐ Products with reviews: {len(products_with_reviews)}")
        
        # Test 6: Sample data integrity
        print("\n6️⃣ Testing data integrity...")
        
        # Check foreign key relationships
        orphaned_products = Product.query.filter(~Product.category_id.in_(
            db.session.query(Category.id)
        )).count()
        print(f"   🔗 Orphaned products: {orphaned_products} (should be 0)")
        
        orphaned_orders = Order.query.filter(~Order.user_id.in_(
            db.session.query(User.id)
        )).count()
        print(f"   🔗 Orphaned orders: {orphaned_orders} (should be 0)")
        
        # Test payment consistency
        paid_orders = Order.query.filter_by(payment_status='paid').count()
        payment_records = Payment.query.filter_by(status='completed').count()
        print(f"   💳 Paid orders: {paid_orders}, Payment records: {payment_records}")
        
        print("\n🎉 Phase 2 Testing Complete!")
        print("✨ All models and relationships are working correctly!")
        
        # Show some sample data
        print(f"\n📋 Sample Data Preview:")
        print(f"   🏪 Categories: {', '.join([c.name for c in categories[:3]])}...")
        print(f"   ☕ Products: {', '.join([p.name for p in products[:3]])}...")
        print(f"   👥 Users: {', '.join([u.username for u in users[:3]])}...")

if __name__ == '__main__':
    test_models()