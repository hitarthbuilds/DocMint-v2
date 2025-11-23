import streamlit as st
import os
import json
import numpy as np
import faiss

from utils.pdf_reader import extract_text_from_pdf
from ai.embeddings import embed_text_batch

UPLOAD_DIR = "data/uploads"
CHUNKS_DIR = "data/chunks"

# -----------------------------
# Ensure directories exist
# -----------------------------
def ensure_dirs():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(CHUNKS_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# -----------------------------
# Chunking logic
# -----------------------------
def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# -----------------------------
# Save embeddings + FAISS index
# -----------------------------
def build_faiss_index(chunks, filename):
    embeddings = embed_text_batch(chunks)

    # FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    index_path = os.path.join(CHUNKS_DIR, f"{filename}.index")
    faiss.write_index(index, index_path)

    meta = {
        "document": filename,
        "chunks": chunks
    }

    meta_path = os.path.join(CHUNKS_DIR, f"{filename}_chunks.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return index_path, meta_path

# -----------------------------
# UI
# -----------------------------
st.title("📁 Upload & Process PDFs")
st.write("Upload a PDF to extract text, chunk it, embed it, and build a searchable index.")

ensure_dirs()

uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

if uploaded_file:
    st.success(f"Uploaded: **{uploaded_file.name}**")
    file_path = save_uploaded_file(uploaded_file)
    base_name = os.path.splitext(uploaded_file.name)[0]

    st.info(f"Saved to `{file_path}`")

    with st.spinner("Extracting text..."):
        text = extract_text_from_pdf(file_path)

    if not text.strip():
        st.error("Failed to extract text.")
        st.stop()

    st.success("Text extraction complete!")

    # Preview
    st.text_area("Preview (first 2000 chars)", text[:2000], height=300)

    # Process button
    if st.button("⚙️ Process into searchable format"):
        with st.spinner("Chunking text..."):
            chunks = chunk_text(text)

        with st.spinner("Embedding chunks..."):
            index_path, meta_path = build_faiss_index(chunks, base_name)

        st.success("Processing complete! 🎉")
        st.write(f"Index saved to: `{index_path}`")
        st.write(f"Chunk metadata saved to: `{meta_path}`")

        st.info("You can now go to the **Chat** page and ask questions about this document.")
