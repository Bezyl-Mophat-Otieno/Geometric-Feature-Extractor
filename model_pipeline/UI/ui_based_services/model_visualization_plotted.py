import streamlit as st
import numpy as np
import trimesh
import open3d as o3d
import tempfile  # To create a temporary file

def create_point_cloud_from_mesh(mesh, density=10000):
    """
    Create a point cloud from a mesh by sampling points from its surface using trimesh.
    
    Parameters:
        mesh (trimesh.Trimesh): The input mesh.
        density (int): Number of points to sample from the mesh surface.
        
    Returns:
        numpy.ndarray: Array of sampled points.
    """
    points = mesh.sample(density)
    return points

def visualize_point_cloud(points):
    """
    Visualize a point cloud with red dots using Open3D.
    
    Parameters:
        points (numpy.ndarray): Array of points to visualize.
    """
    # Create an Open3D point cloud object
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    # Set point color to red
    colors = np.asarray(pcd.points)
    pcd.colors = o3d.utility.Vector3dVector(np.ones_like(colors) * [1, 0, 0])
    
    # Visualize the point cloud in Open3D
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    
    # Set the point size
    render_option = vis.get_render_option()
    render_option.point_size = 5
    
    # Render the point cloud
    vis.poll_events()
    vis.update_renderer()
    
    # Display the point cloud in the Open3D window
    vis.run()
    vis.destroy_window()

def save_point_cloud_visualization(points, image_path):
    """
    Save a point cloud visualization as an image using Open3D.
    
    Parameters:
        points (numpy.ndarray): Array of points to visualize.
        image_path (str): Path to save the image.
    """
    # Create an Open3D point cloud object
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    # Set point color to red
    colors = np.asarray(pcd.points)
    pcd.colors = o3d.utility.Vector3dVector(np.ones_like(colors) * [1, 0, 0])
    
    # Create the visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    
    # Set the point size
    render_option = vis.get_render_option()
    render_option.point_size = 5
    
    # Capture the screenshot
    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image(image_path)
    vis.destroy_window()
    print(f"Point cloud visualization saved to {image_path}")