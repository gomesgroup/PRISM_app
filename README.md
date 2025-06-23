# Interactive Chemical Reaction Rates Heatmap

A Flask web application that displays an interactive heatmap visualization of chemical reaction rates data from `sorted_final_rates.csv`.

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

The application reads data from `data/sorted_final_rates.csv`, which contains:
- Rows: Different chemical compounds
- Columns: Different amines
- Values: Reaction rate measurements

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