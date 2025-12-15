"""
Example 4: Complex Model

This example demonstrates how to build a complete CAD model
by combining shapes, boolean operations, and transformations.
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    mo.md("# Building Complex CAD Models")
    return mo,


@app.cell
def __():
    import marimocad as mc
    import math
    return math, mc


@app.cell
def __(mo):
    mo.md("""
    ## Project: Mechanical Bracket
    
    Let's build a mechanical bracket with mounting holes and slots.
    This demonstrates a real-world CAD modeling workflow.
    """)
    return


@app.cell
def __(mo):
    mo.md("### Step 1: Create the Base Plate")
    return


@app.cell
def __(mc, mo):
    # Base plate dimensions
    plate_width = 50
    plate_height = 40
    plate_thickness = 5
    
    base_plate = mc.Box(
        width=plate_width,
        height=plate_height,
        depth=plate_thickness,
        name="base_plate"
    )
    
    mo.md(f"""
    ```python
    base_plate = mc.Box(width=50, height=40, depth=5, name="base_plate")
    ```
    
    **Volume:** {base_plate.volume():.2f} cubic units
    
    This forms the foundation of our bracket.
    """)
    return base_plate, plate_height, plate_thickness, plate_width


@app.cell
def __(mo):
    mo.md("### Step 2: Add Corner Fillets")
    return


@app.cell
def __(base_plate, mc, mo):
    # Add rounded corners by intersecting with a larger rounded shape
    fillet_radius = 3
    
    # Create a slightly larger box for the intersection
    outer_box = mc.Box(
        width=base_plate.width + 0.1,
        height=base_plate.height + 0.1,
        depth=base_plate.depth + 0.1
    )
    
    # Create a sphere at each corner for fillets (simplified approach)
    # In a real implementation, this would be more sophisticated
    
    mo.md(f"""
    ```python
    # Rounded corners with fillet radius {fillet_radius}
    # (Simplified for demonstration)
    ```
    
    Corner fillets make the part more durable and aesthetically pleasing.
    """)
    return fillet_radius, outer_box


@app.cell
def __(mo):
    mo.md("### Step 3: Add Mounting Holes")
    return


@app.cell
def __(base_plate, mc, mo, plate_height, plate_width):
    # Create mounting holes at the corners
    hole_radius = 2.5
    hole_spacing_x = plate_width * 0.8
    hole_spacing_y = plate_height * 0.8
    
    holes = []
    
    # Four corner holes
    for x_sign in [-1, 1]:
        for y_sign in [-1, 1]:
            hole = mc.Cylinder(
                radius=hole_radius,
                height=base_plate.depth * 2,  # Through-hole
                name=f"hole_{x_sign}_{y_sign}"
            )
            mc.translate(
                hole,
                x=x_sign * hole_spacing_x / 2,
                y=y_sign * hole_spacing_y / 2,
                z=0
            )
            holes.append(hole)
    
    # Subtract holes from base plate
    bracket_with_holes = mc.difference(base_plate, *holes, name="plate_with_holes")
    
    mo.md(f"""
    ```python
    # Create 4 mounting holes
    hole_radius = 2.5
    hole_spacing_x = {hole_spacing_x:.1f}
    hole_spacing_y = {hole_spacing_y:.1f}
    
    # Subtract all holes from base plate
    bracket_with_holes = mc.difference(base_plate, *holes)
    ```
    
    **Number of holes:** {len(holes)}
    
    **Hole diameter:** {hole_radius * 2:.1f} units
    """)
    return (
        bracket_with_holes,
        hole,
        hole_radius,
        hole_spacing_x,
        hole_spacing_y,
        holes,
        x_sign,
        y_sign,
    )


@app.cell
def __(mo):
    mo.md("### Step 4: Add Vertical Support")
    return


@app.cell
def __(bracket_with_holes, mc, mo, plate_height, plate_thickness):
    # Add a vertical support wall
    support_height = 30
    support_thickness = 4
    
    support_wall = mc.Box(
        width=support_thickness,
        height=plate_height,
        depth=support_height,
        name="support_wall"
    )
    
    # Position at the edge of the base plate
    mc.translate(
        support_wall,
        x=0,
        y=0,
        z=(plate_thickness + support_height) / 2
    )
    
    # Union with the base
    bracket_with_support = mc.union(
        bracket_with_holes,
        support_wall,
        name="bracket_with_support"
    )
    
    mo.md(f"""
    ```python
    support_wall = mc.Box(
        width=4,
        height={plate_height},
        depth={support_height},
        name="support_wall"
    )
    
    # Position and attach to base
    mc.translate(support_wall, z={(plate_thickness + support_height) / 2:.1f})
    bracket_with_support = mc.union(bracket_with_holes, support_wall)
    ```
    
    The vertical wall provides structural support.
    """)
    return (
        bracket_with_support,
        support_height,
        support_thickness,
        support_wall,
    )


@app.cell
def __(mo):
    mo.md("### Step 5: Add a Slot in the Support")
    return


@app.cell
def __(bracket_with_support, mc, mo, plate_thickness, support_height):
    # Add an elongated slot for cable routing or adjustment
    slot_width = 8
    slot_height = 20
    slot_thickness = 10
    
    slot = mc.Box(
        width=slot_thickness,
        height=slot_width,
        depth=slot_height,
        name="cable_slot"
    )
    
    # Position in the center of the support wall
    mc.translate(
        slot,
        x=0,
        y=0,
        z=plate_thickness + support_height / 2
    )
    
    # Subtract the slot
    final_bracket = mc.difference(
        bracket_with_support,
        slot,
        name="final_bracket"
    )
    
    mo.md(f"""
    ```python
    slot = mc.Box(width=8, height=20, depth=10, name="cable_slot")
    mc.translate(slot, z={plate_thickness + support_height / 2:.1f})
    final_bracket = mc.difference(bracket_with_support, slot)
    ```
    
    **Result:** {final_bracket}
    
    The slot provides a channel for cables or allows for adjustable mounting.
    """)
    return final_bracket, slot, slot_height, slot_thickness, slot_width


@app.cell
def __(mo):
    mo.md("""
    ## Project: Parametric Gear
    
    Now let's create a simple gear using parametric design principles.
    """)
    return


@app.cell
def __(mo):
    mo.md("### Gear Parameters")
    return


@app.cell
def __(mo):
    # Gear parameters
    num_teeth = 12
    tooth_height = 3
    gear_radius = 15
    gear_thickness = 5
    shaft_radius = 3
    
    mo.md(f"""
    ```python
    num_teeth = {num_teeth}
    tooth_height = {tooth_height}
    gear_radius = {gear_radius}
    gear_thickness = {gear_thickness}
    shaft_radius = {shaft_radius}
    ```
    
    These parameters define our gear geometry.
    """)
    return (
        gear_radius,
        gear_thickness,
        num_teeth,
        shaft_radius,
        tooth_height,
    )


@app.cell
def __(gear_radius, gear_thickness, mc, mo):
    # Create the main gear body
    gear_body = mc.Cylinder(
        radius=gear_radius,
        height=gear_thickness,
        name="gear_body"
    )
    
    mo.md(f"""
    ```python
    gear_body = mc.Cylinder(radius={gear_radius}, height={gear_thickness})
    ```
    
    **Volume:** {gear_body.volume():.2f} cubic units
    """)
    return gear_body,


@app.cell
def __(gear_radius, gear_thickness, math, mc, mo, num_teeth, tooth_height):
    # Add teeth around the perimeter
    teeth = []
    
    for i in range(num_teeth):
        angle = (360 / num_teeth) * i
        
        # Create a tooth (simplified as a small box)
        tooth = mc.Box(
            width=2,
            height=tooth_height,
            depth=gear_thickness,
            name=f"tooth_{i}"
        )
        
        # Position at the gear perimeter
        x = (gear_radius + tooth_height / 2) * math.cos(math.radians(angle))
        y = (gear_radius + tooth_height / 2) * math.sin(math.radians(angle))
        
        mc.translate(tooth, x=x, y=y, z=0)
        mc.rotate(tooth, angle=angle, axis='z')
        
        teeth.append(tooth)
    
    mo.md(f"""
    ```python
    # Create {num_teeth} teeth around the perimeter
    for i in range(num_teeth):
        angle = (360 / num_teeth) * i
        tooth = mc.Box(width=2, height={tooth_height}, depth={gear_thickness})
        # Position and rotate each tooth
        ...
    ```
    
    **Number of teeth:** {len(teeth)}
    """)
    return angle, i, teeth, tooth, x, y


@app.cell
def __(gear_body, mc, mo, teeth):
    # Union all teeth with the body
    gear_with_teeth = mc.union(gear_body, *teeth, name="gear_with_teeth")
    
    mo.md(f"""
    ```python
    gear_with_teeth = mc.union(gear_body, *teeth)
    ```
    
    **Result:** {gear_with_teeth}
    """)
    return gear_with_teeth,


@app.cell
def __(gear_thickness, gear_with_teeth, mc, mo, shaft_radius):
    # Add central shaft hole
    shaft_hole = mc.Cylinder(
        radius=shaft_radius,
        height=gear_thickness * 2,
        name="shaft_hole"
    )
    
    # Create final gear
    final_gear = mc.difference(gear_with_teeth, shaft_hole, name="final_gear")
    
    mo.md(f"""
    ```python
    shaft_hole = mc.Cylinder(radius={shaft_radius}, height={gear_thickness * 2})
    final_gear = mc.difference(gear_with_teeth, shaft_hole)
    ```
    
    **Final gear:** {final_gear}
    
    The central hole allows the gear to be mounted on a shaft.
    """)
    return final_gear, shaft_hole


@app.cell
def __(mo):
    mo.md("""
    ## Summary
    
    This example demonstrated:
    
    1. **Building a mechanical bracket** with:
       - Base plate structure
       - Mounting holes
       - Vertical support wall
       - Cable routing slot
    
    2. **Creating a parametric gear** with:
       - Circular body
       - Evenly-spaced teeth
       - Central shaft hole
    
    These techniques can be combined and adapted to create
    a wide variety of CAD models.
    """)
    return


@app.cell
def __(mo):
    mo.md("""
    ## Next Steps
    
    - See `05_parametric_design.py` for more on parametric modeling
    - Experiment with different parameters to customize these models
    - Try combining these patterns to create your own designs
    """)
    return


if __name__ == "__main__":
    app.run()
