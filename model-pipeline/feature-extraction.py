#feature-extraction.py extracts geometric features from a 3D mesh. The script identifies shapes such as rectangles and squares from the mesh faces and calculates their dimensions. The extracted features are saved to a JSON file for further analysis or visualization.
import trimesh
import numpy as np
import json


def calculate_dimensions(face_vertices):
    # Calculate dimensions of the shape
    length = np.linalg.norm(face_vertices[0] - face_vertices[1])
    width = np.linalg.norm(face_vertices[1] - face_vertices[2])
    return {"length": length, "width": width}

def process_mesh(file_path):
    # Load the mesh
    mesh = trimesh.load(file_path)
    vertices = mesh.vertices
    faces = mesh.faces
    estimated_mean_curvatures = np.linalg.norm(mesh.face_normals, axis=1)


    # Prepare features dictionary
    features = {
        "vertices": vertices.tolist(),
        "faces": faces.tolist(),
        "edges": mesh.edges.tolist(),
        "curvatures": estimated_mean_curvatures.tolist(),
    }

    return features

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\custom-shared.stl'
    features = process_mesh(model_path)

    # Save features to a JSON file
    output_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\statistics\extracted_features.json'
    with open(output_path, 'w') as json_file:
        json.dump(features, json_file, indent=4)

    print(f"Extracted features saved to {output_path}")
