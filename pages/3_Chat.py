import os
import json
import base64

import streamlit as st
import streamlit.components.v1 as components

from core.config import get_openai_client
from ai.rag import retrieve_relevant_chunks, load_index_and_chunks
from ai.embeddings import CHUNKS_DIR

UPLOAD_DIR = "data/uploads"


# ---------- Helpers ----------

def list_indexed_documents():
    """Return list of doc names that have chunk metadata."""
    if not os.path.exists(CHUNKS_DIR):
        return []

    docs = set()
    for fname in os.listdir(CHUNKS_DIR):
        if fname.endswith("_chunks.json"):
            meta_path = os.path.join(CHUNKS_DIR, fname)
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    doc_name = meta.get("doc_name")
                    if doc_name:
                        docs.add(doc_name)
            except Exception:
                continue

    return sorted(docs)


def render_pdf_preview(doc_name: str):
    """Show an inline PDF viewer for the given document, if it exists."""
    pdf_path = os.path.join(UPLOAD_DIR, doc_name)

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


# ---------- Page UI ----------

st.title("💬 Chat with Your Documents")
st.write("Ask questions about any PDF you’ve already processed in DocMint.")

docs = list_indexed_documents()

if not docs:
    st.info("No processed documents found. Go to **Documents** and upload + process a PDF first.")
    st.stop()

# Document selector
selected_doc = st.selectbox("Select a document", docs)

# Make sure index & chunks exist for this doc
try:
    index, chunks = load_index_and_chunks(selected_doc)
except Exception:
    st.error("No valid index found for this document. Re-process it from the Documents page.")
    st.stop()

# Initialise chat history per document
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if selected_doc not in st.session_state.chat_history:
    st.session_state.chat_history[selected_doc] = []

# Layout: chat (left) + preview (right)
chat_col, preview_col = st.columns([2, 1])

with chat_col:
    st.subheader("Conversation")

    # Show previous messages
    for role, msg in st.session_state.chat_history[selected_doc]:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(msg)

    # Input at bottom
    user_query = st.chat_input("Ask something about this document...")

    if user_query:
        # Append user message
        st.session_state.chat_history[selected_doc].append(("user", user_query))

        # Retrieve relevant chunks
        with st.spinner("Retrieving relevant context from your document..."):
            retrieved = retrieve_relevant_chunks(selected_doc, user_query, top_k=5)
            context_text = "\n\n".join([c[0] for c in retrieved])

        # Build prompt
        prompt = f"""
You are DocMint, an AI assistant. Answer the user's question ONLY using the context below.
If the answer is not present, say: "I could not find this in your document."

CONTEXT:
{context_text}

QUESTION:
{user_query}
"""

        client = get_openai_client()

        with st.spinner("Generating answer..."):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are DocMint, a helpful assistant for understanding PDFs."},
                    {"role": "user", "content": prompt},
                ],
            )
            answer = resp.choices[0].message.content

        # Append assistant message
        st.session_state.chat_history[selected_doc].append(("assistant", answer))

        # Re-render chat immediately
        st.rerun()

with preview_col:
    render_pdf_preview(selected_doc)
