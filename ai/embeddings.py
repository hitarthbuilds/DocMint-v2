# ai/embeddings.py
from core.config import get_openai_client

def embed_text_batch(chunks):
    """
    Takes a list of text chunks and returns embeddings using OpenAI.
    """

    client = get_openai_client()

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks
    )

    return [item.embedding for item in response.data]
