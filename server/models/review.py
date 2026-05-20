from extensions import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Review content
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    
    # Review metadata
    is_verified_purchase = db.Column(db.Boolean, default=False)  # Did user actually buy this?
    is_approved = db.Column(db.Boolean, default=True)  # For moderation
    helpful_count = db.Column(db.Integer, default=0)  # How many found this helpful
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints to prevent duplicate reviews
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_review'),)
    
    def to_dict(self, include_user=True):
        """Convert review to dictionary"""
        data = {
            'id': self.id,
            'product_id': self.product_id,
            'rating': self.rating,
            'comment': self.comment,
            'is_verified_purchase': self.is_verified_purchase,
            'is_approved': self.is_approved,
            'helpful_count': self.helpful_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_user and self.user:
            data['user'] = {
                'id': self.user.id,
                'username': self.user.username,
                'first_name': self.user.first_name
            }
            
        return data
    
    @staticmethod
    def validate_rating(rating):
        """Validate rating is between 1 and 5"""
        return 1 <= rating <= 5
    
    def __repr__(self):
        return f'<Review {self.rating}★ by {self.user.username}>'