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

    # Create a Plotly mesh object
    mesh3d = go.Mesh3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        opacity=0.5,
        colorscale='Blues'
    )

    # Create annotations
    annotations = []
    for face in faces:
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
            arrowhead=2
        ))

    # Create the figure
    fig = go.Figure(data=[mesh3d])
    for annotation in annotations:
        fig.add_trace(go.Scatter3d(
            x=[annotation['x']],
            y=[annotation['y']],
            z=[annotation['z']],
            mode='markers+text',
            marker=dict(size=4),
            text=[annotation['text']],
            textposition='top center'
        ))

    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ))

    fig.show()

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-3-digits.stl'
    visualize_mesh_with_annotations(model_path)
