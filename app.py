import streamlit as st
import os
from datetime import datetime, timedelta
from PIL import Image
import qrcode

# ------------------ CONFIG ------------------
UPLOAD_FOLDER = "uploads"
QR_FOLDER = "qr_codes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

AUTO_DELETE_HOURS = 24

st.set_page_config(page_title="Premium File Share", layout="wide")
st.title("🚀 Premium File Sharing Tool")
st.markdown("Drag & drop files, share via QR code, auto-delete in 24h!")

# ------------------ FUNCTIONS ------------------
def cleanup_files():
    now = datetime.now()
    for f in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, f)
        if datetime.fromtimestamp(os.path.getctime(path)) + timedelta(hours=AUTO_DELETE_HOURS) < now:
            os.remove(path)
    for q in os.listdir(QR_FOLDER):
        path = os.path.join(QR_FOLDER, q)
        if datetime.fromtimestamp(os.path.getctime(path)) + timedelta(hours=AUTO_DELETE_HOURS) < now:
            os.remove(path)

def generate_qr(file_path, file_name):
    url = f"http://{st.runtime.scriptrunner.server_address}:{st.runtime.scriptrunner.server_port}/?download={file_name}"
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(QR_FOLDER, f"{file_name}.png")
    img.save(qr_path)
    return qr_path

# ------------------ AUTO CLEAN ------------------
cleanup_files()

# ------------------ FILE UPLOAD ------------------
uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)
if uploaded_files:
    for file in uploaded_files:
        with open(os.path.join(UPLOAD_FOLDER, file.name), "wb") as f:
            f.write(file.getbuffer())
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")

# ------------------ FILE LIST ------------------
st.subheader("Available Files")
files = os.listdir(UPLOAD_FOLDER)
if files:
    for f in files:
        path = os.path.join(UPLOAD_FOLDER, f)
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            # Preview for images
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                st.image(path, width=120)
            elif f.lower().endswith(('.mp4', '.mov', '.avi')):
                st.video(path)
            else:
                st.write(f)
        with col2:
            with open(path, "rb") as file:
                st.download_button("⬇ Download", file, file_name=f)
        with col3:
            if st.button(f"❌ Delete {f}"):
                os.remove(path)
                st.experimental_rerun()
        # QR Code
        qr_path = generate_qr(path, f)
        st.image(qr_path, caption="Scan to download", width=120)
else:
    st.info("No files uploaded yet.")

# ------------------ BULK DELETE ------------------
if st.button("🗑️ Delete All Files"):
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    st.experimental_rerun()
