import streamlit as st
from PIL import Image
import os

# Directory for storing uploaded files
UPLOAD_DIR = "uploaded_images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# App title
st.set_page_config(page_title="Gallery App", layout="wide")
st.title("🌟 Beautiful Gallery App")
st.markdown("Upload and explore your pictures with an elegant gallery interface.")

# Sidebar options
st.sidebar.title("Options")
option = st.sidebar.radio("Choose an action:", ["Upload", "Gallery", "About"])

def view_full_image(image_list, start_index=0):
    """Display images in full view with navigation."""
    current_index = st.session_state.get("current_image_index", start_index)
    image_path = os.path.join(UPLOAD_DIR, image_list[current_index])
    img = Image.open(image_path)

    st.markdown("---")
    st.image(img, caption=image_list[current_index], use_container_width=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Previous", key="prev"):
            st.session_state["current_image_index"] = (current_index - 1) % len(image_list)
    with col3:
        if st.button("➡️ Next", key="next"):
            st.session_state["current_image_index"] = (current_index + 1) % len(image_list)

if option == "Upload":
    st.header("📤 Upload Your Pictures")
    uploaded_files = st.file_uploader(
        "Choose images to upload (png, jpg, jpeg)", type=["png", "jpg", "jpeg"], accept_multiple_files=True
    )
    
    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_DIR, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())
        st.success("Upload successful! Check out your gallery.")

elif option == "Gallery":
    st.header("🖼️ Your Picture Gallery")
    images = [f for f in os.listdir(UPLOAD_DIR) if f.endswith((".png", ".jpg", ".jpeg"))]
    
    if images:
        cols = st.columns(4)
        for i, image_name in enumerate(images):
            image_path = os.path.join(UPLOAD_DIR, image_name)
            img = Image.open(image_path)
            with cols[i % 4]:
                st.image(img, caption=image_name, use_container_width=True, output_format="JPEG")
                if st.button(f"View {image_name}", key=f"view_{i}"):
                    st.session_state["current_image_index"] = i
                    st.session_state["view_gallery"] = True
        
        if st.session_state.get("view_gallery"):
            view_full_image(images)
    else:
        st.info("No images found. Please upload some pictures.")

elif option == "About":
    st.header("📖 About this App")
    st.write(
        "This is a beautiful gallery app built with Streamlit. "
        "You can upload pictures, view them in a gallery format, and download them as needed."
    )
    st.markdown("---")
    st.markdown("### Features:")
    st.markdown("- Upload multiple pictures at once.")
    st.markdown("- View pictures in an elegant grid layout.")
    st.markdown("- Navigate through pictures in a detailed view with next and previous buttons.")
