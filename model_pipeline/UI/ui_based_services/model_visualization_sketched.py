import streamlit as st
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

def load_model(file_path):
    """
    Load the model using Open3D.
    
    Parameters:
        file_path (str): Path to the STL model file.
        
    Returns:
        open3d.geometry.TriangleMesh: Loaded 3D model.
    """
    mesh = o3d.io.read_triangle_mesh(file_path)
    return mesh

def create_hand_drawn_effect(mesh):
    """
    Create a hand-drawn style effect for the 3D model with dashed edges.
    
    Parameters:
        mesh (open3d.geometry.TriangleMesh): Loaded 3D model.
    """
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.triangles)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot dashed edges for each face
    for face in faces:
        for i in range(3):
            start = vertices[face[i]]
            end = vertices[face[(i + 1) % 3]]
            line = np.vstack([start, end])
            ax.plot(line[:, 0], line[:, 1], line[:, 2], c='k', linestyle='--')

    # Label axes
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    # Show plot
    plt.show()

def draw_dimensions(vertices, faces, ax):
    """
    Draw the dimensions on the edges of the model by calculating edge lengths.
    
    Parameters:
        vertices (numpy.ndarray): Vertices of the mesh.
        faces (numpy.ndarray): Faces (triangles) of the mesh.
        ax (Axes3D): The matplotlib 3D axis to draw the dimensions on.
    """
    for face in faces:
        for i in range(3):
            start = vertices[face[i]]
            end = vertices[face[(i + 1) % 3]]
            mid_point = (start + end) / 2
            ax.text(mid_point[0], mid_point[1], mid_point[2], f'{np.linalg.norm(end - start):.2f}', color='red')