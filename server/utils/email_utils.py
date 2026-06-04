"""
Email Utilities
Helper functions for sending emails
"""

from flask import render_template_string
import smtplib
import logging
import os

logger = logging.getLogger(__name__)

SMTP_TIMEOUT = 10


def _get_smtp_config():
    return {
        'host': os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
        'port': int(os.getenv('MAIL_PORT', '587')),
        'user': os.getenv('MAIL_USERNAME'),
        'password': os.getenv('MAIL_PASSWORD'),
    }


def send_email(to, subject, body, html=None):
    cfg = _get_smtp_config()
    if not cfg['user'] or not cfg['password']:
        logger.warning("Email not configured, skipping email send")
        return False

    content = html or body
    msg_str = (f"From: {cfg['user']}\n"
               f"To: {to}\n"
               f"Subject: {subject}\n"
               f"MIME-Version: 1.0\n"
               f"Content-Type: text/html\n\n"
               f"{content}")

    attempts = [
        ('STARTTLS', cfg['host'], 587),
        ('SSL', cfg['host'], 465),
    ]

    for label, host, port in attempts:
        try:
            if label == 'SSL':
                with smtplib.SMTP_SSL(host, port, timeout=SMTP_TIMEOUT) as server:
                    server.login(cfg['user'], cfg['password'])
                    server.sendmail(cfg['user'], [to], msg_str.encode())
            else:
                with smtplib.SMTP(host, port, timeout=SMTP_TIMEOUT) as server:
                    server.starttls()
                    server.login(cfg['user'], cfg['password'])
                    server.sendmail(cfg['user'], [to], msg_str.encode())

            logger.info(f"Email sent to {to} via {label} ({host}:{port})")
            return True
        except Exception as e:
            logger.warning(f"SMTP {label} ({host}:{port}) failed: {e}")
            continue

    logger.error(f"All SMTP attempts failed for {to}")
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
