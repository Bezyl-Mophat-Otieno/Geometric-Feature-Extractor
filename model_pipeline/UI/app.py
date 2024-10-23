import sys
import os
import streamlit as st
import tempfile
import open3d as o3d

# Update the system path to import your local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from load_view_model import load_and_display_model

# Streamlit App
st.set_page_config(page_title="3D Model Viewer", layout="wide")

# Sidebar for navigation
st.sidebar.title("CAD FEATURE EXTRACTION")
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
    st.write("This section will allow users to extract features from the uploaded STL file.")
    # Placeholder for feature extraction functionality
    st.info("Feature Extraction functionality will be implemented here.")

elif selection == "Feature Analysis":
    st.header("Feature Analysis")
    st.write("This section will allow users to analyze extracted features.")
    # Placeholder for feature analysis functionality
    st.info("Feature Analysis functionality will be implemented here.")

elif selection == "Feature Visualization":
    st.header("Feature Visualization")
    st.write("This section will allow users to visualize features extracted from the model.")
    # Placeholder for feature visualization functionality
    st.info("Feature Visualization functionality will be implemented here.")
