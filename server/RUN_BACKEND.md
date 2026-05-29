# 🚀 Running Driftwood Cafe Backend

## Quick Start (3 Steps)

### Step 1: Start the Server
```bash
./start_server.sh
```

This will:
- Create virtual environment (if needed)
- Install dependencies
- Check database connection
- Run migrations
- Start the server on http://localhost:5000

### Step 2: Seed the Database (First Time Only)
If the database is empty, open a new terminal and run:
```bash
source env/bin/activate
python3 seed_data.py
```

### Step 3: Test the Backend
Open a new terminal and run:
```bash
./test_backend.sh
```

---

## Manual Setup (If Scripts Don't Work)

### 1. Create Virtual Environment
```bash
python3 -m venv env
source env/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Database
```bash
# Initialize migrations (if not done)
flask db init

# Run migrations
flask db upgrade

# Seed data
python3 seed_data.py
```

### 4. Start Server
```bash
python3 run.py
```

---

## Testing the API

### Using cURL

#### Health Check
```bash
curl http://localhost:5000/api/health
```

#### Get Products
```bash
curl http://localhost:5000/api/products
```

#### Get Categories
```bash
curl http://localhost:5000/api/categories
```

#### Login (Admin)
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@driftwood.com","password":"password123"}'
```

#### Create Order (Guest Checkout)
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"product_id": 1, "quantity": 2}],
    "order_type": "pickup",
    "payment_method": "cash"
  }'
```

### Using Browser

Open these URLs in your browser:
- http://localhost:5000/ - Welcome message
- http://localhost:5000/api/health - Health check
- http://localhost:5000/api/products - All products
- http://localhost:5000/api/categories - All categories

### Using Postman

Import the API endpoints from `API_ENDPOINTS_REFERENCE.md`

---

## Test Credentials

### Admin User
- **Email:** admin@driftwood.com
- **Password:** password123
- **Role:** admin

### Staff User
- **Email:** staff@driftwood.com
- **Password:** password123
- **Role:** staff

### Customer User
- **Email:** john@example.com
- **Password:** password123
- **Role:** customer

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Activate virtual environment and install dependencies
```bash
source env/bin/activate
pip install -r requirements.txt
```

### Issue: "Database connection failed"
**Solution:** Check PostgreSQL is running and .env has correct credentials
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Or start PostgreSQL
sudo systemctl start postgresql
```

### Issue: "Port 5000 already in use"
**Solution:** Kill the process using port 5000
```bash
# Find process
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Issue: "Database is empty"
**Solution:** Run seed data script
```bash
source env/bin/activate
python3 seed_data.py
```

---

## What to Check

### ✅ Backend is Working If:
1. Server starts without errors
2. Health check returns `{"status": "ok"}`
3. Products endpoint returns list of products
4. Categories endpoint returns list of categories
5. Login works with test credentials
6. Guest checkout creates an order

### ❌ Something is Wrong If:
1. Server won't start (check dependencies)
2. Database errors (check PostgreSQL)
3. 404 errors (check routes are registered)
4. 500 errors (check logs for details)

---

## Viewing Logs

Server logs will show in the terminal where you ran `./start_server.sh`

Look for:
- ✅ `Running on http://127.0.0.1:5000` - Server started
- ✅ `200 GET /api/products` - Successful request
- ❌ `500 POST /api/orders` - Server error
- ❌ `404 GET /api/unknown` - Route not found

---

## Next Steps After Backend is Running

1. **Test all endpoints** - Use test_backend.sh or manual testing
2. **Check what's missing** - Review API_ENDPOINTS_REFERENCE.md
3. **Connect frontend** - Point React app to http://localhost:5000
4. **Deploy** - When ready, deploy to production

---

## Quick Reference

### Start Server
```bash
./start_server.sh
```

### Stop Server
Press `Ctrl+C` in the terminal running the server

### Test Backend
```bash
./test_backend.sh
```

### View API Documentation
```bash
cat API_ENDPOINTS_REFERENCE.md
```

### Check Database
```bash
source env/bin/activate
python3 -c "
from app import create_app
from extensions import db
from models import User, Product, Category, Order

app = create_app()
with app.app_context():
    print(f'Users: {User.query.count()}')
    print(f'Products: {Product.query.count()}')
    print(f'Categories: {Category.query.count()}')
    print(f'Orders: {Order.query.count()}')
"
```

---

## 🎉 Success!

If you can:
- ✅ Start the server
- ✅ See products in the API
- ✅ Login with test credentials
- ✅ Create a guest order

**Your backend is fully functional!** 🚀

---

**Need Help?** Check:
- `backend.md` - Complete backend guide
- `API_ENDPOINTS_REFERENCE.md` - All endpoints
- `PHASE4_COMPLETION_SUMMARY.md` - What's implemented
