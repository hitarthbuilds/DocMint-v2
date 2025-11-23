import os
from openai import OpenAI

def load_api_key():
    """Return OpenAI API key from environment variable."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("Missing OPENAI_API_KEY in environment.")
    return key


def get_openai_client():
    """Return an OpenAI client instance."""
    api_key = load_api_key()
    return OpenAI(api_key=api_key)
