"""Tests for the 3D viewer module."""

import unittest

from unittest.mock import MagicMock, Mock, patch


class TestViewer(unittest.TestCase):
    """Test cases for the viewer module."""

    def test_create_threejs_viewer_empty(self):
        """Test creating an empty viewer."""
        from marimocad.viewer import create_threejs_viewer

        html = create_threejs_viewer([])
        self.assertIn("three.min.js", html)
        self.assertIn("OrbitControls", html)
        self.assertIn("viewer-container", html)

    def test_create_threejs_viewer_with_geometry(self):
        """Test creating a viewer with geometry data."""
        from marimocad.viewer import create_threejs_viewer

        geometry_data = {
            "vertices": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            "faces": [[0, 1, 2]],
            "color": "#ff0000",
        }
        html = create_threejs_viewer([geometry_data])
        self.assertIn("three.min.js", html)
        self.assertIn("#ff0000", html)

    def test_create_threejs_viewer_custom_size(self):
        """Test creating a viewer with custom dimensions."""
        from marimocad.viewer import create_threejs_viewer

        html = create_threejs_viewer([], width=1000, height=800)
        self.assertIn("1000px", html)
        self.assertIn("800px", html)

    def test_create_threejs_viewer_custom_background(self):
        """Test creating a viewer with custom background color."""
        from marimocad.viewer import create_threejs_viewer

        html = create_threejs_viewer([], background_color="#123456")
        self.assertIn("#123456", html)

    def test_geometry_to_mesh_data_unsupported_type(self):
        """Test that unsupported geometry types raise ValueError."""
        from marimocad.viewer import geometry_to_mesh_data

        unsupported_geometry = "not a geometry"
        with self.assertRaises(ValueError) as context:
            geometry_to_mesh_data(unsupported_geometry)
        self.assertIn("Unsupported geometry type", str(context.exception))

    def test_geometry_to_mesh_data_build123d(self):
        """Test converting Build123d geometry."""
        # Skip this test - it requires actual Build123d geometries
        # which we can't easily mock
        self.skipTest("Requires actual Build123d geometry")

    def test_ocp_to_mesh(self):
        """Test OCP to mesh conversion."""
        from marimocad.viewer import _ocp_to_mesh

        # This test requires OCP to be installed
        try:
            from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox

            box = BRepPrimAPI_MakeBox(10, 10, 10).Shape()
            mesh_data = _ocp_to_mesh(box)

            self.assertIn("vertices", mesh_data)
            self.assertIn("faces", mesh_data)
            self.assertIn("color", mesh_data)
            self.assertGreater(len(mesh_data["vertices"]), 0)
            self.assertGreater(len(mesh_data["faces"]), 0)
        except ImportError:
            self.skipTest("OCP not installed")


class TestMarimoIntegration(unittest.TestCase):
    """Test cases for Marimo integration."""

    def test_viewer_import_error(self):
        """Test viewer raises error when marimo is not installed."""
        with patch.dict("sys.modules", {"marimo": None}):
            # Force reimport
            import importlib

            import marimocad.marimo

            importlib.reload(marimocad.marimo)

            from marimocad.marimo import viewer

            with self.assertRaises(ImportError) as context:
                viewer(None)
            self.assertIn("marimo is required", str(context.exception))

    @patch("marimocad.marimo.geometry_to_mesh_data")
    @patch("marimocad.marimo.create_threejs_viewer")
    def test_viewer_empty(self, mock_create_viewer, mock_mesh_data):
        """Test viewer with no geometry."""
        from marimocad.marimo import viewer

        mock_create_viewer.return_value = "<html></html>"

        result = viewer(None)
        # viewer should call marimo's Html
        self.assertIsNotNone(result)

    @patch("marimocad.marimo.geometry_to_mesh_data")
    @patch("marimocad.marimo.create_threejs_viewer")
    def test_viewer_single_geometry(self, mock_create_viewer, mock_mesh_data):
        """Test viewer with a single geometry."""
        from marimocad.marimo import viewer

        mock_mesh_data.return_value = {
            "vertices": [[0, 0, 0]],
            "faces": [[0, 1, 2]],
            "color": "#3498db",
        }
        mock_create_viewer.return_value = "<html></html>"
        mock_geom = Mock()

        result = viewer(mock_geom)
        mock_mesh_data.assert_called_once()
        mock_create_viewer.assert_called_once()

    @patch("marimocad.marimo.geometry_to_mesh_data")
    @patch("marimocad.marimo.create_threejs_viewer")
    def test_viewer_multiple_geometries(self, mock_create_viewer, mock_mesh_data):
        """Test viewer with multiple geometries."""
        from marimocad.marimo import viewer

        mock_mesh_data.return_value = {
            "vertices": [[0, 0, 0]],
            "faces": [[0, 1, 2]],
            "color": "#3498db",
        }
        mock_create_viewer.return_value = "<html></html>"
        mock_geoms = [Mock(), Mock()]

        result = viewer(mock_geoms)
        self.assertEqual(mock_mesh_data.call_count, 2)
        mock_create_viewer.assert_called_once()

    def test_geometry_card_initialization(self):
        """Test GeometryCard initialization."""
        from marimocad.marimo import GeometryCard

        mock_geom = Mock()
        mock_geom.faces.return_value = [1, 2, 3]
        mock_geom.edges.return_value = [1, 2, 3, 4]
        mock_geom.vertices.return_value = [1, 2, 3, 4, 5]

        card = GeometryCard(mock_geom)
        self.assertIsNotNone(card._properties)

    def test_geometry_card_render(self):
        """Test GeometryCard rendering."""
        from marimocad.marimo import GeometryCard

        mock_geom = Mock()
        mock_geom.faces.return_value = [1, 2, 3]

        card = GeometryCard(mock_geom)
        result = card.render()
        # Check that result is a marimo component (has certain structure)
        self.assertIsNotNone(result)

    def test_parametric_model(self):
        """Test parametric model creation."""
        # Skip this test due to complexity in mocking marimo components
        self.skipTest("Complex marimo component mocking")

    def test_parametric_model_error(self):
        """Test parametric model with error in function."""
        from marimocad.marimo import parametric_model

        mock_slider = Mock()
        mock_slider.value = 10

        params = {"length": mock_slider}

        def error_func(**kwargs):
            raise ValueError("Test error")

        result = parametric_model(error_func, params)
        # Should return an error HTML component
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
