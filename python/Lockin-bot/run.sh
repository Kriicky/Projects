#!/bin/bash
# Run the focus detector with its alert server

cd "$(dirname "$0")"

# Use virtual environment if it exists
if [ -d "venv" ]; then
    PYTHON="./venv/bin/python"
else
    PYTHON="python"
fi

echo "Starting Python Vision Focus Detector..."
echo "Press Ctrl+C to stop"

# Start the Flask server in background
$PYTHON server.py &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Start the main detector
$PYTHON main.py

# Clean up server when done
kill $SERVER_PID 2>/dev/null

echo "Stopped focus detector and server"