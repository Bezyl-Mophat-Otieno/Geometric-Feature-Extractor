#feature-extraction.py extracts geometric features from a 3D mesh.
import trimesh
import numpy as np
import json


def calculate_dimensions(face_vertices):
    # Calculate dimensions of the shape
    length = np.linalg.norm(face_vertices[0] - face_vertices[1])
    width = np.linalg.norm(face_vertices[1] - face_vertices[2])
    return {"length": length, "width": width}

def process_mesh_features(file_path):
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

