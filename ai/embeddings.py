import os
import json
import numpy as np
from openai import OpenAI

CHUNKS_DIR = "data/chunks"

def load_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("Missing OPENAI_API_KEY in environment.")
    return key


def get_client():
    return OpenAI(api_key=load_api_key())


def embed_text_batch(texts, model="text-embedding-3-small"):
    client = get_client()
    resp = client.embeddings.create(model=model, input=texts)
    vectors = [item.embedding for item in resp.data]
    return np.array(vectors, dtype=np.float32)
