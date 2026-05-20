from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Category relationship
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Product details
    image_url = db.Column(db.String(255))
    tag = db.Column(db.String(20))  # Bestseller, New, Featured, etc.
    is_available = db.Column(db.Boolean, default=True)
    
    # Inventory management
    stock_quantity = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=5)
    
    # Product metadata
    preparation_time = db.Column(db.Integer)  # in minutes
    calories = db.Column(db.Integer)
    allergens = db.Column(db.Text)  # JSON string for allergen information
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)
    
    def get_average_rating(self):
        """Calculate average rating from reviews"""
        if not self.reviews:
            return 0
        total_rating = sum(review.rating for review in self.reviews)
        return round(total_rating / len(self.reviews), 1)
    
    def get_review_count(self):
        """Get total number of reviews"""
        return len(self.reviews) if self.reviews else 0
    
    def is_low_stock(self):
        """Check if product is low on stock"""
        return self.stock_quantity <= self.low_stock_threshold
    
    def to_dict(self, include_reviews=False):
        """Convert product to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'image_url': self.image_url,
            'tag': self.tag,
            'is_available': self.is_available,
            'stock_quantity': self.stock_quantity,
            'is_low_stock': self.is_low_stock(),
            'preparation_time': self.preparation_time,
            'calories': self.calories,
            'average_rating': self.get_average_rating(),
            'review_count': self.get_review_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_reviews:
            data['reviews'] = [review.to_dict() for review in self.reviews]
            
        return data
    
    def __repr__(self):
        return f'<Product {self.name}>'