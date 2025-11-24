# pages/2_Documents.py

import os
import time

import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from ai.rag import build_faiss_index_for_chunks
from ai.embeddings import CHUNKS_DIR  # just to ensure directory structure exists

UPLOAD_DIR = "data/uploads"


# ---------- helpers ----------

def ensure_dirs():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(CHUNKS_DIR, exist_ok=True)


def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150):
    """
    Simple character-based chunking.
    Larger chunks = fewer embeddings = faster on weak machines.
    """
    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


# ---------- page UI ----------

st.title("📁 Upload & Process PDFs")
st.write(
    "Upload a PDF, extract text, chunk it, embed it with a local model, "
    "and build a searchable index. No API calls, fully local."
)

ensure_dirs()

uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

if "last_processed_doc" not in st.session_state:
    st.session_state.last_processed_doc = None

if uploaded_file:
    st.success(f"Uploaded: **{uploaded_file.name}**")

    file_path = save_uploaded_file(uploaded_file)
    base_name = os.path.splitext(uploaded_file.name)[0]

    st.caption(f"Saved to: `{file_path}`")

    # Only extract text ONCE per upload
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(file_path)

    if not text or not text.strip():
        st.error("Failed to extract text from this PDF.")
        st.stop()

    st.success("Text extraction complete.")

    with st.expander("🔍 Preview extracted text (first 2000 characters)", expanded=False):
        st.text_area(
            "Text preview",
            text[:2000],
            height=260,
        )

    st.markdown("---")

    process_clicked = st.button("⚙️ Process into searchable format")

    if process_clicked:
        # status block gives user feedback without freezing totally
        with st.status("Chunking & indexing document...", expanded=True) as status:
            status.write("Step 1/3 – Splitting document into chunks...")
            start_time = time.time()
            chunks = chunk_text(text)
            status.write(f"→ Created {len(chunks)} chunks.")
            time.sleep(0.1)

            status.write("Step 2/3 – Computing embeddings locally (this is the heavy part)...")
            # build_faiss_index_for_chunks calls embed_text_batch internally
            index_path, meta_path = build_faiss_index_for_chunks(
                chunks=chunks,
                doc_id=base_name,
                file_name=uploaded_file.name,
            )
            time.sleep(0.1)

            status.write("Step 3/3 – Saving index & metadata...")
            elapsed = time.time() - start_time

            st.session_state.last_processed_doc = base_name
            status.update(
                label=f"Done in {elapsed:0.1f} seconds ✅",
                state="complete",
            )

        st.success("Document processed successfully! 🎉")
        st.write(f"FAISS index saved to: `{index_path}`")
        st.write(f"Chunk metadata saved to: `{meta_path}`")
        st.info(
            "You can now switch to the **Chat** page and start asking questions "
            "about this document."
        )

else:
    st.info("Upload a PDF file above to begin.")
