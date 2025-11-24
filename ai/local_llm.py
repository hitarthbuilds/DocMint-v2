# ai/local_llm.py

import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

@st.cache_resource  # load ONCE, not on rerun
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="cpu",
        torch_dtype=torch.float32,
        load_in_8bit=True  # 8-bit quantization = MUCH faster/smaller
    )
    return tokenizer, model


tokenizer, model = load_model()


def generate_answer(context, question, max_new_tokens=200):

    prompt = f"""Answer based ONLY on the context below.

Context:
{context}

Question:
{question}

If answer not found in the context, say:
"I could not find this in your document."

Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        temperature=0.2,
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "Answer:" in text:
        return text.split("Answer:", 1)[-1].strip()

    return text.strip()
