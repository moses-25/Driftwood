"""
Stock Adjustment Model
Tracks all inventory adjustments for audit trail
"""

from extensions import db
from datetime import datetime


class StockAdjustment(db.Model):
    __tablename__ = 'stock_adjustments'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity_change = db.Column(db.Integer, nullable=False)  # +/- value
    reason = db.Column(db.String(200), nullable=False)
    adjustment_type = db.Column(db.String(50), nullable=False)  # manual, order, restock, correction
    reference_id = db.Column(db.String(100))  # Order ID or other reference
    adjusted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='stock_adjustments')
    user = db.relationship('User', backref='stock_adjustments')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity_change': self.quantity_change,
            'reason': self.reason,
            'adjustment_type': self.adjustment_type,
            'reference_id': self.reference_id,
            'adjusted_by': self.user.username if self.user else 'System',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<StockAdjustment {self.product.name if self.product else "Unknown"} {self.quantity_change:+d}>'
