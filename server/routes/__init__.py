# Temporarily commented out during Phase 2 model migration
# from .menu_routes import menu_bp
# from .order_routes import order_bp
# from .customer_routes import customer_bp

def register_routes(app):
    """Register all route blueprints"""
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