#!/usr/bin/env python3
"""
Verification script to ensure all features work correctly.
"""

import sys

import numpy as np

from marimocad import Viewer3D


def test_basic_creation():
    """Test basic viewer creation"""
    viewer = Viewer3D()
    assert viewer is not None
    assert viewer.width == 800
    assert viewer.height == 600
    print("✓ Basic viewer creation works")

def test_geometry_addition():
    """Test adding all geometry types"""
    viewer = Viewer3D()
    
    viewer.add_box([0, 0, 0], [1, 1, 1], color="blue")
    assert len(viewer.traces) == 1
    
    viewer.add_sphere([1, 1, 1], 0.5, color="red")
    assert len(viewer.traces) == 2
    
    viewer.add_cylinder([2, 2, 2], 0.3, 1.0, color="green")
    assert len(viewer.traces) == 3
    
    # Test custom mesh
    vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    faces = np.array([[0, 1, 2]])
    viewer.add_mesh(vertices, faces, color="purple")
    assert len(viewer.traces) == 4
    
    print("✓ All geometry types can be added")

def test_method_chaining():
    """Test method chaining"""
    viewer = (
        Viewer3D()
        .add_box([0, 0, 0], [1, 1, 1])
        .add_sphere([1, 1, 1], 0.5)
        .set_camera(eye=dict(x=2, y=2, z=2))
        .clear()
    )
    assert len(viewer.traces) == 0
    print("✓ Method chaining works")

def test_camera_control():
    """Test camera settings"""
    viewer = Viewer3D()
    viewer.set_camera(
        eye=dict(x=5, y=5, z=5),
        center=dict(x=0, y=0, z=0)
    )
    assert viewer.camera['eye']['x'] == 5
    print("✓ Camera controls work")

def test_figure_generation():
    """Test Plotly figure generation"""
    viewer = Viewer3D()
    viewer.add_box([0, 0, 0], [1, 1, 1])
    
    fig = viewer.to_figure()
    assert fig is not None
    assert len(fig.data) == 1
    print("✓ Figure generation works")

def test_html_generation():
    """Test HTML output generation"""
    viewer = Viewer3D()
    viewer.add_sphere([0, 0, 0], 1.0)
    
    # This would normally return mo.Html, but we can test the figure
    fig = viewer.to_figure()
    html = fig.to_html(include_plotlyjs='cdn')
    assert html is not None
    assert 'plotly' in html.lower()
    print("✓ HTML generation works")

def main():
    """Run all verification tests"""
    print("Running marimocad verification tests...\n")
    
    try:
        test_basic_creation()
        test_geometry_addition()
        test_method_chaining()
        test_camera_control()
        test_figure_generation()
        test_html_generation()
        
        print("\n" + "="*50)
        print("✓ All verification tests passed!")
        print("="*50)
        print("\nThe marimocad package is ready to use.")
        print("Try the demo: python demo.py")
        print("Or open the example notebook in Marimo:")
        print("  marimo edit examples/basic_example.py")
        return 0
        
    except Exception as e:
        print(f"\n✗ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
