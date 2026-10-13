# Interactive Chemical Reaction Rates Heatmap

Interactive heatmap of PRISM rate constants, served at `/prism/data` by the top-level `app.py`. (`heatmap/app.py` is an older standalone version and is not used by the site.)

## Features

- **Interactive Heatmap**: Hover over cells to see detailed information about compounds, amines, and rate values
- **Responsive Design**: Beautiful, modern UI that works on different screen sizes
- **Data Statistics**: Overview panel showing dataset information (min/max/mean values, data points count)
- **Zoom & Pan**: Navigate through the heatmap with mouse controls
- **Professional Styling**: Clean interface with Bootstrap and custom CSS

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask development server**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and go to:
   ```
   http://localhost:5000
   ```

## Usage

- **Hover**: Move your mouse over any cell in the heatmap to see detailed information
- **Zoom**: Use your mouse wheel or trackpad to zoom in/out
- **Pan**: Click and drag to move around when zoomed in
- **Color Scale**: Color intensity represents rate values (darker = higher rates)

## Data

The page reads four files in `data/`, built from the PRISM repository
(https://github.com/gomesgroup/PRISM) by `build_data.py`:

| file | contents |
|---|---|
| `rate_constants.csv` | rate constant *k* (M⁻¹ min⁻¹) for each acyl chloride × amine pair; blank if not measurable |
| `reaction_classes.csv` | class of each pair: measurable, instant, un-reactive or undetermined |
| `rate_plots.json` | for each pair: 1/[A]₀ against t₁/₂ for every well, whether the well was used in the fit, the no-amine control, the fitted line, the class and its note |
| `acids_smiles.csv`, `amines_smiles.csv` | SMILES for the structure pop-ups |

Rate constants come from the per-well hydrolysis control (1.5×): a well is used only if the
no-amine control is at least 1.5× slower than the reaction at the same concentration, and *k*
is the slope of 1/[A]₀ against t₁/₂ over those wells. Pairs without a measured *k* are grey.

To rebuild after the PRISM data change:

```bash
python heatmap/build_data.py --prism <path to a clone of gomesgroup/PRISM>
```

## Technical Details

- **Backend**: Flask (Python)
- **Visualization**: Plotly.js
- **Styling**: Bootstrap 5
- **Data Processing**: Pandas
- **Interactive Features**: Plotly hover templates and zoom/pan controls

## API Endpoints

- `/` - Main application page
- `/api/heatmap-data` - Returns heatmap data as JSON
- `/api/data-info` - Returns dataset statistics and metadata

## Dependencies

- Flask 2.3.3
- pandas 2.0.3
- plotly 5.17.0
- numpy 1.24.3 