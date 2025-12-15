"""
marimocad Example Usage

This file demonstrates various usage patterns for the marimocad library.
These examples show how to create, manipulate, and visualize CAD models
in a Marimo notebook environment.
"""

# =============================================================================
# Example 1: Basic Primitive Creation and Visualization
# =============================================================================

import marimo as mo
from marimocad import primitives, visualize

# Create basic shapes
box = primitives.box(width=20, height=20, depth=20)
sphere = primitives.sphere(radius=15)
cylinder = primitives.cylinder(radius=5, height=30)

# Visualize individual shapes
viewer1 = visualize(box, color="#FF6B6B")
viewer2 = visualize(sphere, color="#4ECDC4")
viewer3 = visualize(cylinder, color="#45B7D1")

# Display in Marimo
mo.hstack([viewer1, viewer2, viewer3])


# =============================================================================
# Example 2: Boolean Operations
# =============================================================================

from marimocad import primitives, visualize

# Create shapes
cube = primitives.box(30, 30, 30)
sphere = primitives.sphere(radius=20)

# Boolean operations
union = cube + sphere
difference = cube - sphere
intersection = cube & sphere

# Visualize results
mo.hstack([
    visualize(union, color="#FF6B6B"),
    visualize(difference, color="#4ECDC4"),
    visualize(intersection, color="#45B7D1")
])


# =============================================================================
# Example 3: Transformations
# =============================================================================

from marimocad import primitives, visualize

# Create base shape
base = primitives.box(10, 10, 10)

# Apply transformations
translated = base.translate(x=20, y=0, z=0)
rotated = base.rotate(axis="Z", angle=45).translate(x=40, y=0, z=0)
scaled = base.scale(x=2, y=1, z=1).translate(x=60, y=0, z=0)

# Visualize transformations
visualize([base, translated, rotated, scaled])


# =============================================================================
# Example 4: Reactive Parameters with Marimo
# =============================================================================

import marimo as mo
from marimocad import primitives, visualize

# Create reactive controls
radius = mo.ui.slider(5, 30, value=15, label="Radius")
height = mo.ui.slider(10, 50, value=30, label="Height")
segments = mo.ui.slider(3, 8, value=6, label="Segments")

# Create parametric shape
cylinder = primitives.cylinder(radius=radius.value, height=height.value)

# Optional: Create a multi-sided prism instead
if segments.value > 4:
    profile = primitives.polygon(
        points=[(radius.value * np.cos(i * 2 * np.pi / segments.value),
                 radius.value * np.sin(i * 2 * np.pi / segments.value))
                for i in range(segments.value)]
    )
    shape = profile.extrude(distance=height.value)
else:
    shape = cylinder

# Display controls and visualization
mo.vstack([
    mo.hstack([radius, height, segments]),
    visualize(shape, color="#FF6B6B")
])


# =============================================================================
# Example 5: Sketch-Based Modeling
# =============================================================================

from marimocad import Sketch, BuildPart, visualize

# Create a complex part using sketch-based approach
with BuildPart() as bracket:
    # Base plate
    with Sketch(plane="XY") as base:
        base.add_rectangle(width=100, height=60)
    bracket.extrude(distance=5)
    
    # Mounting holes
    for x in [-35, 35]:
        for y in [-20, 20]:
            hole = primitives.cylinder(radius=4, height=5)
            hole = hole.translate(x=x, y=y, z=0)
            bracket.part = bracket.part - hole
    
    # Vertical wall
    with Sketch(plane="XZ") as wall:
        wall.add_rectangle(width=100, height=40, center=(0, 25))
    bracket.extrude(distance=5)
    
    # Fillet edges for strength
    bracket.fillet(edges=bracket.edges(), radius=3)

# Visualize the bracket
visualize(bracket.part, color="#4ECDC4", show_edges=True)


# =============================================================================
# Example 6: Parametric Component Class
# =============================================================================

import marimo as mo
from marimocad import Component, primitives, visualize

class ParametricFlange(Component):
    """A parametric flange component."""
    
    def __init__(self, outer_diameter, inner_diameter, thickness, bolt_holes):
        super().__init__()
        self.outer_diameter = outer_diameter
        self.inner_diameter = inner_diameter
        self.thickness = thickness
        self.bolt_holes = bolt_holes
    
    def build(self):
        # Main flange body
        outer = primitives.cylinder(
            radius=self.outer_diameter / 2,
            height=self.thickness
        )
        
        # Inner bore
        inner = primitives.cylinder(
            radius=self.inner_diameter / 2,
            height=self.thickness
        )
        
        flange = outer - inner
        
        # Bolt holes
        bolt_circle_radius = (self.outer_diameter + self.inner_diameter) / 4
        for i in range(self.bolt_holes):
            angle = i * 2 * 3.14159 / self.bolt_holes
            x = bolt_circle_radius * np.cos(angle)
            y = bolt_circle_radius * np.sin(angle)
            
            hole = primitives.cylinder(radius=3, height=self.thickness)
            hole = hole.translate(x=x, y=y, z=0)
            flange = flange - hole
        
        return flange

# Create interactive flange
outer_d = mo.ui.slider(50, 150, value=100, label="Outer Diameter")
inner_d = mo.ui.slider(20, 80, value=40, label="Inner Diameter")
thickness = mo.ui.slider(5, 20, value=10, label="Thickness")
holes = mo.ui.slider(4, 12, value=8, label="Bolt Holes")

flange = ParametricFlange(
    outer_diameter=outer_d.value,
    inner_diameter=inner_d.value,
    thickness=thickness.value,
    bolt_holes=holes.value
)

mo.vstack([
    mo.hstack([outer_d, inner_d, thickness, holes]),
    visualize(flange.build(), color="#45B7D1")
])


# =============================================================================
# Example 7: Assembly Creation
# =============================================================================

from marimocad import Assembly, primitives, visualize

# Create an assembly
motor_assembly = Assembly(name="simple_motor")

# Add base plate
base = primitives.box(width=150, height=100, depth=10)
motor_assembly.add_part("base", base, position=(0, 0, 0))

# Add motor body
motor_body = primitives.cylinder(radius=25, height=60)
motor_assembly.add_part(
    "motor",
    motor_body,
    position=(0, 0, 10),
    rotation=(90, 0, 0)  # Rotate to align horizontally
)

# Add motor shaft
shaft = primitives.cylinder(radius=5, height=100)
motor_assembly.add_part(
    "shaft",
    shaft,
    position=(0, 0, 40),
    rotation=(90, 0, 0)
)

# Add mounting brackets
for x in [-50, 50]:
    bracket = primitives.box(width=20, height=60, depth=40)
    motor_assembly.add_part(
        f"bracket_{x}",
        bracket,
        position=(x, 0, 10)
    )

# Visualize assembly
visualize(motor_assembly, show_edges=True)

# Export assembly
motor_assembly.export_step("motor_assembly.step")


# =============================================================================
# Example 8: Advanced Surface Modeling with Loft
# =============================================================================

from marimocad import primitives, loft, visualize
import numpy as np

# Create profiles at different heights
profiles = []

# Bottom profile - large circle
profiles.append(
    primitives.circle(radius=20).translate(z=0)
)

# Middle profile - square
profiles.append(
    primitives.rectangle(width=30, height=30).translate(z=20)
)

# Top profile - small circle
profiles.append(
    primitives.circle(radius=10).translate(z=40)
)

# Loft between profiles
vase = loft(profiles)

# Visualize
visualize(vase, color="#FF6B6B", opacity=0.9)


# =============================================================================
# Example 9: Sweep Operation
# =============================================================================

from marimocad import primitives, spline, sweep, visualize
import numpy as np

# Define sweep path (helix)
t = np.linspace(0, 4 * np.pi, 100)
path_points = [
    (10 * np.cos(ti), 10 * np.sin(ti), ti * 5)
    for ti in t
]
path = spline(points=path_points, degree=3)

# Define profile to sweep
profile = primitives.circle(radius=2)

# Perform sweep
spring = sweep(profile=profile, path=path)

# Visualize
visualize(spring, color="#4ECDC4")


# =============================================================================
# Example 10: Complex Part with Modifications
# =============================================================================

from marimocad import primitives, visualize

# Create base shape
body = primitives.box(width=60, height=40, depth=30)

# Add features through boolean operations
feature1 = primitives.cylinder(radius=8, height=30)
feature1 = feature1.translate(x=-20, y=0, z=0)
body = body - feature1

feature2 = primitives.cylinder(radius=8, height=30)
feature2 = feature2.translate(x=20, y=0, z=0)
body = body - feature2

# Add chamfers and fillets
body = body.chamfer(
    edges=body.edges(">Z"),  # Top edges
    distance=3
)
body = body.fillet(
    edges=body.edges("<Z"),  # Bottom edges
    radius=5
)

# Shell the part
body = body.shell(
    faces=[body.faces(">Y")[0]],  # Remove top face
    thickness=3
)

# Visualize final part
visualize(body, color="#45B7D1", show_edges=True)


# =============================================================================
# Example 11: Measurements and Queries
# =============================================================================

from marimocad import primitives
import marimo as mo

# Create a complex shape
box = primitives.box(30, 20, 15)
sphere = primitives.sphere(radius=12)
part = box - sphere

# Get measurements
volume = part.volume
surface_area = part.surface_area
center = part.center_of_mass
bbox = part.bounding_box

# Display measurements
mo.md(f"""
## Part Properties

- **Volume:** {volume:.2f} cubic units
- **Surface Area:** {surface_area:.2f} square units
- **Center of Mass:** ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f})
- **Bounding Box:**
  - Min: ({bbox.min[0]:.2f}, {bbox.min[1]:.2f}, {bbox.min[2]:.2f})
  - Max: ({bbox.max[0]:.2f}, {bbox.max[1]:.2f}, {bbox.max[2]:.2f})
- **Number of Faces:** {len(part.faces())}
- **Number of Edges:** {len(part.edges())}
- **Number of Vertices:** {len(part.vertices())}
""")


# =============================================================================
# Example 12: File Import/Export
# =============================================================================

from marimocad import io, primitives, visualize

# Create a part
part = primitives.box(50, 30, 20)
part = part.fillet(edges=part.edges(), radius=3)

# Export to various formats
io.export_step(part, "part.step")
io.export_stl(part, "part.stl", linear_deflection=0.01)
io.export_obj(part, "part.obj")
io.export_gltf(part, "part.gltf")

# Import from file
imported_part = io.import_step("existing_model.step")
visualize(imported_part)


# =============================================================================
# Example 13: Interactive Design Iteration
# =============================================================================

import marimo as mo
from marimocad import primitives, visualize

# Create multiple design variations
length = mo.ui.slider(20, 100, value=50, label="Length")
width = mo.ui.slider(10, 50, value=30, label="Width")
height = mo.ui.slider(5, 30, value=15, label="Height")
corner_radius = mo.ui.slider(0, 10, value=5, label="Corner Radius")

# Create parametric box
box = primitives.box(length.value, width.value, height.value)

# Apply corner radius if > 0
if corner_radius.value > 0:
    box = box.fillet(edges=box.edges(), radius=corner_radius.value)

# Calculate and display properties
volume = box.volume
mass = volume * 0.00785  # Assuming steel density (g/mm³)

# Display everything
mo.vstack([
    mo.md("## Parametric Box Designer"),
    mo.hstack([length, width, height, corner_radius]),
    mo.md(f"""
    ### Properties
    - Volume: {volume:.2f} mm³
    - Estimated Mass: {mass:.2f} g (steel)
    """),
    visualize(box, color="#FF6B6B", show_edges=True)
])


# =============================================================================
# Example 14: Pattern Creation
# =============================================================================

from marimocad import primitives, visualize
import numpy as np

# Create base feature
feature = primitives.cylinder(radius=3, height=20)

# Create circular pattern
num_features = 8
radius = 30
result = None

for i in range(num_features):
    angle = i * 2 * np.pi / num_features
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    
    positioned_feature = feature.translate(x=x, y=y, z=0)
    
    if result is None:
        result = positioned_feature
    else:
        result = result + positioned_feature

# Add center hub
hub = primitives.cylinder(radius=15, height=15)
result = result + hub

# Visualize pattern
visualize(result, color="#4ECDC4")


# =============================================================================
# Example 15: Complex Assembly with Constraints
# =============================================================================

import marimo as mo
from marimocad import Assembly, primitives, visualize

# Create a gear assembly example
def create_gear(num_teeth, module, thickness):
    """Simple gear approximation."""
    # Pitch diameter
    pitch_diameter = num_teeth * module
    
    # Create base cylinder
    gear = primitives.cylinder(radius=pitch_diameter/2, height=thickness)
    
    # Add center hole
    hole = primitives.cylinder(radius=module, height=thickness)
    gear = gear - hole
    
    return gear

# Create assembly
gear_assembly = Assembly(name="gear_train")

# Add first gear
gear1 = create_gear(num_teeth=20, module=2, thickness=10)
gear_assembly.add_part("gear1", gear1, position=(-22, 0, 0))

# Add second gear (larger)
gear2 = create_gear(num_teeth=30, module=2, thickness=10)
gear_assembly.add_part("gear2", gear2, position=(32, 0, 0))

# Add base plate
plate = primitives.box(width=120, height=80, depth=5)
gear_assembly.add_part("plate", plate, position=(0, 0, -8))

# Visualize
visualize(gear_assembly, show_edges=True)

# Export
gear_assembly.export_step("gear_assembly.step")
