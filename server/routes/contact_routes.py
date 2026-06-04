from flask import Blueprint, request, jsonify
from utils.email_utils import send_email, _get_smtp_config
import smtplib
import os

contact_bp = Blueprint('contact', __name__)


@contact_bp.route('/contact/test-email', methods=['GET'])
def test_email():
    import smtplib
    cfg = _get_smtp_config()
    results = []
    for label, host, port in [('STARTTLS', 'smtp.gmail.com', 587), ('SSL', 'smtp.gmail.com', 465)]:
        try:
            if label == 'SSL':
                with smtplib.SMTP_SSL(host, port, timeout=10) as server:
                    server.login(cfg['user'], cfg['password'])
                    server.sendmail(cfg['user'], [cfg['user']],
                        f"From: {cfg['user']}\nTo: {cfg['user']}\nSubject: Test from Render\n\nThis is a test.".encode())
            else:
                with smtplib.SMTP(host, port, timeout=10) as server:
                    server.starttls()
                    server.login(cfg['user'], cfg['password'])
                    server.sendmail(cfg['user'], [cfg['user']],
                        f"From: {cfg['user']}\nTo: {cfg['user']}\nSubject: Test from Render\n\nThis is a test.".encode())
            results.append(f'{label}: SUCCESS')
        except Exception as e:
            results.append(f'{label}: {e}')
    return jsonify({'results': results}), 200 if any('SUCCESS' in r for r in results) else 500


@contact_bp.route('/contact', methods=['POST'])
def submit_contact_form():
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()
        
        if not all([name, email, message]):
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Name, email, and message are required'
            }), 400
        
        if '@' not in email or '.' not in email:
            return jsonify({
                'error': 'Invalid email',
                'message': 'Please provide a valid email address'
            }), 400
        
        owner_email = os.getenv('OWNER_EMAIL', 'mosesotieno8363@gmail.com')
        
        html = f"""<html><body style="font-family:Arial,sans-serif;padding:20px;background:#f9f9f9">
<div style="max-width:600px;margin:0 auto;background:white;padding:20px;border-radius:10px">
<h2 style="color:#8B4513;border-bottom:2px solid #D2691E;padding-bottom:10px">New Contact Form Submission</h2>
<div style="background:white;padding:20px;border-radius:5px;margin:20px 0">
<p><strong>From:</strong> {name}</p>
<p><strong>Email:</strong> {email}</p>
<p><strong>Phone:</strong> {phone or 'Not provided'}</p>
</div>
<div style="background:white;padding:20px;border-radius:5px;margin:20px 0">
<h3 style="color:#8B4513;margin-top:0">Message:</h3>
<p style="white-space:pre-wrap">{message}</p>
</div>
<p style="color:#666;font-size:12px;text-align:center;margin-top:30px">Sent via Driftwood Cafe contact form</p>
</div></body></html>"""
        
        send_email(owner_email, f'Contact Form Submission from {name}', message, html)
        
        return jsonify({
            'success': True,
            'message': 'Thank you for contacting us! We will get back to you soon.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to send message',
            'message': 'An error occurred while processing your request. Please try again later.'
        }), 500
