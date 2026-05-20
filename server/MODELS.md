# Driftwood Cafe - Database Models Documentation

This document provides comprehensive documentation for all database models in the Driftwood Cafe backend system.

## Overview

The database schema consists of 7 main models that handle user management, product catalog, orders, payments, and reviews. All models follow consistent patterns for timestamps, relationships, and data validation.

---

## Models

### 1. User Model (`models/user.py`)

**Purpose:** Manages user accounts for customers, staff, and administrators.

**Table:** `users`

**Fields:**
- `id` (Integer, Primary Key) - Unique user identifier
- `username` (String, 80, Unique) - User's chosen username
- `email` (String, 120, Unique) - User's email address
- `password_hash` (String, 255) - Hashed password using Werkzeug
- `first_name` (String, 50) - User's first name
- `last_name` (String, 50) - User's last name
- `phone` (String, 20) - User's phone number
- `address` (Text) - User's address
- `role` (String, 20, Default: 'customer') - User role: customer, staff, admin
- `is_active` (Boolean, Default: True) - Account status
- `email_verified` (Boolean, Default: False) - Email verification status
- `created_at` (DateTime) - Account creation timestamp
- `updated_at` (DateTime) - Last update timestamp
- `last_login` (DateTime) - Last login timestamp

**Relationships:**
- `orders` - One-to-many with Order model
- `reviews` - One-to-many with Review model

**Methods:**
- `set_password(password)` - Hash and set password
- `check_password(password)` - Verify password
- `get_full_name()` - Get formatted full name
- `to_dict(include_sensitive=False)` - Convert to dictionary

**Usage Example:**
```python
# Create new user
user = User(
    username="john_doe",
    email="john@example.com",
    first_name="John",
    last_name="Doe"
)
user.set_password("secure_password")
db.session.add(user)
db.session.commit()

# Verify password
if user.check_password("secure_password"):
    print("Password correct")
```

---

### 2. Category Model (`models/category.py`)

**Purpose:** Organizes products into logical categories (Hot Coffee, Pastries, etc.).

**Table:** `categories`

**Fields:**
- `id` (Integer, Primary Key) - Unique category identifier
- `name` (String, 100, Unique) - Category name
- `description` (Text) - Category description
- `is_active` (Boolean, Default: True) - Category status
- `sort_order` (Integer, Default: 0) - Display order
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

**Relationships:**
- `products` - One-to-many with Product model

**Methods:**
- `to_dict()` - Convert to dictionary with product count

**Usage Example:**
```python
# Create category
category = Category(
    name="Hot Coffee",
    description="Freshly brewed hot coffee drinks",
    sort_order=1
)
db.session.add(category)
db.session.commit()
```

---

### 3. Product Model (`models/product.py`)

**Purpose:** Represents individual menu items and merchandise.

**Table:** `products`

**Fields:**
- `id` (Integer, Primary Key) - Unique product identifier
- `name` (String, 100) - Product name
- `description` (Text) - Product description
- `price` (Numeric, 10,2) - Product price in KES
- `category_id` (Integer, Foreign Key) - Reference to Category
- `image_url` (String, 255) - Product image URL
- `tag` (String, 20) - Product tag (Bestseller, New, etc.)
- `is_available` (Boolean, Default: True) - Availability status
- `stock_quantity` (Integer, Default: 0) - Current stock level
- `low_stock_threshold` (Integer, Default: 5) - Low stock alert threshold
- `preparation_time` (Integer) - Preparation time in minutes
- `calories` (Integer) - Calorie content
- `allergens` (Text) - Allergen information (JSON string)
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

**Relationships:**
- `category` - Many-to-one with Category model
- `order_items` - One-to-many with OrderItem model
- `reviews` - One-to-many with Review model

**Methods:**
- `get_average_rating()` - Calculate average rating from reviews
- `get_review_count()` - Get total number of reviews
- `is_low_stock()` - Check if product is low on stock
- `to_dict(include_reviews=False)` - Convert to dictionary

**Usage Example:**
```python
# Create product
product = Product(
    name="Cappuccino",
    description="Espresso with steamed milk and foam",
    price=250.00,
    category_id=hot_coffee_category.id,
    stock_quantity=50,
    preparation_time=5,
    calories=120
)
db.session.add(product)
db.session.commit()
```

---

### 4. Order Model (`models/order.py`)

**Purpose:** Represents customer orders with items, delivery, and payment information.

**Table:** `orders`

**Fields:**
- `id` (Integer, Primary Key) - Unique order identifier
- `order_number` (String, 50, Unique) - Human-readable order number
- `user_id` (Integer, Foreign Key) - Reference to User
- `total_amount` (Numeric, 10,2) - Total order amount
- `order_type` (String, 20) - Order type: pickup, delivery
- `status` (String, 20, Default: 'pending') - Order status
- `payment_method` (String, 20) - Payment method
- `payment_status` (String, 20, Default: 'pending') - Payment status
- `payment_reference` (String, 100) - Payment reference
- `delivery_address` (Text) - Delivery address (if applicable)
- `delivery_instructions` (Text) - Delivery instructions
- `delivery_fee` (Numeric, 10,2, Default: 0) - Delivery fee
- `created_at` (DateTime) - Order creation timestamp
- `updated_at` (DateTime) - Last update timestamp
- `estimated_ready_time` (DateTime) - Estimated completion time

**Relationships:**
- `user` - Many-to-one with User model
- `order_items` - One-to-many with OrderItem model (cascade delete)
- `payment` - One-to-one with Payment model

**Methods:**
- `to_dict()` - Convert to dictionary with all related data

**Order Status Flow:**
1. `pending` - Order created, awaiting confirmation
2. `confirmed` - Order confirmed by staff
3. `preparing` - Order being prepared
4. `ready` - Order ready for pickup/delivery
5. `completed` - Order completed
6. `cancelled` - Order cancelled

**Usage Example:**
```python
# Create order
order = Order(
    user_id=customer.id,
    total_amount=500.00,
    order_type="pickup",
    status="pending"
)
db.session.add(order)
db.session.commit()
```

---

### 5. OrderItem Model (`models/order_item.py`)

**Purpose:** Represents individual items within an order with quantities and customizations.

**Table:** `order_items`

**Fields:**
- `id` (Integer, Primary Key) - Unique item identifier
- `order_id` (Integer, Foreign Key) - Reference to Order
- `product_id` (Integer, Foreign Key) - Reference to Product
- `quantity` (Integer, Default: 1) - Item quantity
- `unit_price` (Numeric, 10,2) - Price per unit at time of order
- `subtotal` (Numeric, 10,2) - Total price for this item
- `customizations` (Text) - JSON string for customizations

**Relationships:**
- `order` - Many-to-one with Order model
- `product` - Many-to-one with Product model

**Methods:**
- `set_customizations(customizations_dict)` - Set customizations from dictionary
- `get_customizations()` - Get customizations as dictionary
- `to_dict()` - Convert to dictionary

**Customization Examples:**
```json
{
  "size": "Large",
  "milk": "Oat",
  "sugar": "2 tsp",
  "extras": ["Extra shot", "Vanilla syrup"]
}
```

**Usage Example:**
```python
# Create order item
item = OrderItem(
    order_id=order.id,
    product_id=cappuccino.id,
    quantity=2,
    unit_price=cappuccino.price,
    subtotal=cappuccino.price * 2
)
item.set_customizations({
    "size": "Large",
    "milk": "Oat"
})
db.session.add(item)
db.session.commit()
```

---

### 6. Payment Model (`models/payment.py`)

**Purpose:** Tracks payment transactions for orders, especially M-Pesa integration.

**Table:** `payments`

**Fields:**
- `id` (Integer, Primary Key) - Unique payment identifier
- `order_id` (Integer, Foreign Key) - Reference to Order
- `amount` (Numeric, 10,2) - Payment amount
- `payment_method` (String, 20) - Payment method: mpesa, card, cash
- `transaction_id` (String, 100, Unique) - External transaction reference
- `status` (String, 20, Default: 'pending') - Payment status
- `mpesa_receipt_number` (String, 50) - M-Pesa receipt number
- `mpesa_phone_number` (String, 15) - M-Pesa phone number
- `mpesa_checkout_request_id` (String, 100) - M-Pesa checkout request ID
- `currency` (String, 3, Default: 'KES') - Payment currency
- `payment_reference` (String, 100) - Internal payment reference
- `failure_reason` (Text) - Failure reason if payment failed
- `created_at` (DateTime) - Payment creation timestamp
- `updated_at` (DateTime) - Last update timestamp
- `completed_at` (DateTime) - Payment completion timestamp

**Relationships:**
- `order` - One-to-one with Order model

**Methods:**
- `mark_as_completed(transaction_id, receipt_number)` - Mark payment as completed
- `mark_as_failed(reason)` - Mark payment as failed
- `to_dict()` - Convert to dictionary

**Payment Status Flow:**
1. `pending` - Payment initiated
2. `completed` - Payment successful
3. `failed` - Payment failed
4. `refunded` - Payment refunded

**Usage Example:**
```python
# Create payment
payment = Payment(
    order_id=order.id,
    amount=order.total_amount,
    payment_method="mpesa",
    mpesa_phone_number="254712345678"
)
db.session.add(payment)
db.session.commit()

# Mark as completed
payment.mark_as_completed("TXN123456", "MPE123456")
db.session.commit()
```

---

### 7. Review Model (`models/review.py`)

**Purpose:** Manages customer reviews and ratings for products.

**Table:** `reviews`

**Fields:**
- `id` (Integer, Primary Key) - Unique review identifier
- `user_id` (Integer, Foreign Key) - Reference to User
- `product_id` (Integer, Foreign Key) - Reference to Product
- `rating` (Integer) - Rating from 1-5 stars
- `comment` (Text) - Review comment
- `is_verified_purchase` (Boolean, Default: False) - Verified purchase flag
- `is_approved` (Boolean, Default: True) - Moderation approval
- `helpful_count` (Integer, Default: 0) - Helpful votes count
- `created_at` (DateTime) - Review creation timestamp
- `updated_at` (DateTime) - Last update timestamp

**Relationships:**
- `user` - Many-to-one with User model
- `product` - Many-to-one with Product model

**Constraints:**
- Unique constraint on (user_id, product_id) - One review per user per product

**Methods:**
- `to_dict(include_user=True)` - Convert to dictionary
- `validate_rating(rating)` - Static method to validate rating range

**Usage Example:**
```python
# Create review
review = Review(
    user_id=customer.id,
    product_id=cappuccino.id,
    rating=5,
    comment="Excellent coffee, perfect temperature!",
    is_verified_purchase=True
)
db.session.add(review)
db.session.commit()
```

---

## Database Relationships Summary

```
User (1) ←→ (N) Order ←→ (1) Payment
User (1) ←→ (N) Review

Category (1) ←→ (N) Product
Product (1) ←→ (N) OrderItem ←→ (N) Order
Product (1) ←→ (N) Review
```

## Common Query Patterns

### Get User's Orders with Items
```python
user = User.query.get(user_id)
orders = user.orders.order_by(Order.created_at.desc()).all()
for order in orders:
    for item in order.order_items:
        print(f"{item.product.name} x{item.quantity}")
```

### Get Product Reviews with User Info
```python
product = Product.query.get(product_id)
reviews = product.reviews.filter_by(is_approved=True).all()
for review in reviews:
    print(f"{review.user.username}: {review.rating}⭐ - {review.comment}")
```

### Calculate Category Revenue
```python
revenue = db.session.query(
    Category.name,
    db.func.sum(OrderItem.subtotal).label('revenue')
).select_from(Category)\
 .join(Product)\
 .join(OrderItem)\
 .group_by(Category.id).all()
```

### Find Popular Products
```python
popular = db.session.query(
    Product,
    db.func.count(OrderItem.id).label('order_count')
).join(OrderItem)\
 .group_by(Product.id)\
 .order_by(db.desc('order_count')).all()
```

---

## Data Validation Rules

1. **User emails must be unique**
2. **Usernames must be unique**
3. **Category names must be unique**
4. **Order numbers are auto-generated and unique**
5. **Payment transaction IDs must be unique**
6. **Reviews: one per user per product**
7. **Ratings must be between 1-5**
8. **Prices must be positive numbers**
9. **Stock quantities cannot be negative**

---

## Migration Notes

- All models use consistent timestamp fields (`created_at`, `updated_at`)
- Foreign key relationships use proper constraints
- Cascade deletes are configured where appropriate (Order → OrderItems)
- Indexes should be added for frequently queried fields (email, order_number, etc.)

---

This documentation covers Phase 2 of the Driftwood Cafe backend development. All models are fully implemented with proper relationships, validation, and helper methods.