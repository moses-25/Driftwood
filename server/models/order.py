from extensions import db
from datetime import datetime
import uuid

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4())[:8].upper())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Order details
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    order_type = db.Column(db.String(20), nullable=False)  # pickup, delivery
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, preparing, ready, completed, cancelled
    
    # Payment details
    payment_method = db.Column(db.String(20))  # mpesa, cash
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    payment_reference = db.Column(db.String(100))
    
    # Delivery details (if applicable)
    delivery_address = db.Column(db.Text)
    delivery_instructions = db.Column(db.Text)
    delivery_fee = db.Column(db.Numeric(10, 2), default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estimated_ready_time = db.Column(db.DateTime)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user': self.user.to_dict() if self.user else None,
            'total_amount': float(self.total_amount),
            'order_type': self.order_type,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'delivery_address': self.delivery_address,
            'delivery_instructions': self.delivery_instructions,
            'delivery_fee': float(self.delivery_fee) if self.delivery_fee else 0,
            'created_at': self.created_at.isoformat(),
            'estimated_ready_time': self.estimated_ready_time.isoformat() if self.estimated_ready_time else None,
            'items': [item.to_dict() for item in self.order_items],
            'payment': self.payment.to_dict() if self.payment else None
        }
    
    def __repr__(self):
        return f'<Order {self.order_number}>'