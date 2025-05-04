# modules/text_preprocessor.py

import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")
    
def preprocess_text(text):
    doc = nlp(text)
    chunks = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 20]
    return chunks