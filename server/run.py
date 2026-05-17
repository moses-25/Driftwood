#!/usr/bin/env python3
"""
Development server runner for Driftwood Café Backend
"""

from app import create_app
from utils.database import init_database

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Initialize database on first run
        init_database()
    
    # Run the development server
    app.run(debug=True, host='0.0.0.0', port=5000)