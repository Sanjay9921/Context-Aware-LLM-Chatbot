# modules/text_preprocessor.py

import spacy
import subprocess
import sys

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")
    
def preprocess_text(text):
    doc = nlp(text)
    chunks = [(ent.text, ent.label_) for ent in doc.ents]
    return chunks