from extensions import db
import json

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
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
            'menu_item': self.menu_item.to_dict() if self.menu_item else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price),
            'customizations': self.get_customizations()
        }
    
    def __repr__(self):
        return f'<OrderItem {self.menu_item.name} x{self.quantity}>'