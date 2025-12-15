"""
Tests for utility functions.
"""

import numpy as np

from marimocad.utils import (
    compute_bounding_box,
    compute_centroid,
    create_box_mesh,
    transform_mesh,
)


class TestUtils:
    """Test suite for utility functions."""
    
    def test_create_box_mesh(self):
        """Test box mesh creation."""
        vertices, faces = create_box_mesh((0, 0, 0), (2, 2, 2))
        
        # Check vertices
        assert vertices.shape == (8, 3)
        assert np.allclose(vertices.min(axis=0), [-1, -1, -1])
        assert np.allclose(vertices.max(axis=0), [1, 1, 1])
        
        # Check faces
        assert faces.shape[0] == 12  # 6 faces * 2 triangles per face
        assert faces.shape[1] == 3   # 3 vertices per triangle
        
        # All face indices should be valid (0-7)
        assert faces.min() >= 0
        assert faces.max() <= 7
    
    def test_create_box_mesh_custom_position(self):
        """Test box mesh creation at custom position."""
        vertices, faces = create_box_mesh((5, 5, 5), (1, 1, 1))
        
        # Check center is at (5, 5, 5)
        centroid = vertices.mean(axis=0)
        assert np.allclose(centroid, [5, 5, 5])
        
        # Check size is 1x1x1
        extents = vertices.max(axis=0) - vertices.min(axis=0)
        assert np.allclose(extents, [1, 1, 1])
    
    def test_transform_mesh_translation(self):
        """Test mesh translation."""
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        
        translated = transform_mesh(vertices, translation=(1, 2, 3))
        
        expected = vertices + np.array([1, 2, 3])
        assert np.allclose(translated, expected)
    
    def test_transform_mesh_scale(self):
        """Test mesh scaling."""
        vertices = np.array([
            [1, 1, 1],
            [2, 2, 2],
        ])
        
        scaled = transform_mesh(vertices, scale=(2, 3, 4))
        
        expected = np.array([
            [2, 3, 4],
            [4, 6, 8]
        ])
        assert np.allclose(scaled, expected)
    
    def test_transform_mesh_rotation_x(self):
        """Test mesh rotation around X axis."""
        vertices = np.array([[0, 1, 0]])
        
        # Rotate 90 degrees around X axis
        rotated = transform_mesh(vertices, rotation=(np.pi/2, 0, 0))
        
        # Y becomes Z
        expected = np.array([[0, 0, 1]])
        assert np.allclose(rotated, expected, atol=1e-10)
    
    def test_transform_mesh_rotation_y(self):
        """Test mesh rotation around Y axis."""
        vertices = np.array([[1, 0, 0]])
        
        # Rotate 90 degrees around Y axis
        rotated = transform_mesh(vertices, rotation=(0, np.pi/2, 0))
        
        # X becomes -Z
        expected = np.array([[0, 0, -1]])
        assert np.allclose(rotated, expected, atol=1e-10)
    
    def test_transform_mesh_rotation_z(self):
        """Test mesh rotation around Z axis."""
        vertices = np.array([[1, 0, 0]])
        
        # Rotate 90 degrees around Z axis
        rotated = transform_mesh(vertices, rotation=(0, 0, np.pi/2))
        
        # X becomes Y
        expected = np.array([[0, 1, 0]])
        assert np.allclose(rotated, expected, atol=1e-10)
    
    def test_transform_mesh_combined(self):
        """Test combined transformations."""
        vertices = np.array([[1, 0, 0]])
        
        # Scale, rotate 90° around Z, then translate
        transformed = transform_mesh(
            vertices,
            translation=(5, 5, 5),
            rotation=(0, 0, np.pi/2),
            scale=(2, 2, 2)
        )
        
        # Scale: [1,0,0] -> [2,0,0]
        # Rotate: [2,0,0] -> [0,2,0]
        # Translate: [0,2,0] -> [5,7,5]
        expected = np.array([[5, 7, 5]])
        assert np.allclose(transformed, expected, atol=1e-10)
    
    def test_compute_bounding_box(self):
        """Test bounding box computation."""
        vertices = np.array([
            [0, 0, 0],
            [1, 2, 3],
            [-1, -2, -3],
            [0.5, 1, 1.5]
        ])
        
        min_point, max_point = compute_bounding_box(vertices)
        
        assert np.allclose(min_point, [-1, -2, -3])
        assert np.allclose(max_point, [1, 2, 3])
    
    def test_compute_centroid(self):
        """Test centroid computation."""
        # Simple square
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0]
        ])
        
        centroid = compute_centroid(vertices)
        
        # Centroid should be at (0.5, 0.5, 0)
        assert np.allclose(centroid, [0.5, 0.5, 0])
    
    def test_compute_centroid_offset(self):
        """Test centroid computation with offset vertices."""
        # Square centered at (5, 5, 5)
        vertices = np.array([
            [4, 4, 4],
            [6, 4, 4],
            [6, 6, 4],
            [4, 6, 4]
        ])
        
        centroid = compute_centroid(vertices)
        
        assert np.allclose(centroid, [5, 5, 4])
