# normalize_model_trimesh.py normalizes a mesh by centering it and scaling it to fit within a unit cube. The normalized mesh is saved as an STL file and displayed in a 3D viewer. The mesh normalization is done using the trimesh library. The normalized mesh is centered at the origin and scaled to fit within a unit cube. This ensures that the mesh is in a consistent and standardized form for further processing or analysis.
import trimesh
import numpy as np
import os

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
    output_dir = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output'
    output_path = os.path.join(output_dir, 'axis-2-digits-normalized-mesh.stl')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print("Loading mesh")
    mesh = trimesh.load(model_path)
    print("Mesh loaded")
    
    normalized_mesh = normalize_mesh(mesh)
    
    # Save the normalized mesh as an STL file
    normalized_mesh.export(output_path, file_type='stl')
    print(f"Normalized mesh saved to {output_path}")
    
    print("Displaying normalized mesh")
    normalized_mesh.show()
