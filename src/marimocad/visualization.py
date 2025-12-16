"""3D visualization utilities for marimocad.

This module provides functions to convert Build123d geometry to 3D visualizations
that can be displayed in marimo notebooks, including WASM environments.

The module supports:
- Mesh extraction from Build123d/OCP geometry
- Plotly 3D mesh visualization
- Browser-compatible rendering for WASM deployment
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import plotly.graph_objects as go


if TYPE_CHECKING:
    from build123d.topology import Part


def extract_mesh_data(part: Part) -> tuple[np.ndarray, np.ndarray]:
    """Extract mesh vertices and triangles from a Build123d Part.

    Args:
        part: Build123d Part object to extract mesh from.

    Returns:
        Tuple of (vertices, triangles) where:
        - vertices: numpy array of shape (n, 3) with vertex coordinates
        - triangles: numpy array of shape (m, 3) with triangle vertex indices

    Raises:
        ImportError: If required OCP modules are not available.
        ValueError: If the part cannot be tessellated.
    """
    # ruff: noqa: PLC0415
    from OCP.BRep import BRep_Tool
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopLoc import TopLoc_Location
    from OCP.TopoDS import TopoDS

    # Tessellate the shape with reasonable defaults
    # Deflection of 0.1 gives good quality for most CAD models
    linear_deflection = 0.1
    angular_deflection = 0.1
    parallel = False
    in_parallel = True
    mesh = BRepMesh_IncrementalMesh(
        part.wrapped,
        linear_deflection,
        parallel,
        angular_deflection,
        in_parallel,
    )
    mesh.Perform()

    vertices = []
    triangles = []
    vertex_offset = 0

    # Explore all faces in the part
    explorer = TopExp_Explorer(part.wrapped, TopAbs_FACE)
    while explorer.More():
        face_shape = explorer.Current()
        face = TopoDS.Face_s(face_shape)

        location = TopLoc_Location()
        triangulation = BRep_Tool.Triangulation_s(face, location)

        if triangulation:
            trsf = location.Transformation()

            # Extract vertices from this face
            for i in range(1, triangulation.NbNodes() + 1):
                node = triangulation.Node(i)
                node.Transform(trsf)
                vertices.append([node.X(), node.Y(), node.Z()])

            # Extract triangles from this face
            for i in range(1, triangulation.NbTriangles() + 1):
                triangle = triangulation.Triangle(i)
                n1, n2, n3 = triangle.Get()
                # Convert from 1-based to 0-based indexing and add offset
                triangles.append([
                    n1 - 1 + vertex_offset,
                    n2 - 1 + vertex_offset,
                    n3 - 1 + vertex_offset,
                ])

            vertex_offset += triangulation.NbNodes()

        explorer.Next()

    if not vertices:
        msg = "No mesh data could be extracted from the part"
        raise ValueError(msg)

    return np.array(vertices), np.array(triangles)


def create_plotly_figure(
    part: Part,
    *,
    color: str = "lightblue",
    opacity: float = 0.9,
    title: str | None = None,
    show_edges: bool = True,
) -> go.Figure:
    """Create a Plotly 3D mesh figure from a Build123d Part.

    Args:
        part: Build123d Part object to visualize.
        color: Color for the mesh (default: 'lightblue').
        opacity: Opacity of the mesh, 0-1 (default: 0.9).
        title: Optional title for the figure.
        show_edges: Whether to show mesh edges (default: True).

    Returns:
        Plotly Figure object ready to display.

    Raises:
        ImportError: If Plotly or required dependencies are not available.
        ValueError: If the part cannot be visualized.
    """
    # Extract mesh data
    vertices, triangles = extract_mesh_data(part)

    # Create Plotly mesh
    mesh_trace = go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=triangles[:, 0],
        j=triangles[:, 1],
        k=triangles[:, 2],
        color=color,
        opacity=opacity,
        flatshading=True,
        lighting={
            "ambient": 0.6,
            "diffuse": 0.8,
            "specular": 0.3,
            "roughness": 0.5,
            "fresnel": 0.2,
        },
    )

    # Optionally add edge lines for better visualization
    traces = [mesh_trace]
    if show_edges:
        # Create lines for mesh edges (simplified - show triangle edges)
        edge_x, edge_y, edge_z = [], [], []
        for tri in triangles:
            for i in range(3):
                v1 = vertices[tri[i]]
                v2 = vertices[tri[(i + 1) % 3]]
                edge_x.extend([v1[0], v2[0], None])
                edge_y.extend([v1[1], v2[1], None])
                edge_z.extend([v1[2], v2[2], None])

        edge_trace = go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode="lines",
            line={"color": "darkgray", "width": 1},
            hoverinfo="none",
            showlegend=False,
        )
        traces.append(edge_trace)

    # Create figure
    fig = go.Figure(data=traces)

    # Update layout for better 3D viewing
    fig.update_layout(
        scene={
            "xaxis": {"title": "X", "backgroundcolor": "white", "gridcolor": "lightgray"},
            "yaxis": {"title": "Y", "backgroundcolor": "white", "gridcolor": "lightgray"},
            "zaxis": {"title": "Z", "backgroundcolor": "white", "gridcolor": "lightgray"},
            "aspectmode": "data",
            "camera": {
                "eye": {"x": 1.5, "y": 1.5, "z": 1.5},
                "up": {"x": 0, "y": 0, "z": 1},
            },
        },
        title=title or "3D Model",
        showlegend=False,
        hovermode="closest",
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
    )

    return fig


def create_multi_part_figure(
    parts: list[tuple[Part, str]],
    *,
    opacity: float = 0.9,
    title: str | None = None,
) -> go.Figure:
    """Create a Plotly figure with multiple parts in different colors.

    Args:
        parts: List of (part, color) tuples to visualize together.
        opacity: Opacity for all parts, 0-1 (default: 0.9).
        title: Optional title for the figure.

    Returns:
        Plotly Figure object with all parts.

    Raises:
        ValueError: If parts list is empty or invalid.
    """
    if not parts:
        msg = "At least one part must be provided"
        raise ValueError(msg)

    traces = []

    for part, color in parts:
        vertices, triangles = extract_mesh_data(part)

        mesh_trace = go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=triangles[:, 0],
            j=triangles[:, 1],
            k=triangles[:, 2],
            color=color,
            opacity=opacity,
            flatshading=True,
            lighting={
                "ambient": 0.6,
                "diffuse": 0.8,
                "specular": 0.3,
                "roughness": 0.5,
                "fresnel": 0.2,
            },
        )
        traces.append(mesh_trace)

    fig = go.Figure(data=traces)

    fig.update_layout(
        scene={
            "xaxis": {"title": "X", "backgroundcolor": "white", "gridcolor": "lightgray"},
            "yaxis": {"title": "Y", "backgroundcolor": "white", "gridcolor": "lightgray"},
            "zaxis": {"title": "Z", "backgroundcolor": "white", "gridcolor": "lightgray"},
            "aspectmode": "data",
            "camera": {
                "eye": {"x": 1.5, "y": 1.5, "z": 1.5},
                "up": {"x": 0, "y": 0, "z": 1},
            },
        },
        title=title or "3D Assembly",
        showlegend=False,
        hovermode="closest",
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
    )

    return fig
