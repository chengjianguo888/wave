#!/bin/bash

# Start script for Visual Wave Detection System

echo "Starting Visual Wave Detection System..."

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker environment"
else
    echo "Running in local environment"

    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is not installed"
        exit 1
    fi

    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "Error: Node.js is not installed"
        exit 1
    fi
fi

# Start backend
echo "Starting backend server..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

echo "Installing backend dependencies..."
pip install -r requirements.txt -q

echo "Starting Flask server..."
python app.py &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend server..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Starting Vite dev server..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "Visual Wave Detection System is running!"
echo "=========================================="
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
