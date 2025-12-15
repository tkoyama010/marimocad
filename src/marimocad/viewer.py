"""
3D Viewer component for Marimo notebooks using Plotly.
"""

from typing import Any, Dict, List, Optional, Union

import marimo as mo
import numpy as np
import plotly.graph_objects as go


class Viewer3D:
    """
    Interactive 3D visualization component for Marimo notebooks.
    
    This widget provides interactive 3D visualization with camera controls,
    multiple geometries, lighting options, and selection features.
    
    Examples:
        >>> viewer = Viewer3D()
        >>> viewer.add_box([0, 0, 0], [1, 1, 1])
        >>> viewer.add_sphere([2, 0, 0], 0.5)
        >>> viewer.show()
    """
    
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        background_color: str = "white",
    ):
        """
        Initialize the 3D viewer.
        
        Args:
            width: Width of the viewer in pixels
            height: Height of the viewer in pixels
            background_color: Background color of the viewer
        """
        self.width = width
        self.height = height
        self.background_color = background_color
        self.traces: List[Union[go.Scatter3d, go.Mesh3d]] = []
        self._selected_trace = None
        
        # Default camera and lighting settings
        self.camera = dict(
            eye=dict(x=1.5, y=1.5, z=1.5),
            center=dict(x=0, y=0, z=0),
            up=dict(x=0, y=0, z=1)
        )
        
    def add_box(
        self,
        center: List[float],
        size: List[float],
        color: str = "blue",
        opacity: float = 0.8,
        name: Optional[str] = None,
    ) -> "Viewer3D":
        """
        Add a box (cuboid) to the viewer.
        
        Args:
            center: [x, y, z] coordinates of the box center
            size: [width, height, depth] dimensions of the box
            color: Color of the box
            opacity: Opacity of the box (0-1)
            name: Optional name for the geometry
            
        Returns:
            Self for method chaining
        """
        cx, cy, cz = center
        w, h, d = size
        
        # Define the 8 vertices of the box
        x = np.array([
            cx - w/2, cx + w/2, cx + w/2, cx - w/2,
            cx - w/2, cx + w/2, cx + w/2, cx - w/2
        ])
        y = np.array([
            cy - h/2, cy - h/2, cy + h/2, cy + h/2,
            cy - h/2, cy - h/2, cy + h/2, cy + h/2
        ])
        z = np.array([
            cz - d/2, cz - d/2, cz - d/2, cz - d/2,
            cz + d/2, cz + d/2, cz + d/2, cz + d/2
        ])
        
        # Define the 12 triangles (2 per face) for the box
        # Vertex indices: 0-3 are bottom face, 4-7 are top face
        # Each face of the box is split into 2 triangles
        # Format: [i, j, k] where each triple defines a triangle
        i = [
            0, 0,   # Bottom face (z-)
            1, 1,   # Bottom face continued
            2, 2,   # Bottom face continued
            3, 3,   # Bottom face continued
            4, 4,   # Top face (z+)
            5, 5,   # Top face continued
            6, 6,   # Top face continued
            7, 7,   # Top face continued
            0, 0,   # Side faces
            1, 1,   # Side faces continued
            2, 2,   # Side faces continued
            3, 3    # Side faces continued
        ]
        j = [
            1, 3,   # Bottom triangles
            2, 0,
            3, 1,
            0, 2,
            5, 7,   # Top triangles
            6, 4,
            7, 5,
            4, 6,
            4, 1,   # Side triangles
            5, 2,
            6, 3,
            7, 0
        ]
        k = [
            2, 4,   # Bottom triangles
            3, 4,
            0, 5,
            1, 5,
            6, 0,   # Top triangles
            7, 1,
            4, 2,
            5, 3,
            5, 5,   # Side triangles
            1, 6,
            2, 7,
            3, 4
        ]
        
        mesh = go.Mesh3d(
            x=x, y=y, z=z,
            i=i, j=j, k=k,
            color=color,
            opacity=opacity,
            name=name or f"Box {len(self.traces)}",
            hoverinfo="name",
            lighting=dict(
                ambient=0.6,
                diffuse=0.8,
                specular=0.3,
                roughness=0.5,
            ),
            lightposition=dict(x=100, y=200, z=300)
        )
        
        self.traces.append(mesh)
        return self
        
    def add_sphere(
        self,
        center: List[float],
        radius: float,
        color: str = "red",
        opacity: float = 0.8,
        resolution: int = 20,
        name: Optional[str] = None,
    ) -> "Viewer3D":
        """
        Add a sphere to the viewer.
        
        Args:
            center: [x, y, z] coordinates of the sphere center
            radius: Radius of the sphere
            color: Color of the sphere
            opacity: Opacity of the sphere (0-1)
            resolution: Number of points used to approximate the sphere
            name: Optional name for the geometry
            
        Returns:
            Self for method chaining
        """
        cx, cy, cz = center
        
        # Create sphere using parametric equations
        theta = np.linspace(0, 2 * np.pi, resolution)
        phi = np.linspace(0, np.pi, resolution)
        theta, phi = np.meshgrid(theta, phi)
        
        x = cx + radius * np.sin(phi) * np.cos(theta)
        y = cy + radius * np.sin(phi) * np.sin(theta)
        z = cz + radius * np.cos(phi)
        
        # Flatten the arrays for Mesh3d
        x_flat = x.flatten()
        y_flat = y.flatten()
        z_flat = z.flatten()
        
        # Create triangulation
        n = resolution
        i, j, k = [], [], []
        for row in range(n - 1):
            for col in range(n - 1):
                idx = row * n + col
                # First triangle
                i.append(idx)
                j.append(idx + 1)
                k.append(idx + n)
                # Second triangle
                i.append(idx + 1)
                j.append(idx + n + 1)
                k.append(idx + n)
        
        mesh = go.Mesh3d(
            x=x_flat, y=y_flat, z=z_flat,
            i=i, j=j, k=k,
            color=color,
            opacity=opacity,
            name=name or f"Sphere {len(self.traces)}",
            hoverinfo="name",
            lighting=dict(
                ambient=0.6,
                diffuse=0.8,
                specular=0.3,
                roughness=0.5,
            ),
            lightposition=dict(x=100, y=200, z=300)
        )
        
        self.traces.append(mesh)
        return self
        
    def add_cylinder(
        self,
        center: List[float],
        radius: float,
        height: float,
        color: str = "green",
        opacity: float = 0.8,
        resolution: int = 20,
        name: Optional[str] = None,
    ) -> "Viewer3D":
        """
        Add a cylinder to the viewer.
        
        Args:
            center: [x, y, z] coordinates of the cylinder center
            radius: Radius of the cylinder
            height: Height of the cylinder (along z-axis)
            color: Color of the cylinder
            opacity: Opacity of the cylinder (0-1)
            resolution: Number of points around the circumference
            name: Optional name for the geometry
            
        Returns:
            Self for method chaining
        """
        cx, cy, cz = center
        
        # Create cylinder vertices
        theta = np.linspace(0, 2 * np.pi, resolution)
        z_vals = np.array([cz - height/2, cz + height/2])
        
        x = []
        y = []
        z = []
        
        # Bottom and top circles
        for z_val in z_vals:
            for t in theta:
                x.append(cx + radius * np.cos(t))
                y.append(cy + radius * np.sin(t))
                z.append(z_val)
        
        # Add center points for caps
        x.extend([cx, cx])
        y.extend([cy, cy])
        z.extend([cz - height/2, cz + height/2])
        
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        
        # Create triangulation
        i, j, k = [], [], []
        n = resolution
        
        # Side faces
        for idx in range(n - 1):
            # Triangle 1
            i.append(idx)
            j.append(idx + 1)
            k.append(idx + n)
            # Triangle 2
            i.append(idx + 1)
            j.append(idx + n + 1)
            k.append(idx + n)
        
        # Connect last to first
        i.append(n - 1)
        j.append(0)
        k.append(2*n - 1)
        
        i.append(0)
        j.append(n)
        k.append(2*n - 1)
        
        # Bottom cap
        bottom_center = 2 * n
        for idx in range(n - 1):
            i.append(bottom_center)
            j.append(idx)
            k.append(idx + 1)
        i.append(bottom_center)
        j.append(n - 1)
        k.append(0)
        
        # Top cap
        top_center = 2 * n + 1
        for idx in range(n, 2*n - 1):
            i.append(top_center)
            j.append(idx + 1)
            k.append(idx)
        i.append(top_center)
        j.append(n)
        k.append(2*n - 1)
        
        mesh = go.Mesh3d(
            x=x, y=y, z=z,
            i=i, j=j, k=k,
            color=color,
            opacity=opacity,
            name=name or f"Cylinder {len(self.traces)}",
            hoverinfo="name",
            lighting=dict(
                ambient=0.6,
                diffuse=0.8,
                specular=0.3,
                roughness=0.5,
            ),
            lightposition=dict(x=100, y=200, z=300)
        )
        
        self.traces.append(mesh)
        return self
        
    def add_mesh(
        self,
        vertices: np.ndarray,
        faces: np.ndarray,
        color: str = "purple",
        opacity: float = 0.8,
        name: Optional[str] = None,
    ) -> "Viewer3D":
        """
        Add a custom mesh to the viewer.
        
        Args:
            vertices: Nx3 array of vertex coordinates
            faces: Mx3 array of face indices
            color: Color of the mesh
            opacity: Opacity of the mesh (0-1)
            name: Optional name for the geometry
            
        Returns:
            Self for method chaining
        """
        mesh = go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=faces[:, 0],
            j=faces[:, 1],
            k=faces[:, 2],
            color=color,
            opacity=opacity,
            name=name or f"Mesh {len(self.traces)}",
            hoverinfo="name",
            lighting=dict(
                ambient=0.6,
                diffuse=0.8,
                specular=0.3,
                roughness=0.5,
            ),
            lightposition=dict(x=100, y=200, z=300)
        )
        
        self.traces.append(mesh)
        return self
        
    def set_camera(
        self,
        eye: Optional[Dict[str, float]] = None,
        center: Optional[Dict[str, float]] = None,
        up: Optional[Dict[str, float]] = None,
    ) -> "Viewer3D":
        """
        Set the camera position and orientation.
        
        Args:
            eye: Camera position as dict with x, y, z keys
            center: Point the camera is looking at
            up: Up direction vector
            
        Returns:
            Self for method chaining
        """
        if eye is not None:
            self.camera['eye'] = eye
        if center is not None:
            self.camera['center'] = center
        if up is not None:
            self.camera['up'] = up
        return self
        
    def clear(self) -> "Viewer3D":
        """
        Clear all geometries from the viewer.
        
        Returns:
            Self for method chaining
        """
        self.traces = []
        return self
        
    def show(self) -> Any:
        """
        Display the 3D viewer in a Marimo notebook.
        
        Returns:
            Marimo UI element displaying the 3D visualization
        """
        fig = go.Figure(data=self.traces)
        
        fig.update_layout(
            width=self.width,
            height=self.height,
            scene=dict(
                xaxis=dict(
                    title="X",
                    gridcolor="rgb(200, 200, 200)",
                    showbackground=True,
                    backgroundcolor=self.background_color,
                ),
                yaxis=dict(
                    title="Y",
                    gridcolor="rgb(200, 200, 200)",
                    showbackground=True,
                    backgroundcolor=self.background_color,
                ),
                zaxis=dict(
                    title="Z",
                    gridcolor="rgb(200, 200, 200)",
                    showbackground=True,
                    backgroundcolor=self.background_color,
                ),
                camera=self.camera,
                aspectmode='cube',
            ),
            paper_bgcolor=self.background_color,
            plot_bgcolor=self.background_color,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor="rgba(255, 255, 255, 0.8)",
            ),
            hovermode='closest',
        )
        
        # Enable interactive controls
        fig.update_scenes(
            xaxis_showspikes=False,
            yaxis_showspikes=False,
            zaxis_showspikes=False,
        )
        
        # Return as Marimo HTML element
        html = fig.to_html(
            include_plotlyjs='cdn',
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['toImage'],
                'scrollZoom': True,
            }
        )
        
        return mo.Html(html)
        
    def to_figure(self) -> go.Figure:
        """
        Get the underlying Plotly figure object.
        
        Returns:
            Plotly Figure object
        """
        fig = go.Figure(data=self.traces)
        
        fig.update_layout(
            width=self.width,
            height=self.height,
            scene=dict(
                xaxis=dict(title="X"),
                yaxis=dict(title="Y"),
                zaxis=dict(title="Z"),
                camera=self.camera,
                aspectmode='cube',
            ),
            showlegend=True,
        )
        
        return fig
