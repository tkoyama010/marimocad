#!/usr/bin/env python3
"""
Simple demo script to test the 3D visualization functionality.
This generates a standalone HTML file that can be viewed in a browser.
"""

from marimocad import Viewer3D

# Create a viewer
viewer = Viewer3D(width=800, height=600)

# Add multiple geometries
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

viewer.add_sphere(
    center=[-1.5, -1.5, 0],
    radius=0.3,
    color="yellow",
    opacity=0.9,
    name="Yellow Sphere"
)

# Set camera for a good view
viewer.set_camera(
    eye=dict(x=3, y=3, z=3),
    center=dict(x=0.5, y=0.5, z=0),
    up=dict(x=0, y=0, z=1)
)

# Get the figure and save as HTML
fig = viewer.to_figure()
html = fig.to_html(
    include_plotlyjs='cdn',
    config={
        'displayModeBar': True,
        'displaylogo': False,
        'scrollZoom': True,
    }
)

# Save to file
output_file = "/tmp/demo_3d_viewer.html"
with open(output_file, 'w') as f:
    f.write(html)

print(f"✓ 3D visualization demo created successfully!")
print(f"✓ Saved to: {output_file}")
print(f"✓ Open this file in a web browser to view the interactive 3D scene")
print(f"\nThe scene contains:")
print(f"  - 1 blue box at origin")
print(f"  - 1 red sphere at (2, 0, 0)")
print(f"  - 1 green cylinder at (0, 2, 0)")
print(f"  - 1 yellow sphere at (-1.5, -1.5, 0)")
print(f"\nInteractive controls:")
print(f"  - Click and drag to rotate")
print(f"  - Right-click and drag to pan")
print(f"  - Scroll to zoom")
print(f"  - Hover over objects to see their names")
