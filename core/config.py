# core/config.py
import os

ENV_PATH = "/workspaces/DocMint-v2/.env"

def get_openai_api_key():
    """
    ALWAYS returns the OpenAI API Key.
    Tries env var first. If missing, manually reads .env.
    This ignores Streamlit sandbox issues completely.
    """

    key = os.getenv("OPENAI_API_KEY")

    # If Streamlit didn't load env vars, force-read .env
    if not key:
        try:
            if os.path.exists(ENV_PATH):
                with open(ENV_PATH, "r") as f:
                    for line in f:
                        if line.startswith("OPENAI_API_KEY="):
                            key = line.strip().split("=", 1)[1]
                            os.environ["OPENAI_API_KEY"] = key
                            break
        except Exception as e:
            print("ERROR reading .env:", e)

    if not key:
        raise ValueError("OPENAI_API_KEY NOT FOUND. Add it to your .env.")

    return key


def get_openai_client():
    """
    Returns OpenAI client using the loaded API key.
    """

    from openai import OpenAI
    return OpenAI(api_key=get_openai_api_key())
