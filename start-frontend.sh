#!/bin/bash

# Start Frontend Server

echo "⚛️  Starting Driftwood Café Frontend Server..."
echo ""

cd client

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules not found!"
    echo "Installing dependencies..."
    npm install
fi

# Start the development server
echo "✅ Starting server at http://localhost:5173"
echo ""
npm run dev
