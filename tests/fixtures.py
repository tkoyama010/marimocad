"""Test fixtures for CAD file import/export."""

import os
import struct
from pathlib import Path


def create_test_files(test_dir: Path) -> None:
    """Create test files for all supported formats."""
    
    # Create a simple cube mesh for testing
    # Vertices of a unit cube
    vertices = [
        (0.0, 0.0, 0.0),  # 0
        (1.0, 0.0, 0.0),  # 1
        (1.0, 1.0, 0.0),  # 2
        (0.0, 1.0, 0.0),  # 3
        (0.0, 0.0, 1.0),  # 4
        (1.0, 0.0, 1.0),  # 5
        (1.0, 1.0, 1.0),  # 6
        (0.0, 1.0, 1.0),  # 7
    ]
    
    # Faces (triangulated)
    faces = [
        # Bottom face
        (0, 1, 2), (0, 2, 3),
        # Top face
        (4, 6, 5), (4, 7, 6),
        # Front face
        (0, 4, 5), (0, 5, 1),
        # Back face
        (2, 6, 7), (2, 7, 3),
        # Left face
        (0, 3, 7), (0, 7, 4),
        # Right face
        (1, 5, 6), (1, 6, 2),
    ]
    
    # Create STEP file
    create_step_file(test_dir / "cube.step")
    
    # Create binary STL file
    create_binary_stl_file(test_dir / "cube_binary.stl", vertices, faces)
    
    # Create ASCII STL file
    create_ascii_stl_file(test_dir / "cube_ascii.stl", vertices, faces)
    
    # Create OBJ file
    create_obj_file(test_dir / "cube.obj", vertices, faces)
    
    # Create invalid files
    create_invalid_files(test_dir)


def create_step_file(filepath: Path) -> None:
    """Create a minimal valid STEP file."""
    content = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Test STEP file'), '2;1');
FILE_NAME('cube.step', '2025-01-01T00:00:00', (''), (''), '', '', '');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1 = CARTESIAN_POINT('', (0., 0., 0.));
#2 = CARTESIAN_POINT('', (1., 0., 0.));
#3 = CARTESIAN_POINT('', (1., 1., 0.));
#4 = CARTESIAN_POINT('', (0., 1., 0.));
ENDSEC;
END-ISO-10303-21;
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def create_binary_stl_file(filepath: Path, vertices: list, faces: list) -> None:
    """Create a binary STL file."""
    with open(filepath, 'wb') as f:
        # Write header (80 bytes)
        header = b'Binary STL test file'
        header = header + b' ' * (80 - len(header))
        f.write(header)
        
        # Write number of triangles
        f.write(struct.pack('<I', len(faces)))
        
        # Write triangles
        for face in faces:
            v0, v1, v2 = [vertices[i] for i in face]
            
            # Calculate normal
            u = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
            v = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
            normal = (
                u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0]
            )
            length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
            if length > 0:
                normal = (normal[0]/length, normal[1]/length, normal[2]/length)
            
            # Write normal
            f.write(struct.pack('<fff', *normal))
            
            # Write vertices
            f.write(struct.pack('<fff', *v0))
            f.write(struct.pack('<fff', *v1))
            f.write(struct.pack('<fff', *v2))
            
            # Write attribute byte count
            f.write(struct.pack('<H', 0))


def create_ascii_stl_file(filepath: Path, vertices: list, faces: list) -> None:
    """Create an ASCII STL file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("solid cube\n")
        
        for face in faces:
            v0, v1, v2 = [vertices[i] for i in face]
            
            # Calculate normal
            u = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
            v = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
            normal = (
                u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0]
            )
            length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
            if length > 0:
                normal = (normal[0]/length, normal[1]/length, normal[2]/length)
            
            f.write(f"  facet normal {normal[0]} {normal[1]} {normal[2]}\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {v0[0]} {v0[1]} {v0[2]}\n")
            f.write(f"      vertex {v1[0]} {v1[1]} {v1[2]}\n")
            f.write(f"      vertex {v2[0]} {v2[1]} {v2[2]}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        
        f.write("endsolid cube\n")


def create_obj_file(filepath: Path, vertices: list, faces: list) -> None:
    """Create an OBJ file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# Test OBJ file\n")
        f.write("# Cube mesh\n\n")
        
        # Write vertices
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        
        f.write("\n")
        
        # Write faces (OBJ uses 1-based indexing)
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")


def create_invalid_files(test_dir: Path) -> None:
    """Create invalid test files."""
    # Empty file
    with open(test_dir / "empty.stl", 'w') as f:
        pass
    
    # Invalid STEP file
    with open(test_dir / "invalid.step", 'w') as f:
        f.write("This is not a valid STEP file\n")
    
    # Corrupted binary STL
    with open(test_dir / "corrupted.stl", 'wb') as f:
        f.write(b'Some random binary data')
    
    # Invalid OBJ file
    with open(test_dir / "invalid.obj", 'w') as f:
        f.write("This is not a valid OBJ file\n")
