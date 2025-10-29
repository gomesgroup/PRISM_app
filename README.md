# PRISM WebApp

A web application for visualizing amide coupling reactions with four integrated modules:
- **Landing** - Animated Game of Life background
- **Menu** - Navigation hub for selecting experiments or data
- **Experiment** - 3D reactor visualization with interactive controls
- **Data** - Interactive heatmap for exploring reaction rates

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
