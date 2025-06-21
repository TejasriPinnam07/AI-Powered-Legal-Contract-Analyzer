# apply_ner_to_clauses.py
import os
import json
import spacy

# Load trained model
nlp = spacy.load("output/model-best")

# Input and output folders
input_dir = "parsed_output"
output_dir = "week3_result"
os.makedirs(output_dir, exist_ok=True)

# Apply NER to clauses
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        with open(input_path, "r", encoding="utf-8") as infile:
            data = json.load(infile)

        results = []
        for clause_text in data.get("clauses", []):
            doc = nlp(clause_text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            results.append({
                "clause": clause_text,
                "entities": entities
            })

        output_data = {
            "source": data.get("source", filename),
            "results": results
        }

        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(output_data, outfile, indent=2)

print(f"NER applied. Outputs saved to '{output_dir}'")
