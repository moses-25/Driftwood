#!/bin/bash

# Start Backend Server

echo "🔧 Starting Driftwood Café Backend Server..."
echo ""

cd server

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create it first: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Flask not installed!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the server
echo "✅ Starting server at http://localhost:5000"
echo ""
python run.py
