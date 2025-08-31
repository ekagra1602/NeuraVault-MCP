#!/bin/bash

# Script to set up and start the NeuraVault MCP frontend

echo "🚀 Setting up NeuraVault MCP Frontend..."

# Check if we're in the correct directory
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found. Please run this script from the NeuraVault MCP project root."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
else
    echo "✅ Dependencies already installed"
fi

echo "🎨 Starting development server..."
echo "📍 Frontend will be available at: http://localhost:5173"
echo "🔗 Make sure your NeuraVault MCP backend is running at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm run dev
