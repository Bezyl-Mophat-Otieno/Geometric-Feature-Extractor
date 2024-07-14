# load_model.py

import open3d as o3d

def load_and_display_model(model_path):
    # Load the 3D CAD Model
    mesh = o3d.io.read_triangle_mesh(model_path)
    
    if not mesh.is_empty():
        print(f"Model loaded successfully from {model_path}")
    else:
        print(f"Failed to load model from {model_path}")

    # Display the model
    o3d.visualization.draw_geometries([mesh])
    
    return mesh

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\axis-2-digits-simplified-mesh.stl'
    load_and_display_model(model_path)
