# feature-analysis.py analyzes geometric features extracted from a 3D mesh. The script computes statistical measures such as the number of vertices, faces, and mean curvatures of the mesh. The feature statistics are saved to CSV and JSON files for further analysis or visualization.
import numpy as np
import pandas as pd
import json
import os

def analyze_features(vertices, faces, curvatures):
    """
    Analyzes geometric features extracted from the 3D mesh.

    Parameters:
    - vertices (np.ndarray): Array of vertices.
    - faces (np.ndarray): Array of faces.
    - curvatures (np.ndarray): Mean curvatures of vertices.

    Returns:
    - feature_df (pd.DataFrame): DataFrame containing feature statistics.
    """
    # Compute statistical measures
    vertex_count = len(vertices)
    face_count = len(faces)
    curvature_mean = np.mean(curvatures)
    curvature_std = np.std(curvatures)
    curvature_min = np.min(curvatures)
    curvature_max = np.max(curvatures)

    # Prepare feature statistics
    feature_stats = {
        "vertex_count": vertex_count,
        "face_count": face_count,
        "curvature_mean": curvature_mean,
        "curvature_std": curvature_std,
        "curvature_min": curvature_min,
        "curvature_max": curvature_max
    }

    # Create a DataFrame for feature statistics
    feature_df = pd.DataFrame([feature_stats])

    return feature_df

def save_features(feature_df, output_dir):
    """
    Saves feature statistics to CSV and JSON files.

    Parameters:
    - feature_df (pd.DataFrame): DataFrame containing feature statistics.
    - output_dir (str): Directory where the files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "feature_statistics.csv")
    json_path = os.path.join(output_dir, "feature_statistics.json")

    # Save to CSV
    feature_df.to_csv(csv_path, index=False)
    print(f"Feature statistics saved to {csv_path}")

    # Save to JSON
    feature_df.to_json(json_path, orient="records", indent=4)
    print(f"Feature statistics saved to {json_path}")
