import trimesh
import numpy as np
import pyvista as pv

def load_mesh(model_path):
    """
    Load a 3D model using trimesh.
    
    Parameters:
        model_path (str): Path to the model file.
        
    Returns:
        trimesh.Trimesh: Loaded 3D model.
    """
    mesh = trimesh.load(model_path)
    return mesh

def calculate_edge_lengths(vertices, face):
    """
    Calculate the edge lengths of a face.
    
    Parameters:
        vertices (numpy.ndarray): Vertices of the mesh.
        face (list): Indices of the face's vertices.
        
    Returns:
        list: Edge lengths of the face.
    """
    face_vertices = vertices[face]
    edge_lengths = [np.linalg.norm(face_vertices[i] - face_vertices[(i+1) % len(face_vertices)]) for i in range(len(face_vertices))]
    return edge_lengths

def visualize_mesh_with_annotations(mesh):
    """
    Visualize a 3D mesh with annotations for edge lengths on hover.
    
    Parameters:
        mesh (trimesh.Trimesh): Loaded 3D model.
    """
    points = mesh.vertices
    faces = mesh.faces.reshape(-1, 3)  # Reshape faces correctly

    # PyVista expects faces formatted as [n, v0, v1, ..., vn, n, v0, v1, ..., vn, ...]
    face_indices = np.hstack([[3] + list(face) for face in faces])

    # Create a PyVista mesh object
    pyvista_mesh = pv.PolyData(points, face_indices)

    # Create a PyVista plotter object
    plotter = pv.Plotter()

    annotation = None  # Variable to store the annotation text

    def hover_callback(mesh, idx):
        nonlocal annotation  # Declare annotation as nonlocal to modify it
        if annotation:
            plotter.remove_actor(annotation)  # Remove previous annotation
        if idx < 0:
            return
        face = faces[idx]
        edge_lengths = calculate_edge_lengths(points, face)
        annotation_text = ", ".join(f"Edge {i+1}: {length:.2f}" for i, length in enumerate(edge_lengths))
        annotation = plotter.add_text(annotation_text, position='lower_left', font_size=10, color='black')
        plotter.render()

    plotter.add_mesh(pyvista_mesh, show_edges=True, color='lightblue', pickable=True)
    plotter.enable_point_picking(callback=hover_callback, show_message=True, use_mesh=True)

    # Show the plot
    plotter.show()