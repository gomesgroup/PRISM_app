# Reactor 3D Visualization

A Flask web application for visualizing a reactor assembly exported from SolidWorks as a GLTF file.

## Features

- 3D visualization of the reactor assembly using Three.js
- Interactive controls (zoom, pan, rotate)
- Wireframe toggle
- Auto-rotation mode
- Real-time lighting adjustments
- Model information display
- **Exploded view with manual component positioning**
- **Preset save/load functionality (JSON format)**
- **Real-time animation of explosion sequences**

## Files Structure

```
reactor/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Main visualization page
├── assembly/
│   ├── Assem2.gltf       # Main GLTF file
│   ├── mapping.csv       # STL to binary file mapping
│   ├── bin/              # Binary geometry files
│   └── STL/              # STL source files
└── requirements.txt      # Python dependencies
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Using the startup script (Recommended)
```bash
./start_server.sh
```

### Option 2: Direct Python execution
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5001
```

## Controls

### Basic Navigation
- **Mouse**: 
  - Left click + drag: Rotate view
  - Right click + drag: Pan view
  - Scroll wheel: Zoom in/out

### View Controls
- **Toggle Wireframe**: Switch between solid and wireframe rendering
- **Reset View**: Return camera to default position
- **Auto Rotate**: Enable/disable automatic rotation
- **Light Intensity**: Adjust directional lighting

### Model Orientation
- **Flip X/Y/Z**: Rotate model 180° around respective axis
- **Reset Orientation**: Return to default orientation

### Exploded View
- **Toggle Exploded View**: Show/hide component position controls
- **Animate Explosion**: Smooth animation using current settings
- **Reset All Offsets**: Return components to assembled positions
- **Animation Speed**: Control explosion animation speed (0.5x to 5x)
- **Component Sliders**: Individual Y-offset control for each part (-2 to +2 units)
- **Manual Entry**: Direct numerical input for precise positioning
- **Save Preset**: Export current explosion settings to JSON file
- **Load Preset**: Import explosion settings from JSON file

## Components

The reactor assembly includes the following grouped components:
- **Legs (Both)** - Support structure (both leg assemblies move together)
- **96 Well Plate** - Main reaction vessel (includes mesh_3 and mesh_3_1)
- **Camera Mount Bottom** - Lower camera support
- **Camera Mount Top** - Upper camera support
- **Light Cap** - LED housing cover
- **Light Gradient Filter** - Optical filtering component
- **Reactor Lid** - Top assembly cover
- **Light Filter & Funnel** - Additional optical component

## Technical Details

- **GLTF Version**: 2.0
- **Exported from**: SolidWorks
- **Renderer**: Three.js WebGL
- **File Format**: Binary GLTF with external .bin files
- **Materials**: PBR (Physically Based Rendering)

## Explosion Preset Format

Preset files are saved as JSON with the following structure:
```json
{
  "version": "1.1",
  "timestamp": "2025-08-02T14:30:00.000Z",
  "modelName": "Reactor Assembly",
  "componentOffsets": {
    "Legs (Both)": -0.75,
    "96 Well Plate": 0.00,
    "CameraMountBottom-1": 0.25,
    "CameraMountTop-1": 0.50,
    "LightCap-1": 1.00,
    "v2-96wellLightGradient-6": 1.25,
    "ReactorLid-2": 1.50,
    "LightFilter & Funnel-1": 1.75
  },
  "cameraSettings": {
    "position": {
      "x": 1.2345,
      "y": 0.8765,
      "z": 2.1098
    },
    "target": {
      "x": 0.0,
      "y": 0.0,
      "z": 0.0
    }
  },
  "animationSpeed": 2.5
}
```

### Format Details:
- **componentOffsets**: Y-axis offset values (-2.0 to +2.0) for each component
- **cameraSettings**: Camera position and target for consistent viewpoint
  - **position**: Camera location in 3D space (x, y, z)
  - **target**: Point the camera is looking at (x, y, z)
- **animationSpeed**: Animation playback speed (0.5x to 5.0x)
- **timestamp**: ISO format creation time
- **version**: Preset format version (1.1 includes camera + speed)

### Compatibility:
- **Version 1.1**: Full preset with camera and animation settings *(recommended)*
- **Version 1.0**: Component offsets only (legacy format, still supported)

When you load a preset, the system will:
1. ✅ Apply all component positions
2. ✅ Restore camera viewpoint (if available)
3. ✅ Set animation speed (if available)
4. ✅ Enable exploded view mode automatically

## API Endpoints

- `GET /`: Main visualization page
- `GET /assembly/<filename>`: Serve GLTF and binary files
- `GET /api/model-info`: Get model metadata and component information

## Troubleshooting

1. **Model not loading**: Check that all .bin files are present in the `assembly/bin/` directory
2. **Missing components**: Verify the mapping.csv file has correct paths
3. **Performance issues**: Try reducing the model scale or disabling shadows in the browser console