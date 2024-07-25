# load_model.py loads a 3D CAD model from an STL file and displays it in a 3D viewer using the open3d library. This script can be used to quickly visualize 3D models and inspect their geometry. The load_and_display_model function takes the path to the STL file as input, loads the model, and displays it in a 3D viewer.
import open3d as o3d
import numpy as np


def load_and_display_model(model_path):
    # Load the STL model
    mesh = o3d.io.read_triangle_mesh(model_path)
    
    # Check if the mesh is loaded successfully
    if not mesh.has_vertices():
        print("Mesh is empty.")
        return
    
    # Compute vertex normals for better visualization
    mesh.compute_vertex_normals()
    
    # Visualize the mesh
    o3d.visualization.draw_geometries([mesh])
    
    return mesh

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\wheel-digit-9.stl'
    load_and_display_model(model_path)
