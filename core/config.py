import os
from dotenv import load_dotenv
from openai import OpenAI

# ============================
# FORCE .env LOADING ABSOLUTELY
# ============================

# Absolute root directory of your project:
ROOT_DIR = "/workspaces/DocMint-v2"

# Absolute path to your .env
ENV_PATH = os.path.join(ROOT_DIR, ".env")

# Load .env explicitly from this path
load_dotenv(dotenv_path=ENV_PATH)

def load_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(f"OPENAI_API_KEY missing. Tried loading from {ENV_PATH}")
    return api_key

def get_client():
    return OpenAI(api_key=load_api_key())
