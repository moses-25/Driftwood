#!/usr/bin/env python3
"""
Script to create and run database migrations
"""
from flask import Flask
from flask_migrate import init, migrate, upgrade
from app import create_app
from extensions import db
import os

def setup_migrations():
    """Initialize and run database migrations"""
    app = create_app()
    
    with app.app_context():
        # Check if migrations folder is initialized
        if not os.path.exists('migrations/versions'):
            print("Initializing migrations...")
            try:
                init()
                print("✅ Migrations initialized successfully!")
            except Exception as e:
                print(f"Migration init error (might already exist): {e}")
        
        # Create migration
        print("Creating migration for all models...")
        try:
            migrate(message="Initial migration with all models")
            print("✅ Migration created successfully!")
        except Exception as e:
            print(f"Migration creation error: {e}")
        
        # Apply migration
        print("Applying migrations to database...")
        try:
            upgrade()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"Migration upgrade error: {e}")
        
        # Verify tables were created
        print("\nVerifying database tables...")
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['users', 'categories', 'products', 'orders', 'order_items', 'payments', 'reviews']
        
        print("Created tables:")
        for table in tables:
            status = "✅" if table in expected_tables else "ℹ️"
            print(f"  {status} {table}")
        
        missing_tables = [t for t in expected_tables if t not in tables]
        if missing_tables:
            print(f"\n❌ Missing tables: {missing_tables}")
        else:
            print("\n🎉 All expected tables created successfully!")

if __name__ == '__main__':
    setup_migrations()