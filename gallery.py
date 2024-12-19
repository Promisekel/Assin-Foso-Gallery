import streamlit as st
from pathlib import Path
from PIL import Image

# Mock Data
USER_PROFILE = {
    "name": "Amelia Rice",
    "photo_count": 2390,
    "albums": ["Christmas Party 2024", "Summer 2015", "Aspen 2015", "Croatia 2015"],
    "categories": ["Photos", "Videos", "Projects"]
}


# File Structure for Images
IMAGE_DIR = "images/"  # Folder to store image albums
LOGO_PATH = "assets/logo.png"  # Path to your logo

# Sidebar: User Profile and Navigation
st.sidebar.title("Photo Gallery")
if Path(LOGO_PATH).is_file():
    st.sidebar.image(LOGO_PATH, width=150, caption=USER_PROFILE["name"])
else:
    st.sidebar.write("Logo not found. Please upload 'logo.png' to the assets folder.")

st.sidebar.title("Categories")
for category in USER_PROFILE["categories"]:
    st.sidebar.write(f"- {category}")

st.sidebar.title("Albums")
selected_album = st.sidebar.selectbox("Select Album", USER_PROFILE["albums"])

# Main Section: Album Photos
st.title(f"Album: {selected_album}")
st.write(f"Displaying images from the **{selected_album}** album")
album_path = Path(IMAGE_DIR) / selected_album
album_path.mkdir(parents=True, exist_ok=True)  # Ensure the album folder exists
image_files = list(album_path.glob("*.jpg")) + list(album_path.glob("*.png"))

if image_files:
    st.write(f"Total Photos: {len(image_files)}")
    # Image Gallery
    cols = st.columns(3)  # Arrange images in a grid with 3 columns
    for i, img_path in enumerate(image_files):
        img = Image.open(img_path)
        with cols[i % 3]:  # Dynamically place images in columns
            if st.button(f"View {img_path.stem}", key=f"btn-{i}"):
                st.session_state.current_image_index = i
else:
    st.write("No images found in this album. Upload new photos below.")
    st.stop()  # Stop execution if no images are available

# Full Image Viewer with Next and Previous Buttons
if "current_image_index" not in st.session_state:
    st.session_state.current_image_index = 0

current_index = st.session_state.current_image_index

if current_index < len(image_files):  # Ensure the index is within range
    current_image = image_files[current_index]

    # Display the full image
    st.image(Image.open(current_image), use_column_width=True, caption=current_image.stem)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if current_index > 0:
            if st.button("Previous"):
                st.session_state.current_image_index -= 1
    with col2:
        st.write("")  # Spacer
    with col3:
        if current_index < len(image_files) - 1:
            if st.button("Next"):
                st.session_state.current_image_index += 1

    # Close button
    if st.button("Close"):
        st.session_state.current_image_index = None
else:
    st.error("Error: The current image index is out of range.")

# Upload Section
st.sidebar.title("Upload New Photos")
uploaded_files = st.sidebar.file_uploader(
    "Upload photos", type=["jpg", "png"], accept_multiple_files=True
)
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Save each uploaded file to the appropriate album
        save_path = album_path / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.sidebar.success("Uploaded photos successfully!")

    # Refresh the image list to include newly uploaded images
    image_files = list(album_path.glob("*.jpg")) + list(album_path.glob("*.png"))
    st.experimental_rerun()  # Reload the app to reflect the new images in the gallery

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Built with ❤️ using Streamlit")
