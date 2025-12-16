"""Tests for the marimocad.visualization module."""

import numpy as np
import pytest

from build123d import Box, BuildPart, Cylinder


def test_extract_mesh_data_box() -> None:
    """Test mesh extraction from a simple box."""
    from marimocad.visualization import extract_mesh_data

    with BuildPart() as box:
        Box(10, 10, 10)

    vertices, triangles = extract_mesh_data(box.part)

    # Check that we got reasonable mesh data
    assert isinstance(vertices, np.ndarray)
    assert isinstance(triangles, np.ndarray)
    assert vertices.shape[1] == 3  # 3D coordinates
    assert triangles.shape[1] == 3  # Triangle indices
    assert len(vertices) > 0
    assert len(triangles) > 0

    # Box should have 6 faces, each tessellated into triangles
    # Minimum 2 triangles per face = 12 triangles
    assert len(triangles) >= 12


def test_extract_mesh_data_cylinder() -> None:
    """Test mesh extraction from a cylinder."""
    from marimocad.visualization import extract_mesh_data

    with BuildPart() as cylinder:
        Cylinder(5, 10)

    vertices, triangles = extract_mesh_data(cylinder.part)

    assert isinstance(vertices, np.ndarray)
    assert isinstance(triangles, np.ndarray)
    assert vertices.shape[1] == 3
    assert triangles.shape[1] == 3
    assert len(vertices) > 0
    assert len(triangles) > 0

    # Cylinder should have many more triangles than a box
    assert len(triangles) > 100


def test_create_plotly_figure_basic() -> None:
    """Test creating a basic Plotly figure."""
    from marimocad.visualization import create_plotly_figure

    with BuildPart() as box:
        Box(10, 10, 10)

    fig = create_plotly_figure(box.part)

    # Check figure structure
    assert fig is not None
    assert len(fig.data) >= 1  # At least the mesh trace

    # Check mesh trace properties
    mesh_trace = fig.data[0]
    assert mesh_trace.type == "mesh3d"
    assert len(mesh_trace.x) > 0
    assert len(mesh_trace.y) > 0
    assert len(mesh_trace.z) > 0


def test_create_plotly_figure_with_options() -> None:
    """Test creating a Plotly figure with custom options."""
    from marimocad.visualization import create_plotly_figure

    with BuildPart() as box:
        Box(15, 10, 8)

    fig = create_plotly_figure(
        box.part,
        color="red",
        opacity=0.7,
        title="Custom Box",
        show_edges=False,
    )

    assert fig is not None
    assert fig.layout.title.text == "Custom Box"

    mesh_trace = fig.data[0]
    assert mesh_trace.color == "red"
    assert mesh_trace.opacity == 0.7

    # With show_edges=False, should only have mesh trace
    assert len(fig.data) == 1


def test_create_plotly_figure_with_edges() -> None:
    """Test creating a Plotly figure with edge display."""
    from marimocad.visualization import create_plotly_figure

    with BuildPart() as box:
        Box(10, 10, 10)

    fig = create_plotly_figure(box.part, show_edges=True)

    # With show_edges=True, should have mesh and edge traces
    assert len(fig.data) == 2
    assert fig.data[0].type == "mesh3d"
    assert fig.data[1].type == "scatter3d"


def test_create_multi_part_figure() -> None:
    """Test creating a figure with multiple parts."""
    from marimocad.visualization import create_multi_part_figure

    with BuildPart() as box:
        Box(10, 10, 10)

    with BuildPart() as cylinder:
        Cylinder(5, 10)

    parts = [
        (box.part, "lightblue"),
        (cylinder.part, "lightcoral"),
    ]

    fig = create_multi_part_figure(parts, title="Multi-Part Assembly")

    assert fig is not None
    assert len(fig.data) == 2  # Two mesh traces
    assert fig.layout.title.text == "Multi-Part Assembly"

    # Check that both parts are present
    assert fig.data[0].type == "mesh3d"
    assert fig.data[1].type == "mesh3d"
    assert fig.data[0].color == "lightblue"
    assert fig.data[1].color == "lightcoral"


def test_create_multi_part_figure_empty_list() -> None:
    """Test that empty parts list raises ValueError."""
    from marimocad.visualization import create_multi_part_figure

    with pytest.raises(ValueError, match="At least one part must be provided"):
        create_multi_part_figure([])


def test_extract_mesh_data_preserves_dimensions() -> None:
    """Test that mesh extraction preserves proper dimensions."""
    from marimocad.visualization import extract_mesh_data

    # Test with different sized boxes
    test_sizes = [(10, 10, 10), (20, 15, 5), (5, 30, 12)]

    for length, width, height in test_sizes:
        with BuildPart() as box:
            Box(length, width, height)

        vertices, _triangles = extract_mesh_data(box.part)

        # Check bounding box roughly matches input dimensions
        # (with some tolerance for tessellation)
        x_range = vertices[:, 0].max() - vertices[:, 0].min()
        y_range = vertices[:, 1].max() - vertices[:, 1].min()
        z_range = vertices[:, 2].max() - vertices[:, 2].min()

        assert abs(x_range - length) < 0.1
        assert abs(y_range - width) < 0.1
        assert abs(z_range - height) < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
