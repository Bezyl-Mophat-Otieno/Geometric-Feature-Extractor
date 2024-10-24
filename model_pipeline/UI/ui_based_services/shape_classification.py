import numpy as np
import trimesh
import json
import open3d as o3d
import pyvista as pv


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


def process_mesh(file_path):
    mesh = trimesh.load(file_path)
    vertices = mesh.vertices
    faces = mesh.faces
    print(f"Loaded mesh with {len(vertices)} vertices and {len(faces)} faces")

    shapes = [{'faces': [i]} for i in range(len(faces))]
    shapes = refine_shapes(shapes, vertices, faces)
    
    
    return shapes

# Load the mesh and visualize it
def visualize_mesh(file_path):
    model_mesh = trimesh.load(file_path)
    pv_mesh = pv.wrap(model_mesh)
    plotter = pv.Plotter()
    plotter.add_mesh(pv_mesh)
    plotter.show()

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

import streamlit as st
import pandas as pd

def shape_statistics_table(shapes):
    # Calculate shape counts
    shape_counts = {
        'cylinder': sum(1 for s in shapes if s['shape'] == 'cylinder'),
        'square': sum(1 for s in shapes if s['shape'] == 'square'),
        'rectangle': sum(1 for s in shapes if s['shape'] == 'rectangle'),
        'circle': sum(1 for s in shapes if s['shape'] == 'circle'),
        'triangle': sum(1 for s in shapes if s['shape'] == 'triangle')
    }
    
    # Convert to a DataFrame for better display
    shape_df = pd.DataFrame(list(shape_counts.items()), columns=['Shape Type', 'Count'])
    
    # Display table in Streamlit
    st.dataframe(shape_df)

