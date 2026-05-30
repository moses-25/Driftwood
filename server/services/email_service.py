"""
Email Service
Handles all email-related operations
"""

from utils.email_utils import send_email, render_email_template
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for handling email operations"""
    
    @staticmethod
    def send_newsletter_subscription(email):
        """
        Send newsletter subscription confirmation email
        
        Args:
            email: Subscriber email address
            
        Returns:
            Boolean indicating success
        """
        try:
            subject = "Welcome to Driftwood Cafe Newsletter!"
            
            body = f"""
            Thank you for subscribing to the Driftwood Cafe newsletter!
            
            You'll now receive updates about:
            - New menu items and seasonal specials
            - Exclusive promotions and discounts
            - Cafe events and news
            
            We're excited to keep you updated!
            
            Best regards,
            The Driftwood Cafe Team
            """
            
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f7fafc;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2 style="color: #2D3748; margin-bottom: 20px;">Welcome to Driftwood Cafe Newsletter!</h2>
                    <p style="color: #4A5568; line-height: 1.6;">Thank you for subscribing to our newsletter!</p>
                    <p style="color: #4A5568; line-height: 1.6;">You'll now receive updates about:</p>
                    <ul style="color: #4A5568; line-height: 1.8;">
                        <li>New menu items and seasonal specials</li>
                        <li>Exclusive promotions and discounts</li>
                        <li>Cafe events and news</li>
                    </ul>
                    <p style="color: #4A5568; line-height: 1.6;">We're excited to keep you updated!</p>
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #E2E8F0;">
                        <p style="color: #718096; font-size: 14px;">Best regards,<br>The Driftwood Cafe Team</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return send_email(email, subject, body, html)
            
        except Exception as e:
            logger.error(f"Error sending newsletter subscription email: {str(e)}")
            return False
    
    
    @staticmethod
    def send_contact_form_notification(name, email, phone, message):
        """
        Send contact form notification to cafe owner
        
        Args:
            name: Contact name
            email: Contact email
            phone: Contact phone
            message: Contact message
            
        Returns:
            Boolean indicating success
        """
        try:
            from flask import current_app
            owner_email = current_app.config.get('OWNER_EMAIL')
            
            if not owner_email:
                logger.warning("OWNER_EMAIL not configured")
                return False
            
            subject = f"New Contact Form Submission from {name}"
            
            body = f"""
            New contact form submission:
            
            Name: {name}
            Email: {email}
            Phone: {phone}
            
            Message:
            {message}
            """
            
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #2D3748;">New Contact Form Submission</h2>
                <div style="background-color: #f7fafc; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Phone:</strong> {phone}</p>
                </div>
                <div style="margin-top: 20px;">
                    <p><strong>Message:</strong></p>
                    <p style="background-color: #f7fafc; padding: 15px; border-left: 4px solid #4299E1; border-radius: 3px;">
                        {message}
                    </p>
                </div>
            </body>
            </html>
            """
            
            return send_email(owner_email, subject, body, html)
            
        except Exception as e:
            logger.error(f"Error sending contact form notification: {str(e)}")
            return False
    
    
    @staticmethod
    def send_order_confirmation(order):
        """
        Send order confirmation email to customer
        
        Args:
            order: Order object
            
        Returns:
            Boolean indicating success
        """
        try:
            if not order.user or not order.user.email:
                logger.warning(f"No email address for order {order.order_number}")
                return False
            
            subject = f"Order Confirmation - #{order.order_number}"
            
            body = f"""
            Hi {order.user.name},
            
            Your order #{order.order_number} has been confirmed!
            
            Total: KES {order.total_amount}
            Payment Status: {order.payment_status}
            
            Thank you for choosing Driftwood Cafe!
            """
            
            context = {
                'customer_name': order.user.name,
                'order_number': order.order_number,
                'total_amount': order.total_amount,
                'estimated_time': '15-20 minutes'
            }
            
            html = render_email_template('order_confirmed', context)
            
            return send_email(order.user.email, subject, body, html)
            
        except Exception as e:
            logger.error(f"Error sending order confirmation: {str(e)}")
            return False
