import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.linear_model import LogisticRegression
import joblib  # For saving/loading models

# Load BERT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")

# Load trained classifier
clf = joblib.load("logreg_model.pkl")  # Saved classifier from training

# Label map
label_map = {0: "standard", 1: "important", 2: "risky"}

def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def predict_clause(clause):
    embedding = get_embedding(clause)
    prediction = clf.predict([embedding])[0]
    return label_map[prediction]

# Example
if __name__ == "__main__":
    clause = input("Enter a clause: ")
    label = predict_clause(clause)
    print(f"\n📄 Clause Type: {label.upper()}")
