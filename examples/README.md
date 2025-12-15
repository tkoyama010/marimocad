# marimocad Examples

This directory contains example marimo notebooks demonstrating various features of marimocad.

## Running the Examples

To run these examples, you need to have marimo and marimocad installed:

```bash
pip install marimocad marimo
```

Then run any example using marimo:

```bash
marimo edit examples/01_basic_shapes.py
```

## Examples Overview

### 1. Basic Shapes (`01_basic_shapes.py`)
**Difficulty:** Beginner  
**Topics:** Shape creation, properties, error handling

Learn how to create and work with the three fundamental 3D shapes:
- Creating boxes, cylinders, and spheres
- Accessing shape properties (volume, surface area, bounds)
- Naming shapes for better organization
- Understanding error handling for invalid parameters

**Key Concepts:**
- `Box(width, height, depth)`
- `Cylinder(radius, height)`
- `Sphere(radius)`
- Shape properties and validation

---

### 2. Boolean Operations (`02_boolean_operations.py`)
**Difficulty:** Beginner to Intermediate  
**Topics:** CSG operations, shape combinations

Master constructive solid geometry (CSG) operations:
- Union: Combining shapes together
- Intersection: Finding common volume
- Difference: Subtracting shapes
- Nesting operations for complex results

**Key Concepts:**
- `union(shape1, shape2, ...)`
- `intersection(shape1, shape2, ...)`
- `difference(base, to_subtract1, ...)`
- Creating hollow shapes and cutouts

---

### 3. Transformations (`03_transformations.py`)
**Difficulty:** Intermediate  
**Topics:** Geometric transformations, positioning

Learn to manipulate shapes in 3D space:
- Translation: Moving shapes
- Rotation: Rotating around axes
- Scaling: Uniform and non-uniform resizing
- Mirroring: Reflecting across planes
- Creating geometric patterns

**Key Concepts:**
- `translate(shape, x, y, z)`
- `rotate(shape, angle, axis)`
- `scale(shape, factor)` or `scale(shape, x, y, z)`
- `mirror(shape, plane)`
- Transformation chaining

---

### 4. Complex Models (`04_complex_model.py`)
**Difficulty:** Intermediate to Advanced  
**Topics:** Complete CAD models, practical applications

Build real-world mechanical components:
- **Mechanical Bracket**: Base plate, mounting holes, support wall, cable slots
- **Parametric Gear**: Circular body, teeth generation, shaft hole

This example demonstrates:
- Multi-step modeling workflow
- Combining shapes, operations, and transformations
- Practical engineering designs
- Parameter-driven design

**Key Concepts:**
- Modeling workflow
- Component assembly
- Hole patterns
- Parametric teeth generation

---

### 5. Parametric Design (`05_parametric_design.py`)
**Difficulty:** Intermediate  
**Topics:** Interactive design, marimo integration

Create interactive parametric models:
- **Parametric Box**: Interactive dimension sliders
- **Hollow Cylinder**: Wall thickness control
- **Parametric Bolt**: Complete bolt specification
- **Gear Generator**: Configurable gear parameters

This example shows the power of marimo's reactive execution:
- Real-time parameter updates
- Calculated properties
- Design validation
- Interactive exploration

**Key Concepts:**
- `marimo.ui.slider()` for parameters
- Reactive model updates
- Design calculations
- Parameter validation

---

## Learning Path

**For Complete Beginners:**
1. Start with `01_basic_shapes.py`
2. Move to `02_boolean_operations.py`
3. Try `03_transformations.py`

**For Intermediate Users:**
1. Review `04_complex_model.py` for practical patterns
2. Explore `05_parametric_design.py` for interactive features

**For Advanced Users:**
- Combine techniques from multiple examples
- Create your own complex models
- Experiment with nested operations and transformations

## Tips for Learning

1. **Run interactively**: Use `marimo edit` to run examples and modify them in real-time
2. **Experiment**: Change parameters to see how models respond
3. **Read the code**: Examples include detailed comments and explanations
4. **Check the docs**: Refer to the [API documentation](../docs/source/api/index.rst) for detailed function descriptions
5. **Start simple**: Begin with basic shapes before attempting complex models

## Common Patterns

### Creating a Simple Model
```python
import marimocad as mc

# Create base shape
base = mc.Box(width=10, height=10, depth=5)

# Add a feature
hole = mc.Cylinder(radius=2, height=10)

# Combine
result = mc.difference(base, hole)
```

### Positioning Shapes
```python
import marimocad as mc

# Create and position
box = mc.Box(width=5, height=5, depth=5)
mc.translate(box, x=10, y=0, z=5)
mc.rotate(box, angle=45, axis='z')
```

### Parametric Design with marimo
```python
import marimo as mo
import marimocad as mc

# Create controls
size = mo.ui.slider(1, 20, value=10, label="Size")

# Create reactive model
box = mc.Box(width=size.value, height=size.value, depth=size.value)
mo.md(f"Volume: {box.volume()}")
```

## Getting Help

- **Documentation**: See [README.md](../README.md) for installation and basics
- **API Reference**: Check [docs/source/api/](../docs/source/api/) for detailed API docs
- **Contributing**: See [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute examples
- **Issues**: Report problems at [GitHub Issues](https://github.com/tkoyama010/marimocad/issues)

## Contributing Examples

Have a great example? We'd love to include it! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

Example contributions should:
- Be well-documented with comments
- Include a clear learning objective
- Demonstrate best practices
- Work with the current version of marimocad

---

**Happy modeling! 🚀**
