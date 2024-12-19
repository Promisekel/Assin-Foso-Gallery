import streamlit as st
from pathlib import Path
from PIL import Image

# Folder to store image files
IMAGE_DIR = "images/"
Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

# Function to load all images from the directory
def load_images(directory):
    return list(Path(directory).glob("*.jpg")) + list(Path(directory).glob("*.png"))

# Sidebar: Upload Section
st.sidebar.title("Upload Images")
uploaded_files = st.sidebar.file_uploader(
    "Upload images", type=["jpg", "png"], accept_multiple_files=True
)

# Save uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(Path(IMAGE_DIR) / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.sidebar.success("Images uploaded successfully!")
    st.experimental_rerun()  # Refresh the app to load new images

# Load all images
image_files = load_images(IMAGE_DIR)

# Main Section: Gallery Display
if image_files:
    # State to keep track of the selected image
    if "selected_image_index" not in st.session_state:
        st.session_state.selected_image_index = 0

    # Display the selected image in a large view
    selected_image = Image.open(image_files[st.session_state.selected_image_index])
    st.image(selected_image, use_column_width=True)

    # Navigation: Scrollable Thumbnail Gallery
    st.markdown(
        """
        <style>
        .thumbnail-container {
            display: flex;
            overflow-x: auto;
            padding: 10px;
            gap: 10px;
        }
        .thumbnail {
            flex-shrink: 0;
            width: 100px;
            height: 100px;
            cursor: pointer;
            object-fit: cover;
            border: 2px solid transparent;
        }
        .thumbnail:hover {
            border-color: #4CAF50;
        }
        .thumbnail.selected {
            border-color: #FF5722;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display thumbnails
    thumbnails_html = '<div class="thumbnail-container">'
    for i, img_path in enumerate(image_files):
        img_url = img_path.as_posix()
        selected_class = "selected" if i == st.session_state.selected_image_index else ""
        thumbnails_html += f"""
        <img
            src="{img_url}" class="thumbnail {selected_class}"
            onclick="window.location.href='?selected={i}'"
        />
        """
    thumbnails_html += "</div>"
    st.markdown(thumbnails_html, unsafe_allow_html=True)

    # JavaScript to handle thumbnail click
    st.markdown(
        """
        <script>
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const selected = urlParams.get('selected');
        if (selected) {
            document.body.onload = () => {
                window.parent.postMessage({'streamlit:setQueryParams': {selected: selected}}, '*');
            };
        }
        </script>
        """,
        unsafe_allow_html=True,
    )

else:
    st.write("No images uploaded yet. Use the sidebar to upload images.")

# Footer
st.markdown("---")
st.write("Built with ❤️ using Streamlit")
