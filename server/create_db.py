#!/usr/bin/env python3
"""
Direct database creation script for Phase 2
"""

from app import create_app
from extensions import db

def create_database():
    """Create all database tables"""
    app = create_app()
    
    with app.app_context():
        print("🗄️  Creating database tables...")
        
        # Drop all existing tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        
        # Print table information
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"   • {table}")

if __name__ == "__main__":
    create_database()