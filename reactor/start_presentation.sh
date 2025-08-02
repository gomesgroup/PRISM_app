#!/bin/bash

# Reactor User-Facing Presentation Server Startup Script

echo "=== Starting Reactor Presentation Server ==="
echo "User-facing server will be available at: http://localhost:5002"
echo "Developer server should be running at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo "================================================"

# Change to the reactor directory
cd "$(dirname "$0")"

# Check if required files exist
if [ ! -d "user_templates" ]; then
    echo "Error: User templates directory not found"
    exit 1
fi

if [ ! -f "user_templates/index.html" ]; then
    echo "Error: User HTML template not found"
    exit 1
fi

# Activate conda environment if available
if command -v conda &> /dev/null; then
    echo "Activating conda environment 'amides'..."
    source activate amides 2>/dev/null || echo "Note: Could not activate conda environment"
fi

# Start the Flask application
python user_app.py