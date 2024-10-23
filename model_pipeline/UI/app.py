import streamlit as st
import tempfile
import os

from ..load_view_model import load_and_display_model
# Streamlit App
st.title("3D Model Viewer")

# Upload file section
st.write("Upload your STL file:")
uploaded_file = st.file_uploader("Choose a STL file", type="stl")

if uploaded_file is not None:
    # Create a temporary file to store the uploaded STL file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    
    # Load and display the model
    st.write("Displaying the uploaded 3D model:")
    mesh = load_and_display_model(temp_file_path)

    # Optionally, you can display some basic info about the mesh
    if mesh:
        st.write(f"Number of vertices: {len(mesh.vertices)}")
        st.write(f"Number of triangles: {len(mesh.triangles)}")
        
    # Clean up the temporary file after visualization
    os.remove(temp_file_path)
else:
    st.info("Please upload an STL file to visualize.")