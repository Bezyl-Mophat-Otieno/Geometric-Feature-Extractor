# normalize_model_trimesh.py

import trimesh
import numpy as np

def normalize_mesh(mesh):
    # Center the mesh
    mesh.apply_translation(-mesh.centroid)
    
    # Scale the mesh to fit within a unit cube
    scale_factor = 1.0 / np.max(mesh.bounds[1] - mesh.bounds[0])
    mesh.apply_scale(scale_factor)
    
    print("Mesh normalized successfully")
    return mesh

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-2-digits.stl'
    print("Loading mesh")
    mesh = trimesh.load(model_path)
    print("Mesh loaded")
    normalized_mesh = normalize_mesh(mesh)
    print("Displaying normalized mesh")
    normalized_mesh.show()
