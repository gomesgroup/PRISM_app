from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Configure template folder for user-facing templates
app.template_folder = 'user_templates'

@app.route('/')
def index():
    """User-facing page with animated Game of Life background"""
    return render_template('index.html')

@app.route('/assembly/<path:filename>')
def serve_assembly_files(filename):
    """Serve GLTF and binary files from the assembly directory (for future 3D visualization)"""
    import os
    from flask import abort
    
    # First try the main assembly directory
    main_path = os.path.join('assembly', filename)
    if os.path.exists(main_path):
        return send_from_directory('assembly', filename)
    
    # If not found, try the bin subdirectory for .bin files
    if filename.endswith('.bin'):
        bin_path = os.path.join('assembly', 'bin', filename)
        if os.path.exists(bin_path):
            return send_from_directory(os.path.join('assembly', 'bin'), filename)
    
    # If still not found, return 404
    abort(404)

@app.route('/api/explosion-preset')
def get_explosion_preset():
    """Serve the explosion preset for future 3D visualization"""
    try:
        preset_file = 'explosion_preset.json'
        if os.path.exists(preset_file):
            return send_from_directory('.', preset_file)
        else:
            return {'error': 'Preset file not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    # Create user templates directory if it doesn't exist
    os.makedirs('user_templates', exist_ok=True)
    
    # Print some debug info
    print("=== Reactor Presentation Server ===")
    print(f"Assembly directory: {os.path.abspath('assembly')}")
    print(f"GLTF file exists: {os.path.exists('assembly/Assem2.gltf')}")
    print(f"Explosion preset exists: {os.path.exists('explosion_preset.json')}")
    print("===================================")
    
    app.run(debug=True, host='0.0.0.0', port=5002)