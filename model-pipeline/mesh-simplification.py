# mesh_simplification.py

import open3d as o3d
from load_view_model import load_and_display_model
import os

def simplify_mesh(mesh, target_number_of_triangles=1000):
    simplified_mesh = mesh.simplify_quadric_decimation(target_number_of_triangles)
    
    if not simplified_mesh.is_empty():
        print(f"Mesh simplified to {len(simplified_mesh.triangles)} triangles")
    else:
        print("Mesh simplification failed")

    return simplified_mesh

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-2-digits.stl'
    output_dir = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output'
    output_path = os.path.join(output_dir, 'axis-2-digits-simplified-mesh.stl')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    mesh = o3d.io.read_triangle_mesh(model_path)
    mesh.compute_vertex_normals()
    simplified_mesh = simplify_mesh(mesh)
    
    # Save the simplified mesh as an STL file
    o3d.io.write_triangle_mesh(output_path, simplified_mesh)
    
    # Visualization
    load_and_display_model(output_path)
