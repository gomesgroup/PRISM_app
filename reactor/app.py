from flask import Flask, render_template, send_from_directory, jsonify
import os
import json

app = Flask(__name__)

# Configure static folders
app.static_folder = 'static'

@app.route('/')
def index():
    """Main page with 3D reactor visualization"""
    return render_template('index.html')

@app.route('/assembly/<path:filename>')
def serve_assembly_files(filename):
    """Serve GLTF and binary files from the assembly directory"""
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

@app.route('/api/model-info')
def model_info():
    """Provide information about the model components"""
    try:
        # Read the mapping CSV
        mapping_data = []
        mapping_file = os.path.join('assembly', 'mapping.csv')
        
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r') as f:
                lines = f.readlines()[1:]  # Skip header
                for line in lines:
                    parts = line.strip().split(', ')
                    if len(parts) >= 2 and parts[1]:  # Only include rows with bin mapping
                        mapping_data.append({
                            'stl': parts[0],
                            'bin': parts[1]
                        })
        
        # Read GLTF file info
        gltf_file = os.path.join('assembly', 'Assem2.gltf')
        gltf_info = {}
        
        if os.path.exists(gltf_file):
            with open(gltf_file, 'r') as f:
                gltf_data = json.load(f)
                
            # Extract node information
            nodes = []
            if 'nodes' in gltf_data:
                for i, node in enumerate(gltf_data['nodes']):
                    if 'name' in node and node['name'] != 'current camera':
                        nodes.append({
                            'id': i,
                            'name': node['name'],
                            'has_mesh': 'mesh' in node,
                            'has_children': 'children' in node
                        })
            
            gltf_info = {
                'nodes': nodes,
                'total_meshes': len(gltf_data.get('meshes', [])),
                'total_materials': len(gltf_data.get('materials', [])),
                'total_buffers': len(gltf_data.get('buffers', []))
            }
        
        return jsonify({
            'mapping': mapping_data,
            'gltf_info': gltf_info,
            'model_file': 'assembly/Assem2.gltf'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return f"File not found: {error}", 404

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Print some debug info
    print("=== Reactor 3D Visualization Server ===")
    print(f"Assembly directory: {os.path.abspath('assembly')}")
    print(f"GLTF file exists: {os.path.exists('assembly/Assem2.gltf')}")
    print(f"Binary files count: {len(os.listdir('assembly/bin')) if os.path.exists('assembly/bin') else 0}")
    print(f"STL files count: {len(os.listdir('assembly/STL')) if os.path.exists('assembly/STL') else 0}")
    print("=====================================")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
