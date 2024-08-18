# 3D Model Shape Extraction and Visualization

## Overview

This project involves extracting and identifying shapes from a 3D CAD model. The script processes the 3D mesh, projects it onto 2D planes, detects various geometric shapes (e.g., triangles, rectangles, squares, circles), and visualizes these shapes on the original 3D model. The identified shapes and their properties are saved to a JSON file for further analysis.

## Features

- **Shape Detection**: Identifies various shapes including triangles, rectangles, squares, and circles from the 3D model.
- **Dimension Calculation**: Computes dimensions such as height, width, radius, and diameter for each detected shape.
- **Visualization**: Displays the detected shapes overlaid on the 3D model.
- **Output**: Saves the shape properties (type, area, perimeter, dimensions) to a JSON file.

## Prerequisites

- **Python 3.x**
- **Libraries**:
  - `trimesh`
  - `numpy`
  - `shapely`
  - `skimage`
  - `matplotlib`

You can install the required libraries using `pip`:

```bash
pip install trimesh numpy shapely scikit-image matplotlib
```

## Usage

1. **Prepare Your 3D Model**: Ensure your 3D model is in STL format and located at the specified path.

2. **Update File Paths**:
   - Edit the `model_path` and `output_json_path` in the script to point to your 3D model file and desired output JSON file location.

3. **Run the Script**:

   ```bash
   python shape-extraction.py
   ```

   This will process the 3D model, detect shapes, visualize them, and save the results to the specified JSON file.

## Script Explanation

- **`project_to_2d_planes(mesh)`**: Projects the 3D model onto the XY, XZ, and YZ planes.
- **`extract_contours(plane_points)`**: Extracts contours from the 2D projections using binary image processing.
- **`analyze_contours(contours)`**: Converts contours into `shapely` polygons and verifies their validity.
- **`identify_shape(shape)`**: Determines the type of shape (triangle, rectangle, square, circle) based on the number of vertices and geometric properties.
- **`calculate_dimensions(shape)`**: Computes dimensions such as side lengths, height, width, radius, and diameter.
- **`get_shape_properties(shape)`**: Gathers properties of the identified shapes.
- **`visualize_shapes_on_model(mesh, xy_shapes, xz_shapes, yz_shapes)`**: Visualizes the detected shapes on the 3D model.
- **`process_mesh(file_path, output_json)`**: Main function to process the mesh, detect shapes, save results, and visualize.

## Example Output

- **JSON File**: Contains the properties of detected shapes for each plane.

  ```json
  {
      "XY Plane": [
          {
              "type": "Rectangle",
              "area": 20.0,
              "perimeter": 18.0,
              "length": 5.0,
              "width": 4.0
          }
      ],
      "XZ Plane": [
          {
              "type": "Circle",
              "area": 28.27,
              "perimeter": 18.84,
              "radius": 3.0,
              "diameter": 6.0
          }
      ],
      "YZ Plane": [
          {
              "type": "Triangle",
              "area": 10.0,
              "perimeter": 15.0,
              "side_1": 5.0,
              "side_2": 5.0,
              "side_3": 7.0,
              "height": 5.0,
              "base": 7.0
          }
      ]
  }
  ```

- **Visualization**: A 3D plot showing the 3D model with the detected shapes overlaid.

## Troubleshooting

- Ensure your 3D model file is correctly formatted and accessible.
- Verify that all required libraries are installed and up-to-date.
- Adjust the image size or scaling factors in the `extract_contours` function if you encounter boundary issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
