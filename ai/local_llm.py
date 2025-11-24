# ai/local_llm.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Small-ish instruction-tuned model. Good enough for Q&A.
_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

_tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
_model = AutoModelForCausalLM.from_pretrained(
    _MODEL_NAME,
    torch_dtype=torch.float32,
    device_map="cpu"
)


def generate_answer(context: str, question: str, max_new_tokens: int = 256) -> str:
    """
    Generate an answer based on given context + question using a local LLM.
    Completely free, runs on CPU (slower than OpenAI, but no quota).
    """

    prompt = f"""You are DocMint, an assistant that answers strictly from the given context.

Context:
{context}

Question:
{question}

If the answer cannot be found in the context, say exactly:
"I could not find this in your document."

Answer:
"""

    inputs = _tokenizer(prompt, return_tensors="pt")
    outputs = _model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.2,
        do_sample=False,
    )

    full_text = _tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Naive post-processing: return only text after "Answer:"
    if "Answer:" in full_text:
        return full_text.split("Answer:", 1)[-1].strip()
    return full_text.strip()
