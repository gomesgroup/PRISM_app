# PRISM WebApp

A web application for visualizing amide coupling reactions with four integrated modules:
- **Landing** - Animated Game of Life background
- **Menu** - Navigation hub for selecting experiments or data
- **Experiment** - 3D reactor visualization with interactive controls
- **Data** - Interactive heatmap of PRISM rate constants (1.5× hydrolysis control); data built by `heatmap/build_data.py` from https://github.com/gomesgroup/PRISM

The repository contains the published dataset of 1,085 amine–acyl chloride pairs, including 363 measured rate constants. The [hosted viewer](https://gomes.andrew.cmu.edu/prism/) preserves an earlier dataset and links to the [publication archive](https://doi.org/10.5281/zenodo.23924416).

## Running the Application

In a Python 3.11 environment, run these commands from the repository root:

```bash
python -m pip install -r requirements.txt
python -m flask --app app run --host 127.0.0.1 --port 8001
```

Open [the local landing page](http://127.0.0.1:8001/prism/) in your browser. The [menu](http://127.0.0.1:8001/prism/menu) links to the [reactor](http://127.0.0.1:8001/prism/experiment) and the [heatmap](http://127.0.0.1:8001/prism/data).

## Citation

Mitchell Baumer, Liliana C. Gallegos, Dylan M. Anstine, Andrew Kubaney, Jose Emilio A. Regio, Olexandr Isayev, Stefan Bernhard, and Gabe Gomes.
[Democratizing reaction kinetics through machine vision and learning](https://doi.org/10.1039/D6DD00225K). *Digital Discovery* (2026). Gabe Gomes is the corresponding author.

Archived web application (v1.0.0): [10.5281/zenodo.23924416](https://doi.org/10.5281/zenodo.23924416).
