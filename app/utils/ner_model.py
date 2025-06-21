# ner_model.py
import spacy

# Load trained SpaCy model
nlp = spacy.load("output/model-best")

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

if __name__ == "__main__":
    examples = [
        "This Agreement shall be governed by the laws of California.",
        "This Agreement is effective as of January 1, 2022.",
        "The term of this agreement shall expire on December 31, 2026.",
        "Either party may terminate this agreement at any time with thirty (30) days prior written notice.",
        "This agreement shall automatically renew for successive one-year terms unless either party gives notice.",
        "Each party agrees to keep the terms of this agreement strictly confidential.",
        "The Licensee shall not engage in any competing business for a period of two years.",
        "The Supplier agrees to provide the Products exclusively to the Distributor in the region.",
        "The Company reserves the right to audit the financial records of the Partner annually.",
        "No third-party beneficiary rights are intended or created by this Agreement."
    ]

    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}: {example}")
        print("Entities:", extract_entities(example))
