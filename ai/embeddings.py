# ai/embeddings.py

from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Directory where we store FAISS index + chunk metadata
CHUNKS_DIR = "data/chunks"

# Load a small, fast embedding model (free, local)
# This one is solid for semantic search.
_EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_embed_model = SentenceTransformer(_EMBED_MODEL_NAME)


def embed_text_batch(text_list):
    """
    Embed a list of strings into dense vectors using a local model.
    Returns a numpy array of shape (n, d) with dtype float32.
    """
    if not isinstance(text_list, list):
        text_list = [text_list]

    embeddings = _embed_model.encode(text_list, batch_size=32, show_progress_bar=False)
    return np.asarray(embeddings, dtype="float32")
