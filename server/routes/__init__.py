from .menu_routes import menu_bp
from .order_routes import order_bp
from .customer_routes import customer_bp

def register_routes(app):
    """Register all route blueprints"""
    app.register_blueprint(menu_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(customer_bp, url_prefix='/api')