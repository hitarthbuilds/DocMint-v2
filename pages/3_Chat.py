# pages/3_Chat.py

import os
import json
import base64

import streamlit as st
import streamlit.components.v1 as components

from ai.rag import retrieve_relevant_chunks, load_index_and_metadata
from ai.embeddings import CHUNKS_DIR
from ai.local_llm import generate_answer

UPLOAD_DIR = "data/uploads"


def list_processed_docs():
    """List available processed documents based on *_chunks.json files."""
    if not os.path.exists(CHUNKS_DIR):
        return []

    docs = []
    for fname in os.listdir(CHUNKS_DIR):
        if fname.endswith("_chunks.json"):
            path = os.path.join(CHUNKS_DIR, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                docs.append(
                    {
                        "doc_id": meta["doc_id"],
                        "file_name": meta["file_name"],
                        "meta_path": path,
                    }
                )
            except Exception:
                continue

    # sort by file name for consistency
    docs.sort(key=lambda d: d["file_name"])
    return docs


def render_pdf_preview(file_name: str):
    """Inline PDF viewer for the selected document."""
    pdf_path = os.path.join(UPLOAD_DIR, file_name)

    st.subheader("📄 Document Preview")

    if not os.path.exists(pdf_path):
        st.info("Original PDF not found in uploads.")
        return

    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        pdf_html = f"""
        <iframe
            src="data:application/pdf;base64,{b64_pdf}"
            width="100%"
            height="700px"
            style="border:none;"
            type="application/pdf">
        </iframe>
        """
        components.html(pdf_html, height=700, scrolling=True)
    except Exception as e:
        st.error(f"Could not render PDF preview: {e}")


# ---- UI ----

st.title("💬 Chat with Your Documents (Local, Free)")
st.write("No OpenAI, no API keys, everything runs locally.")

docs = list_processed_docs()

if not docs:
    st.info("No processed documents found. Go to **Documents** and process a PDF first.")
    st.stop()

# Map doc label → doc_id
label_to_doc = {f"{d['file_name']} (id: {d['doc_id']})": d for d in docs}

selected_label = st.selectbox("Select a document to chat with:", list(label_to_doc.keys()))
selected_doc = label_to_doc[selected_label]
doc_id = selected_doc["doc_id"]
file_name = selected_doc["file_name"]

# Load metadata to ensure index exists
try:
    _, meta = load_index_and_metadata(doc_id)
except Exception as e:
    st.error(f"Index/metadata error for this document: {e}")
    st.stop()

# per-document chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if doc_id not in st.session_state.chat_history:
    st.session_state.chat_history[doc_id] = []

chat_col, preview_col = st.columns([2, 1])

with chat_col:
    st.subheader("Conversation")

    # Past messages
    for role, msg in st.session_state.chat_history[doc_id]:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(msg)

    # New message
    user_input = st.chat_input("Ask something about this document...")

    if user_input:
        # add user msg
        st.session_state.chat_history[doc_id].append(("user", user_input))

        with st.spinner("Retrieving relevant chunks..."):
            retrieved, meta = retrieve_relevant_chunks(doc_id, user_input, top_k=5)
            context_text = "\n\n".join([c[0] for c in retrieved]) if retrieved else ""

        with st.spinner("Generating answer (local model)..."):
            answer = generate_answer(context_text, user_input)

        st.session_state.chat_history[doc_id].append(("assistant", answer))

        st.rerun()

with preview_col:
    render_pdf_preview(file_name)
