"""
Basic 3D Visualization Example

This example demonstrates the core features of marimocad:
- Creating a 3D viewer
- Adding different geometries (box, sphere, cylinder)
- Customizing colors and opacity
- Interactive camera controls
"""

import marimo as mo

from marimocad import Viewer3D


def __() -> None:
    """
    Create a 3D viewer with multiple geometries.
    
    This demonstrates:
    - Creating a viewer with custom dimensions
    - Adding a box, sphere, and cylinder
    - Using different colors for each geometry
    - Method chaining for concise code
    """
    viewer = Viewer3D(width=800, height=600)
    
    # Add geometries with different colors
    viewer.add_box(
        center=[0, 0, 0],
        size=[1, 1, 1],
        color="blue",
        opacity=0.8,
        name="Blue Box"
    )
    
    viewer.add_sphere(
        center=[2, 0, 0],
        radius=0.5,
        color="red",
        opacity=0.8,
        name="Red Sphere"
    )
    
    viewer.add_cylinder(
        center=[0, 2, 0],
        radius=0.5,
        height=1.5,
        color="green",
        opacity=0.8,
        name="Green Cylinder"
    )
    
    # Set camera position for a good view
    viewer.set_camera(
        eye=dict(x=3, y=3, z=3),
        center=dict(x=1, y=1, z=0),
        up=dict(x=0, y=0, z=1)
    )
    
    return viewer.show()


def __() -> None:
    """
    Interactive Example: Use Marimo sliders to control geometry.
    
    This demonstrates reactivity - the 3D view updates when sliders change.
    """
    # Create sliders
    radius_slider = mo.ui.slider(
        0.1, 2.0,
        value=0.5,
        step=0.1,
        label="Sphere Radius"
    )
    
    height_slider = mo.ui.slider(
        0.5, 3.0,
        value=1.5,
        step=0.1,
        label="Cylinder Height"
    )
    
    return mo.vstack([
        mo.md("## Interactive Controls"),
        mo.md("Adjust the sliders to change the geometry:"),
        radius_slider,
        height_slider,
    ])


def __(radius_slider, height_slider) -> None:
    """
    Create a reactive 3D scene that updates based on slider values.
    """
    viewer = Viewer3D(width=800, height=600)
    
    # Box with fixed size
    viewer.add_box(
        center=[0, 0, 0],
        size=[1, 1, 1],
        color="blue",
        opacity=0.7,
        name="Box"
    )
    
    # Sphere with reactive radius
    viewer.add_sphere(
        center=[2, 0, 0],
        radius=radius_slider.value,
        color="red",
        opacity=0.8,
        name=f"Sphere (r={radius_slider.value:.1f})"
    )
    
    # Cylinder with reactive height
    viewer.add_cylinder(
        center=[0, 2, 0],
        radius=0.5,
        height=height_slider.value,
        color="green",
        opacity=0.8,
        name=f"Cylinder (h={height_slider.value:.1f})"
    )
    
    viewer.set_camera(
        eye=dict(x=3, y=3, z=3),
        center=dict(x=1, y=1, z=0)
    )
    
    return viewer.show()


def __() -> None:
    """
    Advanced Example: Multiple instances and complex arrangements.
    """
    return mo.md("""
    ## Advanced Features
    
    You can create complex scenes with multiple geometries:
    - Arrange objects in patterns
    - Use different materials and colors
    - Create assemblies of parts
    """)


def __() -> None:
    """Create a grid of colored boxes"""
    viewer = Viewer3D(width=800, height=600)
    
    colors = ["red", "blue", "green", "yellow", "purple", "orange"]
    
    for i in range(3):
        for j in range(3):
            viewer.add_box(
                center=[i * 1.5, j * 1.5, 0],
                size=[0.8, 0.8, 0.8],
                color=colors[(i + j) % len(colors)],
                opacity=0.8,
                name=f"Box ({i},{j})"
            )
    
    viewer.set_camera(
        eye=dict(x=5, y=5, z=5),
        center=dict(x=1.5, y=1.5, z=0)
    )
    
    return viewer.show()


def __() -> None:
    """Information about camera controls"""
    return mo.md("""
    ## Camera Controls
    
    The 3D viewer supports interactive controls:
    
    - **Rotate**: Click and drag to rotate the view
    - **Pan**: Right-click (or Shift+click) and drag to pan
    - **Zoom**: Use mouse wheel or pinch gesture to zoom
    - **Reset**: Double-click to reset the view
    - **Hover**: Move mouse over objects to see their names
    
    Try interacting with the visualizations above!
    """)


if __name__ == "__main__":
    mo.run()
