import streamlit as st
import plotly.graph_objects as go
import numpy as np
import trimesh
import tempfile

def load_mesh(model_path):
    """
    Load a 3D mesh from a file path using trimesh.
    
    Parameters:
        model_path (str): Path to the STL model file.
        
    Returns:
        trimesh.Trimesh: Loaded mesh model.
    """
    mesh = trimesh.load(model_path)
    return mesh

def calculate_face_dimensions(vertices, face):
    """
    Calculate dimensions of a triangular face, returning width and height.
    
    Parameters:
        vertices (np.ndarray): Vertices of the mesh.
        face (np.ndarray): Indices of the vertices forming a face.
        
    Returns:
        dict: A dictionary with 'width' and 'height' of the face.
    """
    face_vertices = vertices[face]
    edges = [np.linalg.norm(face_vertices[i] - face_vertices[(i+1) % len(face_vertices)]) for i in range(len(face_vertices))]
    dimensions = {
        'width': edges[0],
        'height': edges[1] if len(edges) > 1 else edges[0],
    }
    return dimensions

def create_hover_template(face_dimensions):
    """
    Create a hover template displaying width and height.
    
    Parameters:
        face_dimensions (dict): Dictionary with 'width' and 'height'.
        
    Returns:
        str: Formatted hover text with width and height.
    """
    return f"Width: {face_dimensions['width']:.2f}<br>Height: {face_dimensions['height']:.2f}"

def visualize_mesh_with_face_annotations(mesh):
    """
    Visualize a 3D mesh with Plotly, adding face dimension annotations.
    
    Parameters:
        mesh (trimesh.Trimesh): Loaded mesh model.
    """
    points = mesh.vertices
    faces = mesh.faces

    # Create face dimension annotations
    face_x = []
    face_y = []
    face_z = []
    face_texts = []

    for face in faces:
        dimensions = calculate_face_dimensions(points, face)
        centroid = points[face].mean(axis=0)
        face_x.append(centroid[0])
        face_y.append(centroid[1])
        face_z.append(centroid[2])
        face_texts.append(create_hover_template(dimensions))

    # Color the vertices based on Z-coordinate
    colors = points[:, 2]  # Use Z-coordinate for color gradient

    # Create the Plotly figure
    fig = go.Figure()

    # Add faces as a 3D mesh with annotations
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

    # Update layout for axis titles
    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ))

    # Display the figure in Streamlit
    st.plotly_chart(fig)