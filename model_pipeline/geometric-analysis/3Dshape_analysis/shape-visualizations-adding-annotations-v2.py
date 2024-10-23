import pyvista as pv
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
    faces = mesh.faces.reshape(-1, 3)  # Ensure faces are correctly shaped

    # PyVista expects faces to be formatted as [n, v0, v1, ..., vn, n, v0, v1, ..., vn, ...]
    # Where n is the number of points in the face
    face_indices = np.hstack([[3] + list(face) for face in faces])

    # Create a PyVista mesh object
    pyvista_mesh = pv.PolyData(points, face_indices)

    # Create a PyVista plotter object
    plotter = pv.Plotter()

    annotation = None  # Variable to store the annotation text

    def hover_callback(mesh, idx):
        nonlocal annotation  # Declare annotation as nonlocal to modify it
        if annotation:
            plotter.remove_actor(annotation)  # Remove the previous annotation
        if idx < 0:
            return
        face = faces[idx]
        edge_lengths = calculate_edge_lengths(points, face)
        annotation_text = ", ".join(f"Edge {i+1}: {length:.2f}" for i, length in enumerate(edge_lengths))
        annotation = plotter.add_text(annotation_text, position='lower_left', font_size=10, color='black')
        plotter.render()

    plotter.add_mesh(pyvista_mesh, show_edges=True, color='lightblue', pickable=True)
    plotter.enable_point_picking(callback=hover_callback, show_message=True, use_mesh=True)

    # Show plot
    plotter.show()

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-3-digits.stl'
    visualize_mesh_with_annotations(model_path)
