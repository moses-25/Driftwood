# Driftwood Café - Frontend Integration Guide

## Overview
This document explains the frontend architecture of Driftwood Café to help the backend team understand how to integrate with the React-based client application.

## Frontend Technology Stack
- **Framework**: React 19.2.5 with Vite 8.0.10
- **Styling**: Tailwind CSS 4.2.4
- **Animations**: Framer Motion 12.38.0
- **Smooth Scrolling**: Lenis 1.3.23
- **State Management**: React Context API
- **Build Tool**: Vite with ES modules

## Project Structure
```
client/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── checkout/        # Checkout-specific components
│   │   ├── CartItem.jsx     # Individual cart item component
│   │   ├── MenuCard.jsx     # Menu item display component
│   │   ├── Navbar.jsx       # Navigation component
│   │   └── ...
│   ├── pages/               # Main page components
│   │   ├── Hero.jsx         # Landing section
│   │   ├── Menu.jsx         # Menu display page
│   │   ├── Cart.jsx         # Shopping cart page
│   │   ├── Checkout.jsx     # Checkout process page
│   │   └── ...
│   ├── context/             # State management
│   │   └── CartContext.jsx  # Shopping cart state
│   ├── data/                # Static data and mock data
│   │   └── menuData.js      # Menu items, gallery, reviews
│   ├── hooks/               # Custom React hooks
│   ├── utils/               # Utility functions
│   └── animations/          # Animation components
├── public/                  # Static assets
└── package.json
```

## Key Frontend Features

### 1. Single Page Application (SPA)
- Uses hash-based routing (`#cart`, `#checkout`)
- Smooth scrolling between sections
- No page reloads for navigation

### 2. Shopping Cart System
- **State Management**: React Context with localStorage persistence
- **Cart Persistence**: 24-hour TTL in localStorage
- **Cart Operations**: Add, remove, update quantities, clear cart
- **Item Identification**: Uses `cartItemId` for line items with customizations

### 3. Menu System
- **Categories**: Hot drinks, Cold drinks, Pastries, Specials, Merchandise
- **Item Structure**: Each item has id, name, description, price (KES currency), image
- **Customizations**: Support for item modifications (size, milk type, etc.)

## Data Structures Expected by Frontend

### Menu Item Structure
```javascript
{
  id: number,
  category: "hot" | "cold" | "pastries" | "specials" | "merch",
  name: string,
  description: string,
  price: string, // Format: "KES 350"
  image: string, // Image URL or path
  tag?: "Bestseller" | "New" | null // Optional tag for merchandise
}
```

### Cart Item Structure
```javascript
{
  id: number,           // Product catalog ID
  cartItemId: string,   // Unique line item ID (includes customizations)
  name: string,
  price: string,        // Format: "KES 350"
  image: string,
  quantity: number,
  customizations?: {    // Optional customizations
    size?: string,
    milk?: string,
    extras?: string[]
  }
}
```

### Order Structure (for checkout)
```javascript
{
  items: CartItem[],
  customerInfo: {
    name: string,
    email: string,
    phone: string
  },
  deliveryInfo?: {
    address: string,
    instructions?: string
  },
  paymentMethod: "card" | "mpesa" | "cash",
  totalAmount: number,
  orderType: "pickup" | "delivery"
}
```

## API Endpoints Needed

### Menu Management
- `GET /api/menu` - Fetch all menu items
- `GET /api/menu/:category` - Fetch items by category
- `GET /api/menu/item/:id` - Fetch single item details

### Order Management
- `POST /api/orders` - Create new order
- `GET /api/orders/:id` - Get order details
- `PUT /api/orders/:id/status` - Update order status

### Customer Management
- `POST /api/customers` - Create/update customer info
- `GET /api/customers/:email` - Get customer by email

## Frontend Behavior Notes

### Cart Functionality
- Cart persists in localStorage with 24-hour expiration
- Automatically clears legacy price formats (migration safety)
- Supports quantity updates and item removal
- Calculates totals client-side but should be verified server-side

### Navigation
- Hash-based routing: `#cart`, `#checkout`, `#section-name`
- Smooth scrolling to sections on main page
- Full-page overlays for cart and checkout

### State Management
- Uses React Context for cart state
- No external state management library
- Local storage for persistence

## Development Commands
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## Integration Points

### 1. Menu Data
Replace static `menuData.js` with API calls to fetch real-time menu data, pricing, and availability.

### 2. Order Processing
Implement order submission endpoint that accepts the cart structure and customer information.

### 3. Payment Integration
Add payment processing for M-Pesa and card payments during checkout.

### 4. Real-time Updates
Consider WebSocket integration for order status updates and menu availability.

### 5. Image Management
Set up proper image hosting/CDN for menu item images and optimize for web delivery.

## Environment Variables Needed
```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_PAYMENT_PUBLIC_KEY=your_payment_key
VITE_MPESA_SHORTCODE=your_mpesa_code
```

## Notes for Backend Team
1. **Currency Format**: Frontend expects prices as strings in "KES XXX" format
2. **Image URLs**: Provide full URLs for menu item images
3. **CORS**: Enable CORS for the frontend domain
4. **Validation**: Validate all cart totals server-side for security
5. **Error Handling**: Return consistent error response format for frontend error handling

## Contact
For questions about frontend integration, refer to the frontend team or check the component implementations in the `client/src` directory.
---


## Backend Setup Instructions

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone and Navigate to Server Directory**
   ```bash
   cd server
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL Database**
   ```bash
   # Create database
   createdb driftwood_cafe
   
   # Or using psql
   psql -c "CREATE DATABASE driftwood_cafe;"
   ```

5. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```

6. **Initialize Database**
   ```bash
   # Initialize Flask-Migrate
   flask db init
   
   # Create initial migration
   flask db migrate -m "Initial migration"
   
   # Apply migrations
   flask db upgrade
   
   # Seed with sample data
   python -c "from utils.database import seed_menu_data; seed_menu_data()"
   ```

7. **Run Development Server**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:5000`

### Docker Setup (Alternative)

1. **Using Docker Compose**
   ```bash
   docker-compose up --build
   ```

   This will start both PostgreSQL and the Flask application.

### API Testing

Test the API endpoints:

```bash
# Get all menu items
curl http://localhost:5000/api/menu

# Get items by category
curl http://localhost:5000/api/menu/hot

# Create a test order
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customerInfo": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+254700000000"
    },
    "items": [
      {
        "id": 1,
        "quantity": 2
      }
    ],
    "totalAmount": 700,
    "orderType": "pickup",
    "paymentMethod": "cash"
  }'
```

### Database Migrations

When you make changes to models:

```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

### Production Deployment

1. **Set Environment Variables**
   ```bash
   export FLASK_ENV=production
   export DATABASE_URL=postgresql://user:pass@host:port/dbname
   ```

2. **Use Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:application
   ```

3. **Or Deploy with Docker**
   ```bash
   docker build -t driftwood-backend .
   docker run -p 5000:5000 driftwood-backend
   ```

### Project Structure

```
server/
├── app.py                 # Flask application factory
├── config.py             # Configuration settings
├── extensions.py         # Flask extensions initialization
├── run.py               # Development server runner
├── wsgi.py              # Production WSGI entry point
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── models/             # Database models
│   ├── __init__.py
│   ├── menu_item.py
│   ├── customer.py
│   ├── order.py
│   └── order_item.py
├── routes/             # API route handlers
│   ├── __init__.py
│   ├── menu_routes.py
│   ├── order_routes.py
│   └── customer_routes.py
├── services/           # Business logic services
│   ├── __init__.py
│   └── payment_service.py
├── utils/              # Utility functions
│   ├── __init__.py
│   └── database.py
├── tests/              # Unit tests
│   ├── __init__.py
│   └── test_menu_routes.py
└── migrations/         # Database migrations
```

### Testing

Run tests:
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
python -m pytest tests/
```

### M-Pesa Integration

To enable M-Pesa payments:

1. Register with Safaricom Developer Portal
2. Get your Consumer Key, Consumer Secret, and Shortcode
3. Add credentials to `.env` file
4. Update the callback URL in `payment_service.py`

### Troubleshooting

**Database Connection Issues:**
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

**Import Errors:**
- Ensure virtual environment is activated
- Install all requirements: `pip install -r requirements.txt`

**Migration Issues:**
- Delete `migrations/` folder and reinitialize: `flask db init`
- Check for circular imports in models

### API Documentation

The API follows RESTful conventions:

- `GET /api/menu` - List all menu items
- `GET /api/menu/{category}` - List items by category
- `GET /api/menu/item/{id}` - Get specific menu item
- `POST /api/orders` - Create new order
- `GET /api/orders/{id}` - Get order details
- `PUT /api/orders/{id}/status` - Update order status
- `POST /api/customers` - Create/update customer
- `GET /api/customers/{email}` - Get customer by email

All responses follow the format:
```json
{
  "success": true|false,
  "data": {...},
  "error": "Error message if success is false"
}
```