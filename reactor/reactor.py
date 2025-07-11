#!/usr/bin/env python3
"""
Simple STL File Visualizer
A minimalist Flask webapp for visualizing STL files
"""

import os
import json
from flask import Flask, render_template, send_file, jsonify, abort, request
from pathlib import Path

app = Flask(__name__)

# Configuration
STL_DIR = Path(__file__).parent / "STL"
CONFIG_DIR = Path(__file__).parent / "configs"

def get_file_info(filepath):
    """Get file information"""
    stat = filepath.stat()
    return {
        'name': filepath.name,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
    }

def scan_stl_files():
    """Scan for STL files"""
    files = []
    if STL_DIR.exists():
        for file_path in STL_DIR.glob("*.STL"):
            files.append(get_file_info(file_path))
    return files

@app.route('/')
def index():
    """Main page showing STL files"""
    files = scan_stl_files()
    return render_template('index.html', files=files)

@app.route('/assembly')
def assembly():
    """Assembly editor for positioning reactor parts"""
    files = scan_stl_files()
    return render_template('assembly.html', files=files)

@app.route('/view/<filename>')
def view_stl(filename):
    """View STL file in 3D viewer"""
    stl_path = STL_DIR / filename
    if not stl_path.exists() or stl_path.suffix.upper() != '.STL':
        abort(404)
    
    file_info = get_file_info(stl_path)
    return render_template('viewer.html', file_info=file_info)

@app.route('/serve/<filename>')
def serve_stl(filename):
    """Serve STL file for 3D viewer"""
    stl_path = STL_DIR / filename
    if not stl_path.exists() or stl_path.suffix.upper() != '.STL':
        abort(404)
    
    return send_file(stl_path, mimetype='application/octet-stream')

@app.route('/api/assembly/save', methods=['POST'])
def save_assembly():
    """Save assembly configuration"""
    CONFIG_DIR.mkdir(exist_ok=True)
    
    config_data = request.json
    config_name = config_data.get('name', 'default')
    
    config_file = CONFIG_DIR / f"{config_name}.json"
    
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    return jsonify({'success': True, 'message': f'Assembly saved as {config_name}'})

@app.route('/api/assembly/load/<config_name>')
def load_assembly(config_name):
    """Load assembly configuration"""
    config_file = CONFIG_DIR / f"{config_name}.json"
    
    if not config_file.exists():
        abort(404)
    
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    
    return jsonify(config_data)

@app.route('/api/assembly/list')
def list_assemblies():
    """List saved assembly configurations"""
    configs = []
    if CONFIG_DIR.exists():
        for config_file in CONFIG_DIR.glob("*.json"):
            configs.append(config_file.stem)
    return jsonify(configs)

if __name__ == '__main__':
    # Create directories if they don't exist
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    CONFIG_DIR.mkdir(exist_ok=True)
    
    print("🚀 Starting STL Visualizer...")
    print(f"📁 STL files: {len(list(STL_DIR.glob('*.STL'))) if STL_DIR.exists() else 0}")
    print("🌐 Open http://localhost:5003 in your browser")
    print("🔧 Assembly editor: http://localhost:5003/assembly")
    
    app.run(debug=True, host='0.0.0.0', port=5003)
