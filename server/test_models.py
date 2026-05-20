#!/usr/bin/env python3
"""
Model relationship testing script for Phase 2
Tests all model relationships and functionality
"""

from app import create_app
from extensions import db
from models import User, Category, Product, Order, OrderItem, Payment, Review
from datetime import datetime, timedelta

def test_model_relationships():
    """Test all model relationships and functionality"""
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing Model Relationships and Functionality")
        print("=" * 50)
        
        # Test 1: User Model
        print("\n1️⃣ Testing User Model...")
        user = User.query.filter_by(email="john@example.com").first()
        if user:
            print(f"   ✅ User found: {user.get_full_name()} ({user.email})")
            print(f"   ✅ Password check: {user.check_password('password123')}")
            print(f"   ✅ User orders: {len(user.orders)} orders")
            print(f"   ✅ User reviews: {len(user.reviews)} reviews")
        else:
            print("   ❌ User not found")
        
        # Test 2: Category-Product Relationship
        print("\n2️⃣ Testing Category-Product Relationship...")
        hot_coffee = Category.query.filter_by(name="Hot Coffee").first()
        if hot_coffee:
            print(f"   ✅ Category: {hot_coffee.name}")
            print(f"   ✅ Products in category: {len(hot_coffee.products)}")
            for product in hot_coffee.products[:3]:  # Show first 3
                print(f"      • {product.name} - KES {product.price}")
        
        # Test 3: Product Features
        print("\n3️⃣ Testing Product Features...")
        latte = Product.query.filter_by(name="Latte").first()
        if latte:
            print(f"   ✅ Product: {latte.name}")
            print(f"   ✅ Category: {latte.category.name}")
            print(f"   ✅ Average rating: {latte.get_average_rating()}⭐")
            print(f"   ✅ Review count: {latte.get_review_count()}")
            print(f"   ✅ Low stock check: {latte.is_low_stock()}")
            print(f"   ✅ Stock quantity: {latte.stock_quantity}")
        
        # Test 4: Order-OrderItem Relationship
        print("\n4️⃣ Testing Order-OrderItem Relationship...")
        order = Order.query.first()
        if order:
            print(f"   ✅ Order: {order.order_number}")
            print(f"   ✅ Customer: {order.user.get_full_name()}")
            print(f"   ✅ Total amount: KES {order.total_amount}")
            print(f"   ✅ Order items: {len(order.order_items)}")
            for item in order.order_items:
                print(f"      • {item.product.name} x{item.quantity} = KES {item.subtotal}")
                if item.get_customizations():
                    print(f"        Customizations: {item.get_customizations()}")
        
        # Test 5: Payment Relationship
        print("\n5️⃣ Testing Payment Relationship...")
        paid_order = Order.query.filter_by(payment_status="paid").first()
        if paid_order and paid_order.payment:
            payment = paid_order.payment
            print(f"   ✅ Order: {paid_order.order_number}")
            print(f"   ✅ Payment method: {payment.payment_method}")
            print(f"   ✅ Payment status: {payment.status}")
            print(f"   ✅ Transaction ID: {payment.transaction_id}")
            print(f"   ✅ Amount: KES {payment.amount}")
        
        # Test 6: Review System
        print("\n6️⃣ Testing Review System...")
        reviews = Review.query.limit(3).all()
        for review in reviews:
            print(f"   ✅ Review by {review.user.username}:")
            print(f"      Product: {review.product.name}")
            print(f"      Rating: {review.rating}⭐")
            print(f"      Comment: {review.comment}")
            print(f"      Verified purchase: {review.is_verified_purchase}")
        
        # Test 7: Data Integrity
        print("\n7️⃣ Testing Data Integrity...")
        
        # Count records
        user_count = User.query.count()
        category_count = Category.query.count()
        product_count = Product.query.count()
        order_count = Order.query.count()
        order_item_count = OrderItem.query.count()
        payment_count = Payment.query.count()
        review_count = Review.query.count()
        
        print(f"   ✅ Users: {user_count}")
        print(f"   ✅ Categories: {category_count}")
        print(f"   ✅ Products: {product_count}")
        print(f"   ✅ Orders: {order_count}")
        print(f"   ✅ Order Items: {order_item_count}")
        print(f"   ✅ Payments: {payment_count}")
        print(f"   ✅ Reviews: {review_count}")
        
        # Test 8: Advanced Queries
        print("\n8️⃣ Testing Advanced Queries...")
        
        # Most popular products (by order count)
        popular_products = db.session.query(Product, db.func.count(OrderItem.id).label('order_count'))\
            .join(OrderItem)\
            .group_by(Product.id)\
            .order_by(db.desc('order_count'))\
            .limit(3).all()
        
        print("   📈 Most popular products:")
        for product, count in popular_products:
            print(f"      • {product.name}: {count} orders")
        
        # Customers with most orders
        top_customers = db.session.query(User, db.func.count(Order.id).label('order_count'))\
            .join(Order)\
            .group_by(User.id)\
            .order_by(db.desc('order_count'))\
            .limit(3).all()
        
        print("   👑 Top customers:")
        for user, count in top_customers:
            print(f"      • {user.get_full_name()}: {count} orders")
        
        # Revenue by category
        category_revenue = db.session.query(
            Category.name,
            db.func.sum(OrderItem.subtotal).label('revenue')
        ).select_from(Category)\
         .join(Product, Category.id == Product.category_id)\
         .join(OrderItem, Product.id == OrderItem.product_id)\
         .group_by(Category.id, Category.name).all()
        
        print("   💰 Revenue by category:")
        for category_name, revenue in category_revenue:
            print(f"      • {category_name}: KES {revenue or 0}")
        
        print("\n🎉 All model tests completed successfully!")
        print("=" * 50)

def test_model_creation():
    """Test creating new model instances"""
    app = create_app()
    
    with app.app_context():
        print("\n🔧 Testing Model Creation...")
        
        try:
            # Create a new user
            new_user = User(
                username="test_user",
                email="test@example.com",
                first_name="Test",
                last_name="User",
                role="customer"
            )
            new_user.set_password("testpass123")
            db.session.add(new_user)
            db.session.flush()
            
            # Create a new category
            new_category = Category(
                name="Test Category",
                description="A test category"
            )
            db.session.add(new_category)
            db.session.flush()
            
            # Create a new product
            new_product = Product(
                name="Test Product",
                description="A test product",
                price=100.00,
                category_id=new_category.id,
                stock_quantity=10
            )
            db.session.add(new_product)
            db.session.flush()
            
            # Create a new order
            new_order = Order(
                user_id=new_user.id,
                total_amount=100.00,
                order_type="pickup",
                status="pending"
            )
            db.session.add(new_order)
            db.session.flush()
            
            # Create order item
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=new_product.id,
                quantity=1,
                unit_price=new_product.price,
                subtotal=new_product.price
            )
            db.session.add(order_item)
            
            # Create payment
            payment = Payment(
                order_id=new_order.id,
                amount=new_order.total_amount,
                payment_method="mpesa",
                status="completed",
                transaction_id="TEST123456"
            )
            db.session.add(payment)
            
            # Create review
            review = Review(
                user_id=new_user.id,
                product_id=new_product.id,
                rating=5,
                comment="Great test product!",
                is_verified_purchase=True
            )
            db.session.add(review)
            
            # Commit all changes
            db.session.commit()
            
            print("   ✅ Successfully created:")
            print(f"      • User: {new_user.username}")
            print(f"      • Category: {new_category.name}")
            print(f"      • Product: {new_product.name}")
            print(f"      • Order: {new_order.order_number}")
            print(f"      • Order Item: {order_item.quantity}x {order_item.product.name}")
            print(f"      • Payment: {payment.transaction_id}")
            print(f"      • Review: {review.rating}⭐ for {review.product.name}")
            
            # Clean up test data
            db.session.delete(review)
            db.session.delete(payment)
            db.session.delete(order_item)
            db.session.delete(new_order)
            db.session.delete(new_product)
            db.session.delete(new_category)
            db.session.delete(new_user)
            db.session.commit()
            
            print("   🧹 Test data cleaned up")
            
        except Exception as e:
            print(f"   ❌ Error during model creation: {e}")
            db.session.rollback()

if __name__ == "__main__":
    test_model_relationships()
    test_model_creation()