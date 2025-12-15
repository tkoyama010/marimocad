"""
Tests for the Viewer3D class.
"""

import numpy as np

from marimocad import Viewer3D


class TestViewer3D:
    """Test suite for Viewer3D class."""
    
    def test_initialization(self):
        """Test viewer initialization with default and custom parameters."""
        # Default initialization
        viewer = Viewer3D()
        assert viewer.width == 800
        assert viewer.height == 600
        assert viewer.background_color == "white"
        assert len(viewer.traces) == 0
        
        # Custom initialization
        viewer = Viewer3D(width=1000, height=800, background_color="black")
        assert viewer.width == 1000
        assert viewer.height == 800
        assert viewer.background_color == "black"
    
    def test_add_box(self):
        """Test adding a box to the viewer."""
        viewer = Viewer3D()
        result = viewer.add_box([0, 0, 0], [1, 1, 1])
        
        # Check method chaining
        assert result is viewer
        
        # Check trace was added
        assert len(viewer.traces) == 1
        assert viewer.traces[0].type == "mesh3d"
        assert viewer.traces[0].name == "Box 0"
        
        # Add another box with custom name
        viewer.add_box([1, 1, 1], [0.5, 0.5, 0.5], name="Custom Box")
        assert len(viewer.traces) == 2
        assert viewer.traces[1].name == "Custom Box"
    
    def test_add_sphere(self):
        """Test adding a sphere to the viewer."""
        viewer = Viewer3D()
        result = viewer.add_sphere([0, 0, 0], 0.5)
        
        # Check method chaining
        assert result is viewer
        
        # Check trace was added
        assert len(viewer.traces) == 1
        assert viewer.traces[0].type == "mesh3d"
        assert viewer.traces[0].name == "Sphere 0"
        
        # Test with custom parameters
        viewer.add_sphere(
            [1, 1, 1],
            1.0,
            color="red",
            opacity=0.5,
            resolution=10,
            name="Red Sphere"
        )
        assert len(viewer.traces) == 2
        assert viewer.traces[1].name == "Red Sphere"
        assert viewer.traces[1].opacity == 0.5
    
    def test_add_cylinder(self):
        """Test adding a cylinder to the viewer."""
        viewer = Viewer3D()
        result = viewer.add_cylinder([0, 0, 0], 0.5, 1.5)
        
        # Check method chaining
        assert result is viewer
        
        # Check trace was added
        assert len(viewer.traces) == 1
        assert viewer.traces[0].type == "mesh3d"
        assert viewer.traces[0].name == "Cylinder 0"
        
        # Test with custom parameters
        viewer.add_cylinder(
            [1, 1, 1],
            0.3,
            2.0,
            color="green",
            opacity=0.7,
            name="Green Cylinder"
        )
        assert len(viewer.traces) == 2
        assert viewer.traces[1].name == "Green Cylinder"
    
    def test_add_mesh(self):
        """Test adding a custom mesh to the viewer."""
        viewer = Viewer3D()
        
        # Create a simple tetrahedron
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0.5, 1, 0],
            [0.5, 0.5, 1]
        ])
        
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [1, 2, 3],
            [2, 0, 3]
        ])
        
        result = viewer.add_mesh(vertices, faces)
        
        # Check method chaining
        assert result is viewer
        
        # Check trace was added
        assert len(viewer.traces) == 1
        assert viewer.traces[0].type == "mesh3d"
        assert viewer.traces[0].name == "Mesh 0"
        
        # Verify vertex data
        assert len(viewer.traces[0].x) == 4
        assert len(viewer.traces[0].y) == 4
        assert len(viewer.traces[0].z) == 4
    
    def test_set_camera(self):
        """Test setting camera position."""
        viewer = Viewer3D()
        
        # Set camera position
        result = viewer.set_camera(
            eye=dict(x=2, y=2, z=2),
            center=dict(x=0, y=0, z=0),
            up=dict(x=0, y=1, z=0)
        )
        
        # Check method chaining
        assert result is viewer
        
        # Verify camera settings
        assert viewer.camera['eye'] == dict(x=2, y=2, z=2)
        assert viewer.camera['center'] == dict(x=0, y=0, z=0)
        assert viewer.camera['up'] == dict(x=0, y=1, z=0)
    
    def test_clear(self):
        """Test clearing all geometries."""
        viewer = Viewer3D()
        
        # Add some geometries
        viewer.add_box([0, 0, 0], [1, 1, 1])
        viewer.add_sphere([1, 1, 1], 0.5)
        assert len(viewer.traces) == 2
        
        # Clear
        result = viewer.clear()
        
        # Check method chaining
        assert result is viewer
        
        # Verify all traces removed
        assert len(viewer.traces) == 0
    
    def test_method_chaining(self):
        """Test that all methods support chaining."""
        viewer = (
            Viewer3D()
            .add_box([0, 0, 0], [1, 1, 1])
            .add_sphere([1, 1, 1], 0.5)
            .add_cylinder([2, 2, 2], 0.3, 1.0)
            .set_camera(eye=dict(x=3, y=3, z=3))
        )
        
        assert len(viewer.traces) == 3
        assert viewer.camera['eye'] == dict(x=3, y=3, z=3)
    
    def test_to_figure(self):
        """Test getting the Plotly figure."""
        viewer = Viewer3D()
        viewer.add_box([0, 0, 0], [1, 1, 1])
        
        fig = viewer.to_figure()
        
        # Check figure properties
        assert fig.layout.width == 800
        assert fig.layout.height == 600
        assert len(fig.data) == 1
        assert fig.data[0].type == "mesh3d"
    
    def test_multiple_geometries(self):
        """Test adding multiple different geometries."""
        viewer = Viewer3D()
        
        # Add various geometries
        viewer.add_box([0, 0, 0], [1, 1, 1], color="blue")
        viewer.add_sphere([2, 0, 0], 0.5, color="red")
        viewer.add_cylinder([0, 2, 0], 0.5, 1.5, color="green")
        
        vertices = np.array([[0, 0, 2], [1, 0, 2], [0.5, 1, 2]])
        faces = np.array([[0, 1, 2]])
        viewer.add_mesh(vertices, faces, color="purple")
        
        # Verify all were added
        assert len(viewer.traces) == 4
        
        # Verify colors
        assert viewer.traces[0].color == "blue"
        assert viewer.traces[1].color == "red"
        assert viewer.traces[2].color == "green"
        assert viewer.traces[3].color == "purple"
