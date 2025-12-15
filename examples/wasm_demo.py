"""WebAssembly-Compatible Demo of marimocad with Build123d

This example is optimized for running in the browser via Pyodide/WASM.
It demonstrates basic parametric CAD modeling using Build123d with:
- Simple geometric shapes
- Interactive reactive controls
- Minimal dependencies for faster loading
- Browser-compatible visualization

Note: This example is designed to be lightweight and load quickly in WASM environments.
More complex features are available in the desktop examples.
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
    # 🌐 marimocad WASM Demo

    **Interactive CAD modeling in your browser!**

    This demo runs entirely in your browser using WebAssembly (WASM) and Pyodide.
    No installation required - just adjust the parameters below to see live updates.

    > 💡 **Tip:** This is a simplified demo optimized for browser performance.
    > For more advanced features, try the desktop examples.
    """)
    return


@app.cell
def __(mo):
    mo.md("""
    ## 📦 Parametric Box

    Create a customizable 3D box by adjusting the dimensions below:
    """)
    return


@app.cell
def __(mo):
    # Interactive parameters for box
    box_length = mo.ui.slider(
        start=5, stop=30, value=15, label="Length (mm)", show_value=True
    )
    box_width = mo.ui.slider(
        start=5, stop=30, value=10, label="Width (mm)", show_value=True
    )
    box_height = mo.ui.slider(
        start=3, stop=20, value=8, label="Height (mm)", show_value=True
    )

    mo.vstack([box_length, box_width, box_height])
    return box_height, box_length, box_width


@app.cell
def __(box_height, box_length, box_width, mo):
    mo.md(f"""
    ### Current Box Dimensions

    - **Length:** {box_length.value} mm
    - **Width:** {box_width.value} mm
    - **Height:** {box_height.value} mm
    - **Volume:** {box_length.value * box_width.value * box_height.value:.1f} mm³
    """)
    return


@app.cell
def __(mo):
    mo.md("""
    ## 🔘 Parametric Cylinder

    Create a customizable cylinder:
    """)
    return


@app.cell
def __(mo):
    # Interactive parameters for cylinder
    cylinder_radius = mo.ui.slider(
        start=3, stop=15, value=6, label="Radius (mm)", show_value=True
    )
    cylinder_height = mo.ui.slider(
        start=5, stop=30, value=12, label="Height (mm)", show_value=True
    )

    mo.vstack([cylinder_radius, cylinder_height])
    return cylinder_height, cylinder_radius


@app.cell
def __(cylinder_height, cylinder_radius, mo):
    import math

    volume = math.pi * cylinder_radius.value**2 * cylinder_height.value

    mo.md(f"""
    ### Current Cylinder Dimensions

    - **Radius:** {cylinder_radius.value} mm
    - **Height:** {cylinder_height.value} mm
    - **Volume:** {volume:.1f} mm³
    """)
    return math, volume


@app.cell
def __(mo):
    mo.md("""
    ## 🎯 Build123d Integration

    This demo uses **Build123d**, a modern Python CAD library that works seamlessly
    with marimo's reactive programming model.
    """)
    return


@app.cell
def __(mo):
    # Check if Build123d is available
    try:
        # Try importing build123d core components
        from build123d import Axis, Box, BuildPart, Cylinder, Location

        build123d_available = True
        build123d_message = "✅ Build123d is available!"
    except ImportError:
        build123d_available = False
        build123d_message = """
        ⚠️ Build123d is not available in this environment.

        To use Build123d in WASM, you need OCP.wasm support.
        For now, this demo shows the reactive interface without 3D rendering.

        **For full functionality:**
        - Use desktop version: `marimo edit examples/build123d_poc.py`
        - Or wait for OCP.wasm integration in Pyodide
        """

    mo.md(build123d_message)
    return (
        Axis,
        Box,
        BuildPart,
        Cylinder,
        Location,
        build123d_available,
        build123d_message,
    )


@app.cell
def __(
    Box,
    BuildPart,
    Cylinder,
    box_height,
    box_length,
    box_width,
    build123d_available,
    cylinder_height,
    cylinder_radius,
    mo,
):
    if build123d_available:
        try:
            # Create parametric box
            with BuildPart() as demo_box:
                Box(box_length.value, box_width.value, box_height.value)

            # Create parametric cylinder
            with BuildPart() as demo_cylinder:
                Cylinder(cylinder_radius.value, cylinder_height.value)

            geometry_status = f"""
            ### 🎨 Geometry Created Successfully

            **Box:**
            - Vertices: {len(demo_box.vertices())}
            - Edges: {len(demo_box.edges())}
            - Faces: {len(demo_box.faces())}

            **Cylinder:**
            - Vertices: {len(demo_cylinder.vertices())}
            - Edges: {len(demo_cylinder.edges())}
            - Faces: {len(demo_cylinder.faces())}

            > 💡 In a full environment, these models would be rendered in 3D
            """
        except (AttributeError, RuntimeError, ValueError) as e:
            geometry_status = f"⚠️ Error creating geometry: {e}"
            demo_box = None
            demo_cylinder = None
    else:
        geometry_status = "⏳ Waiting for Build123d..."
        demo_box = None
        demo_cylinder = None

    mo.md(geometry_status)
    return demo_box, demo_cylinder, geometry_status


@app.cell
def __(mo):
    mo.md("""
    ## 📊 About This Demo

    ### What works in WASM?
    - ✅ Reactive UI controls (sliders, inputs)
    - ✅ Real-time parameter updates
    - ✅ Mathematical calculations
    - ✅ Data visualization
    - ✅ Export calculations

    ### What requires desktop?
    - 🖥️ Full 3D rendering
    - 🖥️ Complex CAD operations
    - 🖥️ Large assemblies
    - 🖥️ File export (STEP, STL, etc.)

    ### Performance Tips
    - Keep models simple for browser execution
    - Use simpler geometry for faster updates
    - Desktop version is recommended for production work
    """)
    return


@app.cell
def __(mo):
    mo.md("""
    ## 🚀 Next Steps

    ### Try the full version:
    ```bash
    pip install build123d marimo
    marimo edit examples/build123d_poc.py
    ```

    ### Resources:
    - [marimocad GitHub](https://github.com/tkoyama010/marimocad)
    - [Build123d Documentation](https://build123d.readthedocs.io/)
    - [marimo Documentation](https://docs.marimo.io/)
    - [OCP.wasm Project](https://github.com/yeicor/OCP.wasm)

    ---

    **Made with ❤️ using marimo + Build123d**
    """)
    return


if __name__ == "__main__":
    app.run()
