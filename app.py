import streamlit as st
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.title("📁 WiFi File Share (Streamlit Version)")

# Upload section
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded: {uploaded_file.name}")

# File list
st.subheader("📂 Available Files")

files = os.listdir(UPLOAD_FOLDER)

if files:
    for file in files:
        with open(os.path.join(UPLOAD_FOLDER, file), "rb") as f:
            st.download_button(
                label=f"Download {file}",
                data=f,
                file_name=file
            )
else:
    st.info("No files uploaded yet")