# ai/rag.py

import os
import json
import numpy as np
import faiss

from ai.embeddings import embed_text_batch, CHUNKS_DIR


def build_faiss_index_for_chunks(chunks, doc_id: str, file_name: str):
    """
    Given text chunks and a doc_id, build and save FAISS index + metadata.
    doc_id is usually the base filename without .pdf.
    """

    os.makedirs(CHUNKS_DIR, exist_ok=True)

    # 1. Embed all chunks
    vectors = embed_text_batch(chunks)  # shape (n, d)
    n, d = vectors.shape

    # 2. Build FAISS index
    index = faiss.IndexFlatL2(d)
    index.add(vectors)

    index_path = os.path.join(CHUNKS_DIR, f"{doc_id}.index")
    faiss.write_index(index, index_path)

    # 3. Save metadata (chunks + mapping to original file)
    meta = {
        "doc_id": doc_id,
        "file_name": file_name,
        "chunks": chunks,
    }

    meta_path = os.path.join(CHUNKS_DIR, f"{doc_id}_chunks.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return index_path, meta_path


def load_index_and_metadata(doc_id: str):
    """
    Load FAISS index + metadata for a given doc_id.
    """

    index_path = os.path.join(CHUNKS_DIR, f"{doc_id}.index")
    meta_path = os.path.join(CHUNKS_DIR, f"{doc_id}_chunks.json")

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found for doc_id={doc_id}")
    if not os.path.exists(meta_path):
        raise FileNotFoundError(f"Chunk metadata not found for doc_id={doc_id}")

    index = faiss.read_index(index_path)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    return index, meta


def retrieve_relevant_chunks(doc_id: str, question: str, top_k: int = 5):
    """
    Given a doc_id and a question, return top_k (chunk_text, score) pairs.
    """

    index, meta = load_index_and_metadata(doc_id)
    chunks = meta["chunks"]

    # Embed question
    q_vec = embed_text_batch([question])  # shape (1, d)
    scores, ids = index.search(q_vec, top_k)

    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0 or idx >= len(chunks):
            continue
        results.append((chunks[idx], float(score)))

    return results, meta
