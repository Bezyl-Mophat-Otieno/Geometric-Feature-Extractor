import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.colors import Normalize, LinearSegmentedColormap
import json
import os
import streamlit as st
import tempfile
import open3d as o3d
from ui_based_services.load_view_model import load_and_display_model
from ui_based_services.feature_extraction import process_mesh_features
from ui_based_services.feature_analysis import analyze_features
from ui_based_services.shape_classification import (
    refine_shapes,visualize_mesh, shape_statistics_table,
)
from ui_based_services.feature_visualizations import (
    visualize_curvature_distribution, load_features, visualize_mesh_with_curvature,
)
from ui_based_services.model_visualization_plotted import (
    visualize_point_cloud, create_point_cloud_from_mesh,
)

from ui_based_services.model_visualization_annotated import (
    load_mesh, visualize_mesh_with_annotations
)

from ui_based_services.model_visualization_sketched import (
    load_model, create_hand_drawn_effect
)
# Streamlit App
st.set_page_config(page_title="3D Model Viewer", layout="wide")

# Sidebar for navigation
st.sidebar.title("CAD FEATURE EXTRACTION")
main_section = st.sidebar.radio("Select Section", ["Model Viewer & Feature Extraction", "Geometric Analysis"])

if main_section == "Model Viewer & Feature Extraction":
    selection = st.sidebar.radio("Go to", ["Open3D Viewer", "Feature Extraction", "Feature Analysis", "Feature Visualization"])

    if selection == "Open3D Viewer":
        # Main area for visualizations and interactions
        st.header("3D Model Viewer")

        uploaded_file = st.file_uploader("Choose a STL file", type="stl")

        if uploaded_file is not None:
            # Create a temporary file to store the uploaded STL file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            mesh = load_and_display_model(temp_file_path)

            # Optionally, display some basic info about the mesh
            if mesh:
                # Display the mesh interactively
                st.write("Displaying the uploaded 3D model:")
                features_df = pd.DataFrame({
                "Number of Vertices": [len(mesh.vertices)],
                "Number of Triangles": [len(mesh.triangles)],
                })
                st.table(features_df)
                if st.button("Open 3D Viewer"):
                    # Open 3D visualizer window
                    o3d.visualization.draw_geometries([mesh], window_name="3D Model Viewer", width=800, height=600, left=50, top=50)
                st.write(f"Number of vertices: {len(mesh.vertices)}")
                st.write(f"Number of triangles: {len(mesh.triangles)}")
            else:
                st.error("Failed to load the model. Please check the file format.")

            # Clean up the temporary file after visualization
            os.remove(temp_file_path)
        else:
            st.info("Please upload an STL file to visualize.")

    elif selection == "Feature Extraction":
        st.header("Feature Extraction")
        st.write("This section allows you to extract geometric features from the uploaded STL file.")
        
        uploaded_file = st.file_uploader("Upload your STL file for feature extraction", type="stl")

        if uploaded_file is not None:
            # Create a temporary file to store the uploaded STL file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            # Process the mesh to extract features
            features = process_mesh_features(temp_file_path)

            # Display features in a table
            st.subheader("Extracted Features")
            
            # Convert features to a DataFrame for easier display
            features_df = pd.DataFrame({
                "vertices": [len(features["vertices"])],
                "faces": [len(features["faces"])],
                "edges": [len(features["edges"])],
                "curvatures": [np.mean(features["curvatures"])]
            })

            st.table(features_df)

            # Place download buttons side by side
            col1, col2 = st.columns(2)

            with col1:
                # Create a downloadable CSV button
                csv = features_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download aggregated features as CSV",
                    data=csv,
                    file_name='extracted_features(CSV).csv',
                    mime='text/csv'
                )
            
            with col2:
                # Convert the 'features' dictionary to a JSON format and make it downloadable
                features_json = json.dumps(features, indent=4).encode('utf-8')
                st.download_button(
                    label="Download raw features as JSON",
                    data=features_json,
                    file_name='extracted_features(JSON).json',
                    mime='application/json'
                )
            
            os.remove(temp_file_path)
        else:
            st.info("Please upload an STL file to extract features.")

    elif selection == "Feature Analysis":
        st.header("Feature Analysis")
        st.write("This section allows you to analyze the geometric features extracted from the uploaded STL file.")
        
        # Provide a way to load previously extracted features or allow a new upload
        extracted_features_path = st.file_uploader("Upload extracted features JSON", type="json")

        if extracted_features_path is not None:
            # Load the extracted features
            features = json.load(extracted_features_path)
            
            vertices = np.array(features['vertices'])
            faces = np.array(features['faces'])
            curvatures = np.array(features['curvatures'])
            
            # Analyze features
            feature_df = analyze_features(vertices, faces, curvatures)

            # Display statistics in a table
            st.subheader("Feature Statistics")
            st.table(feature_df)

            # Create downloadable files
            csv = feature_df.to_csv(index=False).encode('utf-8')
            json_data = feature_df.to_json(orient="records", indent=4).encode('utf-8')
            # Place download buttons side by side
            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="Download statistics as CSV",
                    data=csv,
                    file_name='feature_statistics(CSV).csv',
                    mime='text/csv'
                )

            with col2:
                st.download_button(
                    label="Download statistics as JSON",
                    data=json_data,
                    file_name='feature_statistics(JSON).json',
                    mime='application/json'
                )

    elif selection == "Feature Visualization":      
        st.header("Feature Visualization")
        st.write("Visualize and analyze the geometric features extracted from the model.")

        # File uploader for STL and JSON feature files
        uploaded_mesh_file = st.file_uploader("Upload the STL file for mesh visualization", type="stl")
        uploaded_feature_file = st.file_uploader("Upload the JSON file for extracted features", type="json")

        if uploaded_mesh_file is not None and uploaded_feature_file is not None:
            # Create temporary files for STL and JSON
            with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as temp_stl_file:
                temp_stl_file.write(uploaded_mesh_file.read())
                stl_file_path = temp_stl_file.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_json_file:
                temp_json_file.write(uploaded_feature_file.read())
                json_file_path = temp_json_file.name

            # Load extracted features from JSON
            features = load_features(json_file_path)

            # Extract curvatures from features
            curvatures = np.array(features['curvatures'])

            # Visualize curvature distribution as a histogram
            st.subheader("Curvature Distribution")
            curvature_fig = visualize_curvature_distribution(curvatures)
            st.pyplot(curvature_fig)

            # Create a download button for the curvature histogram
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_hist_file:
                curvature_fig.savefig(temp_hist_file.name)
                st.download_button(
                    label="Download Curvature Histogram as PNG",
                    data=open(temp_hist_file.name, 'rb').read(),
                    file_name="curvature_histogram.png",
                    mime="image/png"
                )
            
            # Visualize the 3D mesh with curvature values
            st.subheader("Mesh with Curvature Visualization")
            mesh = visualize_mesh_with_curvature(stl_file_path, curvatures)
            
            # Display mesh using trimesh in Streamlit (can use trimesh viewer, though external window)
            if st.button("Open 3D Mesh Viewer"):
                trimesh.Scene([mesh]).show()
            
        else:
            st.info("Please upload both an STL file and a JSON file containing extracted features to proceed with visualization.")

elif main_section == "Geometric Analysis":
    # New section for Geometric Analysis
    st.sidebar.title("Geometric Analysis")
    analysis_selection = st.sidebar.radio("Choose Analysis Tool", ["Shape Classification", "Model Visualization - Plotted", "Model Visualization - Annotated"])

    if analysis_selection == "Shape Classification":
        st.header("Shape Classification")
        st.write("Classify the shapes in the uploaded 3D model.")
        # Proceed with implementation for shape classification
        # File uploader
        uploaded_file = st.file_uploader("Upload a 3D model file (STL format)", type=["stl"])

        

        if uploaded_file is not None:
            # Save uploaded file temporarily
            with open("temp_model.stl", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Process and classify shapes
            shapes = refine_shapes([{'faces': [i]} for i in range(len(trimesh.load("temp_model.stl").faces))], 
                                trimesh.load("temp_model.stl").vertices, trimesh.load("temp_model.stl").faces)
            
            # Display classified shapes
            st.subheader("Classified Shapes:")
            shape_type = st.selectbox("Filter by shape type", ["All", "cylinder", "square", "rectangle", "circle", "triangle"])
            
            filtered_shapes = [shape for shape in shapes if shape['shape'] == shape_type or shape_type == "All"]

            col1, col2 = st.columns(2)

            with col1:    
                # Display 3D model visualization
                if st.button("Visualize 3D Model"):
                    visualize_mesh("temp_model.stl")
            with col2:
                # Option to download the classified shapes as JSON
                output_json = json.dumps(filtered_shapes, indent=4)
                st.download_button(label="Download Filtered Classified Shapes", data=output_json, file_name="filtered_shapes.json", mime="application/json")

            # Display some statistical insights
            st.subheader("Statistical Insights")
            shape_statistics_table(shapes=shapes)

        
            st.subheader("Classified Filtered Shapes:")
            st.json(filtered_shapes)
                



    elif analysis_selection == "Model Visualization - Plotted":
        st.header("Model Visualization - Plotted")
        st.write("View the plotted representation of the model.")
        # Proceed with implementation for plotted visualization

            # Upload the STL file
        uploaded_file = st.file_uploader("Upload your STL model", type=['stl'])
        if uploaded_file is not None:
            # Create a temporary file to save the uploaded STL
            with tempfile.NamedTemporaryFile(delete=False, suffix='.stl') as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            # Load the mesh using trimesh from the saved temporary file
            mesh = trimesh.load(temp_file_path)

            point_cloud = create_point_cloud_from_mesh(mesh, density=10000)
                # Button to visualize point cloud
            if st.button("Visualize Point Cloud"):
                # Create a point cloud from the mesh

                # Visualize the point cloud
                visualize_point_cloud(point_cloud)


    elif analysis_selection == "Model Visualization - Annotated":
        st.header("Model Visualization - Annotated")
        st.write("View the annotated Model")
        # Proceed with implementation for annotated visualization
        # Upload the STL file
        uploaded_file = st.file_uploader("Upload your STL model", type=['stl'])
        if uploaded_file is not None:
            # Create a temporary file to save the uploaded STL
            with tempfile.NamedTemporaryFile(delete=False, suffix='.stl') as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name
            
            # Load the mesh using trimesh from the saved temporary file
            mesh = load_mesh(temp_file_path)

            # Button to visualize the annotated model
            if st.button("Visualize Annotated Model"):
                # Visualize the annotated mesh
                visualize_mesh_with_annotations(mesh)
