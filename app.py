from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.graph_objects as go
import plotly.utils
import json
import numpy as np

app = Flask(__name__)

def load_data():
    """Load and prepare the CSV data for the heatmap"""
    df = pd.read_csv('data/sorted_final_rates.csv', index_col=0)
    return df

def load_smiles_data():
    """Load SMILES data for both amines and acids"""
    try:
        amines_df = pd.read_csv('data/amines_smiles.csv')
        acids_df = pd.read_csv('data/acids_smiles.csv')
        
        # Create dictionaries for easy lookup
        amines_smiles = dict(zip(amines_df['index'], amines_df['amine_smiles']))
        acids_smiles = dict(zip(acids_df['index'], acids_df['acid_smiles']))
        
        return amines_smiles, acids_smiles
    except Exception as e:
        print(f"Error loading SMILES data: {e}")
        return {}, {}

@app.route('/')
def index():
    """Main page with the heatmap"""
    return render_template('index.html')

@app.route('/api/heatmap-data')
def get_heatmap_data():
    """API endpoint to get heatmap data as JSON"""
    try:
        df = load_data()
        
        # Apply SymLogNorm transformation to match the notebook exactly
        linthresh = 10
        vmin = df.min().min()
        vmax = df.max().max()
        z_data = df.values
        
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
        
        # Create custom colorbar tick values and labels to show original scale
        # Generate some representative values for the colorbar
        original_ticks = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
        # Filter to values within our data range
        valid_ticks = [t for t in original_ticks if vmin <= t <= vmax]
        
        # Transform these tick values using symlog - these will be the tick positions
        transformed_ticks = [symlog_transform(np.array([t]), linthresh)[0] for t in valid_ticks]
        
        # Create the heatmap
        fig = go.Figure(data=go.Heatmap(
            z=z_normalized,
            x=df.columns.tolist(),
            y=df.index.tolist(),
            colorscale='Cividis',
            hovertemplate='<b>Acid Chloride:</b> %{y}<br>' +
                         '<b>Amine:</b> %{x}<br>' +
                         '<b>Rate:</b> %{customdata:.2f} (M⁻¹ · min⁻¹)<br>' +
                         '<extra></extra>',
            customdata=z_data,  # Use original data for hover
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
                constrain='domain'
            ),
            yaxis=dict(
                tickmode='linear',
                autorange='reversed',
                scaleanchor='x',
                scaleratio=1,
                constrain='domain',
                side='right'
            ),
            # Calculate dimensions for square cells - 125% larger
            # 30 rows (acid chlorides) × 34 columns (amines)
            # Base cell size of 25 pixels (125% of 20px)
            width=34 * 30 + 100 + 30 + 70,  # Larger for better detail
            height=30 * 30 + 35 + 60,  # Larger for better detail
            margin=dict(l=100, r=30, t=8, b=30)
        )
        
        # Convert to JSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data-info')
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
            'mean_value': float(df.mean().mean())
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/smiles-data')
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
