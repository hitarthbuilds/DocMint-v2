# core/config.py

import os
from dotenv import load_dotenv

# Absolute path (Codespaces sometimes shifts working dirs)
ENV_PATH = "/workspaces/DocMint-v2/.env"

print("[CONFIG] Loading .env from:", ENV_PATH)

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
    print("[CONFIG] .env loaded successfully.")
else:
    print("[CONFIG] .env file NOT FOUND at:", ENV_PATH)


def get_openai_key():
    key = os.getenv("OPENAI_API_KEY")
    print("[CONFIG] READ OPENAI_API_KEY:", key[:10] + "..." if key else None)

    if not key:
        raise ValueError(
            "OPENAI_API_KEY missing in environment. Expected at: " + ENV_PATH
        )
    return key
