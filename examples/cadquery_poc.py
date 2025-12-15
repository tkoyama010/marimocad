"""CadQuery Proof of Concept for Marimo Integration

This example demonstrates how CadQuery integrates with Marimo for parametric CAD modeling.
CadQuery is recommended as a secondary backend for marimocad due to its:
- Mature and stable API
- Excellent documentation
- Large community
- Fluent, chainable interface
"""

import marimo


__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo

    return (mo,)


@app.cell
def __():
    import cadquery as cq

    return (cq,)


@app.cell
def __(mo):
    mo.md("""
    # CadQuery Parametric CAD Demo

    This demonstrates CadQuery's integration with Marimo for reactive CAD modeling.
    Adjust the sliders to see the model update in real-time.
    """)


@app.cell
def __(mo):
    # Create reactive parameters
    length = mo.ui.slider(start=10, stop=50, value=30, label="Length")
    width = mo.ui.slider(start=10, stop=50, value=20, label="Width")
    height = mo.ui.slider(start=5, stop=30, value=15, label="Height")
    hole_diameter = mo.ui.slider(start=2, stop=15, value=8, label="Hole Diameter")
    fillet_radius = mo.ui.slider(start=0, stop=5, value=2, label="Fillet Radius")

    mo.vstack([length, width, height, hole_diameter, fillet_radius])
    return fillet_radius, height, hole_diameter, length, width


@app.cell
def __(cq, fillet_radius, height, hole_diameter, length, width):
    # Create parametric box with hole using fluent API
    parametric_box = (
        cq.Workplane("XY")
        .box(length.value, width.value, height.value)
        .faces(">Z")
        .workplane()
        .hole(hole_diameter.value)
    )

    # Add fillets if radius > 0
    if fillet_radius.value > 0:
        parametric_box = parametric_box.edges("|Z").fillet(fillet_radius.value)

    parametric_box
    return (parametric_box,)


@app.cell
def __(mo, parametric_box):
    # Display model information
    mo.md(f"""
    ## Generated Model

    **Solids:** {parametric_box.solids().size()}
    **Faces:** {parametric_box.faces().size()}
    **Edges:** {parametric_box.edges().size()}
    **Vertices:** {parametric_box.vertices().size()}

    To visualize this model in Marimo, use jupyter-cadquery or three-cad-viewer:
    ```bash
    pip install jupyter-cadquery
    ```

    Then use:
    ```python
    from jupyter_cadquery import show
    show(parametric_box)
    ```
    """)


@app.cell
def __(mo):
    mo.md("""
    ## More Complex Example: Parametric Bearing Block
    """)


@app.cell
def __(mo):
    # Parameters for bearing block
    block_size = mo.ui.slider(start=20, stop=60, value=40, label="Block Size")
    bearing_diameter = mo.ui.slider(start=10, stop=30, value=20, label="Bearing Diameter")
    mounting_holes = mo.ui.slider(start=2, stop=6, value=4, step=1, label="Mounting Holes")

    mo.vstack([block_size, bearing_diameter, mounting_holes])
    return bearing_diameter, block_size, mounting_holes


@app.cell
def __(bearing_diameter, block_size, cq, mounting_holes):
    # Create parametric bearing block
    bearing_block = (
        cq.Workplane("XY")
        # Main block
        .box(block_size.value, block_size.value, block_size.value / 2)
        # Center hole for bearing
        .faces(">Z")
        .workplane()
        .hole(bearing_diameter.value)
        # Mounting holes at corners
        .faces(">Z")
        .workplane()
        .rect(block_size.value * 0.7, block_size.value * 0.7, forConstruction=True)
        .vertices()
        .circle(block_size.value * 0.1)
        .cutThruAll()
        # Add chamfers to top edges
        .faces(">Z")
        .edges()
        .chamfer(block_size.value * 0.05)
        # Add fillets to bottom edges
        .faces("<Z")
        .edges()
        .fillet(block_size.value * 0.05)
    )
    return (bearing_block,)


@app.cell
def __(bearing_block, mo):
    mo.md(f"""
    ## Bearing Block Model

    **Solids:** {bearing_block.solids().size()}
    **Faces:** {bearing_block.faces().size()}
    **Edges:** {bearing_block.edges().size()}
    **Vertices:** {bearing_block.vertices().size()}
    """)


@app.cell
def __(mo):
    mo.md("""
    ## CadQuery Selector Demo

    One of CadQuery's strengths is its powerful selector system.
    """)


@app.cell
def __(cq):
    # Demonstrate selectors
    demo_box = cq.Workplane("XY").box(30, 20, 10)

    # Select different faces
    top_faces = demo_box.faces(">Z").size()  # Faces pointing up in Z
    bottom_faces = demo_box.faces("<Z").size()  # Faces pointing down in Z
    side_faces = demo_box.faces("|Z").size()  # Faces parallel to Z axis

    # Select edges
    vertical_edges = demo_box.edges("|Z").size()  # Edges parallel to Z
    horizontal_edges = demo_box.edges("#Z").size()  # Edges perpendicular to Z

    selector_info = {
        "Top faces (>Z)": top_faces,
        "Bottom faces (<Z)": bottom_faces,
        "Side faces (|Z)": side_faces,
        "Vertical edges (|Z)": vertical_edges,
        "Horizontal edges (#Z)": horizontal_edges,
    }
    selector_info
    return (
        bottom_faces,
        demo_box,
        horizontal_edges,
        selector_info,
        side_faces,
        top_faces,
        vertical_edges,
    )


@app.cell
def __(mo):
    mo.md("""
    ## Export Options

    CadQuery supports multiple export formats:
    """)


@app.cell
def __(mo):
    export_format = mo.ui.dropdown(
        options=["STEP", "STL", "SVG", "DXF", "AMF"], value="STEP", label="Export Format"
    )
    export_format
    return (export_format,)


@app.cell
def __(bearing_block, export_format):
    # Export functionality
    def export_cadquery_model(model, format_type, filename):
        """Export CadQuery model to specified format"""
        try:
            if format_type == "STEP":
                model.val().exportStep(filename)
                return f"Exported to {filename}"
            if format_type == "STL":
                model.val().exportStl(filename)
                return f"Exported to {filename}"
            if format_type == "SVG":
                svg_data = model.toSvg()
                with open(filename, "w") as f:
                    f.write(svg_data)
                return f"Exported to {filename}"
            if format_type == "DXF":
                # DXF export for 2D projections
                return "DXF export requires ezdxf integration"
            if format_type == "AMF":
                model.val().exportAmf(filename)
                return f"Exported to {filename}"
            return f"{format_type} export not implemented"
        except Exception as e:
            return f"Export error: {e}"

    # Example: export_cadquery_model(bearing_block, export_format.value, f"bearing_block.{export_format.value.lower()}")
    export_info = f"Selected format: {export_format.value}"
    export_info
    return export_cadquery_model, export_info


@app.cell
def __(mo):
    mo.md("""
    ## CadQuery Assembly Demo

    CadQuery has excellent assembly support:
    """)


@app.cell
def __(cq):
    # Simple assembly example
    # Create a bolt
    bolt = cq.Workplane("XY").circle(3).extrude(20).faces(">Z").workplane().circle(5).extrude(2)

    # Create a nut
    nut = (
        cq.Workplane("XY")
        .polygon(6, 10)
        .extrude(5)
        .faces(">Z")
        .workplane()
        .circle(3.2)
        .cutThruAll()
    )

    # Create assembly
    assembly = cq.Assembly()
    assembly.add(bolt, name="bolt", color=cq.Color("gray"))
    assembly.add(nut, name="nut", loc=cq.Location((0, 0, 15)), color=cq.Color("silver"))

    assembly_info = {
        "Components": len(assembly.children),
        "Bolt faces": bolt.faces().size(),
        "Nut faces": nut.faces().size(),
    }
    assembly_info
    return assembly, assembly_info, bolt, nut


@app.cell
def __(mo):
    mo.md("""
    ## Summary

    This proof of concept demonstrates:

    1. ✅ **Fluent API**: Chainable methods for clean code
    2. ✅ **Powerful Selectors**: Intuitive face/edge/vertex selection
    3. ✅ **Workplane Concept**: Flexible 2D sketching on any face
    4. ✅ **Parametric Design**: Easy parameter-driven modeling
    5. ✅ **Assembly Support**: Built-in assembly capabilities
    6. ✅ **Export Capabilities**: STEP, STL, SVG, AMF, and more
    7. ✅ **Marimo Integration**: Works well with reactive notebooks

    ### Why CadQuery for marimocad?

    - **Mature and stable**: Well-tested with large user base
    - **Excellent docs**: Comprehensive tutorials and examples
    - **Strong community**: Active Discord and forum support
    - **Proven track record**: Used in production by many
    - **Fluent API**: Intuitive and readable code
    - **Rich ecosystem**: Many plugins and extensions

    ### Comparison with Build123d

    **CadQuery Strengths:**
    - More mature and stable
    - Better documentation
    - Larger community
    - More examples and tutorials

    **Build123d Strengths:**
    - More modern API (context managers)
    - Better notebook integration
    - More flexible (multiple paradigms)
    - More Pythonic

    ### Next Steps

    1. Consider CadQuery as secondary/alternative backend
    2. Could support both Build123d and CadQuery
    3. Unified API could abstract the differences
    4. Users could choose their preferred backend
    """)


if __name__ == "__main__":
    app.run()
