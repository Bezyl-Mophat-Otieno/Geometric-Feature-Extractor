import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap



def process_mesh(file_path):
    # Load the mesh
    mesh = trimesh.load(file_path)
    
    # Extract vertices and faces
    vertices = mesh.vertices
    faces = mesh.faces
    print(f"Loaded mesh with {len(vertices)} vertices and {len(faces)} faces")

    # Compute surface normals
    mesh.face_normals
    print(f"Computed surface normals for {len(mesh.face_normals)} faces")

    # Estimate mean curvatures (simplified approach)
    estimated_mean_curvatures = np.linalg.norm(mesh.face_normals, axis=1)
    print(f"Estimated mean curvatures for {len(estimated_mean_curvatures)} faces")

    # Define a colormap for curvature values
    cmap = plt.cm.jet  # Example colormap, choose one that suits your visualization needs
    norm = Normalize(vmin=np.min(estimated_mean_curvatures), vmax=np.max(estimated_mean_curvatures))
    colormap = LinearSegmentedColormap.from_list("my_colormap", cmap(np.linspace(0, 1, 256)))

    # Map mean curvatures to colors
    face_colors = colormap(norm(estimated_mean_curvatures))

    # Set face colors in RGBA format
    mesh.visual.face_colors = (face_colors[:, :3] * 255).astype(np.uint8)

    # Optionally, visualize the mesh
    mesh.show()

if __name__ == "__main__":
    # Replace with the path to your 3D model file
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-2-digits.stl'

    process_mesh(model_path)
