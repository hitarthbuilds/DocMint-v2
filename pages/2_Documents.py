import streamlit as st
import os
from utils.pdf_reader import extract_text_from_pdf

UPLOAD_DIR = "data/uploads"

def ensure_upload_dir():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# PAGE
st.title("📁 Upload Documents")

st.write("Upload your PDF files to process them inside DocMint.")

ensure_upload_dir()

uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    # Save to local storage
    file_path = save_uploaded_file(uploaded_file)
    st.info(f"Saved to: `{file_path}`")

    # Extract text
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(file_path)

    if text.strip():
        st.success("Text extraction complete!")
        st.text_area("Extracted Text Preview", text[:2000], height=300)
    else:
        st.error("Failed to extract text from this PDF.")
