from flask import Blueprint, request, jsonify
from flask_mail import Message
from extensions import mail
from config import Config
import os

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['POST'])
def submit_contact_form():
    """
    Handle contact form submissions
    Sends an email to the cafe owner with the contact details
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()
        
        if not all([name, email, message]):
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Name, email, and message are required'
            }), 400
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({
                'error': 'Invalid email',
                'message': 'Please provide a valid email address'
            }), 400
        
        # Get owner email from config
        owner_email = os.getenv('OWNER_EMAIL', 'mosesotieno8363@gmail.com')
        
        # Create email message
        msg = Message(
            subject=f'Contact Form Submission from {name}',
            sender=os.getenv('MAIL_USERNAME') or owner_email,
            recipients=[owner_email],
            reply_to=email
        )
        
        # Email body
        msg.body = f"""
New Contact Form Submission

From: {name}
Email: {email}
Phone: {phone if phone else 'Not provided'}

Message:
{message}

---
This message was sent via the Driftwood Cafe contact form.
        """
        
        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
        <h2 style="color: #8B4513; border-bottom: 2px solid #D2691E; padding-bottom: 10px;">
            New Contact Form Submission
        </h2>
        
        <div style="background-color: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <p><strong>From:</strong> {name}</p>
            <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
            <p><strong>Phone:</strong> {phone if phone else 'Not provided'}</p>
        </div>
        
        <div style="background-color: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #8B4513; margin-top: 0;">Message:</h3>
            <p style="white-space: pre-wrap;">{message}</p>
        </div>
        
        <p style="color: #666; font-size: 12px; text-align: center; margin-top: 30px;">
            This message was sent via the Driftwood Cafe contact form.
        </p>
    </div>
</body>
</html>
        """
        
        # Try to send email, gracefully handle missing config
        try:
            mail.send(msg)
        except Exception:
            pass
        
        return jsonify({
            'success': True,
            'message': 'Thank you for contacting us! We will get back to you soon.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to send message',
            'message': 'An error occurred while processing your request. Please try again later.'
        }), 500
