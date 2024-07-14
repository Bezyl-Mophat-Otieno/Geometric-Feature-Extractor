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

if __name__ == "__main__":
    # Load the extracted features from the JSON file
    extracted_features_path = r'C:\Users\BezylMophatOtieno\source\repos\FreeCAD-models\combination-lock\model-pipeline\output\extracted_features.json'
    with open(extracted_features_path, 'r') as json_file:
        features = json.load(json_file)

    vertices = np.array(features['vertices'])
    faces = np.array(features['faces'])
    curvatures = np.array(features['curvatures']) # Replace with actual curvatures

    # Analyze features
    feature_df = analyze_features(vertices, faces, curvatures)

    # Print feature statistics
    print("Feature Statistics:")
    print(feature_df)

    # Save feature statistics
    output_directory = "output"  # You can change this to your desired output directory
    save_features(feature_df, output_directory)
