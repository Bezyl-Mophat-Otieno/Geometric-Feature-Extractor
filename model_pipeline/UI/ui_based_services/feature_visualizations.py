# This script visualizes the extracted features from a 3D mesh model.

import json
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.colors import Normalize, LinearSegmentedColormap


def load_features(json_path):
    """Load extracted features from a JSON file."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def visualize_curvature_distribution(curvatures):
    """Create a histogram of curvature distribution and return the plot."""
    fig, ax = plt.subplots()
    ax.hist(curvatures, bins=50, color='blue', alpha=0.7)
    ax.set_title('Curvature Distribution')
    ax.set_xlabel('Curvature')
    ax.set_ylabel('Frequency')
    return fig

def visualize_mesh_with_curvature(mesh_path, curvatures):
    """Visualize the 3D mesh with curvature values highlighted."""
    # Load the mesh
    mesh = trimesh.load(mesh_path)
    
    # Define a colormap for curvature values
    cmap = plt.cm.jet
    norm = Normalize(vmin=np.min(curvatures), vmax=np.max(curvatures))
    colormap = LinearSegmentedColormap.from_list("my_colormap", cmap(np.linspace(0, 1, 256)))
    
    # Map mean curvatures to colors
    face_colors = colormap(norm(curvatures))
    
    # Set face colors in RGBA format
    mesh.visual.face_colors = (face_colors[:, :3] * 255).astype(np.uint8)
    
    # Return the mesh object for visualization
    return mesh