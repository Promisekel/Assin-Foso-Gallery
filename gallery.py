import streamlit as st
from pathlib import Path
import os
from PIL import Image

# Mock Data
USER_PROFILE = {
    "name": "Amelia Rice",
    "photo_count": 2390,
    "albums": ["Aspen 2015", "Croatia 2015"],
    "categories": ["Photos", "Videos", "Projects"]
}

# File Structure for Images
IMAGE_DIR = "images/"  # Place your images here (e.g., images/album_name)

# App Layout
st.sidebar.image("logo.jpg", width=150, caption=USER_PROFILE["name"])  # Replace with user's profile picture
st.sidebar.title("Categories")
for category in USER_PROFILE["categories"]:
    st.sidebar.write(f"- {category}")

st.sidebar.title("Albums")
selected_album = st.sidebar.selectbox("Select Album", USER_PROFILE["albums"])

st.title(f"Album: {selected_album}")
st.write(f"{USER_PROFILE['photo_count']} files")

# Display Images from Selected Album
album_path = Path(IMAGE_DIR) / selected_album
if album_path.exists():
    image_files = list(album_path.glob("*.jpg"))
    if image_files:
        for img_path in image_files:
            img = Image.open(img_path)
            st.image(img, caption=img_path.stem, use_column_width=True)
    else:
        st.write("No images found in this album.")
else:
    st.write("Album not found.")
