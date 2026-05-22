from extensions import db
from datetime import datetime

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # hot, cold, pastries, specials, merch
    image_url = db.Column(db.String(255))
    tag = db.Column(db.String(20))  # Bestseller, New, etc.
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': f"KES {int(self.price)}",
            'category': self.category,
            'image': self.image_url,
            'tag': self.tag,
            'is_available': self.is_available
        }
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'