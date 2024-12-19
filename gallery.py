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

# Path for the selected album
album_path = Path(IMAGE_DIR) / selected_album
album_path.mkdir(parents=True, exist_ok=True)  # Ensure the album folder exists
image_files = list(album_path.glob("*.jpg")) + list(album_path.glob("*.png"))

# Session state for tracking clicked image
if "clicked_image" not in st.session_state:
    st.session_state.clicked_image = None

# Display Images in the Selected Album
if image_files:
    cols = st.columns(3)  # Arrange images in a grid with 3 columns
    for i, img_path in enumerate(image_files):
        with cols[i % 3]:  # Dynamically place images in columns
            img = Image.open(img_path)
            # Make the image itself clickable
            if st.button(f"Click here to open {img_path.stem} ", ###Make Below Block standard responsive app 
            # Display Full View
