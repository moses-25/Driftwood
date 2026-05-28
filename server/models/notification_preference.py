"""
Notification Preference Model
User notification preferences
"""

from extensions import db


class NotificationPreference(db.Model):
    __tablename__ = 'notification_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    email_enabled = db.Column(db.Boolean, default=True)
    sms_enabled = db.Column(db.Boolean, default=False)
    order_status_updates = db.Column(db.Boolean, default=True)
    promotional_emails = db.Column(db.Boolean, default=True)
    low_stock_alerts = db.Column(db.Boolean, default=True)  # For staff/admin
    
    # Relationships
    user = db.relationship('User', backref=db.backref('notification_preferences', uselist=False))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email_enabled': self.email_enabled,
            'sms_enabled': self.sms_enabled,
            'order_status_updates': self.order_status_updates,
            'promotional_emails': self.promotional_emails,
            'low_stock_alerts': self.low_stock_alerts
        }
    
    def __repr__(self):
        return f'<NotificationPreference User#{self.user_id}>'
