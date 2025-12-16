"""3D Visualization Demo for Marimo

This example demonstrates the new 3D visualization capabilities in marimocad.
It shows:
- Interactive 3D viewer with camera controls
- Reactive updates when parameters change
- Multiple geometries in one view
- Geometry selection and highlighting
"""

import marimo


__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo

    return (mo,)


@app.cell
def __(mo):
    mo.md("""
    # marimocad 3D Visualization Demo

    This notebook demonstrates the interactive 3D viewer for CAD geometries.
    The viewer uses Three.js for high-performance WebGL rendering.

    ## Features
    - 🎮 **Interactive Controls**: Orbit, pan, and zoom with mouse
    - 🔄 **Reactive Updates**: Model updates automatically when parameters change
    - 🎨 **Multiple Geometries**: Display multiple objects in one view
    - 🖱️ **Selection**: Click on objects to highlight them
    - 📐 **Grid & Axes**: Visual reference for orientation
    """)


@app.cell
def __(mo):
    mo.md("## Simple Box Example")


@app.cell
def __(mo):
    # Create reactive parameters for a simple box
    length = mo.ui.slider(start=5, stop=30, value=10, label="Length")
    width = mo.ui.slider(start=5, stop=30, value=10, label="Width")
    height = mo.ui.slider(start=5, stop=30, value=10, label="Height")

    mo.vstack([length, width, height])
    return height, length, width


@app.cell
def __(height, length, width):
    # Create a simple box geometry
    try:
        from build123d import Box, BuildPart

        with BuildPart() as simple_box:
            Box(length.value, width.value, height.value)

        box_part = simple_box.part
    except ImportError:
        # Fallback if build123d is not installed
        box_part = None
        print("build123d not installed. Install with: pip install build123d")
    return Box, BuildPart, box_part, simple_box


@app.cell
def __(box_part):
    # Display the box with the viewer
    try:
        import marimocad as mc

        if box_part is not None:
            mc.viewer(box_part, width=700, height=500)
        else:
            print("No geometry to display")
    except ImportError:
        print("marimocad not properly installed")
    return (mc,)


@app.cell
def __(mo):
    mo.md("""
    ## Complex Example: Parametric Bracket

    A more complex example with multiple features:
    - Base plate and vertical plate
    - Mounting holes
    - Lightening hole
    - Fillets
    """)


@app.cell
def __(mo):
    # Parameters for bracket
    bracket_length = mo.ui.slider(start=30, stop=100, value=50, label="Bracket Length")
    bracket_thickness = mo.ui.slider(start=3, stop=10, value=5, label="Thickness")
    mounting_holes = mo.ui.slider(start=2, stop=6, value=4, step=1, label="Mounting Holes")

    mo.vstack([bracket_length, bracket_thickness, mounting_holes])
    return bracket_length, bracket_thickness, mounting_holes


@app.cell
def __(bracket_length, bracket_thickness, mounting_holes):
    # Create parametric bracket
    try:
        from build123d import (
            Axis,
            Box,
            BuildPart,
            Cylinder,
            GridLocations,
            Hole,
            Locations,
            Mode,
            Plane,
            fillet,
        )

        with BuildPart() as bracket:
            # Base plate
            with BuildPart() as base_plate:
                Box(
                    bracket_length.value,
                    bracket_length.value / 2,
                    bracket_thickness.value,
                )

            # Vertical plate
            with BuildPart(Plane.XZ) as vertical_plate:
                Box(
                    bracket_length.value,
                    bracket_length.value / 2,
                    bracket_thickness.value,
                )

            # Add mounting holes to base
            hole_spacing = bracket_length.value / (mounting_holes.value + 1)
            with Locations(base_plate.faces().sort_by(Axis.Z)[-1]):
                with GridLocations(hole_spacing, hole_spacing, mounting_holes.value, 2):
                    Hole(bracket_thickness.value / 2)

            # Add lightening hole to vertical plate
            with Locations(vertical_plate.faces().sort_by(Axis.Y)[-1].center()):
                Cylinder(
                    bracket_length.value / 4,
                    bracket_thickness.value,
                    mode=Mode.SUBTRACT,
                )

            # Add fillets
            edges_to_fillet = bracket.edges().filter_by(Axis.Z, reverse=True)
            if edges_to_fillet:
                try:
                    fillet(edges_to_fillet, bracket_thickness.value / 2)
                except Exception:
                    pass  # Some edges might not be filleted

        bracket_part = bracket.part
    except ImportError:
        bracket_part = None
        print("build123d not installed")
    return (
        Axis,
        Cylinder,
        GridLocations,
        Hole,
        Locations,
        Mode,
        Plane,
        base_plate,
        bracket,
        bracket_part,
        edges_to_fillet,
        fillet,
        hole_spacing,
        vertical_plate,
    )


@app.cell
def __(bracket_part, mc):
    # Display the bracket
    if bracket_part is not None:
        mc.viewer(bracket_part, width=700, height=500)


@app.cell
def __(bracket_part, mc, mo):
    # Show geometry properties
    if bracket_part is not None:
        card = mc.GeometryCard(bracket_part)
        card.render()
    else:
        mo.md("No geometry to display properties for")
    return (card,)


@app.cell
def __(mo):
    mo.md("""
    ## Multiple Geometries

    The viewer can display multiple geometries at once with different colors.
    """)


@app.cell
def __():
    # Create multiple simple shapes
    try:
        from build123d import Box, BuildPart, Cylinder, Sphere

        with BuildPart() as part1:
            Box(10, 10, 10)

        with BuildPart() as part2:
            Cylinder(5, 15)

        with BuildPart() as part3:
            Sphere(7)

        parts = [part1.part, part2.part, part3.part]
    except ImportError:
        parts = []
    return Sphere, part1, part2, part3, parts


@app.cell
def __(mc, parts):
    # Display all parts together
    if parts:
        mc.viewer(parts, width=700, height=500)


@app.cell
def __(mo):
    mo.md("""
    ## Controls Guide

    ### Mouse Controls
    - **Left Click + Drag**: Rotate camera around the model
    - **Right Click + Drag**: Pan the camera
    - **Scroll Wheel**: Zoom in/out
    - **Click on Object**: Select and highlight geometry

    ### Display Options
    - **Wireframe Toggle**: Switch between solid and wireframe display
    - **Grid Helper**: Reference grid on the ground plane
    - **Axes Helper**: RGB axes (X=red, Y=green, Z=blue)

    ## Performance

    The viewer uses WebGL for hardware-accelerated rendering, providing smooth
    interaction even with complex geometries. The tessellation quality can be
    adjusted for a balance between visual quality and performance.

    ## Next Steps

    1. Export models to STEP, STL, or other formats
    2. Create assemblies with multiple parts
    3. Add custom components from the component library
    4. Apply materials and rendering effects
    """)


if __name__ == "__main__":
    app.run()
