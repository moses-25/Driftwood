#!/usr/bin/env python3
"""
Database seeder for Driftwood Cafe
Creates initial data for testing and development
"""

from app import create_app
from extensions import db
from models import User, Category, Product, Order, OrderItem, Payment, Review
from datetime import datetime, timedelta
import random

def seed_database():
    """Seed the database with initial data"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("🗑️  Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create Categories
        print("📂 Creating categories...")
        categories = [
            Category(name="Hot Coffee", description="Freshly brewed hot coffee drinks", sort_order=1),
            Category(name="Cold Coffee", description="Iced and cold brew coffee drinks", sort_order=2),
            Category(name="Pastries", description="Fresh baked pastries and desserts", sort_order=3),
            Category(name="Specials", description="Chef's special items and seasonal offerings", sort_order=4),
            Category(name="Merchandise", description="Driftwood Cafe branded items", sort_order=5)
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        print(f"✅ Created {len(categories)} categories")
        
        # Create Products
        print("☕ Creating products...")
        products_data = [
            # Hot Coffee
            {"name": "Espresso", "description": "Rich, bold espresso shot", "price": 150, "category": "Hot Coffee", "tag": "Classic"},
            {"name": "Americano", "description": "Espresso with hot water", "price": 200, "category": "Hot Coffee", "tag": "Popular"},
            {"name": "Cappuccino", "description": "Espresso with steamed milk and foam", "price": 250, "category": "Hot Coffee", "tag": "Bestseller"},
            {"name": "Latte", "description": "Espresso with steamed milk", "price": 280, "category": "Hot Coffee", "tag": "Bestseller"},
            {"name": "Mocha", "description": "Espresso with chocolate and steamed milk", "price": 320, "category": "Hot Coffee", "tag": "Sweet"},
            
            # Cold Coffee
            {"name": "Iced Americano", "description": "Espresso with cold water over ice", "price": 220, "category": "Cold Coffee", "tag": "Refreshing"},
            {"name": "Iced Latte", "description": "Espresso with cold milk over ice", "price": 300, "category": "Cold Coffee", "tag": "Popular"},
            {"name": "Cold Brew", "description": "Smooth, cold-steeped coffee", "price": 280, "category": "Cold Coffee", "tag": "Specialty"},
            {"name": "Frappuccino", "description": "Blended coffee with ice and cream", "price": 350, "category": "Cold Coffee", "tag": "Indulgent"},
            
            # Pastries
            {"name": "Croissant", "description": "Buttery, flaky French pastry", "price": 180, "category": "Pastries", "tag": "Fresh"},
            {"name": "Chocolate Muffin", "description": "Rich chocolate chip muffin", "price": 200, "category": "Pastries", "tag": "Sweet"},
            {"name": "Blueberry Scone", "description": "Traditional scone with fresh blueberries", "price": 220, "category": "Pastries", "tag": "Homemade"},
            {"name": "Cheesecake Slice", "description": "Creamy New York style cheesecake", "price": 350, "category": "Pastries", "tag": "Indulgent"},
            
            # Specials
            {"name": "Driftwood Special", "description": "Our signature coffee blend", "price": 400, "category": "Specials", "tag": "Signature"},
            {"name": "Seasonal Latte", "description": "Limited time seasonal flavor", "price": 380, "category": "Specials", "tag": "Limited"},
            
            # Merchandise
            {"name": "Driftwood Mug", "description": "Ceramic mug with Driftwood logo", "price": 800, "category": "Merchandise", "tag": "Souvenir"},
            {"name": "Coffee Beans (250g)", "description": "Premium Driftwood coffee beans", "price": 1200, "category": "Merchandise", "tag": "Premium"}
        ]
        
        products = []
        for product_data in products_data:
            category = Category.query.filter_by(name=product_data["category"]).first()
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                category_id=category.id,
                tag=product_data["tag"],
                stock_quantity=random.randint(10, 50),
                preparation_time=random.randint(3, 15),
                calories=random.randint(50, 400) if "Coffee" in product_data["category"] else random.randint(200, 600)
            )
            products.append(product)
            db.session.add(product)
        
        db.session.commit()
        print(f"✅ Created {len(products)} products")
        
        # Create Users
        print("👥 Creating users...")
        users_data = [
            {"username": "admin", "email": "admin@driftwood.com", "role": "admin", "first_name": "Admin", "last_name": "User"},
            {"username": "staff1", "email": "staff@driftwood.com", "role": "staff", "first_name": "Jane", "last_name": "Smith"},
            {"username": "john_doe", "email": "john@example.com", "role": "customer", "first_name": "John", "last_name": "Doe"},
            {"username": "mary_jane", "email": "mary@example.com", "role": "customer", "first_name": "Mary", "last_name": "Jane"},
            {"username": "coffee_lover", "email": "lover@example.com", "role": "customer", "first_name": "Coffee", "last_name": "Lover"}
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone=f"+254{random.randint(700000000, 799999999)}",
                email_verified=True
            )
            user.set_password("password123")  # Default password for all test users
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create Sample Orders
        print("🛒 Creating sample orders...")
        customer_users = [u for u in users if u.role == "customer"]
        
        for i in range(10):  # Create 10 sample orders
            customer = random.choice(customer_users)
            order = Order(
                user_id=customer.id,
                total_amount=0,  # Will calculate after adding items
                order_type=random.choice(["pickup", "delivery"]),
                status=random.choice(["pending", "confirmed", "preparing", "ready", "completed"]),
                payment_method=random.choice(["mpesa", "card", "cash"]),
                payment_status=random.choice(["pending", "paid"]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            
            if order.order_type == "delivery":
                order.delivery_address = f"{random.randint(1, 999)} Sample Street, Nairobi"
                order.delivery_fee = 100
            
            db.session.add(order)
            db.session.flush()  # Get the order ID
            
            # Add 1-4 items to each order
            total_amount = 0
            num_items = random.randint(1, 4)
            
            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                unit_price = product.price
                subtotal = unit_price * quantity
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal
                )
                
                # Add some customizations for coffee items
                if "Coffee" in product.category.name:
                    customizations = {
                        "size": random.choice(["Small", "Medium", "Large"]),
                        "milk": random.choice(["Regular", "Oat", "Almond", "Soy"]),
                        "sugar": random.choice(["None", "1 tsp", "2 tsp"])
                    }
                    order_item.set_customizations(customizations)
                
                total_amount += subtotal
                db.session.add(order_item)
            
            # Update order total
            order.total_amount = total_amount + (order.delivery_fee or 0)
            
            # Create payment record
            if order.payment_status == "paid":
                payment = Payment(
                    order_id=order.id,
                    amount=order.total_amount,
                    payment_method=order.payment_method,
                    status="completed",
                    transaction_id=f"TXN{random.randint(100000, 999999)}",
                    completed_at=order.created_at + timedelta(minutes=random.randint(1, 10))
                )
                db.session.add(payment)
        
        db.session.commit()
        print("✅ Created 10 sample orders with items and payments")
        
        # Create Sample Reviews
        print("⭐ Creating sample reviews...")
        completed_orders = Order.query.filter_by(status="completed").all()
        
        for order in completed_orders[:5]:  # Add reviews for first 5 completed orders
            for item in order.order_items[:2]:  # Review max 2 items per order
                if random.choice([True, False]):  # 50% chance of review
                    review = Review(
                        user_id=order.user_id,
                        product_id=item.product_id,
                        rating=random.randint(3, 5),  # Mostly positive reviews
                        comment=random.choice([
                            "Great coffee, loved it!",
                            "Perfect taste and temperature.",
                            "Excellent service and quality.",
                            "Will definitely order again.",
                            "Amazing flavor, highly recommended!",
                            "Good value for money.",
                            "Fresh and delicious."
                        ]),
                        is_verified_purchase=True,
                        helpful_count=random.randint(0, 10)
                    )
                    db.session.add(review)
        
        db.session.commit()
        print("✅ Created sample reviews")
        
        # Print summary
        print("\n🎉 Database seeding completed successfully!")
        print(f"📊 Summary:")
        print(f"   • Categories: {Category.query.count()}")
        print(f"   • Products: {Product.query.count()}")
        print(f"   • Users: {User.query.count()}")
        print(f"   • Orders: {Order.query.count()}")
        print(f"   • Order Items: {OrderItem.query.count()}")
        print(f"   • Payments: {Payment.query.count()}")
        print(f"   • Reviews: {Review.query.count()}")
        
        print(f"\n🔑 Test User Credentials:")
        print(f"   • Admin: admin@driftwood.com / password123")
        print(f"   • Staff: staff@driftwood.com / password123")
        print(f"   • Customer: john@example.com / password123")

if __name__ == "__main__":
    seed_database()