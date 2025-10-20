# Amides WebApp - Unified Application

A comprehensive web application for visualizing amide coupling reactions, combining four integrated modules:
1. **Landing** - Initial landing page with animated Game of Life background
2. **Menu** - Navigation page with two-column layout for selecting experiments or data
3. **Experiment** - 3D reactor visualization with interactive controls
4. **Data** - Interactive heatmap for exploring reaction rates

## Running the Application

```bash
cd /home/jose/amides_webapp
python app.py
```

The server will start on `http://0.0.0.0:8000`

## Navigation

- **Landing**: `http://localhost:8000/` - Initial landing page
- **Menu**: `http://localhost:8000/menu` - Navigation page for selecting sections
- **Experiment**: `http://localhost:8000/experiment` - Reactor 3D visualization
- **Data**: `http://localhost:8000/data` - Heatmap analysis

## Structure

```
amides_webapp/
├── app.py                          # Main unified Flask application
├── templates/                      # All HTML templates
│   ├── landing/
│   │   └── index.html             # Landing page
│   ├── menu/
│   │   └── index.html             # Menu navigation page
│   ├── reactor/
│   │   └── index.html             # Reactor visualization page
│   └── heatmap/
│       └── index.html             # Heatmap analysis page
├── reactor/                        # Reactor data and assets
│   ├── assembly/                  # 3D model files
│   │   ├── Assem2.gltf
│   │   └── bin/
│   └── explosion_preset.json     # Preset configurations
├── heatmap/                       # Heatmap data
│   └── data/
│       ├── sorted_final_rates.csv
│       ├── amines_smiles.csv
│       ├── acids_smiles.csv
│       └── complete_rate_plots.pkl
├── landing/                       # Legacy landing folder (deprecated)
└── menu/                          # Legacy menu folder (deprecated)
```

## Features

### Landing Page
- Animated Game of Life cellular automaton background
- Clean, minimal design
- Responsive layout for all screen sizes

### Menu Page
- Animated Game of Life cellular automaton background
- Two-column layout with "Experiment" and "Data" sections
- Interactive hover effects with grey transparent overlays
- Vertical divider line between sections
- Clean, modern design with Avenir typography
- Clickable sections navigate to respective pages
- Responsive layout for all screen sizes

### Experiment Page
- Full 3D visualization of reactor assembly
- Exploded view with animation controls
- Component highlighting and rotation
- Interactive labels with hover effects

### Data Page
- Interactive heatmap of reaction rates
- Hover for detailed reaction information
- SMILES structure visualization
- Rate plot data for individual reactions

## Dependencies

```
Flask
pandas
plotly
numpy
pickle
```

## Notes

- All four pages now run on a single port (8000)
- The old individual app.py files in landing/, menu/, reactor/, and heatmap/ are now deprecated
- All routing is handled through the main /home/jose/amides_webapp/app.py
- Landing page (/) → Menu page (/menu) → Experiment or Data pages
- Back buttons on Experiment and Data pages return to Menu page

