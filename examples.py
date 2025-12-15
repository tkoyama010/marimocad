#!/usr/bin/env python
"""Example usage of marimocad file import/export."""

from marimocad import import_file, export_file, detect_format, validate_file
from marimocad.io import FileFormat
import tempfile
from pathlib import Path


def create_simple_triangle():
    """Create a simple triangle mesh."""
    return {
        'vertices': [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.5, 1.0, 0.0),
        ],
        'faces': [(0, 1, 2)],
    }


def example_basic_export():
    """Example: Export a simple triangle to different formats."""
    print("=" * 60)
    print("Example 1: Basic Export")
    print("=" * 60)
    
    data = create_simple_triangle()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Export to STL
        stl_file = tmpdir / "triangle.stl"
        export_file(stl_file, data, FileFormat.STL)
        print(f"✓ Exported to STL: {stl_file}")
        print(f"  File size: {stl_file.stat().st_size} bytes")
        
        # Export to OBJ
        obj_file = tmpdir / "triangle.obj"
        export_file(obj_file, data)  # Format auto-detected from extension
        print(f"✓ Exported to OBJ: {obj_file}")
        print(f"  File size: {obj_file.stat().st_size} bytes")
        print()


def example_import_and_validate():
    """Example: Import a file and validate it."""
    print("=" * 60)
    print("Example 2: Import and Validate")
    print("=" * 60)
    
    data = create_simple_triangle()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Export a file first
        stl_file = tmpdir / "test.stl"
        export_file(stl_file, data, FileFormat.STL)
        
        # Detect format
        detected_format = detect_format(stl_file)
        print(f"✓ Detected format: {detected_format}")
        
        # Validate file
        is_valid = validate_file(stl_file)
        print(f"✓ File is valid: {is_valid}")
        
        # Import file
        imported_data = import_file(stl_file)
        print(f"✓ Imported successfully")
        print(f"  Format: {imported_data['format']}")
        print(f"  Vertices: {len(imported_data['vertices'])}")
        print(f"  Faces: {len(imported_data['faces'])}")
        print(f"  Metadata: {imported_data['metadata']}")
        print()


def example_progress_tracking():
    """Example: Import with progress tracking."""
    print("=" * 60)
    print("Example 3: Progress Tracking")
    print("=" * 60)
    
    # Create a slightly larger mesh for better progress demonstration
    vertices = []
    faces = []
    
    # Create a grid of triangles
    grid_size = 10
    for i in range(grid_size):
        for j in range(grid_size):
            x, y = float(i), float(j)
            base_idx = len(vertices)
            
            # Add 4 vertices for a quad
            vertices.extend([
                (x, y, 0.0),
                (x + 1, y, 0.0),
                (x + 1, y + 1, 0.0),
                (x, y + 1, 0.0),
            ])
            
            # Add 2 triangles
            faces.extend([
                (base_idx, base_idx + 1, base_idx + 2),
                (base_idx, base_idx + 2, base_idx + 3),
            ])
    
    data = {'vertices': vertices, 'faces': faces}
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        stl_file = tmpdir / "grid.stl"
        
        # Export with progress
        print("Exporting...")
        def export_progress(percent):
            print(f"  Export progress: {percent}%")
        
        export_file(stl_file, data, FileFormat.STL, progress_callback=export_progress)
        
        # Import with progress
        print("\nImporting...")
        def import_progress(percent):
            print(f"  Import progress: {percent}%")
        
        result = import_file(stl_file, progress_callback=import_progress)
        
        print(f"\n✓ Created mesh with {len(result['faces'])} triangles")
        print()


def example_roundtrip():
    """Example: Export and import roundtrip."""
    print("=" * 60)
    print("Example 4: Format Conversion (Roundtrip)")
    print("=" * 60)
    
    data = create_simple_triangle()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Export to STL
        stl_file = tmpdir / "model.stl"
        export_file(stl_file, data, FileFormat.STL)
        print(f"✓ Exported to STL")
        
        # Import from STL
        imported = import_file(stl_file)
        print(f"✓ Imported from STL")
        
        # Export to OBJ
        obj_file = tmpdir / "model.obj"
        export_file(obj_file, imported, FileFormat.OBJ)
        print(f"✓ Converted to OBJ")
        
        # Verify
        final = import_file(obj_file)
        print(f"✓ Verified OBJ file")
        print(f"  Original vertices: {len(data['vertices'])}")
        print(f"  Final vertices: {len(final['vertices'])}")
        print(f"  Original faces: {len(data['faces'])}")
        print(f"  Final faces: {len(final['faces'])}")
        print()


def example_error_handling():
    """Example: Error handling."""
    print("=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)
    
    from marimocad.io import FileFormatError, ImportError, ExportError
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Try to import non-existent file
        try:
            import_file(tmpdir / "nonexistent.stl")
        except ImportError as e:
            print(f"✓ Caught ImportError: {type(e).__name__}")
        
        # Try to export with missing data
        try:
            export_file(tmpdir / "invalid.stl", {}, FileFormat.STL)
        except ExportError as e:
            print(f"✓ Caught ExportError: {type(e).__name__}")
        
        # Try to export with unknown format
        try:
            export_file(tmpdir / "file.xyz", {'vertices': [], 'faces': []})
        except FileFormatError as e:
            print(f"✓ Caught FileFormatError: {type(e).__name__}")
        
        print()


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         marimocad File Import/Export Examples             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    example_basic_export()
    example_import_and_validate()
    example_progress_tracking()
    example_roundtrip()
    example_error_handling()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
    print()
