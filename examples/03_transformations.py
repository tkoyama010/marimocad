"""
Example 3: Transformations

This example demonstrates how to transform shapes using
translation, rotation, and scaling operations.
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    mo.md("# Transformations in marimocad")
    return mo,


@app.cell
def __():
    import marimocad as mc
    import numpy as np
    return mc, np


@app.cell
def __(mo):
    mo.md("""
    ## Transformation Operations
    
    marimocad provides several transformation operations:
    - **translate**: Move shapes in 3D space
    - **rotate**: Rotate shapes around an axis
    - **scale**: Resize shapes uniformly or non-uniformly
    - **mirror**: Reflect shapes across a plane
    """)
    return


@app.cell
def __(mo):
    mo.md("### Translation (Moving)")
    return


@app.cell
def __(mc, mo, np):
    # Create a box at origin
    box1 = mc.Box(width=5, height=5, depth=5)
    original_pos = box1.position.copy()
    
    # Move it to a new position
    mc.translate(box1, x=10, y=5, z=3)
    new_pos = box1.position.copy()
    
    mo.md(f"""
    ```python
    box = mc.Box(width=5, height=5, depth=5)
    mc.translate(box, x=10, y=5, z=3)
    ```
    
    **Original position:** {original_pos}
    
    **New position:** {new_pos}
    
    Translation moves a shape by adding to its position coordinates.
    """)
    return box1, new_pos, original_pos


@app.cell
def __(mo):
    mo.md("### Incremental Translation")
    return


@app.cell
def __(mc, mo):
    # Create a cylinder
    cylinder = mc.Cylinder(radius=2, height=8)
    
    # Move in steps
    mc.translate(cylinder, x=5)
    pos1 = cylinder.position.copy()
    
    mc.translate(cylinder, y=3)
    pos2 = cylinder.position.copy()
    
    mc.translate(cylinder, z=-2)
    pos3 = cylinder.position.copy()
    
    mo.md(f"""
    ```python
    cylinder = mc.Cylinder(radius=2, height=8)
    mc.translate(cylinder, x=5)      # position: {pos1}
    mc.translate(cylinder, y=3)      # position: {pos2}
    mc.translate(cylinder, z=-2)     # position: {pos3}
    ```
    
    Translations are cumulative - each call adds to the current position.
    """)
    return cylinder, pos1, pos2, pos3


@app.cell
def __(mo):
    mo.md("### Rotation")
    return


@app.cell
def __(mc, mo):
    # Create and rotate a box
    box2 = mc.Box(width=10, height=3, depth=3)
    
    # Rotate around z-axis
    mc.rotate(box2, angle=45, axis='z')
    
    mo.md(f"""
    ```python
    box = mc.Box(width=10, height=3, depth=3)
    mc.rotate(box, angle=45, axis='z')
    ```
    
    **Shape:** {box2}
    
    Rotation angles are in degrees. You can rotate around 'x', 'y', or 'z' axes.
    """)
    return box2,


@app.cell
def __(mo):
    mo.md("### Custom Rotation Axis")
    return


@app.cell
def __(mc, mo):
    # Rotate around a custom axis
    cylinder2 = mc.Cylinder(radius=3, height=10)
    
    # Rotate around a diagonal axis
    mc.rotate(cylinder2, angle=90, axis=(1, 1, 0))
    
    mo.md(f"""
    ```python
    cylinder = mc.Cylinder(radius=3, height=10)
    mc.rotate(cylinder, angle=90, axis=(1, 1, 0))
    ```
    
    You can specify a custom rotation axis as a (x, y, z) tuple.
    The axis (1, 1, 0) points diagonally in the XY plane.
    """)
    return cylinder2,


@app.cell
def __(mo):
    mo.md("### Uniform Scaling")
    return


@app.cell
def __(mc, mo):
    # Create a sphere and scale it
    sphere1 = mc.Sphere(radius=3)
    original_radius = sphere1.radius
    
    # Scale uniformly
    mc.scale(sphere1, factor=2.0)
    scaled_radius = sphere1.radius
    
    mo.md(f"""
    ```python
    sphere = mc.Sphere(radius=3)
    mc.scale(sphere, factor=2.0)
    ```
    
    **Original radius:** {original_radius}
    
    **Scaled radius:** {scaled_radius}
    
    Uniform scaling multiplies all dimensions by the same factor.
    """)
    return original_radius, scaled_radius, sphere1


@app.cell
def __(mo):
    mo.md("### Non-uniform Scaling")
    return


@app.cell
def __(mc, mo):
    # Create a box and scale non-uniformly
    box3 = mc.Box(width=5, height=5, depth=5)
    original_dims = (box3.width, box3.height, box3.depth)
    
    # Scale differently in each direction
    mc.scale(box3, x=2, y=1, z=0.5)
    scaled_dims = (box3.width, box3.height, box3.depth)
    
    mo.md(f"""
    ```python
    box = mc.Box(width=5, height=5, depth=5)
    mc.scale(box, x=2, y=1, z=0.5)
    ```
    
    **Original dimensions:** {original_dims}
    
    **Scaled dimensions:** {scaled_dims}
    
    Non-uniform scaling allows different factors for each axis.
    - X dimension doubled (×2)
    - Y dimension unchanged (×1)
    - Z dimension halved (×0.5)
    """)
    return box3, original_dims, scaled_dims


@app.cell
def __(mo):
    mo.md("### Mirroring")
    return


@app.cell
def __(mc, mo):
    # Create a box and mirror it
    box4 = mc.Box(width=5, height=5, depth=5)
    mc.translate(box4, z=10)
    original_z = box4.position[2]
    
    # Mirror across XY plane (flip Z)
    mc.mirror(box4, plane='xy')
    mirrored_z = box4.position[2]
    
    mo.md(f"""
    ```python
    box = mc.Box(width=5, height=5, depth=5)
    mc.translate(box, z=10)
    mc.mirror(box, plane='xy')
    ```
    
    **Original Z position:** {original_z}
    
    **Mirrored Z position:** {mirrored_z}
    
    Mirroring reflects a shape across a specified plane ('xy', 'xz', or 'yz').
    """)
    return box4, mirrored_z, original_z


@app.cell
def __(mo):
    mo.md("### Combining Transformations")
    return


@app.cell
def __(mc, mo):
    # Create a complex transformed shape
    cyl = mc.Cylinder(radius=2, height=10)
    
    # Apply multiple transformations
    mc.translate(cyl, x=5, y=5, z=0)
    mc.rotate(cyl, angle=45, axis='z')
    mc.scale(cyl, x=1.5, y=1.5, z=0.5)
    
    final_pos = cyl.position
    final_radius = cyl.radius
    final_height = cyl.height
    
    mo.md(f"""
    ```python
    cylinder = mc.Cylinder(radius=2, height=10)
    mc.translate(cylinder, x=5, y=5, z=0)
    mc.rotate(cylinder, angle=45, axis='z')
    mc.scale(cylinder, x=1.5, y=1.5, z=0.5)
    ```
    
    **Final position:** {final_pos}
    
    **Final radius:** {final_radius:.2f}
    
    **Final height:** {final_height:.2f}
    
    Transformations can be chained together to create complex arrangements.
    """)
    return cyl, final_height, final_pos, final_radius


@app.cell
def __(mo):
    mo.md("""
    ## Practical Example: Creating a Pattern
    
    Use transformations to create geometric patterns:
    """)
    return


@app.cell
def __(mc, mo):
    # Create a circular pattern of boxes
    boxes = []
    num_boxes = 8
    radius = 10
    
    for i in range(num_boxes):
        angle = (360 / num_boxes) * i
        box = mc.Box(width=2, height=2, depth=5, name=f"box_{i}")
        
        # Position in a circle
        import math
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        mc.translate(box, x=x, y=y, z=0)
        
        # Rotate to face center
        mc.rotate(box, angle=angle, axis='z')
        
        boxes.append(box)
    
    mo.md(f"""
    ```python
    boxes = []
    num_boxes = 8
    radius = 10
    
    for i in range(num_boxes):
        angle = (360 / num_boxes) * i
        box = mc.Box(width=2, height=2, depth=5)
        
        # Position in a circle
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        mc.translate(box, x=x, y=y, z=0)
        
        # Rotate to face center
        mc.rotate(box, angle=angle, axis='z')
        
        boxes.append(box)
    ```
    
    **Created {len(boxes)} boxes** in a circular pattern.
    
    This demonstrates how transformations can be used programmatically
    to create complex geometric arrangements.
    """)
    return angle, box, boxes, i, math, num_boxes, radius, x, y


@app.cell
def __(mo):
    mo.md("""
    ## Next Steps
    
    - See `04_complex_model.py` to build complete CAD models
    - See `05_parametric_design.py` for parametric modeling techniques
    """)
    return


if __name__ == "__main__":
    app.run()
