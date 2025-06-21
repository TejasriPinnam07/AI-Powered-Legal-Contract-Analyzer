# Legal Contract Analyzer
A complete web-based tool to automate the extraction, classification, and summarization of clauses in legal contracts using Natural Language Processing (NLP).

# Overview
This project leverages:

SpaCy for clause-level Named Entity Recognition (NER)

Legal-BERT embeddings for clause classification (standard / important / risky)

TextRank algorithm for extractive summarization

Streamlit for building an interactive user interface

It supports PDF/DOCX/TXT contracts and provides:
✅ Clause parsing
✅ Entity extraction
✅ Risk classification
✅ Summary generation
✅ Downloadable results with filters
# Project Structure
legal-contract-analyzer/

 app/
 
   main.py                 # Main application entry point

   auth.py                 # User authentication system
   
   utils/                  # Core processing modules
   
     document_parser.py  # File parsing and text extraction
     
     summarizer.py       # Text summarization functionality
     
     classifier.py       # Clause classification
     
     ner_model.py        # Named entity recognition
     
   components/             # UI components
   
     contract_display.py # Analysis results presentation
     
     header.py           # Application header
     
     footer.py           # Application footer
     
     sidebar.py          # Navigation sidebar
     
   models/                 # Machine learning models
   
     logreg_model.pkl    # Trained classifier model
     
assets/                     # Static resources

     logo.png                # Application logo
     
    login_bg.jpg            # Background image
    
    style.css               # Custom styles
# Installation Steps
git clone https://github.com/TejasriPinnam07/AI-Powered-Legal-Contract-Analyzer
cd legal-contract-analyzer
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
# Run the App Locally
streamlit run app/main.py
