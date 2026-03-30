import streamlit as st
import os
import time
from datetime import datetime, timedelta

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- CONFIG ----------
EXPIRY_HOURS = 24

st.set_page_config(page_title="WiFi Share", page_icon="📁", layout="centered")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}
.stButton button {
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
}
.file-card {
    padding: 12px;
    margin: 10px 0;
    border-radius: 10px;
    background: #1e293b;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("⚡ WiFi File Share")
st.caption("Fast • Simple • Auto-clean")

# ---------- AUTO DELETE OLD FILES ----------
def cleanup_files():
    now = datetime.now()
    for file in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, file)
        created_time = datetime.fromtimestamp(os.path.getctime(path))
        if now - created_time > timedelta(hours=EXPIRY_HOURS):
            os.remove(path)

cleanup_files()

# ---------- UPLOAD ----------
st.subheader("📤 Upload File")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file:
    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Uploaded: {uploaded_file.name}")

# ---------- FILE LIST ----------
st.subheader("📂 Available Files")

files = os.listdir(UPLOAD_FOLDER)

if files:
    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file)
        
        created_time = datetime.fromtimestamp(os.path.getctime(path))
        expiry_time = created_time + timedelta(hours=EXPIRY_HOURS)
        remaining = expiry_time - datetime.now()

        col1, col2, col3 = st.columns([4, 2, 1])

        with col1:
            st.markdown(f"**{file}**")

        with col2:
            st.caption(f"Expires in: {str(remaining).split('.')[0]}")

        with col3:
            # DELETE BUTTON
            if st.button("❌", key=file):
                os.remove(path)
                st.rerun()

        # DOWNLOAD BUTTON
        with open(path, "rb") as f:
            st.download_button(
                label="⬇ Download",
                data=f,
                file_name=file,
                key="dl_" + file
            )

else:
    st.info("No files uploaded yet")
