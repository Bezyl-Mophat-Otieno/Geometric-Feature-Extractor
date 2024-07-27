import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.colors as mcolors



def load_model(file_path):
    # Load the model using Open3D
    mesh = o3d.io.read_triangle_mesh(file_path)
    return mesh

def create_hand_drawn_effect(mesh, output_image_path):
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.triangles)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for face in faces:
        for i in range(3):
            start = vertices[face[i]]
            end = vertices[face[(i + 1) % 3]]
            line = np.vstack([start, end])
            ax.plot(line[:, 0], line[:, 1], line[:, 2], c='k', linestyle='--')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    plt.savefig(output_image_path)
    plt.show()


def draw_dimensions(vertices, faces, ax):
    for face in faces:
        for i in range(3):
            start = vertices[face[i]]
            end = vertices[face[(i + 1) % 3]]
            mid_point = (start + end) / 2
            ax.text(mid_point[0], mid_point[1], mid_point[2], f'{np.linalg.norm(end - start):.2f}', color='red')

def create_point_cloud_from_mesh(mesh, density=10000):
    """
    Create a point cloud from a mesh by sampling points from its surface.
    
    Parameters:
        mesh (trimesh.Trimesh): The input mesh.
        density (int): Number of points to sample from the mesh surface.
        
    Returns:
        numpy.ndarray: Array of sampled points.
    """
    # Sample points from the mesh surface
    points, _ = mesh.sample(density)
    return points

def visualize_point_cloud(points):
    """
    Visualize a point cloud with red dots.
    
    Parameters:
        points (numpy.ndarray): Array of points to visualize.
    """
    # Create an Open3D point cloud object
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    # Set point color to red
    colors = np.asarray(pcd.points)
    pcd.colors = o3d.utility.Vector3dVector(np.ones_like(colors) * [1, 0, 0])
    
    # Visualize the point cloud
    o3d.visualization.draw_geometries([pcd], window_name='Point Cloud Visualization')




if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-3-digits.stl'
    mesh = load_model(model_path)
    
    
    hand_drawn_image_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\images\axis-3-digits-hand-drawn.png'
    create_hand_drawn_effect(mesh, hand_drawn_image_path)













