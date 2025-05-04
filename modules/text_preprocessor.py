# modules/text_preprocessor.py

import spacy
from spacy.cli import download

try:
    # Try loading the model
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model is missing, download it
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text)
    chunks = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 20]
    return chunks