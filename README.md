# marimocad

A reactive CAD library for Marimo notebooks - Design, model, and visualize 3D CAD models with the power of reactive programming.

## Overview

marimocad brings professional CAD modeling capabilities to Marimo's reactive notebook environment. Create parametric 3D models that automatically update as you adjust parameters, leveraging Marimo's reactive programming model for an intuitive and powerful design experience.

## Features

- 🎨 **Intuitive API** - Pythonic interface with primitives, transformations, and boolean operations
- ⚡ **Reactive by Default** - Models automatically update when parameters change
- 🔧 **Parametric Modeling** - Create designs that adapt to changing requirements
- 📐 **Professional CAD Operations** - Filleting, chamfering, shelling, lofting, and more
- 🏗️ **Assembly Management** - Build complex assemblies with multiple components
- 📊 **3D Visualization** - Interactive 3D viewer integrated into Marimo notebooks
- 💾 **Industry Standard Formats** - Import/export STEP, IGES, STL, OBJ, GLTF
- 🧮 **Measurements & Analysis** - Volume, surface area, center of mass, and more

## Quick Example

```python
import marimo as mo
from marimocad import primitives, visualize

# Create reactive parameters
radius = mo.ui.slider(5, 30, value=15, label="Radius")
height = mo.ui.slider(10, 50, value=30, label="Height")

# Create parametric CAD model
cylinder = primitives.cylinder(radius=radius.value, height=height.value)

# Visualize (automatically updates when sliders change)
mo.vstack([
    mo.hstack([radius, height]),
    visualize(cylinder, color="#4ECDC4")
])
```

## Documentation

Comprehensive documentation is available in the [docs](./docs) directory:

- **[API Specification](./docs/API_SPECIFICATION.md)** - Complete API reference with examples
- **[Architecture](./docs/ARCHITECTURE.md)** - System design and architecture details
- **[Design Decisions](./docs/DESIGN_DECISIONS.md)** - Rationale behind key design choices
- **[Examples](./docs/examples.py)** - 15+ comprehensive usage examples

## Installation (Planned)

```bash
pip install marimocad
```

## Current Status

🚧 **In Design Phase** - This project is currently in the design and planning phase. The API specification, architecture, and design documentation have been completed. Implementation is planned for future releases.

## Design Highlights

### Immutable & Reactive
All shapes are immutable, making them perfect for Marimo's reactive programming model. Changes create new objects, enabling automatic dependency tracking.

### Pythonic API
```python
# Method chaining for transformations
result = box.translate(x=10).rotate(axis="Z", angle=45).fillet(radius=2)

# Operator overloading for boolean operations
combined = box1 + box2 - sphere  # union and difference

# Context managers for complex construction
with BuildPart() as bracket:
    with Sketch(plane="XY") as profile:
        profile.add_rectangle(width=30, height=20)
    bracket.extrude(distance=10)
```

### Professional CAD Kernel
Built on OpenCASCADE (via OCP), providing industry-standard BREP modeling, NURBS surfaces, and advanced geometric operations.

## Roadmap

- [x] API specification and design
- [x] Architecture documentation
- [x] Example code and use cases
- [ ] Core geometry engine implementation
- [ ] Marimo integration
- [ ] 3D visualization component
- [ ] File I/O support
- [ ] Testing and validation
- [ ] Initial release (v0.1.0)

## Contributing

Contributions are welcome! This project is in early stages, and we're looking for:
- Feedback on API design
- Use case suggestions
- Implementation contributions
- Documentation improvements

## License

[To be determined]

## Acknowledgments

Inspired by:
- [Marimo](https://github.com/marimo-team/marimo) - Reactive Python notebooks
- [CadQuery](https://github.com/CadQuery/cadquery) - Python CAD scripting
- [build123d](https://github.com/gumyr/build123d) - Pythonic CAD modeling
- [OpenCASCADE](https://www.opencascade.com/) - CAD kernel

## Contact

For questions or discussions, please open an issue on GitHub.