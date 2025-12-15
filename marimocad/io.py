"""Core file I/O functionality for CAD file formats."""

import os
import struct
from pathlib import Path
from typing import Any, Dict, Optional, Union, Callable
from enum import Enum


class FileFormat(Enum):
    """Supported CAD file formats."""
    STEP = "step"
    STL = "stl"
    OBJ = "obj"
    UNKNOWN = "unknown"


class FileFormatError(Exception):
    """Exception raised for file format errors."""
    pass


class ImportError(Exception):
    """Exception raised for import errors."""
    pass


class ExportError(Exception):
    """Exception raised for export errors."""
    pass


def detect_format(filepath: Union[str, Path]) -> FileFormat:
    """
    Detect the file format based on extension and content.
    
    Args:
        filepath: Path to the file
        
    Returns:
        FileFormat enum value
        
    Raises:
        FileFormatError: If format cannot be detected
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileFormatError(f"File not found: {filepath}")
    
    # Check by extension first
    ext = filepath.suffix.lower()
    if ext in ['.step', '.stp']:
        return FileFormat.STEP
    elif ext == '.stl':
        return FileFormat.STL
    elif ext == '.obj':
        return FileFormat.OBJ
    
    # Try to detect by content for ambiguous cases
    try:
        with open(filepath, 'rb') as f:
            header = f.read(100)
            
        # Check for binary STL (80 byte header + uint32 triangle count)
        if len(header) >= 84:
            # Binary STL typically doesn't start with "solid"
            if header[:5] != b'solid':
                # Try to read triangle count
                try:
                    triangle_count = struct.unpack('<I', header[80:84])[0]
                    # Check if file size matches expected size for binary STL
                    expected_size = 84 + triangle_count * 50
                    actual_size = filepath.stat().st_size
                    if actual_size == expected_size:
                        return FileFormat.STL
                except (struct.error, ValueError, IndexError):
                    pass
        
        # Check for ASCII STL
        if b'solid' in header[:10]:
            return FileFormat.STL
            
        # Check for STEP file
        if b'ISO-10303' in header or b'STEP' in header:
            return FileFormat.STEP
            
        # Check for OBJ file
        if b'v ' in header or b'vn ' in header or b'vt ' in header:
            return FileFormat.OBJ
            
    except Exception as e:
        raise FileFormatError(f"Error detecting format: {e}")
    
    return FileFormat.UNKNOWN


def validate_file(filepath: Union[str, Path], expected_format: Optional[FileFormat] = None) -> bool:
    """
    Validate a CAD file.
    
    Args:
        filepath: Path to the file
        expected_format: Expected format (optional)
        
    Returns:
        True if valid, False otherwise
        
    Raises:
        FileFormatError: If file cannot be validated
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileFormatError(f"File not found: {filepath}")
    
    if filepath.stat().st_size == 0:
        return False
    
    detected_format = detect_format(filepath)
    
    if expected_format and detected_format != expected_format:
        return False
    
    if detected_format == FileFormat.UNKNOWN:
        return False
    
    return True


def import_file(
    filepath: Union[str, Path],
    format: Optional[FileFormat] = None,
    progress_callback: Optional[Callable[[int], None]] = None,
) -> Dict[str, Any]:
    """
    Import a CAD file.
    
    Args:
        filepath: Path to the file
        format: File format (auto-detected if not provided)
        progress_callback: Optional callback for progress updates (0-100)
        
    Returns:
        Dictionary containing the imported data:
        - 'format': FileFormat enum
        - 'vertices': List of vertices for mesh formats
        - 'faces': List of faces for mesh formats
        - 'shape': CAD shape object for STEP files
        - 'metadata': Additional metadata
        
    Raises:
        FileFormatError: If format is not supported
        ImportError: If import fails
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise ImportError(f"File not found: {filepath}")
    
    # Detect format if not provided
    if format is None:
        format = detect_format(filepath)
    
    if format == FileFormat.UNKNOWN:
        raise FileFormatError(f"Unknown file format: {filepath}")
    
    # Call progress callback at start
    if progress_callback:
        progress_callback(0)
    
    try:
        if format == FileFormat.STEP:
            result = _import_step(filepath, progress_callback)
        elif format == FileFormat.STL:
            result = _import_stl(filepath, progress_callback)
        elif format == FileFormat.OBJ:
            result = _import_obj(filepath, progress_callback)
        else:
            raise FileFormatError(f"Unsupported format: {format}")
        
        # Call progress callback at end
        if progress_callback:
            progress_callback(100)
        
        return result
        
    except Exception as e:
        raise ImportError(f"Failed to import {filepath}: {e}")


def export_file(
    filepath: Union[str, Path],
    data: Dict[str, Any],
    format: Optional[FileFormat] = None,
    progress_callback: Optional[Callable[[int], None]] = None,
) -> None:
    """
    Export a CAD file.
    
    Args:
        filepath: Path to save the file
        data: Dictionary containing data to export:
            - 'vertices': List of vertices for mesh formats
            - 'faces': List of faces for mesh formats
            - 'shape': CAD shape object for STEP files
        format: File format (auto-detected from extension if not provided)
        progress_callback: Optional callback for progress updates (0-100)
        
    Raises:
        FileFormatError: If format is not supported
        ExportError: If export fails
    """
    filepath = Path(filepath)
    
    # Detect format from extension if not provided
    if format is None:
        ext = filepath.suffix.lower()
        if ext in ['.step', '.stp']:
            format = FileFormat.STEP
        elif ext == '.stl':
            format = FileFormat.STL
        elif ext == '.obj':
            format = FileFormat.OBJ
        else:
            raise FileFormatError(f"Cannot determine format from extension: {ext}")
    
    # Call progress callback at start
    if progress_callback:
        progress_callback(0)
    
    try:
        if format == FileFormat.STEP:
            _export_step(filepath, data, progress_callback)
        elif format == FileFormat.STL:
            _export_stl(filepath, data, progress_callback)
        elif format == FileFormat.OBJ:
            _export_obj(filepath, data, progress_callback)
        else:
            raise FileFormatError(f"Unsupported format: {format}")
        
        # Call progress callback at end
        if progress_callback:
            progress_callback(100)
        
    except Exception as e:
        raise ExportError(f"Failed to export to {filepath}: {e}")


def _import_step(filepath: Path, progress_callback: Optional[Callable[[int], None]] = None) -> Dict[str, Any]:
    """Import STEP file (basic implementation without pythonocc)."""
    # Read file content
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if progress_callback:
        progress_callback(50)
    
    # Basic validation - STEP files must start with ISO-10303-21 or have proper structure
    if 'ISO-10303-21' not in content:
        raise ImportError("Invalid STEP file format: missing ISO-10303-21 header")
    
    return {
        'format': FileFormat.STEP,
        'content': content,
        'metadata': {
            'size': len(content),
            'has_header': 'HEADER;' in content.upper(),
            'has_data': 'DATA;' in content.upper(),
        }
    }


def _export_step(filepath: Path, data: Dict[str, Any], progress_callback: Optional[Callable[[int], None]] = None) -> None:
    """Export STEP file (basic implementation without pythonocc)."""
    if 'content' not in data:
        raise ExportError("STEP export requires 'content' in data")
    
    if progress_callback:
        progress_callback(50)
    
    # Write content to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(data['content'])


def _import_stl(filepath: Path, progress_callback: Optional[Callable[[int], None]] = None) -> Dict[str, Any]:
    """Import STL file (both ASCII and binary formats)."""
    with open(filepath, 'rb') as f:
        header = f.read(5)
        f.seek(0)
        
        # Check if binary or ASCII
        is_binary = header[:5] != b'solid'
        
        if is_binary:
            return _import_stl_binary(f, progress_callback)
        else:
            return _import_stl_ascii(f, progress_callback)


def _import_stl_binary(f, progress_callback: Optional[Callable[[int], None]] = None) -> Dict[str, Any]:
    """Import binary STL file."""
    # Read header (80 bytes)
    header = f.read(80)
    
    if progress_callback:
        progress_callback(10)
    
    # Read number of triangles
    num_triangles = struct.unpack('<I', f.read(4))[0]
    
    vertices = []
    faces = []
    normals = []
    
    vertex_map = {}
    vertex_index = 0
    
    for i in range(num_triangles):
        # Read normal (3 floats)
        normal = struct.unpack('<fff', f.read(12))
        normals.append(normal)
        
        # Read 3 vertices (3 floats each)
        triangle_indices = []
        for j in range(3):
            vertex = struct.unpack('<fff', f.read(12))
            
            # Check if vertex already exists
            vertex_key = vertex
            if vertex_key not in vertex_map:
                vertex_map[vertex_key] = vertex_index
                vertices.append(vertex)
                vertex_index += 1
            
            triangle_indices.append(vertex_map[vertex_key])
        
        faces.append(tuple(triangle_indices))
        
        # Read attribute byte count (not used)
        f.read(2)
        
        if progress_callback and (i + 1) % max(1, num_triangles // 10) == 0:
            progress = 10 + int(90 * (i + 1) / num_triangles)
            progress_callback(progress)
    
    return {
        'format': FileFormat.STL,
        'vertices': vertices,
        'faces': faces,
        'normals': normals,
        'metadata': {
            'num_triangles': num_triangles,
            'num_vertices': len(vertices),
            'binary': True,
        }
    }


def _import_stl_ascii(f, progress_callback: Optional[Callable[[int], None]] = None) -> Dict[str, Any]:
    """Import ASCII STL file."""
    vertices = []
    faces = []
    normals = []
    
    vertex_map = {}
    vertex_index = 0
    
    current_normal = None
    current_vertices = []
    
    for line in f:
        line = line.decode('utf-8', errors='ignore').strip()
        
        if line.startswith('facet normal'):
            parts = line.split()
            current_normal = (float(parts[2]), float(parts[3]), float(parts[4]))
        elif line.startswith('vertex'):
            parts = line.split()
            vertex = (float(parts[1]), float(parts[2]), float(parts[3]))
            
            # Check if vertex already exists
            vertex_key = vertex
            if vertex_key not in vertex_map:
                vertex_map[vertex_key] = vertex_index
                vertices.append(vertex)
                vertex_index += 1
            
            current_vertices.append(vertex_map[vertex_key])
        elif line.startswith('endfacet'):
            if len(current_vertices) == 3 and current_normal:
                faces.append(tuple(current_vertices))
                normals.append(current_normal)
            current_vertices = []
            current_normal = None
    
    if progress_callback:
        progress_callback(90)
    
    return {
        'format': FileFormat.STL,
        'vertices': vertices,
        'faces': faces,
        'normals': normals,
        'metadata': {
            'num_triangles': len(faces),
            'num_vertices': len(vertices),
            'binary': False,
        }
    }


def _export_stl(filepath: Path, data: Dict[str, Any], progress_callback: Optional[Callable[[int], None]] = None) -> None:
    """Export STL file (binary format)."""
    if 'vertices' not in data or 'faces' not in data:
        raise ExportError("STL export requires 'vertices' and 'faces' in data")
    
    vertices = data['vertices']
    faces = data['faces']
    normals = data.get('normals', None)
    
    if progress_callback:
        progress_callback(10)
    
    with open(filepath, 'wb') as f:
        # Write header (80 bytes)
        header = b'Binary STL file generated by marimocad'
        header = header + b' ' * (80 - len(header))
        f.write(header)
        
        # Write number of triangles
        f.write(struct.pack('<I', len(faces)))
        
        if progress_callback:
            progress_callback(20)
        
        for i, face in enumerate(faces):
            # Calculate normal if not provided
            if normals and i < len(normals):
                normal = normals[i]
            else:
                # Calculate normal from vertices
                v0, v1, v2 = [vertices[idx] for idx in face]
                # Cross product
                u = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
                v = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
                normal = (
                    u[1] * v[2] - u[2] * v[1],
                    u[2] * v[0] - u[0] * v[2],
                    u[0] * v[1] - u[1] * v[0]
                )
                # Normalize
                length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
                if length > 0:
                    normal = (normal[0]/length, normal[1]/length, normal[2]/length)
            
            # Write normal
            f.write(struct.pack('<fff', *normal))
            
            # Write vertices
            for idx in face:
                vertex = vertices[idx]
                f.write(struct.pack('<fff', *vertex))
            
            # Write attribute byte count (unused)
            f.write(struct.pack('<H', 0))
            
            if progress_callback and (i + 1) % max(1, len(faces) // 10) == 0:
                progress = 20 + int(70 * (i + 1) / len(faces))
                progress_callback(progress)


def _import_obj(filepath: Path, progress_callback: Optional[Callable[[int], None]] = None) -> Dict[str, Any]:
    """Import OBJ file."""
    vertices = []
    normals = []
    texcoords = []
    faces = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if progress_callback:
        progress_callback(20)
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        parts = line.split()
        if not parts:
            continue
        
        if parts[0] == 'v':
            # Vertex
            vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
        elif parts[0] == 'vn':
            # Normal
            normals.append((float(parts[1]), float(parts[2]), float(parts[3])))
        elif parts[0] == 'vt':
            # Texture coordinate
            texcoords.append((float(parts[1]), float(parts[2])))
        elif parts[0] == 'f':
            # Face
            face_vertices = []
            face_normals = []
            face_texcoords = []
            
            for j in range(1, len(parts)):
                indices = parts[j].split('/')
                # Vertex index (OBJ is 1-indexed)
                face_vertices.append(int(indices[0]) - 1)
                # Texture coordinate index (optional)
                if len(indices) > 1 and indices[1]:
                    face_texcoords.append(int(indices[1]) - 1)
                # Normal index (optional)
                if len(indices) > 2 and indices[2]:
                    face_normals.append(int(indices[2]) - 1)
            
            faces.append({
                'vertices': tuple(face_vertices),
                'normals': tuple(face_normals) if face_normals else None,
                'texcoords': tuple(face_texcoords) if face_texcoords else None,
            })
        
        if progress_callback and (i + 1) % max(1, len(lines) // 10) == 0:
            progress = 20 + int(70 * (i + 1) / len(lines))
            progress_callback(progress)
    
    return {
        'format': FileFormat.OBJ,
        'vertices': vertices,
        'normals': normals,
        'texcoords': texcoords,
        'faces': faces,
        'metadata': {
            'num_vertices': len(vertices),
            'num_normals': len(normals),
            'num_texcoords': len(texcoords),
            'num_faces': len(faces),
        }
    }


def _export_obj(filepath: Path, data: Dict[str, Any], progress_callback: Optional[Callable[[int], None]] = None) -> None:
    """Export OBJ file."""
    if 'vertices' not in data or 'faces' not in data:
        raise ExportError("OBJ export requires 'vertices' and 'faces' in data")
    
    vertices = data['vertices']
    faces = data['faces']
    normals = data.get('normals', [])
    texcoords = data.get('texcoords', [])
    
    if progress_callback:
        progress_callback(10)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("# OBJ file generated by marimocad\n")
        f.write(f"# Vertices: {len(vertices)}\n")
        f.write(f"# Faces: {len(faces)}\n\n")
        
        if progress_callback:
            progress_callback(20)
        
        # Write vertices
        for i, vertex in enumerate(vertices):
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
            if progress_callback and (i + 1) % max(1, len(vertices) // 5) == 0:
                progress = 20 + int(20 * (i + 1) / len(vertices))
                progress_callback(progress)
        
        # Write normals
        if normals:
            f.write("\n")
            for normal in normals:
                f.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
        
        # Write texture coordinates
        if texcoords:
            f.write("\n")
            for texcoord in texcoords:
                f.write(f"vt {texcoord[0]} {texcoord[1]}\n")
        
        if progress_callback:
            progress_callback(50)
        
        # Write faces
        f.write("\n")
        for i, face in enumerate(faces):
            # Handle both simple tuple faces and dict faces
            if isinstance(face, dict):
                face_vertices = face['vertices']
                face_normals = face.get('normals')
                face_texcoords = face.get('texcoords')
            else:
                face_vertices = face
                face_normals = None
                face_texcoords = None
            
            f.write("f")
            for j, v_idx in enumerate(face_vertices):
                # OBJ uses 1-based indexing
                f.write(f" {v_idx + 1}")
                if face_texcoords or face_normals:
                    f.write("/")
                    if face_texcoords and j < len(face_texcoords):
                        f.write(f"{face_texcoords[j] + 1}")
                    if face_normals:
                        f.write("/")
                        if j < len(face_normals):
                            f.write(f"{face_normals[j] + 1}")
            f.write("\n")
            
            if progress_callback and (i + 1) % max(1, len(faces) // 5) == 0:
                progress = 50 + int(40 * (i + 1) / len(faces))
                progress_callback(progress)
