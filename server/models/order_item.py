from extensions import db
import json

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Store customizations as JSON
    customizations = db.Column(db.Text)  # JSON string for size, milk type, extras, etc.
    
    def set_customizations(self, customizations_dict):
        """Set customizations from a dictionary"""
        self.customizations = json.dumps(customizations_dict) if customizations_dict else None
    
    def get_customizations(self):
        """Get customizations as a dictionary"""
        if self.customizations:
            try:
                return json.loads(self.customizations)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'subtotal': float(self.subtotal),
            'customizations': self.get_customizations()
        }
    
    def __repr__(self):
        return f'<OrderItem {self.product.name} x{self.quantity}>'