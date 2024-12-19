import streamlit as st
import os
from PIL import Image

# Directory to store uploaded images
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper function to list all images in the directory
def list_images():
    return [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

# Initialize session state for navigation
if "image_index" not in st.session_state:
    st.session_state.image_index = 0

# Title
st.title("Image Gallery App")

# Upload images
uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(os.path.join(UPLOAD_DIR, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
    st.success("Images uploaded successfully!")

# Get the list of images
images = list_images()

if images:
    # Display current image
    current_image = images[st.session_state.image_index]
    image_path = os.path.join(UPLOAD_DIR, current_image)
    image = Image.open(image_path)
    st.image(image, caption=current_image, use_column_width=True)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous"):
            st.session_state.image_index = (st.session_state.image_index - 1) % len(images)
    with col2:
        st.download_button("Download", data=open(image_path, "rb"), file_name=current_image)
    with col3:
        if st.button("Next"):
            st.session_state.image_index = (st.session_state.image_index + 1) % len(images)
else:
    st.info("No images uploaded yet. Use the uploader above to add images.")
