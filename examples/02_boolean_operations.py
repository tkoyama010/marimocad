"""
Example 2: Boolean Operations

This example demonstrates how to combine shapes using
Constructive Solid Geometry (CSG) operations.
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    mo.md("# Boolean Operations in marimocad")
    return mo,


@app.cell
def __():
    import marimocad as mc
    return mc,


@app.cell
def __(mo):
    mo.md("""
    ## Constructive Solid Geometry (CSG)
    
    marimocad supports three fundamental boolean operations:
    - **Union**: Combines shapes together
    - **Intersection**: Finds the common volume between shapes
    - **Difference**: Subtracts one shape from another
    """)
    return


@app.cell
def __(mo):
    mo.md("### Union Operation")
    return


@app.cell
def __(mc, mo):
    # Create two overlapping boxes
    box1 = mc.Box(width=10, height=10, depth=10)
    box2 = mc.Box(width=8, height=8, depth=8)
    mc.translate(box2, x=5, y=5, z=5)
    
    # Union combines them
    union_result = mc.union(box1, box2, name="union_example")
    
    mo.md(f"""
    ```python
    box1 = mc.Box(width=10, height=10, depth=10)
    box2 = mc.Box(width=8, height=8, depth=8)
    mc.translate(box2, x=5, y=5, z=5)
    
    union_result = mc.union(box1, box2)
    ```
    
    **Result:** {union_result}
    
    **Bounds:** {union_result.get_bounds()}
    """)
    return box1, box2, union_result


@app.cell
def __(mo):
    mo.md("### Intersection Operation")
    return


@app.cell
def __(mc, mo):
    # Create overlapping shapes
    box3 = mc.Box(width=10, height=10, depth=10)
    sphere1 = mc.Sphere(radius=6)
    
    # Intersection finds common volume
    intersection_result = mc.intersection(box3, sphere1, name="rounded_cube")
    
    mo.md(f"""
    ```python
    box = mc.Box(width=10, height=10, depth=10)
    sphere = mc.Sphere(radius=6)
    
    # Creates a rounded cube
    intersection_result = mc.intersection(box, sphere)
    ```
    
    **Result:** {intersection_result}
    
    This creates a "rounded cube" effect - the sharp corners of the box
    are cut off by the sphere boundary.
    """)
    return box3, intersection_result, sphere1


@app.cell
def __(mo):
    mo.md("### Difference Operation")
    return


@app.cell
def __(mc, mo):
    # Create a box with a hole
    base_box = mc.Box(width=10, height=10, depth=10)
    hole_cylinder = mc.Cylinder(radius=3, height=15)
    
    # Difference subtracts the cylinder from the box
    difference_result = mc.difference(base_box, hole_cylinder, name="box_with_hole")
    
    mo.md(f"""
    ```python
    base_box = mc.Box(width=10, height=10, depth=10)
    hole_cylinder = mc.Cylinder(radius=3, height=15)
    
    # Creates a box with a cylindrical hole through it
    difference_result = mc.difference(base_box, hole_cylinder)
    ```
    
    **Result:** {difference_result}
    
    This creates a box with a cylindrical hole through its center.
    """)
    return base_box, difference_result, hole_cylinder


@app.cell
def __(mo):
    mo.md("### Complex Combinations")
    return


@app.cell
def __(mc, mo):
    # Create a more complex shape
    large_box = mc.Box(width=20, height=20, depth=10)
    sphere2 = mc.Sphere(radius=8)
    mc.translate(sphere2, x=7, y=7, z=0)
    
    sphere3 = mc.Sphere(radius=8)
    mc.translate(sphere3, x=-7, y=-7, z=0)
    
    # Subtract both spheres
    complex_result = mc.difference(large_box, sphere2, sphere3, name="complex_shape")
    
    mo.md(f"""
    ```python
    large_box = mc.Box(width=20, height=20, depth=10)
    
    sphere1 = mc.Sphere(radius=8)
    mc.translate(sphere1, x=7, y=7, z=0)
    
    sphere2 = mc.Sphere(radius=8)
    mc.translate(sphere2, x=-7, y=-7, z=0)
    
    # Subtract multiple shapes at once
    complex_result = mc.difference(large_box, sphere1, sphere2)
    ```
    
    **Result:** {complex_result}
    
    You can subtract multiple shapes from a base shape in a single operation.
    """)
    return complex_result, large_box, sphere2, sphere3


@app.cell
def __(mo):
    mo.md("""
    ## Nested Operations
    
    You can nest operations to create more complex shapes:
    """)
    return


@app.cell
def __(mc, mo):
    # Create nested operations
    outer_box = mc.Box(width=15, height=15, depth=15)
    inner_sphere = mc.Sphere(radius=8)
    
    # First create a rounded cube
    rounded = mc.intersection(outer_box, inner_sphere)
    
    # Then subtract a smaller sphere
    small_sphere = mc.Sphere(radius=5)
    
    # Final result is a hollow rounded cube
    hollow_rounded = mc.difference(rounded, small_sphere, name="hollow_rounded_cube")
    
    mo.md(f"""
    ```python
    outer_box = mc.Box(width=15, height=15, depth=15)
    inner_sphere = mc.Sphere(radius=8)
    rounded = mc.intersection(outer_box, inner_sphere)
    
    small_sphere = mc.Sphere(radius=5)
    hollow_rounded = mc.difference(rounded, small_sphere)
    ```
    
    **Result:** {hollow_rounded}
    
    This creates a hollow rounded cube by first rounding the corners,
    then subtracting an inner sphere.
    """)
    return hollow_rounded, inner_sphere, outer_box, rounded, small_sphere


@app.cell
def __(mo):
    mo.md("""
    ## Next Steps
    
    - See `03_transformations.py` to learn about transforming shapes
    - See `04_complex_model.py` for building complete CAD models
    """)
    return


if __name__ == "__main__":
    app.run()
