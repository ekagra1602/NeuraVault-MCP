#!/bin/bash

# Script to start the NeuraVault MCP backend server

echo "🚀 Starting NeuraVault MCP Backend Server..."

# Check if we're in the correct directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Backend files not found. Please run this script from the NeuraVault MCP project root."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run './setup.sh' first."
    exit 1
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source .venv/bin/activate

# Check if FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI not installed. Please run './setup.sh' first."
    exit 1
fi

echo "🎯 Starting FastAPI server..."
echo "📍 Backend will be available at: http://localhost:8000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔍 Interactive API: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
