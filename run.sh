#!/bin/bash

set -e

echo "Starting Smart Group Trip Planner API..."

# Create virtual environment if it does not exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env from .env.example if .env does not exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Start application in background for testing
echo "Starting application for testing..."
python run.py &

SERVER_PID=$!

# Give the server some time to start
sleep 2

# Run API tests
echo "Running tests..."
python test.py

# Stop background server
echo "Stopping test server..."
kill $SERVER_PID

# Start application in foreground
echo "Starting application..."
echo "Server is running at http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server."

python run.py