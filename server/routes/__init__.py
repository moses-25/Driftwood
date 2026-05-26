# Phase 3: Authentication routes
from .auth_routes import auth_bp
from .protected_example import protected_bp

# Phase 4: Core API routes
from .product_routes import product_bp
from .category_routes import category_bp
from .order_routes import order_bp
from .payment_routes import payment_bp
from .user_routes import user_bp

# Legacy routes (to be deprecated)
# from .menu_routes import menu_bp  # Replaced by product_routes
# from .customer_routes import customer_bp  # Replaced by user_routes

def register_routes(app):
    """Register all route blueprints"""
    # Authentication routes
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(protected_bp, url_prefix='/api')  # Example protected routes
    
    # Phase 4: Core API routes
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(category_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(payment_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    
    # Simple health check route
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': 'Driftwood Cafe API is running'}
    
    @app.route('/')
    def index():
        return {'message': 'Welcome to Driftwood Cafe API'}