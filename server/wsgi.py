"""
WSGI entry point for production deployment
"""

from flask_migrate import upgrade
from app import create_app

application = create_app()

with application.app_context():
    upgrade()

if __name__ == "__main__":
    application.run()