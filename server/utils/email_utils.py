"""
Email Utilities
Helper functions for sending emails
"""

from flask import render_template_string
import logging
import os

logger = logging.getLogger(__name__)

SMTP_TIMEOUT = 10
RESEND_API = 'https://api.resend.com/emails'


def send_email(to, subject, body, html=None):
    resend_key = os.getenv('RESEND_API_KEY')
    from_email = os.getenv('MAIL_USERNAME') or 'onboarding@resend.dev'

    if resend_key and resend_key != 'your_resend_api_key_here':
        return _send_via_resend(resend_key, from_email, to, subject, html or body)
    return _send_via_smtp(to, subject, html or body)


def _send_via_resend(api_key, from_email, to, subject, content):
    try:
        import requests
        resp = requests.post(RESEND_API,
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={'from': from_email, 'to': [to], 'subject': subject, 'html': content},
            timeout=15)
        if resp.ok:
            logger.info(f"Email sent via Resend to {to}: {subject}")
            return True
        logger.warning(f"Resend error {resp.status_code}: {resp.text}")
        return False
    except Exception as e:
        logger.error(f"Resend request failed: {e}")
        return False


def _send_via_smtp(to, subject, content):
    import smtplib
    cfg = {
        'host': os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
        'port': int(os.getenv('MAIL_PORT', '587')),
        'user': os.getenv('MAIL_USERNAME'),
        'password': os.getenv('MAIL_PASSWORD'),
    }
    if not cfg['user'] or not cfg['password']:
        logger.warning("SMTP not configured, skipping email send")
        return False

    msg_str = (f"From: {cfg['user']}\n"
               f"To: {to}\n"
               f"Subject: {subject}\n"
               f"MIME-Version: 1.0\n"
               f"Content-Type: text/html\n\n"
               f"{content}")

    for label, host, port in [('STARTTLS', cfg['host'], 587), ('SSL', cfg['host'], 465)]:
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
            logger.info(f"Email sent via SMTP {label} ({host}:{port})")
            return True
        except Exception as e:
            logger.warning(f"SMTP {label} failed: {e}")
            continue

    logger.error(f"All SMTP attempts failed")
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
