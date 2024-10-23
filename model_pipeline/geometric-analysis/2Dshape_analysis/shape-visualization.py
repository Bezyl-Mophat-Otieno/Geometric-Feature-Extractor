import trimesh
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from skimage import measure
import json
import matplotlib.pyplot as plt

def project_to_2d_planes(mesh):
    vertices = mesh.vertices
    xy_plane = vertices[:, :2]
    xz_plane = vertices[:, [0, 2]]
    yz_plane = vertices[:, 1:]
    return xy_plane, xz_plane, yz_plane

def extract_contours(plane_points, img_size=1000):
    min_vals = plane_points.min(axis=0)
    max_vals = plane_points.max(axis=0)
    scale = (img_size - 1) / (max_vals - min_vals)
    offset = min_vals * scale
    scaled_points = (plane_points * scale - offset).astype(int)
    
    img = np.zeros((img_size, img_size), dtype=np.uint8)
    x, y = scaled_points.T
    valid = (x >= 0) & (x < img_size) & (y >= 0) & (y < img_size)
    img[x[valid], y[valid]] = 1

    contours = measure.find_contours(img, level=0.5)
    return contours

def analyze_contours(contours):
    shapes = []
    for contour in contours:
        if len(contour) < 3:
            continue
        poly = Polygon(contour)
        if poly.is_valid:
            shapes.append(orient(poly))
    return shapes

def identify_shape(shape):
    if shape.is_empty:
        return "No shape detected"

    exterior_coords = list(shape.exterior.coords)
    num_coords = len(exterior_coords)
    
    if num_coords == 3:
        return "Triangle"
    elif num_coords == 4:
        area = shape.area
        length = shape.length
        if abs(area - length ** 2) < 1e-5:
            return "Square"
        else:
            return "Rectangle"
    elif num_coords > 4:
        area = shape.area
        perimeter = shape.length
        if perimeter ** 2 / (4 * np.pi * area) > 0.8:
            return "Circle"
        return "Polygon"
    return "Unknown shape"

def calculate_dimensions(shape):
    dimensions = {}
    coords = np.array(shape.exterior.coords)
    
    if len(coords) == 3:
        a = np.linalg.norm(coords[0] - coords[1])
        b = np.linalg.norm(coords[1] - coords[2])
        c = np.linalg.norm(coords[2] - coords[0])
        dimensions = {
            "side_1": a,
            "side_2": b,
            "side_3": c,
            "height": min(a, b, c),
            "base": max(a, b, c)
        }
    elif len(coords) == 4:
        length = np.linalg.norm(coords[0] - coords[1])
        width = np.linalg.norm(coords[1] - coords[2])
        dimensions = {
            "length": length,
            "width": width
        }
    else:
        perimeter = shape.length
        area = shape.area
        radius = np.sqrt(area / np.pi)
        diameter = 2 * radius
        dimensions = {
            "radius": radius,
            "diameter": diameter
        }
    
    return dimensions

def get_shape_properties(shape):
    shape_type = identify_shape(shape)
    dimensions = calculate_dimensions(shape)
    return {
        "type": shape_type,
        "area": shape.area,
        "perimeter": shape.length,
        **dimensions
    }

def process_mesh(file_path, output_json):
    mesh = trimesh.load(file_path)
    xy_plane, xz_plane, yz_plane = project_to_2d_planes(mesh)

    xy_contours = extract_contours(xy_plane)
    xz_contours = extract_contours(xz_plane)
    yz_contours = extract_contours(yz_plane)

    xy_shapes = analyze_contours(xy_contours)
    xz_shapes = analyze_contours(xz_contours)
    yz_shapes = analyze_contours(yz_contours)

    features = {
        "XY Plane": [get_shape_properties(shape) for shape in xy_shapes],
        "XZ Plane": [get_shape_properties(shape) for shape in xz_shapes],
        "YZ Plane": [get_shape_properties(shape) for shape in yz_shapes]
    }

    with open(output_json, 'w') as json_file:
        json.dump(features, json_file, indent=4)

    visualize_shapes_on_model(mesh, xy_shapes, xz_shapes, yz_shapes)

def visualize_shapes_on_model(mesh, xy_shapes, xz_shapes, yz_shapes):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the mesh
    ax.plot_trisurf(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], triangles=mesh.faces, color='lightgrey', alpha=0.5)

    # Function to plot 3D shapes on the model
    def plot_shapes(shapes, z_offset=0, color='red'):
        for shape in shapes:
            coords = np.array(shape.exterior.coords)
            ax.plot(coords[:, 0], coords[:, 1], zs=z_offset, color=color, lw=2)

    # Plot the identified shapes on the 3D model
    plot_shapes(xy_shapes, z_offset=0, color='red')  # XY plane shapes
    plot_shapes(xz_shapes, z_offset=0, color='green')  # XZ plane shapes
    plot_shapes(yz_shapes, z_offset=0, color='blue')  # YZ plane shapes

    plt.show()

if __name__ == "__main__":
    model_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\STLs\custom-shared.stl'
    output_json_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\statistics\extracted_shapes.json'
    process_mesh(model_path, output_json_path)
