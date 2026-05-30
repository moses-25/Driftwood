from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt, mail
from routes import register_routes
from database.connection import test_database_connection

def test():
    is_connected = test_database_connection()

    if not is_connected:
        raise RuntimeError("Database connection failed. Application cannot start.")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Import all models so Alembic can see the full schema for migrations
    from models.user import User
    from models.product import Product
    from models.category import Category
    from models.order import Order
    from models.order_item import OrderItem
    from models.review import Review
    from models.payment import Payment
    from models.stock_adjustment import StockAdjustment
    from models.order_status_history import OrderStatusHistory
    from models.notification_preference import NotificationPreference

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    
    # Configure CORS with specific origin
    client_origin = app.config.get('CLIENT_ORIGIN', 'http://localhost:5173')
    CORS(app, resources={
        r"/api/*": {
            "origins": [client_origin],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })
    
    # Register routes
    register_routes(app)
    
    test()
    return app