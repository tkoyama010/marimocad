# 3D Viewer Documentation

## Overview

The marimocad 3D viewer provides interactive visualization of CAD geometries in Marimo notebooks using Three.js WebGL rendering.

## Features

### Interactive Controls
- **Orbit**: Left-click and drag to rotate the camera around the model
- **Pan**: Right-click and drag to move the camera
- **Zoom**: Scroll wheel to zoom in/out
- **Selection**: Click on objects to select and highlight them

### Display Options
- **Wireframe Toggle**: Switch between solid and wireframe display
- **Grid Helper**: Reference grid on the ground plane
- **Axes Helper**: RGB axes (X=red, Y=green, Z=blue) for orientation
- **Auto-fit Camera**: Automatically positions camera to view all geometries

### Geometry Support
- Build123d geometries (Part, Shape)
- CadQuery geometries (Workplane, Shape)
- OpenCascade (OCP) TopoDS_Shape objects

### Lighting
- Ambient light for overall illumination
- Two directional lights for depth perception
- Configurable background color

### Multiple Geometries
- Display multiple objects in one view
- Automatic color coding for different geometries
- Support for up to 6 different colors with cycling

## Installation

```bash
pip install marimocad marimo
# For Build123d support (recommended)
pip install build123d
# For CadQuery support
pip install cadquery
```

## Basic Usage

### Simple Box Example

```python
import marimo as mo
import marimocad as mc

app = mo.App()

@app.cell
def __():
    # Create interactive sliders
    length = mo.ui.slider(5, 30, value=10, label="Length")
    width = mo.ui.slider(5, 30, value=10, label="Width")
    height = mo.ui.slider(5, 30, value=10, label="Height")
    return mo.vstack([length, width, height])

@app.cell
def __():
    from build123d import Box, BuildPart
    
    with BuildPart() as box:
        Box(length.value, width.value, height.value)
    
    return mc.viewer(box.part, width=700, height=500)
```

### Multiple Geometries

```python
from build123d import Box, Cylinder, Sphere, BuildPart

# Create multiple shapes
with BuildPart() as part1:
    Box(10, 10, 10)

with BuildPart() as part2:
    Cylinder(5, 15)

with BuildPart() as part3:
    Sphere(7)

# Display all together
mc.viewer([part1.part, part2.part, part3.part])
```

### Geometry Properties Card

```python
# Display geometry information
box = ...  # some geometry
card = mc.GeometryCard(box)
card.render()  # Shows: faces, edges, vertices, volume, surface area, etc.
```

### Parametric Model

```python
def create_bracket(length, width, thickness):
    # ... create parametric bracket
    return bracket

params = {
    "length": mo.ui.slider(20, 100, value=50),
    "width": mo.ui.slider(10, 50, value=25),
    "thickness": mo.ui.slider(2, 10, value=5),
}

mc.parametric_model(create_bracket, params)
```

## API Reference

### `viewer(geom, width, height, background_color, camera_position)`

Create an interactive 3D viewer.

**Parameters:**
- `geom`: Geometry or list of geometries to display
- `width`: Viewer width in pixels (default: 800)
- `height`: Viewer height in pixels (default: 600)
- `background_color`: Background color in hex format (default: "#f0f0f0")
- `camera_position`: Initial camera position as (x, y, z) (default: (50, 50, 50))

**Returns:**
- Marimo HTML component with the 3D viewer

### `GeometryCard(geom)`

Create a card displaying geometry properties.

**Parameters:**
- `geom`: Geometry to display info for

**Methods:**
- `render()`: Returns a Marimo component with the info card

### `parametric_model(func, params, width, height)`

Create a reactive parametric model viewer.

**Parameters:**
- `func`: Function that creates geometry from parameters
- `params`: Dictionary of Marimo UI elements (sliders, inputs, etc.)
- `width`: Viewer width in pixels (default: 800)
- `height`: Viewer height in pixels (default: 600)

**Returns:**
- Interactive parametric model viewer with controls

## Advanced Usage

### Custom Camera Position

```python
# View from top
mc.viewer(geometry, camera_position=(0, 0, 100))

# View from side
mc.viewer(geometry, camera_position=(100, 0, 0))

# Isometric view
mc.viewer(geometry, camera_position=(50, 50, 50))
```

### Custom Background Color

```python
# Dark background
mc.viewer(geometry, background_color="#2c3e50")

# White background
mc.viewer(geometry, background_color="#ffffff")

# Custom color
mc.viewer(geometry, background_color="#1a1a2e")
```

### Larger Viewer

```python
# Full width
mc.viewer(geometry, width=1200, height=800)
```

## Performance Tips

1. **Tessellation Quality**: The default tessellation settings provide a good balance. For very large models, you may want to adjust these settings.

2. **Number of Geometries**: The viewer can handle multiple geometries efficiently, but very complex scenes (100+ objects) may impact performance.

3. **Model Complexity**: Complex boolean operations or highly detailed models may take longer to tessellate. Consider simplifying geometry when possible.

4. **Browser Limits**: WebGL has memory limits. Very large models may require splitting into multiple views.

## Troubleshooting

### Geometry Not Displaying

**Problem**: Viewer shows but geometry is not visible.

**Solutions:**
- Check that geometry is not None or empty
- Verify the geometry is a supported type (Build123d, CadQuery, OCP)
- Try adjusting camera position
- Check browser console for JavaScript errors

### Import Errors

**Problem**: `ImportError: marimo is required`

**Solution**: Install marimo:
```bash
pip install marimo
```

**Problem**: `ImportError: No module named 'build123d'`

**Solution**: Install the CAD library you're using:
```bash
pip install build123d  # or cadquery
```

### Performance Issues

**Problem**: Viewer is slow or unresponsive.

**Solutions:**
- Simplify geometry (reduce number of faces)
- Use fewer geometries in one view
- Close other browser tabs
- Try a different browser (Chrome/Edge recommended)

## Browser Compatibility

The viewer works best in modern browsers with WebGL support:

- ✅ Chrome 90+ (Recommended)
- ✅ Edge 90+ (Recommended)
- ✅ Firefox 88+
- ✅ Safari 14+
- ❌ Internet Explorer (not supported)

## Examples

See `examples/viewer_demo.py` for a complete working example demonstrating all features.

## Technical Details

### Three.js Version

The viewer uses Three.js v0.160.0 loaded from CDN.

### Tessellation

Geometries are tessellated using OpenCascade's BRepMesh_IncrementalMesh with default parameters:
- Linear deflection: 0.1
- Angular deflection: 0.5

### Coordinate System

The viewer uses a right-handed coordinate system:
- X-axis: Red (right)
- Y-axis: Green (up)
- Z-axis: Blue (forward)

## Future Enhancements

Planned features for future releases:
- [ ] Save camera position
- [ ] Export viewer to image (PNG, SVG)
- [ ] Multiple camera views (top, front, side)
- [ ] Section views
- [ ] Measurement tools
- [ ] Annotations and labels
- [ ] Animation support
- [ ] VR/AR support

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## License

MIT License - see LICENSE file for details.
