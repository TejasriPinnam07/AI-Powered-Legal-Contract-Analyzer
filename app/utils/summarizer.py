import re
from sumy.parsers.plaintext import PlaintextParser 
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer


def clean_summary_text(text: str) -> str:
    """Clean and refine the summary text for readability"""
    text = re.sub(r'(\[REDACTED\]\s*){2,}', '[REDACTED]', text)
    text = re.sub(r'(Confidential|PROPRIETARY)\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[\s*REDACTED\s*\]', '[REDACTED]', text)
    text = text.strip()

    # Add final period if missing
    if text and not text.endswith('.'):
        text += '.'
    return text


def enhance_sentences(sentences: list[str]) -> str:
    """Join sentences smoothly to make it feel like a natural summary"""
    if not sentences:
        return ""

    # Add intro sentence
    output = ["This summary outlines the key points of the document:"]
    for s in sentences:
        s = s.strip()
        if not s.endswith('.'):
            s += '.'
        output.append(s)

    return " ".join(output)


def generate_summary(text: str, sentence_count: int = 5) -> str:
    """
    Generate a short, clean summary of a contract using TextRank.
    Returns a natural-language paragraph summary.
    """
    # Pre-clean
    text = re.sub(r'\[\s*\*\s*\]', '[REDACTED]', text)

    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        summary_sentences = [str(s) for s in summarizer(parser.document, sentence_count)]

        # Enhance and clean
        joined_summary = enhance_sentences(summary_sentences)
        return clean_summary_text(joined_summary)

    except Exception as e:
        return f"Summary unavailable due to an error: {str(e)}"
