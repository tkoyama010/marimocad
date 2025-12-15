"""
Example 5: Parametric Design

This example demonstrates parametric CAD modeling techniques
using marimo's reactive features.
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    mo.md("# Parametric Design with marimocad")
    return mo,


@app.cell
def __():
    import marimocad as mc
    import math
    return math, mc


@app.cell
def __(mo):
    mo.md("""
    ## What is Parametric Design?
    
    Parametric design allows you to create models controlled by parameters
    that can be easily adjusted. When you change a parameter, the entire
    model updates automatically.
    
    This is especially powerful in marimo notebooks, where the reactive
    execution model makes the UI update instantly when parameters change.
    """)
    return


@app.cell
def __(mo):
    mo.md("## Example 1: Parametric Box")
    return


@app.cell
def __(mo):
    # Create interactive sliders for box dimensions
    width_slider = mo.ui.slider(1, 20, value=10, label="Width", step=0.5)
    height_slider = mo.ui.slider(1, 20, value=5, label="Height", step=0.5)
    depth_slider = mo.ui.slider(1, 20, value=3, label="Depth", step=0.5)
    
    mo.md(f"""
    ### Adjust the dimensions:
    
    {width_slider}
    
    {height_slider}
    
    {depth_slider}
    """)
    return depth_slider, height_slider, width_slider


@app.cell
def __(depth_slider, height_slider, mc, mo, width_slider):
    # Create a box with the slider values
    param_box = mc.Box(
        width=width_slider.value,
        height=height_slider.value,
        depth=depth_slider.value,
        name="parametric_box"
    )
    
    mo.md(f"""
    ### Current Box:
    
    **Dimensions:** {param_box.width} × {param_box.height} × {param_box.depth}
    
    **Volume:** {param_box.volume():.2f} cubic units
    
    **Surface Area:** {param_box.surface_area():.2f} square units
    
    Try adjusting the sliders above to see the values update!
    """)
    return param_box,


@app.cell
def __(mo):
    mo.md("## Example 2: Parametric Cylinder with Hole")
    return


@app.cell
def __(mo):
    # Parameters for a cylinder with a coaxial hole
    outer_radius_slider = mo.ui.slider(2, 10, value=5, label="Outer Radius", step=0.5)
    inner_radius_slider = mo.ui.slider(0, 8, value=2, label="Inner Radius", step=0.5)
    cylinder_height_slider = mo.ui.slider(2, 20, value=10, label="Height", step=0.5)
    
    mo.md(f"""
    ### Design a Hollow Cylinder:
    
    {outer_radius_slider}
    
    {inner_radius_slider}
    
    {cylinder_height_slider}
    """)
    return (
        cylinder_height_slider,
        inner_radius_slider,
        outer_radius_slider,
    )


@app.cell
def __(
    cylinder_height_slider,
    inner_radius_slider,
    mc,
    mo,
    outer_radius_slider,
):
    # Create the hollow cylinder
    outer_cylinder = mc.Cylinder(
        radius=outer_radius_slider.value,
        height=cylinder_height_slider.value
    )
    
    inner_cylinder = mc.Cylinder(
        radius=inner_radius_slider.value,
        height=cylinder_height_slider.value * 1.1  # Slightly taller to ensure clean cut
    )
    
    hollow_cylinder = mc.difference(outer_cylinder, inner_cylinder, name="hollow_cylinder")
    
    # Calculate wall thickness and volume
    wall_thickness = outer_radius_slider.value - inner_radius_slider.value
    outer_volume = outer_cylinder.volume()
    inner_volume = inner_cylinder.volume()
    material_volume = outer_volume - inner_volume
    
    mo.md(f"""
    ### Result:
    
    **Outer Radius:** {outer_radius_slider.value}
    
    **Inner Radius:** {inner_radius_slider.value}
    
    **Wall Thickness:** {wall_thickness:.2f}
    
    **Height:** {cylinder_height_slider.value}
    
    **Material Volume:** {material_volume:.2f} cubic units
    
    **Weight Savings:** {(inner_volume / outer_volume * 100):.1f}% compared to solid cylinder
    """)
    return (
        hollow_cylinder,
        inner_cylinder,
        inner_volume,
        material_volume,
        outer_cylinder,
        outer_volume,
        wall_thickness,
    )


@app.cell
def __(mo):
    mo.md("## Example 3: Parametric Bolt")
    return


@app.cell
def __(mo):
    # Bolt parameters
    head_diameter_slider = mo.ui.slider(5, 15, value=10, label="Head Diameter", step=0.5)
    head_height_slider = mo.ui.slider(2, 8, value=4, label="Head Height", step=0.5)
    shaft_diameter_slider = mo.ui.slider(2, 10, value=5, label="Shaft Diameter", step=0.5)
    shaft_length_slider = mo.ui.slider(10, 50, value=30, label="Shaft Length", step=1)
    
    mo.md(f"""
    ### Design a Bolt:
    
    {head_diameter_slider}
    
    {head_height_slider}
    
    {shaft_diameter_slider}
    
    {shaft_length_slider}
    """)
    return (
        head_diameter_slider,
        head_height_slider,
        shaft_diameter_slider,
        shaft_length_slider,
    )


@app.cell
def __(
    head_diameter_slider,
    head_height_slider,
    mc,
    mo,
    shaft_diameter_slider,
    shaft_length_slider,
):
    # Create bolt head
    bolt_head = mc.Cylinder(
        radius=head_diameter_slider.value / 2,
        height=head_height_slider.value,
        name="bolt_head"
    )
    
    # Position at top
    mc.translate(bolt_head, z=head_height_slider.value / 2)
    
    # Create bolt shaft
    bolt_shaft = mc.Cylinder(
        radius=shaft_diameter_slider.value / 2,
        height=shaft_length_slider.value,
        name="bolt_shaft"
    )
    
    # Position below head
    mc.translate(
        bolt_shaft,
        z=-(shaft_length_slider.value / 2)
    )
    
    # Combine
    bolt = mc.union(bolt_head, bolt_shaft, name="bolt")
    
    # Calculate total volume and weight (assuming steel: 7.85 g/cm³)
    total_volume = bolt_head.volume() + bolt_shaft.volume()
    steel_density = 7.85  # g/cm³
    weight = total_volume * steel_density
    
    mo.md(f"""
    ### Bolt Specifications:
    
    **Head:**
    - Diameter: {head_diameter_slider.value}
    - Height: {head_height_slider.value}
    
    **Shaft:**
    - Diameter: {shaft_diameter_slider.value}
    - Length: {shaft_length_slider.value}
    
    **Total Length:** {head_height_slider.value + shaft_length_slider.value}
    
    **Volume:** {total_volume:.2f} cubic units
    
    **Weight (steel):** {weight:.2f} grams
    """)
    return bolt, bolt_head, bolt_shaft, steel_density, total_volume, weight


@app.cell
def __(mo):
    mo.md("## Example 4: Parametric Gear Generator")
    return


@app.cell
def __(mo):
    # Gear parameters
    num_teeth_slider = mo.ui.slider(6, 24, value=12, label="Number of Teeth", step=1)
    gear_radius_slider = mo.ui.slider(10, 30, value=15, label="Gear Radius", step=1)
    tooth_size_slider = mo.ui.slider(1, 5, value=3, label="Tooth Size", step=0.5)
    gear_thickness_slider = mo.ui.slider(2, 10, value=5, label="Thickness", step=0.5)
    
    mo.md(f"""
    ### Design a Gear:
    
    {num_teeth_slider}
    
    {gear_radius_slider}
    
    {tooth_size_slider}
    
    {gear_thickness_slider}
    """)
    return (
        gear_radius_slider,
        gear_thickness_slider,
        num_teeth_slider,
        tooth_size_slider,
    )


@app.cell
def __(
    gear_radius_slider,
    gear_thickness_slider,
    math,
    mc,
    mo,
    num_teeth_slider,
    tooth_size_slider,
):
    # Create gear body
    gear_main = mc.Cylinder(
        radius=gear_radius_slider.value,
        height=gear_thickness_slider.value,
        name="gear_body"
    )
    
    # Create teeth
    gear_teeth = []
    
    for i in range(num_teeth_slider.value):
        angle = (360 / num_teeth_slider.value) * i
        
        tooth = mc.Box(
            width=2,
            height=tooth_size_slider.value,
            depth=gear_thickness_slider.value,
            name=f"tooth_{i}"
        )
        
        # Position at perimeter
        x = (gear_radius_slider.value + tooth_size_slider.value / 2) * math.cos(math.radians(angle))
        y = (gear_radius_slider.value + tooth_size_slider.value / 2) * math.sin(math.radians(angle))
        
        mc.translate(tooth, x=x, y=y, z=0)
        mc.rotate(tooth, angle=angle, axis='z')
        
        gear_teeth.append(tooth)
    
    # Combine
    complete_gear = mc.union(gear_main, *gear_teeth, name="parametric_gear")
    
    # Calculate metrics
    pitch_diameter = gear_radius_slider.value * 2
    circular_pitch = (math.pi * pitch_diameter) / num_teeth_slider.value
    
    mo.md(f"""
    ### Gear Specifications:
    
    **Basic:**
    - Number of Teeth: {num_teeth_slider.value}
    - Pitch Diameter: {pitch_diameter:.2f}
    - Tooth Size: {tooth_size_slider.value}
    
    **Calculated:**
    - Circular Pitch: {circular_pitch:.2f}
    - Thickness: {gear_thickness_slider.value}
    
    **Volume:** {gear_main.volume():.2f} cubic units (body only)
    
    This gear can mesh with another gear of the same circular pitch.
    """)
    return (
        angle,
        circular_pitch,
        complete_gear,
        gear_main,
        gear_teeth,
        i,
        pitch_diameter,
        tooth,
        x,
        y,
    )


@app.cell
def __(mo):
    mo.md("""
    ## Best Practices for Parametric Design
    
    1. **Use meaningful variable names** - Make your code self-documenting
    2. **Set reasonable bounds** - Use slider min/max to prevent invalid values
    3. **Add validation** - Check that parameters make sense together
    4. **Calculate derived values** - Show users useful metrics
    5. **Provide visual feedback** - Display the current state clearly
    6. **Use reactive updates** - Let marimo handle the UI updates
    
    ## Benefits of Parametric Modeling
    
    - **Rapid iteration**: Quickly explore design variations
    - **Design optimization**: Find optimal parameters
    - **Reusability**: Create templates for similar parts
    - **Documentation**: Parameters serve as specifications
    - **Collaboration**: Easy for others to customize
    """)
    return


@app.cell
def __(mo):
    mo.md("""
    ## Try It Yourself
    
    Experiment with the sliders above to:
    - Create different box sizes
    - Design hollow cylinders with various wall thicknesses
    - Generate bolts of different sizes
    - Create gears with different numbers of teeth
    
    The reactive nature of marimo means everything updates instantly!
    """)
    return


if __name__ == "__main__":
    app.run()
