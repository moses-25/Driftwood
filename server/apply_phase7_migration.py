#!/usr/bin/env python3
"""
Apply Phase 7 database migration
"""

from app import create_app
from flask_migrate import upgrade

def apply_migration():
    """Apply Phase 7 migration"""
    app = create_app()
    
    with app.app_context():
        print("Applying Phase 7 migration...")
        upgrade()
        print("Migration applied successfully!")

if __name__ == '__main__':
    apply_migration()
