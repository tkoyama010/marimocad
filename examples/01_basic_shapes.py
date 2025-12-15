"""
Example 1: Basic Shapes

This example demonstrates how to create and use basic 3D shapes
in marimocad.
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    mo.md("# Basic Shapes in marimocad")
    return mo,


@app.cell
def __():
    import marimocad as mc
    import numpy as np
    return mc, np


@app.cell
def __(mo):
    mo.md("""
    ## Creating Basic Shapes
    
    marimocad provides three fundamental 3D shapes:
    - **Box**: A rectangular cuboid
    - **Cylinder**: A cylindrical shape
    - **Sphere**: A spherical shape
    """)
    return


@app.cell
def __(mc, mo):
    # Create a box
    box = mc.Box(width=10, height=5, depth=3, name="my_box")
    
    mo.md(f"""
    ### Box
    
    ```python
    box = mc.Box(width=10, height=5, depth=3, name="my_box")
    ```
    
    **Properties:**
    - Volume: {box.volume():.2f} cubic units
    - Surface Area: {box.surface_area():.2f} square units
    - Bounds: {box.get_bounds()}
    """)
    return box,


@app.cell
def __(mc, mo):
    # Create a cylinder
    cylinder = mc.Cylinder(radius=3, height=10, name="my_cylinder")
    
    mo.md(f"""
    ### Cylinder
    
    ```python
    cylinder = mc.Cylinder(radius=3, height=10, name="my_cylinder")
    ```
    
    **Properties:**
    - Volume: {cylinder.volume():.2f} cubic units
    - Surface Area: {cylinder.surface_area():.2f} square units
    - Bounds: {cylinder.get_bounds()}
    """)
    return cylinder,


@app.cell
def __(mc, mo):
    # Create a sphere
    sphere = mc.Sphere(radius=5, name="my_sphere")
    
    mo.md(f"""
    ### Sphere
    
    ```python
    sphere = mc.Sphere(radius=5, name="my_sphere")
    ```
    
    **Properties:**
    - Volume: {sphere.volume():.2f} cubic units
    - Surface Area: {sphere.surface_area():.2f} square units
    - Bounds: {sphere.get_bounds()}
    """)
    return sphere,


@app.cell
def __(mo):
    mo.md("""
    ## Creating a Cube
    
    A cube is just a box with equal dimensions:
    """)
    return


@app.cell
def __(mc, mo):
    # Create a cube (box with equal dimensions)
    cube = mc.Box(width=5, height=5, depth=5, name="cube")
    
    mo.md(f"""
    ```python
    cube = mc.Box(width=5, height=5, depth=5, name="cube")
    ```
    
    **Properties:**
    - Volume: {cube.volume():.2f} cubic units
    - Surface Area: {cube.surface_area():.2f} square units
    """)
    return cube,


@app.cell
def __(mo):
    mo.md("""
    ## Error Handling
    
    All shapes validate their parameters and raise helpful errors:
    """)
    return


@app.cell
def __(mc, mo):
    # This will raise an error
    try:
        invalid_box = mc.Box(width=-5, height=10, depth=3)
    except ValueError as e:
        error_message = str(e)
    
    mo.md(f"""
    ```python
    try:
        invalid_box = mc.Box(width=-5, height=10, depth=3)
    except ValueError as e:
        print(e)  # "All dimensions must be positive"
    ```
    
    **Error:** `{error_message}`
    """)
    return error_message,


@app.cell
def __(mo):
    mo.md("""
    ## Next Steps
    
    - See `02_boolean_operations.py` to learn how to combine shapes
    - See `03_transformations.py` to learn how to move and transform shapes
    """)
    return


if __name__ == "__main__":
    app.run()
