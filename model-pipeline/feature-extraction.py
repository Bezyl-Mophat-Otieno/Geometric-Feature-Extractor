#feature-extraction.py extracts geometric features from a 3D mesh. The script identifies shapes such as rectangles and squares from the mesh faces and calculates their dimensions. The extracted features are saved to a JSON file for further analysis or visualization.
import trimesh
import numpy as np
import json

def recognize_shapes(vertices, faces):
    shapes = []

    # Example logic to identify rectangles and squares
    for face in faces:
        face_vertices = vertices[face]
        # Simple checks to identify shapes
        if len(face) == 4:
            if is_square(face_vertices):
                shapes.append({"type": "Square", "dimensions": calculate_dimensions(face_vertices)})
            else:
                shapes.append({"type": "Rectangle", "dimensions": calculate_dimensions(face_vertices)})


    return shapes

def is_square(face_vertices):
    # Check if the vertices form a square (simple distance checks)
    return np.isclose(np.linalg.norm(face_vertices[0] - face_vertices[1]), 
                       np.linalg.norm(face_vertices[1] - face_vertices[2])) and \
           np.isclose(np.linalg.norm(face_vertices[1] - face_vertices[2]), 
                       np.linalg.norm(face_vertices[2] - face_vertices[3]))

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

    # Recognize shapes
    recognized_shapes = recognize_shapes(vertices, faces)

    # Prepare features dictionary
    features = {
        "vertices": vertices.tolist(),
        "faces": faces.tolist(),
        "curvatures": estimated_mean_curvatures.tolist(),
        "shapes": recognized_shapes
    }

    return features

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\wheel-digit-9.stl'
    features = process_mesh(model_path)

    # Save features to a JSON file
    output_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\extracted_features.json'
    with open(output_path, 'w') as json_file:
        json.dump(features, json_file, indent=4)

    print(f"Extracted features saved to {output_path}")
