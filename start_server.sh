#!/bin/bash

# Startup script for Nudge AI Agent API

echo "🚀 Starting Nudge AI Agent API..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo "   Please edit .env with your configuration"
    echo ""
fi

# Display configuration
echo "📋 Configuration:"
source .env 2>/dev/null || true
echo "   Model Provider: ${MODEL_PROVIDER:-not set}"
echo "   Model Name: ${MODEL_NAME:-not set}"
echo "   Nudge API: ${NUDGE_API_BASE_URL:-http://localhost:8080}"
echo "   Server Port: ${PORT:-8000}"
echo ""

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null; then
    echo "❌ Error: pipenv is not installed"
    echo "   Install with: pip install pipenv"
    exit 1
fi

# Install dependencies if needed
if [ ! -f Pipfile.lock ]; then
    echo "📦 Installing dependencies..."
    pipenv install
    echo ""
fi

# Start the server
echo "✅ Starting server..."
echo "   API: http://localhost:${PORT:-8000}"
echo "   Docs: http://localhost:${PORT:-8000}/docs"
echo ""
echo "Press CTRL+C to stop"
echo ""

pipenv run python api.py
