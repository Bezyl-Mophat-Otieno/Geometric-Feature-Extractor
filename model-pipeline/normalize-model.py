# normalize_model.py

import open3d as o3d
import numpy as np

def simplify_mesh(mesh, target_reduction=0.5):
    print("Simplifying mesh")
    mesh_simplified = mesh.simplify_quadric_decimation(int(len(mesh.triangles) * target_reduction))
    print("Mesh simplified")
    return mesh_simplified

def normalize_mesh(mesh):
    # Check if mesh is not empty
    if mesh.is_empty():
        print("Mesh is empty")
        return mesh

    # Print mesh details
    print(f"Number of vertices: {len(mesh.vertices)}")
    print(f"Number of triangles: {len(mesh.triangles)}")

    # Simplify the mesh if it's too complex
    if len(mesh.triangles) > 100000:  # Adjust this threshold based on your system's capabilities
        mesh = simplify_mesh(mesh)

    print("Mesh bounds before centering:")
    print("Min bound:", mesh.get_min_bound())
    print("Max bound:", mesh.get_max_bound())

    try:
        print("Calculating center")
        center = mesh.get_center()
        print("Center:", center)

        print("Centering the mesh")
        # Center the mesh
        mesh.translate(-center)
    except Exception as e:
        print("Error during centering:", e)
    
    print("Mesh bounds after centering:")
    print("Min bound:", mesh.get_min_bound())
    print("Max bound:", mesh.get_max_bound())

    try:
        print("Scaling the mesh")
        # Scale the mesh to fit within a unit cube
        scale_factor = 1.0 / np.max(mesh.get_max_bound() - mesh.get_min_bound())
        mesh.scale(scale_factor, center=False)
    except Exception as e:
        print("Error during scaling:", e)

    print("Mesh normalized successfully")
    return mesh

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-2-digits.stl'
    print("Loading mesh")
    mesh = o3d.io.read_triangle_mesh(model_path)
    print("Mesh loaded")
    normalized_mesh = normalize_mesh(mesh)
    print("Displaying normalized mesh")
    o3d.visualization.draw_geometries([normalized_mesh])
