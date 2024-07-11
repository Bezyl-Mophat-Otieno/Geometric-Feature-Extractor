# mesh_simplification.py

import open3d as o3d

def simplify_mesh(mesh, target_number_of_triangles=1000):
    # Simplify the mesh using Quadric Edge Collapse Decimation
    simplified_mesh = mesh.simplify_quadric_decimation(target_number_of_triangles)
    
    if not simplified_mesh.is_empty():
        print(f"Mesh simplified to {len(simplified_mesh.triangles)} triangles")
    else:
        print("Mesh simplification failed")

    return simplified_mesh

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-2-digits.stl'
    mesh = o3d.io.read_triangle_mesh(model_path)
    simplified_mesh = simplify_mesh(mesh)
    o3d.visualization.draw_geometries([simplified_mesh])
