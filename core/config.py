import os
from dotenv import load_dotenv

# Load .env file explicitly
load_dotenv(dotenv_path="/workspaces/DocMint-v2/.env")

def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY missing from environment.")
    return key
