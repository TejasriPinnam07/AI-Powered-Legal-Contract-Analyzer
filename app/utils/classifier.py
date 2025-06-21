import joblib
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np

# Load model and tokenizer at module level
MODEL_PATH = "app/models/logreg_model.pkl"
BERT_MODEL = "nlpaueb/legal-bert-base-uncased"

# Load models once when module is imported
try:
    classifier = joblib.load(MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL)
    bert_model = AutoModel.from_pretrained(BERT_MODEL)
except Exception as e:
    raise ImportError(f"Failed to load models: {str(e)}")

def get_embedding(text):
    """Generate BERT embedding for a single text"""
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def classify_clauses(text):
    """
    Classify a single clause or list of clauses
    Returns: Dictionary with only 'type' key (removed 'risk')
    """
    if isinstance(text, str):
        embeddings = get_embedding(text)
        prediction = classifier.predict([embeddings])[0]
    elif isinstance(text, list):
        embeddings = np.array([get_embedding(t) for t in text])
        prediction = classifier.predict(embeddings)[0]
    else:
        raise ValueError("Input must be string or list of strings")

    type_map = {0: "Standard", 1: "Important", 2: "Risky"}
    return {"type": type_map.get(prediction, "Unknown")}

if __name__ == "__main__":
    # Test classification
    test_clause = "This Agreement shall be governed by the laws of the State of California."
    print(classify_clauses(test_clause))
