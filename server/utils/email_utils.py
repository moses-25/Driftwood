"""
Email Utilities
Helper functions for sending emails
"""

from flask import current_app, render_template_string
from flask_mail import Mail, Message
import logging

logger = logging.getLogger(__name__)

mail = Mail()


def configure_email(app):
    """
    Configure email service
    
    Args:
        app: Flask application instance
    """
    mail.init_app(app)
    logger.info("Email service configured")


def validate_email_config():
    """
    Validate email configuration
    
    Returns:
        Boolean indicating if email is properly configured
    """
    required_settings = ['MAIL_SERVER', 'MAIL_USERNAME', 'MAIL_PASSWORD']
    
    for setting in required_settings:
        if not current_app.config.get(setting):
            logger.warning(f"Email configuration missing: {setting}")
            return False
    
    return True


def send_email(to, subject, body, html=None):
    """
    Send email
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Plain text body
        html: HTML body (optional)
    
    Returns:
        Boolean indicating success
    """
    try:
        if not validate_email_config():
            logger.warning("Email not configured, skipping email send")
            return False
        
        msg = Message(
            subject=subject,
            sender=current_app.config.get('MAIL_USERNAME'),
            recipients=[to] if isinstance(to, str) else to
        )
        
        msg.body = body
        if html:
            msg.html = html
        
        mail.send(msg)
        logger.info(f"Email sent to {to}: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False


def render_email_template(template_name, context):
    """
    Render email template
    
    Args:
        template_name: Template name
        context: Template context dictionary
    
    Returns:
        Rendered HTML string
    """
    try:
        # Simple template rendering
        # In production, use proper template files
        templates = {
            'order_confirmed': """
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #4A5568;">Order Confirmed!</h2>
                    <p>Hi {{ customer_name }},</p>
                    <p>Your order <strong>#{{ order_number }}</strong> has been confirmed.</p>
                    <p><strong>Total:</strong> KES {{ total_amount }}</p>
                    <p><strong>Estimated Ready Time:</strong> {{ estimated_time }}</p>
                    <p>Thank you for choosing Driftwood Cafe!</p>
                </body>
                </html>
            """,
            'order_preparing': """
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #4A5568;">Your Order is Being Prepared</h2>
                    <p>Hi {{ customer_name }},</p>
                    <p>Great news! Your order <strong>#{{ order_number }}</strong> is now being prepared.</p>
                    <p>We'll notify you when it's ready for {{ order_type }}.</p>
                </body>
                </html>
            """,
            'order_ready': """
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #48BB78;">Your Order is Ready!</h2>
                    <p>Hi {{ customer_name }},</p>
                    <p>Your order <strong>#{{ order_number }}</strong> is ready for {{ order_type }}!</p>
                    <p>{% if order_type == 'pickup' %}Please come pick it up at your convenience.{% endif %}</p>
                </body>
                </html>
            """,
            'order_completed': """
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #48BB78;">Order Completed</h2>
                    <p>Hi {{ customer_name }},</p>
                    <p>Your order <strong>#{{ order_number }}</strong> has been completed.</p>
                    <p>Thank you for your business! We hope to see you again soon.</p>
                    <p>Please consider leaving a review of your experience.</p>
                </body>
                </html>
            """,
            'order_cancelled': """
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #F56565;">Order Cancelled</h2>
                    <p>Hi {{ customer_name }},</p>
                    <p>Your order <strong>#{{ order_number }}</strong> has been cancelled.</p>
                    <p>If you have any questions, please contact us.</p>
                </body>
                </html>
            """
        }
        
        template = templates.get(template_name, '<p>{{ message }}</p>')
        return render_template_string(template, **context)
        
    except Exception as e:
        logger.error(f"Error rendering email template: {str(e)}")
        return f"<p>{context.get('message', 'Notification')}</p>"
