#!/usr/bin/env python3
"""
Create Phase 7 database migration
Adds tables for stock adjustments, order status history, and notification preferences
"""

from app import create_app
from extensions import db
from flask_migrate import migrate as flask_migrate, upgrade
import os

def create_migration():
    """Create migration for Phase 7 models"""
    app = create_app()
    
    with app.app_context():
        print("Creating Phase 7 migration...")
        
        # Create migration
        os.system('flask db migrate -m "Phase 7: Add stock_adjustments, order_status_history, notification_preferences tables"')
        
        print("\nMigration created successfully!")
        print("\nTo apply the migration, run:")
        print("  flask db upgrade")
        print("\nOr use Python:")
        print("  python apply_phase7_migration.py")

if __name__ == '__main__':
    create_migration()
