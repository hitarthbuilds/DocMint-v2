# pages/2_Documents.py

import streamlit as st
import os

from utils.pdf_reader import extract_text_from_pdf
from ai.rag import build_faiss_index_for_chunks

UPLOAD_DIR = "data/uploads"


def ensure_dirs():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs("data/chunks", exist_ok=True)


def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


st.title("📁 Upload & Process PDFs")
st.write("Upload a PDF, extract text, chunk it, and build a local searchable index. No APIs used.")

ensure_dirs()

uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

if uploaded_file:
    st.success(f"Uploaded: **{uploaded_file.name}**")
    file_path = save_uploaded_file(uploaded_file)
    base_name = os.path.splitext(uploaded_file.name)[0]

    st.info(f"Saved to `{file_path}`")

    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(file_path)

    if not text.strip():
        st.error("Failed to extract text from this PDF.")
        st.stop()

    st.success("Text extraction complete!")
    st.text_area("Preview (first 2000 characters)", text[:2000], height=300)

    if st.button("⚙️ Process into searchable format"):
        with st.spinner("Chunking & indexing..."):
            chunks = chunk_text(text)
            index_path, meta_path = build_faiss_index_for_chunks(
                chunks=chunks,
                doc_id=base_name,
                file_name=uploaded_file.name,
            )

        st.success("Processing complete! 🎉")
        st.write(f"Index saved to: `{index_path}`")
        st.write(f"Metadata saved to: `{meta_path}`")
        st.info("You can now go to the **Chat** page and start asking questions.")
