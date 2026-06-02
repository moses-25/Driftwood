# Phase 3: Authentication routes
from .auth_routes import auth_bp

# Phase 4: Core API routes
from .product_routes import product_bp
from .category_routes import category_bp
from .order_routes import order_bp
from .payment_routes import payment_bp
from .user_routes import user_bp

# Phase 6: File upload routes
from .upload_routes import upload_bp

# Phase 7: Advanced features routes
from .review_routes import review_bp
from .analytics_routes import analytics_bp
from .inventory_routes import inventory_bp
from .notification_routes import notification_bp

# Contact form routes
from .contact_routes import contact_bp

def register_routes(app):
    """Register all route blueprints"""
    # Authentication routes
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    # Phase 4: Core API routes
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(category_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(payment_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    
    # Phase 6: File upload routes
    app.register_blueprint(upload_bp, url_prefix='/api')
    
    # Phase 7: Advanced features routes
    app.register_blueprint(review_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    app.register_blueprint(inventory_bp, url_prefix='/api')
    app.register_blueprint(notification_bp)  # Already has /api/notifications prefix
    
    # Contact form routes
    app.register_blueprint(contact_bp, url_prefix='/api')
    
    # Simple health check route
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': 'Driftwood Cafe API is running'}
    
    @app.route('/')
    def index():
        return {'message': 'Welcome to Driftwood Cafe API'}