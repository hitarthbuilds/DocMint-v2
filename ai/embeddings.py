# ai/embeddings.py

import os
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

# Where FAISS index + metadata live (used by rag.py)
CHUNKS_DIR = "data/chunks"


@lru_cache(maxsize=1)
def get_embed_model():
    """
    Load a SMALL, fast, local embedding model exactly once.
    'paraphrase-MiniLM-L3-v2' is tiny and good enough for RAG.
    """
    model_name = "sentence-transformers/paraphrase-MiniLM-L3-v2"
    return SentenceTransformer(model_name)


def embed_text_batch(text_list):
    """
    Embed a list of text chunks into dense vectors (float32 numpy array).

    Parameters
    ----------
    text_list : list[str] | str
        Single string or list of strings.

    Returns
    -------
    np.ndarray
        Shape (n, d) float32 embeddings.
    """
    if not isinstance(text_list, list):
        text_list = [text_list]

    model = get_embed_model()

    # batch_size kept modest for weak CPUs (Codespaces, etc.)
    embeddings = model.encode(
        text_list,
        batch_size=16,
        show_progress_bar=False,
        convert_to_numpy=True,
    )

    return embeddings.astype("float32")
