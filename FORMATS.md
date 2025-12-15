# File Import/Export Documentation

## Overview

The `marimocad` package provides comprehensive support for importing and exporting CAD models in standard file formats. This document describes the supported formats, usage examples, and limitations.

## Supported Formats

### STEP (Standard for the Exchange of Product Data)
- **Extensions**: `.step`, `.stp`
- **Import**: ✅ Supported
- **Export**: ✅ Supported
- **Description**: STEP is an ISO standard (ISO 10303) for representing 3D product data. It's widely used for exchanging CAD models between different software applications.

#### Limitations:
- Current implementation provides basic STEP file handling
- Complex assemblies may require additional processing
- For advanced STEP processing, consider using pythonocc-core

### STL (Stereolithography)
- **Extensions**: `.stl`
- **Import**: ✅ Supported (both ASCII and binary)
- **Export**: ✅ Supported (binary format)
- **Description**: STL is a widely-used format for 3D printing and mesh-based CAD models.

#### Features:
- Automatic detection of ASCII vs. binary format
- Vertex deduplication on import
- Normal calculation on export (if not provided)
- Progress reporting for large files

#### Limitations:
- Only supports triangular meshes
- No color or material information
- Binary export only (for efficiency)

### OBJ (Wavefront Object)
- **Extensions**: `.obj`
- **Import**: ✅ Supported
- **Export**: ✅ Supported
- **Description**: OBJ is a simple text-based format commonly used in 3D graphics and CAD applications.

#### Features:
- Supports vertices, normals, and texture coordinates
- Handles both simple and complex face definitions
- Human-readable format

#### Limitations:
- Material definitions (.mtl files) not yet supported
- No advanced geometry types (curves, surfaces)

## Usage Examples

### Basic Import

```python
from marimocad import import_file

# Import a file (format auto-detected)
result = import_file("model.stl")

print(f"Format: {result['format']}")
print(f"Vertices: {len(result['vertices'])}")
print(f"Faces: {len(result['faces'])}")
```

### Basic Export

```python
from marimocad import export_file
from marimocad.io import FileFormat

# Prepare data
data = {
    'vertices': [
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.5, 1.0, 0.0),
    ],
    'faces': [(0, 1, 2)],
}

# Export to STL
export_file("triangle.stl", data, FileFormat.STL)

# Export to OBJ (format auto-detected from extension)
export_file("triangle.obj", data)
```

### Progress Tracking

```python
from marimocad import import_file

def progress_callback(percent):
    print(f"Progress: {percent}%")

# Import with progress tracking
result = import_file("large_model.stl", progress_callback=progress_callback)
```

### Format Detection and Validation

```python
from marimocad import detect_format, validate_file
from marimocad.io import FileFormat

# Detect format
format = detect_format("model.stl")
print(f"Detected format: {format}")

# Validate file
is_valid = validate_file("model.stl")
print(f"Valid: {is_valid}")

# Validate with expected format
is_valid_stl = validate_file("model.stl", FileFormat.STL)
print(f"Valid STL: {is_valid_stl}")
```

### Working with STEP Files

```python
from marimocad import import_file, export_file
from marimocad.io import FileFormat

# Import STEP file
step_data = import_file("model.step")

# Access content
content = step_data['content']
metadata = step_data['metadata']

print(f"Has header: {metadata['has_header']}")
print(f"Has data: {metadata['has_data']}")

# Export STEP file
export_file("output.step", step_data, FileFormat.STEP)
```

### Working with STL Files

```python
from marimocad import import_file, export_file

# Import STL (automatically handles ASCII and binary)
stl_data = import_file("model.stl")

# Access mesh data
vertices = stl_data['vertices']
faces = stl_data['faces']
normals = stl_data['normals']

print(f"Number of triangles: {len(faces)}")
print(f"Binary format: {stl_data['metadata']['binary']}")

# Modify or process mesh...

# Export as binary STL
export_file("output.stl", stl_data)
```

### Working with OBJ Files

```python
from marimocad import import_file, export_file

# Import OBJ
obj_data = import_file("model.obj")

# Access data
vertices = obj_data['vertices']
faces = obj_data['faces']
normals = obj_data.get('normals', [])
texcoords = obj_data.get('texcoords', [])

# Create OBJ with normals
data = {
    'vertices': vertices,
    'faces': [
        {
            'vertices': (0, 1, 2),
            'normals': (0, 0, 0),
        }
    ],
    'normals': [(0.0, 0.0, 1.0)],
}

export_file("output.obj", data)
```

### Error Handling

```python
from marimocad import import_file, export_file
from marimocad.io import FileFormatError, ImportError, ExportError

try:
    result = import_file("model.stl")
except FileFormatError as e:
    print(f"Format error: {e}")
except ImportError as e:
    print(f"Import error: {e}")

try:
    export_file("output.stl", data)
except ExportError as e:
    print(f"Export error: {e}")
```

## Data Format Specifications

### Import Result Dictionary

All import functions return a dictionary with the following structure:

```python
{
    'format': FileFormat,        # Enum indicating the format
    'vertices': List[Tuple],     # List of (x, y, z) tuples (for mesh formats)
    'faces': List[Tuple],        # List of face vertex indices (for mesh formats)
    'normals': List[Tuple],      # List of normal vectors (optional)
    'texcoords': List[Tuple],    # List of texture coordinates (optional, OBJ only)
    'content': str,              # File content (STEP only)
    'metadata': Dict,            # Format-specific metadata
}
```

### Export Data Dictionary

For mesh formats (STL, OBJ):
```python
{
    'vertices': [
        (x1, y1, z1),
        (x2, y2, z2),
        # ...
    ],
    'faces': [
        (v1_idx, v2_idx, v3_idx),  # Triangle
        # ...
    ],
    'normals': [  # Optional
        (nx, ny, nz),
        # ...
    ],
    'texcoords': [  # Optional, OBJ only
        (u, v),
        # ...
    ],
}
```

For STEP format:
```python
{
    'content': "ISO-10303-21;\\n...",  # STEP file content
}
```

## Performance Considerations

### Large Files

- **Progress Callbacks**: Use progress callbacks for visual feedback on large files
- **Binary STL**: Binary STL format is more efficient than ASCII for large meshes
- **Memory Usage**: Large meshes are loaded entirely into memory

### Optimization Tips

1. For large STL files, prefer binary format over ASCII
2. Use progress callbacks to provide user feedback
3. Consider file size limits based on available memory
4. For very large files, consider streaming or chunked processing (not yet implemented)

## Integration with marimo

The `marimocad` package is designed to work seamlessly with marimo notebooks:

```python
import marimo as mo
from marimocad import import_file, export_file

# File upload widget
file_upload = mo.ui.file()

# Process uploaded file
if file_upload.value:
    # Save uploaded content
    with open("uploaded_model.stl", "wb") as f:
        f.write(file_upload.value.content)
    
    # Import and process
    model_data = import_file("uploaded_model.stl")
    
    # Display info
    mo.md(f"""
    ## Model Information
    - Format: {model_data['format']}
    - Vertices: {len(model_data['vertices'])}
    - Faces: {len(model_data['faces'])}
    """)
```

## Future Enhancements

Planned features for future releases:

- [ ] Full pythonocc-core integration for advanced STEP processing
- [ ] IGES format support
- [ ] Advanced mesh processing (decimation, smoothing)
- [ ] Material and color support for OBJ
- [ ] Streaming support for very large files
- [ ] Assembly support for STEP files
- [ ] Unit conversion utilities
- [ ] Mesh validation and repair tools

## Troubleshooting

### Common Issues

1. **"Unknown file format"**
   - Ensure file has correct extension
   - Verify file is not corrupted
   - Check file content matches expected format

2. **"Import failed"**
   - Check file permissions
   - Verify file is not empty
   - Ensure file format is valid

3. **"Export failed"**
   - Verify output directory exists and is writable
   - Check that required data fields are present
   - Ensure data types are correct

### Getting Help

For issues or questions:
1. Check this documentation
2. Review the test cases in `tests/test_io.py`
3. Open an issue on GitHub

## Version History

### 0.1.0 (Current)
- Initial release
- STEP import/export (basic)
- STL import/export (ASCII and binary)
- OBJ import/export
- Format detection and validation
- Progress callback support
- Comprehensive test suite
