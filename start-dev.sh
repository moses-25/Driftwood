#!/bin/bash

# Driftwood Café Development Startup Script
# This script starts both frontend and backend servers

echo "🚀 Starting Driftwood Café Development Servers..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if tmux is available
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}❌ tmux is not installed. Please install it first:${NC}"
    echo "   Ubuntu/Debian: sudo apt-get install tmux"
    echo "   macOS: brew install tmux"
    exit 1
fi

# Kill existing tmux session if it exists
tmux kill-session -t driftwood 2>/dev/null

# Create new tmux session
tmux new-session -d -s driftwood

# Split window horizontally
tmux split-window -h -t driftwood

# Start backend in left pane
tmux send-keys -t driftwood:0.0 'cd server && source .venv/bin/activate && echo "🔧 Starting Backend Server..." && python run.py' C-m

# Start frontend in right pane
tmux send-keys -t driftwood:0.1 'cd client && echo "⚛️  Starting Frontend Server..." && npm run dev' C-m

# Attach to the session
echo -e "${GREEN}✅ Servers starting in tmux session 'driftwood'${NC}"
echo ""
echo -e "${BLUE}📝 Useful commands:${NC}"
echo "   - Ctrl+B then D: Detach from tmux (servers keep running)"
echo "   - Ctrl+B then Arrow Keys: Switch between panes"
echo "   - tmux attach -t driftwood: Reattach to session"
echo "   - tmux kill-session -t driftwood: Stop all servers"
echo ""
echo -e "${GREEN}🌐 URLs:${NC}"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:5000"
echo ""
echo "Attaching to tmux session in 3 seconds..."
sleep 3

tmux attach -t driftwood
