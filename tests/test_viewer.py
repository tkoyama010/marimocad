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

    @patch("marimocad.viewer._build123d_to_mesh")
    def test_geometry_to_mesh_data_build123d(self, mock_build123d):
        """Test converting Build123d geometry."""
        from marimocad.viewer import geometry_to_mesh_data

        # Mock Build123d imports
        with patch.dict("sys.modules", {"build123d": MagicMock()}):
            from build123d import Part

            mock_geometry = Mock(spec=Part)
            mock_build123d.return_value = {
                "vertices": [],
                "faces": [],
                "color": "#3498db",
            }

            result = geometry_to_mesh_data(mock_geometry)
            self.assertEqual(result["color"], "#3498db")
            mock_build123d.assert_called_once()

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

    @patch("marimocad.marimo.mo")
    def test_viewer_import_error(self, mock_mo):
        """Test viewer raises error when marimo is not installed."""
        with patch.dict("sys.modules", {"marimo": None}):
            from marimocad.marimo import viewer

            with self.assertRaises(ImportError) as context:
                viewer(None)
            self.assertIn("marimo is required", str(context.exception))

    @patch("marimocad.marimo.mo")
    @patch("marimocad.marimo.geometry_to_mesh_data")
    def test_viewer_empty(self, mock_mesh_data, mock_mo):
        """Test viewer with no geometry."""
        from marimocad.marimo import viewer

        result = viewer(None)
        mock_mo.Html.assert_called_once()

    @patch("marimocad.marimo.mo")
    @patch("marimocad.marimo.geometry_to_mesh_data")
    def test_viewer_single_geometry(self, mock_mesh_data, mock_mo):
        """Test viewer with a single geometry."""
        from marimocad.marimo import viewer

        mock_mesh_data.return_value = {
            "vertices": [[0, 0, 0]],
            "faces": [[0, 1, 2]],
            "color": "#3498db",
        }
        mock_geom = Mock()

        result = viewer(mock_geom)
        mock_mesh_data.assert_called_once()
        mock_mo.Html.assert_called_once()

    @patch("marimocad.marimo.mo")
    @patch("marimocad.marimo.geometry_to_mesh_data")
    def test_viewer_multiple_geometries(self, mock_mesh_data, mock_mo):
        """Test viewer with multiple geometries."""
        from marimocad.marimo import viewer

        mock_mesh_data.return_value = {
            "vertices": [[0, 0, 0]],
            "faces": [[0, 1, 2]],
            "color": "#3498db",
        }
        mock_geoms = [Mock(), Mock()]

        result = viewer(mock_geoms)
        self.assertEqual(mock_mesh_data.call_count, 2)
        mock_mo.Html.assert_called_once()

    def test_geometry_card_initialization(self):
        """Test GeometryCard initialization."""
        from marimocad.marimo import GeometryCard

        mock_geom = Mock()
        mock_geom.faces.return_value = [1, 2, 3]
        mock_geom.edges.return_value = [1, 2, 3, 4]
        mock_geom.vertices.return_value = [1, 2, 3, 4, 5]

        card = GeometryCard(mock_geom)
        self.assertIsNotNone(card._properties)

    @patch("marimocad.marimo.mo")
    def test_geometry_card_render(self, mock_mo):
        """Test GeometryCard rendering."""
        from marimocad.marimo import GeometryCard

        mock_geom = Mock()
        mock_geom.faces.return_value = [1, 2, 3]

        card = GeometryCard(mock_geom)
        result = card.render()
        mock_mo.md.assert_called_once()

    @patch("marimocad.marimo.mo")
    @patch("marimocad.marimo.viewer")
    def test_parametric_model(self, mock_viewer, mock_mo):
        """Test parametric model creation."""
        from marimocad.marimo import parametric_model

        # Mock UI elements
        mock_slider = Mock()
        mock_slider.value = 10

        params = {"length": mock_slider}
        func = Mock(return_value=Mock())

        result = parametric_model(func, params)
        func.assert_called_once_with(length=10)
        mock_viewer.assert_called_once()

    @patch("marimocad.marimo.mo")
    def test_parametric_model_error(self, mock_mo):
        """Test parametric model with error in function."""
        from marimocad.marimo import parametric_model

        mock_slider = Mock()
        mock_slider.value = 10

        params = {"length": mock_slider}

        def error_func(**kwargs):
            raise ValueError("Test error")

        result = parametric_model(error_func, params)
        mock_mo.Html.assert_called_once()


if __name__ == "__main__":
    unittest.main()
