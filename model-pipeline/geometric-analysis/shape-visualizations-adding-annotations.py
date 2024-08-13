import plotly.graph_objects as go
import numpy as np
import trimesh

def load_mesh(model_path):
    mesh = trimesh.load(model_path)
    return mesh

def calculate_face_dimensions(vertices, face):
    face_vertices = vertices[face]
    edges = [np.linalg.norm(face_vertices[i] - face_vertices[(i+1) % len(face_vertices)]) for i in range(len(face_vertices))]
    dimensions = {
        'width': edges[0],
        'height': edges[1] if len(edges) > 1 else edges[0],
    }
    return dimensions

def create_hover_template(face_dimensions):
    return f"Width: {face_dimensions['width']:.2f}<br>Height: {face_dimensions['height']:.2f}"

def visualize_mesh_with_face_annotations(model_path):
    mesh = load_mesh(model_path)
    points = mesh.vertices
    faces = mesh.faces

    # Create face dimension annotations
    face_x = []
    face_y = []
    face_z = []
    face_texts = []

    for face in faces:
        face_vertices = points[face]
        dimensions = calculate_face_dimensions(points, face)
        centroid = face_vertices.mean(axis=0)
        face_x.append(centroid[0])
        face_y.append(centroid[1])
        face_z.append(centroid[2])
        face_texts.append(create_hover_template(dimensions))

    # Generate a color array for the points (e.g., a gradient based on z-coordinate)
    colors = points[:, 2]  # Example: color based on the z-coordinate

    # Create the figure
    fig = go.Figure()

    # Add faces as mesh3d trace
    fig.add_trace(go.Mesh3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        opacity=0.5,
        hoverinfo='text',
        hovertext=face_texts,
        colorscale='Blues',
        showscale=False
    ))

    # Add vertices as scatter3d with color
    fig.add_trace(go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode='markers',
        marker=dict(size=4, color=colors, colorscale='Viridis', colorbar=dict(title='Z Coordinate')),
        showlegend=False
    ))

    # Update layout
    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ))

    fig.show()

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\custom-shared.stl'
    visualize_mesh_with_face_annotations(model_path)
