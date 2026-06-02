# 🚀 Driftwood Café - Quick Start Guide

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+
- **PostgreSQL** 12+

---

## 🏃 Quick Start (2 Terminals)

### Terminal 1: Backend

```bash
./start-backend.sh
```

Or manually:
```bash
cd server
source .venv/bin/activate
python run.py
```

**Backend will run at:** http://localhost:5000

### Terminal 2: Frontend

```bash
./start-frontend.sh
```

Or manually:
```bash
cd client
npm run dev
```

**Frontend will run at:** http://localhost:5173

---

## 🔧 First Time Setup

### 1. Backend Setup

```bash
cd server

# Create virtual environment (if not exists)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb driftwood_cafe  # Create PostgreSQL database

# Run migrations
flask db upgrade

# Seed sample data (optional)
python -c "from utils.database import seed_menu_data; seed_menu_data()"
```

### 2. Frontend Setup

```bash
cd client

# Install dependencies
npm install
```

### 3. Environment Variables

**Backend (.env in server/):**
```bash
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/driftwood_cafe
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CLIENT_ORIGIN=http://localhost:5173
PORT=5000

# Email Configuration (for contact form & newsletter)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
OWNER_EMAIL=owner@example.com

# M-Pesa (optional, for payments)
MPESA_CONSUMER_KEY=your_key
MPESA_CONSUMER_SECRET=your_secret
MPESA_SHORTCODE=your_shortcode
MPESA_PASSKEY=your_passkey
```

**Frontend (.env in client/):**
```bash
VITE_API_URL=http://localhost:5000
```

---

## ✅ Verify Everything Works

### 1. Check Backend Health

```bash
curl http://localhost:5000/api/health
```

Should return:
```json
{"status":"ok","message":"Driftwood Cafe API is running"}
```

### 2. Test All Routes

```bash
cd server
python test_routes.py
```

### 3. Open Frontend

Visit: http://localhost:5173

---

## 📋 Available Features

### ✅ Working Features:

1. **Menu Display** - Browse hot drinks, cold brews, pastries, specials, and merchandise
2. **Shopping Cart** - Add items, customize orders, persistent storage (24h TTL)
3. **Checkout** - Guest checkout with pickup/delivery options
4. **Order Management** - Create and track orders
5. **Contact Form** - Send messages to café owner
6. **Newsletter Subscription** - Subscribe to updates
7. **Product Search** - Search and filter menu items
8. **Reviews** - View customer reviews
9. **Gallery** - Browse café photos
10. **Map Integration** - Find café location

### 🔐 Admin Features (Requires Authentication):

- Product management
- Order status updates
- Inventory tracking
- Analytics dashboard
- User management

---

## 🐛 Troubleshooting

### Backend won't start?

**Check PostgreSQL:**
```bash
pg_isready
```

**Check database exists:**
```bash
psql -l | grep driftwood_cafe
```

**Create database if missing:**
```bash
createdb driftwood_cafe
```

**Check port 5000:**
```bash
lsof -i :5000
```

### Frontend won't start?

**Check port 5173:**
```bash
lsof -i :5173
```

**Clear and reinstall:**
```bash
cd client
rm -rf node_modules package-lock.json
npm install
```

### Contact form not working?

**Check email configuration in server/.env:**
- `MAIL_SERVER` - SMTP server
- `MAIL_USERNAME` - Your email
- `MAIL_PASSWORD` - App password (not regular password)
- `OWNER_EMAIL` - Where contact forms are sent

**For Gmail:**
1. Enable 2-factor authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password in `MAIL_PASSWORD`

### Newsletter subscription not working?

Same as contact form - requires email configuration.

### Orders not working?

**Check products exist:**
```bash
curl http://localhost:5000/api/products
```

**Check categories exist:**
```bash
curl http://localhost:5000/api/categories
```

**Seed sample data if empty:**
```bash
cd server
source .venv/bin/activate
python -c "from utils.database import seed_menu_data; seed_menu_data()"
```

---

## 🎯 Production Deployment

### Frontend Build

```bash
cd client
npm run build
# Output in client/dist/
```

### Backend Production

```bash
cd server
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:application
```

### Environment Variables for Production

Update `.env` files with:
- Strong `SECRET_KEY` and `JWT_SECRET_KEY`
- Production database URL
- Production `CLIENT_ORIGIN` (your frontend URL)
- Real M-Pesa credentials
- Production email settings

---

## 📞 Support

If you encounter issues:

1. Check this guide first
2. Run `python test_routes.py` to test backend
3. Check browser console for frontend errors
4. Check terminal output for backend errors
5. Verify `.env` files are configured correctly

---

## 🎉 You're All Set!

Visit http://localhost:5173 and start exploring Driftwood Café!
