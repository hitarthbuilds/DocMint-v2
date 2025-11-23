import os
import json
import numpy as np
import faiss

from ai.embeddings import embed_text_batch, CHUNKS_DIR


def load_index_and_chunks(doc_name):
    """Load FAISS index + chunk metadata for a document."""
    index_path = os.path.join(CHUNKS_DIR, f"{doc_name}.index")
    meta_path = os.path.join(CHUNKS_DIR, f"{doc_name}_chunks.json")

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found for {doc_name}")

    if not os.path.exists(meta_path):
        raise FileNotFoundError("Chunk metadata missing.")

    index = faiss.read_index(index_path)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    chunks = meta["chunks"]
    return index, chunks


def retrieve_relevant_chunks(doc_name, query, top_k=5):
    """Return the most relevant chunks for a given query."""
    index, chunks = load_index_and_chunks(doc_name)

    query_vec = embed_text_batch([query])[0].reshape(1, -1)

    scores, ids = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0:
            continue
        results.append((chunks[idx], float(score)))

    return results
