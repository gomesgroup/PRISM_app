# PRISM WebApp

A web application for visualizing amide coupling reactions with four integrated modules:
- **Landing** - Animated Game of Life background
- **Menu** - Navigation hub for selecting experiments or data
- **Experiment** - 3D reactor visualization with interactive controls
- **Data** - Interactive heatmap of PRISM rate constants (1.5× hydrolysis control); data built by `heatmap/build_data.py` from https://github.com/gomesgroup/PRISM

## Running the Application

```bash
python app.py
```

The server starts on `http://0.0.0.0:8000`

## Navigation

- `/` - Landing page
- `/menu` - Navigation menu
- `/experiment` - 3D reactor visualization
- `/data` - Heatmap analysis

## Dependencies

```
Flask
pandas
plotly
numpy
```

## Citation

Mitchell Baumer, Liliana C. Gallegos, Dylan M. Anstine, Andrew Kubaney, Jose Emilio A. Regio, Olexandr Isayev, Stefan Bernhard, and Gabe Gomes.
[Democratizing reaction kinetics through machine vision and learning](https://doi.org/10.1039/D6DD00225K). *Digital Discovery* (2026).

Archived web application (v1.0.0): [10.5281/zenodo.23924416](https://doi.org/10.5281/zenodo.23924416).
