#!/bin/bash

# Reactor 3D Visualization Server Startup Script

echo "=== Starting Reactor 3D Visualization Server ==="
echo "Server will be available at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo "================================================"

# Change to the reactor directory
cd "$(dirname "$0")"

# Check if required files exist
if [ ! -f "assembly/Assem2.gltf" ]; then
    echo "Error: GLTF file not found at assembly/Assem2.gltf"
    exit 1
fi

if [ ! -d "assembly/bin" ]; then
    echo "Error: Binary files directory not found at assembly/bin"
    exit 1
fi

# Start the Flask application
python app.py