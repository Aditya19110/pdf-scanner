from onnxruntime import InferenceSession
from transformers import AutoTokenizer
import numpy as np
import os
from pathlib import Path

os.environ["TRANSFORMERS_OFFLINE"] = "1"

def load_model_components():
    """Load tokenizer and ONNX model with error handling."""
    try:
        tokenizer_path = Path("model/tokenizer")
        model_path = Path("model/model.onnx")
        if not tokenizer_path.exists():
            raise FileNotFoundError(f"Tokenizer not found at {tokenizer_path}")
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")
        tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path))
        session = InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
        return tokenizer, session
    except Exception as e:
        print(f"Error loading model components: {e}")
        raise

tokenizer, session = load_model_components()

def get_embedding(text: str):
    """Generate text embedding using the loaded ONNX model."""
    try:
        tokens = tokenizer(
            text,
            return_tensors="np",
            truncation=True,
            max_length=32,
            padding="max_length"
        )
        ort_inputs = {
            "input_ids": tokens["input_ids"],
            "attention_mask": tokens["attention_mask"]
        }
        if "token_type_ids" in tokens:
            ort_inputs["token_type_ids"] = tokens["token_type_ids"]
        ort_outs = session.run(None, ort_inputs)
        embedding = np.mean(ort_outs[0], axis=1)[0]
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
            
        return embedding
        
    except Exception as e:
        print(f"Error generating embedding for text '{text[:50]}...': {e}")
        return np.zeros(768)  