import numpy as np
import trimesh
import open3d as o3d

def create_point_cloud_from_mesh(mesh, density=10000):
    """
    Create a point cloud from a mesh by sampling points from its surface using trimesh.
    
    Parameters:
        mesh (trimesh.Trimesh): The input mesh.
        density (int): Number of points to sample from the mesh surface.
        
    Returns:
        numpy.ndarray: Array of sampled points.
    """
    # Sample points from the mesh surface using trimesh
    points = mesh.sample(density)
    return points

def visualize_point_cloud(points, image_path):
    """
    Visualize a point cloud with red dots using Open3D and save the visualization as an image.
    
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
    print(f"Point cloud visualization saved to {image_path}")
    
    # Run the visualizer and save the image
    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    # Load the mesh
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\axis-3-digits.stl'
    image_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\images\axis-3-digits-point-cloud.png'
    # Load the mesh
    mesh = trimesh.load(model_path)

    # Create a point cloud from the mesh
    point_cloud = create_point_cloud_from_mesh(mesh, density=10000)
    visualize_point_cloud(point_cloud,image_path)
