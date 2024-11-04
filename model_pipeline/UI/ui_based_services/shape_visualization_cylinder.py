import streamlit as st
import plotly.graph_objects as go
import numpy as np
import trimesh
import tempfile

def load_mesh(model_path):
    """Load a 3D mesh using trimesh."""
    mesh = trimesh.load(model_path)
    return mesh

def identify_circular_faces(mesh):
    """Identify circular faces and calculate their dimensions."""
    circular_faces = []
    for face in mesh.faces:
        face_vertices = mesh.vertices[face]
        if is_circular_face(face_vertices):
            print("Is circular face")
            center, radius = calculate_circle_properties(face_vertices)
            circular_faces.append({
                'face': face,
                'center': center,
                'radius': radius,
                'diameter': 2 * radius,
                'circumference': 2 * np.pi * radius
            })
        print
    return circular_faces

def is_circular_face(face_vertices, tolerance=1e-3):
    """Check if a face is circular based on vertex positions."""
    # Calculate the centroid of the face vertices
    center = face_vertices.mean(axis=0)

    # Calculate distances from each vertex to the center
    distances = np.linalg.norm(face_vertices - center, axis=1)

    # Check if all distances are approximately equal (within a tolerance)
    radius = distances.mean()
    if np.all(np.abs(distances - radius) < tolerance):
        return True
    return False


def calculate_circle_properties(face_vertices):
    """Calculate center and radius of a circular face."""
    center = face_vertices.mean(axis=0)
    radius = np.mean(np.linalg.norm(face_vertices - center, axis=1))
    return center, radius

def create_hover_template_circle(face_properties):
    """Create hover template for circular face dimensions."""
    return (f"Diameter: {face_properties['diameter']:.2f}<br>"
            f"Circumference: {face_properties['circumference']:.2f}")

def visualize_mesh_with_highlighted_faces(mesh, circular_faces):
    """Visualize the mesh and highlight circular faces with annotations."""
    points = mesh.vertices
    faces = mesh.faces

    # Create hover text and highlighting
    face_x, face_y, face_z, face_texts = [], [], [], []

    for face_info in circular_faces:
        face_center = face_info['center']
        face_x.append(face_center[0])
        face_y.append(face_center[1])
        face_z.append(face_center[2])
        face_texts.append(create_hover_template_circle(face_info))

    fig = go.Figure()

    # Add the main mesh
    fig.add_trace(go.Mesh3d(
        x=points[:, 0], y=points[:, 1], z=points[:, 2],
        i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
        opacity=0.5,
        colorscale='Blues',
        hoverinfo='skip'  # Skip default hover for main mesh
    ))

    # Add hoverable circular faces as scatter points with custom hover text
    fig.add_trace(go.Scatter3d(
        x=face_x, y=face_y, z=face_z,
        mode='markers',
        marker=dict(size=5, color='red'),
        text=face_texts,
        hoverinfo='text'
    ))

    # Update layout
    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ))

    st.plotly_chart(fig)

