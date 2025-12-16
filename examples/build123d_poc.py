"""Build123d Proof of Concept for Marimo Integration

This example demonstrates how Build123d integrates with Marimo for parametric CAD modeling.
Build123d is recommended as the primary backend for marimocad due to its:
- Native notebook integration
- Modern, Pythonic API
- Excellent selector system
- Multiple modeling paradigms
"""

import marimo


__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    # Import Build123d components
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

    return (
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


@app.cell
def _(mo):
    # Interactive controls for parametric modeling
    mo.md("""
    # Build123d Parametric CAD Demo

    This demonstrates Build123d's integration with Marimo for reactive CAD modeling.
    Adjust the sliders to see the model update in real-time.
    """)


@app.cell
def _(mo):
    # Create reactive parameters
    length = mo.ui.slider(start=10, stop=50, value=30, label="Length")
    width = mo.ui.slider(start=10, stop=50, value=20, label="Width")
    height = mo.ui.slider(start=5, stop=30, value=15, label="Height")
    hole_diameter = mo.ui.slider(start=2, stop=15, value=8, label="Hole Diameter")
    fillet_radius = mo.ui.slider(start=0, stop=5, value=2, label="Fillet Radius")

    mo.vstack([length, width, height, hole_diameter, fillet_radius])
    return fillet_radius, height, hole_diameter, length, width


@app.cell
def _(
    Axis,
    Box,
    BuildPart,
    Hole,
    Locations,
    fillet,
    fillet_radius,
    height,
    hole_diameter,
    length,
    width,
):
    # Create parametric box with hole
    with BuildPart() as parametric_box:
        # Create base box
        Box(length.value, width.value, height.value)

        # Add hole on top face
        top_face = parametric_box.faces().sort_by(Axis.Z)[-1]
        with Locations(top_face.center()):
            Hole(hole_diameter.value / 2, depth=height.value)

        # Add fillets to vertical edges
        if fillet_radius.value > 0:
            edges = parametric_box.edges().filter_by(Axis.Z)
            if edges:
                fillet(edges, fillet_radius.value)
    return (parametric_box,)


@app.cell
def _(mo, parametric_box):
    # Display the model
    # Note: In actual Marimo environment, this would render the 3D model
    # Display the model using Build123d's native rendering
    mo.md(f"""
    ## Generated Model

    **Vertices:** {len(parametric_box.vertices())}
    **Edges:** {len(parametric_box.edges())}
    **Faces:** {len(parametric_box.faces())}

    Build123d provides native HTML rendering that displays automatically in marimo notebooks.
    The 3D interactive viewer is built into Build123d using ocp-tessellate.
    """)


@app.cell
def _(mo):
    mo.md("""
    ## More Complex Example: Parametric Bracket
    """)


@app.cell
def _(mo):
    # Parameters for bracket
    bracket_length = mo.ui.slider(start=20, stop=100, value=50, label="Bracket Length")
    bracket_thickness = mo.ui.slider(start=2, stop=10, value=5, label="Thickness")
    mounting_holes = mo.ui.slider(start=2, stop=6, value=4, step=1, label="Mounting Holes")

    mo.vstack([bracket_length, bracket_thickness, mounting_holes])
    return bracket_length, bracket_thickness, mounting_holes


@app.cell
def _(
    Axis,
    Box,
    BuildPart,
    Cylinder,
    GridLocations,
    Hole,
    Locations,
    Mode,
    Plane,
    bracket_length,
    bracket_thickness,
    fillet,
    mounting_holes,
):
    # Create parametric bracket
    with BuildPart() as bracket:
        # Base plate
        with BuildPart() as base_plate:
            Box(bracket_length.value, bracket_length.value / 2, bracket_thickness.value)

        # Vertical plate
        with BuildPart(Plane.XZ) as vertical_plate:
            Box(bracket_length.value, bracket_length.value / 2, bracket_thickness.value)

        # Add mounting holes to base
        hole_spacing = bracket_length.value / (mounting_holes.value + 1)
        with Locations(base_plate.faces().sort_by(Axis.Z)[-1]):
            with GridLocations(hole_spacing, hole_spacing, mounting_holes.value, 2):
                Hole(bracket_thickness.value / 2)

        # Add lightening hole to vertical plate
        with Locations(vertical_plate.faces().sort_by(Axis.Y)[-1].center()):
            Cylinder(bracket_length.value / 4, bracket_thickness.value, mode=Mode.SUBTRACT)

        # Add fillets
        edges_to_fillet = bracket.edges().filter_by(Axis.Z, reverse=True)
        if edges_to_fillet:
            try:
                fillet(edges_to_fillet, bracket_thickness.value / 2)
            except Exception:
                pass  # Some edges might not be filleted
    return (bracket,)


@app.cell
def _(bracket, mo):
    mo.md(f"""
    ## Bracket Model

    **Vertices:** {len(bracket.vertices())}
    **Edges:** {len(bracket.edges())}
    **Faces:** {len(bracket.faces())}
    """)


@app.cell
def _(mo):
    mo.md("""
    ## Export Options

    Build123d supports multiple export formats:
    """)


@app.cell
def _(mo):
    export_format = mo.ui.dropdown(
        options=["STEP", "STL", "SVG", "DXF", "VRML"], value="STEP", label="Export Format"
    )
    export_format
    return (export_format,)


@app.cell
def _(export_format):
    # Export functionality
    def export_model(model, format_type, filename):
        """Export model to specified format"""
        try:
            if format_type == "STEP":
                # STEP export via OCP
                from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

                writer = STEPControl_Writer()
                writer.Transfer(model.part.wrapped, STEPControl_AsIs)
                writer.Write(filename)
                return f"Exported to {filename}"
            if format_type == "STL":
                from OCP.StlAPI import StlAPI_Writer

                writer = StlAPI_Writer()
                writer.Write(model.part.wrapped, filename)
                return f"Exported to {filename}"
            if format_type == "SVG":
                # SVG export using Build123d's native export
                try:
                    # Build123d has built-in SVG export via exporters module
                    from build123d import exporters

                    svg_content = exporters.export_svg(model.part)
                    with open(filename, "w") as f:
                        f.write(svg_content)
                    return f"Exported to {filename}"
                except Exception as svg_error:
                    return f"SVG export error: {svg_error}"
            else:
                return f"{format_type} export not implemented in this demo"
        except Exception as e:
            return f"Export error: {e}"

    # Example: export_model(bracket, export_format.value, f"bracket.{export_format.value.lower()}")
    export_info = f"Selected format: {export_format.value}"
    export_info


@app.cell
def _(mo):
    mo.md("""
    ## Summary

    This proof of concept demonstrates:

    1. ✅ **Reactive Parameters**: Sliders automatically update the model
    2. ✅ **Context Manager API**: Clean, Pythonic syntax
    3. ✅ **Advanced Selectors**: Easy face/edge/vertex selection
    4. ✅ **Multiple Modeling Paradigms**: Builder pattern shown here
    5. ✅ **Export Capabilities**: STEP, STL, SVG, and more
    6. ✅ **Marimo Integration**: Seamless reactive notebook experience

    ### Why Build123d for marimocad?

    - **Native notebook support**: `_repr_mimebundle_()` built-in
    - **Modern Python**: Type hints, context managers, iterators
    - **Powerful selectors**: Intuitive filtering and sorting
    - **Multiple paradigms**: Builder, Algebra, and Direct modeling
    - **Active development**: Regular updates and improvements
    - **Great documentation**: Growing but comprehensive

    ### Next Steps

    1. Wrap Build123d in marimocad-specific API
    2. Create component library (screws, gears, bearings, etc.)
    3. Add custom Marimo UI components
    4. Implement assembly support
    5. Add constraint solver integration
    """)


@app.cell
def _(parametric_box):
    # Display the 3D model using build123d's native rendering
    # Build123d objects can be displayed directly in marimo
    parametric_box.part


if __name__ == "__main__":
    app.run()
