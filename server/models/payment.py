from extensions import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    
    # Payment details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # mpesa, card, cash
    transaction_id = db.Column(db.String(100), unique=True)  # External transaction reference
    
    # Payment status
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    
    # M-Pesa specific fields
    mpesa_receipt_number = db.Column(db.String(50))
    mpesa_phone_number = db.Column(db.String(15))
    mpesa_checkout_request_id = db.Column(db.String(100))
    
    # Additional payment information
    currency = db.Column(db.String(3), default='KES')
    payment_reference = db.Column(db.String(100))  # Internal reference
    failure_reason = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def mark_as_completed(self, transaction_id=None, receipt_number=None):
        """Mark payment as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        if transaction_id:
            self.transaction_id = transaction_id
        if receipt_number:
            self.mpesa_receipt_number = receipt_number
    
    def mark_as_failed(self, reason=None):
        """Mark payment as failed"""
        self.status = 'failed'
        if reason:
            self.failure_reason = reason
    
    def to_dict(self):
        """Convert payment to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': float(self.amount),
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'mpesa_receipt_number': self.mpesa_receipt_number,
            'mpesa_phone_number': self.mpesa_phone_number,
            'currency': self.currency,
            'payment_reference': self.payment_reference,
            'failure_reason': self.failure_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.payment_reference} - {self.status}>'