import plotly.graph_objects as go
import numpy as np
import trimesh

def load_mesh(model_path):
    mesh = trimesh.load(model_path)
    return mesh

def calculate_edge_lengths(vertices, face):
    face_vertices = vertices[face]
    edge_lengths = [np.linalg.norm(face_vertices[i] - face_vertices[(i+1) % len(face_vertices)]) for i in range(len(face_vertices))]
    return edge_lengths

def visualize_mesh_with_annotations(model_path):
    mesh = load_mesh(model_path)
    points = mesh.vertices
    faces = mesh.faces

    # Create a Plotly scatter3d trace for edges
    edge_lines = []
    for face in faces:
        face_vertices = points[face]
        for i in range(len(face_vertices)):
            start = face_vertices[i]
            end = face_vertices[(i + 1) % len(face_vertices)]
            edge_lines.append([start, end])

    # Convert edge lines to separate x, y, z lists for plotting
    edge_x = []
    edge_y = []
    edge_z = []
    for line in edge_lines:
        edge_x.extend([line[0][0], line[1][0], None])
        edge_y.extend([line[0][1], line[1][1], None])
        edge_z.extend([line[0][2], line[1][2], None])

    # Create the figure
    fig = go.Figure()

    # Add edges as scatter3d with black lines for sketch appearance
    fig.add_trace(go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode='lines',
        line=dict(color='black', width=2),
        showlegend=False
    ))

    # Add points for vertices (optional)
    fig.add_trace(go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode='markers',
        marker=dict(size=4, color='black'),
        showlegend=False
    ))

    # Create annotations
    annotations = []
    for i, face in enumerate(faces):
        face_vertices = points[face]
        edge_lengths = calculate_edge_lengths(points, face)
        centroid = face_vertices.mean(axis=0)
        annotation_text = ", ".join(f"Edge {i+1}: {length:.2f}" for i, length in enumerate(edge_lengths))
        
        annotations.append(dict(
            x=centroid[0],
            y=centroid[1],
            z=centroid[2],
            text=annotation_text,
            showarrow=True,
            arrowhead=2,
            arrowcolor='black'
        ))

    # Add annotations to the figure
    for annotation in annotations:
        fig.add_trace(go.Scatter3d(
            x=[annotation['x']],
            y=[annotation['y']],
            z=[annotation['z']],
            mode='markers+text',
            marker=dict(size=4, color='black'),
            text=[annotation['text']],
            textposition='top center'
        ))

    # Update layout
    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ))

    fig.show()

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-3-digits.stl'
    visualize_mesh_with_annotations(model_path)
