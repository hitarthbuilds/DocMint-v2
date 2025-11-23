# ai/embeddings.py

from sentence_transformers import SentenceTransformer

# Load the free local embedding model ONCE
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text_batch(text_list):
    """
    Embeds a list of text chunks using a free local model.
    Returns a list of vector embeddings.
    """

    if not isinstance(text_list, list):
        text_list = [text_list]

    # SentenceTransformers returns numpy arrays → convert to python lists
    embeddings = model.encode(text_list)
    return embeddings.tolist()
