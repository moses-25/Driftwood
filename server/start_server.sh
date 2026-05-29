#!/bin/bash
# Driftwood Cafe Backend Startup Script

echo "🚀 Starting Driftwood Cafe Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Check database connection
echo "🗄️  Checking database connection..."
python3 -c "from app import create_app; app = create_app(); print('✅ Database connection: OK')" 2>&1

# Check if migrations exist
if [ ! -d "migrations" ]; then
    echo "🔨 Initializing database migrations..."
    flask db init
fi

# Run migrations
echo "🔄 Running database migrations..."
flask db upgrade

# Check if database has data
echo "📊 Checking database data..."
python3 -c "
from app import create_app
from extensions import db
from models import User, Product, Category

app = create_app()
with app.app_context():
    user_count = User.query.count()
    product_count = Product.query.count()
    category_count = Category.query.count()
    
    print(f'Users: {user_count}')
    print(f'Products: {product_count}')
    print(f'Categories: {category_count}')
    
    if user_count == 0 or product_count == 0:
        print('')
        print('⚠️  Database is empty. Run seed_data.py to populate it.')
        print('   Command: python3 seed_data.py')
"

echo ""
echo "✅ All checks passed!"
echo ""
echo "🌐 Starting Flask server on http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""

# Start the server
python3 run.py
