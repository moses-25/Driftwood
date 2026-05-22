#!/usr/bin/env python3
"""
Script to reset and recreate database migrations
"""
from flask import Flask
from app import create_app
from extensions import db
import os
import shutil

# Import all models so SQLAlchemy knows about them
from models import User, Category, Product, Order, OrderItem, Payment, Review

def reset_and_create_migrations():
    """Reset migrations and recreate database"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Resetting database and migrations...")
        
        # Remove existing database
        db_path = 'instance/driftwood_cafe.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"✅ Removed existing database: {db_path}")
        
        # Remove migrations versions
        versions_path = 'migrations/versions'
        if os.path.exists(versions_path):
            for file in os.listdir(versions_path):
                if file.endswith('.py'):
                    os.remove(os.path.join(versions_path, file))
            print("✅ Cleared migration versions")
        
        # Create all tables directly
        print("📊 Creating database tables...")
        db.create_all()
        print("✅ All tables created successfully!")
        
        # Verify tables were created
        print("\n🔍 Verifying database tables...")
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['users', 'categories', 'products', 'orders', 'order_items', 'payments', 'reviews']
        
        print("Created tables:")
        for table in sorted(tables):
            status = "✅" if table in expected_tables else "ℹ️"
            print(f"  {status} {table}")
        
        missing_tables = [t for t in expected_tables if t not in tables]
        if missing_tables:
            print(f"\n❌ Missing tables: {missing_tables}")
            return False
        else:
            print(f"\n🎉 All {len(expected_tables)} expected tables created successfully!")
            
        # Show table details
        print("\n📋 Table Details:")
        for table_name in expected_tables:
            columns = inspector.get_columns(table_name)
            print(f"  📄 {table_name}: {len(columns)} columns")
            
        return True

if __name__ == '__main__':
    success = reset_and_create_migrations()
    if success:
        print("\n✨ Database setup complete! Ready for Phase 2 testing.")
    else:
        print("\n❌ Database setup failed. Please check the errors above.")