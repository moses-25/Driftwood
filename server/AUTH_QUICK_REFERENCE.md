# Authentication Quick Reference Guide

## 🚀 Quick Start

### 1. Register a User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass@123",
  "first_name": "John",
  "last_name": "Doe"
}

Response: { access_token, refresh_token, user }
```

### 2. Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass@123"
}

Response: { access_token, refresh_token, user }
```

### 3. Use Protected Routes
```bash
GET /api/auth/me
Authorization: Bearer <access_token>

Response: { user }
```

## 📋 All Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/api/auth/register` | No | Register new user |
| POST | `/api/auth/login` | No | Login user |
| POST | `/api/auth/refresh` | Refresh Token | Get new access token |
| GET | `/api/auth/me` | Access Token | Get current user |
| POST | `/api/auth/change-password` | Access Token | Change password |
| POST | `/api/auth/request-password-reset` | No | Request reset token |
| POST | `/api/auth/reset-password` | Reset Token | Reset password |
| POST | `/api/auth/verify-email` | Verification Token | Verify email |

## 🔐 Decorators

### Basic Authentication
```python
from flask_jwt_extended import jwt_required

@app.route('/protected')
@jwt_required()
def protected():
    return {'message': 'Authenticated users only'}
```

### Role-Based Access
```python
from utils.decorators import admin_required, staff_required, role_required

# Admin only
@app.route('/admin')
@jwt_required()
@admin_required
def admin_only():
    return {'message': 'Admin access'}

# Staff or Admin
@app.route('/staff')
@jwt_required()
@staff_required
def staff_only():
    return {'message': 'Staff access'}

# Custom roles
@app.route('/custom')
@jwt_required()
@role_required('staff', 'admin')
def custom_roles():
    return {'message': 'Staff or Admin'}
```

### Get Current User
```python
from utils.decorators import get_current_user

@app.route('/profile')
@jwt_required()
def profile():
    user = get_current_user()
    return {'username': user.username, 'email': user.email}
```

## 🔑 Token Types

### Access Token
- **Expiration:** 1 hour
- **Use:** API authentication
- **Header:** `Authorization: Bearer <access_token>`

### Refresh Token
- **Expiration:** 30 days
- **Use:** Get new access token
- **Header:** `Authorization: Bearer <refresh_token>`
- **Endpoint:** `POST /api/auth/refresh`

## 👥 User Roles

| Role | Access Level | Description |
|------|--------------|-------------|
| `admin` | Full access | Can access all routes |
| `staff` | Staff + Customer | Can access staff and customer routes |
| `customer` | Customer only | Can access customer routes |

## ✅ Password Requirements

- Minimum 8 characters
- At least 1 uppercase letter (A-Z)
- At least 1 lowercase letter (a-z)
- At least 1 digit (0-9)
- At least 1 special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

**Valid:** `SecurePass@123`, `MyP@ssw0rd`, `Test@1234`
**Invalid:** `password`, `12345678`, `Password` (no special char)

## 🧪 Test Users

```python
# Admin
email: admin@driftwood.com
password: password123
role: admin

# Staff
email: staff@driftwood.com
password: password123
role: staff

# Customer
email: john@example.com
password: password123
role: customer
```

## 🐍 Python Examples

### Register
```python
import requests

response = requests.post('http://localhost:5000/api/auth/register', json={
    'username': 'newuser',
    'email': 'new@example.com',
    'password': 'Secure@123'
})
tokens = response.json()['data']
```

### Login
```python
response = requests.post('http://localhost:5000/api/auth/login', json={
    'email': 'new@example.com',
    'password': 'Secure@123'
})
access_token = response.json()['data']['access_token']
```

### Protected Request
```python
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get('http://localhost:5000/api/auth/me', headers=headers)
user = response.json()['data']
```

### Refresh Token
```python
headers = {'Authorization': f'Bearer {refresh_token}'}
response = requests.post('http://localhost:5000/api/auth/refresh', headers=headers)
new_access_token = response.json()['data']['access_token']
```

## 🌐 JavaScript/Frontend Examples

### Register
```javascript
const response = await fetch('http://localhost:5000/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'newuser',
    email: 'new@example.com',
    password: 'Secure@123'
  })
});
const { data } = await response.json();
const { access_token, refresh_token } = data;
```

### Login
```javascript
const response = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'new@example.com',
    password: 'Secure@123'
  })
});
const { data } = await response.json();
localStorage.setItem('access_token', data.access_token);
localStorage.setItem('refresh_token', data.refresh_token);
```

### Protected Request
```javascript
const token = localStorage.getItem('access_token');
const response = await fetch('http://localhost:5000/api/auth/me', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const { data } = await response.json();
```

### Refresh Token
```javascript
const refreshToken = localStorage.getItem('refresh_token');
const response = await fetch('http://localhost:5000/api/auth/refresh', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${refreshToken}` }
});
const { data } = await response.json();
localStorage.setItem('access_token', data.access_token);
```

## ⚠️ Common Errors

### 401 Unauthorized
- **Cause:** Missing, invalid, or expired token
- **Solution:** Login again or refresh token

### 403 Forbidden
- **Cause:** Insufficient permissions (wrong role)
- **Solution:** Check user role matches route requirements

### 409 Conflict
- **Cause:** Username or email already exists
- **Solution:** Use different username/email

### 400 Bad Request
- **Cause:** Invalid input (weak password, invalid email)
- **Solution:** Check validation requirements

## 🔧 Configuration

Edit `.env` file:
```env
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour
JWT_REFRESH_TOKEN_EXPIRES=2592000  # 30 days
```

## 📝 Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message here"
}
```

## 🎯 Best Practices

1. **Store tokens securely** - Use httpOnly cookies or secure storage
2. **Always use HTTPS** - Never send tokens over HTTP in production
3. **Handle token expiration** - Implement automatic token refresh
4. **Logout properly** - Clear tokens from storage
5. **Validate on backend** - Never trust frontend validation alone

## 🚨 Security Notes

- Tokens are stateless (no server-side session storage)
- Access tokens expire after 1 hour
- Refresh tokens expire after 30 days
- Passwords are hashed with bcrypt (never stored in plain text)
- Failed login attempts should be rate-limited (not yet implemented)

---

**Need help?** Check `PHASE3_COMPLETE.md` for detailed documentation.
