# 🎯 START HERE - Driftwood Café

## 🚀 Quick Start (3 Steps)

### 1. Start Backend (Terminal 1)
```bash
cd server
source .venv/bin/activate
python run.py
```
✅ Backend runs at: **http://localhost:5000**

### 2. Start Frontend (Terminal 2)
```bash
cd client
npm run dev
```
✅ Frontend runs at: **http://localhost:5173**

### 3. Open Browser
Visit: **http://localhost:5173**

---

## ⚙️ Configuration Required

### Email Setup (For Contact Form & Newsletter)

Edit `server/.env`:
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password  # Not your regular password!
OWNER_EMAIL=owner@example.com
```

**For Gmail:**
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use that password in `MAIL_PASSWORD`

---

## ✅ What's Working

### Frontend Features:
- ✅ Menu browsing (Hot, Cold, Pastries, Specials, Merch)
- ✅ Shopping cart with persistence
- ✅ Checkout (pickup & delivery)
- ✅ Contact form
- ✅ Newsletter subscription
- ✅ Product search
- ✅ Reviews display
- ✅ Gallery
- ✅ Map integration

### Backend Routes:
- ✅ All product endpoints
- ✅ Order creation (guest checkout)
- ✅ Contact form submission
- ✅ Newsletter subscription
- ✅ Payment integration (M-Pesa)
- ✅ Admin features (with auth)

---

## 🧪 Test Everything

```bash
cd server
python test_routes.py
```

This will test:
- Health check
- Contact form
- Newsletter subscription
- Product listing
- Order creation

---

## 📚 Documentation

- **QUICK_START.md** - Detailed setup guide
- **ROUTES_FIXED.md** - All API routes & fixes applied
- **README.md** - Full project documentation

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check PostgreSQL
pg_isready

# Check database exists
psql -l | grep driftwood_cafe

# Create if missing
createdb driftwood_cafe
```

### Contact form not working?
- Check email configuration in `server/.env`
- Use Gmail App Password, not regular password
- Check backend terminal for error messages

### Orders not working?
```bash
# Seed sample data
cd server
source .venv/bin/activate
python -c "from utils.database import seed_menu_data; seed_menu_data()"
```

---

## 🎉 You're Ready!

1. ✅ Start backend: `cd server && source .venv/bin/activate && python run.py`
2. ✅ Start frontend: `cd client && npm run dev`
3. ✅ Visit: http://localhost:5173
4. ✅ Test contact form at: http://localhost:5173/#visit
5. ✅ Test ordering: Add items to cart → Checkout

---

## 📞 Need Help?

Check the documentation:
- Setup issues → **QUICK_START.md**
- Route issues → **ROUTES_FIXED.md**
- General info → **README.md**

Run tests:
```bash
cd server
python test_routes.py
```

---

**Everything is configured and ready to go!** 🚀
