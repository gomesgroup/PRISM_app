from flask import Flask, render_template, send_from_directory, jsonify, request
import os
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.utils
import numpy as np

app = Flask(__name__)

# ============================================================================
# LANDING PAGE ROUTE
# ============================================================================

@app.route('/prism/')
def landing():
    """Landing page with Game of Life background"""
    return render_template('landing/index.html')

@app.route('/prism/paper.json')
def serve_paper_json():
    """Serve the paper metadata JSON file"""
    return send_from_directory('.', 'paper.json')

# ============================================================================
# MENU ROUTES
# ============================================================================

@app.route('/prism/menu')
def menu():
    """Main menu page with Game of Life background"""
    return render_template('menu/index.html')

# ============================================================================
# REACTOR/EXPERIMENT ROUTES
# ============================================================================

@app.route('/prism/experiment')
def experiment():
    """Reactor visualization page"""
    return render_template('reactor/index.html')

@app.route('/prism/assembly/<path:filename>')
def serve_assembly_files(filename):
    """Serve GLTF and binary files from the reactor assembly directory"""
    from flask import abort
    
    # First try the main assembly directory
    main_path = os.path.join('reactor', 'assembly', filename)
    if os.path.exists(main_path):
        return send_from_directory(os.path.join('reactor', 'assembly'), filename)
    
    # If not found, try the bin subdirectory for .bin files
    if filename.endswith('.bin'):
        bin_path = os.path.join('reactor', 'assembly', 'bin', filename)
        if os.path.exists(bin_path):
            return send_from_directory(os.path.join('reactor', 'assembly', 'bin'), filename)
    
    # If still not found, return 404
    abort(404)

@app.route('/prism/api/explosion-preset')
def get_explosion_preset():
    """Serve the explosion preset for reactor visualization"""
    try:
        preset_file = os.path.join('reactor', 'explosion_preset.json')
        if os.path.exists(preset_file):
            return send_from_directory('reactor', 'explosion_preset.json')
        else:
            return {'error': 'Preset file not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/prism/api/model-info')
def model_info():
    """Provide information about the reactor model components"""
    try:
        # Read the mapping CSV
        mapping_data = []
        mapping_file = os.path.join('reactor', 'assembly', 'mapping.csv')
        
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
        gltf_file = os.path.join('reactor', 'assembly', 'Assem2.gltf')
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

# ============================================================================
# HEATMAP/DATA ROUTES
# ============================================================================

def load_data():
    """Rate constants (M^-1 min^-1); blank where the pair has no measured k.
    Built by heatmap/build_data.py from the PRISM repository (1.5x hydrolysis control)."""
    return pd.read_csv('heatmap/data/rate_constants.csv', index_col=0)

def load_classes():
    """Class of every pair: measurable, instant, un-reactive or undetermined."""
    return pd.read_csv('heatmap/data/reaction_classes.csv', index_col=0).fillna('')

def load_smiles_data():
    """Load SMILES data for both amines and acids"""
    try:
        amines_df = pd.read_csv('heatmap/data/amines_smiles.csv')
        acids_df = pd.read_csv('heatmap/data/acids_smiles.csv')
        
        # Create dictionaries for easy lookup
        amines_smiles = dict(zip(amines_df['index'], amines_df['amine_smiles']))
        acids_smiles = dict(zip(acids_df['index'], acids_df['acid_smiles']))
        
        return amines_smiles, acids_smiles
    except Exception as e:
        print(f"Error loading SMILES data: {e}")
        return {}, {}

def load_rate_plots_data():
    """Per-pair well data for the rate plots (heatmap/build_data.py)."""
    try:
        with open('heatmap/data/rate_plots.json') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading rate plots data: {e}")
        return {}

@app.route('/prism/data')
def data():
    """Heatmap analysis page"""
    return render_template('heatmap/index.html')

@app.route('/prism/api/heatmap-data')
def get_heatmap_data():
    """API endpoint to get heatmap data as JSON"""
    try:
        df = load_data()
        classes = load_classes().reindex(index=df.index, columns=df.columns).fillna('')
        
        # Apply SymLogNorm transformation to match the notebook exactly
        linthresh = 10
        vmin = np.nanmin(df.values)
        vmax = np.nanmax(df.values)
        z_data = df.values.astype(float)
        
        # Implement matplotlib's SymLogNorm transformation
        def symlog_transform(x, linthresh):
            """Apply symmetric log transformation matching matplotlib's SymLogNorm"""
            with np.errstate(divide='ignore', invalid='ignore'):
                abs_x = np.abs(x)
                sign_x = np.sign(x)
                
                # Linear region: |x| <= linthresh
                linear_region = abs_x <= linthresh
                
                # Log region: |x| > linthresh  
                log_region = abs_x > linthresh
                
                result = np.zeros_like(x)
                
                # Linear part
                result[linear_region] = x[linear_region]
                
                # Log part - this matches matplotlib's SymLogNorm
                result[log_region] = sign_x[log_region] * linthresh * (
                    1 + np.log(abs_x[log_region] / linthresh)
                )
                
                return result
        
        z_normalized = symlog_transform(z_data, linthresh)
        z_normalized = np.where(np.isnan(z_data), np.nan, z_normalized)  # no k: transparent
        
        # Create custom colorbar tick values and labels to show original scale
        # Generate some representative values for the colorbar
        original_ticks = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
        # Filter to values within our data range
        valid_ticks = [t for t in original_ticks if vmin <= t <= vmax]
        
        # Transform these tick values using symlog - these will be the tick positions
        transformed_ticks = [symlog_transform(np.array([t]), linthresh)[0] for t in valid_ticks]
        
        # Create the heatmap (original colouring: Plotly's Cividis on the symlog scale).
        # Pairs without a measured k have no value and are left blank; their customdata
        # is the class name, so a click shows the class.
        not_measured = (classes.values != 'measurable') & (classes.values != '')
        custom = [[c if nm else (None if np.isnan(v) else float(v))
                   for v, c, nm in zip(zr, cr, nr)]
                  for zr, cr, nr in zip(z_data, classes.values, not_measured)]
        fig = go.Figure(data=go.Heatmap(
            # plain list: newer Plotly (6.x) would otherwise send a binary array that
            # the page's Plotly.js 2.26 cannot read
            z=[[None if np.isnan(v) else float(v) for v in row] for row in z_normalized],
            x=df.columns.tolist(),
            y=df.index.tolist(),
            colorscale='Cividis',
            hovertemplate='<b>Acid Chloride:</b> %{y}<br>' +
                         '<b>Amine:</b> %{x}<br>' +
                         '<b>Rate:</b> %{customdata:.2f} (M⁻¹ · min⁻¹)<br>' +
                         '<extra></extra>',
            customdata=custom,
            showscale=False,  # Hide the colorbar/scale
            # Add grid lines like in the notebook
            xgap=1,
            ygap=1
        ))
        
        # Update layout for square heatmap
        fig.update_layout(
            xaxis=dict(
                tickangle=45,
                side='bottom',
                constrain='domain',
                tickfont=dict(family='Avenir, Avenir Next, -apple-system, BlinkMacSystemFont, Helvetica Neue, sans-serif'),
                title=dict(font=dict(family='Avenir, Avenir Next, -apple-system, BlinkMacSystemFont, Helvetica Neue, sans-serif'))
            ),
            yaxis=dict(
                tickmode='linear',
                autorange='reversed',
                scaleanchor='x',
                scaleratio=1,
                constrain='domain',
                side='right',
                tickfont=dict(family='Avenir, Avenir Next, -apple-system, BlinkMacSystemFont, Helvetica Neue, sans-serif'),
                title=dict(font=dict(family='Avenir, Avenir Next, -apple-system, BlinkMacSystemFont, Helvetica Neue, sans-serif'))
            ),
            # Square cells, 30 px each
            width=df.shape[1] * 30 + 100 + 30 + 70,
            height=df.shape[0] * 30 + 35 + 60,
            margin=dict(l=100, r=30, t=8, b=30),
            font=dict(family='Avenir, Avenir Next, -apple-system, BlinkMacSystemFont, Helvetica Neue, sans-serif')
        )
        
        # Convert to JSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/prism/api/data-info')
def get_data_info():
    """API endpoint to get basic information about the dataset"""
    try:
        df = load_data()
        info = {
            'shape': df.shape,
            'compounds': df.index.tolist(),
            'amines': df.columns.tolist(),
            'min_value': float(df.min().min()),
            'max_value': float(df.max().max()),
            'measured_pairs': int(df.notna().sum().sum()),
            'classes': load_classes().stack().value_counts().to_dict()
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/prism/api/smiles-data')
def get_smiles_data():
    """API endpoint to get SMILES data for both amines and acids"""
    try:
        amines_smiles, acids_smiles = load_smiles_data()
        return jsonify({
            'amines': amines_smiles,
            'acids': acids_smiles
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/prism/api/rate-plot-data')
def get_rate_plot_data():
    """API endpoint to get rate plot data for a specific reaction"""
    try:
        acid_chloride = request.args.get('acid_chloride')
        amine = request.args.get('amine')
        
        if not acid_chloride or not amine:
            return jsonify({'error': 'Both acid_chloride and amine parameters are required'}), 400
        
        plots = load_rate_plots_data()
        row = plots.get(f"{acid_chloride}||{amine}")
        if row is None:
            return jsonify({'error': 'No data found for this reaction'}), 404
        return jsonify(row)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return f"File not found: {error}", 404

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Print some debug info
    print("=" * 60)
    print("=== Amides WebApp Unified Server ===")
    print("=" * 60)
    print(f"Landing page: http://0.0.0.0:8001/prism/")
    print(f"Menu page: http://0.0.0.0:8001/prism/menu")
    print(f"Experiment (Reactor): http://0.0.0.0:8001/prism/experiment")
    print(f"Data (Heatmap): http://0.0.0.0:8001/prism/data")
    print("=" * 60)
    print(f"Deployment URL: https://gomes.andrew.cmu.edu/prism/")
    print("=" * 60)
    print(f"Reactor assembly: {os.path.exists('reactor/assembly/Assem2.gltf')}")
    print(f"Heatmap data: {os.path.exists('heatmap/data/rate_constants.csv')}")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=8001)

