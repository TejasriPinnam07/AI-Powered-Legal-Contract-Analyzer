import os
import pdfplumber
import docx2txt
import re
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')

def clean_text(text):
    """Enhanced text cleaning"""
    # Remove HTML tags
    text = re.sub(r'<\/?[a-z][^>]*>', '', text)
    # Remove confidential markers
    text = re.sub(r'\*?Confidential treatment requested\*?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\w+\s+Confidential', '', text)
    # Standardize redactions
    text = re.sub(r'\[\s*\*\s*\]', '[REDACTED]', text)
    # Clean artifacts
    text = re.sub(r'\n\s*-\s*\d+\s*-\s*', '\n', text)  # Page numbers
    text = re.sub(r'\x0c', '\n', text)  # Form feeds
    # Normalize whitespace
    text = re.sub(r'[ ]{2,}', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def parse_document(file_path):
    """Handle file parsing with better error checking"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        if file_path.lower().endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif file_path.lower().endswith('.docx'):
            return docx2txt.process(file_path)
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise Exception(f"Error parsing {file_path}: {str(e)}")

def parse_pdf(file_path):
    """Robust PDF parser with improved text extraction"""
    full_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Improved text extraction with layout preservation
                text = page.extract_text(
                    x_tolerance=1,
                    y_tolerance=1,
                    layout=False,  # Change to True if dealing with complex layouts
                    keep_blank_chars=False
                )
                if text:
                    full_text += text + "\n"
                    
        # Fallback if no text extracted (try with layout=True)
        if not full_text.strip():
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text(layout=True)
                    if text:
                        full_text += text + "\n"
                        
        if not full_text.strip():
            raise ValueError("No text could be extracted from PDF")
            
        return full_text
    except Exception as e:
        raise Exception(f"PDF parsing error: {str(e)}")

def parse_docx(file_path):
    """DOCX parser with error handling"""
    try:
        text = docx2txt.process(file_path)
        if not text.strip():
            raise ValueError("Empty document content")
        return text
    except Exception as e:
        raise Exception(f"DOCX parsing error: {str(e)}")

def parse_txt(file_path):
    """TXT parser with encoding detection"""
    try:
        # Try common encodings
        encodings = ['utf-8', 'latin-1', 'windows-1252']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    text = f.read()
                    if text.strip():
                        return text
            except UnicodeDecodeError:
                continue
        raise ValueError("Could not decode text file with common encodings")
    except Exception as e:
        raise Exception(f"TXT parsing error: {str(e)}")

def split_into_clauses(text):
    """Improved clause splitting for legal documents"""
    # First split by major sections
    sections = re.split(r'(\n\d+\.\d+\s+.+?\n)', text)
    
    clauses = []
    current_section = ""
    
    for part in sections:
        if re.match(r'\n\d+\.\d+\s+.+?\n', part):
            current_section = part.strip()
        else:
            # Split into sentences but keep context
            sentences = sent_tokenize(part)
            for sentence in sentences:
                if is_valid_clause(sentence):
                    clause = f"{current_section}: {sentence}" if current_section else sentence
                    clauses.append(clause.strip())
    
    return merge_split_clauses([c for c in clauses if is_valid_clause(c)])

def is_valid_clause(text):
    """Determine if text is a complete clause"""
    text = text.strip()
    if not text:
        return False
    if len(text.split()) < 4:
        return False
    if re.match(r'^[-\d\s]+$', text):
        return False
    if re.match(r'^\d+\.\d+$', text):
        return False
    return True

def merge_split_clauses(clauses):
    """Combine clauses that were incorrectly split"""
    merged = []
    buffer = ""
    
    for clause in clauses:
        # If clause ends with connector or is short, buffer it
        if clause.endswith((':', ';', ',')) or len(clause.split()) < 8:
            buffer += " " + clause
        else:
            if buffer:
                merged.append(buffer.strip())
                buffer = ""
            merged.append(clause)
    
    if buffer:
        merged.append(buffer.strip())
    
    return [c for c in merged if is_valid_clause(c)]