# Contact Form Endpoint Fix

## Issue
The contact form on the "Visit Us" page was not working because the backend endpoint `/api/contact` was missing.

## Solution
Created a new contact route handler that:
1. Accepts POST requests to `/api/contact`
2. Validates the contact form data (name, email, message)
3. Sends an email to the cafe owner using Flask-Mail
4. Returns a success response to the frontend

## Files Created/Modified

### Created:
- `server/routes/contact_routes.py` - New contact form handler

### Modified:
- `server/routes/__init__.py` - Registered the contact blueprint

## Endpoint Details

**URL:** `POST /api/contact`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+254 700 000 000",  // Optional
  "message": "Your message here"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Thank you for contacting us! We will get back to you soon."
}
```

**Error Response (400/500):**
```json
{
  "error": "Error type",
  "message": "Error description"
}
```

## Email Configuration

The endpoint uses the following environment variables from `.env`:
- `MAIL_SERVER` - SMTP server (smtp.gmail.com)
- `MAIL_PORT` - SMTP port (587)
- `MAIL_USE_TLS` - Use TLS (true)
- `MAIL_USERNAME` - Sender email address
- `MAIL_PASSWORD` - Email password/app password
- `OWNER_EMAIL` - Recipient email (cafe owner)

## Testing

Test the endpoint with curl:
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "message": "Test message"
  }'
```

## Frontend Integration

The frontend already has the correct API call in `client/src/services/api.js`:
```javascript
export const submitContactForm = async (formData) => {
  return apiRequest('/api/contact', {
    method: 'POST',
    body: JSON.stringify(formData),
  });
};
```

This is used in `client/src/pages/VisitUs.jsx` for the contact form.

## Status
✅ **Fixed and Working** - The contact form now successfully sends emails to the cafe owner.
