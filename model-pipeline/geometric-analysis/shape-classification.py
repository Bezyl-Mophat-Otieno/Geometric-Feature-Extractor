import numpy as np
import trimesh
import json
import open3d as o3d

def is_cylinder(vertices, threshold=0.1):
    bounds = np.ptp(vertices, axis=0)
    height = bounds[2]
    radius = np.mean(bounds[:2]) / 2
    return height > radius * threshold

def is_rectangle(vertices, threshold=0.1):
    if len(vertices) != 4:
        return False
    edges = np.linalg.norm(np.diff(vertices, axis=0), axis=1)
    return np.allclose(edges[0], edges[2], rtol=threshold) and np.allclose(edges[1], edges[3], rtol=threshold)

def is_square(vertices, threshold=0.1):
    if not is_rectangle(vertices, threshold):
        return False
    edges = np.linalg.norm(np.diff(vertices, axis=0), axis=1)
    return np.allclose(edges[0], edges[1], rtol=threshold)

def is_circle(vertices, threshold=0.1):
    center = np.mean(vertices, axis=0)
    distances = np.linalg.norm(vertices - center, axis=1)
    return np.allclose(distances, distances[0], rtol=threshold)

def refine_shapes(shapes, vertices, faces):
    refined_shapes = []

    for shape in shapes:
        face_indices = shape['faces']
        face_vertices = vertices[np.unique(faces[face_indices])]

        if is_cylinder(face_vertices):
            refined_shapes.append({
                'shape': 'cylinder',
                'vertices': face_vertices.tolist(),
                'dimensions': {'height': np.ptp(face_vertices[:, 2]), 'radius': np.mean(np.ptp(face_vertices[:, :2], axis=0))}
            })
        elif is_square(face_vertices):
            refined_shapes.append({
                'shape': 'square',
                'vertices': face_vertices.tolist(),
                'dimensions': {'side_length': np.ptp(face_vertices[:, 0])}
            })
        elif is_rectangle(face_vertices):
            refined_shapes.append({
                'shape': 'rectangle',
                'vertices': face_vertices.tolist(),
                'dimensions': {'width': np.ptp(face_vertices[:, 0]), 'height': np.ptp(face_vertices[:, 1])}
            })
        elif is_circle(face_vertices):
            refined_shapes.append({
                'shape': 'circle',
                'vertices': face_vertices.tolist(),
                'dimensions': {'radius': np.mean(np.linalg.norm(face_vertices - np.mean(face_vertices, axis=0), axis=1))}
            })
        else:
            refined_shapes.append({
                'shape': 'triangle',
                'vertices': face_vertices.tolist()
            })

    return refined_shapes

def process_mesh(file_path):
    mesh = trimesh.load(file_path)
    vertices = mesh.vertices
    faces = mesh.faces
    print(f"Loaded mesh with {len(vertices)} vertices and {len(faces)} faces")

    shapes = [{'faces': [i]} for i in range(len(faces))]
    shapes = refine_shapes(shapes, vertices, faces)
    
    # Define color mapping
    color_mapping = {
        'cylinder': [1, 0, 0],  # Red
        'square': [0, 1, 0],  # Green
        'rectangle': [0, 0, 1],  # Blue
        'circle': [1, 1, 0],  # Yellow
        'triangle': [0, 1, 1]  # Cyan
    }

# Corrected part of the process_mesh function
    for face_index, shape_info in enumerate(shapes):
            face_color = color_mapping.get(shape_info['shape'], [0, 0, 0])  # Default to black if no match
            # Ensure face_color is a 3-element tuple
            if isinstance(face_color, list):
                face_color = tuple(face_color)
                print(face_color)
            # Set the face color for the current face
            mesh.visual.face_colors[face_index] = face_color


    # Save the colored mesh to a .ply file
    colored_model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\colored_mesh.ply'
    o3d.io.write_triangle_mesh(colored_model_path, mesh)

    return shapes, mesh

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-2-digits.stl'
    shapes, mesh = process_mesh(model_path)
    output_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\classified_shapes.json'

    with open(output_path, 'w') as json_file:
        json.dump(shapes, json_file, indent=4)

    # Visualize the colored mesh
    o3d.visualization.draw_geometries([mesh])

    print(f"Classified shapes saved to {output_path}")
