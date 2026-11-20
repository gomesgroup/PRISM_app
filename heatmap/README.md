# Interactive Chemical Reaction Rates Heatmap

Interactive heatmap of PRISM rate constants, served at `/prism/data` by the top-level `app.py`. (`heatmap/app.py` is an older standalone version and is not used by the site.)

## Features

- **Interactive Heatmap**: Hover over cells to see detailed information about compounds, amines, and rate values
- **Responsive Design**: Beautiful, modern UI that works on different screen sizes
- **Data Statistics**: Overview panel showing dataset information (min/max/mean values, data points count)
- **Zoom & Pan**: Navigate through the heatmap with mouse controls
- **Professional Styling**: Clean interface with Bootstrap and custom CSS

## Running the integrated heatmap

Follow the [repository's local setup instructions](../README.md#running-the-application) from the repository root. Open the [local heatmap](http://127.0.0.1:8001/prism/data) to explore the publication dataset.

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

## Integrated API endpoints

- `/prism/data` – heatmap page
- `/prism/api/heatmap-data` – heatmap data
- `/prism/api/data-info` – dataset statistics and metadata
