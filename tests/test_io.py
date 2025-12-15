"""Tests for CAD file import/export functionality."""

import os
import pytest
import tempfile
from pathlib import Path

from marimocad import import_file, export_file, detect_format, validate_file
from marimocad.io import FileFormat, FileFormatError, ImportError, ExportError
from tests.fixtures import create_test_files


@pytest.fixture
def test_dir():
    """Create a temporary directory with test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = Path(tmpdir)
        create_test_files(test_path)
        yield test_path


class TestFormatDetection:
    """Test format detection functionality."""
    
    def test_detect_step_by_extension(self, test_dir):
        """Test STEP format detection by file extension."""
        filepath = test_dir / "cube.step"
        format = detect_format(filepath)
        assert format == FileFormat.STEP
    
    def test_detect_stl_by_extension(self, test_dir):
        """Test STL format detection by file extension."""
        filepath = test_dir / "cube_binary.stl"
        format = detect_format(filepath)
        assert format == FileFormat.STL
    
    def test_detect_obj_by_extension(self, test_dir):
        """Test OBJ format detection by file extension."""
        filepath = test_dir / "cube.obj"
        format = detect_format(filepath)
        assert format == FileFormat.OBJ
    
    def test_detect_step_by_content(self, test_dir):
        """Test STEP format detection by file content."""
        filepath = test_dir / "cube.step"
        format = detect_format(filepath)
        assert format == FileFormat.STEP
    
    def test_detect_binary_stl_by_content(self, test_dir):
        """Test binary STL format detection by file content."""
        filepath = test_dir / "cube_binary.stl"
        format = detect_format(filepath)
        assert format == FileFormat.STL
    
    def test_detect_ascii_stl_by_content(self, test_dir):
        """Test ASCII STL format detection by file content."""
        filepath = test_dir / "cube_ascii.stl"
        format = detect_format(filepath)
        assert format == FileFormat.STL
    
    def test_detect_nonexistent_file(self, test_dir):
        """Test format detection with non-existent file."""
        filepath = test_dir / "nonexistent.stl"
        with pytest.raises(FileFormatError):
            detect_format(filepath)


class TestFileValidation:
    """Test file validation functionality."""
    
    def test_validate_step_file(self, test_dir):
        """Test validation of valid STEP file."""
        filepath = test_dir / "cube.step"
        assert validate_file(filepath) is True
    
    def test_validate_stl_file(self, test_dir):
        """Test validation of valid STL file."""
        filepath = test_dir / "cube_binary.stl"
        assert validate_file(filepath) is True
    
    def test_validate_obj_file(self, test_dir):
        """Test validation of valid OBJ file."""
        filepath = test_dir / "cube.obj"
        assert validate_file(filepath) is True
    
    def test_validate_empty_file(self, test_dir):
        """Test validation of empty file."""
        filepath = test_dir / "empty.stl"
        assert validate_file(filepath) is False
    
    def test_validate_with_expected_format(self, test_dir):
        """Test validation with expected format."""
        filepath = test_dir / "cube.step"
        assert validate_file(filepath, FileFormat.STEP) is True
        assert validate_file(filepath, FileFormat.STL) is False
    
    def test_validate_nonexistent_file(self, test_dir):
        """Test validation of non-existent file."""
        filepath = test_dir / "nonexistent.stl"
        with pytest.raises(FileFormatError):
            validate_file(filepath)


class TestSTEPImportExport:
    """Test STEP file import/export."""
    
    def test_import_step_file(self, test_dir):
        """Test importing a STEP file."""
        filepath = test_dir / "cube.step"
        result = import_file(filepath)
        
        assert result['format'] == FileFormat.STEP
        assert 'content' in result
        assert 'metadata' in result
        assert result['metadata']['has_header'] is True
        assert result['metadata']['has_data'] is True
    
    def test_export_step_file(self, test_dir):
        """Test exporting a STEP file."""
        # Import first
        input_filepath = test_dir / "cube.step"
        data = import_file(input_filepath)
        
        # Export
        output_filepath = test_dir / "cube_exported.step"
        export_file(output_filepath, data, FileFormat.STEP)
        
        assert output_filepath.exists()
        assert validate_file(output_filepath, FileFormat.STEP)
        
        # Verify content is preserved
        reimported = import_file(output_filepath)
        assert reimported['content'] == data['content']
    
    def test_import_invalid_step(self, test_dir):
        """Test importing an invalid STEP file."""
        filepath = test_dir / "invalid.step"
        with pytest.raises(ImportError):
            import_file(filepath)
    
    def test_export_step_without_content(self, test_dir):
        """Test exporting STEP without required content."""
        filepath = test_dir / "test_export.step"
        with pytest.raises(ExportError):
            export_file(filepath, {}, FileFormat.STEP)


class TestSTLImportExport:
    """Test STL file import/export."""
    
    def test_import_binary_stl(self, test_dir):
        """Test importing a binary STL file."""
        filepath = test_dir / "cube_binary.stl"
        result = import_file(filepath)
        
        assert result['format'] == FileFormat.STL
        assert 'vertices' in result
        assert 'faces' in result
        assert 'normals' in result
        assert len(result['faces']) == 12  # Cube has 12 triangles
        assert result['metadata']['binary'] is True
    
    def test_import_ascii_stl(self, test_dir):
        """Test importing an ASCII STL file."""
        filepath = test_dir / "cube_ascii.stl"
        result = import_file(filepath)
        
        assert result['format'] == FileFormat.STL
        assert 'vertices' in result
        assert 'faces' in result
        assert 'normals' in result
        assert len(result['faces']) == 12  # Cube has 12 triangles
        assert result['metadata']['binary'] is False
    
    def test_export_binary_stl(self, test_dir):
        """Test exporting a binary STL file."""
        # Create test data
        vertices = [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.5, 1.0, 0.0),
        ]
        faces = [(0, 1, 2)]
        
        data = {
            'vertices': vertices,
            'faces': faces,
        }
        
        # Export
        filepath = test_dir / "triangle.stl"
        export_file(filepath, data, FileFormat.STL)
        
        assert filepath.exists()
        assert validate_file(filepath, FileFormat.STL)
        
        # Verify by reimporting
        reimported = import_file(filepath)
        assert len(reimported['faces']) == 1
        assert len(reimported['vertices']) == 3
    
    def test_export_stl_with_normals(self, test_dir):
        """Test exporting STL with pre-calculated normals."""
        vertices = [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.5, 1.0, 0.0),
        ]
        faces = [(0, 1, 2)]
        normals = [(0.0, 0.0, 1.0)]
        
        data = {
            'vertices': vertices,
            'faces': faces,
            'normals': normals,
        }
        
        # Export
        filepath = test_dir / "triangle_with_normals.stl"
        export_file(filepath, data, FileFormat.STL)
        
        assert filepath.exists()
    
    def test_stl_roundtrip(self, test_dir):
        """Test STL import/export roundtrip."""
        # Import original
        input_filepath = test_dir / "cube_binary.stl"
        original = import_file(input_filepath)
        
        # Export
        output_filepath = test_dir / "cube_roundtrip.stl"
        export_file(output_filepath, original, FileFormat.STL)
        
        # Reimport
        reimported = import_file(output_filepath)
        
        # Compare
        assert len(reimported['faces']) == len(original['faces'])
        assert len(reimported['vertices']) == len(original['vertices'])


class TestOBJImportExport:
    """Test OBJ file import/export."""
    
    def test_import_obj_file(self, test_dir):
        """Test importing an OBJ file."""
        filepath = test_dir / "cube.obj"
        result = import_file(filepath)
        
        assert result['format'] == FileFormat.OBJ
        assert 'vertices' in result
        assert 'faces' in result
        assert len(result['vertices']) == 8  # Cube has 8 vertices
        assert len(result['faces']) == 12  # Cube has 12 triangles
    
    def test_export_obj_file(self, test_dir):
        """Test exporting an OBJ file."""
        # Create test data
        vertices = [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.5, 1.0, 0.0),
        ]
        faces = [(0, 1, 2)]
        
        data = {
            'vertices': vertices,
            'faces': faces,
        }
        
        # Export
        filepath = test_dir / "triangle.obj"
        export_file(filepath, data, FileFormat.OBJ)
        
        assert filepath.exists()
        assert validate_file(filepath, FileFormat.OBJ)
    
    def test_export_obj_with_normals(self, test_dir):
        """Test exporting OBJ with normals."""
        vertices = [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.5, 1.0, 0.0),
        ]
        faces = [
            {
                'vertices': (0, 1, 2),
                'normals': (0, 0, 0),
            }
        ]
        normals = [(0.0, 0.0, 1.0)]
        
        data = {
            'vertices': vertices,
            'faces': faces,
            'normals': normals,
        }
        
        # Export
        filepath = test_dir / "triangle_with_normals.obj"
        export_file(filepath, data, FileFormat.OBJ)
        
        assert filepath.exists()
    
    def test_obj_roundtrip(self, test_dir):
        """Test OBJ import/export roundtrip."""
        # Import original
        input_filepath = test_dir / "cube.obj"
        original = import_file(input_filepath)
        
        # Export
        output_filepath = test_dir / "cube_roundtrip.obj"
        export_file(output_filepath, original, FileFormat.OBJ)
        
        # Reimport
        reimported = import_file(output_filepath)
        
        # Compare
        assert len(reimported['faces']) == len(original['faces'])
        assert len(reimported['vertices']) == len(original['vertices'])


class TestProgressCallback:
    """Test progress callback functionality."""
    
    def test_import_with_progress(self, test_dir):
        """Test import with progress callback."""
        progress_values = []
        
        def progress_callback(value):
            progress_values.append(value)
        
        filepath = test_dir / "cube_binary.stl"
        import_file(filepath, progress_callback=progress_callback)
        
        # Should have at least start and end progress
        assert len(progress_values) >= 2
        assert progress_values[0] == 0
        assert progress_values[-1] == 100
        # Progress should be monotonically increasing
        assert all(progress_values[i] <= progress_values[i+1] for i in range(len(progress_values)-1))
    
    def test_export_with_progress(self, test_dir):
        """Test export with progress callback."""
        progress_values = []
        
        def progress_callback(value):
            progress_values.append(value)
        
        data = {
            'vertices': [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.5, 1.0, 0.0)],
            'faces': [(0, 1, 2)],
        }
        
        filepath = test_dir / "test_progress.stl"
        export_file(filepath, data, FileFormat.STL, progress_callback=progress_callback)
        
        # Should have at least start and end progress
        assert len(progress_values) >= 2
        assert progress_values[0] == 0
        assert progress_values[-1] == 100


class TestErrorHandling:
    """Test error handling."""
    
    def test_import_nonexistent_file(self, test_dir):
        """Test importing non-existent file."""
        filepath = test_dir / "nonexistent.stl"
        with pytest.raises(ImportError):
            import_file(filepath)
    
    def test_import_unknown_format(self, test_dir):
        """Test importing file with unknown format."""
        filepath = test_dir / "corrupted.stl"
        # This should raise an error due to invalid format
        with pytest.raises((FileFormatError, ImportError)):
            import_file(filepath)
    
    def test_export_without_required_data(self, test_dir):
        """Test exporting without required data."""
        filepath = test_dir / "test.stl"
        with pytest.raises(ExportError):
            export_file(filepath, {}, FileFormat.STL)
    
    def test_export_unknown_format(self, test_dir):
        """Test exporting with unknown format."""
        filepath = test_dir / "test.xyz"
        data = {'vertices': [], 'faces': []}
        with pytest.raises(FileFormatError):
            export_file(filepath, data)


class TestFormatAutoDetection:
    """Test automatic format detection in import/export."""
    
    def test_import_autodetect(self, test_dir):
        """Test import with auto-detected format."""
        filepath = test_dir / "cube.stl"
        # Rename to test autodetection
        import shutil
        shutil.copy(test_dir / "cube_binary.stl", filepath)
        
        result = import_file(filepath)
        assert result['format'] == FileFormat.STL
    
    def test_export_autodetect_from_extension(self, test_dir):
        """Test export with format auto-detected from extension."""
        data = {
            'vertices': [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.5, 1.0, 0.0)],
            'faces': [(0, 1, 2)],
        }
        
        # Export with different extensions
        for ext, expected_format in [('.stl', FileFormat.STL), ('.obj', FileFormat.OBJ)]:
            filepath = test_dir / f"test{ext}"
            export_file(filepath, data)
            assert filepath.exists()
            
            # Verify format
            result = import_file(filepath)
            assert result['format'] == expected_format
