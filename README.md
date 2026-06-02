<div align="center">

# Driftwood Café

### *Modern Full-Stack Coffee Shop Experience*

[![React](https://img.shields.io/badge/React-19.2.5-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Vite](https://img.shields.io/badge/Vite-8.0.10-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-4.2.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

**A modern, full-stack coffee shop application featuring a React frontend with smooth animations and a robust Python/Flask backend with PostgreSQL database.**

[Quick Start](#quick-start) • [Documentation](#documentation) • [API Endpoints](#api-endpoints) • [Docker Setup](#docker-setup-alternative)

</div>

---

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Environment Configuration](#environment-configuration)
- [Payment Integration](#payment-integration)
- [Testing](#testing)
- [Deployment](#deployment)

---

## Features

<table>
<tr>
<td width="50%">

### **Customer Experience**

- Interactive menu with 5+ categories
- Smart shopping cart (24hr TTL)
- Smooth animations & scrolling
- Fully responsive design
- Multiple payment methods
- Real-time order tracking

</td>
<td width="50%">

### **Business Management**

- RESTful API architecture
- Order processing & analytics
- Customer data management
- M-Pesa integration
- Inventory management
- Admin control panel

</td>
</tr>
</table>

---

## Technology Stack

<div align="center">

### Frontend Stack
| Technology | Version | Purpose |
|:----------:|:-------:|:-------:|
| ![React](https://img.shields.io/badge/-React-61DAFB?logo=react&logoColor=white&style=flat-square) | 19.2.5 | UI Framework |
| ![Vite](https://img.shields.io/badge/-Vite-646CFF?logo=vite&logoColor=white&style=flat-square) | 8.0.10 | Build Tool |
| ![TailwindCSS](https://img.shields.io/badge/-Tailwind-38B2AC?logo=tailwind-css&logoColor=white&style=flat-square) | 4.2.4 | Styling |
| ![Framer Motion](https://img.shields.io/badge/-Framer-0055FF?logo=framer&logoColor=white&style=flat-square) | 12.38.0 | Animations |

### Backend Stack
| Technology | Version | Purpose |
|:----------:|:-------:|:-------:|
| ![Flask](https://.shields.io/badge/-Flask-000000?logo=flask&logoColor=white&style=flat-sqimguare) | 3.0.0 | API Framework |
| ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?logo=postgresql&logoColor=white&style=flat-square) | 12+ | Database |
| ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-D71F00?logoColor=white&style=flat-square) | Latest | ORM |
| ![Gunicorn](https://img.shields.io/badge/-Gunicorn-499848?logo=gunicorn&logoColor=white&style=flat-square) | Latest | WSGI Server |

</div>

---

## Project Structure

```
driftwood-cafe/
│
├── client/                     # React Frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Main page components
│   │   ├── context/           # React Context for state
│   │   ├── data/              # Static data and mock data
│   │   ├── hooks/             # Custom React hooks
│   │   ├── utils/             # Utility functions
│   │   └── animations/        # Animation components
│   ├── public/                # Static assets
│   ├── package.json
│   └── vite.config.js
│
├── server/                    # Python/Flask Backend
│   ├── models/                # Database models
│   │   ├── menu_item.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   └── order_item.py
│   ├── routes/                # API route handlers
│   │   ├── menu_routes.py
│   │   ├── order_routes.py
│   │   └── customer_routes.py
│   ├── services/              # Business logic
│   │   └── payment_service.py
│   ├── utils/                 # Utilities and database helpers
│   ├── tests/                 # Unit tests
│   ├── migrations/            # Database migrations
│   ├── app.py                # Flask application factory
│   ├── config.py              # Configuration management
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Container configuration
│   └── docker-compose.yml    # Multi-service setup
│
└── README.md
```

---

## Quick Start

### Prerequisites

<table>
<tr>
<td width="50%">

**Frontend Requirements**
```bash
Node.js 18+
npm or yarn
```

</td>
<td width="50%">

**Backend Requirements**
```bash
Python 3.8+
PostgreSQL 12+
```

</td>
</tr>
</table>

---

### Frontend Setup

```bash
# Navigate to client directory
cd client

# Install dependencies
npm install

# Start development server
npm run dev
```

<div align="center">

**Frontend runs at:** `http://localhost:5173`

</div>

---

### Backend Setup

```bash
# Navigate to server directory
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

<div align="center">

**Backend API runs at:** `http://localhost:5000`

</div>

---

### Docker Setup (Alternative)

```bash
# Navigate to server directory
cd server

# Build and run with Docker Compose
docker-compose up --build
```

<div align="center">

**That's it! Your app is now running!**

</div>

---

## API Endpoints

### Menu Management

| Method | Endpoint | Description | Auth Required |
|:------:|:---------|:------------|:-------------:|
| `GET` | `/api/menu` | Fetch all menu items | No |
| `GET` | `/api/menu/{category}` | Fetch items by category | No |
| `GET` | `/api/menu/item/{id}` | Fetch single item details | No |
| `POST` | `/api/menu` | Create new menu item | Admin |
| `PUT` | `/api/menu/item/{id}` | Update menu item | Admin |

---

### Order Management

| Method | Endpoint | Description | Auth Required |
|:------:|:---------|:------------|:-------------:|
| `POST` | `/api/orders` | Create new order | No |
| `GET` | `/api/orders/{id}` | Get order details | Yes |
| `GET` | `/api/orders/{order_number}` | Get order by number | Yes |
| `PUT` | `/api/orders/{id}/status` | Update order status | Admin |
| `GET` | `/api/orders` | List orders with filtering | Admin |

---

### Customer Management

| Method | Endpoint | Description | Auth Required |
|:------:|:---------|:------------|:-------------:|
| `POST` | `/api/customers` | Create/update customer | No |
| `GET` | `/api/customers/{email}` | Get customer by email | Yes |
| `GET` | `/api/customers/{id}/orders` | Get customer order history | Yes |

---

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

---

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

---

## Environment Configuration

### Frontend `.env` (in `client/`)

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:5000/api

# Payment Configuration
VITE_PAYMENT_PUBLIC_KEY=your_payment_key
VITE_MPESA_SHORTCODE=your_mpesa_code
```

---

### Backend `.env` (in `server/`)

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/driftwood_cafe

# Security
SECRET_KEY=your-secret-key-here

# M-Pesa Integration
MPESA_CONSUMER_KEY=your_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
MPESA_SHORTCODE=your_mpesa_shortcode
MPESA_PASSKEY=your_mpesa_passkey
```

> **Important:** Never commit `.env` files to version control!

---

## Payment Integration

<div align="center">

The system supports multiple payment methods:

| Payment Method | Status | Integration |
|:--------------:|:------:|:-----------:|
| **M-Pesa** | Active | STK Push |
| **Card Payments** | Coming Soon | Gateway Ready |
| **Cash** | Active | Pickup Orders |

</div>

---

## Testing

### Frontend Testing

```bash
cd client

# Run linter
npm run lint

# Test production build
npm run build
```

---

### Backend Testing

```bash
cd server

# Install testing dependencies
pip install pytest pytest-flask

# Run test suite
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov
```

<div align="center">

**Always test before committing!**

</div>

---

## Deployment

### Frontend Deployment (Vercel/Netlify)

```bash
cd client

# Build for production
npm run build

# Deploy dist/ folder
```

---

### Backend Deployment (Production)

```bash
cd server

# Set production environment
export FLASK_ENV=production

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:application
```

---

### Docker Deployment

```bash
cd server

# Build Docker image
docker build -t driftwood-backend .

# Run container
docker run -p 5000:5000 driftwood-backend
```

---

## Development Workflow

<div align="center">

```mermaid
graph LR
    A[Frontend Dev] -->|Hot Reload| B[Vite Server]
    C[Backend Dev] -->|Auto Reload| D[Flask Server]
    E[Database] -->|Migrations| F[Flask-Migrate]
    G[Testing] -->|Before Commit| H[Git Push]
```

</div>

### Best Practices

1. **Frontend Development:** Use Vite's hot reload for rapid UI development
2. **Backend Development:** Flask development server with auto-reload
3. **Database Changes:** Use Flask-Migrate for schema management
4. **Testing:** Run tests before committing changes
5. **Integration:** Test frontend-backend integration regularly

---

## Browser Support

<div align="center">

| Browser | Minimum Version |
|:-------:|:---------------:|
| ![Chrome](https://img.shields.io/badge/-Chrome-4285F4?logo=google-chrome&logoColor=white&style=flat-square) | 90+ |
| ![Firefox](https://img.shields.io/badge/-Firefox-FF7139?logo=firefox&logoColor=white&style=flat-square) | 88+ |
| ![Safari](https://img.shields.io/badge/-Safari-000000?logo=safari&logoColor=white&style=flat-square) | 14+ |
| ![Edge](https://img.shields.io/badge/-Edge-0078D7?logo=microsoft-edge&logoColor=white&style=flat-square) | 90+ |

</div>

---

## Contributing

We welcome contributions! Here's how to get started:

<div align="center">

```mermaid
graph LR
    A[Fork Repo] --> B[Create Branch]
    B --> C[Make Changes]
    C --> D[Test]
    D --> E[Commit]
    E --> F[Push]
    F --> G[Pull Request]
```

</div>

### Steps

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Make** your changes
4. **Test** both frontend and backend
5. **Commit** your changes
   ```bash
   git commit -m 'feat: Add amazing feature'
   ```
6. **Push** to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
7. **Open** a Pull Request

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Documentation

<div align="center">

### Comprehensive Documentation

</div>

<table>
<tr>
<td width="50%">

#### Quick Access
- **[Complete Project Status](./docs/COMPLETE_PROJECT_STATUS.md)**
  <br/>Full system overview
- **[Security Quick Fix](./docs/SECURITY_QUICK_FIX.md)**
  <br/>Security guidelines
- **[Image Upload Guide](./docs/START_HERE_IMAGES.md)**
  <br/>Add product images

</td>
<td width="50%">

#### Documentation Categories
- **Getting Started** - Setup guides and checklists
- **Feature Fixes** - Bug fixes and improvements
- **Image Upload** - Product image management
- **Security** - Best practices
- **API Reference** - Endpoint documentation

</td>
</tr>
</table>

<div align="center">

**[View All Documentation](./docs/README.md)**

</div>

---

## Support

<div align="center">

Need help? We're here for you!

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red?style=for-the-badge&logo=github)](https://github.com/yourusername/driftwood-cafe/issues)
[![Discussions](https://img.shields.io/badge/GitHub-Discussions-blue?style=for-the-badge&logo=github)](https://github.com/yourusername/driftwood-cafe/discussions)

For questions or support, please open an issue in the GitHub repository.

</div>

---

<div align="center">

### Star this repo if you find it helpful!

**Made with coffee and love by the Driftwood Team**

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/driftwood-cafe?style=social)](https://github.com/yourusername/driftwood-cafe)
[![GitHub Forks](https://img.shields.io/github/forks/yourusername/driftwood-cafe?style=social)](https://github.com/yourusername/driftwood-cafe)

</div>