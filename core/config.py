import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file automatically
load_dotenv()

def load_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in environment.")
    return api_key

def get_client():
    return OpenAI(api_key=load_api_key())
