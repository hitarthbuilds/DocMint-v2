import os
from dotenv import load_dotenv

# Force-load .env file
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)

def get_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("DEBUG: .env path =", dotenv_path)
        print("DEBUG: ENV CONTENTS =", open(dotenv_path).read())
        print("DEBUG: os.environ =", dict(os.environ))
        raise ValueError("OPENAI_API_KEY is missing.")
    return key
