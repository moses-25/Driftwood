# Temporarily commented out during Phase 2 model migration
# from .menu_routes import menu_bp
# from .order_routes import order_bp
# from .customer_routes import customer_bp
from .auth_routes import auth_bp
from .protected_example import protected_bp

def register_routes(app):
    """Register all route blueprints"""
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(protected_bp, url_prefix='/api')  # Example protected routes

    # Temporarily disabled during Phase 2 migration
    # app.register_blueprint(menu_bp, url_prefix='/api')
    # app.register_blueprint(order_bp, url_prefix='/api')
    # app.register_blueprint(customer_bp, url_prefix='/api')
    
    # Simple health check route
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': 'Driftwood Cafe API is running'}
    
    @app.route('/')
    def index():
        return {'message': 'Welcome to Driftwood Cafe API'}