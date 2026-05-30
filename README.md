# Driftwood Café

A modern, full-stack coffee shop application featuring a React frontend with smooth animations and a robust Python/Flask backend with PostgreSQL database. Built for seamless online ordering, menu management, and customer experience.

## Project Overview

Driftwood Café is a comprehensive coffee shop management system that provides customers with an intuitive ordering experience and businesses with powerful backend tools for managing orders, payments, and customer data.

### Key Features

**Customer Experience:**
- Interactive menu with categories (Hot, Cold, Pastries, Specials, Merchandise)
- Shopping cart with persistent storage and 24-hour TTL
- Smooth scrolling single-page application
- Responsive design with custom animations
- Checkout process with multiple payment options
- Order tracking and status updates

**Business Management:**
- RESTful API for menu management
- Order processing and status tracking
- Customer data management
- Payment integration (M-Pesa, Cash)
- Database-driven inventory and pricing
- Admin tools for menu updates

## Technology Stack

### Frontend (Client)
- **Framework:** React 19.2.5 with Vite 8.0.10
- **Styling:** Tailwind CSS 4.2.4
- **Animations:** Framer Motion 12.38.0
- **Smooth Scrolling:** Lenis 1.3.23
- **State Management:** React Context API
- **Build Tool:** Vite with ES modules
- **Fonts:** Multiple Google Fonts integration

### Backend (Server)
- **Framework:** Flask 3.0.0 (Python)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Migrations:** Flask-Migrate
- **API:** RESTful endpoints with JSON responses
- **Payment Processing:** M-Pesa STK Push integration
- **CORS:** Flask-CORS for cross-origin requests
- **Production Server:** Gunicorn WSGI server

## Project Structure

```
driftwood-cafe/
├── client/                    # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Main page components
│   │   ├── context/          # React Context for state
│   │   ├── data/             # Static data and mock data
│   │   ├── hooks/            # Custom React hooks
│   │   ├── utils/            # Utility functions
│   │   └── animations/       # Animation components
│   ├── public/               # Static assets
│   ├── package.json
│   └── vite.config.js
├── server/                   # Python/Flask Backend
│   ├── models/               # Database models
│   │   ├── menu_item.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   └── order_item.py
│   ├── routes/               # API route handlers
│   │   ├── menu_routes.py
│   │   ├── order_routes.py
│   │   └── customer_routes.py
│   ├── services/             # Business logic
│   │   └── payment_service.py
│   ├── utils/                # Utilities and database helpers
│   ├── tests/                # Unit tests
│   ├── migrations/           # Database migrations
│   ├── app.py               # Flask application factory
│   ├── config.py            # Configuration management
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Container configuration
│   └── docker-compose.yml   # Multi-service setup
└── README.md
```

## Quick Start

### Prerequisites
- **Frontend:** Node.js 18+ and npm
- **Backend:** Python 3.8+ and PostgreSQL 12+

### Frontend Setup
```bash
cd client
npm install
npm run dev
```
Frontend runs at: http://localhost:5173

### Backend Setup
```bash
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb driftwood_cafe
cp .env.example .env
# Edit .env with your database credentials

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed sample data
python -c "from utils.database import seed_menu_data; seed_menu_data()"

# Run development server
python run.py
```
Backend API runs at: http://localhost:5000

### Docker Setup (Alternative)
```bash
cd server
docker-compose up --build
```

## API Endpoints

### Menu Management
- `GET /api/menu` - Fetch all menu items
- `GET /api/menu/{category}` - Fetch items by category
- `GET /api/menu/item/{id}` - Fetch single item details
- `POST /api/menu` - Create new menu item (admin)
- `PUT /api/menu/item/{id}` - Update menu item (admin)

### Order Management
- `POST /api/orders` - Create new order
- `GET /api/orders/{id}` - Get order details
- `GET /api/orders/{order_number}` - Get order by number
- `PUT /api/orders/{id}/status` - Update order status
- `GET /api/orders` - List orders with filtering

### Customer Management
- `POST /api/customers` - Create/update customer
- `GET /api/customers/{email}` - Get customer by email
- `GET /api/customers/{id}/orders` - Get customer order history

## Data Models

### Menu Item
```json
{
  "id": 1,
  "name": "Driftwood Espresso",
  "description": "Double shot, dark roast...",
  "price": "KES 350",
  "category": "hot",
  "image": "/images/hot1.jpg",
  "tag": "Bestseller",
  "is_available": true
}
```

### Order
```json
{
  "id": 1,
  "order_number": "ABC12345",
  "customer": {...},
  "items": [...],
  "total_amount": 700.00,
  "order_type": "pickup",
  "status": "confirmed",
  "payment_method": "mpesa",
  "payment_status": "paid"
}
```

## Environment Configuration

### Frontend (.env in client/)
```bash
VITE_API_BASE_URL=http://localhost:5000/api
VITE_PAYMENT_PUBLIC_KEY=your_payment_key
VITE_MPESA_SHORTCODE=your_mpesa_code
```

### Backend (.env in server/)
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/driftwood_cafe
SECRET_KEY=your-secret-key-here
MPESA_CONSUMER_KEY=your_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
MPESA_SHORTCODE=your_mpesa_shortcode
MPESA_PASSKEY=your_mpesa_passkey
```

## Payment Integration

The system supports multiple payment methods:
- **M-Pesa:** STK Push integration for mobile payments
- **Card Payments:** Ready for integration with payment gateways
- **Cash:** For pickup orders

## Testing

### Frontend
```bash
cd client
npm run lint
npm run build  # Test production build
```

### Backend
```bash
cd server
pip install pytest pytest-flask
python -m pytest tests/
```

## Deployment

### Frontend (Vercel)
```bash
cd client
npm run build
# Deploy dist/ folder
```

### Backend (Production)
```bash
cd server
# Set production environment variables
export FLASK_ENV=production
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:application
```

### Docker Deployment
```bash
cd server
docker build -t driftwood-backend .
docker run -p 5000:5000 driftwood-backend
```

## Development Workflow

1. **Frontend Development:** Use Vite's hot reload for rapid UI development
2. **Backend Development:** Flask development server with auto-reload
3. **Database Changes:** Use Flask-Migrate for schema management
4. **Testing:** Run tests before committing changes
5. **Integration:** Test frontend-backend integration regularly

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b Feature`)
3. Make your changes
4. Test both frontend and backend
5. Commit your changes (`git commit -m 'Added amazing feature'`)
6. Push to the branch (`git push origin Feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 Documentation

Comprehensive documentation is available in the [`/docs`](./docs) folder:

### Quick Links
- **[Complete Project Status](./docs/COMPLETE_PROJECT_STATUS.md)** - Full system overview
- **[Security Quick Fix](./docs/SECURITY_QUICK_FIX.md)** - Security guidelines
- **[Image Upload Guide](./docs/START_HERE_IMAGES.md)** - Add product images
- **[All Documentation](./docs/README.md)** - Complete documentation index

### Documentation Categories
- **Getting Started:** Setup guides and checklists
- **Feature Fixes:** Bug fixes and improvements
- **Image Upload:** Product image management
- **Security:** Security best practices
- **API Reference:** Endpoint documentation

## Support

For questions or support, please open an issue in the GitHub repository or contact the development team.