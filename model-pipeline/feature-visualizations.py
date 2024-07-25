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

def visualize_curvature_distribution(curvatures, output_path):
    """Create a histogram of curvature distribution."""
    plt.hist(curvatures, bins=50, color='blue', alpha=0.7)
    plt.title('Curvature Distribution')
    plt.xlabel('Curvature')
    plt.ylabel('Frequency')
    plt.savefig(output_path)
    plt.close()
    print(f"Curvature distribution saved to {output_path}")

def visualize_mesh_with_curvature(mesh_path, curvatures, output_path):
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
    
    # Save the visualized mesh
    mesh.export(output_path)
    print(f"Mesh with curvature visualization saved to {output_path}")
    
    # Optionally, visualize the mesh interactively
    mesh.show()

    # Plotting color bar for curvature values
    plt.figure(figsize=(6, 2))
    plt.title("Curvature Color Mapping")
    plt.imshow([np.arange(len(face_colors))], aspect='auto', cmap=colormap, norm=norm)
    plt.colorbar(label='Curvature Value')
    plt.xlabel('Curvature Color Mapping')
    plt.yticks([])  # Hide y-axis ticks
    plt.savefig(f"{output_path}_colorbar.png", bbox_inches='tight')  # Save colorbar
    plt.show()

if __name__ == "__main__":
    # Paths to input files
    features_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\extracted_features.json'
    normalized_mesh_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\wheel-digit-5.stl'
    
    # Paths to output files
    curvature_histogram_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\curvature_histogram.png'
    mesh_with_curvature_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\mesh_with_curvature.stl'

    # Load extracted features
    features = load_features(features_path)
    
    # Extract curvatures from loaded features
    curvatures = np.array(features['curvatures'])
    
    # Visualize curvature distribution
    visualize_curvature_distribution(curvatures, curvature_histogram_path)
    
    # Visualize mesh with curvature
    visualize_mesh_with_curvature(normalized_mesh_path, curvatures, mesh_with_curvature_path)
