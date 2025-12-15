"""
Utility functions for 3D geometry creation and manipulation.
"""

from typing import Tuple

import numpy as np


def create_box_mesh(
    center: Tuple[float, float, float],
    size: Tuple[float, float, float]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create a box mesh with vertices and faces.
    
    Args:
        center: (x, y, z) coordinates of box center
        size: (width, height, depth) dimensions
        
    Returns:
        Tuple of (vertices, faces) as numpy arrays
    """
    cx, cy, cz = center
    w, h, d = size
    
    vertices = np.array([
        [cx - w/2, cy - h/2, cz - d/2],
        [cx + w/2, cy - h/2, cz - d/2],
        [cx + w/2, cy + h/2, cz - d/2],
        [cx - w/2, cy + h/2, cz - d/2],
        [cx - w/2, cy - h/2, cz + d/2],
        [cx + w/2, cy - h/2, cz + d/2],
        [cx + w/2, cy + h/2, cz + d/2],
        [cx - w/2, cy + h/2, cz + d/2],
    ])
    
    faces = np.array([
        [0, 1, 2], [0, 2, 3],  # bottom
        [4, 6, 5], [4, 7, 6],  # top
        [0, 5, 1], [0, 4, 5],  # front
        [2, 7, 3], [2, 6, 7],  # back
        [0, 7, 4], [0, 3, 7],  # left
        [1, 6, 2], [1, 5, 6],  # right
    ])
    
    return vertices, faces


def transform_mesh(
    vertices: np.ndarray,
    translation: Tuple[float, float, float] = (0, 0, 0),
    rotation: Tuple[float, float, float] = (0, 0, 0),
    scale: Tuple[float, float, float] = (1, 1, 1)
) -> np.ndarray:
    """
    Apply transformations to mesh vertices.
    
    Args:
        vertices: Nx3 array of vertex coordinates
        translation: (x, y, z) translation
        rotation: (rx, ry, rz) rotation angles in radians
        scale: (sx, sy, sz) scale factors
        
    Returns:
        Transformed vertices as numpy array
    """
    # Scale
    vertices = vertices * np.array(scale)
    
    # Rotate around X axis
    if rotation[0] != 0:
        rx = rotation[0]
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(rx), -np.sin(rx)],
            [0, np.sin(rx), np.cos(rx)]
        ])
        vertices = vertices @ Rx.T
    
    # Rotate around Y axis
    if rotation[1] != 0:
        ry = rotation[1]
        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry)],
            [0, 1, 0],
            [-np.sin(ry), 0, np.cos(ry)]
        ])
        vertices = vertices @ Ry.T
    
    # Rotate around Z axis
    if rotation[2] != 0:
        rz = rotation[2]
        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0],
            [np.sin(rz), np.cos(rz), 0],
            [0, 0, 1]
        ])
        vertices = vertices @ Rz.T
    
    # Translate
    vertices = vertices + np.array(translation)
    
    return vertices


def compute_bounding_box(vertices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the bounding box of a mesh.
    
    Args:
        vertices: Nx3 array of vertex coordinates
        
    Returns:
        Tuple of (min_point, max_point) as numpy arrays
    """
    min_point = np.min(vertices, axis=0)
    max_point = np.max(vertices, axis=0)
    return min_point, max_point


def compute_centroid(vertices: np.ndarray) -> np.ndarray:
    """
    Compute the centroid of a mesh.
    
    Args:
        vertices: Nx3 array of vertex coordinates
        
    Returns:
        Centroid as numpy array [x, y, z]
    """
    return np.mean(vertices, axis=0)
