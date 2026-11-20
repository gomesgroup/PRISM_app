# Historical deployment notes for the earlier hosted viewer

These notes record the original integration of the `/prism/` routes.

## Changes Made

### 1. Flask Application (`app.py`)

**Routes Updated:**
- All routes now prefixed with `/prism/`:
  - `/prism/` (landing page)
  - `/prism/menu`
  - `/prism/experiment`
  - `/prism/data`
  - `/prism/assembly/<filename>`
  - `/prism/api/explosion-preset`
  - `/prism/api/model-info`
  - `/prism/api/heatmap-data`
  - `/prism/api/data-info`
  - `/prism/api/smiles-data`
  - `/prism/api/rate-plot-data`
  - `/prism/paper.json`

**Port Configuration:**
- Changed from port 8000 to port 8001 (line 361)

**Debug Output:**
- Updated debug messages to show `/prism/` prefixed URLs
- Added deployment URL: `https://gomes.andrew.cmu.edu/prism/`

### 2. Templates Updated

**Landing Page (`templates/landing/index.html`):**
- Updated "Check the webapp" button: `/menu` → `/prism/menu`
- Updated fetch call: `/paper.json` → `/prism/paper.json`

**Menu Page (`templates/menu/index.html`):**
- Updated back button: `/` → `/prism/`
- Updated "Experiment" link: `/experiment` → `/prism/experiment`
- Updated "Data" link: `/data` → `/prism/data`

**Reactor Page (`templates/reactor/index.html`):**
- Updated back button: `/menu` → `/prism/menu`
- Updated API call: `/api/explosion-preset` → `/prism/api/explosion-preset`
- Updated 3D model path: `/assembly/Assem2.gltf` → `/prism/assembly/Assem2.gltf`

**Heatmap Page (`templates/heatmap/index.html`):**
- Updated back button: `/menu` → `/prism/menu`
- Updated SMILES API: `/api/smiles-data` → `/prism/api/smiles-data`
- Updated heatmap API: `/api/heatmap-data` → `/prism/api/heatmap-data`
- Updated rate plot API: `/api/rate-plot-data` → `/prism/api/rate-plot-data`

## Running this repository locally

Use the [local setup instructions](README.md#running-the-application) from the repository root. The [local heatmap](http://127.0.0.1:8001/prism/data) uses the dataset in this repository. The [hosted viewer](https://gomes.andrew.cmu.edu/prism/) serves an earlier data release.
