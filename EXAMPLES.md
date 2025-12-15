# marimocad Example Usage

This document provides comprehensive examples of using the marimocad API for parametric 3D modeling in Marimo notebooks.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Primitives](#basic-primitives)
3. [Transformations](#transformations)
4. [Boolean Operations](#boolean-operations)
5. [Modifications](#modifications)
6. [2D to 3D Operations](#2d-to-3d-operations)
7. [Assemblies](#assemblies)
8. [Component Library](#component-library)
9. [Reactive Modeling](#reactive-modeling)
10. [Import/Export](#importexport)
11. [Advanced Examples](#advanced-examples)

## Getting Started

```python
import marimo as mo
import marimocad as mc

# Check version
print(mc.__version__)
```

## Basic Primitives

### Creating Simple Shapes

```python
# Box
box = mc.box(length=20, width=15, height=10)

# Centered box
centered_box = mc.box(10, 10, 10, center=True)

# Sphere
sphere = mc.sphere(radius=5)

# Cylinder
cylinder = mc.cylinder(radius=3, height=15)

# Cone
cone = mc.cone(radius=5, height=10)

# Frustum (truncated cone)
frustum = mc.cone(radius=5, height=10, top_radius=2)

# Torus
torus = mc.torus(major_radius=10, minor_radius=2)

# Display any geometry
mc.viewer(box)
```

### 2D Shapes

```python
# Circle
circle = mc.circle(radius=5)

# Rectangle
rect = mc.rectangle(width=20, height=10)

# Polygon
triangle = mc.polygon([(0, 0), (10, 0), (5, 8.66)])

# Text
text_face = mc.text("Hello", font_size=12, font="Arial")
```

## Transformations

### Translation

```python
box = mc.box(10, 10, 10)

# Move along X axis
moved_x = mc.translate(box, x=5)

# Move in 3D space
moved_xyz = mc.translate(box, x=5, y=10, z=3)
```

### Rotation

```python
box = mc.box(20, 10, 5)

# Rotate around Z axis
rotated = mc.rotate(box, angle=45, axis="Z")

# Rotate around custom axis
rotated_custom = mc.rotate(box, angle=30, axis=(1, 1, 0))

# Rotate around a specific point
rotated_centered = mc.rotate(
    box,
    angle=45,
    axis="Z",
    center=(10, 5, 2.5)
)
```

### Scaling

```python
box = mc.box(10, 10, 10)

# Uniform scaling
bigger = mc.scale(box, factor=2.0)

# Non-uniform scaling
stretched = mc.scale(box, factor=(2, 1, 0.5))

# Scale from specific center
scaled = mc.scale(box, factor=1.5, center=(5, 5, 5))
```

### Mirroring

```python
box = mc.box(20, 10, 5)

# Mirror across XY plane
mirrored_xy = mc.mirror(box, plane="XY")

# Mirror across custom plane
mirrored_custom = mc.mirror(box, plane=(1, 0, 1))
```

## Boolean Operations

### Union

```python
# Create two overlapping boxes
box1 = mc.box(20, 20, 10)
box2 = mc.translate(mc.box(20, 20, 10), x=10)

# Combine them
combined = mc.union(box1, box2)

# Union multiple objects
box3 = mc.translate(mc.box(20, 20, 10), x=20)
all_combined = mc.union(box1, box2, box3)
```

### Subtraction

```python
# Box with cylindrical hole
box = mc.box(30, 30, 10)
hole = mc.cylinder(radius=5, height=15)
hole = mc.translate(hole, x=15, y=15)

result = mc.subtract(box, hole)

# Multiple subtractions
hole2 = mc.translate(hole, x=-10)
result = mc.subtract(box, hole, hole2)
```

### Intersection

```python
# Create intersection of sphere and box
sphere = mc.sphere(radius=15)
box = mc.box(20, 20, 20, center=True)

intersection = mc.intersect(sphere, box)
```

## Modifications

### Fillets

```python
box = mc.box(20, 20, 10)

# Fillet all edges
rounded = mc.fillet(box, radius=2.0)

# Fillet specific edges
top_face = mc.select_faces(box, ">Z")
top_edges = mc.select_edges(top_face[0])
selective_fillet = mc.fillet(box, radius=2.0, edges=top_edges)
```

### Chamfers

```python
box = mc.box(20, 20, 10)

# Chamfer all edges
chamfered = mc.chamfer(box, distance=2.0)

# Chamfer specific edges
edges = mc.select_edges(box, "parallel_to_z")
selective_chamfer = mc.chamfer(box, distance=1.5, edges=edges)
```

### Shell (Hollow)

```python
box = mc.box(40, 30, 20)

# Create hollow box with wall thickness
top_face = mc.select_faces(box, ">Z")
hollow = mc.shell(box, thickness=2.0, faces=top_face)
```

### Offset

```python
box = mc.box(20, 20, 10)

# Offset outward
larger = mc.offset(box, distance=2.0)

# Offset inward
smaller = mc.offset(box, distance=-1.0)
```

## 2D to 3D Operations

### Extrusion

```python
# Extrude circle to create cylinder
circle = mc.circle(radius=5)
cylinder = mc.extrude(circle, distance=20)

# Extrude with taper
tapered = mc.extrude(circle, distance=20, taper=5)

# Extrude in custom direction
profile = mc.rectangle(10, 5)
extruded = mc.extrude(profile, distance=15, direction=(1, 0, 1))
```

### Revolution

```python
# Revolve profile to create bottle
profile = mc.polygon([
    (0, 0), (5, 0), (5, 10), (3, 12),
    (3, 15), (4, 18), (4, 20), (0, 20)
])

bottle = mc.revolve(profile, angle=360, axis="Z")

# Partial revolution
half_bottle = mc.revolve(profile, angle=180, axis="Z")
```

### Lofting

```python
# Create loft through multiple profiles
circle1 = mc.circle(radius=5)
circle2 = mc.translate(mc.circle(radius=8), z=10)
circle3 = mc.translate(mc.circle(radius=3), z=20)

lofted = mc.loft([circle1, circle2, circle3])

# Ruled loft
ruled_loft = mc.loft([circle1, circle2], ruled=True)
```

### Sweeping

```python
# Create path
from marimocad.sketch import line, arc

path = line((0, 0, 0), (10, 0, 0))
path = arc((10, 0, 0), (20, 10, 0), radius=10)

# Sweep circle along path
circle = mc.circle(radius=2)
pipe = mc.sweep(circle, path)
```

## Assemblies

### Basic Assembly

```python
# Create assembly
robot = mc.Assembly(name="simple_robot")

# Add base
base = mc.cylinder(radius=30, height=10)
robot.add_part(base, name="base", position=(0, 0, 0))

# Add column
column = mc.cylinder(radius=5, height=50)
robot.add_part(column, name="column", position=(0, 0, 10))

# Add arm
arm = mc.box(80, 10, 10)
robot.add_part(arm, name="arm", position=(40, 0, 60))

# Get all parts
all_parts = robot.parts()

# Display
mc.viewer(robot)
```

### Assembly with Constraints

```python
# Create assembly
mechanism = mc.Assembly(name="mechanism")

# Add parts
gear1 = mc.gear(num_teeth=20, module=2, thickness=5)
gear2 = mc.gear(num_teeth=40, module=2, thickness=5)

mechanism.add_part(gear1, name="gear1", position=(0, 0, 0))
mechanism.add_part(gear2, name="gear2", position=(60, 0, 0))

# Add constraint to maintain gear contact
mechanism.add_constraint(
    constraint_type="distance",
    part1="gear1",
    part2="gear2",
    distance=60  # Center distance for meshing gears
)

# Solve constraints
mechanism.solve()
```

## Component Library

### Mechanical Components

```python
# M8 screw
screw = mc.screw(
    diameter=8,
    length=30,
    thread_pitch=1.25,
    head_type="hex"
)

# Spur gear
gear = mc.gear(
    num_teeth=30,
    module=2.5,
    thickness=10,
    pressure_angle=20
)

# Ball bearing
bearing = mc.bearing(
    inner_diameter=8,
    outer_diameter=22,
    thickness=7
)
```

### Structural Profiles

```python
# I-beam profile
i_beam_profile = mc.i_beam(
    height=200,
    width=150,
    web_thickness=10,
    flange_thickness=15
)

# Extrude to create beam
beam = mc.extrude(i_beam_profile, distance=1000)

# Channel profile
channel_profile = mc.channel(
    height=100,
    width=50,
    thickness=5
)
channel = mc.extrude(channel_profile, distance=500)
```

## Reactive Modeling

### Simple Reactive Box

```python
import marimo as mo
import marimocad as mc

# Create reactive sliders
length = mo.ui.slider(start=5, stop=50, value=20, label="Length")
width = mo.ui.slider(start=5, stop=50, value=15, label="Width")
height = mo.ui.slider(start=5, stop=30, value=10, label="Height")

# Display controls
mo.vstack([length, width, height])

# Create reactive geometry
box = mc.box(length.value, width.value, height.value)

# Display
mc.viewer(box)
```

### Parametric Box with Hole

```python
import marimo as mo
import marimocad as mc

# Parameters
box_size = mo.ui.slider(start=10, stop=50, value=30, label="Box Size")
hole_diameter = mo.ui.slider(start=2, stop=20, value=8, label="Hole Diameter")
fillet_radius = mo.ui.slider(start=0, stop=5, value=2, label="Fillet Radius")

mo.vstack([box_size, hole_diameter, fillet_radius])

# Create geometry
box = mc.box(box_size.value, box_size.value, box_size.value / 2)

# Add hole
hole = mc.cylinder(
    radius=hole_diameter.value / 2,
    height=box_size.value
)
hole = mc.translate(hole, x=box_size.value / 2, y=box_size.value / 2)

result = mc.subtract(box, hole)

# Add fillets if radius > 0
if fillet_radius.value > 0:
    result = mc.fillet(result, radius=fillet_radius.value)

# Display
mc.viewer(result)
```

### Parametric Gear Train

```python
import marimo as mo
import marimocad as mc

# Parameters
teeth1 = mo.ui.slider(start=10, stop=50, value=20, label="Gear 1 Teeth")
teeth2 = mo.ui.slider(start=10, stop=50, value=40, label="Gear 2 Teeth")
module = mo.ui.slider(start=1, stop=5, value=2, label="Module")

mo.vstack([teeth1, teeth2, module])

# Create gears
gear1 = mc.gear(
    num_teeth=int(teeth1.value),
    module=module.value,
    thickness=5
)

gear2 = mc.gear(
    num_teeth=int(teeth2.value),
    module=module.value,
    thickness=5
)

# Calculate center distance for meshing
center_distance = (teeth1.value + teeth2.value) * module.value / 2
gear2 = mc.translate(gear2, x=center_distance)

# Combine for visualization
gears = mc.union(gear1, gear2)

mc.viewer(gears)
```

### Using Parametric Model Helper

```python
import marimo as mo
import marimocad as mc

def create_bottle(height, radius, neck_radius, neck_height):
    """Create a parametric bottle."""
    # Body
    body = mc.cylinder(radius=radius, height=height - neck_height)

    # Neck
    neck = mc.cylinder(radius=neck_radius, height=neck_height)
    neck = mc.translate(neck, z=height - neck_height)

    return mc.union(body, neck)

# Create UI
params = {
    "height": mo.ui.slider(20, 100, value=60, label="Height"),
    "radius": mo.ui.slider(5, 30, value=15, label="Radius"),
    "neck_radius": mo.ui.slider(2, 15, value=5, label="Neck Radius"),
    "neck_height": mo.ui.slider(5, 40, value=15, label="Neck Height"),
}

# Create and display parametric model
mc.parametric_model(create_bottle, params)
```

## Import/Export

### Exporting

```python
import marimocad as mc

# Create geometry
box = mc.box(20, 15, 10)
box = mc.fillet(box, radius=2.0)

# Export to STEP
mc.export_step(box, "part.step")

# Export to STL for 3D printing
mc.export_stl(
    box,
    "part.stl",
    linear_deflection=0.1,
    angular_deflection=0.5
)

# Export to SVG (2D projection)
mc.export_svg(box, "part_top.svg", view="top")
mc.export_svg(box, "part_iso.svg", view="iso")
```

### Importing

```python
import marimocad as mc

# Import STEP file
imported = mc.import_step("model.step")

# Import STL file
mesh = mc.import_stl("scan.stl")

# Modify imported geometry
modified = mc.fillet(imported, radius=1.0)

# Export modified version
mc.export_step(modified, "modified.step")
```

## Advanced Examples

### Complex Part with Multiple Features

```python
import marimocad as mc

def create_bracket(
    base_length: float = 50,
    base_width: float = 40,
    base_height: float = 5,
    wall_height: float = 30,
    wall_thickness: float = 5,
    hole_diameter: float = 6,
    fillet_radius: float = 2,
):
    """Create a mounting bracket."""

    # Base plate
    base = mc.box(base_length, base_width, base_height)

    # Vertical wall
    wall = mc.box(wall_thickness, base_width, wall_height)
    wall = mc.translate(wall, z=base_height)

    # Combine
    bracket = mc.union(base, wall)

    # Add mounting holes in base
    hole1 = mc.cylinder(radius=hole_diameter / 2, height=base_height * 2)
    hole1 = mc.translate(hole1, x=10, y=base_width / 2, z=-base_height / 2)

    hole2 = mc.translate(hole1, x=base_length - 20)

    bracket = mc.subtract(bracket, hole1, hole2)

    # Add holes in wall
    wall_hole = mc.cylinder(radius=hole_diameter / 2, height=wall_thickness * 2)
    wall_hole = mc.rotate(wall_hole, angle=90, axis="Y")
    wall_hole = mc.translate(
        wall_hole,
        x=-wall_thickness / 2,
        y=base_width / 2,
        z=base_height + wall_height / 2
    )

    bracket = mc.subtract(bracket, wall_hole)

    # Add fillets
    bracket = mc.fillet(bracket, radius=fillet_radius)

    return bracket

# Create bracket
bracket = create_bracket()
mc.viewer(bracket)

# Export
mc.export_step(bracket, "bracket.step")
```

### Parametric Enclosure

```python
import marimocad as mc

def create_enclosure(
    length: float = 100,
    width: float = 80,
    height: float = 40,
    wall_thickness: float = 2,
    corner_radius: float = 5,
):
    """Create an electronics enclosure."""

    # Outer shell
    outer = mc.box(length, width, height)

    # Round corners
    outer = mc.fillet(outer, radius=corner_radius)

    # Create cavity
    cavity = mc.box(
        length - 2 * wall_thickness,
        width - 2 * wall_thickness,
        height - wall_thickness
    )
    cavity = mc.translate(
        cavity,
        x=wall_thickness,
        y=wall_thickness,
        z=wall_thickness
    )

    # Shell it
    enclosure = mc.subtract(outer, cavity)

    # Add mounting posts
    post = mc.cylinder(radius=3, height=height - wall_thickness)
    post = mc.translate(post, z=wall_thickness)

    post_positions = [
        (10, 10, 0),
        (length - 10, 10, 0),
        (10, width - 10, 0),
        (length - 10, width - 10, 0),
    ]

    for x, y, z in post_positions:
        positioned_post = mc.translate(post, x=x, y=y)
        enclosure = mc.union(enclosure, positioned_post)

    return enclosure

# Create enclosure
enclosure = create_enclosure()
mc.viewer(enclosure)
```

### Gear Box Assembly

```python
import marimocad as mc

def create_gearbox():
    """Create a simple gearbox assembly."""

    # Housing
    housing = mc.box(120, 80, 60)
    housing = mc.fillet(housing, radius=5)

    # Cavity
    cavity = mc.box(110, 70, 50)
    cavity = mc.translate(cavity, x=5, y=5, z=5)
    housing = mc.subtract(housing, cavity)

    # Gears
    gear1 = mc.gear(num_teeth=20, module=2, thickness=15)
    gear1 = mc.translate(gear1, x=30, y=40, z=30)

    gear2 = mc.gear(num_teeth=40, module=2, thickness=15)
    gear2 = mc.translate(gear2, x=70, y=40, z=30)

    # Shafts
    shaft1 = mc.cylinder(radius=5, height=60)
    shaft1 = mc.rotate(shaft1, angle=90, axis="Y")
    shaft1 = mc.translate(shaft1, x=30, y=40, z=30)

    shaft2 = mc.cylinder(radius=5, height=60)
    shaft2 = mc.rotate(shaft2, angle=90, axis="Y")
    shaft2 = mc.translate(shaft2, x=70, y=40, z=30)

    # Combine
    assembly = mc.union(housing, gear1, gear2, shaft1, shaft2)

    return assembly

# Create and display
gearbox = create_gearbox()
mc.viewer(gearbox)

# Export
mc.export_step(gearbox, "gearbox.step")
```

## Tips and Best Practices

### 1. Use Named Parameters

```python
# Good
box = mc.box(length=20, width=15, height=10)

# Less clear
box = mc.box(20, 15, 10)
```

### 2. Build Complex Models Incrementally

```python
# Start simple
model = mc.box(50, 40, 20)

# Add features one at a time
model = mc.fillet(model, radius=2)

hole = mc.cylinder(radius=3, height=25)
hole = mc.translate(hole, x=25, y=20)
model = mc.subtract(model, hole)

# Continue building...
```

### 3. Use Variables for Magic Numbers

```python
# Good
BASE_SIZE = 50
HOLE_DIAMETER = 8
FILLET_RADIUS = 2

base = mc.box(BASE_SIZE, BASE_SIZE, 10)
base = mc.fillet(base, radius=FILLET_RADIUS)

# Not ideal
base = mc.box(50, 50, 10)
base = mc.fillet(base, radius=2)
```

### 4. Leverage Reactive Programming

```python
# Let Marimo handle reactivity
# When slider changes, everything updates automatically

length = mo.ui.slider(10, 100, value=50)
box = mc.box(length.value, length.value, length.value / 2)
```

### 5. Export Early and Often

```python
# Export intermediate steps for verification
base = mc.box(50, 40, 20)
mc.export_step(base, "step1_base.step")

with_holes = mc.subtract(base, holes)
mc.export_step(with_holes, "step2_holes.step")

final = mc.fillet(with_holes, radius=2)
mc.export_step(final, "final.step")
```

---

**Version**: 1.0
**Last Updated**: 2024-12-15
